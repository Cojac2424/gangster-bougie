// Printify order builder for verified Gangster Bougie carts.
// SAFETY: builds/validates payload only. It does NOT call Printify or create an order.
import { resolveCart } from './fulfillment-resolver.mjs';

export function buildPrintifyOrder({items,shipping,external_id,label='Gangster Bougie'}){
 const mapped=resolveCart(items);
 if(!mapped.ok)return {ok:false,error:'unresolved_items',unresolved:mapped.unresolved};
 const s=shipping||{};
 const required=['first_name','last_name','email','phone','country','region','address1','city','zip'];
 const missing=required.filter(k=>!String(s[k]||'').trim());
 if(missing.length)return {ok:false,error:'missing_shipping_fields',missing};
 return {ok:true,payload:{
   external_id:String(external_id||'').slice(0,100),
   label:String(label).slice(0,100),
   line_items:mapped.items.map(x=>({product_id:x.product_id,variant_id:x.variant_id,quantity:x.quantity})),
   shipping_method:1,
   send_shipping_notification:false,
   address_to:{
     first_name:s.first_name,last_name:s.last_name,email:s.email,phone:s.phone,
     country:s.country,region:s.region,address1:s.address1,address2:s.address2||'',
     city:s.city,zip:s.zip
   }
 }};
}
