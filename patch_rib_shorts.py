from pathlib import Path

p=Path('index.html')
s=p.read_text()

# v59 — Classic image-state fix only.
# Keep the established Classic Printify mappings authoritative after Add Both to Cart and after
# ANY cart quantity +/- rerender. No Build Your Fit geometry, model boards, labels, prices or layout changes.
if 'Classic authoritative image state v59' not in s:
    js=r'''
<script>/* Classic authoritative image state v59 */
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
 function normalize(n){return (n||'').replace(/\s*-\s*(Cream|Grey|Black|Blue|Green|Red|Espresso)$/,' – $1').trim()}
 function repaintFit(id){
  const nameEl=document.getElementById(id);if(!nameEl)return;
  const name=normalize(nameEl.textContent),pics=products[name];if(!pics)return;
  const item=nameEl.closest('.byf-fit-item');if(!item)return;
  const pair=item.querySelector('.byf-real-product-pair,.byf-bottom-real-product-pair');if(!pair)return;
  let imgs=pair.querySelectorAll('img');
  if(imgs.length<2){pair.innerHTML='<img loading="lazy" decoding="async"><img loading="lazy" decoding="async">';imgs=pair.querySelectorAll('img')}
  if(imgs[0].getAttribute('src')!==pics[0])imgs[0].src=pics[0];
  if(imgs[1].getAttribute('src')!==pics[1])imgs[1].src=pics[1];
  imgs[0].alt=name+' front';imgs[1].alt=name+' back';
  pair.style.display='flex';pair.classList.add('show');
 }
 function repaintFitBoth(){repaintFit('byfShopTopName');repaintFit('byfShopBottomName')}
 function repairCart(){
  document.querySelectorAll('.gb-cart-line').forEach(function(row){
   const nameEl=row.querySelector('.gb-cart-line-name');if(!nameEl)return;
   const name=normalize(nameEl.textContent),pics=products[name];if(!pics)return;
   let slot=row.querySelector('.gb-cart-thumb-slot');
   if(!slot){
    const existing=row.querySelector('img.gb-cart-thumb');
    if(existing){if(existing.getAttribute('src')!==pics[0])existing.src=pics[0];existing.alt=name;return}
    return;
   }
   let img=slot.querySelector('img.gb-cart-thumb');
   if(!img){img=document.createElement('img');img.className='gb-cart-thumb';img.loading='lazy';img.decoding='async';slot.appendChild(img)}
   if(img.getAttribute('src')!==pics[0])img.src=pics[0];img.alt=name;
  });
 }
 function settle(){requestAnimationFrame(function(){requestAnimationFrame(function(){repaintFitBoth();repairCart()})})}
 function install(){
  // Add Both is the Classic preview failure point: repaint only after all older handlers finish.
  const add=document.getElementById('byfAddFit');if(add)add.addEventListener('click',settle);
  // Cart open/reopen and every quantity +/- operation must re-bind each row by its own product name.
  const cart=document.getElementById('gbCartLink');if(cart)cart.addEventListener('click',settle);
  document.addEventListener('click',function(e){
   if(e.target.closest('.gb-cart-line button,.gb-cart-line .gb-cart-qty button,.gb-cart-line [data-action]'))settle();
  });
  const lines=document.getElementById('gbCartLines');
  if(lines&&window.MutationObserver){let queued=false;new MutationObserver(function(){if(queued)return;queued=true;requestAnimationFrame(function(){queued=false;repairCart()})}).observe(lines,{childList:true,subtree:true})}
  repaintFitBoth();repairCart();
 }
 if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',install);else install();
})();
</script>
'''
    s=s.replace('</body>',js+'\n</body>')

p.write_text(s)
