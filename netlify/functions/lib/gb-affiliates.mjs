// Gangster Bougie affiliate records and commission ledger.
// All values live in Netlify Blobs; never expose raw customer information to affiliates.
import { getStore } from '@netlify/blobs';

const DATA='gb-affiliates-v1', LEDGER='gb-affiliate-ledger-v1';
export const HOLD_DAYS=30, ATTRIBUTION_DAYS=30;
const enc=new TextEncoder();
export const cleanEmail=v=>String(v||'').trim().toLowerCase();
export const cleanCode=v=>String(v||'').trim().toUpperCase().replace(/[^A-Z0-9_-]/g,'').slice(0,30);
export async function digest(v){const hash=await crypto.subtle.digest('SHA-256',enc.encode(String(v)));return [...new Uint8Array(hash)].map(b=>b.toString(16).padStart(2,'0')).join('')}
const id=()=>crypto.randomUUID();
const data=()=>getStore(DATA),ledger=()=>getStore(LEDGER);
const affKey=id=>'affiliate/'+encodeURIComponent(id);
const codeKey=code=>'code/'+encodeURIComponent(cleanCode(code));
const emailKey=async email=>'email/'+await digest(cleanEmail(email));
const ledgerKey=session=>'commission/'+encodeURIComponent(String(session));
const rateKey=async name=>'rate/'+await digest(String(name));
async function listRecords(store,prefix){
 const out=[];let cursor;
 do{
  const page=await store.list({prefix,...(cursor?{cursor}:{})});
  for(const blob of page.blobs||[]){const row=await store.get(blob.key,{type:'json'});if(row)out.push(row)}
  cursor=page.cursor||null;
 }while(cursor);
 return out;
}
export async function applyAffiliate({name,email,website='',channel=''}) {
 const e=cleanEmail(email),n=String(name||'').trim().slice(0,100);
 if(n.length<2||!/^\S+@\S+\.\S+$/.test(e))return {ok:false,error:'Enter your name and a valid email address.'};
 const st=data(),key=await emailKey(e),existingId=await st.get(key,{type:'text'});
 if(existingId)return {ok:true,existing:true};
 const row={id:id(),name:n,email:e,website:String(website).trim().slice(0,240),channel:String(channel).trim().slice(0,240),status:'pending',code:null,created_at:new Date().toISOString(),updated_at:new Date().toISOString()};
 await st.setJSON(affKey(row.id),row);await st.set(key,row.id);
 return {ok:true,existing:false};
}
export async function findAffiliateByEmail(e){
 const st=data(),affiliateId=await st.get(await emailKey(e),{type:'text'});
 return affiliateId?st.get(affKey(affiliateId),{type:'json'}):null;
}
export async function getAffiliateById(affiliateId){
 return affiliateId?data().get(affKey(affiliateId),{type:'json'}):null;
}
export async function getAffiliateByCode(raw){
 const code=cleanCode(raw);if(!/^[A-Z0-9][A-Z0-9_-]{2,29}$/.test(code))return null;
 const st=data(),affiliateId=await st.get(codeKey(code),{type:'text'});
 const aff=affiliateId?await st.get(affKey(affiliateId),{type:'json'}):null;
 return aff&&aff.status==='approved'&&aff.code===code?aff:null;
}
export async function listAffiliates(){return (await listRecords(data(),'affiliate/')).sort((a,b)=>String(b.created_at).localeCompare(String(a.created_at)))}
export async function updateAffiliate(affiliateId,action,requestedCode=''){
 const st=data(),row=await st.get(affKey(affiliateId),{type:'json'});
 if(!row)return {ok:false,error:'Affiliate not found.'};
 const now=new Date().toISOString();
 if(action==='approve'){
  let code=cleanCode(requestedCode);
  if(!code){const root=cleanCode(row.name).replace(/[_-]/g,'').slice(0,10)||'GB';code=root+crypto.randomUUID().replace(/-/g,'').slice(0,5).toUpperCase()}
  if(code.length<3||code.length>30)return {ok:false,error:'Referral code must contain 3–30 letters, numbers, underscores, or hyphens.'};
  const previous=await st.get(codeKey(code),{type:'text'});
  if(previous&&previous!==row.id)return {ok:false,error:'Referral code already taken.'};
  if(row.code&&row.code!==code)await st.delete(codeKey(row.code));
  await st.set(codeKey(code),row.id);
  row.code=code;row.status='approved';row.approved_at=row.approved_at||now;
 }else if(action==='reject'||action==='suspend'){
  row.status=action==='reject'?'rejected':'suspended';
 }else if(action==='reactivate'){
  if(!row.code)return {ok:false,error:'Approve this applicant first.'};
  row.status='approved';
 }else return {ok:false,error:'Invalid action.'};
 row.updated_at=now;await st.setJSON(affKey(row.id),row);return {ok:true,affiliate:row};
}
export async function setCommissionRate(name,cents) {
 const n=String(name||'').trim().slice(0,180),amount=Number(cents);
 if(n.length<2||!Number.isInteger(amount)||amount<0||amount>100000)return {ok:false,error:'Enter an exact product name and a nonnegative commission in cents.'};
 const st=data(),key=await rateKey(n);
 const record={name:n,cents:amount,updated_at:new Date().toISOString()};
 await st.setJSON(key,record);return {ok:true,rate:record};
}
export async function getCommissionRate(name){return data().get(await rateKey(name),{type:'json'})}
export async function listCommissionRates(){return listRecords(data(),'rate/')}
export async function listCommissions(){return (await listRecords(ledger(),'commission/')).sort((a,b)=>String(b.created_at).localeCompare(String(a.created_at)))}
export async function getCommissionBySession(session){return ledger().get(ledgerKey(session),{type:'json'})}
export async function recordVerifiedSale({session,affiliate,items,customerEmail,orderNumber,referralCode=''}) {
 if(!session?.id||session.payment_status!=='paid'||!affiliate?.id||!orderNumber)return {ok:false,error:'unverified_sale'};
 const st=ledger(),key=ledgerKey(session.id),existing=await st.get(key,{type:'json'});
 if(existing)return {ok:true,created:false,record:existing};
 // Commission is calculated ONLY from Stripe-verified line items, NEVER browser-supplied totals.
 const calculated=[];
 for(const item of items||[]){
  const name=String(item.name||''),qty=Math.min(100,Math.max(1,Math.floor(Number(item.quantity)||1)));
  const rate=await getCommissionRate(name);
  calculated.push({name,quantity:qty,rate_cents:Number.isInteger(rate?.cents)?rate.cents:null,commission_cents:rate?.cents!=null?rate.cents*qty:null});
 }
 const pending=calculated.some(x=>x.commission_cents===null);
 const selfReferral=cleanEmail(customerEmail)===cleanEmail(affiliate.email);
 const affiliateInactive=affiliate.status!=='approved'||Boolean(referralCode&&referralCode!==affiliate.code);
 const now=new Date().toISOString();
 const record={stripe_session_id:session.id,payment_intent:typeof session.payment_intent==='string'?session.payment_intent:session.payment_intent?.id||null,order_number:orderNumber,affiliate_id:affiliate.id,affiliate_code:referralCode||affiliate.code,currency:String(session.currency||'usd').toUpperCase(),items:calculated,commission_total_cents:pending?null:calculated.reduce((sum,x)=>sum+x.commission_cents,0),status:selfReferral?'review_self_referral':affiliateInactive?'review_inactive_affiliate':pending?'needs_rates':'pending_hold',self_referral:selfReferral,affiliate_inactive:affiliateInactive,refund_flag:false,created_at:now,hold_until:new Date(Date.now()+HOLD_DAYS*86400000).toISOString(),paid_at:null,updated_at:now};
 await st.setJSON(key,record);return {ok:true,created:true,record};
}
export async function adminUpdateCommission(session,action,updates={}) {
 const st=ledger(),key=ledgerKey(session),row=await st.get(key,{type:'json'});
 if(!row)return {ok:false,error:'Commission not found.'};
 const now=new Date().toISOString();
 if(action==='recalculate'){
  if(row.status==='paid'||row.status==='void'||row.status==='refund_review')return {ok:false,error:'Resolve the paid/void/refund state first.'};
  for(const item of row.items){const rate=await getCommissionRate(item.name);item.rate_cents=Number.isInteger(rate?.cents)?rate.cents:null;item.commission_cents=item.rate_cents===null?null:item.rate_cents*item.quantity}
  const pending=row.items.some(x=>x.commission_cents===null);
  row.commission_total_cents=pending?null:row.items.reduce((s,x)=>s+x.commission_cents,0);
  row.status=pending?'needs_rates':row.refund_flag?'refund_review':row.self_referral?'review_self_referral':row.affiliate_inactive?'review_inactive_affiliate':'pending_hold';
 }else if(action==='mark_paid'){
  if(row.status!=='pending_hold'&&row.status!=='approved_for_payout')return {ok:false,error:'Commission needs review before payment.'};
  if(Date.parse(row.hold_until)>Date.now())return {ok:false,error:'30-day holding period has not elapsed.'};
  if(!Number.isInteger(row.commission_total_cents)||row.commission_total_cents<=0)return {ok:false,error:'No commission payable.'};
  row.status='paid';row.paid_at=now;row.payout_note=String(updates.note||'').trim().slice(0,160);
 }else if(action==='void'){
  if(row.status==='paid')return {ok:false,error:'Already paid: handle any recovery manually.'};
  row.status='void';row.review_note=String(updates.note||'').trim().slice(0,160);
 }else if(action==='approve_for_payout'){
  if(!['review_self_referral','review_inactive_affiliate','pending_hold','needs_rates','refund_review'].includes(row.status)||!Number.isInteger(row.commission_total_cents))return {ok:false,error:'Set all product rates before approval.'};
  row.status='approved_for_payout';row.review_note=String(updates.note||'').trim().slice(0,160);
 }else return {ok:false,error:'Invalid action.'};
 row.updated_at=now;await st.setJSON(key,row);return {ok:true,record:row};
}
export async function flagRefund(paymentIntent) {
 if(!paymentIntent)return {ok:false,error:'missing_payment_intent'};
 const results=[];
 for(const row of await listCommissions()){
  if(row.payment_intent!==paymentIntent)continue;
  row.refund_flag=true;if(row.status==='paid'){row.refund_after_payout=true}else{row.status='refund_review'}
  row.updated_at=new Date().toISOString();await ledger().setJSON(ledgerKey(row.stripe_session_id),row);results.push(row.stripe_session_id);
 }
 return {ok:true,flagged:results};
}
