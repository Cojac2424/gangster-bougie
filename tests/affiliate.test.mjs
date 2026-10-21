import test from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { Script } from 'node:vm';
import { PRICE_CENTS, VARIABLE_PRICES, SELLABLE_PRODUCT_NAMES, AFFILIATE_RATE_PRODUCTS, AFFILIATE_COST_PRODUCTS, AFFILIATE_RATE_MEMBERS, AFFILIATE_LEGACY_UNMAPPED_NAMES, COMMISSION_PRODUCT_ALIASES, canonicalCommissionName } from '../netlify/functions/lib/gb-product-catalog.mjs';
import { normalizeReferralCode, referralExpiryMs, referralIsValid, commissionForPaidItems, commissionTotalCents, commissionHoldUntil, REFERRAL_WINDOW_DAYS, COMMISSION_HOLD_DAYS } from '../netlify/functions/lib/gb-affiliate-rules.mjs';
import {getWorstShippingCents,planProductCommission,FEE_ESTIMATE_BASIS_POINTS,conservativeFamilyCommission} from '../netlify/functions/lib/gb-affiliate-cost-math.mjs';
import {customerShippingContribution} from '../netlify/functions/lib/gb-shipping-contribution.mjs';
import {readPrintifyCost} from '../netlify/functions/lib/gb-affiliate-printify-reader.mjs';
import {affiliateMappedVariants} from '../netlify/functions/lib/fulfillment-resolver.mjs';
import {AFFILIATE_EXCLUDED_RATE_NAMES,AFFILIATE_EXCLUDED_PRODUCT_NAMES,AFFILIATE_ELIGIBLE_RATE_PRODUCTS,isAffiliateExcluded} from '../netlify/functions/lib/gb-product-catalog.mjs';
import {commissionLineFromRate,summarizeCommissionLines} from '../netlify/functions/lib/gb-affiliate-commission-lines.mjs';
import {retrieveAllStripeLineItems} from '../netlify/functions/lib/gb-stripe-line-items.mjs';

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

