from pathlib import Path

p=Path('index.html')
s=p.read_text()
if 'id="build-your-fit"' not in s: raise SystemExit('Build Your Fit not present')

# v42 — wire the complete sports-bra category into the already-approved shopping UI.
# Product images are assigned ONLY when that bra is selected, so they do not preload on page load.
# No Build Your Fit compositor geometry, split points, model sizing, or arrow positions are changed.
if 'Sports bra product data v42' not in s:
    js=r'''
<script>/* Sports bra product data v42 */
(function(){
 const bras={
  'Heritage Plaid Sports Bra':{
   front:'IMG_0522.jpeg',back:'IMG_0523.jpeg',price:39.99,
   details:`<p>Make a statement without saying a word. The Gangster Bougie Heritage Plaid Sports Bra combines deep burgundy, black and gold with our signature GB monogram and crown detailing for a luxury streetwear take on activewear.</p><p>Designed with a supportive U-shaped back and removable chest padding, it delivers comfort and attitude whether you’re training, styling it casually, or building a complete Signature fit.</p><ul><li>Exclusive Gangster Bougie Heritage Plaid design</li><li>Signature GB monogram and crown detailing</li><li>Soft, lightweight and breathable polyester</li><li>U-shaped back for added support</li><li>Removable chest padding</li><li>Available in sizes S–2XL</li><li>Part of the GB Signature Collection</li><li>Made to order.</li></ul><p><strong>Material:</strong> 100% polyester<br><strong>U-shaped back</strong><br><strong>Please note:</strong> Size tolerance up to 1.2&quot; (3 cm)</p>`},
  'Vault Sports Bra':{
   front:'IMG_0527.jpeg',back:'IMG_0528.jpeg',price:39.99,
   details:`<p>Make luxury part of the uniform. The Gangster Bougie Signature Vault Sports Bra features our espresso, brown and gold Art Deco-inspired Vault design, finished with signature GB detailing for a rich, elevated look.</p><p>Designed for movement while making a statement, this fitted sports bra combines comfort and attitude with an all-over pattern created to coordinate across the GB Signature collection.</p><ul><li>Signature espresso, brown &amp; gold Vault design</li><li>Art Deco-inspired detailing</li><li>Signature GB monogram</li><li>Comfortable, supportive fit</li><li>All-over printed design</li><li>Designed to coordinate with Vault Leggings and Workout Shorts</li><li>Part of the GB Signature Collection</li><li>Made to order.</li></ul><p><strong>Material:</strong> 100% polyester<br><strong>U-shaped back</strong><br><strong>Please note:</strong> Size tolerance up to 1.2&quot; (3 cm)</p>`},
  'Onyx Sports Bra':{
   front:'IMG_0545.jpeg',back:'IMG_0546.jpeg',price:39.99,
   details:`<p>Clean. Elevated, unmistakably Gangster Bougie. The Gangster Bougie Signature Essentials Onyx Sports Bra pairs a solid Onyx black foundation with understated gold GB detailing for a versatile luxury-athletic look.</p><p>A gold GB monogram finishes the front, while the signature crown and “What Hustle Looks Like” detail marks the back. Designed to stand on its own or mix effortlessly with Heritage Plaid, Vault, Bougie Houndstooth and matching Signature Essentials bottoms.</p><ul><li>Solid Onyx black</li><li>Gold GB front detail</li><li>Gold crown + “What Hustle Looks Like” back detail</li><li>Clean, minimal Signature design</li><li>Designed for training and everyday wear</li><li>Made to coordinate across the GB Signature Collection</li><li>Made to order.</li></ul><p><strong>Material:</strong> 100% polyester<br><strong>U-shaped back</strong><br><strong>Please note:</strong> Size tolerance up to 1.2&quot; (3 cm)</p>`},
  'Oxblood Sports Bra':{
   front:'IMG_0547.jpeg',back:'IMG_0548.jpeg',price:39.99,
   details:`<p>Bold, elevated and unmistakably Gangster Bougie. The Gangster Bougie Signature Essentials Oxblood Sports Bra combines a rich Oxblood red foundation with understated gold GB detailing for a luxury-athletic look.</p><p>A gold GB monogram finishes the front, while the signature gold crown and “What Hustle Looks Like” detail marks the back. Designed to stand on its own or mix effortlessly with pieces throughout the GB Signature Collection.</p><ul><li>Rich Oxblood red</li><li>Gold GB front detail</li><li>Gold crown + “What Hustle Looks Like” back detail</li><li>Clean, minimal Signature design</li><li>Designed for training and everyday wear</li><li>Made to coordinate across GB Signature Collection</li><li>Made to order.</li></ul><p><strong>Material:</strong> 100% polyester<br><strong>U-shaped back</strong><br><strong>Please note:</strong> Size tolerance up to 1.2&quot; (3 cm)</p>`},
  'Cream Sports Bra':{
   front:'IMG_0551.jpeg',back:'IMG_0552.jpeg',price:39.99,
   details:`<p>Clean, refined and effortlessly Gangster Bougie. The Gangster Bougie Signature Essentials Cream Sports Bra pairs a soft Cream foundation with understated gold GB detailing for an elevated luxury-athletic look.</p><p>A gold GB monogram finishes the front, while the signature gold crown and “What Hustle Looks Like” detail marks the back. Designed to stand on its own or coordinate effortlessly with pieces throughout the GB Signature Collection.</p><ul><li>Soft Cream colour</li><li>Gold GB front detail</li><li>Gold crown + “What Hustle Looks Like” back detail</li><li>Clean, minimal Signature design</li><li>Designed for training and everyday wear</li><li>Made to coordinate across the GB Signature Collection</li><li>Made to order.</li></ul><p><strong>Material:</strong> 100% polyester<br><strong>U-shaped back</strong><br><strong>Please note:</strong> Size tolerance up to 1.2&quot; (3 cm)</p>`}
 };
 function syncBra(){
  const nameEl=document.getElementById('byfShopTopName'),pair=document.getElementById('byfTopRealProductPair');
  if(!nameEl||!pair)return;
  const name=(nameEl.textContent||'').trim(),d=bras[name];
  if(!d){pair.style.display='none';return}
  let imgs=pair.querySelectorAll('img');
  if(imgs.length<2){pair.innerHTML='<img alt="" loading="lazy" decoding="async"><img alt="" loading="lazy" decoding="async">';imgs=pair.querySelectorAll('img')}
  // src is changed only for the selected bra: no category-wide image preload.
  if(imgs[0].getAttribute('src')!==d.front)imgs[0].src=d.front;
  if(imgs[1].getAttribute('src')!==d.back)imgs[1].src=d.back;
  imgs[0].alt=name+' front';imgs[1].alt=name+' back';pair.style.display='flex';
  const topItem=nameEl.closest('.byf-fit-item');
  if(topItem){const det=topItem.querySelector('details');if(det){const body=det.querySelector('.byf-details-body')||det.querySelector('div');if(body)body.innerHTML=d.details}}
 }
 const nameEl=document.getElementById('byfShopTopName');
 if(nameEl&&window.MutationObserver)new MutationObserver(syncBra).observe(nameEl,{childList:true,characterData:true,subtree:true});
 const root=document.getElementById('build-your-fit');if(root){root.addEventListener('click',()=>setTimeout(syncBra,0));root.addEventListener('pointerup',()=>setTimeout(syncBra,0))}
 syncBra();
 // Keep cart thumbnails synchronized with the exact selected bra. One front image only.
 function syncCartThumbs(){document.querySelectorAll('.gb-cart-line').forEach(row=>{const n=(row.querySelector('.gb-cart-line-name')?.textContent||'').trim(),d=bras[n],slot=row.querySelector('.gb-cart-thumb-slot');if(!slot||!d)return;let im=slot.querySelector('img');if(!im){im=document.createElement('img');im.className='gb-cart-thumb';im.loading='lazy';im.decoding='async';slot.appendChild(im)}if(im.getAttribute('src')!==d.front)im.src=d.front;im.alt=n})}
 const cartLines=document.getElementById('gbCartLines');if(cartLines&&window.MutationObserver)new MutationObserver(syncCartThumbs).observe(cartLines,{childList:true,subtree:true});syncCartThumbs();
})();
</script>
'''
    s=s.replace('</body>',js+'</body>')

p.write_text(s)
