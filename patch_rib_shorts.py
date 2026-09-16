from pathlib import Path

p=Path('index.html')
s=p.read_text()

# v60 — Classic Product Details mapping only.
# Replaces the old Signature/Onyx fallback whenever a Classic item is selected.
# No model geometry, product images, cart behavior, sizes, prices, arrows or layout changes.
if 'Classic Product Details mapping v60' not in s:
    js=r'''
<script>/* Classic Product Details mapping v60 */
(function(){
 const colours=['Cream','Grey','Black','Blue','Green','Red','Espresso'];
 const tone={
  Cream:'a refined cream', Grey:'a sleek grey', Black:'a sleek black', Blue:'a rich blue',
  Green:'a rich green', Red:'a bold red', Espresso:'a rich espresso-brown'
 };
 function normalize(n){return (n||'').replace(/\s*-\s*(Cream|Grey|Black|Blue|Green|Red|Espresso)$/,' – $1').trim()}
 function colour(name){for(const c of colours)if(name.endsWith('– '+c))return c;return null}
 function bra(c){return `
  <p>Luxury meets performance. The GB Classic Sports Bra combines ${tone[c]} athletic silhouette with signature gold lattice detailing and the crowned GB emblem for an elevated Gangster Bougie look.</p>
  <ul>
   <li>100% polyester</li>
   <li>U-shaped back</li>
   <li>Size tolerance up to 1.2 in (3 cm)</li>
   <li>Signature gold lattice detailing</li>
   <li>Crowned GB emblem</li>
   <li>Made to order</li>
  </ul>`}
 function leggings(c){return `
  <p>Luxury meets performance. The GB Classic High-Waisted Leggings combine ${tone[c]} silhouette with signature gold lattice detailing running down the outer legs and the crowned GB emblem for an elevated Gangster Bougie look.</p>
  <ul>
   <li>83% polyester, 17% spandex</li>
   <li>Skinny fit</li>
   <li>Double-layer waistband</li>
   <li>Runs small — consider sizing up</li>
   <li>Outside seam thread is colour-matched to the design</li>
   <li>Interior seam thread is white</li>
   <li>Slightly see-through when stretched; undyed white may show at seams and sewn areas</li>
   <li>Assembled in the USA from globally sourced parts</li>
   <li>Made to order</li>
  </ul>`}
 function paint(nameId,detailsId){
  const n=document.getElementById(nameId),d=document.getElementById(detailsId);if(!n||!d)return;
  const name=normalize(n.textContent),c=colour(name);if(!c||!name.startsWith('GB Classic'))return;
  const body=d.querySelector('.byf-details-body');if(!body)return;
  body.innerHTML=name.includes('Sports Bra')?bra(c):leggings(c);
 }
 function sync(){paint('byfShopTopName','byfTopDetails');paint('byfShopBottomName','byfBottomDetails')}
 function install(){
  ['byfShopTopName','byfShopBottomName'].forEach(function(id){const el=document.getElementById(id);if(el&&window.MutationObserver)new MutationObserver(function(){requestAnimationFrame(sync)}).observe(el,{childList:true,characterData:true,subtree:true})});
  const view=document.getElementById('byfViewFit');if(view)view.addEventListener('click',function(){requestAnimationFrame(sync)});
  sync();
 }
 if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',install);else install();
})();
</script>
'''
    s=s.replace('</body>',js+'\n</body>')

p.write_text(s)
