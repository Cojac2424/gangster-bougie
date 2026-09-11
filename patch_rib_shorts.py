from pathlib import Path
p=Path('index.html')
s=p.read_text()
if 'id="openGymBottle"' in s:
    raise SystemExit('Gym bottle already present')

# Add the bottle card immediately after the Performance T-Shirt card, preserving the exact established card classes.
marker='id="openPerformanceTee"'
pos=s.index(marker)
article_start=s.rfind('<article',0,pos)
article_end=s.index('</article>',pos)+len('</article>')
card='''
<article class="product-card" data-category="accessories">
  <div class="product-image"><img src="IMG_0412.jpeg" alt="Gangster Bougie Stainless Steel Gym Bottle"></div>
  <div class="product-accent"></div>
  <div class="product-info">
    <div class="product-tag">ACCESSORIES • GYM</div>
    <div class="product-name">Gangster Bougie Stainless Steel Gym Bottle</div>
    <div class="product-status">12 oz US$49.99 • 18 oz US$54.99</div>
    <button class="view-item" id="openGymBottle" type="button">View Item</button>
  </div>
</article>'''
s=s[:article_end]+card+s[article_end:]

# Add viewer before the Performance Tee viewer. Same sports/product viewer structure used throughout the store.
modal_marker='<div class="modal" id="performanceTeeModal"'
mp=s.index(modal_marker)
modal='''
<div class="modal" id="gymBottleModal" aria-hidden="true">
  <div class="modal-box sports-modal-box">
    <button class="modal-close" id="closeGymBottle" type="button">Close</button>
    <div class="sports-layout">
      <div class="sports-main-wrap">
        <div class="main-product-photo sports-stage"><img id="gymBottleMain" src="IMG_0412.jpeg" alt="Gangster Bougie Stainless Steel Gym Bottle 12 oz"></div>
        <button class="sports-arrow prev" id="gymBottlePrev" type="button" aria-label="Previous image">‹</button>
        <button class="sports-arrow next" id="gymBottleNext" type="button" aria-label="Next image">›</button>
      </div>
      <div class="sports-info">
        <h2>Gangster Bougie Stainless Steel Gym Bottle</h2>
        <div class="sports-price" id="gymBottlePrice">US$49.99</div>
        <p class="sports-description">Hydration with hustle. This black stainless-steel bottle brings Gangster Bougie style to the gym, work, travel, and everyday life with signature black, white, and gold branding.</p>
        <ul class="sports-benefits">
          <li>Durable stainless-steel construction</li>
          <li>Carry-handle lid</li>
          <li>Sleek black finish</li>
          <li>Signature Gangster Bougie branding</li>
          <li>Reusable and easy to carry</li>
          <li>Designed for gym, travel, work, and everyday use</li>
        </ul>
        <hr class="sports-divider">
        <div class="sports-colour-line">Colour: <strong>Black</strong></div>
        <div class="sports-buy-row">
          <div class="sports-size-block">
            <span class="option-label">Size</span>
            <div class="sizes">
              <button class="size active gym-bottle-size" type="button" data-index="0" data-price="US$49.99">12 oz</button>
              <button class="size gym-bottle-size" type="button" data-index="1" data-price="US$54.99">18 oz</button>
            </div>
          </div>
          <button class="sports-add" type="button" aria-label="Add to cart coming soon"><span>🛒</span>Add to Cart</button>
        </div>
        <div class="sports-preview-note">Cart connection coming soon.</div>
      </div>
      <div class="sports-gallery">
        <button class="sports-thumb active gym-bottle-thumb" type="button" data-index="0"><img src="IMG_0412.jpeg" alt="Gangster Bougie Stainless Steel Gym Bottle 12 oz"><span class="sports-thumb-label">12 oz</span></button>
        <button class="sports-thumb gym-bottle-thumb" type="button" data-index="1"><img src="IMG_0413.jpeg" alt="Gangster Bougie Stainless Steel Gym Bottle 18 oz"><span class="sports-thumb-label">18 oz</span></button>
      </div>
    </div>
  </div>
</div>
'''
s=s[:mp]+modal+s[mp:]

# Wire viewer without touching any existing product behaviour.
js='''
(function(){
 const modal=document.getElementById('gymBottleModal');
 const main=document.getElementById('gymBottleMain');
 const price=document.getElementById('gymBottlePrice');
 const files=['IMG_0412.jpeg','IMG_0413.jpeg'];
 const labels=['12 oz','18 oz'];
 const prices=['US$49.99','US$54.99'];
 const thumbs=[...document.querySelectorAll('.gym-bottle-thumb')];
 const sizes=[...document.querySelectorAll('.gym-bottle-size')];
 let idx=0;
 function show(i){idx=(i+files.length)%files.length;main.src=files[idx];main.alt='Gangster Bougie Stainless Steel Gym Bottle '+labels[idx];price.textContent=prices[idx];thumbs.forEach((b,n)=>b.classList.toggle('active',n===idx));sizes.forEach((b,n)=>b.classList.toggle('active',n===idx));}
 document.getElementById('openGymBottle').onclick=()=>{modal.classList.add('open');modal.setAttribute('aria-hidden','false');show(0);document.body.style.overflow='hidden';};
 document.getElementById('closeGymBottle').onclick=()=>{modal.classList.remove('open');modal.setAttribute('aria-hidden','true');document.body.style.overflow='';};
 document.getElementById('gymBottlePrev').onclick=()=>show(idx-1);
 document.getElementById('gymBottleNext').onclick=()=>show(idx+1);
 thumbs.forEach((b,n)=>b.onclick=()=>show(n));
 sizes.forEach((b,n)=>b.onclick=()=>show(n));
 modal.addEventListener('click',e=>{if(e.target===modal)document.getElementById('closeGymBottle').click();});
})();
'''
sp=s.rfind('</script>')
if sp<0: raise SystemExit('script close not found')
s=s[:sp]+js+s[sp:]
p.write_text(s)
