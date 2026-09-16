from pathlib import Path

p=Path('index.html')
s=p.read_text()

# v49 — make the established Product Details dropdown template visible for every Signature Fit product.
if 'Signature Fit Product Details template v49' not in s:
    js=r'''
<script>/* Signature Fit Product Details template v49 */
(function(){
 function ensure(itemId,detailsId){
  const name=document.getElementById(itemId);if(!name)return null;
  const item=name.closest('.byf-fit-item');if(!item)return null;
  let details=document.getElementById(detailsId)||item.querySelector('details.byf-product-details');
  if(!details){
   details=document.createElement('details');details.className='byf-product-details';details.id=detailsId;
   const summary=document.createElement('summary');summary.textContent='Product Details';
   const body=document.createElement('div');body.className='byf-details-body';
   details.appendChild(summary);details.appendChild(body);
   const pair=item.querySelector('.byf-real-product-pair,.byf-bottom-real-product-pair');
   item.insertBefore(details,pair||null);
  }
  details.style.display='block';
  return details;
 }
 function install(){
  ensure('byfShopTopName','byfTopDetails');ensure('byfShopBottomName','byfBottomDetails');
  ['byfShopTopName','byfShopBottomName'].forEach(function(id){const el=document.getElementById(id);if(el&&window.MutationObserver)new MutationObserver(function(){ensure(id,id==='byfShopTopName'?'byfTopDetails':'byfBottomDetails')}).observe(el,{childList:true,characterData:true,subtree:true})});
 }
 if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',install);else install();
})();
</script>
'''
    s=s.replace('</body>',js+'</body>')

# v50 — Classic collection four-view boards in Build Your Fit.
if 'GB Classic Sports Bra – Cream' not in s:
    top_anchor="  ['Bougie Houndstooth Sports Bra','648F1080-1C4C-4FFD-BA17-C79CBE5D7309.jpeg']\n ];"
    top_repl="""  ['Bougie Houndstooth Sports Bra','648F1080-1C4C-4FFD-BA17-C79CBE5D7309.jpeg'],
  ['GB Classic Sports Bra – Cream','BB251A6A-A1C5-4955-AD45-12977154FDD1.jpeg'],
  ['GB Classic Sports Bra – Grey','48A8992E-44EE-4EA0-9216-6151AA482183.jpeg'],
  ['GB Classic Sports Bra – Black','6A0433B5-2CB5-487C-BF0C-BA13AEBF3614.jpeg'],
  ['GB Classic Sports Bra – Blue','1319CBE4-7111-42FE-AFB6-72211748DA6B.jpeg'],
  ['GB Classic Sports Bra – Green','7475A5C3-1000-4C72-9498-153934E2DE66.jpeg'],
  ['GB Classic Sports Bra – Red','71EA0B6E-ADAC-48A9-972B-6F8B9B4CF6AA.jpeg'],
  ['GB Classic Sports Bra – Espresso','5EA988CF-42B7-475B-BD47-B4E8F6D26456.jpeg']
 ];"""
    if top_anchor not in s: raise SystemExit('v50 top array anchor not found')
    s=s.replace(top_anchor,top_repl,1)
    bottom_anchor="  ['Bougie Houndstooth Leggings','648F1080-1C4C-4FFD-BA17-C79CBE5D7309.jpeg'],['Bougie Houndstooth Workout Shorts','D2DC5FB5-3654-4B80-978B-238C3C4974F0.jpeg']\n ];"
    bottom_repl="""  ['Bougie Houndstooth Leggings','648F1080-1C4C-4FFD-BA17-C79CBE5D7309.jpeg'],['Bougie Houndstooth Workout Shorts','D2DC5FB5-3654-4B80-978B-238C3C4974F0.jpeg'],
  ['GB Classic High-Waisted Leggings – Cream','BB251A6A-A1C5-4955-AD45-12977154FDD1.jpeg'],
  ['GB Classic High-Waisted Leggings – Grey','48A8992E-44EE-4EA0-9216-6151AA482183.jpeg'],
  ['GB Classic High-Waisted Leggings – Black','6A0433B5-2CB5-487C-BF0C-BA13AEBF3614.jpeg'],
  ['GB Classic High-Waisted Leggings – Blue','1319CBE4-7111-42FE-AFB6-72211748DA6B.jpeg'],
  ['GB Classic High-Waisted Leggings – Green','7475A5C3-1000-4C72-9498-153934E2DE66.jpeg'],
  ['GB Classic High-Waisted Leggings – Red','71EA0B6E-ADAC-48A9-972B-6F8B9B4CF6AA.jpeg'],
  ['GB Classic High-Waisted Leggings – Espresso','5EA988CF-42B7-475B-BD47-B4E8F6D26456.jpeg']
 ];"""
    if bottom_anchor not in s: raise SystemExit('v50 bottom array anchor not found')
    s=s.replace(bottom_anchor,bottom_repl,1)
    old="if(st)st.textContent=tops[ti][0];if(sb)sb.textContent=bottomName;if(sp)sp.textContent=bottomName.includes('Workout Shorts')?'US$54.99':'US$69.99';"
    new="if(st)st.textContent=tops[ti][0];if(sb)sb.textContent=bottomName;if(sp)sp.textContent=bottomName.includes('Workout Shorts')?'US$54.99':'US$69.99';const tp=document.querySelector('#byfShopTopName + .byf-fit-price');if(tp)tp.textContent=tops[ti][0].startsWith('GB Classic')?'US$29.99':'US$39.99';"
    if old in s: s=s.replace(old,new,1)

