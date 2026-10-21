// Owner-only affiliate administration. Set GB_AFFILIATE_ADMIN_SECRET (>=24 characters)
// in Netlify before attempting access; this endpoint fails closed without it.
import {digest,listAffiliates,listCommissions,listCommissionRates,setCommissionRate,updateAffiliate,adminUpdateCommission} from './lib/gb-affiliates.mjs';
import {sendAffiliateApprovalNotice} from './lib/gb-email.mjs';
import {AFFILIATE_RATE_PRODUCTS} from './lib/gb-product-catalog.mjs';
import {listCostSnapshots,syncCostBatch,applyProposedRates} from './lib/gb-affiliate-cost-sync.mjs';
const json=(body,status=200)=>Response.json(body,{status,headers:{'Cache-Control':'no-store'}});
async function authorized(req){
 const expected=String(process.env.GB_AFFILIATE_ADMIN_SECRET||'');
 if(expected.length<24)return false;
 const h=String(req.headers.get('authorization')||''),value=h.startsWith('Bearer ')?h.slice(7):'';
 if(value.length!==expected.length)return false;
 const a=await digest(value),b=await digest(expected);
 let diff=0;for(let i=0;i<a.length;i++)diff|=a.charCodeAt(i)^b.charCodeAt(i);
 return diff===0;
}
export default async req=>{
 if(!process.env.GB_AFFILIATE_ADMIN_SECRET||process.env.GB_AFFILIATE_ADMIN_SECRET.length<24)return json({error:'Affiliate admin access has not been configured.'},503);
 if(!await authorized(req))return json({error:'Unauthorized.'},401);
 if(req.method==='GET'){
  const [affiliates,commissions,rates,printify_costs]=await Promise.all([listAffiliates(),listCommissions(),listCommissionRates(),listCostSnapshots()]);
  return json({ok:true,affiliates,commissions,rates,printify_costs,catalog_products:AFFILIATE_RATE_PRODUCTS,hold_days:30});
 }
 if(req.method!=='POST')return json({error:'Method not allowed.'},405);
 let b;try{b=await req.json()}catch{return json({error:'Invalid request.'},400)}
 let result;
 if(b.action==='sync_printify_costs')result=await syncCostBatch({offset:b.offset,batchSize:3});
 else if(b.action==='approve_all_cost_rates')result=await applyProposedRates({offset:b.offset,batchSize:4});
 else if(b.action==='set_rate')result=await setCommissionRate(b.name,b.cents);
 else if(['approve','reject','suspend','reactivate'].includes(b.action))result=await updateAffiliate(String(b.affiliate_id||''),b.action,b.code||'');
 else if(['recalculate','mark_paid','void','approve_for_payout'].includes(b.action))result=await adminUpdateCommission(String(b.stripe_session_id||''),b.action,{note:b.note||''});
 else return json({error:'Unsupported action.'},400);
 if(result.ok&&b.action==='approve'&&result.affiliate){try{const mail=await sendAffiliateApprovalNotice({to:result.affiliate.email,name:result.affiliate.name,code:result.affiliate.code});if(!mail.ok)console.error('AFFILIATE APPROVAL EMAIL FAILED',mail.error)}catch(e){console.error('AFFILIATE APPROVAL EMAIL FAILED',String(e?.message||e))}}
 return result.ok?json(result):json({error:result.error||'Update failed.'},400);
};
