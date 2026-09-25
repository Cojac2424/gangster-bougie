// Stripe webhook endpoint for Gangster Bougie.
// SECURITY: verifies Stripe's signature before accepting a payment event.
// SAFETY: Printify submission is gated to verified Stripe live-mode payments and an explicit Netlify enable flag.

import { buildPrintifyOrder } from './lib/printify-order-builder.mjs';
import { buildGbOrderRecord } from './lib/gb-order-record.mjs';
import { saveGbOrder, updateGbOrderFulfillment, markGbOrderConfirmationSent } from './lib/gb-order-store.mjs';
import { submitPrintifyOrder } from './lib/printify-submit.mjs';
import { sendOrderConfirmation } from './lib/gb-email.mjs';

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
     return {name:md.storefront_name||prod.name||li.description,size:md.storefront_selection||'',qty:li.quantity||1,printify_product_id:md.printify_product_id||null,printify_variant_id:md.printify_variant_id||null};
   });
   const built=buildPrintifyOrder({items,external_id:s.id,shipping:{
     first_name:first,last_name:last,email:details.email||full.customer_email||'',phone:details.phone||'Not provided',
     country:addr.country||'',region:addr.state||'',address1:addr.line1||'',address2:addr.line2||'',city:addr.city||'',zip:addr.postal_code||''
   }});
   if(!built.ok){
     console.error('PAID CHECKOUT NEEDS REVIEW',JSON.stringify({event_id:event.id,session_id:s.id,reason:built.error,details:built}));
     return Response.json({received:true,accepted:true,verified_paid:true,fulfillment_ready:false,printify_order_created:false});
   }
   const order=buildGbOrderRecord({stripeSession:full,eventId:event.id,items});
   if(!order.ok){
     console.error('GB ORDER RECORD BUILD FAILED',JSON.stringify({event_id:event.id,session_id:s.id,error:order.error}));
     return Response.json({received:true,accepted:true,verified_paid:true,fulfillment_ready:true,order_record_ready:false,printify_order_created:false});
   }
   let saved;
   try{saved=await saveGbOrder(order.record)}
   catch(e){
     console.error('GB ORDER STORAGE FAILED',JSON.stringify({event_id:event.id,session_id:s.id,error:String(e?.message||e)}));
     return Response.json({error:'Verified payment could not be persisted.',received:true,accepted:true,verified_paid:true,fulfillment_ready:true,order_record_ready:true,order_saved:false},{status:500});
   }
   if(!saved.ok){
     console.error('GB ORDER STORAGE REJECTED',JSON.stringify({event_id:event.id,session_id:s.id,error:saved.error}));
     return Response.json({error:'Verified payment could not be persisted.',received:true,accepted:true,verified_paid:true,fulfillment_ready:true,order_record_ready:true,order_saved:false},{status:500});
   }
   // Printify auto-fulfillment is intentionally gated twice:
   // 1) only real Stripe live-mode payments can submit; sandbox/test payments never can;
   // 2) PRINTIFY_AUTO_FULFILLMENT must be explicitly set to "true" in Netlify.
   let printify={ok:true,skipped:true,reason:full.livemode?'auto_fulfillment_disabled':'stripe_sandbox'};
   const allowPrintify=full.livemode===true && String(process.env.PRINTIFY_AUTO_FULFILLMENT||'').toLowerCase()==='true';
   if(saved.created && allowPrintify){
    try{printify=await submitPrintifyOrder(built.payload,{allow:true})}catch(e){printify={ok:false,error:String(e?.message||e)}}
    if(printify.ok && printify.order_id){
     const updated=await updateGbOrderFulfillment(saved.record.order_number,{printify_order_id:printify.order_id,status:'submitted_to_printify'}).catch(()=>null);
     if(updated?.ok)saved.record=updated.record;
    }else if(!printify.ok){
     console.error('PRINTIFY SUBMISSION FAILED',JSON.stringify({event_id:event.id,session_id:s.id,order_number:saved.record.order_number,error:printify.error,status:printify.status||null}));
    }
   }
   // Retry confirmation on a later Stripe webhook delivery until a successful send is recorded.
   // This avoids losing the email when order storage succeeds but Resend temporarily fails.
   const confirmationAlreadySent=!!saved.record.confirmation_email_sent_at;
   let confirmation={ok:true,skipped:confirmationAlreadySent};
   if(!confirmationAlreadySent){
    try{confirmation=await sendOrderConfirmation(saved.record)}catch(e){confirmation={ok:false,error:String(e?.message||e)}}
    if(confirmation.ok){
     const marked=await markGbOrderConfirmationSent(saved.record.order_number).catch(()=>null);
     if(marked?.ok)saved.record=marked.record;
     else console.error('ORDER CONFIRMATION SENT BUT STATUS MARK FAILED',JSON.stringify({event_id:event.id,session_id:s.id,order_number:saved.record.order_number}));
    }else console.error('ORDER CONFIRMATION EMAIL FAILED',JSON.stringify({event_id:event.id,session_id:s.id,order_number:saved.record.order_number,error:confirmation.error,status:confirmation.status||null}));
   }
   console.log('VERIFIED PAID CHECKOUT READY',JSON.stringify({event_id:event.id,session_id:s.id,gb_order_number:saved.record.order_number,payment_status:s.payment_status,amount_total:s.amount_total,currency:s.currency,line_items:built.payload.line_items.length,fulfillment_ready:true,order_record_ready:true,order_saved:true,order_created:saved.created,confirmation_email_sent:!!(saved.record.confirmation_email_sent_at||(!confirmationAlreadySent&&confirmation.ok)),printify_order_created:!!printify.order_id,printify_order_id:printify.order_id||null,printify_submission_skipped:!!printify.skipped}));
   return Response.json({received:true,accepted:true,verified_paid:true,fulfillment_ready:true,order_record_ready:true,order_saved:true,order_number:saved.record.order_number,confirmation_email_sent:!!(saved.record.confirmation_email_sent_at||(!confirmationAlreadySent&&confirmation.ok)),printify_order_created:!!printify.order_id,printify_order_id:printify.order_id||null,printify_submission_skipped:!!printify.skipped});
 }
 return Response.json({received:true,ignored:true,type:event.type});
};

// Branch deploy refresh after webhook secret configuration.
