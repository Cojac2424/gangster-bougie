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
# IMPORTANT: array-only extension. Existing compositor geometry, split points, background positions,
# model dimensions, arrows, front/back viewer, swipe and cart architecture are untouched.
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

    # Classic sports bras are US$29.99; Signature bras remain US$39.99.
    old="if(st)st.textContent=tops[ti][0];if(sb)sb.textContent=bottomName;if(sp)sp.textContent=bottomName.includes('Workout Shorts')?'US$54.99':'US$69.99';"
    new="if(st)st.textContent=tops[ti][0];if(sb)sb.textContent=bottomName;if(sp)sp.textContent=bottomName.includes('Workout Shorts')?'US$54.99':'US$69.99';const tp=document.querySelector('#byfShopTopName + .byf-fit-price');if(tp)tp.textContent=tops[ti][0].startsWith('GB Classic')?'US$29.99':'US$39.99';"
    if old in s: s=s.replace(old,new,1)

p.write_text(s)
