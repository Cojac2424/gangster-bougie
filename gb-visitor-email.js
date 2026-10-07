(function(){
 'use strict';

 function moneyText(v){
  var m=String(v||'').replace(/,/g,'').match(/([0-9]+(?:\.[0-9]+)?)/);
  return m?Number(m[1]):0;
 }
 function item(name,variant,price,qty){
  return {name:String(name||'Gangster Bougie Item').trim(),variant:String(variant||'').trim(),price:Number(price)||0,quantity:Number(qty)||1};
 }
 function cart(){
  try{return JSON.parse(localStorage.getItem('gbCart')||'[]').map(function(x){return item(x.name,x.size,x.price,x.qty);});}
  catch(_){return [];}
 }
 function total(items){
  return (items||[]).reduce(function(n,x){return n+(Number(x.price)||0)*(Number(x.quantity)||1);},0);
 }
 function source(){
  var q=new URLSearchParams(location.search),u=(q.get('utm_source')||'').trim();
  if(u)return u;
  var h='';try{h=new URL(document.referrer||'').hostname.toLowerCase();}catch(_){}
  if(/tiktok/.test(h))return 'TikTok';
  if(/instagram/.test(h))return 'Instagram';
  if(/facebook|fb\.com|l\.facebook/.test(h))return 'Facebook';
  if(/google/.test(h))return 'Google';
  return h||'Direct / Unknown';
 }
 function post(event,p){
  p=p||{};
  try{
   fetch('/.netlify/functions/visitor-email',{
    method:'POST',
    headers:{'Content-Type':'application/json'},
    credentials:'same-origin',
    cache:'no-store',
    keepalive:true,
    body:JSON.stringify({
     event:event,
     path:location.pathname+location.search,
     referrer:document.referrer||'',
     source:source(),
     ua:navigator.userAgent||'',
     items:p.items||[],
     value:p.value==null?null:p.value
    })
   }).catch(function(){});
  }catch(_){}
 }
 function cardProduct(card){
  if(!card)return null;
  var n=card.querySelector('.gb-women-name,.gb-men-name,.gb-access-name,.product-name,h3,h2');
  var p=card.querySelector('.gb-women-price,.gb-men-price,.gb-access-price,.product-price,.price');
  return item(n&&n.textContent,'',moneyText(p&&p.textContent),1);
 }
 function addedItems(before,after){
  var seen={};
  (before||[]).forEach(function(x){
   var k=String(x.name)+'|'+String(x.variant);
   seen[k]=(seen[k]||0)+(Number(x.quantity)||1);
  });
  var out=[];
  (after||[]).forEach(function(x){
   var k=String(x.name)+'|'+String(x.variant);
   var prev=seen[k]||0,now=Number(x.quantity)||1,diff=Math.max(0,now-prev);
   seen[k]=Math.max(prev,now);
   if(diff)out.push(item(x.name,x.variant,x.price,diff));
  });
  return out;
 }
 function sendVisit(){post('visit',{});}

 if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',sendVisit,{once:true});
 else sendVisit();

 document.addEventListener('click',function(e){
  var view=e.target.closest('.gb-women-view,.gb-men-view,.gb-access-view,.view-item');
  if(view){
   var cp=cardProduct(view.closest('.gb-women-card,.gb-men-card,.gb-access-card,.product-card'));
   if(cp)post('view_item',{items:[cp],value:cp.price});
  }

  var add=e.target.closest('#gbWqAdd,#gbMqAdd,.sports-add,#byfAddFit');
  if(add){
   var before=cart();
   setTimeout(function(){
    var after=cart(),added=addedItems(before,after);
    if(added.length)post('add_to_cart',{items:added,value:total(added)});
   },75);
  }
 },true);

 document.addEventListener('gb:checkout-start',function(){
  var items=cart();
  if(items.length)post('begin_checkout',{items:items,value:total(items)});
 });
})();