// Private Printify cost synchronizer. Called only from affiliate-admin after owner auth.
// Never expose this module through an unauthenticated function or the affiliate dashboard.
import {getStore} from '@netlify/blobs';
import {AFFILIATE_RATE_PRODUCTS,PRICE_CENTS,VARIABLE_PRICES} from './gb-product-catalog.mjs';
import {affiliateMappedVariants} from './fulfillment-resolver.mjs';
import {customerShippingContribution} from './gb-shipping-contribution.mjs';
import {getWorstShippingCents,planProductCommission} from './gb-affiliate-cost-math.mjs';
import {setCommissionRate} from './gb-affiliates.mjs';

const SHOP_ID='28816619',ROOT='https://api.printify.com/v1';
const store=()=>getStore('gb-owner-printify-affiliate-cost-v1');
const key=name=>'cost/'+encodeURIComponent(name);
const safeError=error=>{const value=String(error?.message||'');return /^(printify_http_\d{3}|printify_product_id_mismatch|printify_provider_missing|invalid_printify_response)$/.test(value)?value:'printify_request_failed'};
const unitsFromPrice=name=>Math.min(PRICE_CENTS[name],...Object.values(VARIABLE_PRICES[name]||{}));
async function requestPrintify(path,token,fetcher){
 const response=await fetcher(ROOT+path,{method:'GET',headers:{Authorization:'Bearer '+token,Accept:'application/json'}});
 if(!response.ok)throw Error('printify_http_'+response.status);
 const data=await response.json();
 if(!data||typeof data!=='object')throw Error('invalid_printify_response');
 return data;
}
async function readCost(name,token,fetcher){
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
   if(!variant||!Number.isSafeInteger(Number(variant.cost))||Number(variant.cost)<0){
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
export async function listCostSnapshots(){
 const output=[],s=store();let cursor;
 do{
  const p=await s.list({prefix:'cost/',...(cursor?{cursor}:{})});
  for(const file of p.blobs||[]){const row=await s.get(file.key,{type:'json'});if(row)output.push(row)}
  cursor=p.cursor||null;
 }while(cursor);
 return output.sort((a,b)=>a.name.localeCompare(b.name));
}
export async function syncCostBatch({offset=0,batchSize=3,fetcher=fetch}={}){
 const token=process.env.PRINTIFY_API_TOKEN;
 if(!token)return {ok:false,error:'PRINTIFY_API_TOKEN is not configured in Netlify.'};
 const start=Number(offset);if(!Number.isSafeInteger(start)||start<0||start>AFFILIATE_RATE_PRODUCTS.length)return {ok:false,error:'Invalid sync offset.'};
 const n=Math.max(1,Math.min(4,Number(batchSize)||3));
 const selected=AFFILIATE_RATE_PRODUCTS.slice(start,start+n);
 const rows=await Promise.all(selected.map(async name=>{
  let value;try{value=await readCost(name,token,fetcher)}
  catch(error){value={name,status:'error',reason:safeError(error),checked_at:new Date().toISOString()}}
  await store().setJSON(key(name),value);
  return {name,status:value.status,reason:value.reason||null};
 }));
 return {ok:true,processed:rows.length,total:AFFILIATE_RATE_PRODUCTS.length,next_offset:start+rows.length,done:start+rows.length>=AFFILIATE_RATE_PRODUCTS.length,rows};
}
export async function applyProposedRates({offset=0,batchSize=4}={}){
 const start=Number(offset);
 if(!Number.isSafeInteger(start)||start<0||start>AFFILIATE_RATE_PRODUCTS.length)return {ok:false,error:'Invalid batch offset.'};
 // Fail closed for ALL products before the first rate can be activated.
 const s=store(),rows=await Promise.all(AFFILIATE_RATE_PRODUCTS.map(name=>s.get(key(name),{type:'json'})));
 const now=Date.now();
 const unready=rows.filter((r,i)=>r?.name!==AFFILIATE_RATE_PRODUCTS[i]||r.status!=='proposal_ready'||
  !Number.isSafeInteger(r.proposed_commission_cents)||r.proposed_commission_cents<=0||
  !Number.isFinite(Date.parse(r.checked_at))||now-Date.parse(r.checked_at)>14*86400000);
 if(unready.length)return {ok:false,error:'All 52 products need fresh verified costs and positive proposed rates before bulk approval.',remaining:unready.length};
 const selected=rows.slice(start,start+Math.max(1,Math.min(5,Number(batchSize)||4)));
 const saved=[];
 for(const r of selected){const v=await setCommissionRate(r.name,r.proposed_commission_cents);
  if(!v.ok)return {ok:false,error:'Unable to save rate for '+r.name,saved};
  saved.push({name:r.name,cents:r.proposed_commission_cents});}
 return {ok:true,saved,processed:saved.length,next_offset:start+saved.length,done:start+saved.length>=rows.length,total:rows.length};
}
