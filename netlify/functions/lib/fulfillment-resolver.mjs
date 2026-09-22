import { VERIFIED_ACTIVEWEAR_PRODUCTS } from './verified-activewear-fulfillment.mjs';
import { VERIFIED_MENS_PRODUCTS } from './verified-mens-fulfillment.mjs';
import { VERIFIED_ACCESSORIES_PRODUCTS, VERIFIED_TRAVEL_BAGS } from './verified-accessories-fulfillment.mjs';

// Server-side fulfillment resolver. It never creates an order.
// It only translates a storefront name + selected option into an exact Printify product/variant pair.
const ALL={...VERIFIED_ACTIVEWEAR_PRODUCTS,...VERIFIED_MENS_PRODUCTS,...VERIFIED_ACCESSORIES_PRODUCTS,...VERIFIED_TRAVEL_BAGS};
const ALIASES={
 'Gangster Bougie Stainless Steel Gym Bottle':'Stainless Steel Gym Bottle',
 'Gangster Bougie Gym Face Towel':'Gym Face Towel',
 'Gangster Bougie Gym Bag':'Gym Bag',
 'Gangster Bougie Foam Yoga Mat':'Foam Yoga Mat',
 'Gangster Bougie GB Faux Leather Travel Bag':'GB Faux Leather Travel Bag',
 'Gangster Bougie “Baddie” Faux Leather Travel Bag':'“Baddie” Faux Leather Travel Bag',
 'Gangster Bougie Mini Wrap Bandana':'Mini Wrap Bandana',
 'Gangster Bougie Embroidered Structured Cap':'Embroidered Structured Cap'
};
function canonicalName(name){const n=String(name||'').trim();return ALIASES[n]||n;}
function text(v){return String(v||'').trim();}
function findKey(haystack,keys){
 const h=text(haystack).toLowerCase();
 return keys.find(k=>h.includes(String(k).toLowerCase()))||null;
}
export function resolveFulfillment(name,option=''){
 const key=canonicalName(name), p=ALL[key];
 if(!p) return {ok:false,error:'unmapped_product',name:key};
 if(p.sizes){
   let wanted=findKey(option,Object.keys(p.sizes));
   // Normalize bottle storefront spacing: "12 oz" / "18 oz" -> mapping "12oz" / "18oz".
   if(!wanted){const compact=text(option).replace(/\s+/g,'');wanted=findKey(compact,Object.keys(p.sizes));}
   if(!wanted) return {ok:false,error:'unmapped_size',name:key,option:text(option)};
   return {ok:true,name:key,product_id:p.product_id,variant_id:p.sizes[wanted],selection:wanted};
 }
 if(p.colors){
   const color=findKey(option,Object.keys(p.colors));
   if(!color) return {ok:false,error:'unmapped_color',name:key,option:text(option)};
   const v=p.colors[color];
   if(typeof v==='number') return {ok:true,name:key,product_id:p.product_id,variant_id:v,selection:color};
   return {ok:true,name:key,product_id:v.product_id,variant_id:v.variant_id,selection:color};
 }
 if(p.variant_id) return {ok:true,name:key,product_id:p.product_id,variant_id:p.variant_id,selection:text(option)||'One Size'};
 return {ok:false,error:'invalid_mapping',name:key};
}
export function resolveCart(items){
 if(!Array.isArray(items)) return {ok:false,error:'invalid_cart',items:[]};
 const resolved=items.map(x=>({...resolveFulfillment(x?.name,x?.size),quantity:Math.max(1,Math.min(20,Math.floor(Number(x?.qty)||1)))}));
 const bad=resolved.filter(x=>!x.ok);
 return {ok:bad.length===0,error:bad.length?'unresolved_items':null,items:resolved,unresolved:bad};
}