# v51 — old Classic board preview retained for migration; v52 below overrides it with real Printify product photos.
if 'Classic real product previews v51' not in s:
    js=r'''
<script>/* Classic real product previews v51 */
(function(){
 const boards={
  'Cream':'BB251A6A-A1C5-4955-AD45-12977154FDD1.jpeg','Grey':'48A8992E-44EE-4EA0-9216-6151AA482183.jpeg',
  'Black':'6A0433B5-2CB5-487C-BF0C-BA13AEBF3614.jpeg','Blue':'1319CBE4-7111-42FE-AFB6-72211748DA6B.jpeg',
  'Green':'7475A5C3-1000-4C72-9498-153934E2DE66.jpeg','Red':'71EA0B6E-ADAC-48A9-972B-6F8B9B4CF6AA.jpeg',
  'Espresso':'5EA988CF-42B7-475B-BD47-B4E8F6D26456.jpeg'
 };
 function colour(name){for(const c in boards)if(name.endsWith('– '+c)||name.endsWith('- '+c))return c;return null}
 function pairFor(nameId){const n=document.getElementById(nameId);return n&&n.closest('.byf-fit-item')?.querySelector('.byf-real-product-pair,.byf-bottom-real-product-pair')}
 function paint(nameId){const n=document.getElementById(nameId);if(!n)return;const name=(n.textContent||'').trim(),c=colour(name);if(!c)return;const pair=pairFor(nameId);if(!pair)return;pair.style.display='flex';pair.classList.add('show');let a=pair.querySelectorAll('img');if(a.length<2){pair.innerHTML='<img loading="lazy" decoding="async"><img loading="lazy" decoding="async">';a=pair.querySelectorAll('img')}a[0].src=boards[c];a[1].src=boards[c]}
 function sync(){paint('byfShopTopName');paint('byfShopBottomName')}
 function install(){['byfShopTopName','byfShopBottomName'].forEach(function(id){const el=document.getElementById(id);if(el&&window.MutationObserver)new MutationObserver(function(){requestAnimationFrame(sync)}).observe(el,{childList:true,characterData:true,subtree:true})});sync()}
 if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',install);else install();
})();
</script>
'''
    s=s.replace('</body>',js+'</body>')

# v52 — real Printify front/back photos for every GB Classic bra and legging.
# This changes only the product-preview/cart imagery; Build Your Fit model geometry is untouched.
if 'Classic Printify front back photos v52' not in s:
    js=r'''
<script>/* Classic Printify front back photos v52 */
(function(){
 const products={
  'GB Classic Sports Bra – Cream':['IMG_0586.jpeg','IMG_0588.jpeg'],
  'GB Classic Sports Bra – Grey':['IMG_0609.jpeg','IMG_0610.jpeg'],
  'GB Classic Sports Bra – Black':['IMG_0591.jpeg','IMG_0592.jpeg'],
  'GB Classic Sports Bra – Blue':['IMG_0607.jpeg','IMG_0608.jpeg'],
  'GB Classic Sports Bra – Green':['IMG_0584.jpeg','IMG_0585.jpeg'],
  'GB Classic Sports Bra – Red':['IMG_0589.jpeg','IMG_0590.jpeg'],
  'GB Classic Sports Bra – Espresso':['IMG_0605.jpeg','IMG_0606.jpeg'],
  'GB Classic High-Waisted Leggings – Cream':['IMG_0611.jpeg','IMG_0612.jpeg'],
  'GB Classic High-Waisted Leggings – Grey':['IMG_0601.jpeg','IMG_0602.jpeg'],
  'GB Classic High-Waisted Leggings – Black':['IMG_0595.jpeg','IMG_0596.jpeg'],
  'GB Classic High-Waisted Leggings – Blue':['IMG_0599.jpeg','IMG_0600.jpeg'],
  'GB Classic High-Waisted Leggings – Green':['IMG_0593.jpeg','IMG_0594.jpeg'],
  'GB Classic High-Waisted Leggings – Red':['IMG_0603.jpeg','IMG_0604.jpeg'],
  'GB Classic High-Waisted Leggings – Espresso':['IMG_0597.jpeg','IMG_0598.jpeg']
 };
 function normalize(name){return (name||'').replace(/\s*-\s*(Cream|Grey|Black|Blue|Green|Red|Espresso)$/,' – $1').trim()}
 function pairFor(nameEl){return nameEl&&nameEl.closest('.byf-fit-item')?.querySelector('.byf-real-product-pair,.byf-bottom-real-product-pair')}
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
  imgs[0].style.objectPosition='center';imgs[1].style.objectPosition='center';
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
  const lines=document.getElementById('gbCartLines');if(lines&&window.MutationObserver){let queued=false;new MutationObserver(function(){if(queued)return;queued=true;requestAnimationFrame(function(){queued=false;repairCart()})}).observe(lines,{childList:true})}
  const cart=document.getElementById('gbCartLink');if(cart)cart.addEventListener('click',function(){requestAnimationFrame(repairCart)});
  sync();repairCart();
 }
 if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',install);else install();
})();
</script>
'''
    s=s.replace('</body>',js+'</body>')

p.write_text(s)
