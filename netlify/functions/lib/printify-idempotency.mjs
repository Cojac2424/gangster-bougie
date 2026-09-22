// Stripe/Printify idempotency helpers.
// A Stripe Checkout Session ID is the stable external_id used for Printify.
// Before creating an order, query Printify by external_id; if one exists, reuse it.
// This makes Stripe webhook retries safe even across separate serverless invocations.
const SHOP_ID='28816619';

export async function findPrintifyOrderByExternalId(externalId){
 const token=process.env.PRINTIFY_API_TOKEN;
 if(!token) return {ok:false,error:'printify_not_configured'};
 const id=String(externalId||'').trim();
 if(!id) return {ok:false,error:'missing_external_id'};
 // Printify order list is paginated. Search recent pages conservatively before any create.
 for(let page=1;page<=20;page++){
   const r=await fetch('https://api.printify.com/v1/shops/'+SHOP_ID+'/orders.json?page='+page,{headers:{Authorization:'Bearer '+token}});
   const d=await r.json().catch(()=>({}));
   if(!r.ok)return {ok:false,error:'printify_lookup_failed',status:r.status};
   const rows=Array.isArray(d.data)?d.data:(Array.isArray(d)?d:[]);
   const hit=rows.find(o=>String(o.external_id||'')===id);
   if(hit)return {ok:true,exists:true,order:hit};
   if(!d.next_page_url && rows.length<10)break;
 }
 return {ok:true,exists:false,order:null};
}
