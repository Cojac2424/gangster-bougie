from pathlib import Path

p=Path('index.html')
s=p.read_text()

# v53 — correct GB Classic Printify front/back image mapping by actual colour/product.
# Product-preview/cart imagery only. Build Your Fit model geometry is untouched.
if 'Classic Printify colour mapping v53' not in s:
    js=r'''
<script>/* Classic Printify colour mapping v53 */
(function(){
 const products={
  'GB Classic Sports Bra – Cream':['IMG_0589.jpeg','IMG_0590.jpeg'],
  'GB Classic Sports Bra – Grey':['IMG_0586.jpeg','IMG_0588.jpeg'],
  'GB Classic Sports Bra – Black':['IMG_0597.jpeg','IMG_0598.jpeg'],
  'GB Classic Sports Bra – Blue':['IMG_0591.jpeg','IMG_0592.jpeg'],
  'GB Classic Sports Bra – Green':['IMG_0595.jpeg','IMG_0596.jpeg'],
  'GB Classic Sports Bra – Red':['IMG_0593.jpeg','IMG_0594.jpeg'],
  'GB Classic Sports Bra – Espresso':['IMG_0611.jpeg','IMG_0612.jpeg'],
  'GB Classic High-Waisted Leggings – Cream':['IMG_0584.jpeg','IMG_0585.jpeg'],
  'GB Classic High-Waisted Leggings – Grey':['IMG_0607.jpeg','IMG_0608.jpeg'],
  'GB Classic High-Waisted Leggings – Black':['IMG_0605.jpeg','IMG_0606.jpeg'],
  'GB Classic High-Waisted Leggings – Blue':['IMG_0603.jpeg','IMG_0604.jpeg'],
  'GB Classic High-Waisted Leggings – Green':['IMG_0601.jpeg','IMG_0602.jpeg'],
  'GB Classic High-Waisted Leggings – Red':['IMG_0599.jpeg','IMG_0600.jpeg'],
  'GB Classic High-Waisted Leggings – Espresso':['IMG_0609.jpeg','IMG_0610.jpeg']
 };
 function normalize(name){return (name||'').replace(/\s*-\s*(Cream|Grey|Black|Blue|Green|Red|Espresso)$/,' – $1').trim()}
 function pairFor(el){return el&&el.closest('.byf-fit-item')?.querySelector('.byf-real-product-pair,.byf-bottom-real-product-pair')}
 function paint(id){
  const el=document.getElementById(id);if(!el)return;
  const name=normalize(el.textContent),pics=products[name];if(!pics)return;
  const pair=pairFor(el);if(!pair)return;
  pair.style.display='flex';pair.classList.add('show');
  let imgs=pair.querySelectorAll('img');
  if(imgs.length<2){pair.innerHTML='<img loading="lazy" decoding="async"><img loading="lazy" decoding="async">';imgs=pair.querySelectorAll('img')}
  if(imgs[0].getAttribute('src')!==pics[0])imgs[0].src=pics[0];
  if(imgs[1].getAttribute('src')!==pics[1])imgs[1].src=pics[1];
  imgs[0].alt=name+' front';imgs[1].alt=name+' back';
 }
 function sync(){paint('byfShopTopName');paint('byfShopBottomName')}
 function repairCart(){
  document.querySelectorAll('.gb-cart-line').forEach(function(row){
   const n=row.querySelector('.gb-cart-line-name'),slot=row.querySelector('.gb-cart-thumb-slot');if(!n||!slot)return;
   const name=normalize(n.textContent),pics=products[name];if(!pics)return;
   let img=slot.querySelector('img.gb-cart-thumb');if(!img){img=document.createElement('img');img.className='gb-cart-thumb';img.loading='lazy';img.decoding='async';slot.appendChild(img)}
   if(img.getAttribute('src')!==pics[0])img.src=pics[0];img.alt=name;
  });
 }
 function install(){
  ['byfShopTopName','byfShopBottomName'].forEach(function(id){const el=document.getElementById(id);if(el&&window.MutationObserver)new MutationObserver(function(){requestAnimationFrame(sync)}).observe(el,{childList:true,characterData:true,subtree:true})});
  const view=document.getElementById('byfViewFit');if(view)view.addEventListener('click',function(){requestAnimationFrame(sync)});
  const add=document.getElementById('byfAddFit');if(add)add.addEventListener('click',function(){requestAnimationFrame(function(){requestAnimationFrame(repairCart)})});
  const cart=document.getElementById('gbCartLink');if(cart)cart.addEventListener('click',function(){requestAnimationFrame(repairCart)});
  sync();repairCart();
 }
 if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',install);else install();
})();
</script>
'''
    s=s.replace('</body>',js+'</body>')

p.write_text(s)
