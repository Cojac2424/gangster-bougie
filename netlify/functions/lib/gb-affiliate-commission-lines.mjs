// Pure ledger-line calculations used by paid Stripe sale capture and admin recalculation.
// Each item retains its original Stripe-verified display name. Exclusions are explicit,
// and an absent *eligible* rate is never silently counted as a zero commission.
export function commissionLineFromRate(item,rate) {
 const name=String(item?.name||'');
 const quantity=Math.min(100,Math.max(1,Math.floor(Number(item?.quantity)||1)));
 const excluded=Boolean(rate?.excluded);
 const rate_cents=excluded?0:Number.isSafeInteger(rate?.cents)&&rate.cents>=0?rate.cents:null;
 return {name,quantity,excluded,rate_cents,
  commission_cents:rate_cents===null?null:rate_cents*quantity};
}
export function summarizeCommissionLines(items) {
 const list=Array.isArray(items)?items:[];
 const missing_rate=list.some(item=>item.commission_cents===null);
 const excluded_only=list.length>0&&list.every(item=>item.excluded===true);
 return {missing_rate,excluded_only,commission_total_cents:missing_rate?null:
  list.reduce((total,item)=>total+item.commission_cents,0)};
}
