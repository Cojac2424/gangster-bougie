import test from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { Script } from 'node:vm';
import { PRICE_CENTS, VARIABLE_PRICES, SELLABLE_PRODUCT_NAMES } from '../netlify/functions/lib/gb-product-catalog.mjs';
import { normalizeReferralCode, referralExpiryMs, referralIsValid, commissionForPaidItems, commissionTotalCents, commissionHoldUntil, REFERRAL_WINDOW_DAYS, COMMISSION_HOLD_DAYS } from '../netlify/functions/lib/gb-affiliate-rules.mjs';

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
