from pathlib import Path

p=Path('index.html')
s=p.read_text()

# v66 — persistent jeweled cart + responsive cart pill containment.
# Keeps all Build Your Fit geometry and commerce behavior untouched.
if 'Persistent jeweled cart v66' not in s:
    css=r'''
<style>/* Persistent jeweled cart v66 */
#gbCartLink{box-sizing:border-box!important;display:inline-flex!important;align-items:center!important;justify-content:center!important;gap:6px!important;white-space:nowrap!important;width:auto!important;min-width:max-content!important;padding-left:12px!important;padding-right:14px!important;overflow:visible!important}
#gbCartLink .gb-jeweled-cart{display:inline-flex!important;align-items:center!important;justify-content:center!important;width:22px!important;height:19px!important;margin:0!important;flex:0 0 22px!important;position:static!important;transform:none!important}
#gbCartLink .gb-jeweled-cart svg{display:block!important;width:22px!important;height:19px!important;overflow:visible!important}
#gbCartLink .gb-jeweled-cart .cart-stroke{fill:none;stroke:#e5b83d;stroke-width:1.7;stroke-linecap:round;stroke-linejoin:round;filter:drop-shadow(0 0 2px rgba(229,184,61,.4))}
#gbCartLink .gb-jeweled-cart .gem{fill:#ffe68b;stroke:#c9961d;stroke-width:.65}
#gbCartLink .gb-jeweled-cart .spark{fill:#fff0ad}
@media(max-width:760px){
 .nav-links{grid-template-columns:minmax(0,.9fr) minmax(0,.9fr) minmax(108px,1.4fr) minmax(0,.95fr) minmax(94px,1.25fr)!important;gap:4px!important}
 .nav-links #gbCartLink{min-width:94px!important;max-width:none!important;padding:7px 7px!important;gap:4px!important;font-size:clamp(.53rem,2.25vw,.68rem)!important;justify-self:stretch!important}
 .nav-links #gbCartLink .gb-jeweled-cart{width:19px!important;height:17px!important;flex-basis:19px!important}
 .nav-links #gbCartLink .gb-jeweled-cart svg{width:19px!important;height:17px!important}
}
@media(min-width:761px) and (max-width:1180px){#gbCartLink{padding-left:11px!important;padding-right:13px!important;gap:5px!important;min-width:112px!important}}
</style>
'''
    js=r'''
<script>/* Persistent jeweled cart v66 */
(function(){
 const ICON='<span class="gb-jeweled-cart" aria-hidden="true"><svg viewBox="0 0 24 20" xmlns="http://www.w3.org/2000/svg"><path class="cart-stroke" d="M1.5 2h2.4l2.1 10.2h11.8l2.3-7.4H5.1M7.2 15.6h.1M17.1 15.6h.1"/><circle class="cart-stroke" cx="7.3" cy="16.2" r="1.35"/><circle class="cart-stroke" cx="17.2" cy="16.2" r="1.35"/><path class="gem" d="M8 6.2l1.6-1.5 1.7 1.5-1.7 2.1z"/><path class="gem" d="M12.2 6.2l1.6-1.5 1.7 1.5-1.7 2.1z"/><path class="spark" d="M18.7 1.2l.45 1.05 1.05.45-1.05.45-.45 1.05-.45-1.05-1.05-.45 1.05-.45z"/></svg></span>';
 let repairing=false;
 function ensureIcon(){
  const cart=document.getElementById('gbCartLink');if(!cart||repairing)return;
  if(!cart.querySelector('.gb-jeweled-cart')){
   repairing=true;
   cart.insertAdjacentHTML('afterbegin',ICON);
   repairing=false;
  }
 }
 function install(){
  ensureIcon();
  const nav=document.querySelector('.nav-links');
  if(nav){new MutationObserver(function(){ensureIcon()}).observe(nav,{subtree:true,childList:true,characterData:true})}
  // Existing cart refreshes can rewrite the link text; re-apply icon immediately afterward.
  let tries=0;
  const hook=setInterval(function(){
   ensureIcon();tries++;
   if(window.gbCartRefresh&&!window.gbCartRefresh.__gbIconHooked){
    const original=window.gbCartRefresh;
    const wrapped=function(){const r=original.apply(this,arguments);ensureIcon();requestAnimationFrame(ensureIcon);return r};
    wrapped.__gbIconHooked=true;window.gbCartRefresh=wrapped;clearInterval(hook)
   }else if(tries>80)clearInterval(hook)
  },100);
  document.addEventListener('click',function(e){if(e.target.closest('#gbCartLink')||e.target.closest('.gb-cart-close'))setTimeout(ensureIcon,0)},true);
 }
 if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',install);else install();
})();
</script>
'''
    s=s.replace('</head>',css+'\n</head>')
    s=s.replace('</body>',js+'\n</body>')

p.write_text(s)
