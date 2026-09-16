from pathlib import Path

p=Path('index.html')
s=p.read_text()

# v61 — Classic preview persistence + mobile thumbnail sizing only.
# Keep the existing real Printify front/back images visible when Product Details opens/closes,
# and keep Classic sports-bra thumbnails to the same compact footprint as leggings on mobile.
# No Build Your Fit model geometry, boards, joins, arrows, product mapping, cart, prices or sizes changed.
if 'Classic preview persistence v61' not in s:
    css=r'''
<style>/* Classic preview persistence v61 */
@media(max-width:760px){
 #build-your-fit .byf-fit-item:has(#byfShopTopName) .byf-real-product-pair,
 #build-your-fit .byf-fit-item:has(#byfShopTopName) .byf-bottom-real-product-pair{
   width:276px!important;max-width:44%!important;gap:8px!important;
 }
 #build-your-fit .byf-fit-item:has(#byfShopTopName) .byf-real-product-pair img,
 #build-your-fit .byf-fit-item:has(#byfShopTopName) .byf-bottom-real-product-pair img{
   width:128px!important;max-width:calc(50% - 4px)!important;height:auto!important;object-fit:contain!important;
 }
}
</style>
'''
    js=r'''
<script>/* Classic preview persistence v61 */
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
 function repaint(nameId){
  const nameEl=document.getElementById(nameId);if(!nameEl)return;
  const name=normalize(nameEl.textContent),pics=products[name];if(!pics)return;
  const item=nameEl.closest('.byf-fit-item');if(!item)return;
  const pair=item.querySelector('.byf-real-product-pair,.byf-bottom-real-product-pair');if(!pair)return;
  let imgs=pair.querySelectorAll('img');
  if(imgs.length<2){pair.innerHTML='<img loading="lazy" decoding="async"><img loading="lazy" decoding="async">';imgs=pair.querySelectorAll('img')}
  if(imgs[0].getAttribute('src')!==pics[0])imgs[0].src=pics[0];
  if(imgs[1].getAttribute('src')!==pics[1])imgs[1].src=pics[1];
  imgs[0].alt=name+' front';imgs[1].alt=name+' back';
  pair.style.setProperty('display','flex','important');pair.classList.add('show');
 }
 function repaintBoth(){repaint('byfShopTopName');repaint('byfShopBottomName')}
 function settle(){requestAnimationFrame(function(){requestAnimationFrame(repaintBoth)})}
 function install(){
  // Opening/closing either Product Details row must never hide the Classic product previews.
  ['byfTopDetails','byfBottomDetails'].forEach(function(id){const d=document.getElementById(id);if(d)d.addEventListener('toggle',settle)});
  // Preserve the already-correct behavior after size selection and View This Fit.
  const panel=document.getElementById('byfFitPanel');if(panel)panel.addEventListener('click',function(e){if(e.target.closest('.byf-sizes button'))settle()});
  const view=document.getElementById('byfViewFit');if(view)view.addEventListener('click',settle);
  repaintBoth();
 }
 if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',install);else install();
})();
</script>
'''
    s=s.replace('</head>',css+'\n</head>')
    s=s.replace('</body>',js+'\n</body>')

p.write_text(s)
