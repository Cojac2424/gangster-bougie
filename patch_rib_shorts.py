from pathlib import Path

p=Path('index.html')
s=p.read_text()

# v46 — all six workout shorts: real Printify photos, exact prices/sizes and supplied product details.
# Shopping panel/cart data only. Do not alter Build Your Fit model geometry.
if 'Workout shorts product data v46' not in s:
    js=r'''
<script>/* Workout shorts product data v46 */
(function(){
 const common=`<p><strong>Material:</strong> 100% polyester</p><p><strong>Fabric:</strong> Medium-heavy fabric (8.5 oz/yd² (290 g/m²))</p><p>Printed-in size and care label.</p><p>Seam thread colour automatically matched to design (black or white).</p><p>Assembled in the USA from globally sourced parts.</p>`;
 const products={
  'Cream Workout Shorts':{front:'IMG_0555.jpeg',back:'IMG_0556.jpeg',details:`<p>Clean, refined and built to move. The Gangster Bougie Signature Essentials Cream Workout Shorts feature a soft Cream foundation finished with understated gold Gangster Bougie detailing.</p><p>A small gold GB monogram accents the front-left hip, while the signature gold crown finishes the back for a clean luxury-athletic look. Designed to pair with the Cream Sports Bra or mix effortlessly throughout the GB Signature Collection.</p><ul><li>Soft Cream colour</li><li>Gold GB detail at the front-left hip</li><li>Signature gold crown at the back</li><li>Clean, minimal Signature design</li><li>Comfortable workout-ready silhouette</li><li>Designed for movement and everyday wear</li><li>Part of the GB Signature Collection</li><li>Made to order.</li></ul>`},
  'Oxblood Workout Shorts':{front:'IMG_0557.jpeg',back:'IMG_0558.jpeg',details:`<p>Clean, confident and built to move. The Gangster Bougie Signature Essentials Oxblood Workout Shorts feature a rich Oxblood red foundation finished with understated gold Gangster Bougie detailing.</p><p>A small gold GB monogram accents the front-left hip, while the signature gold crown finishes the back for a clean luxury-athletic look. Designed to pair with the Oxblood Sports Bra or mix effortlessly throughout the GB Signature Collection.</p><ul><li>Rich Oxblood red</li><li>Gold GB detail at the front-left hip</li><li>Signature gold crown at the back</li><li>Clean, minimal Signature design</li><li>Comfortable workout-ready silhouette</li><li>Designed for movement and everyday wear</li><li>Part of the GB Signature Collection</li><li>Made to order.</li></ul>`},
  'Onyx Workout Shorts':{front:'IMG_0543.jpeg',back:'IMG_0544.jpeg',details:`<p>Clean, confident and built to move. The Gangster Bougie Signature Essentials Onyx Workout Shorts feature a solid Onyx black foundation with understated gold Gangster Bougie detailing.</p><p>A small gold GB monogram accents the front-left hip, while a signature gold crown finishes the back for a clean luxury-athletic look. Designed to pair seamlessly with the Onyx Sports Bra or mix with pieces throughout the GB Signature Collection.</p><ul><li>Solid Onyx black</li><li>Gold GB detail at the front-left hip</li><li>Signature gold crown at the back</li><li>Clean, minimal Signature design</li><li>Comfortable workout-ready silhouette</li><li>Designed for movement and everyday wear</li><li>Part of the GB Signature Collection</li><li>Made to order.</li></ul>`},
  'Bougie Houndstooth Workout Shorts':{front:'IMG_0536.jpeg',back:'IMG_0537.jpeg',details:`<p>Make every move a statement in the Gangster Bougie Signature Bougie Houndstooth Workout Shorts. Featuring our elevated black, cream and gold houndstooth design with signature GB detailing, these shorts bring luxury attitude to an athletic silhouette.</p><p>Designed for training, everyday wear and statement styling, they pair with the matching Bougie Houndstooth Sports Bra or other pieces from the GB Signature Collection.</p><ul><li>Black, cream &amp; gold Bougie Houndstooth design</li><li>Signature GB detailing</li><li>Comfortable athletic fit</li><li>All-over printed design</li><li>Designed for movement and everyday wear</li><li>Coordinates with the Bougie Houndstooth Sports Bra and High-Waisted Leggings</li><li>Part of the GB Signature Collection</li><li>Made to order.</li></ul>`},
  'Vault Workout Shorts':{front:'IMG_0529.jpeg',back:'IMG_0530.jpeg',details:`<p>Make every move a statement in the Gangster Bougie Signature Vault Workout Shorts. Featuring our espresso, brown and gold Art Deco-inspired Vault design with signature GB detailing, these shorts bring elevated luxury styling to an athletic silhouette.</p><p>Designed for movement, training and everyday wear, they can be worn alone or paired with the Signature Vault Sports Bra for a coordinated look.</p><ul><li>Signature espresso, brown &amp; gold Vault design</li><li>Art Deco-inspired detailing</li><li>Signature GB monogram</li><li>Comfortable athletic fit</li><li>All-over printed design</li><li>Designed to coordinate with the Vault Sports Bra and High-Waisted Leggings</li><li>Part of the GB Signature Collection</li><li>Made to order.</li></ul>`},
  'Heritage Plaid Workout Shorts':{front:'IMG_0515.jpeg',back:'IMG_0516.jpeg',details:`<p>Make every move a statement in the Gangster Bougie Signature Heritage Plaid Workout Shorts. Featuring our signature burgundy, black and gold Heritage Plaid with iconic GB and crown detailing, these fitted shorts bring luxury streetwear attitude to an active silhouette.</p><p>Made from durable 100% polyester with a medium-heavy feel, they’re designed to retain their shape while providing comfort for training, everyday movement or styling as part of the complete Heritage Plaid look.</p><ul><li>Signature burgundy, black &amp; gold Heritage Plaid</li><li>Iconic GB &amp; crown detailing</li><li>100% polyester</li><li>Medium-heavy fabric</li><li>Gusset insert for active movement</li><li>Vibrant all-over print</li><li>Designed to coordinate with the Heritage Plaid Sports Bra and Leggings</li><li>Part of the GB Signature Collection</li><li>Made to order.</li></ul>`}
 };
 function sync(){
  const nameEl=document.getElementById('byfShopBottomName'), pair=document.getElementById('byfBottomRealProductPair'), details=document.querySelector('#byfBottomDetails .byf-details-body'), price=document.getElementById('byfShopBottomPrice');
  if(!nameEl||!pair)return;
  const name=(nameEl.textContent||'').trim(), p=products[name];
  if(!p)return;
  pair.style.display='flex';
  pair.innerHTML='<img src="'+p.front+'" alt="'+name+' front" loading="lazy" decoding="async"><img src="'+p.back+'" alt="'+name+' back" loading="lazy" decoding="async">';
  if(details)details.innerHTML=p.details+common;
  if(price)price.textContent='US$54.99';
 }
 const nameEl=document.getElementById('byfShopBottomName');
 if(nameEl&&window.MutationObserver)new MutationObserver(sync).observe(nameEl,{childList:true,characterData:true,subtree:true});
 const root=document.getElementById('build-your-fit');
 if(root){root.addEventListener('click',()=>setTimeout(sync,0));root.addEventListener('pointerup',()=>setTimeout(sync,0));}
 sync();

 // Cart thumbnails: one real product image per shorts line item.
 const thumbMap={
  'Cream Workout Shorts':'IMG_0555.jpeg','Oxblood Workout Shorts':'IMG_0557.jpeg','Onyx Workout Shorts':'IMG_0543.jpeg',
  'Bougie Houndstooth Workout Shorts':'IMG_0536.jpeg','Vault Workout Shorts':'IMG_0529.jpeg','Heritage Plaid Workout Shorts':'IMG_0515.jpeg'
 };
 function repairCartThumbs(){
  document.querySelectorAll('.gb-cart-line').forEach(row=>{
   const nm=(row.querySelector('.gb-cart-line-name')?.textContent||'').trim(), slot=row.querySelector('.gb-cart-thumb-slot'), src=thumbMap[nm];
   if(!slot||!src)return;
   slot.innerHTML=''; const im=document.createElement('img'); im.className='gb-cart-thumb'; im.src=src; im.alt=nm; im.loading='lazy'; im.decoding='async'; slot.appendChild(im);
  });
 }
 document.addEventListener('click',()=>setTimeout(repairCartThumbs,0),true);
 new MutationObserver(repairCartThumbs).observe(document.body,{childList:true,subtree:true});
})();
</script>
'''
    s=s.replace('</body>',js+'</body>')

p.write_text(s)
