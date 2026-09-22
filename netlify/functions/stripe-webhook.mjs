// Stripe webhook endpoint for Gangster Bougie.
// SECURITY: verifies Stripe's signature before accepting a payment event.
// SAFETY: does NOT create a Printify order yet.

import { buildPrintifyOrder } from './lib/printify-order-builder.mjs';
import { submitPrintifyOrder } from './lib/printify-submit.mjs';

const enc=new TextEncoder();
function hex(bytes){return [...new Uint8Array(bytes)].map(b=>b.toString(16).padStart(2,'0')).join('');}
function constantTime(a,b){
 if(a.length!==b.length)return false;
 let x=0;for(let i=0;i<a.length;i++)x|=a.charCodeAt(i)^b.charCodeAt(i);return x===0;
}
async function hmac(secret,payload){
 const key=await crypto.subtle.importKey('raw',enc.encode(secret),{name:'HMAC',hash:'SHA-256'},false,['sign']);
 return hex(await crypto.subtle.sign('HMAC',key,enc.encode(payload)));
}
async function verify(raw,header,secret){
 const parts=String(header||'').split(',').map(x=>x.split('='));
 const t=parts.find(x=>x[0]==='t')?.[1];
 const sigs=parts.filter(x=>x[0]==='v1').map(x=>x[1]);
 if(!t||!sigs.length)return false;
 const age=Math.abs(Math.floor(Date.now()/1000)-Number(t));
 if(!Number.isFinite(age)||age>300)return false;
 const expected=await hmac(secret,t+'.'+raw);
 return sigs.some(s=>constantTime(expected,s));
}
export default async(req)=>{
 if(req.method!=='POST')return new Response('Method not allowed',{status:405,headers:{Allow:'POST'}});
 const secret=process.env.STRIPE_WEBHOOK_SECRET;
 if(!secret)return Response.json({error:'Webhook secret is not configured.'},{status:500});
 const raw=await req.text();
 if(!(await verify(raw,req.headers.get('stripe-signature'),secret)))return Response.json({error:'Invalid Stripe signature.'},{status:400});
 let event;try{event=JSON.parse(raw)}catch(_){return Response.json({error:'Invalid payload.'},{status:400})}
 if(event.type==='checkout.session.completed'){
   const s=event.data?.object||{};
   if(s.payment_status!=='paid')return Response.json({received:true,accepted:false,reason:'payment_not_paid'});
   // Fetch the authoritative paid session + line items from Stripe; never trust browser cart data here.
   const sk=process.env.STRIPE_SECRET_KEY;
   if(!sk)return Response.json({error:'Stripe API key is not configured.'},{status:500});
   const sr=await fetch('https://api.stripe.com/v1/checkout/sessions/'+encodeURIComponent(s.id)+'?expand[]=line_items.data.price.product',{headers:{Authorization:'Bearer '+sk}});
   const full=await sr.json();
   if(!sr.ok)return Response.json({error:'Unable to retrieve paid checkout.'},{status:502});
   const details=full.customer_details||{}, addr=details.address||full.shipping_details?.address||{};
   const fullName=String(details.name||full.shipping_details?.name||'').trim(), parts=fullName.split(/\\s+/), first=parts.shift()||'', last=parts.join(' ')||'-';
   const items=(full.line_items?.data||[]).map(li=>{
     const prod=li.price?.product||{}, md=prod.metadata||{};
     return {name:md.storefront_name||prod.name||li.description,size:md.storefront_selection||'',qty:li.quantity||1};
   });
   const built=buildPrintifyOrder({items,external_id:s.id,shipping:{
     first_name:first,last_name:last,email:details.email||full.customer_email||'',phone:details.phone||'Not provided',
     country:addr.country||'',region:addr.state||'',address1:addr.line1||'',address2:addr.line2||'',city:addr.city||'',zip:addr.postal_code||''
   }});
   if(!built.ok){
     console.error('PAID CHECKOUT NEEDS REVIEW',JSON.stringify({event_id:event.id,session_id:s.id,reason:built.error,details:built}));
     return Response.json({received:true,accepted:true,verified_paid:true,fulfillment_ready:false,printify_order_created:false});
   }
   // Submission is wired but remains OFF unless PRINTIFY_FULFILLMENT_ENABLED is explicitly set to "true".
   // Printify recommends Manual order approval when controlling when orders enter production.
   const enabled=String(process.env.PRINTIFY_FULFILLMENT_ENABLED||'').toLowerCase()==='true';
   if(!enabled){
     console.log('VERIFIED PAID CHECKOUT READY - PRINTIFY LOCKED',JSON.stringify({event_id:event.id,session_id:s.id,line_items:built.payload.line_items.length}));
     return Response.json({received:true,accepted:true,verified_paid:true,fulfillment_ready:true,printify_submission_locked:true,printify_order_created:false});
   }
   const submitted=await submitPrintifyOrder(built.payload,{allow:true});
   if(!submitted.ok){
     console.error('PRINTIFY SUBMISSION FAILED',JSON.stringify({event_id:event.id,session_id:s.id,error:submitted.error,status:submitted.status||null}));
     return Response.json({received:true,accepted:true,verified_paid:true,fulfillment_ready:true,printify_submission_attempted:true,printify_order_created:false,error:'printify_submission_failed'},{status:500});
   }
   console.log('PRINTIFY ORDER RESOLVED',JSON.stringify({event_id:event.id,session_id:s.id,order_id:submitted.order_id,duplicate_prevented:!!submitted.duplicate_prevented}));
   return Response.json({received:true,accepted:true,verified_paid:true,fulfillment_ready:true,printify_submission_attempted:true,printify_order_created:!submitted.duplicate_prevented,duplicate_prevented:!!submitted.duplicate_prevented,printify_order_id:submitted.order_id||null});
 }
 return Response.json({received:true,ignored:true,type:event.type});
};

// Branch deploy refresh after webhook secret configuration.
