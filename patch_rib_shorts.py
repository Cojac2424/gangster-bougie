from pathlib import Path

p=Path('index.html')
s=p.read_text()

# v62 — price parity: every Classic Sports Bra is US$39.99 everywhere.
# Updates View This Fit display and cart data/calculation for Classic bras.
# No product images, details, sizes, Build Your Fit geometry, joins, arrows, or leggings pricing changed.
if 'Classic sports bra price parity v62' not in s:
    js=r'''
<script>/* Classic sports bra price parity v62 */
(function(){
 const PRICE=39.99;
 function isClassicBra(name){return /^GB Classic Sports Bra\s*[–-]\s*/.test((name||'').trim())}
 function fixFitPrice(){
  const n=document.getElementById('byfShopTopName');if(!n||!isClassicBra(n.textContent))return;
  const item=n.closest('.byf-fit-item');if(!item)return;
  const price=item.querySelector('.byf-fit-price');if(price)price.textContent='US$39.99';
 }
 function fixStoredCart(){
  try{
   const cart=JSON.parse(localStorage.getItem('gbCart')||'[]');let changed=false;
   cart.forEach(function(line){if(line&&isClassicBra(line.name)&&Number(line.price)!==PRICE){line.price=PRICE;changed=true}});
   if(changed){localStorage.setItem('gbCart',JSON.stringify(cart));if(window.gbCartRefresh)window.gbCartRefresh()}
  }catch(e){}
 }
 function settle(){requestAnimationFrame(function(){fixFitPrice();fixStoredCart()})}
 function install(){
  fixFitPrice();fixStoredCart();
  const n=document.getElementById('byfShopTopName');if(n&&window.MutationObserver)new MutationObserver(settle).observe(n,{childList:true,characterData:true,subtree:true});
  const panel=document.getElementById('byfFitPanel');if(panel)panel.addEventListener('click',function(e){
   if(e.target.closest('#byfAddFit,.byf-add-fit,.byf-sizes button'))setTimeout(settle,0);
  });
  const cart=document.getElementById('gbCartDrawer')||document.getElementById('gbCartLines');
  if(cart&&window.MutationObserver)new MutationObserver(function(){fixStoredCart()}).observe(cart,{childList:true,subtree:true});
 }
 if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',install);else install();
})();
</script>
'''
    # Also remove the old Classic-only 29.99 display rule wherever it exists in the generated page.
    s=s.replace("tops[ti][0].startsWith('GB Classic')?'US$29.99':'US$39.99'", "'US$39.99'")
    s=s.replace('US$29.99','US$39.99')
    s=s.replace('</body>',js+'\n</body>')

p.write_text(s)
