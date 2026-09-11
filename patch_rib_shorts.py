from pathlib import Path
p=Path('index.html'); s=p.read_text()
if 'id="openPerformanceTee"' in s:
    raise SystemExit('Performance tee already exists')

# Duplicate the exact established Sweatpants exterior card structure.
marker='<button class="view-item" id="openSweatpants">VIEW ITEM</button>'
pos=s.index(marker); start=s.rfind('<article',0,pos); end=s.index('</article>',pos)+len('</article>')
card=s[start:end]
tee=card.replace('IMG_0362.jpeg','IMG_0385.jpeg',1).replace('Gangster Bougie Embroidered Fleece Sweatpants','Gangster Bougie “Self Made Still Bougie” Performance T-Shirt',1).replace('8 colourways • US$69.99','14 colourways • US$46.99',1).replace('id="openSweatpants"','id="openPerformanceTee"',1)
s=s[:end]+'\n'+tee+s[end:]

modal='''
<div class="modal" id="performanceTeeModal" aria-hidden="true"><div class="modal-box sports-modal-box"><button class="modal-close" id="closePerformanceTee" aria-label="Close"></button><div class="sports-layout"><div class="sports-main-wrap"><div class="main-product-photo sports-stage"><img id="performanceTeeMain" src="IMG_0385.jpeg" alt="Gangster Bougie Self Made Still Bougie Performance T-Shirt Red front"></div><button class="sports-arrow prev" id="performanceTeePrev" aria-label="Previous image">‹</button><button class="sports-arrow next" id="performanceTeeNext" aria-label="Next image">›</button></div><div class="sports-info"><h2>Gangster Bougie “Self Made Still Bougie” Performance T-Shirt</h2><div class="sports-price">US$46.99</div><p class="sports-description">Built different. Made to move. The Gangster Bougie Performance T-Shirt combines everyday comfort with an athletic feel, featuring the signature arched Gangster Bougie branding on the front and the bold “SELF MADE STILL BOUGIE” statement with GB detail on the back. Designed for training, casual wear and everyday hustle.</p><ul class="sports-benefits"><li>100% spun polyester, ideal for sublimating</li><li>Moisture-wicking, odor control and snag-resistant</li><li>Modern classic fit with taped neck and shoulders</li><li>Made with OEKO-TEX certified low-impact dyes</li></ul><hr class="sports-divider"><div class="sports-colour-line">Colour: <strong id="performanceTeeColour">Red</strong></div><div class="sports-colors" id="performanceTeeColours"></div><div class="sports-buy-row"><div class="sports-size-block"><span class="option-label">Size</span><div class="sizes" id="performanceTeeSizes"></div></div><button class="sports-add" type="button" aria-label="Add to cart coming soon"><span>🛒</span>Add to Cart</button></div><div class="sports-preview-note">Cart connection coming soon.</div></div><div class="sports-gallery" id="performanceTeeGallery"></div></div></div></div>
'''
body=s.rfind('</body>'); s=s[:body]+modal+s[body:]
script='''
<script>
(()=>{
 const pairs=[['Red','#b72f35'],['Sport Grey','#aaa'],['White','#f5f5f2'],['Sage','#9aa58a'],['Prairie Dust','#b5a27c'],['Charcoal','#555'],['Sage Green','#77866b'],['Military Green','#596044'],['Dusty Green','#8b9277'],['Grey','#777'],['Black','#222'],['Light Grey','#bbb'],['Dark Grey','#444'],['Green','#536b50']];
 const files=[]; for(let n=385;n<=411;n+=2){files.push('IMG_0'+n+'.jpeg','IMG_0'+(n+1)+'.jpeg')}
 // The upload contains 28 files / 14 front-back pairs. Labels are provisional and can be switched after visual review.
 const modal=document.getElementById('performanceTeeModal'), main=document.getElementById('performanceTeeMain'), gallery=document.getElementById('performanceTeeGallery'), colour=document.getElementById('performanceTeeColour'), colors=document.getElementById('performanceTeeColours'), sizes=document.getElementById('performanceTeeSizes'); let current=0;
 pairs.forEach((p,i)=>{const b=document.createElement('button');b.className='sports-color'+(i===0?' active':'');b.style.background=p[1];b.dataset.index=i*2;b.setAttribute('aria-label',p[0]);b.onclick=()=>render(i*2);colors.appendChild(b)});
 files.forEach((f,i)=>{const pair=pairs[Math.floor(i/2)]||['Colour'];const side=i%2?'Back':'Front';const b=document.createElement('button');b.className='sports-thumb'+(i===0?' active':'');b.innerHTML='<img src="'+f+'" alt="'+pair[0]+' '+side+'"><span class="sports-thumb-label">'+pair[0]+' '+side+'</span>';b.onclick=()=>render(i);gallery.appendChild(b)});
 ['S','M','L','XL','2XL','3XL'].forEach((x,i)=>{const b=document.createElement('button');b.className='size'+(i===0?' active':'');b.textContent=x;b.onclick=()=>{sizes.querySelectorAll('.size').forEach(y=>y.classList.remove('active'));b.classList.add('active')};sizes.appendChild(b)});
 function render(i){current=(i+files.length)%files.length;main.src=files[current];const pi=Math.floor(current/2);colour.textContent=pairs[pi][0];gallery.querySelectorAll('.sports-thumb').forEach((x,n)=>x.classList.toggle('active',n===current));colors.querySelectorAll('.sports-color').forEach((x,n)=>x.classList.toggle('active',n===pi))}
 document.getElementById('performanceTeePrev').onclick=()=>render(current-1);document.getElementById('performanceTeeNext').onclick=()=>render(current+1);document.getElementById('openPerformanceTee').onclick=()=>{modal.classList.add('open');modal.setAttribute('aria-hidden','false');document.body.style.overflow='hidden'};document.getElementById('closePerformanceTee').onclick=()=>{modal.classList.remove('open');modal.setAttribute('aria-hidden','true');document.body.style.overflow=''};modal.onclick=e=>{if(e.target===modal)document.getElementById('closePerformanceTee').click()};
})();
</script>
'''
body=s.rfind('</body>'); s=s[:body]+script+s[body:]; p.write_text(s)
