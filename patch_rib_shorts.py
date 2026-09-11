from pathlib import Path
p=Path('index.html')
s=p.read_text()
if 'id="openGymBag"' in s:
    raise SystemExit('Gym bag already present')

# Add card after yoga mat using established product-card structure.
pos=s.index('id="openYogaMat"')
article_end=s.index('</article>',pos)+len('</article>')
card='''
<article class="product-card" data-category="accessories">
  <div class="product-image"><img src="IMG_0093.jpeg" alt="Gangster Bougie Gym Bag"></div>
  <div class="product-accent"></div>
  <div class="product-info">
    <div class="product-tag">ACCESSORIES • GYM</div>
    <div class="product-name">Gangster Bougie Gym Bag</div>
    <div class="product-status">6 colourways • US$54.99</div>
    <button class="view-item" id="openGymBag" type="button">View Item</button>
  </div>
</article>'''
s=s[:article_end]+card+s[article_end:]

mp=s.index('<div class="modal" id="yogaMatModal"')
modal='''
<div class="modal" id="gymBagModal" aria-hidden="true">
  <div class="modal-box sports-modal-box">
    <button class="modal-close" id="closeGymBag" type="button">Close</button>
    <div class="sports-layout">
      <div class="sports-main-wrap">
        <div class="main-product-photo sports-stage"><img id="gymBagMain" src="IMG_0093.jpeg" alt="Gangster Bougie Gym Bag Black"></div>
        <button class="sports-arrow prev" id="gymBagPrev" type="button" aria-label="Previous image">‹</button>
        <button class="sports-arrow next" id="gymBagNext" type="button" aria-label="Next image">›</button>
      </div>
      <div class="sports-info">
        <h2>Gangster Bougie Gym Bag</h2>
        <div class="sports-price">US$54.99</div>
        <p class="sports-description">A practical everyday gym bag built for workouts, travel, and life on the move. Designed with a spacious main compartment, easy-carry handles, and signature Gangster Bougie branding for a clean street-luxury look.</p>
        <ul class="sports-benefits">
          <li>Spacious main compartment</li>
          <li>Carry handles plus detachable, adjustable shoulder strap</li>
          <li>600D polyester with 50% recycled polyester</li>
          <li>Zippered main compartment and side zipper pocket</li>
          <li>Designed for gym gear, activewear, shoes, towel, bottle, and everyday essentials</li>
          <li>One size: 10.75&quot; × 20.75&quot; × 9.5&quot;</li>
        </ul>
        <hr class="sports-divider">
        <div class="sports-colour-line">Colour: <strong id="gymBagColourName">Black</strong></div>
        <div class="sports-colors" aria-label="Choose colour">
          <button class="sports-color gym-bag-color active" type="button" data-index="0" aria-label="Black" title="Black" style="background:#17191b"></button>
          <button class="sports-color gym-bag-color" type="button" data-index="1" aria-label="Gold" title="Gold" style="background:#d9a11e"></button>
          <button class="sports-color gym-bag-color" type="button" data-index="2" aria-label="Hunter" title="Hunter" style="background:#174b34"></button>
          <button class="sports-color gym-bag-color" type="button" data-index="3" aria-label="Maroon" title="Maroon" style="background:#762838"></button>
          <button class="sports-color gym-bag-color" type="button" data-index="4" aria-label="Tropical Pink" title="Tropical Pink" style="background:#d72c78"></button>
          <button class="sports-color gym-bag-color" type="button" data-index="5" aria-label="Royal" title="Royal" style="background:#2456a8"></button>
        </div>
        <div class="sports-buy-row">
          <div class="sports-size-block"><span class="option-label">Size</span><div class="sizes"><button class="size active" type="button">One Size</button></div></div>
          <button class="sports-add" type="button" aria-label="Add to cart coming soon"><span>🛒</span>Add to Cart</button>
        </div>
        <div class="sports-preview-note">Cart connection coming soon.</div>
      </div>
      <div class="sports-gallery">
        <button class="sports-thumb active gym-bag-thumb" type="button" data-index="0"><img src="IMG_0093.jpeg" alt="Black Gangster Bougie Gym Bag"><span class="sports-thumb-label">Black</span></button>
        <button class="sports-thumb gym-bag-thumb" type="button" data-index="1"><img src="IMG_0096.jpeg" alt="Gold Gangster Bougie Gym Bag"><span class="sports-thumb-label">Gold</span></button>
        <button class="sports-thumb gym-bag-thumb" type="button" data-index="2"><img src="IMG_0097.jpeg" alt="Hunter Gangster Bougie Gym Bag"><span class="sports-thumb-label">Hunter</span></button>
        <button class="sports-thumb gym-bag-thumb" type="button" data-index="3"><img src="IMG_0095.jpeg" alt="Maroon Gangster Bougie Gym Bag"><span class="sports-thumb-label">Maroon</span></button>
        <button class="sports-thumb gym-bag-thumb" type="button" data-index="4"><img src="IMG_0092.jpeg" alt="Tropical Pink Gangster Bougie Gym Bag"><span class="sports-thumb-label">Tropical Pink</span></button>
        <button class="sports-thumb gym-bag-thumb" type="button" data-index="5"><img src="IMG_0094.jpeg" alt="Royal Gangster Bougie Gym Bag"><span class="sports-thumb-label">Royal</span></button>
      </div>
    </div>
  </div>
</div>
'''
s=s[:mp]+modal+s[mp:]

js='''
(function(){
 const modal=document.getElementById('gymBagModal');
 const main=document.getElementById('gymBagMain');
 const name=document.getElementById('gymBagColourName');
 const files=['IMG_0093.jpeg','IMG_0096.jpeg','IMG_0097.jpeg','IMG_0095.jpeg','IMG_0092.jpeg','IMG_0094.jpeg'];
 const labels=['Black','Gold','Hunter','Maroon','Tropical Pink','Royal'];
 const thumbs=[...document.querySelectorAll('.gym-bag-thumb')];
 const colors=[...document.querySelectorAll('.gym-bag-color')];
 let idx=0;
 function show(i){idx=(i+files.length)%files.length;main.src=files[idx];main.alt=labels[idx]+' Gangster Bougie Gym Bag';name.textContent=labels[idx];thumbs.forEach((b,n)=>b.classList.toggle('active',n===idx));colors.forEach((b,n)=>b.classList.toggle('active',n===idx));}
 document.getElementById('openGymBag').onclick=()=>{modal.classList.add('open');modal.setAttribute('aria-hidden','false');show(0);document.body.style.overflow='hidden';};
 document.getElementById('closeGymBag').onclick=()=>{modal.classList.remove('open');modal.setAttribute('aria-hidden','true');document.body.style.overflow='';};
 document.getElementById('gymBagPrev').onclick=()=>show(idx-1);
 document.getElementById('gymBagNext').onclick=()=>show(idx+1);
 thumbs.forEach((b,n)=>b.onclick=()=>show(n));
 colors.forEach((b,n)=>b.onclick=()=>show(n));
 modal.addEventListener('click',e=>{if(e.target===modal)document.getElementById('closeGymBag').click();});
})();
'''
sp=s.rfind('</script>')
if sp<0: raise SystemExit('script close not found')
s=s[:sp]+js+s[sp:]
p.write_text(s)
