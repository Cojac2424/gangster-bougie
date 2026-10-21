// Private owner-only planning math. Never use unverified estimates to commit payouts.
// All amounts are USD cents. Fee is an estimate, not a Stripe statement.
export const FEE_ESTIMATE_BASIS_POINTS=450; // 4.5% conservative planning allowance
export const FEE_ESTIMATE_FIXED_CENTS=30; // conservative per-item allocation
export const PLAN_COUNTRIES=Object.freeze(['US','CA']);
const cents=n=>typeof n==='number'&&Number.isSafeInteger(n)&&n>=0?n:null;
const itemCents=x=>x?.currency==='USD'?cents(x.cost):null;
function relevantProfiles(profiles,variantId,country){
 const eligible=(profiles||[]).filter(p=>(p.variant_ids||[]).some(v=>Number(v)===Number(variantId)));
 const exact=eligible.filter(p=>(p.countries||[]).includes(country));
 return exact.length?exact:eligible.filter(p=>(p.countries||[]).includes('REST_OF_THE_WORLD'));
}
export function getWorstShippingCents(shippingProfiles,variantIds,countries=PLAN_COUNTRIES){
 const perDestination=[];
 for(const variantId of variantIds){
  for(const country of countries){
   const hits=relevantProfiles(shippingProfiles,variantId,country);
   const amounts=hits.map(x=>itemCents(x.first_item)).filter(n=>n!==null);
   if(!amounts.length)return {ok:false,reason:'shipping_profile_missing',variantId,country};
   perDestination.push({variantId,country,cents:Math.max(...amounts)});
  }
 }
 if(!perDestination.length)return {ok:false,reason:'no_shipping_profiles'};
 return {ok:true,maxFirstItemCents:Math.max(...perDestination.map(x=>x.cents)),perDestination};
}
export function planProductCommission({
 name,retailCents,variantCosts,shippingByVariant,customerContributionCents,
 feeRateBasisPoints=FEE_ESTIMATE_BASIS_POINTS,feeFixedCents=FEE_ESTIMATE_FIXED_CENTS
}){
 const sell=cents(retailCents),contribution=cents(customerContributionCents);
 if(!name||sell===null||sell===0||contribution===null)return {name,status:'needs_review',reason:'invalid_retail_or_contribution'};
 const list=Array.isArray(variantCosts)?variantCosts:[];
 if(!list.length||list.some(v=>cents(v.costCents)===null))return {name,status:'needs_review',reason:'unverified_printify_variant_cost'};
 if(!Array.isArray(shippingByVariant)||shippingByVariant.length===0||shippingByVariant.some(v=>cents(v.firstItemCents)===null))
  return {name,status:'needs_review',reason:'shipping_country_or_variant_unverified'};
 const highCost=Math.max(...list.map(v=>Number(v.costCents))),lowCost=Math.min(...list.map(v=>Number(v.costCents)));
 const shipping=Math.max(...shippingByVariant.map(v=>Number(v.firstItemCents)));
 const subsidy=Math.max(0,shipping-contribution);
 if(!Number.isSafeInteger(feeRateBasisPoints)||feeRateBasisPoints<0||feeRateBasisPoints>10000||cents(feeFixedCents)===null)
  return {name,status:'needs_review',reason:'fee_assumption_invalid'};
 // Per-item fee allocation is intentionally conservative for multi-item orders.
 const processing=Math.ceil((sell+Math.min(shipping,contribution))*feeRateBasisPoints/10000)+feeFixedCents;
 const profit=sell-highCost-subsidy-processing;
 const target=Math.max(0,Math.floor(profit*0.2));
 const wholeDollar=Math.floor(target/100)*100;
 // A target close to one dollar can round to $1 only when a safe $4+ profit remains
 // before payout. This covers the previously agreed $1 leggings example (~22%),
 // while rejecting $1 commissions on thin-margin products such as socks/yoga mats.
 const minimumOneDollarException=wholeDollar===0&&target>=75&&profit>=400;
 const proposed=minimumOneDollarException?100:wholeDollar;
 return {name,status:profit>0&&proposed>0?'proposal_ready':'needs_review',
  reason:profit>0&&proposed>0?null:'zero_or_negative_suggested_commission',
  retail_cents:sell,production_high_cents:highCost,production_low_cents:lowCost,
  max_first_item_shipping_cents:shipping,customer_shipping_contribution_cents:contribution,
  gb_shipping_subsidy_cents:subsidy,processing_allowance_cents:processing,
  estimated_profit_cents:profit,twenty_percent_cents:target,proposed_commission_cents:proposed,
  estimated_retained_after_commission_cents:profit-proposed,rounding_note:minimumOneDollarException?'minimum_1_dollar_exception':'rounded_down_whole_dollars',
  fee_basis_points:feeRateBasisPoints,fee_fixed_cents:feeFixedCents,
  cost_variant_count:list.length,shipping_profile_count:shippingByVariant.length};
}
