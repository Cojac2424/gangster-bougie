// Controlled Printify submission module.
// IMPORTANT: no Netlify handler is exported, so this cannot be invoked from the public web.
// A later verified Stripe webhook may import submitPrintifyOrder only after payment verification.
const SHOP_ID='28816619';
export async function submitPrintifyOrder(payload,{allow=false}={}){
 if(!allow) return {ok:false,blocked:true,error:'printify_submission_locked'};
 const token=process.env.PRINTIFY_API_TOKEN;
 if(!token)return {ok:false,error:'printify_not_configured'};
 const r=await fetch('https://api.printify.com/v1/shops/'+SHOP_ID+'/orders.json',{
   method:'POST',headers:{Authorization:'Bearer '+token,'Content-Type':'application/json'},body:JSON.stringify(payload)
 });
 const d=await r.json().catch(()=>({}));
 if(!r.ok)return {ok:false,error:'printify_order_failed',status:r.status,details:d};
 return {ok:true,order_id:d.id||null,status:d.status||null};
}
