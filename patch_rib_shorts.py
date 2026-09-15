from pathlib import Path

p=Path('index.html')
s=p.read_text()

# v49 — make the established Product Details dropdown template visible for every Signature Fit product.
# The existing product-data scripts continue supplying each selected item's own details.
# No Build Your Fit geometry, joins, sizing, arrows, images, prices or layout measurements changed.
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
 function sync(){
  ensure('byfShopTopName','byfTopDetails');
  ensure('byfShopBottomName','byfBottomDetails');
  // Nudge the existing per-product data handlers after the dropdown is guaranteed to exist.
  const root=document.getElementById('build-your-fit');
  if(root)root.dispatchEvent(new Event('pointerup',{bubbles:false}));
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

p.write_text(s)
