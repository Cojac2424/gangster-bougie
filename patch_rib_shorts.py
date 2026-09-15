from pathlib import Path

p=Path('index.html')
s=p.read_text()
if 'id="build-your-fit"' not in s: raise SystemExit('Build Your Fit not present')

# v43 — add Bougie Houndstooth to the approved sports-bra shopping data.
# No compositor geometry, model sizing, split points, or arrow positions are changed.
if 'Bougie Houndstooth product data v43' not in s:
    js=r'''
<script>/* Bougie Houndstooth product data v43 */
(function(){
 const product={
  name:'Bougie Houndstooth Sports Bra',
  front:'IMG_0532.jpeg',back:'IMG_0533.jpeg',price:39.99,
  details:`<p>Black, cream &amp; gold Bougie Houndstooth design with signature GB detailing.</p><ul><li>Black, cream &amp; gold Bougie Houndstooth design</li><li>Signature GB detailing</li><li>All-over printed design</li><li>Comfortable, athletic silhouette</li><li>Designed for training and everyday wear</li><li>Coordinates with Signature Houndstooth bottoms</li><li>Part of the GB Signature Collection</li><li>Made to order.</li></ul><p><strong>Material:</strong> 100% polyester<br><strong>U-shaped back</strong><br><strong>Please note:</strong> Size tolerance up to 1.2&quot; (3 cm)</p>`
 };
 function sync(){
  const nameEl=document.getElementById('byfShopTopName'),pair=document.getElementById('byfTopRealProductPair');
  if(!nameEl||!pair||(nameEl.textContent||'').trim()!==product.name)return;
  let imgs=pair.querySelectorAll('img');
  if(imgs.length<2){pair.innerHTML='<img alt="" loading="lazy" decoding="async"><img alt="" loading="lazy" decoding="async">';imgs=pair.querySelectorAll('img')}
  if(imgs[0].getAttribute('src')!==product.front)imgs[0].src=product.front;
  if(imgs[1].getAttribute('src')!==product.back)imgs[1].src=product.back;
  imgs[0].alt=product.name+' front';imgs[1].alt=product.name+' back';pair.style.display='flex';
  const topItem=nameEl.closest('.byf-fit-item');
  if(topItem){const det=topItem.querySelector('details');if(det){const body=det.querySelector('.byf-details-body')||det.querySelector('div');if(body)body.innerHTML=product.details}}
 }
 const nameEl=document.getElementById('byfShopTopName');
 if(nameEl&&window.MutationObserver)new MutationObserver(sync).observe(nameEl,{childList:true,characterData:true,subtree:true});
 const root=document.getElementById('build-your-fit');if(root){root.addEventListener('click',()=>setTimeout(sync,0));root.addEventListener('pointerup',()=>setTimeout(sync,0))}
 sync();
 function cart(){document.querySelectorAll('.gb-cart-line').forEach(row=>{const n=(row.querySelector('.gb-cart-line-name')?.textContent||'').trim(),slot=row.querySelector('.gb-cart-thumb-slot');if(n!==product.name||!slot)return;let im=slot.querySelector('img');if(!im){im=document.createElement('img');im.className='gb-cart-thumb';im.loading='lazy';im.decoding='async';slot.appendChild(im)}if(im.getAttribute('src')!==product.front)im.src=product.front;im.alt=product.name})}
 const lines=document.getElementById('gbCartLines');if(lines&&window.MutationObserver)new MutationObserver(cart).observe(lines,{childList:true,subtree:true});cart();
})();
</script>
'''
    s=s.replace('</body>',js+'</body>')

p.write_text(s)
