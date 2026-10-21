// Read-only Printify API cost fetcher; kept independent of Netlify Blobs for testability.
// May only be called by an owner-authenticated server endpoint, never directly in the browser.
import {PRICE_CENTS,VARIABLE_PRICES} from './gb-product-catalog.mjs';
import {affiliateMappedVariants} from './fulfillment-resolver.mjs';
import {customerShippingContribution} from './gb-shipping-contribution.mjs';
import {getWorstShippingCents,planProductCommission} from './gb-affiliate-cost-math.mjs';
const SHOP_ID='28816619',ROOT='https://api.printify.com/v1';
const unitsFromPrice=name=>Math.min(PRICE_CENTS[name],...Object.values(VARIABLE_PRICES[name]||{}));
// These are public, representative metro destinations for non-order shipping QUOTES only.
// A reference quote is NOT a guarantee for every US/Canadian address or a replacement
// for the shopper's own Printify quote at checkout.
const MAT_REFERENCE_DESTINATIONS=Object.freeze({
 CA:{country:'CA',region:'ON',city:'Toronto',zip:'M5H 2N2',address1:'100 Queen St W'},
 US:{country:'US',region:'NY',city:'New York',zip:'10118',address1:'350 5th Ave'}
});
async function requestMatShippingQuote(productId,variantId,country,token,fetcher){
 const reference=MAT_REFERENCE_DESTINATIONS[country];
 if(!reference)return {ok:false,reason:'country_not_supported'};
 try{
  const response=await fetcher(ROOT+'/shops/'+SHOP_ID+'/orders/shipping.json',{
   method:'POST',headers:{Authorization:'Bearer '+token,Accept:'application/json',
    'Content-Type':'application/json','User-Agent':'GangsterBougie-Affiliate-Cost-Check'},
   body:JSON.stringify({line_items:[{product_id:productId,variant_id:variantId,quantity:1}],
    address_to:{first_name:'Shipping',last_name:'Estimate',email:'shipping-quote@example.invalid',
     phone:'0000000000',...reference}})
  });
  if(!response.ok)return {ok:false,reason:'printify_quote_http_'+response.status};
  const methods=await response.json();
  if(!Number.isSafeInteger(methods?.standard)||methods.standard<0)
   return {ok:false,reason:'standard_shipping_unavailable'};
  return {ok:true,cents:methods.standard};
 }catch(_e){return {ok:false,reason:'printify_quote_request_failed'};}
}
async function requestPrintify(path,token,fetcher){
 const response=await fetcher((path.startsWith('/v2/')?'https://api.printify.com':ROOT)+path,{method:'GET',headers:{Authorization:'Bearer '+token,Accept:'application/json'}});
 if(!response.ok)throw Error('printify_http_'+response.status);
 const data=await response.json();
 if(!data||typeof data!=='object')throw Error('invalid_printify_response');
 return data;
}
export async function readPrintifyCost(name,token,fetcher=fetch){
 const mapped=affiliateMappedVariants(name);
 const review=(reason,extra={})=>({name,status:'needs_review',reason,retail_cents:unitsFromPrice(name),
  customer_shipping_contribution_cents:customerShippingContribution(name),...extra});
 if(!mapped.length)return review('product_has_no_verified_mapping');
 const products=new Map(),shipping=new Map(),v2Shipping=new Map(),variantCosts=[],shippingCosts=[];
 let usedV2Shipping=false,usedDestinationQuotes=false;
 // Fetch each underlying Printify product concurrently; colour variants may use separate product IDs.
 const productIds=[...new Set(mapped.map(x=>x.productId))];
 const fetched=await Promise.all(productIds.map(async id=>{
  const product=await requestPrintify('/shops/'+SHOP_ID+'/products/'+encodeURIComponent(id)+'.json',token,fetcher);
  if(String(product.id)!==String(id))throw Error('printify_product_id_mismatch');
  if(!Number.isSafeInteger(Number(product.blueprint_id))||!Number.isSafeInteger(Number(product.print_provider_id)))
   throw Error('printify_provider_missing');
  return [id,product];
 }));
 for(const [id,product] of fetched)products.set(id,product);
 const shippingIds=[...new Set(fetched.map(([,p])=>p.blueprint_id+'/'+p.print_provider_id))];
 const downloadedShipping=await Promise.all(shippingIds.map(async id=>{
  const [bp,provider]=id.split('/');
  const sh=await requestPrintify('/catalog/blueprints/'+bp+'/print_providers/'+provider+'/shipping.json',token,fetcher);
  return [id,sh];
 }));
 for(const [id,sh] of downloadedShipping)shipping.set(id,sh);
 for(const [id,product] of products){
  const shipKey=product.blueprint_id+'/'+product.print_provider_id;
  const required=mapped.filter(x=>x.productId===id);
  for(const row of required){
   const variant=(product.variants||[]).find(v=>Number(v.id)===row.variantId);
   if(!variant||!Number.isSafeInteger(variant.cost)||variant.cost<0){
    return review('printify_variant_cost_missing',{printify_product_id:id,variant_id:row.variantId});
   }
   if(variant.is_enabled===false||variant.is_available===false){
    return review('printify_variant_not_available',{printify_product_id:id,variant_id:row.variantId});
   }
   variantCosts.push({costCents:Number(variant.cost),variantId:row.variantId,option:row.option,productId:id});
  }
  let shippingInfo=getWorstShippingCents(shipping.get(shipKey)?.profiles,required.map(x=>x.variantId));
  // Some yoga-mat providers omit destination rates from the V1 profiles. Check Printify's
  // V2 STANDARD rate table (not economy/express) before declaring shipping unverified.
  // Never use a guessed or historical shipping price as a verified quote.
  if(!shippingInfo.ok&&name==='Foam Yoga Mat'){
   try{
    if(!v2Shipping.has(shipKey)){
     const v2=await requestPrintify('/v2/catalog/blueprints/'+product.blueprint_id+
       '/print_providers/'+product.print_provider_id+'/shipping/standard.json',token,fetcher);
     const profiles=(Array.isArray(v2.data)?v2.data:[]).map(row=>row?.attributes)
      .filter(a=>Number.isSafeInteger(a?.variantId)&&Number.isSafeInteger(a?.shippingCost?.firstItem?.amount)&&
        a.shippingCost.firstItem.amount>=0&&a.shippingCost.firstItem.currency==='USD'&&
        typeof a?.country?.code==='string'&&a.shippingType==='standard')
      .map(a=>({variant_ids:[a.variantId],countries:[a.country.code],
        first_item:{currency:'USD',cost:a.shippingCost.firstItem.amount}}));
     v2Shipping.set(shipKey,profiles);
    }
    const verified=getWorstShippingCents(v2Shipping.get(shipKey),required.map(x=>x.variantId));
    if(verified.ok){shippingInfo=verified;usedV2Shipping=true;}
   }catch(_error){/* Keep the V1 failure; shipping remains unverified. */}
  }
  // The catalog may omit a mat's shipping profile despite a valid shop variant.
  // Ask the same read-only shipping calculator used at customer checkout for two
  // representative destinations. Never create an order, invent shipping, or
  // interpret a reference city quote as a nationwide maximum.
  if(!shippingInfo.ok&&name==='Foam Yoga Mat'){
   const refRows=[];
   for(const row of required){
    const checks=await Promise.all(['US','CA'].map(country=>
     requestMatShippingQuote(id,row.variantId,country,token,fetcher)));
    for(let n=0;n<2;n++){
     const country=['US','CA'][n],quote=checks[n];
     if(!quote.ok)return review('printify_reference_'+quote.reason,{
      shipping_country:country,printify_product_id:id,variant_id:row.variantId,
      product_colour:row.option,
      production_high_cents:variantCosts.length?Math.max(...variantCosts.map(x=>x.costCents)):null,
      production_cost_note:'Shipping quote unavailable. Customer shipping and profit NOT verified.'});
     refRows.push({variantId:row.variantId,country,cents:quote.cents});
    }
   }
   shippingInfo={ok:true,perDestination:refRows};usedDestinationQuotes=true;
  }
  if(!shippingInfo.ok)return review(shippingInfo.reason||'shipping_unverified',{
   shipping_country:shippingInfo.country||null,printify_product_id:id,
   production_high_cents:variantCosts.length?Math.max(...variantCosts.map(x=>x.costCents)):null,
   production_cost_note:'Partial product costs only; shipping and margin are NOT verified'});
  shippingCosts.push(...shippingInfo.perDestination.map(x=>({variantId:x.variantId,country:x.country,firstItemCents:x.cents,productId:id})));
 }
 const planned=planProductCommission({name,retailCents:unitsFromPrice(name),variantCosts,
  shippingByVariant:shippingCosts,customerContributionCents:customerShippingContribution(name)});
 return {...planned,printify_product_ids:[...products.keys()],checked_at:new Date().toISOString(),
  cost_source:'Printify shop product variant.cost',
  shipping_source:usedDestinationQuotes?'Printify shop order shipping quotes for representative Toronto, ON and New York, NY addresses; NOT nationwide verified':
   usedV2Shipping?'Printify V2 standard shipping catalog profiles, US and CA':'Printify V1 shipping catalog profiles, US and CA',
  shipping_reference_only:usedDestinationQuotes,
  pricing_note:usedDestinationQuotes?
   'REFERENCE QUOTES ONLY: highest US/CA quote among selected metro destinations and configured mat colours. Actual customer/address shipping may differ; do not assume a nationwide maximum or approve a mat commission.':
   'Uses lowest retail price, highest configured variant production cost, and highest verified first-item catalog shipping among US and CA; fee allowance is an estimate. Requires owner approval.'};
}

