import { findPrintifyOrderByExternalId } from './printify-idempotency.mjs';

// Controlled Printify submission module.
// IMPORTANT: no Netlify handler is exported, so this cannot be invoked from the public web.
// A later verified Stripe webhook may import submitPrintifyOrder only after payment verification.
const SHOP_ID='28816619';
export async function submitPrintifyOrder(payload,{allow=false}={}){
 if(!allow) return {ok:false,blocked:true,error:'printify_submission_locked'};
 if(!payload?.external_id)return {ok:false,error:'missing_external_id'};
 const prior=await findPrintifyOrderByExternalId(payload.external_id);
 if(!prior.ok)return prior;
 if(prior.exists)return {ok:true,duplicate_prevented:true,order_id:prior.order?.id||null,status:prior.order?.status||null};
 const token=process.env.PRINTIFY_API_TOKEN;
 if(!token)return {ok:false,error:'printify_not_configured'};
 const r=await fetch('https://api.printify.com/v1/shops/'+SHOP_ID+'/orders.json',{
   method:'POST',headers:{Authorization:'Bearer '+token,'Content-Type':'application/json'},body:JSON.stringify(payload)
 });
 const d=await r.json().catch(()=>({}));
 if(!r.ok)return {ok:false,error:'printify_order_failed',status:r.status,details:d};
 return {ok:true,order_id:d.id||null,status:d.status||null};
}
