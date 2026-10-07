/* Gangster Bougie GA4 ecommerce tracking */
(function(){
  'use strict';
  var CURRENCY='USD';
  var META_PIXEL_ID='4066826013612662';
  (function(f,b,e,v,n,t,s){
    if(f.fbq)return;n=f.fbq=function(){n.callMethod?n.callMethod.apply(n,arguments):n.queue.push(arguments)};
    if(!f._fbq)f._fbq=n;n.push=n;n.loaded=!0;n.version='2.0';n.queue=[];
    t=b.createElement(e);t.async=!0;t.src=v;s=b.getElementsByTagName(e)[0];s.parentNode.insertBefore(t,s);
  })(window,document,'script','https://connect.facebook.net/en_US/fbevents.js');
  window.fbq('init',META_PIXEL_ID);
  window.fbq('track','PageView');
  function send(name,params){if(typeof window.gtag==='function')window.gtag('event',name,params||{});}
  function source(){
    var q=new URLSearchParams(location.search),u=(q.get('utm_source')||'').trim();
    if(u)return u;
    var r=document.referrer||'',h='';try{h=new URL(r).hostname.toLowerCase()}catch(_){}
    if(/tiktok/.test(h))return 'TikTok';if(/instagram/.test(h))return 'Instagram';if(/facebook|fb\\.com|l\\.facebook/.test(h))return 'Facebook';if(/google/.test(h))return 'Google';return h||'Direct / Unknown';
  }
  function device(){var u=navigator.userAgent||'';if(/iPad/.test(u)||(/Macintosh/.test(u)&&navigator.maxTouchPoints>1))return 'iPad';if(/iPhone/.test(u))return 'iPhone';if(/Android/.test(u))return 'Android';return /Mobi/.test(u)?'Mobile':'Desktop';}
  function browser(){var u=navigator.userAgent||'';if(/Edg\\//.test(u))return 'Edge';if(/CriOS|Chrome\\//.test(u))return 'Chrome';if(/FxiOS|Firefox\\//.test(u))return 'Firefox';if(/Safari\\//.test(u))return 'Safari';return 'Other';}
  function alertAdmin(event,p){
    p=p||{};var body={event:event,source:source(),referrer:document.referrer||'',device:device(),browser:browser(),items:(p.items||[]).map(function(x){return {name:x.item_name,variant:x.item_variant,price:x.price,quantity:x.quantity};}),value:p.value==null?null:p.value};
    try{fetch('/.netlify/functions/activity-alert',{method:'POST',headers:{'Content-Type':'application/json'},credentials:'same-origin',cache:'no-store',body:JSON.stringify(body),keepalive:true}).then(function(r){if(!r.ok)console.error('GB activity alert HTTP '+r.status);}).catch(function(e){console.error('GB activity alert request failed',e);});}catch(e){console.error('GB activity alert request failed',e);}
  }
  function meta(name,p){
    if(typeof window.fbq!=='function'||!p)return;
    var items=p.items||[];
    var mp={currency:p.currency||CURRENCY,value:Number(p.value)||0,content_type:'product',contents:items.map(function(x){return {id:x.item_name,quantity:Number(x.quantity)||1,item_price:Number(x.price)||0};}),content_ids:items.map(function(x){return x.item_name;})};
    window.fbq('track',name,mp);
  }
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
  alertAdmin('visit',{});
  document.addEventListener('click',function(e){
    var view=e.target.closest('.gb-women-view,.gb-men-view,.gb-access-view,.view-item');
    if(view){
      var cp=cardProduct(view.closest('.gb-women-card,.gb-men-card,.gb-access-card,.product-card'));
      if(cp){var vp={currency:CURRENCY,value:cp.price,items:[cp]};send('view_item',vp);meta('ViewContent',vp);alertAdmin('view_item',vp);}
      return;
    }
    var add=e.target.closest('#gbWqAdd,#gbMqAdd,.sports-add');
    if(add){
      var before=cart(),beforeCount=before.reduce(function(n,x){return n+x.quantity;},0);
      setTimeout(function(){
        var after=cart(),afterCount=after.reduce(function(n,x){return n+x.quantity;},0);
        if(afterCount>beforeCount){
          var p=visibleProduct()||after[after.length-1];
          if(p){var ap={currency:CURRENCY,value:p.price,items:[p]};send('add_to_cart',ap);meta('AddToCart',ap);alertAdmin('add_to_cart',ap);}
        }
      },0);
    }
    if(e.target.closest('#byfAddFit')){
      var beforeFit=cart();
      setTimeout(function(){
        var afterFit=cart(),added=afterFit.slice(beforeFit.length);
        if(added.length){var fp={currency:CURRENCY,value:value(added),items:added};send('add_to_cart',fp);meta('AddToCart',fp);alertAdmin('add_to_cart',fp);}
      },0);
    }
  },true);
  document.addEventListener('gb:checkout-start',function(){
    var items=cart();if(items.length){var cp={currency:CURRENCY,value:value(items),items:items};send('begin_checkout',cp);meta('InitiateCheckout',cp);alertAdmin('begin_checkout',cp);}
  });
  function purchase(){
    var q=new URLSearchParams(location.search),sid=q.get('session_id');
    if(q.get('checkout')!=='success'||!sid)return;
    var key='gbGa4Purchase:'+sid;if(sessionStorage.getItem(key))return;
    var raw=sessionStorage.getItem('gbGa4CheckoutCart'),items=[];
    try{items=JSON.parse(raw||'[]');}catch(_){}
    if(!items.length)items=cart();
    var pp={transaction_id:sid,currency:CURRENCY,value:value(items),items:items};send('purchase',pp);meta('Purchase',pp);
    sessionStorage.setItem(key,'1');sessionStorage.removeItem('gbGa4CheckoutCart');
  }
  if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',purchase);else purchase();
  window.gbGa4SnapshotCheckout=function(){
    var items=cart();
    try{sessionStorage.setItem('gbGa4CheckoutCart',JSON.stringify(items));}catch(_){}
    document.dispatchEvent(new CustomEvent('gb:checkout-start'));
  };
})();