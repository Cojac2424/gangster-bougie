// Gangster Bougie order-record foundation.
// Pure deterministic helpers: no database writes and no Printify submission.
// GB order number is derived from the verified Stripe Checkout Session ID so webhook retries
// always produce the same customer-facing number.

function fnv1a32(value){
 let h=0x811c9dc5;
 const s=String(value||'');
 for(let i=0;i<s.length;i++){
  h^=s.charCodeAt(i);
  h=Math.imul(h,0x01000193)>>>0;
 }
 return h>>>0;
}

export function gbOrderNumber(stripeSessionId){
 const id=String(stripeSessionId||'').trim();
 if(!id)throw new Error('stripe_session_id_required');
 // 9-digit stable numeric suffix; keeps the familiar GB-######### format.
 const n=(fnv1a32(id)%900000000)+100000000;
 return 'GB-'+String(n);
}

export function buildGbOrderRecord({stripeSession,eventId,items,printifyOrderId=null,status='confirmed'}){
 const s=stripeSession||{};
 if(!s.id) return {ok:false,error:'stripe_session_id_required'};
 if(s.payment_status!=='paid') return {ok:false,error:'payment_not_paid'};
 const details=s.customer_details||{}, shipping=s.shipping_details||{}, addr=shipping.address||details.address||{};
 const normalizedItems=(items||[]).map(x=>({
  name:String(x.name||''),
  selection:String(x.size||x.selection||''),
  quantity:Math.max(1,Math.floor(Number(x.qty||x.quantity)||1)),
  printify_product_id:x.printify_product_id?String(x.printify_product_id):null,
  printify_variant_id:x.printify_variant_id?Number(x.printify_variant_id):null
 }));
 return {ok:true,record:{
  order_number:gbOrderNumber(s.id),
  status,
  stripe_session_id:s.id,
  stripe_payment_intent:s.payment_intent||null,
  stripe_event_id:eventId||null,
  printify_order_id:printifyOrderId,
  payment_status:s.payment_status,
  currency:String(s.currency||'usd').toUpperCase(),
  amount_total:Number.isFinite(Number(s.amount_total))?Number(s.amount_total):null,
  amount_subtotal:Number.isFinite(Number(s.amount_subtotal))?Number(s.amount_subtotal):null,
  amount_shipping:Number.isFinite(Number(s.total_details?.amount_shipping))?Number(s.total_details.amount_shipping):0,
  amount_tax:Number.isFinite(Number(s.total_details?.amount_tax))?Number(s.total_details.amount_tax):0,
  customer:{email:details.email||s.customer_email||'',name:details.name||shipping.name||'',phone:details.phone||''},
  shipping:{name:shipping.name||details.name||'',address1:addr.line1||'',address2:addr.line2||'',city:addr.city||'',region:addr.state||'',postal_code:addr.postal_code||'',country:addr.country||''},
  items:normalizedItems
 }};
}
