from pathlib import Path

p=Path('index.html')
s=p.read_text()

# v58 — Keep Classic Printify front/back photos visible when a size is selected.
# An older Signature Fit size-selection refresh can hide the preview pair; repaint only the
# currently selected Classic product after that click finishes. No appearance/geometry changes.
if 'Classic photos persist after size v58' not in s:
    js=r'''
<script>/* Classic photos persist after size v58 */
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
 function repaint(id){
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
 function repaintBoth(){repaint('byfShopTopName');repaint('byfShopBottomName')}
 document.addEventListener('click',function(e){
  if(e.target.closest('#byfTopSizes .byf-size,#byfBottomSizes .byf-size,#byfTopSizes button,#byfBottomSizes button')){
   requestAnimationFrame(function(){requestAnimationFrame(repaintBoth)})
  }
 });
})();
</script>
'''
    s=s.replace('</body>',js+'\n</body>')

p.write_text(s)
