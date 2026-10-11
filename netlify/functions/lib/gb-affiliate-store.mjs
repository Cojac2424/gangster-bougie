// Gangster Bougie affiliate / creator partnership foundation.
// Private payout schedule: partners see earnings per product, never GB cost or margin.
import { getStore } from '@netlify/blobs';

const STORE='gb-affiliates-v1';
const norm=v=>String(v||'').trim();
const code=v=>norm(v).toUpperCase().replace(/[^A-Z0-9_-]/g,'').slice(0,40);
const email=v=>norm(v).toLowerCase();

export async function getAffiliateByCode(raw){
 const c=code(raw); if(!c)return null;
 return await getStore(STORE).get('code/'+encodeURIComponent(c),{type:'json'}).catch(()=>null);
}
export async function saveAffiliate(a){
 const c=code(a?.code), e=email(a?.email); if(c.length<3||!e)throw new Error('affiliate_code_and_email_required');
 const store=getStore(STORE), now=new Date().toISOString();
 const current=await getAffiliateByCode(c);
 const record={id:current?.id||crypto.randomUUID(),name:norm(a.name),email:e,code:c,status:a.status||current?.status||'active',created_at:current?.created_at||now,updated_at:now};
 await store.setJSON('code/'+encodeURIComponent(c),record);
 await store.setJSON('affiliate/'+encodeURIComponent(record.id),record);
 return record;
}
export async function savePayoutSchedule(affiliateId,payouts={}){
 const clean={}; for(const [product,amount] of Object.entries(payouts)){const cents=Math.floor(Number(amount));if(product&&Number.isFinite(cents)&&cents>=0)clean[String(product)]=cents;}
 await getStore(STORE).setJSON('payouts/'+encodeURIComponent(affiliateId),{affiliate_id:affiliateId,payouts:clean,updated_at:new Date().toISOString()});
 return clean;
}
export async function getPayoutCents(affiliateId,productName){
 const s=await getStore(STORE).get('payouts/'+encodeURIComponent(affiliateId),{type:'json'}).catch(()=>null);
 return Math.max(0,Math.floor(Number(s?.payouts?.[String(productName)])||0));
}
export async function recordReferral({affiliate,checkoutSessionId}){
 if(!affiliate?.id||!checkoutSessionId)return null;
 const store=getStore(STORE), key='referral/'+encodeURIComponent(checkoutSessionId), existing=await store.get(key,{type:'json'}).catch(()=>null);
 if(existing)return existing;
 const r={affiliate_id:affiliate.id,affiliate_code:affiliate.code,stripe_session_id:checkoutSessionId,created_at:new Date().toISOString()};
 await store.setJSON(key,r); return r;
}
export async function recordCommission({affiliateId,orderNumber,stripeSessionId,items}){
 const store=getStore(STORE), key='commission/'+encodeURIComponent(stripeSessionId), existing=await store.get(key,{type:'json'}).catch(()=>null);
 if(existing)return {created:false,record:existing};
 let total=0; const lines=[];
 for(const x of items||[]){const qty=Math.max(1,Math.floor(Number(x.quantity||x.qty)||1)),unit=await getPayoutCents(affiliateId,x.name),amount=unit*qty;total+=amount;lines.push({product:x.name,quantity:qty,payout_per_item_cents:unit,commission_cents:amount});}
 const earnedAt=new Date(), eligibleAt=new Date(earnedAt.getTime()+30*24*60*60*1000);const record={id:crypto.randomUUID(),affiliate_id:affiliateId,order_number:orderNumber,stripe_session_id:stripeSessionId,commission_cents:total,status:'pending',lines,earned_at:earnedAt.toISOString(),eligible_for_payout_at:eligibleAt.toISOString()};
 await store.setJSON(key,record); await store.setJSON('commission-id/'+encodeURIComponent(record.id),record); return {created:true,record};
}
export async function recordAffiliateClick({affiliateId,code:affiliateCode}){
 if(!affiliateId)return null;
 const store=getStore(STORE), day=new Date().toISOString().slice(0,10), key='clicks/'+encodeURIComponent(affiliateId)+'/'+day;
 const current=await store.get(key,{type:'json'}).catch(()=>null), record={affiliate_id:affiliateId,affiliate_code:code(affiliateCode),day,count:Math.max(0,Number(current?.count)||0)+1,updated_at:new Date().toISOString()};
 await store.setJSON(key,record);return record;
}
export async function voidCommissionByStripeSession(stripeSessionId,reason='refunded'){
 const store=getStore(STORE), key='commission/'+encodeURIComponent(stripeSessionId), current=await store.get(key,{type:'json'}).catch(()=>null);
 if(!current)return {ok:true,found:false}; if(current.status==='void')return {ok:true,found:true,record:current};
 const record={...current,status:'void',void_reason:String(reason),voided_at:new Date().toISOString()};await store.setJSON(key,record);await store.setJSON('commission-id/'+encodeURIComponent(record.id),record);return {ok:true,found:true,record};
}
export {code as normalizeAffiliateCode};
