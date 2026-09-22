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
