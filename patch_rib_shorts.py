from pathlib import Path
p=Path('index.html')
s=p.read_text()
if 'id="openGymTowel"' in s:
    raise SystemExit('Gym towel already present')

# Add card after Gym Bag using the established product-card structure.
pos=s.index('id="openGymBag"')
article_end=s.index('</article>',pos)+len('</article>')
card='''
<article class="product-card" data-category="accessories">
  <div class="product-image"><img src="IMG_0098.jpeg" alt="Gangster Bougie Gym Face Towel"></div>
  <div class="product-accent"></div>
  <div class="product-info">
    <div class="product-tag">ACCESSORIES • GYM</div>
    <div class="product-name">Gangster Bougie Gym Face Towel</div>
    <div class="product-status">Black • 13&quot; × 13&quot; • US$24.99</div>
    <button class="view-item" id="openGymTowel" type="button">View Item</button>
  </div>
</article>'''
s=s[:article_end]+card+s[article_end:]

# Insert modal immediately before the Gym Bag modal, preserving the established Sports-style viewer.
mp=s.index('<div class="modal" id="gymBagModal"')
modal='''
<div class="modal" id="gymTowelModal" aria-hidden="true">
  <div class="modal-box sports-modal-box">
    <button class="modal-close" id="closeGymTowel" type="button">Close</button>
    <div class="sports-layout">
      <div class="sports-main-wrap">
        <div class="main-product-photo sports-stage"><img id="gymTowelMain" src="IMG_0098.jpeg" alt="Gangster Bougie Gym Face Towel"></div>
        <button class="sports-arrow prev" id="gymTowelPrev" type="button" aria-label="Previous image">‹</button>
        <button class="sports-arrow next" id="gymTowelNext" type="button" aria-label="Next image">›</button>
      </div>
      <div class="sports-info">
        <h2>Gangster Bougie Gym Face Towel</h2>
        <div class="sports-price">US$24.99</div>
        <p class="sports-description">A compact workout towel made for gym sessions, training days, and life on the move. Designed in the signature Gangster Bougie black-and-gold style, it’s an easy finishing piece for your activewear setup.</p>
        <ul class="sports-benefits">
          <li>Compact workout / face towel</li>
          <li>100% polyester front and 100% cotton back</li>
          <li>Soft, absorbent and lightweight</li>
          <li>One-sided print with signature Gangster Bougie branding</li>
          <li>Designed for gym bags, workouts, training and travel</li>
          <li>One size: 13&quot; × 13&quot; (33 cm × 33 cm)</li>
        </ul>
        <hr class="sports-divider">
        <div class="sports-colour-line">Colour: <strong>Black</strong></div>
        <div class="sports-buy-row">
          <div class="sports-size-block"><span class="option-label">Size</span><div class="sizes"><button class="size active" type="button">13&quot; × 13&quot;</button></div></div>
          <button class="sports-add" type="button" aria-label="Add to cart coming soon"><span>🛒</span>Add to Cart</button>
        </div>
        <div class="sports-preview-note">Cart connection coming soon.</div>
      </div>
      <div class="sports-gallery">
        <button class="sports-thumb active gym-towel-thumb" type="button" data-index="0"><img src="IMG_0098.jpeg" alt="Gangster Bougie Gym Face Towel View 1"><span class="sports-thumb-label">View 1</span></button>
        <button class="sports-thumb gym-towel-thumb" type="button" data-index="1"><img src="IMG_0099.jpeg" alt="Gangster Bougie Gym Face Towel View 2"><span class="sports-thumb-label">View 2</span></button>
      </div>
    </div>
  </div>
</div>
'''
s=s[:mp]+modal+s[mp:]

js='''
(function(){
 const modal=document.getElementById('gymTowelModal');
 const main=document.getElementById('gymTowelMain');
 const files=['IMG_0098.jpeg','IMG_0099.jpeg'];
 const thumbs=[...document.querySelectorAll('.gym-towel-thumb')];
 let idx=0;
 function show(i){idx=(i+files.length)%files.length;main.src=files[idx];main.alt='Gangster Bougie Gym Face Towel View '+(idx+1);thumbs.forEach((b,n)=>b.classList.toggle('active',n===idx));}
 document.getElementById('openGymTowel').onclick=()=>{modal.classList.add('open');modal.setAttribute('aria-hidden','false');show(0);document.body.style.overflow='hidden';};
 document.getElementById('closeGymTowel').onclick=()=>{modal.classList.remove('open');modal.setAttribute('aria-hidden','true');document.body.style.overflow='';};
 document.getElementById('gymTowelPrev').onclick=()=>show(idx-1);
 document.getElementById('gymTowelNext').onclick=()=>show(idx+1);
 thumbs.forEach((b,n)=>b.onclick=()=>show(n));
 modal.addEventListener('click',e=>{if(e.target===modal)document.getElementById('closeGymTowel').click();});
})();
'''
sp=s.rfind('</script>')
if sp<0: raise SystemExit('script close not found')
s=s[:sp]+js+s[sp:]
p.write_text(s)
