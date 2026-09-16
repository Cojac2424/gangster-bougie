from pathlib import Path

p=Path('index.html')
s=p.read_text()

# v65 — mobile sticky navigation refinement.
# Keeps Build Your Fit geometry, product logic, catalog and cart behavior untouched.
# Removes only the Lookbook nav entry, centers Build Your Fit, and adds a lightweight gold jeweled cart icon.
if 'Mobile nav refinement v65' not in s:
    css=r'''
<style>/* Mobile nav refinement v65 */
.gb-jeweled-cart{display:inline-flex;width:22px;height:19px;vertical-align:-4px;margin-right:5px;flex:0 0 auto}
.gb-jeweled-cart svg{width:100%;height:100%;overflow:visible}
.gb-jeweled-cart .cart-stroke{fill:none;stroke:#e5b83d;stroke-width:1.7;stroke-linecap:round;stroke-linejoin:round;filter:drop-shadow(0 0 2px rgba(229,184,61,.4))}
.gb-jeweled-cart .gem{fill:#ffe68b;stroke:#c9961d;stroke-width:.65}
.gb-jeweled-cart .spark{fill:#fff0ad}
@media(max-width:760px){
 .nav-links{display:grid!important;grid-template-columns:minmax(0,1fr) minmax(0,1fr) minmax(108px,1.45fr) minmax(0,1fr) minmax(0,1.15fr)!important;align-items:center!important;gap:5px!important;width:100%!important}
 .nav-links>a{min-width:0!important;text-align:center!important;justify-content:center!important;white-space:nowrap!important;font-size:clamp(.56rem,2.45vw,.72rem)!important;padding-left:2px!important;padding-right:2px!important}
 .nav-links .byf-nav-link{grid-column:3!important;padding:8px 6px!important;font-size:clamp(.56rem,2.35vw,.69rem)!important}
 .nav-links #gbCartLink{display:flex!important;align-items:center!important;gap:2px!important;padding:7px 3px!important}
}
</style>
'''
    js=r'''
<script>/* Mobile nav refinement v65 */
(function(){
 function install(){
  const nav=document.querySelector('.nav-links');if(!nav)return;
  // Remove only the Lookbook navigation link; the actual Lookbook section remains intact.
  [...nav.querySelectorAll('a')].forEach(function(a){if((a.textContent||'').trim().toLowerCase()==='lookbook')a.remove()});
  let byf=nav.querySelector('.byf-nav-link');
  if(!byf){byf=document.createElement('a');byf.className='byf-nav-link';byf.href='#build-your-fit';byf.textContent='Build Your Fit'}
  const links=[...nav.querySelectorAll('a')];
  function find(label){return links.find(a=>(a.textContent||'').trim().toLowerCase().startsWith(label))}
  const shop=find('shop'),about=find('about'),contact=find('contact'),cart=nav.querySelector('#gbCartLink')||find('cart');
  // Exact requested order: Shop, About, Build Your Fit, Contact, Cart.
  [shop,about,byf,contact,cart].forEach(function(el){if(el)nav.appendChild(el)});
  if(cart&&!cart.querySelector('.gb-jeweled-cart')){
   const icon=document.createElement('span');icon.className='gb-jeweled-cart';icon.setAttribute('aria-hidden','true');
   icon.innerHTML='<svg viewBox="0 0 24 20" xmlns="http://www.w3.org/2000/svg"><path class="cart-stroke" d="M1.5 2h2.4l2.1 10.2h11.8l2.3-7.4H5.1M7.2 15.6h.1M17.1 15.6h.1"/><circle class="cart-stroke" cx="7.3" cy="16.2" r="1.35"/><circle class="cart-stroke" cx="17.2" cy="16.2" r="1.35"/><path class="gem" d="M8 6.2l1.6-1.5 1.7 1.5-1.7 2.1z"/><path class="gem" d="M12.2 6.2l1.6-1.5 1.7 1.5-1.7 2.1z"/><path class="spark" d="M18.7 1.2l.45 1.05 1.05.45-1.05.45-.45 1.05-.45-1.05-1.05-.45 1.05-.45z"/></svg>';
   cart.insertBefore(icon,cart.firstChild);
  }
 }
 if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',install);else install();
})();
</script>
'''
    s=s.replace('</head>',css+'\n</head>')
    s=s.replace('</body>',js+'\n</body>')

p.write_text(s)
