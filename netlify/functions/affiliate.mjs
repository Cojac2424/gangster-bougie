// Public affiliate application, code validation and email-verified affiliate dashboard.
import {getStore} from '@netlify/blobs';
import {applyAffiliate,cleanCode,cleanEmail,digest,findAffiliateByEmail,getAffiliateByCode,listCommissions,listCommissionRates} from './lib/gb-affiliates.mjs';
import {sendAffiliateVerificationCode,sendAffiliateApplicationNotice} from './lib/gb-email.mjs';
const auth=()=>getStore('gb-affiliate-auth-v1');
const json=(value,status=200)=>Response.json(value,{status,headers:{'Cache-Control':'no-store'}});
const token=()=>[...crypto.getRandomValues(new Uint8Array(32))].map(x=>x.toString(16).padStart(2,'0')).join('');
const code=()=>{const a=new Uint32Array(1);crypto.getRandomValues(a);return String(100000+a[0]%900000)};
async function limited(req,kind,max,windowMs) {
 const ip=String(req.headers.get('x-nf-client-connection-ip')||req.headers.get('x-forwarded-for')||'unknown').split(',')[0].trim();
 const key='rate/'+kind+'/'+await digest(ip),store=auth(),now=Date.now(),prior=await store.get(key,{type:'json'}).catch(()=>null);
 const state=prior&&prior.until>now?prior:{count:0,until:now+windowMs};state.count++;
 await store.setJSON(key,state);
 return state.count>max;
}
export default async req=>{
 if(req.method==='GET'){
  const u=new URL(req.url);
  if(u.searchParams.get('action')==='validate_code'){
   const affiliate=await getAffiliateByCode(u.searchParams.get('code'));
   return json({valid:!!affiliate,code:affiliate?.code||null});
  }
  const bearer=String(req.headers.get('authorization')||'');
  const t=bearer.startsWith('Bearer ')?bearer.slice(7):'';
  if(!t)return json({error:'Sign in required.'},401);
  const session=await auth().get('session/'+await digest(t),{type:'json'});
  if(!session||session.expires<Date.now())return json({error:'Session expired.'},401);
  const affiliate=await findAffiliateByEmail(session.email);
  if(!affiliate||affiliate.status!=='approved')return json({error:'This affiliate account is not active.'},403);
  const records=(await listCommissions()).filter(x=>x.affiliate_id===affiliate.id).map(x=>({order_number:x.order_number,created_at:x.created_at,hold_until:x.hold_until,items:x.items,status:x.status,currency:x.currency,commission_total_cents:x.commission_total_cents,paid_at:x.paid_at}));
  const rates=(await listCommissionRates()).filter(x=>Number.isInteger(x.cents)&&x.cents>0).map(x=>({name:x.name,cents:x.cents})).sort((x,y)=>x.name.localeCompare(y.name));
  return json({ok:true,affiliate:{name:affiliate.name,email:affiliate.email,code:affiliate.code,status:affiliate.status},records,rates});
 }
 if(req.method!=='POST')return json({error:'Method not allowed.'},405);
 let body;try{body=await req.json()}catch{return json({error:'Invalid request.'},400)}
 const action=String(body.action||'');
 if(action==='apply'){
  if(await limited(req,'apply',5,60*60*1000))return json({error:'Please try again later.'},429);
  const result=await applyAffiliate(body);
  if(result.ok&&!result.existing){try{const mail=await sendAffiliateApplicationNotice(body);if(!mail.ok)console.error('AFFILIATE APPLICATION ALERT FAILED',mail.error)}catch(e){console.error('AFFILIATE APPLICATION ALERT FAILED',String(e?.message||e))}}
  return result.ok?json({ok:true,message:'Application received. We will review it before issuing a referral code.'}):json({error:result.error},400);
 }
 if(action==='request_code'){
  if(await limited(req,'code',10,10*60*1000))return json({error:'Please wait before requesting another code.'},429);
  const email=cleanEmail(body.email);
  if(!/^\S+@\S+\.\S+$/.test(email))return json({error:'Enter a valid email.'},400);
  const store=auth(),key='emailrate/'+await digest(email),now=Date.now(),last=await store.get(key,{type:'json'}).catch(()=>null);
  if(last?.until>now)return json({error:'Please wait one minute before requesting another code.'},429);
  await store.setJSON(key,{until:now+60000});
  const affiliate=await findAffiliateByEmail(email);
  if(affiliate?.status==='approved'){
   const c=code(),expires=Date.now()+600000;
   await store.setJSON('code/'+await digest(email),{hash:await digest(email+'|'+c),expires,attempts:0});
   const sent=await sendAffiliateVerificationCode({to:email,code:c});
   if(!sent.ok){console.error('AFFILIATE AUTH EMAIL FAILED',sent.error);return json({error:'Unable to send the verification email right now.'},502)}
  }
  return json({ok:true,message:'If this email belongs to an approved affiliate, a six-digit code has been sent.'});
 }
 if(action==='verify_code'){
  if(await limited(req,'verify',30,10*60*1000))return json({error:'Too many attempts. Please wait.'},429);
  const email=cleanEmail(body.email),c=String(body.code||''),store=auth();
  if(!/^\S+@\S+\.\S+$/.test(email)||!/^[0-9]{6}$/.test(c))return json({error:'Invalid code.'},401);
  const key='code/'+await digest(email),state=await store.get(key,{type:'json'});
  if(!state||state.expires<Date.now()||state.attempts>=5)return json({error:'Code expired or unavailable.'},401);
  if(state.hash!==await digest(email+'|'+c)){state.attempts++;await store.setJSON(key,state);return json({error:'Incorrect code.'},401)}
  const affiliate=await findAffiliateByEmail(email);
  if(!affiliate||affiliate.status!=='approved')return json({error:'Affiliate account unavailable.'},403);
  const t=token();await store.setJSON('session/'+await digest(t),{email,expires:Date.now()+24*60*60*1000});await store.delete(key);
  return json({ok:true,token:t});
 }
 return json({error:'Unsupported action.'},400);
};
