// Gangster Bougie affiliate rules. Staging-only foundation; no payouts or checkout changes.
// Commission amounts are set in cents by product name after margin review.
// Never accept a commission amount or affiliate approval from the shopper's browser.
export const REFERRAL_WINDOW_DAYS=30;
export const COMMISSION_HOLD_DAYS=30;
export const COMMISSION_CENTS=Object.freeze({});

export function normalizeReferralCode(value){
 const code=String(value??'').trim().toUpperCase();
 return /^[A-Z0-9][A-Z0-9_-]{2,23}$/.test(code)?code:null;
}
export function referralExpiryMs(clickedAtMs){
 const t=Number(clickedAtMs);
 return Number.isFinite(t)&&t>0?t+REFERRAL_WINDOW_DAYS*86400000:null;
}
export function referralIsValid({code,clickedAtMs,nowMs=Date.now()}){
 const expiry=referralExpiryMs(clickedAtMs);
 return Boolean(normalizeReferralCode(code)&&expiry&&Number(nowMs)>=Number(clickedAtMs)&&Number(nowMs)<expiry);
}
export function commissionForPaidItems(items){
 if(!Array.isArray(items))throw new TypeError('items must be an array');
 return items.map(item=>{
  const name=String(item?.name??'').trim();
  const quantity=Number(item?.quantity??item?.qty??0);
  if(!Number.isSafeInteger(quantity)||quantity<1||quantity>100)throw new RangeError('invalid quantity');
  const cents=COMMISSION_CENTS[name];
  if(!Number.isSafeInteger(cents)||cents<0) return {name,quantity,commissionCents:0,configured:false};
  return {name,quantity,commissionCents:cents*quantity,configured:true};
 });
}
export function commissionTotalCents(lines){
 return lines.reduce((sum,line)=>sum+line.commissionCents,0);
}
export function commissionHoldUntil(paidAtMs){
 const t=Number(paidAtMs);
 return Number.isFinite(t)&&t>0?new Date(t+COMMISSION_HOLD_DAYS*86400000).toISOString():null;
}
