import test from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { Script } from 'node:vm';
import { PRICE_CENTS, VARIABLE_PRICES, SELLABLE_PRODUCT_NAMES, AFFILIATE_RATE_PRODUCTS, AFFILIATE_LEGACY_UNMAPPED_NAMES, COMMISSION_PRODUCT_ALIASES, canonicalCommissionName } from '../netlify/functions/lib/gb-product-catalog.mjs';
import { normalizeReferralCode, referralExpiryMs, referralIsValid, commissionForPaidItems, commissionTotalCents, commissionHoldUntil, REFERRAL_WINDOW_DAYS, COMMISSION_HOLD_DAYS } from '../netlify/functions/lib/gb-affiliate-rules.mjs';
import {getWorstShippingCents,planProductCommission,FEE_ESTIMATE_BASIS_POINTS} from '../netlify/functions/lib/gb-affiliate-cost-math.mjs';
import {customerShippingContribution} from '../netlify/functions/lib/gb-shipping-contribution.mjs';

test('checkout catalog contains distinct authoritative products and positive prices', () => {
 assert.ok(SELLABLE_PRODUCT_NAMES.length >= 50);
 assert.equal(new Set(SELLABLE_PRODUCT_NAMES).size, SELLABLE_PRODUCT_NAMES.length);
 for (const name of SELLABLE_PRODUCT_NAMES) assert.ok(Number.isInteger(PRICE_CENTS[name]) && PRICE_CENTS[name] > 0, name);
 assert.equal(PRICE_CENTS['Gangster Bougie Women’s Signature Crop Tee – Black'], 3999);
 assert.equal(PRICE_CENTS['Gangster Bougie Women’s Signature Crop Tee – White'], 3999);
 for (const [name, sizes] of Object.entries(VARIABLE_PRICES)) {
   assert.ok(SELLABLE_PRODUCT_NAMES.includes(name));
   for (const p of Object.values(sizes)) assert.ok(Number.isInteger(p) && p > 0);
 }
});
test('referral validation and 30-day attribution expiry', () => {
 const start = Date.UTC(2026, 9, 21);
 assert.equal(normalizeReferralCode('Jenn10'), 'JENN10');
 assert.equal(normalizeReferralCode('X'), null);
 assert.equal(normalizeReferralCode('INVALID CODE!'), null);
 assert.equal(REFERRAL_WINDOW_DAYS,30);
 assert.equal(referralExpiryMs(start),start+30*86400000);
 assert.equal(referralIsValid({code:'JENN10',clickedAtMs:start,nowMs:start+29*86400000}),true);
 assert.equal(referralIsValid({code:'JENN10',clickedAtMs:start,nowMs:start+30*86400000}),false);
 assert.equal(referralIsValid({code:'JENN10',clickedAtMs:start,nowMs:start-1}),false);
});
test('fixed commissions reflect quantities and missing rates are marked unconfigured', () => {
 const lines = commissionForPaidItems([{name:'Leggings',quantity:2},{name:'Hoodie',qty:1}],{Leggings:400,Hoodie:600});
 assert.equal(lines[0].commissionCents,800);
 assert.equal(lines[1].commissionCents,600);
 assert.equal(commissionTotalCents(lines),1400);
 const unconfigured=commissionForPaidItems([{name:'New Product',qty:1}],{});
 assert.equal(unconfigured[0].configured,false);
 assert.throws(()=>commissionForPaidItems([{name:'Leggings',qty:0}],{Leggings:400}),RangeError);
});
test('commission holding period is thirty full days', () => {
 const paid=Date.UTC(2026,9,21);
 assert.equal(COMMISSION_HOLD_DAYS,30);
 assert.equal(commissionHoldUntil(paid),new Date(paid+30*86400000).toISOString());
});
test('affiliate page scripts parse as JavaScript', () => {
 for(const filename of ['affiliate.html','affiliate-admin.html']){
  const html=readFileSync(new URL('../'+filename,import.meta.url),'utf8');
  const scripts=[...html.matchAll(/<script(?:\s+[^>]*)?>([\s\S]*?)<\/script>/gi)];
  assert.ok(scripts.length>0,filename+' has inline script');
  scripts.forEach((match,i)=>assert.doesNotThrow(()=>new Script(match[1],{filename:filename+'#script'+i})));
 }
});

test('storefront connects affiliate login and application with the right pages', () => {
 const home=readFileSync(new URL('../index.html',import.meta.url),'utf8');
 const affiliate=readFileSync(new URL('../affiliate.html',import.meta.url),'utf8');
 const admin=readFileSync(new URL('../affiliate-admin.html',import.meta.url),'utf8');
 assert.match(home, /<footer>[\s\S]*?href="\/affiliate\.html"[\s\S]*?Become a Gangster Bougie Affiliate[\s\S]*?<\/footer>/);
 assert.match(home, /id="gbAccountIntro"[\s\S]*?href="\/affiliate\.html"[\s\S]*?>Affiliate Login<\/a>/);
 assert.match(affiliate, /id="applyForm"/);
 assert.match(affiliate, /id="signForm"/);
 assert.match(affiliate, /id="affiliatePanel"/);
 assert.match(admin, /id="authForm"/);
 assert.match(admin, /id="commissions"/);
});

