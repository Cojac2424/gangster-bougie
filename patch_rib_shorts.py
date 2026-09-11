from pathlib import Path
p=Path('index.html'); s=p.read_text()
if 'id="openFashionHoodie"' in s:
    raise SystemExit('Fashion hoodie already exists')

# Duplicate the exact established Sweatpants exterior card structure, replacing only product data.
marker='<button class="view-item" id="openSweatpants">VIEW ITEM</button>'
pos=s.index(marker)
start=s.rfind('<article',0,pos)
end=s.index('</article>',pos)+len('</article>')
card=s[start:end]
hoodie_card=card
hoodie_card=hoodie_card.replace('IMG_0362.jpeg','IMG_0382.jpeg',1)
hoodie_card=hoodie_card.replace('Gangster Bougie Embroidered Fleece Sweatpants','Gangster Bougie “Self Made Still Bougie” Fashion Hoodie',1)
hoodie_card=hoodie_card.replace('8 colourways • US$69.99','4 colourways • US$59.99',1)
hoodie_card=hoodie_card.replace('id="openSweatpants"','id="openFashionHoodie"',1)
s=s[:end]+'\n'+hoodie_card+s[end:]

# Product viewer follows the established sports product-view template.
modal='''
<div class="modal" id="fashionHoodieModal" aria-hidden="true">
  <div class="modal-box sports-modal-box">
    <button class="modal-close" id="closeFashionHoodie" aria-label="Close"></button>
    <div class="sports-layout">
      <div class="sports-main-wrap">
        <div class="main-product-photo sports-stage"><img id="fashionHoodieMain" src="IMG_0382.jpeg" alt="Gangster Bougie Self Made Still Bougie Fashion Hoodie White front"></div>
        <button class="sports-arrow prev" id="fashionHoodiePrev" aria-label="Previous image">‹</button>
        <button class="sports-arrow next" id="fashionHoodieNext" aria-label="Next image">›</button>
      </div>
      <div class="sports-info">
        <h2>Gangster Bougie “Self Made Still Bougie” Fashion Hoodie</h2>
        <div class="sports-price">US$59.99</div>
        <p class="sports-description">Built for those who made their own lane. The Gangster Bougie Fashion Hoodie combines a clean streetwear silhouette with signature branding across the front and the bold “SELF MADE STILL BOUGIE” statement on the back. Designed for an elevated everyday look that represents confidence, ambition and the Gangster Bougie lifestyle.</p>
        <ul class="sports-benefits"><li>75% polyester, 20% cotton, 5% spandex</li><li>Medium-heavy 8.5 oz/yd² (300 g/m²) fabric</li><li>Unisex streetwear fit</li><li>Printed care label inside</li></ul>
        <hr class="sports-divider">
        <div class="sports-colour-line">Colour: <strong id="fashionHoodieColour">White</strong></div>
        <div class="sports-colors" id="fashionHoodieColours">
          <button class="sports-color white active" data-index="0" aria-label="White"></button>
          <button class="sports-color black" data-index="2" aria-label="Black"></button>
          <button class="sports-color" data-index="4" aria-label="Dark Grey" style="background:#555"></button>
          <button class="sports-color brown" data-index="6" aria-label="Brown"></button>
        </div>
        <div class="sports-buy-row"><div class="sports-size-block"><span class="option-label">Size</span><div class="sizes" id="fashionHoodieSizes"></div></div><button class="sports-add" type="button" aria-label="Add to cart coming soon"><span>🛒</span>Add to Cart</button></div>
        <div class="sports-preview-note">Cart connection coming soon.</div>
      </div>
      <div class="sports-gallery" id="fashionHoodieGallery"></div>
    </div>
  </div>
</div>
'''
body_end=s.rfind('</body>')
s=s[:body_end]+modal+s[body_end:]

script='''
<script>
(()=>{
 const modal=document.getElementById('fashionHoodieModal'), open=document.getElementById('openFashionHoodie'), close=document.getElementById('closeFashionHoodie');
 const main=document.getElementById('fashionHoodieMain'), gallery=document.getElementById('fashionHoodieGallery'), colour=document.getElementById('fashionHoodieColour'), sizes=document.getElementById('fashionHoodieSizes');
 const images=[
  ['IMG_0382.jpeg','White','Front'],['IMG_0384.jpeg','White','Back'],
  ['IMG_0380.jpeg','Black','Front'],['IMG_0381.jpeg','Black','Back'],
  ['IMG_0378.jpeg','Dark Grey','Front'],['IMG_0379.jpeg','Dark Grey','Back'],
  ['IMG_0376.jpeg','Brown','Front'],['IMG_0377.jpeg','Brown','Back']
 ];
 let current=0;
 const render=i=>{current=(i+images.length)%images.length; main.src=images[current][0]; main.alt='Gangster Bougie Self Made Still Bougie Fashion Hoodie '+images[current][1]+' '+images[current][2]; colour.textContent=images[current][1]; gallery.querySelectorAll('.sports-thumb').forEach((x,n)=>x.classList.toggle('active',n===current)); document.querySelectorAll('#fashionHoodieColours .sports-color').forEach(x=>x.classList.toggle('active',Number(x.dataset.index)===Math.floor(current/2)*2));};
 images.forEach((x,i)=>{const b=document.createElement('button');b.className='sports-thumb'+(i===0?' active':'');b.innerHTML='<img src="'+x[0]+'" alt="'+x[1]+' '+x[2]+'"><span class="sports-thumb-label">'+x[1]+' '+x[2]+'</span>';b.onclick=()=>render(i);gallery.appendChild(b)});
 ['S','M','L','XL','2XL'].forEach((x,i)=>{const b=document.createElement('button');b.className='size'+(i===0?' active':'');b.textContent=x;b.onclick=()=>{sizes.querySelectorAll('.size').forEach(y=>y.classList.remove('active'));b.classList.add('active')};sizes.appendChild(b)});
 document.querySelectorAll('#fashionHoodieColours .sports-color').forEach(b=>b.onclick=()=>render(Number(b.dataset.index)));
 document.getElementById('fashionHoodiePrev').onclick=()=>render(current-1);document.getElementById('fashionHoodieNext').onclick=()=>render(current+1);
 open.onclick=()=>{modal.classList.add('open');modal.setAttribute('aria-hidden','false');document.body.style.overflow='hidden'};
 close.onclick=()=>{modal.classList.remove('open');modal.setAttribute('aria-hidden','true');document.body.style.overflow=''};
 modal.onclick=e=>{if(e.target===modal)close.click()};
})();
</script>
'''
body_end=s.rfind('</body>')
s=s[:body_end]+script+s[body_end:]
p.write_text(s)
