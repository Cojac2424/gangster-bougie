// Persistent Gangster Bougie order storage using Netlify Blobs.
// Server-side only. Customer-facing reads must go through an authenticated/verified endpoint.
import { getStore } from '@netlify/blobs';

const STORE='gb-orders-v1';
function normalizeEmail(v){return String(v||'').trim().toLowerCase();}
function orderKey(record){return 'order/'+encodeURIComponent(record.order_number);}
function stripeKey(record){return 'stripe/'+encodeURIComponent(record.stripe_session_id);}
function emailIndexKey(email){return 'email/'+encodeURIComponent(normalizeEmail(email));}

export async function saveGbOrder(record){
 if(!record?.order_number||!record?.stripe_session_id)return {ok:false,error:'invalid_order_record'};
 const email=normalizeEmail(record.customer?.email);
 if(!email)return {ok:false,error:'customer_email_required'};
 const store=getStore(STORE);
 // Stripe session is the idempotency anchor. A retry returns the already-saved order.
 const existingNumber=await store.get(stripeKey(record),{type:'text'});
 if(existingNumber){
  const existing=await store.get('order/'+encodeURIComponent(existingNumber),{type:'json'});
  if(existing)return {ok:true,created:false,record:existing};
 }
 const now=new Date().toISOString();
 const stored={...record,customer:{...record.customer,email},created_at:record.created_at||now,updated_at:now};
 const priorIndex=await store.get(emailIndexKey(email),{type:'json'}).catch(()=>null);
 const numbers=Array.isArray(priorIndex?.order_numbers)?priorIndex.order_numbers.filter(Boolean):[];
 if(!numbers.includes(stored.order_number))numbers.unshift(stored.order_number);
 await store.setJSON(orderKey(stored),stored);
 await store.set(stripeKey(stored),stored.order_number);
 await store.setJSON(emailIndexKey(email),{email,order_numbers:numbers.slice(0,100),updated_at:now});
 return {ok:true,created:true,record:stored};
}

export async function getGbOrderByNumber(orderNumber){
 const store=getStore(STORE);
 return await store.get('order/'+encodeURIComponent(String(orderNumber||'')),{type:'json'});
}

export async function listGbOrdersByEmail(email){
 const normalized=normalizeEmail(email);
 if(!normalized)return [];
 const store=getStore(STORE);
 const idx=await store.get(emailIndexKey(normalized),{type:'json'}).catch(()=>null);
 const numbers=Array.isArray(idx?.order_numbers)?idx.order_numbers:[];
 const orders=[];
 for(const n of numbers){
  const order=await getGbOrderByNumber(n);
  if(order&&normalizeEmail(order.customer?.email)===normalized)orders.push(order);
 }
 return orders;
}

export async function updateGbOrderFulfillment(orderNumber,{printify_order_id=null,status=null}={}){
 const store=getStore(STORE);
 const current=await getGbOrderByNumber(orderNumber);
 if(!current)return {ok:false,error:'order_not_found'};
 const updated={...current,printify_order_id:printify_order_id||current.printify_order_id||null,status:status||current.status,updated_at:new Date().toISOString()};
 await store.setJSON(orderKey(updated),updated);
 return {ok:true,record:updated};
}

export async function markGbOrderConfirmationSent(orderNumber){
 const store=getStore(STORE);
 const current=await getGbOrderByNumber(orderNumber);
 if(!current)return {ok:false,error:'order_not_found'};
 const updated={...current,confirmation_email_sent_at:current.confirmation_email_sent_at||new Date().toISOString(),updated_at:new Date().toISOString()};
 await store.setJSON(orderKey(updated),updated);
 return {ok:true,record:updated};
}


export async function updateGbOrderTracking(orderNumber,{printify_order_id=null,tracking=null,tracking_email_sent_at=null}={}){
 const store=getStore(STORE), current=await getGbOrderByNumber(orderNumber);
 if(!current)return {ok:false,error:'order_not_found'};
 const existing=Array.isArray(current.tracking)?current.tracking:[];
 const next=tracking&&tracking.number?[...existing.filter(x=>String(x.number)!==String(tracking.number)),tracking]:existing;
 const already_notified=Boolean(current.tracking_email_sent_at)||Boolean(tracking&&existing.some(x=>String(x.number)===String(tracking.number)&&x.email_sent_at));
 const updated={...current,printify_order_id:printify_order_id||current.printify_order_id||null,status:'shipped',tracking:next,tracking_email_sent_at:tracking_email_sent_at||current.tracking_email_sent_at||null,updated_at:new Date().toISOString()};
 await store.setJSON(orderKey(updated),updated);
 if(updated.printify_order_id)await store.set('printify/'+encodeURIComponent(updated.printify_order_id),updated.order_number);
 return {ok:true,record:updated,already_notified};
}
