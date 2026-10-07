(function(){
 'use strict';
 function sendVisitorEmail(){
  try{
   fetch('/.netlify/functions/visitor-email',{
    method:'POST',
    headers:{'Content-Type':'application/json'},
    credentials:'same-origin',
    cache:'no-store',
    keepalive:true,
    body:JSON.stringify({
     path:location.pathname+location.search,
     referrer:document.referrer||'',
     ua:navigator.userAgent||''
    })
   }).catch(function(){});
  }catch(_){}
 }
 if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',sendVisitorEmail,{once:true});
 else sendVisitorEmail();
})();