// Secure passwordless customer access for Gangster Bougie My Orders.
// No public order lookup by email alone: access requires a short-lived email verification code.
import { getStore } from '@netlify/blobs';
import { listGbOrdersByEmail } from './lib/gb-order-store.mjs';
import { sendVerificationCode } from './lib/gb-email.mjs';

const STORE='gb-customer-auth-v1', enc=new TextEncoder();
function email(v){return String(v||'').trim().toLowerCase()}
function hex(b){return [...new Uint8Array(b)].map(x=>x.toString(16).padStart(2,'0')).join('')}
async function digest(v){return hex(await crypto.subtle.digest('SHA-256',enc.encode(String(v))))}
function token(){const b=crypto.getRandomValues(new Uint8Array(32));return [...b].map(x=>x.toString(16).padStart(2,'0')).join('')}
function code(){const a=new Uint32Array(1);crypto.getRandomValues(a);return String(100000+(a[0]%900000))}
function decodeEntities(v){return String(v??'').replace(/&quot;/g,'"').replace(/&#39;|&apos;/g,"'").replace(/&amp;/g,'&').replace(/&lt;/g,'<').replace(/&gt;/g,'>')}
function cleanOrder(o){return {order_number:o.order_number,status:o.status,payment_status:o.payment_status,currency:o.currency,amount_total:o.amount_total,created_at:o.created_at,items:(o.items||[]).map(x=>({...x,name:decodeEntities(x.name),selection:decodeEntities(x.selection)})),shipping:{city:o.shipping?.city||'',region:o.shipping?.region||'',country:o.shipping?.country||''},printify_order_id:o.printify_order_id||null}}

export default async(req)=>{
 const store=getStore(STORE);
 if(req.method==='POST'){
  let b;try{b=await req.json()}catch(_){return Response.json({error:'Invalid request.'},{status:400})}
  const action=String(b.action||''), e=email(b.email);
  if(action==='request_code'){
   if(!/^\S+@\S+\.\S+$/.test(e))return Response.json({error:'Enter a valid email.'},{status:400});
   const rateKey='rate/'+await digest(e), now=Date.now(), rate=await store.get(rateKey,{type:'json'}).catch(()=>null);if(rate&&rate.until>now)return Response.json({error:'Please wait before requesting another code.'},{status:429,headers:{'Retry-After':String(Math.max(1,Math.ceil((rate.until-now)/1000)))}});await store.setJSON(rateKey,{until:now+60*1000});
   const c=code(), expires=Date.now()+10*60*1000;
   await store.setJSON('code/'+await digest(e),{hash:await digest(e+'|'+c),expires,attempts:0});
   const sent=await sendVerificationCode({to:e,code:c});
   if(!sent.ok){
    console.error('CUSTOMER ACCESS EMAIL FAILED',{email:e,error:sent.error,status:sent.status||null});
    return Response.json({error:'Unable to send verification email right now.'},{status:502});
   }
   console.log('CUSTOMER ACCESS CODE EMAILED',{email:e,expires_at:new Date(expires).toISOString(),email_id:sent.id});
   return Response.json({ok:true,verification_required:true,email_delivery_ready:true,message:'Verification code sent.'});
  }
  if(action==='verify_code'){
   const c=String(b.code||'').trim();
   const k='code/'+await digest(e), saved=await store.get(k,{type:'json'});
   if(!saved||saved.expires<Date.now()||saved.attempts>=5)return Response.json({error:'Code expired or unavailable.'},{status:401});
   if(saved.hash!==await digest(e+'|'+c)){saved.attempts=(saved.attempts||0)+1;await store.setJSON(k,saved);return Response.json({error:'Incorrect code.'},{status:401})}
   const t=token(), expires=Date.now()+24*60*60*1000;
   await store.setJSON('session/'+await digest(t),{email:e,expires});
   await store.delete(k).catch(()=>{});
   return Response.json({ok:true,token:t,expires_at:new Date(expires).toISOString()});
  }
  return Response.json({error:'Unsupported action.'},{status:400});
 }
 if(req.method==='GET'){
  const h=String(req.headers.get('authorization')||''), t=h.startsWith('Bearer ')?h.slice(7):'';
  if(!t)return Response.json({error:'Sign in required.'},{status:401});
  const s=await store.get('session/'+await digest(t),{type:'json'});
  if(!s||s.expires<Date.now())return Response.json({error:'Session expired.'},{status:401});
  const orders=await listGbOrdersByEmail(s.email);
  return Response.json({ok:true,email:s.email,orders:orders.map(cleanOrder)});
 }
 return Response.json({error:'Method not allowed.'},{status:405,headers:{Allow:'GET, POST'}});
};