test('Printify fulfillment picks exact sizes and accessory variants', async () => {
 const {resolveFulfillment}=await import('../netlify/functions/lib/fulfillment-resolver.mjs');
 const blue='GB Classic High-Waisted Leggings – Blue';
 assert.equal(resolveFulfillment(blue,'XS').variant_id,67982);
 assert.equal(resolveFulfillment(blue,'S').variant_id,67983);
 assert.equal(resolveFulfillment(blue,'M').variant_id,67984);
 assert.equal(resolveFulfillment(blue,'L').variant_id,67985);
 assert.equal(resolveFulfillment(blue,'XL').variant_id,67986);
 assert.equal(resolveFulfillment(blue,'2XL').variant_id,67987);
 assert.equal(resolveFulfillment(blue,'Black / XL').variant_id,67986);
 assert.equal(resolveFulfillment(blue,'3XL').ok,false);
 assert.equal(resolveFulfillment('Onyx/Gold Crowned Luxury Full-Zip Hoodie','2XL').variant_id,75723);
 assert.equal(resolveFulfillment('Stainless Steel Gym Bottle','18 oz').variant_id,76802);
 assert.equal(resolveFulfillment('Stainless Steel Gym Bottle','Black / 12 oz').variant_id,76801);
 assert.equal(resolveFulfillment('Embroidered Structured Cap','S/M').variant_id,118702);
 assert.equal(resolveFulfillment('Embroidered Structured Cap','L/XL').variant_id,118703);
 assert.equal(resolveFulfillment('Gangster Bougie Gym Face Towel','Black').variant_id,75135);
 assert.equal(resolveFulfillment('Gangster Bougie Foam Yoga Mat','Dark Blue').variant_id,71786);
});

test('one commission amount per real product, including every accessory alias', () => {
 assert.equal(AFFILIATE_RATE_PRODUCTS.length,52);
 assert.equal(Object.keys(COMMISSION_PRODUCT_ALIASES).length,8);
 assert.equal(AFFILIATE_LEGACY_UNMAPPED_NAMES.length,6);
 for(const name of AFFILIATE_RATE_PRODUCTS) assert.ok(SELLABLE_PRODUCT_NAMES.includes(name));
 for(const [alias,canonical] of Object.entries(COMMISSION_PRODUCT_ALIASES)){
   assert.equal(canonicalCommissionName(alias),canonical);
   assert.ok(AFFILIATE_RATE_PRODUCTS.includes(canonical));
   assert.equal(PRICE_CENTS[alias],PRICE_CENTS[canonical]);
   assert.ok(!AFFILIATE_RATE_PRODUCTS.includes(alias));
 }
 for(const name of AFFILIATE_LEGACY_UNMAPPED_NAMES){
  assert.ok(!AFFILIATE_RATE_PRODUCTS.includes(name));
 }
 assert.ok(AFFILIATE_RATE_PRODUCTS.includes('Gangster Bougie Women’s Signature Crop Tee – Black'));
 assert.ok(AFFILIATE_RATE_PRODUCTS.includes('Gangster Bougie Women’s Signature Crop Tee – White'));
 assert.ok(AFFILIATE_RATE_PRODUCTS.includes('Gym Face Towel'));
 assert.ok(AFFILIATE_RATE_PRODUCTS.includes('Foam Yoga Mat'));
});

test('shipping subsidy uses the same contribution as live checkout', () => {
 assert.equal(customerShippingContribution('Gym Face Towel'),249);
 assert.equal(customerShippingContribution('Foam Yoga Mat'),499);
 assert.equal(customerShippingContribution('Onyx/Gold Crowned Luxury Full-Zip Hoodie'),0);
 assert.equal(customerShippingContribution('Stainless Steel Gym Bottle'),499);
});
test('Printify US and Canada shipping quotes choose highest first-item cost for all offered variants',()=>{
 const profiles=[
  {variant_ids:[10,20],countries:['US'],first_item:{currency:'USD',cost:799}},
  {variant_ids:[10,20],countries:['CA'],first_item:{currency:'USD',cost:1199}}
 ];
 const result=getWorstShippingCents(profiles,[10,20]);
 assert.equal(result.ok,true);
 assert.equal(result.maxFirstItemCents,1199);
 assert.equal(result.perDestination.length,4);
 assert.equal(getWorstShippingCents(profiles.slice(0,1),[10]).ok,false);
});
test('verified Printify cost planner rounds DOWN to fixed whole-dollar USD, requiring owner approval',()=>{
 const row=planProductCommission({
  name:'Example accessory',retailCents:4999,
  variantCosts:[{costCents:1200},{costCents:1600}],
  shippingByVariant:[{firstItemCents:799},{firstItemCents:1199}],
  customerContributionCents:299
 });
 assert.equal(FEE_ESTIMATE_BASIS_POINTS,450);
 assert.equal(row.status,'proposal_ready');
 assert.equal(row.production_high_cents,1600);
 assert.equal(row.gb_shipping_subsidy_cents,900);
 assert.equal(row.processing_allowance_cents,269);
 assert.equal(row.estimated_profit_cents,2230);
 assert.equal(row.twenty_percent_cents,446);
 assert.equal(row.proposed_commission_cents,400);
 assert.equal(planProductCommission({
  name:'Unsafe',retailCents:1999,variantCosts:[],shippingByVariant:[],customerContributionCents:299
 }).status,'needs_review');
 assert.equal(planProductCommission({
  name:'Loss-making',retailCents:2000,variantCosts:[{costCents:3000}],
  shippingByVariant:[{firstItemCents:1000}],customerContributionCents:0
 }).status,'needs_review');
});
test('owner admin has private Printify syncing and proposal approval UI',()=>{
 const admin=readFileSync(new URL('../affiliate-admin.html',import.meta.url),'utf8');
 assert.match(admin,/id="syncPrintifyCosts"/);
 assert.match(admin,/id="approvePrintifyCosts"/);
 assert.match(admin,/approve_all_cost_rates/);
 assert.match(admin,/sync_printify_costs/);
});
