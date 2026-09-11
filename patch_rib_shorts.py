from pathlib import Path
p=Path('index.html')
s=p.read_text()
if 'id="openYogaMat"' in s:
    raise SystemExit('Yoga mat already present')

# Add the yoga mat card directly after the GB travel bag card, preserving the established card template.
pos=s.index('id="openGBTravelBag"')
article_end=s.index('</article>',pos)+len('</article>')
card='''
<article class="product-card" data-category="accessories">
  <div class="product-image"><img src="IMG_0204.jpeg" alt="Gangster Bougie Foam Yoga Mat"></div>
  <div class="product-accent"></div>
  <div class="product-info">
    <div class="product-tag">ACCESSORIES • ACTIVEWEAR</div>
    <div class="product-name">Gangster Bougie Foam Yoga Mat</div>
    <div class="product-status">6 colourways • US$109.99</div>
    <button class="view-item" id="openYogaMat" type="button">View Item</button>
  </div>
</article>'''
s=s[:article_end]+card+s[article_end:]

# Add the established Sports-Bra-style product viewer.
mp=s.index('<div class="modal" id="gbTravelBagModal"')
modal='''
<div class="modal" id="yogaMatModal" aria-hidden="true">
  <div class="modal-box sports-modal-box">
    <button class="modal-close" id="closeYogaMat" type="button">Close</button>
    <div class="sports-layout">
      <div class="sports-main-wrap">
        <div class="main-product-photo sports-stage"><img id="yogaMatMain" src="IMG_0204.jpeg" alt="Gangster Bougie Foam Yoga Mat Black"></div>
        <button class="sports-arrow prev" id="yogaMatPrev" type="button" aria-label="Previous image">‹</button>
        <button class="sports-arrow next" id="yogaMatNext" type="button" aria-label="Next image">›</button>
      </div>
      <div class="sports-info">
        <h2>Gangster Bougie Foam Yoga Mat</h2>
        <div class="sports-price">US$109.99</div>
        <p class="sports-description">Bring Gangster Bougie style into every stretch, workout, and recovery session. This branded foam yoga mat combines a cushioned workout surface with bold signature detailing for a clean, luxury activewear look.</p>
        <ul class="sports-benefits">
          <li>Cushioned 100% foam construction</li>
          <li>Full-length 24&quot; × 72&quot; workout and yoga mat</li>
          <li>0.25&quot; thick and lightweight</li>
          <li>Edge-to-edge print with signature GB and brand artwork</li>
          <li>Suitable for yoga, stretching, floor workouts, mobility work, and home training</li>
          <li>Easy addition to the Gangster Bougie activewear collection</li>
        </ul>
        <hr class="sports-divider">
        <div class="sports-colour-line">Colour: <strong id="yogaMatColourName">Black</strong></div>
        <div class="sports-colors" aria-label="Choose colour">
          <button class="sports-color yoga-mat-color active" type="button" data-index="0" aria-label="Black" title="Black" style="background:#17191b"></button>
          <button class="sports-color yoga-mat-color" type="button" data-index="1" aria-label="Dark Grey" title="Dark Grey" style="background:#626a68"></button>
          <button class="sports-color yoga-mat-color" type="button" data-index="2" aria-label="Dark Red" title="Dark Red" style="background:#c92332"></button>
          <button class="sports-color yoga-mat-color" type="button" data-index="3" aria-label="Dark Blue" title="Dark Blue" style="background:#2752a8"></button>
          <button class="sports-color yoga-mat-color" type="button" data-index="4" aria-label="Turquoise" title="Turquoise" style="background:#20a7bd"></button>
          <button class="sports-color yoga-mat-color" type="button" data-index="5" aria-label="Dark Green" title="Dark Green" style="background:#269754"></button>
        </div>
        <div class="sports-buy-row">
          <div class="sports-size-block"><span class="option-label">Size</span><div class="sizes"><button class="size active" type="button">24&quot; × 72&quot;</button></div></div>
          <button class="sports-add" type="button" aria-label="Add to cart coming soon"><span>🛒</span>Add to Cart</button>
        </div>
        <div class="sports-preview-note">Cart connection coming soon.</div>
      </div>
      <div class="sports-gallery">
        <button class="sports-thumb active yoga-mat-thumb" type="button" data-index="0"><img src="IMG_0204.jpeg" alt="Black Gangster Bougie Foam Yoga Mat"><span class="sports-thumb-label">Black</span></button>
        <button class="sports-thumb yoga-mat-thumb" type="button" data-index="1"><img src="IMG_0203.jpeg" alt="Dark Grey Gangster Bougie Foam Yoga Mat"><span class="sports-thumb-label">Dark Grey</span></button>
        <button class="sports-thumb yoga-mat-thumb" type="button" data-index="2"><img src="IMG_0201.jpeg" alt="Dark Red Gangster Bougie Foam Yoga Mat"><span class="sports-thumb-label">Dark Red</span></button>
        <button class="sports-thumb yoga-mat-thumb" type="button" data-index="3"><img src="IMG_0200.jpeg" alt="Dark Blue Gangster Bougie Foam Yoga Mat"><span class="sports-thumb-label">Dark Blue</span></button>
        <button class="sports-thumb yoga-mat-thumb" type="button" data-index="4"><img src="IMG_0199.jpeg" alt="Turquoise Gangster Bougie Foam Yoga Mat"><span class="sports-thumb-label">Turquoise</span></button>
        <button class="sports-thumb yoga-mat-thumb" type="button" data-index="5"><img src="IMG_0198.jpeg" alt="Dark Green Gangster Bougie Foam Yoga Mat"><span class="sports-thumb-label">Dark Green</span></button>
      </div>
    </div>
  </div>
</div>
'''
s=s[:mp]+modal+s[mp:]

js='''
(function(){
 const modal=document.getElementById('yogaMatModal');
 const main=document.getElementById('yogaMatMain');
 const name=document.getElementById('yogaMatColourName');
 const files=['IMG_0204.jpeg','IMG_0203.jpeg','IMG_0201.jpeg','IMG_0200.jpeg','IMG_0199.jpeg','IMG_0198.jpeg'];
 const labels=['Black','Dark Grey','Dark Red','Dark Blue','Turquoise','Dark Green'];
 const thumbs=[...document.querySelectorAll('.yoga-mat-thumb')];
 const colors=[...document.querySelectorAll('.yoga-mat-color')];
 let idx=0;
 function show(i){idx=(i+files.length)%files.length;main.src=files[idx];main.alt=labels[idx]+' Gangster Bougie Foam Yoga Mat';name.textContent=labels[idx];thumbs.forEach((b,n)=>b.classList.toggle('active',n===idx));colors.forEach((b,n)=>b.classList.toggle('active',n===idx));}
 document.getElementById('openYogaMat').onclick=()=>{modal.classList.add('open');modal.setAttribute('aria-hidden','false');show(0);document.body.style.overflow='hidden';};
 document.getElementById('closeYogaMat').onclick=()=>{modal.classList.remove('open');modal.setAttribute('aria-hidden','true');document.body.style.overflow='';};
 document.getElementById('yogaMatPrev').onclick=()=>show(idx-1);
 document.getElementById('yogaMatNext').onclick=()=>show(idx+1);
 thumbs.forEach((b,n)=>b.onclick=()=>show(n));
 colors.forEach((b,n)=>b.onclick=()=>show(n));
 modal.addEventListener('click',e=>{if(e.target===modal)document.getElementById('closeYogaMat').click();});
})();
'''
sp=s.rfind('</script>')
if sp<0: raise SystemExit('script close not found')
s=s[:sp]+js+s[sp:]
p.write_text(s)
