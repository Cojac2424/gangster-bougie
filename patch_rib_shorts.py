from pathlib import Path
p=Path('index.html')
s=p.read_text()
if 'id="openTravelBag"' in s:
    raise SystemExit('Travel bag already present')

# Duplicate the established accessory product-card structure immediately after the gym bottle.
marker='id="openGymBottle"'
pos=s.index(marker)
article_end=s.index('</article>',pos)+len('</article>')
card='''
<article class="product-card" data-category="accessories">
  <div class="product-image"><img src="IMG_0414.jpeg" alt="Gangster Bougie Faux Leather Travel Bag"></div>
  <div class="product-accent"></div>
  <div class="product-info">
    <div class="product-tag">ACCESSORIES • TRAVEL</div>
    <div class="product-name">Gangster Bougie Faux Leather Travel Bag</div>
    <div class="product-status">Black • 9.5&quot; × 20.8&quot; • US$109.99</div>
    <button class="view-item" id="openTravelBag" type="button">View Item</button>
  </div>
</article>'''
s=s[:article_end]+card+s[article_end:]

# Use the exact established sports/product viewer classes.
modal_marker='<div class="modal" id="gymBottleModal"'
mp=s.index(modal_marker)
modal='''
<div class="modal" id="travelBagModal" aria-hidden="true">
  <div class="modal-box sports-modal-box">
    <button class="modal-close" id="closeTravelBag" type="button">Close</button>
    <div class="sports-layout">
      <div class="sports-main-wrap">
        <div class="main-product-photo sports-stage"><img id="travelBagMain" src="IMG_0414.jpeg" alt="Gangster Bougie Faux Leather Travel Bag"></div>
        <button class="sports-arrow prev" id="travelBagPrev" type="button" aria-label="Previous image">‹</button>
        <button class="sports-arrow next" id="travelBagNext" type="button" aria-label="Next image">›</button>
      </div>
      <div class="sports-info">
        <h2>Gangster Bougie Faux Leather Travel Bag</h2>
        <div class="sports-price">US$109.99</div>
        <p class="sports-description">Built for women who move with purpose and style. The Gangster Bougie Faux Leather Travel Bag brings together a clean luxury look with everyday practicality, finished in signature black with bold gold-and-white branding.</p>
        <ul class="sports-benefits">
          <li>Premium PU faux leather exterior</li>
          <li>Large 9.5&quot; × 20.8&quot; travel size</li>
          <li>Spacious main storage compartment</li>
          <li>Carry handles for easy transport</li>
          <li>Black luxury finish</li>
          <li>Signature Gangster Bougie branding</li>
          <li>Gold “Baddie” detail</li>
          <li>Designed for gym, travel, and everyday use</li>
        </ul>
        <hr class="sports-divider">
        <div class="sports-colour-line">Colour: <strong>Black</strong></div>
        <div class="sports-buy-row">
          <div class="sports-size-block"><span class="option-label">Size</span><div class="sizes"><button class="size active" type="button">9.5&quot; × 20.8&quot;</button></div></div>
          <button class="sports-add" type="button" aria-label="Add to cart coming soon"><span>🛒</span>Add to Cart</button>
        </div>
        <div class="sports-preview-note">Cart connection coming soon.</div>
      </div>
      <div class="sports-gallery">
        <button class="sports-thumb active travel-bag-thumb" type="button" data-index="0"><img src="IMG_0414.jpeg" alt="Gangster Bougie Faux Leather Travel Bag"><span class="sports-thumb-label">Front</span></button>
        <button class="sports-thumb travel-bag-thumb" type="button" data-index="1"><img src="IMG_0415.jpeg" alt="Gangster Bougie Faux Leather Travel Bag"><span class="sports-thumb-label">Back</span></button>
        <button class="sports-thumb travel-bag-thumb" type="button" data-index="2"><img src="IMG_0416.jpeg" alt="Gangster Bougie Faux Leather Travel Bag"><span class="sports-thumb-label">Front</span></button>
        <button class="sports-thumb travel-bag-thumb" type="button" data-index="3"><img src="IMG_0417.jpeg" alt="Gangster Bougie Faux Leather Travel Bag"><span class="sports-thumb-label">Side</span></button>
      </div>
    </div>
  </div>
</div>
'''
s=s[:mp]+modal+s[mp:]

js='''
(function(){
 const modal=document.getElementById('travelBagModal');
 const main=document.getElementById('travelBagMain');
 const files=['IMG_0414.jpeg','IMG_0415.jpeg','IMG_0416.jpeg','IMG_0417.jpeg'];
 const labels=['Front','Back','Front','Side'];
 const thumbs=[...document.querySelectorAll('.travel-bag-thumb')];
 let idx=0;
 function show(i){idx=(i+files.length)%files.length;main.src=files[idx];main.alt='Gangster Bougie Faux Leather Travel Bag '+labels[idx];thumbs.forEach((b,n)=>b.classList.toggle('active',n===idx));}
 document.getElementById('openTravelBag').onclick=()=>{modal.classList.add('open');modal.setAttribute('aria-hidden','false');show(0);document.body.style.overflow='hidden';};
 document.getElementById('closeTravelBag').onclick=()=>{modal.classList.remove('open');modal.setAttribute('aria-hidden','true');document.body.style.overflow='';};
 document.getElementById('travelBagPrev').onclick=()=>show(idx-1);
 document.getElementById('travelBagNext').onclick=()=>show(idx+1);
 thumbs.forEach((b,n)=>b.onclick=()=>show(n));
 modal.addEventListener('click',e=>{if(e.target===modal)document.getElementById('closeTravelBag').click();});
})();
'''
sp=s.rfind('</script>')
if sp<0: raise SystemExit('script close not found')
s=s[:sp]+js+s[sp:]
p.write_text(s)
