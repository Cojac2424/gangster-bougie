// Read-only Printify API cost fetcher; kept independent of Netlify Blobs for testability.
// May only be called by an owner-authenticated server endpoint, never directly in the browser.
import {PRICE_CENTS,VARIABLE_PRICES} from './gb-product-catalog.mjs';
import {affiliateMappedVariants} from './fulfillment-resolver.mjs';
import {customerShippingContribution} from './gb-shipping-contribution.mjs';
import {getWorstShippingCents,planProductCommission} from './gb-affiliate-cost-math.mjs';
const SHOP_ID='28816619',ROOT='https://api.printify.com/v1';
const unitsFromPrice=name=>Math.min(PRICE_CENTS[name],...Object.values(VARIABLE_PRICES[name]||{}));
async function requestPrintify(path,token,fetcher){
 const response=await fetcher(ROOT+path,{method:'GET',headers:{Authorization:'Bearer '+token,Accept:'application/json'}});
 if(!response.ok)throw Error('printify_http_'+response.status);
 const data=await response.json();
 if(!data||typeof data!=='object')throw Error('invalid_printify_response');
 return data;
}
export async function readPrintifyCost(name,token,fetcher=fetch){
 const mapped=affiliateMappedVariants(name);
 if(!mapped.length)return {name,status:'needs_review',reason:'product_has_no_verified_mapping'};
 const products=new Map(),shipping=new Map(),variantCosts=[],shippingCosts=[];
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
    return {name,status:'needs_review',reason:'printify_variant_cost_missing',printify_product_id:id,variant_id:row.variantId};
   }
   if(variant.is_enabled===false||variant.is_available===false){
    return {name,status:'needs_review',reason:'printify_variant_not_available',printify_product_id:id,variant_id:row.variantId};
   }
   variantCosts.push({costCents:Number(variant.cost),variantId:row.variantId,option:row.option,productId:id});
  }
  const shippingInfo=getWorstShippingCents(shipping.get(shipKey)?.profiles,required.map(x=>x.variantId));
  if(!shippingInfo.ok)return {name,status:'needs_review',reason:shippingInfo.reason||'shipping_unverified',shipping_country:shippingInfo.country||null,printify_product_id:id};
  shippingCosts.push(...shippingInfo.perDestination.map(x=>({variantId:x.variantId,country:x.country,firstItemCents:x.cents,productId:id})));
 }
 const planned=planProductCommission({name,retailCents:unitsFromPrice(name),variantCosts,
  shippingByVariant:shippingCosts,customerContributionCents:customerShippingContribution(name)});
 return {...planned,printify_product_ids:[...products.keys()],checked_at:new Date().toISOString(),
  cost_source:'Printify shop product variant.cost',shipping_source:'Printify provider standard shipping profiles, US and CA',
  pricing_note:'Uses lowest retail price, highest configured variant production cost, and highest verified first-item shipping among US and CA; fee allowance is an estimate. Requires owner approval.'};
}

