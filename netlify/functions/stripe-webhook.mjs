// Stripe webhook endpoint for Gangster Bougie.
// SECURITY: verifies Stripe's signature before accepting a payment event.
// SAFETY: does NOT create a Printify order yet.

import { buildPrintifyOrder } from './lib/printify-order-builder.mjs';
import { buildGbOrderRecord } from './lib/gb-order-record.mjs';

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
   console.log('VERIFIED PAID CHECKOUT READY',JSON.stringify({event_id:event.id,session_id:s.id,gb_order_number:order.record.order_number,payment_status:s.payment_status,amount_total:s.amount_total,currency:s.currency,line_items:built.payload.line_items.length,fulfillment_ready:true,order_record_ready:true,printify_order_created:false}));
   return Response.json({received:true,accepted:true,verified_paid:true,fulfillment_ready:true,order_record_ready:true,order_number:order.record.order_number,printify_order_created:false});
 }
 return Response.json({received:true,ignored:true,type:event.type});
};

// Branch deploy refresh after webhook secret configuration.
