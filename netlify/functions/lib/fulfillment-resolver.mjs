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
// Match sizes/capacities as complete tokens; XL and 2XL must never resolve to L.
function findSizeKey(option,keys){
 const h=text(option).toLowerCase().replace(/\s+/g,'');
 for(const key of [...keys].sort((a,b)=>String(b).length-String(a).length)){
  const k=String(key).toLowerCase().replace(/\s+/g,'');
  let at=h.indexOf(k);
  while(at!==-1){
   const before=at===0?'':h[at-1],after=h[at+k.length]||'';
   if(!/[a-z0-9]/.test(before)&&!/[a-z0-9]/.test(after))return key;
   at=h.indexOf(k,at+1);
  }
 }
 return null;
}
export function resolveFulfillment(name,option=''){
 const key=canonicalName(name), p=ALL[key];
 if(!p) return {ok:false,error:'unmapped_product',name:key};
 if(p.sizes){
   const wanted=findSizeKey(option,Object.keys(p.sizes));
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

/**
 * Read-only list of exact configured Printify variants for a commissionable product.
 * Used by the owner-only Printify cost sync, never by public checkout.
 */
export function affiliateMappedVariants(name){
 const key=canonicalName(name),entry=ALL[key];if(!entry)return [];
 const rows=[];
 if(entry.sizes)for(const [option,variantId] of Object.entries(entry.sizes))rows.push({productId:entry.product_id,variantId:Number(variantId),option});
 else if(entry.colors)for(const [option,value] of Object.entries(entry.colors))rows.push({
  productId:typeof value==='number'?entry.product_id:value.product_id,
  variantId:Number(typeof value==='number'?value:value.variant_id),option
 });
 else if(entry.variant_id)rows.push({productId:entry.product_id,variantId:Number(entry.variant_id),option:'One Size'});
 return rows.filter(r=>r.productId&&Number.isSafeInteger(r.variantId)&&r.variantId>0);
}