test('mobile checkout confirms shipping address and recalculates before enabling payment',()=>{
 const home=readFileSync(new URL('../index.html',import.meta.url),'utf8');
 assert.doesNotMatch(home,/id="gbCheckoutCalculateShipping"/);
 assert.doesNotMatch(home,/Calculate shipping<\/button>/);
 assert.match(home,/gbShippingEl\.on\('blur'/);
 assert.match(home,/gbQuoteTimer=setTimeout\(\(\)=>refreshShippingQuote\(version\),350\)/);
 assert.match(home,/gbShippingEl\.getValue\(\)/);
 assert.match(home,/gbActions\.updateShippingAddress\(\{name,address:/);
 assert.match(home,/await gbActions\.runServerUpdate\(/);
 assert.ok(home.indexOf('await gbActions.updateShippingAddress')<home.indexOf('await gbActions.runServerUpdate'));
 assert.match(home,/gbCheckout\.on\('change',session=>updateSummary\(session\)\)/);
 assert.match(home,/gbQuoteBusy\?'Calculating shipping/);
 assert.match(home,/gbQuoteVersion/);
});
test('yoga mat checkout server quotes actual Printify shipping and charges the approved $4.99',async()=>{
 const {default:calculateShipping}=await import('../netlify/functions/calculate-shipping.mjs');
 const originalFetch=globalThis.fetch,originalPrintify=process.env.PRINTIFY_API_TOKEN,originalStripe=process.env.STRIPE_SECRET_KEY;
 process.env.PRINTIFY_API_TOKEN='mock-printify-token';process.env.STRIPE_SECRET_KEY='sk_test_mock';
 const calls=[];
 const goodResponse=(obj)=>new Response(JSON.stringify(obj),{status:200,headers:{'Content-Type':'application/json'}});
 try{
  globalThis.fetch=async(url,opts={})=>{
   calls.push({url,opts});
   if(url.endsWith('/checkout/sessions/cs_test_yogamat')){
    if(opts.method==='POST')return goodResponse({id:'cs_test_yogamat'});
    return goodResponse({id:'cs_test_yogamat',status:'open',payment_status:'unpaid'});
   }
   if(url.includes('/checkout/sessions/cs_test_yogamat/line_items?'))
    return goodResponse({has_more:false,data:[{id:'li_mat',quantity:1,
      price:{product:{metadata:{printify_product_id:'6aa17cf10e017119c60fca91',
      printify_variant_id:'71786'}}}}]});
   if(url.endsWith('/v1/shops/28816619/orders/shipping.json')){
    const body=JSON.parse(opts.body);
    assert.deepEqual(body.line_items,[{product_id:'6aa17cf10e017119c60fca91',variant_id:71786,quantity:1}]);
    assert.equal(body.address_to.country,'CA');
    assert.equal(body.address_to.region,'ON');
    assert.equal(body.address_to.zip,'N2A 0B1');
    return goodResponse({standard:4839});
   }
   throw Error('Unexpected shipping API mock call: '+url);
  };
  const request=new Request('https://preview.example/.netlify/functions/calculate-shipping',{
   method:'POST',headers:{'Content-Type':'application/json'},
   body:JSON.stringify({session_id:'cs_test_yogamat',items:[{name:'Gangster Bougie Foam Yoga Mat',size:'Turquoise • 24" × 72"',qty:1}],
    address:{name:'Customer Example',country:'CA',region:'ON',address1:'100 Example Street',city:'Test City',zip:'N2A 0B1'}})
  });
  const response=await calculateShipping(request);const body=await response.json();
  assert.equal(response.status,200,JSON.stringify(body));
  assert.equal(body.amount,499);
  assert.equal(body.actual_amount,4839);
  assert.equal(body.subsidy,4340);
  assert.equal(calls.filter(x=>x.url.endsWith('/orders/shipping.json')).length,1);
  const posted=calls.find(x=>x.url.endsWith('/checkout/sessions/cs_test_yogamat')&&x.opts.method==='POST');
  assert.ok(posted,'Stripe session shipping was updated');
  const form=new URLSearchParams(posted.opts.body);
  assert.equal(form.get('shipping_options[0][shipping_rate_data][fixed_amount][amount]'),'499');
 }finally{globalThis.fetch=originalFetch;
  if(originalPrintify===undefined)delete process.env.PRINTIFY_API_TOKEN;else process.env.PRINTIFY_API_TOKEN=originalPrintify;
  if(originalStripe===undefined)delete process.env.STRIPE_SECRET_KEY;else process.env.STRIPE_SECRET_KEY=originalStripe;}
});
test('American yoga mat checkout uses the same US$4.99 charge after a US Printify quote',async()=>{
 const {default:calculateShipping}=await import('../netlify/functions/calculate-shipping.mjs');
 const originalFetch=globalThis.fetch,originalPrintify=process.env.PRINTIFY_API_TOKEN,originalStripe=process.env.STRIPE_SECRET_KEY;
 process.env.PRINTIFY_API_TOKEN='mock-printify-token';process.env.STRIPE_SECRET_KEY='sk_test_mock';
 const calls=[];
 const goodResponse=(obj)=>new Response(JSON.stringify(obj),{status:200,headers:{'Content-Type':'application/json'}});
 try{
  globalThis.fetch=async(url,opts={})=>{
   calls.push({url,opts});
   if(url.endsWith('/checkout/sessions/cs_test_yogamat')){
    if(opts.method==='POST')return goodResponse({id:'cs_test_yogamat'});
    return goodResponse({id:'cs_test_yogamat',status:'open',payment_status:'unpaid'});
   }
   if(url.includes('/checkout/sessions/cs_test_yogamat/line_items?'))
    return goodResponse({has_more:false,data:[{id:'li_mat',quantity:1,
      price:{product:{metadata:{printify_product_id:'6aa17cf10e017119c60fca91',
      printify_variant_id:'71786'}}}}]});
   if(url.endsWith('/v1/shops/28816619/orders/shipping.json')){
    const body=JSON.parse(opts.body);
    assert.deepEqual(body.line_items,[{product_id:'6aa17cf10e017119c60fca91',variant_id:71786,quantity:1}]);
    assert.equal(body.address_to.country,'US');
    assert.equal(body.address_to.region,'MI');
    assert.equal(body.address_to.zip,'48201');
    return goodResponse({standard:2200});
   }
   throw Error('Unexpected shipping API mock call: '+url);
  };
  const request=new Request('https://preview.example/.netlify/functions/calculate-shipping',{
   method:'POST',headers:{'Content-Type':'application/json'},
   body:JSON.stringify({session_id:'cs_test_yogamat',items:[{name:'Gangster Bougie Foam Yoga Mat',size:'Turquoise • 24" × 72"',qty:1}],
    address:{name:'Customer Example',country:'US',region:'MI',address1:'100 Example Street',city:'Test City',zip:'48201'}})
  });
  const response=await calculateShipping(request);const body=await response.json();
  assert.equal(response.status,200,JSON.stringify(body));
  assert.equal(body.amount,499);
  assert.equal(body.actual_amount,2200);
  assert.equal(body.subsidy,1701);
  assert.equal(calls.filter(x=>x.url.endsWith('/orders/shipping.json')).length,1);
  const posted=calls.find(x=>x.url.endsWith('/checkout/sessions/cs_test_yogamat')&&x.opts.method==='POST');
  assert.ok(posted,'Stripe session shipping was updated');
  const form=new URLSearchParams(posted.opts.body);
  assert.equal(form.get('shipping_options[0][shipping_rate_data][fixed_amount][amount]'),'499');
 }finally{globalThis.fetch=originalFetch;
  if(originalPrintify===undefined)delete process.env.PRINTIFY_API_TOKEN;else process.env.PRINTIFY_API_TOKEN=originalPrintify;
  if(originalStripe===undefined)delete process.env.STRIPE_SECRET_KEY;else process.env.STRIPE_SECRET_KEY=originalStripe;}
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

test('all physical products are cost-verified, with only one commission per garment type', () => {
 assert.equal(AFFILIATE_COST_PRODUCTS.length,52);
 assert.equal(AFFILIATE_RATE_PRODUCTS.length,21);
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
 assert.equal(AFFILIATE_RATE_MEMBERS['Onyx Sports Bra'].length,13);
 assert.equal(AFFILIATE_RATE_MEMBERS['Onyx Leggings'].length,13);
 assert.equal(AFFILIATE_RATE_MEMBERS['Onyx Workout Shorts'].length,8);
 for(const name of AFFILIATE_COST_PRODUCTS) assert.ok(AFFILIATE_RATE_PRODUCTS.includes(canonicalCommissionName(name)),name);
 for(const name of AFFILIATE_RATE_MEMBERS['Onyx Sports Bra']) assert.equal(canonicalCommissionName(name),'Onyx Sports Bra');
 for(const name of AFFILIATE_RATE_MEMBERS['Onyx Leggings']) assert.equal(canonicalCommissionName(name),'Onyx Leggings');
 for(const name of AFFILIATE_RATE_MEMBERS['Onyx Workout Shorts']) assert.equal(canonicalCommissionName(name),'Onyx Workout Shorts');
 assert.equal(canonicalCommissionName('Gangster Bougie Women’s Signature Crop Tee – Black'),'Gangster Bougie Women’s Signature Crop Tee – Black');
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
 assert.equal(getWorstShippingCents([{variant_ids:[10],countries:['US','CA'],first_item:{currency:'CAD',cost:799}}],[10]).ok,false);
 assert.equal(getWorstShippingCents([{variant_ids:[10],countries:['US','CA'],first_item:{currency:'USD',cost:null}}],[10]).ok,false);
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
 assert.equal(row.estimated_retained_after_commission_cents,1830);
 assert.equal(planProductCommission({
  name:'Unsafe',retailCents:1999,variantCosts:[],shippingByVariant:[],customerContributionCents:299
 }).status,'needs_review');
 assert.equal(planProductCommission({
  name:'Loss-making',retailCents:2000,variantCosts:[{costCents:3000}],
  shippingByVariant:[{firstItemCents:1000}],customerContributionCents:0
 }).status,'needs_review');
});
test('every affiliate product has exact Printify variants and a customer shipping contribution',()=>{
 for(const name of AFFILIATE_COST_PRODUCTS){
   const variants=affiliateMappedVariants(name);
   assert.ok(variants.length>0,'Missing Printify mapping: '+name);
   assert.ok(variants.every(v=>v.productId&&Number.isSafeInteger(v.variantId)&&v.variantId>0),'Invalid variant: '+name);
   assert.ok(Number.isSafeInteger(customerShippingContribution(name)),'Missing customer shipping contribution: '+name);
 }
 assert.equal(customerShippingContribution('Gangster Bougie Women’s Signature Crop Tee – Black'),299);
 assert.equal(customerShippingContribution('Gangster Bougie Women’s Signature Crop Tee – White'),299);
});
test('owner admin has private Printify syncing and proposal approval UI',()=>{
 const admin=readFileSync(new URL('../affiliate-admin.html',import.meta.url),'utf8');
 assert.match(admin,/id="syncPrintifyCosts"/);
 assert.match(admin,/id="syncMatCost"/);
 assert.match(admin,/id="matCostStatus"/);
 assert.match(admin,/id="approvePrintifyCosts"/);
 assert.match(admin,/You keep after commission/);
 assert.match(admin,/id="sharedRateRows"/);
 assert.match(admin,/d\.cost_products/);
 assert.match(admin,/approve_all_cost_rates/);
 assert.match(admin,/sync_printify_costs/);
});

test('mocked Printify API retrieves both bottle sizes and real variant costs before proposing a commission',async()=>{
 const calls=[],productId='6aa0d82a6279c5ea5c03596f';
 const mock=async (url,options)=>{
  calls.push(url);
  assert.equal(options.headers.Authorization,'Bearer TEST_TOKEN');
  let value;
  if(url.endsWith('/products/'+productId+'.json'))value={
   id:productId,blueprint_id:100,print_provider_id:200,
   variants:[{id:76801,cost:2000,is_enabled:true,is_available:true},
             {id:76802,cost:2400,is_enabled:true,is_available:true}]
  };
  else if(url.endsWith('/blueprints/100/print_providers/200/shipping.json'))value={
   profiles:[
    {variant_ids:[76801,76802],countries:['US'],first_item:{currency:'USD',cost:799}},
    {variant_ids:[76801,76802],countries:['CA'],first_item:{currency:'USD',cost:1199}}
   ]
  };
  else throw Error('Unexpected Printify API route: '+url);
  return {ok:true,status:200,json:async()=>value};
 };
 const x=await readPrintifyCost('Stainless Steel Gym Bottle','TEST_TOKEN',mock);
 assert.equal(x.status,'proposal_ready');
 assert.equal(x.production_high_cents,2400);
 assert.equal(x.production_low_cents,2000);
 assert.equal(x.retail_cents,4499);
 assert.equal(x.gb_shipping_subsidy_cents,700);
 assert.equal(x.proposed_commission_cents,200);
 assert.equal(x.cost_variant_count,2);
 assert.equal(calls.length,2);
});
test('mocked two-colour Printify accessory fetch reuses shipping profile across both products',async()=>{
 const ids=['6aa428e6d86adfcd610e9457','6aa16fcea334f4469202f6d7'];
 let productCalls=0,shippingCalls=0;
 const mock=async url=>{
  const id=ids.find(v=>url.endsWith('/products/'+v+'.json'));
  if(id){productCalls++;return {ok:true,json:async()=>({id,blueprint_id:400,print_provider_id:500,variants:[{id:75135,cost:id===ids[0]?300:400,is_enabled:true,is_available:true}]})};}
  if(url.endsWith('/blueprints/400/print_providers/500/shipping.json')){shippingCalls++;return {ok:true,json:async()=>({profiles:[
   {variant_ids:[75135],countries:['US'],first_item:{currency:'USD',cost:250}},
   {variant_ids:[75135],countries:['CA'],first_item:{currency:'USD',cost:350}}
  ]})};}
  throw Error('Unexpected API URL '+url);
 };
 const x=await readPrintifyCost('Gym Face Towel','TEST_TOKEN',mock);
 assert.equal(x.status,'proposal_ready');
 assert.equal(x.production_high_cents,400);
 assert.equal(x.printify_product_ids.length,2);
 assert.equal(productCalls,2);
 assert.equal(shippingCalls,1);
});
test('foam yoga mat retries missing V1 Canada rate against real-format Printify V2 standard shipping',async()=>{
 const ids=['6aa17d76ecf402b473069b65','6aa17cf10e017119c60fca91',
 '6aa17ca22e2c82890e0b1c06','6aa17c5cef297c9cb30b13e7',
 '6aa17bf44e6cc4ad44002904','6aa1778761c176742d02f065'];
 let v2Calls=0;
 const mock=async url=>{
  const id=ids.find(v=>url.endsWith('/products/'+v+'.json'));
  if(id)return {ok:true,json:async()=>({id,blueprint_id:900,print_provider_id:901,
    variants:[{id:71786,cost:5448,is_enabled:true,is_available:true}]})};
  if(url.endsWith('/v1/catalog/blueprints/900/print_providers/901/shipping.json'))
   return {ok:true,json:async()=>({profiles:[{variant_ids:[71786],countries:['US'],
    first_item:{currency:'USD',cost:3900}}]})};
  if(url.endsWith('/v2/catalog/blueprints/900/print_providers/901/shipping/standard.json')){
   v2Calls++;
   return {ok:true,json:async()=>({data:['US','CA'].map(country=>({attributes:{
    shippingType:'standard',variantId:71786,country:{code:country},
    shippingCost:{firstItem:{amount:country==='CA'?4839:3900,currency:'USD'}}
   }}))})};
  }
  throw Error('Unexpected mock route '+url);
 };
 const mat=await readPrintifyCost('Foam Yoga Mat','TEST_TOKEN',mock);
 assert.equal(mat.retail_cents,10499);
 assert.equal(mat.production_high_cents,5448);
 assert.equal(mat.gb_shipping_subsidy_cents,4340);
 assert.equal(mat.estimated_profit_cents,186);
 assert.equal(mat.proposed_commission_cents,0);
 assert.equal(mat.status,'needs_review'); // Excluded: zero proposed payout is intentional.
 assert.match(mat.shipping_source,/V2 standard/);
 assert.equal(v2Calls,1);
});
test('mat with no verified Canada shipping must remain unpriced rather than assume a shipping cost',async()=>{
 const ids=['6aa17d76ecf402b473069b65','6aa17cf10e017119c60fca91',
 '6aa17ca22e2c82890e0b1c06','6aa17c5cef297c9cb30b13e7',
 '6aa17bf44e6cc4ad44002904','6aa1778761c176742d02f065'];
 const mock=async url=>{
  const id=ids.find(v=>url.endsWith('/products/'+v+'.json'));
  if(id)return {ok:true,json:async()=>({id,blueprint_id:900,print_provider_id:901,
   variants:[{id:71786,cost:5448,is_enabled:true,is_available:true}]})};
  if(url.includes('/shipping/standard.json'))return {ok:true,json:async()=>({data:[]})};
  if(url.includes('/shipping.json'))return {ok:true,json:async()=>({profiles:[]})};
  throw Error('Unexpected mock route '+url);
 };
 const mat=await readPrintifyCost('Foam Yoga Mat','TEST_TOKEN',mock);
 assert.equal(mat.status,'needs_review');
 assert.equal(mat.reason,'shipping_profile_missing');
 assert.equal(mat.retail_cents,10499);
 assert.equal(mat.proposed_commission_cents,undefined);
 assert.equal(mat.estimated_profit_cents,undefined);
});
test('Printify importer blocks suggestions when a required variant lacks its actual cost',async()=>{
 const id='6aa0d82a6279c5ea5c03596f';
 const mock=async url=>{
  if(url.endsWith('/products/'+id+'.json'))return {ok:true,json:async()=>({id,blueprint_id:100,print_provider_id:200,variants:[{id:76801,cost:2100,is_enabled:true}]})};
  return {ok:true,json:async()=>({profiles:[]})};
 };
 const x=await readPrintifyCost('Stainless Steel Gym Bottle','TEST_TOKEN',mock);
 assert.equal(x.status,'needs_review');
 assert.equal(x.reason,'printify_variant_cost_missing');
 assert.equal(x.proposed_commission_cents,undefined);
});
test('Printify null production cost cannot be interpreted as zero-cost product',async()=>{
 const id='6aa0d82a6279c5ea5c03596f';
 const mock=async url=>{
  if(url.endsWith('/products/'+id+'.json'))return {ok:true,json:async()=>({id,blueprint_id:100,print_provider_id:200,variants:[
   {id:76801,cost:2000,is_enabled:true},{id:76802,cost:null,is_enabled:true}]})};
  return {ok:true,json:async()=>({profiles:[
   {variant_ids:[76801,76802],countries:['US','CA'],first_item:{currency:'USD',cost:700}}
  ]})};
 };
 const row=await readPrintifyCost('Stainless Steel Gym Bottle','TEST_TOKEN',mock);
 assert.equal(row.status,'needs_review');
 assert.equal(row.reason,'printify_variant_cost_missing');
 assert.equal(row.proposed_commission_cents,undefined);
});

test('one-dollar rounding exception preserves the approved slim-margin leggings example',()=>{
 const leggings=planProductCommission({
  name:'Example higher-cost leggings',retailCents:5999,
  variantCosts:[{costCents:3859}],
  shippingByVariant:[{firstItemCents:1769}],customerContributionCents:399
 });
 assert.equal(leggings.processing_allowance_cents,318);
 assert.equal(leggings.gb_shipping_subsidy_cents,1370);
 assert.equal(leggings.estimated_profit_cents,452);
 assert.equal(leggings.twenty_percent_cents,90);
 assert.equal(leggings.proposed_commission_cents,100);
 assert.equal(leggings.estimated_retained_after_commission_cents,352);
 assert.equal(leggings.rounding_note,'minimum_1_dollar_exception');
 const lowMargin=planProductCommission({
  name:'Example low-margin mat',retailCents:10499,variantCosts:[{costCents:5448}],
  shippingByVariant:[{firstItemCents:4839}],customerContributionCents:499
 });
 assert.equal(lowMargin.estimated_profit_cents,186);
 assert.equal(lowMargin.proposed_commission_cents,0);
 assert.equal(lowMargin.status,'needs_review');
});

test('shared commission uses least profitable garment design and fails closed when one cost is missing',()=>{
 const names=AFFILIATE_RATE_MEMBERS['Onyx Workout Shorts'];
 assert.equal(names.length,8);
 const byName=new Map(names.map((name,i)=>[name,{proposed_commission_cents:i===5?100:200}]));
 assert.equal(conservativeFamilyCommission(names,byName),100);
 byName.delete(names[0]);
 assert.equal(conservativeFamilyCommission(names,byName),null);
});
test('multi-item referral totaling uses the same rate for colourways of bras, leggings and shorts',()=>{
 const sourceRates=new Map([['Onyx Sports Bra',200],['Onyx Leggings',100],['Onyx Workout Shorts',100]]);
 const order=[
 {name:'GB Classic Sports Bra – Cream',quantity:1},
 {name:'Heritage Plaid Sports Bra',quantity:1},
 {name:'GB Classic High-Waisted Leggings – Grey',quantity:2},
 {name:'Shorts – White',quantity:1},
 {name:'Oxblood Workout Shorts',quantity:1}
 ];
 const lines=order.map(x=>({name:x.name,quantity:x.quantity,rate_cents:sourceRates.get(canonicalCommissionName(x.name))}));
 assert.deepEqual(lines.map(x=>x.rate_cents),[200,200,100,100,100]);
 assert.equal(lines.reduce((total,x)=>total+x.quantity*x.rate_cents,0),800);
});


test('explicit low-margin exclusions cover men’s shorts, bottles, mats, socks and bandanas',()=>{
 assert.equal(AFFILIATE_RATE_PRODUCTS.length,21);
 assert.equal(AFFILIATE_ELIGIBLE_RATE_PRODUCTS.length,15);
 assert.equal(AFFILIATE_EXCLUDED_RATE_NAMES.length,6);
 assert.equal(AFFILIATE_EXCLUDED_PRODUCT_NAMES.length,6);
 for(const name of AFFILIATE_EXCLUDED_RATE_NAMES){
  assert.equal(isAffiliateExcluded(name),true);
  assert.equal(AFFILIATE_ELIGIBLE_RATE_PRODUCTS.includes(name),false);
 }
 for(const name of AFFILIATE_ELIGIBLE_RATE_PRODUCTS)assert.equal(isAffiliateExcluded(name),false,name);
 for(const name of [
   'Gangster Bougie Stainless Steel Gym Bottle','Stainless Steel Gym Bottle',
   'Gangster Bougie Foam Yoga Mat','Foam Yoga Mat',
   'Gangster Bougie Mini Wrap Bandana','Mini Wrap Bandana',
   'Crowned Luxury Crew Socks',
   'Onyx/Gold Gangster Bougie Basketball Rib Shorts',
   'Cream/Gold Gangster Bougie Basketball Rib Shorts'
 ])assert.equal(isAffiliateExcluded(name),true,name);
 assert.equal(isAffiliateExcluded('GB Classic High-Waisted Leggings – Black'),false);
 assert.equal(isAffiliateExcluded('Onyx/Gold Crowned Luxury Full-Zip Hoodie'),false);
});
test('server code rejects saved excluded rates and always returns policy-enforced $0',()=>{
 const impl=readFileSync(new URL('../netlify/functions/lib/gb-affiliates.mjs',import.meta.url),'utf8');
 assert.match(impl,/if\(isAffiliateExcluded\(n\)\)return \{ok:false/);
 assert.match(impl,/isAffiliateExcluded\(n\)\?\{name:n,cents:0,excluded:true\}/);
 assert.match(impl,/filter\(rate=>!isAffiliateExcluded\(rate.name\)\)/);
});
test('verified multi-item referral adds eligible rates but pays $0 on excluded items',()=>{
 const lines=[
  commissionLineFromRate({name:'Onyx/Gold Crowned Luxury Full-Zip Hoodie',quantity:1},{cents:300}),
  commissionLineFromRate({name:'GB Classic High-Waisted Leggings – Grey',quantity:2},{cents:100}),
  commissionLineFromRate({name:'Gangster Bougie Stainless Steel Gym Bottle',quantity:1},{cents:0,excluded:true}),
  commissionLineFromRate({name:'Gangster Bougie Foam Yoga Mat',quantity:1},{cents:0,excluded:true}),
 ];
 assert.deepEqual(lines.map(x=>x.commission_cents),[300,200,0,0]);
 assert.deepEqual(lines.map(x=>x.excluded),[false,false,true,true]);
 const summary=summarizeCommissionLines(lines);
 assert.equal(summary.missing_rate,false);
 assert.equal(summary.excluded_only,false);
 assert.equal(summary.commission_total_cents,500);
});
test('excluded-only orders record zero payout; missing eligible rates still need review',()=>{
 const bottle=commissionLineFromRate({name:'Stainless Steel Gym Bottle',quantity:3},{cents:0,excluded:true});
 const socks=commissionLineFromRate({name:'Crowned Luxury Crew Socks',quantity:2},{cents:0,excluded:true});
 assert.deepEqual(summarizeCommissionLines([bottle,socks]),{
  missing_rate:false,excluded_only:true,commission_total_cents:0
 });
 assert.equal(summarizeCommissionLines([bottle,commissionLineFromRate({name:'Unconfigured crop tee',quantity:1},null)]).missing_rate,true);
 assert.equal(summarizeCommissionLines([bottle,commissionLineFromRate({name:'Unconfigured crop tee',quantity:1},null)]).commission_total_cents,null);
});
test('affiliate terms disclose excluded product categories before sign-up and item lines show $0',()=>{
 const affiliate=readFileSync(new URL('../affiliate.html',import.meta.url),'utf8');
 const admin=readFileSync(new URL('../affiliate-admin.html',import.meta.url),'utf8');
 const ledger=readFileSync(new URL('../netlify/functions/lib/gb-affiliates.mjs',import.meta.url),'utf8');
 const sync=readFileSync(new URL('../netlify/functions/lib/gb-affiliate-cost-sync.mjs',import.meta.url),'utf8');
 assert.match(affiliate,/id="affiliateExclusions"/);
 assert.match(affiliate,/Stainless steel gym bottles \(12 oz and 18 oz\)/);
 assert.match(affiliate,/Foam yoga mats \(all colours\)/);
 assert.match(affiliate,/excluded — \$0/);
 assert.match(admin,/EXCLUDED — \$0/);
 assert.match(ledger,/excluded_only/);
 assert.match(sync,/AFFILIATE_ELIGIBLE_RATE_PRODUCTS/);
});

test('complete paid Stripe session line items include every product, not the first handful',async()=>{
 const observed=[];
 const items=Array.from({length:12},(_,i)=>({
  id:'li_'+i,quantity:i%3+1,
  price:{product:{id:'prod_'+i,metadata:{storefront_name:'Product '+i}}}
 }));
 const fetcher=async (url,opts)=>{
  observed.push(url);
  assert.match(opts.headers.Authorization,/^Bearer sk_test_mock$/);
  assert.match(url,/\/line_items\?/);
  return {ok:true,json:async()=>({data:items,has_more:false})};
 };
 const got=await retrieveAllStripeLineItems('cs_test_mock','sk_test_mock',fetcher);
 assert.equal(got.length,12);
 assert.equal(got[11].price.product.metadata.storefront_name,'Product 11');
 assert.equal(observed.length,1);
});
test('Stripe line item pagination is complete, duplicate-safe and fails closed',async()=>{
 let n=0;
 const fetcher=async (url)=>{
  const query=new URL(url).searchParams;
  n++;
  if(n===1){
   assert.equal(query.get('starting_after'),null);
   return {ok:true,json:async()=>({has_more:true,data:[{id:'li_1',quantity:1,price:{product:{id:'p_1'}}}]})};
  }
  assert.equal(query.get('starting_after'),'li_1');
  return {ok:true,json:async()=>({has_more:false,data:[{id:'li_2',quantity:2,price:{product:{id:'p_2'}}}]})};
 };
 const rows=await retrieveAllStripeLineItems('cs_test_mock','sk_test_mock',fetcher);
 assert.deepEqual(rows.map(x=>x.id),['li_1','li_2']);
 const bad=async()=>({ok:true,json:async()=>({data:[{id:'li_1',quantity:1,price:{product:'prod_not_expanded'}}],has_more:false})});
 await assert.rejects(retrieveAllStripeLineItems('cs_test_mock','sk_test_mock',bad),/stripe_line_items_missing_product_metadata/);
 const insufficient=async()=>({ok:true,json:async()=>({data:[],has_more:true})});
 await assert.rejects(retrieveAllStripeLineItems('cs_test_mock','sk_test_mock',insufficient),/pagination_failed/);
});
