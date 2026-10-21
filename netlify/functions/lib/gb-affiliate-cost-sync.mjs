// Private Printify cost synchronizer. Called only from affiliate-admin after owner auth.
// Never expose this module through an unauthenticated function or the affiliate dashboard.
import {getStore} from '@netlify/blobs';
import {AFFILIATE_RATE_PRODUCTS,AFFILIATE_RATE_MEMBERS,AFFILIATE_COST_PRODUCTS} from './gb-product-catalog.mjs';
import {readPrintifyCost} from './gb-affiliate-printify-reader.mjs';
import {setCommissionRate} from './gb-affiliates.mjs';

const store=()=>getStore('gb-owner-printify-affiliate-cost-v1');
const key=name=>'cost/'+encodeURIComponent(name);
const safeError=error=>{const value=String(error?.message||'');return /^(printify_http_\d{3}|printify_product_id_mismatch|printify_provider_missing|invalid_printify_response)$/.test(value)?value:'printify_request_failed'};
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
 const start=Number(offset);if(!Number.isSafeInteger(start)||start<0||start>AFFILIATE_COST_PRODUCTS.length)return {ok:false,error:'Invalid sync offset.'};
 const n=Math.max(1,Math.min(4,Number(batchSize)||3));
 const selected=AFFILIATE_COST_PRODUCTS.slice(start,start+n);
 const rows=await Promise.all(selected.map(async name=>{
  let value;try{value=await readPrintifyCost(name,token,fetcher)}
  catch(error){value={name,status:'error',reason:safeError(error),checked_at:new Date().toISOString()}}
  await store().setJSON(key(name),value);
  return {name,status:value.status,reason:value.reason||null};
 }));
 return {ok:true,processed:rows.length,total:AFFILIATE_COST_PRODUCTS.length,next_offset:start+rows.length,done:start+rows.length>=AFFILIATE_COST_PRODUCTS.length,rows};
}
export async function applyProposedRates({offset=0,batchSize=4}={}){
 const start=Number(offset);
 if(!Number.isSafeInteger(start)||start<0||start>AFFILIATE_RATE_PRODUCTS.length)return {ok:false,error:'Invalid batch offset.'};
 // Block approval until every single physical garment has verified current costs.
 const s=store(),snapshots=await Promise.all(AFFILIATE_COST_PRODUCTS.map(name=>s.get(key(name),{type:'json'})));
 const now=Date.now();
 const unready=snapshots.filter((r,i)=>r?.name!==AFFILIATE_COST_PRODUCTS[i]||r.status!=='proposal_ready'||
  !Number.isSafeInteger(r.proposed_commission_cents)||r.proposed_commission_cents<=0||
  !Number.isFinite(Date.parse(r.checked_at))||now-Date.parse(r.checked_at)>14*86400000);
 if(unready.length)return {ok:false,error:'Every current product needs fresh verified costs and a positive proposed rate before bulk approval.',remaining:unready.length};
 const byName=new Map(snapshots.map(s=>[s.name,s]));
 const sharedRates=AFFILIATE_RATE_PRODUCTS.map(name=>({
   name,members:AFFILIATE_RATE_MEMBERS[name],
   // Use the smallest safe payout in a family so even the least profitable design is covered.
   cents:Math.min(...AFFILIATE_RATE_MEMBERS[name].map(member=>byName.get(member).proposed_commission_cents))
 }));
 const selected=sharedRates.slice(start,start+Math.max(1,Math.min(5,Number(batchSize)||4)));
 const saved=[];
 for(const r of selected){const v=await setCommissionRate(r.name,r.cents);
  if(!v.ok)return {ok:false,error:'Unable to save rate for '+r.name,saved};
  saved.push({name:r.name,cents:r.cents,members:r.members.length});}
 return {ok:true,saved,processed:saved.length,next_offset:start+saved.length,done:start+saved.length>=sharedRates.length,total:sharedRates.length};
}
