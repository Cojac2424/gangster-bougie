from pathlib import Path
p=Path('index.html')
s=p.read_text()
if 'id="openGBTravelBag"' in s:
    raise SystemExit('Split travel bags already present')

# Existing travel bag becomes the Baddie bag using only its first two images.
s=s.replace('Gangster Bougie Faux Leather Travel Bag</div>\n    <div class="product-status">Black • 9.5&quot; × 20.8&quot; • US$109.99</div>\n    <button class="view-item" id="openTravelBag"', 'Gangster Bougie “Baddie” Faux Leather Travel Bag</div>\n    <div class="product-status">Black • 9.5&quot; × 20.8&quot; • US$109.99</div>\n    <button class="view-item" id="openTravelBag"',1)
s=s.replace('<h2>Gangster Bougie Faux Leather Travel Bag</h2>','<h2>Gangster Bougie “Baddie” Faux Leather Travel Bag</h2>',1)
s=s.replace("const files=['IMG_0414.jpeg','IMG_0415.jpeg','IMG_0416.jpeg','IMG_0417.jpeg'];\n const labels=['Front','Back','Front','Side'];","const files=['IMG_0414.jpeg','IMG_0415.jpeg'];\n const labels=['Front','Back'];",1)
# Remove GB thumbnails from existing Baddie gallery.
s=s.replace('''\n        <button class="sports-thumb travel-bag-thumb" type="button" data-index="2"><img src="IMG_0416.jpeg" alt="Gangster Bougie Faux Leather Travel Bag"><span class="sports-thumb-label">Front</span></button>\n        <button class="sports-thumb travel-bag-thumb" type="button" data-index="3"><img src="IMG_0417.jpeg" alt="Gangster Bougie Faux Leather Travel Bag"><span class="sports-thumb-label">Side</span></button>''','',1)

# Add a second card directly after the existing travel bag card.
pos=s.index('id="openTravelBag"')
article_end=s.index('</article>',pos)+len('</article>')
gb_card='''
<article class="product-card" data-category="accessories">
  <div class="product-image"><img src="IMG_0416.jpeg" alt="Gangster Bougie GB Faux Leather Travel Bag"></div>
  <div class="product-accent"></div>
  <div class="product-info">
    <div class="product-tag">ACCESSORIES • TRAVEL</div>
    <div class="product-name">Gangster Bougie GB Faux Leather Travel Bag</div>
    <div class="product-status">Black &amp; White • 9.5&quot; × 20.8&quot; • US$109.99</div>
    <button class="view-item" id="openGBTravelBag" type="button">View Item</button>
  </div>
</article>'''
s=s[:article_end]+gb_card+s[article_end:]

# Add its own established product viewer before the existing travel bag modal.
mp=s.index('<div class="modal" id="travelBagModal"')
gb_modal='''
<div class="modal" id="gbTravelBagModal" aria-hidden="true">
  <div class="modal-box sports-modal-box">
    <button class="modal-close" id="closeGBTravelBag" type="button">Close</button>
    <div class="sports-layout">
      <div class="sports-main-wrap">
        <div class="main-product-photo sports-stage"><img id="gbTravelBagMain" src="IMG_0416.jpeg" alt="Gangster Bougie GB Faux Leather Travel Bag"></div>
        <button class="sports-arrow prev" id="gbTravelBagPrev" type="button" aria-label="Previous image">‹</button>
        <button class="sports-arrow next" id="gbTravelBagNext" type="button" aria-label="Next image">›</button>
      </div>
      <div class="sports-info">
        <h2>Gangster Bougie GB Faux Leather Travel Bag</h2>
        <div class="sports-price">US$109.99</div>
        <p class="sports-description">Built for women who move with purpose and style. This Gangster Bougie faux leather travel bag pairs everyday practicality with a bold black-and-white GB design for a distinctive luxury streetwear finish.</p>
        <ul class="sports-benefits">
          <li>Premium PU faux leather exterior</li>
          <li>Large 9.5&quot; × 20.8&quot; travel size</li>
          <li>Spacious main storage compartment</li>
          <li>Carry handles for easy transport</li>
          <li>Black-and-white luxury finish</li>
          <li>Signature GB branding</li>
          <li>Designed for gym, travel, and everyday use</li>
        </ul>
        <hr class="sports-divider">
        <div class="sports-colour-line">Design: <strong>Black &amp; White GB</strong></div>
        <div class="sports-buy-row">
          <div class="sports-size-block"><span class="option-label">Size</span><div class="sizes"><button class="size active" type="button">9.5&quot; × 20.8&quot;</button></div></div>
          <button class="sports-add" type="button" aria-label="Add to cart coming soon"><span>🛒</span>Add to Cart</button>
        </div>
        <div class="sports-preview-note">Cart connection coming soon.</div>
      </div>
      <div class="sports-gallery">
        <button class="sports-thumb active gb-travel-bag-thumb" type="button" data-index="0"><img src="IMG_0416.jpeg" alt="Gangster Bougie GB Faux Leather Travel Bag front"><span class="sports-thumb-label">Front</span></button>
        <button class="sports-thumb gb-travel-bag-thumb" type="button" data-index="1"><img src="IMG_0417.jpeg" alt="Gangster Bougie GB Faux Leather Travel Bag side"><span class="sports-thumb-label">Side</span></button>
      </div>
    </div>
  </div>
</div>
'''
s=s[:mp]+gb_modal+s[mp:]

js='''
(function(){
 const modal=document.getElementById('gbTravelBagModal');
 const main=document.getElementById('gbTravelBagMain');
 const files=['IMG_0416.jpeg','IMG_0417.jpeg'];
 const labels=['Front','Side'];
 const thumbs=[...document.querySelectorAll('.gb-travel-bag-thumb')];
 let idx=0;
 function show(i){idx=(i+files.length)%files.length;main.src=files[idx];main.alt='Gangster Bougie GB Faux Leather Travel Bag '+labels[idx];thumbs.forEach((b,n)=>b.classList.toggle('active',n===idx));}
 document.getElementById('openGBTravelBag').onclick=()=>{modal.classList.add('open');modal.setAttribute('aria-hidden','false');show(0);document.body.style.overflow='hidden';};
 document.getElementById('closeGBTravelBag').onclick=()=>{modal.classList.remove('open');modal.setAttribute('aria-hidden','true');document.body.style.overflow='';};
 document.getElementById('gbTravelBagPrev').onclick=()=>show(idx-1);
 document.getElementById('gbTravelBagNext').onclick=()=>show(idx+1);
 thumbs.forEach((b,n)=>b.onclick=()=>show(n));
 modal.addEventListener('click',e=>{if(e.target===modal)document.getElementById('closeGBTravelBag').click();});
})();
'''
sp=s.rfind('</script>')
if sp<0: raise SystemExit('script close not found')
s=s[:sp]+js+s[sp:]
p.write_text(s)
