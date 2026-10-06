/* Gangster Bougie GA4 ecommerce tracking */
(function(){
  'use strict';
  var CURRENCY='USD';
  function send(name,params){if(typeof window.gtag==='function')window.gtag('event',name,params||{});}
  function moneyText(v){var m=String(v||'').replace(/,/g,'').match(/([0-9]+(?:\.[0-9]+)?)/);return m?Number(m[1]):0;}
  function item(name,variant,price,qty){return {item_name:String(name||'Gangster Bougie Item').trim(),item_variant:String(variant||'').trim(),price:Number(price)||0,quantity:Number(qty)||1};}
  function cart(){
    try{return JSON.parse(localStorage.getItem('gbCart')||'[]').map(function(x){return item(x.name,x.size,x.price,x.qty);});}catch(_){return [];}
  }
  function value(items){return items.reduce(function(n,x){return n+(Number(x.price)||0)*(Number(x.quantity)||1);},0);}
  function visibleProduct(){
    var m=document.querySelector('#gbWomenQuick.open,#gbMenQuick.open,.modal.open');
    if(!m)return null;
    var nameEl=m.querySelector('#gbWqName,#gbMqName,h2,h3,.product-title,.sports-title');
    var priceEl=m.querySelector('#gbWqPrice,#gbMqPrice,.sports-price,.product-price,.price');
    var sizeEl=m.querySelector('.gb-wq-size.active,.gb-mq-size.active,.sports-size.active,.active[data-size],select');
    return item(nameEl&&nameEl.textContent,sizeEl&&(sizeEl.value||sizeEl.textContent),moneyText(priceEl&&priceEl.textContent),1);
  }
  function cardProduct(card){
    if(!card)return null;
    var n=card.querySelector('.gb-women-name,.gb-men-name,.gb-access-name,.product-name,h3,h2');
    var p=card.querySelector('.gb-women-price,.gb-men-price,.gb-access-price,.product-price,.price');
    return item(n&&n.textContent,'',moneyText(p&&p.textContent),1);
  }
  document.addEventListener('click',function(e){
    var view=e.target.closest('.gb-women-view,.gb-men-view,.gb-access-view,.view-item');
    if(view){
      var cp=cardProduct(view.closest('.gb-women-card,.gb-men-card,.gb-access-card,.product-card'));
      if(cp)send('view_item',{currency:CURRENCY,value:cp.price,items:[cp]});
      return;
    }
    var add=e.target.closest('#gbWqAdd,#gbMqAdd,.sports-add');
    if(add){
      var before=cart(),beforeCount=before.reduce(function(n,x){return n+x.quantity;},0);
      setTimeout(function(){
        var after=cart(),afterCount=after.reduce(function(n,x){return n+x.quantity;},0);
        if(afterCount>beforeCount){
          var p=visibleProduct()||after[after.length-1];
          if(p)send('add_to_cart',{currency:CURRENCY,value:p.price,items:[p]});
        }
      },0);
    }
    if(e.target.closest('#byfAddFit')){
      var beforeFit=cart();
      setTimeout(function(){
        var afterFit=cart(),added=afterFit.slice(beforeFit.length);
        if(added.length)send('add_to_cart',{currency:CURRENCY,value:value(added),items:added});
      },0);
    }
  },false);
  document.addEventListener('gb:checkout-start',function(){
    var items=cart();if(items.length)send('begin_checkout',{currency:CURRENCY,value:value(items),items:items});
  });
  function purchase(){
    var q=new URLSearchParams(location.search),sid=q.get('session_id');
    if(q.get('checkout')!=='success'||!sid)return;
    var key='gbGa4Purchase:'+sid;if(sessionStorage.getItem(key))return;
    var raw=sessionStorage.getItem('gbGa4CheckoutCart'),items=[];
    try{items=JSON.parse(raw||'[]');}catch(_){}
    if(!items.length)items=cart();
    send('purchase',{transaction_id:sid,currency:CURRENCY,value:value(items),items:items});
    sessionStorage.setItem(key,'1');sessionStorage.removeItem('gbGa4CheckoutCart');
  }
  if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',purchase);else purchase();
  window.gbGa4SnapshotCheckout=function(){
    var items=cart();
    try{sessionStorage.setItem('gbGa4CheckoutCart',JSON.stringify(items));}catch(_){}
    document.dispatchEvent(new CustomEvent('gb:checkout-start'));
  };
})();