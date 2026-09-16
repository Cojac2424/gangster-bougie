from pathlib import Path

p=Path('index.html')
s=p.read_text()

# v70 — hard-stop the legacy Shop Women mutation loop.
# v68's observer remains embedded in generated index.html even after later patch versions.
# Disconnect legacy observers by replacing the modal node once at startup, then use direct click lifecycle only.
# Build Your Fit geometry, cart, catalogue layout and product images remain untouched.
if 'Shop Women hard freeze fix v70' not in s:
    js=r'''
<script>/* Shop Women hard freeze fix v70 */
(function(){
 const leggings=['Runs small; consider sizing up.','83% Polyester, 17% Spandex.','Skinny fit.','Outside seam thread is color-matched.','Interior seam thread is white.','Double-layer waistband.','Slightly see-through when stretched; undyed white may show at seams and sewn areas.','Assembled in the USA from globally sourced parts.'];
 const shorts=['100% polyester.','Medium-heavy fabric: 8.5 oz/yd² (290 g/m²).','Printed-in size and care label.','Seam thread is automatically matched to the design in black or white.','Assembled in the USA from globally sourced parts.'];
 function norm(v){return (v||'').replace(/\s+/g,' ').trim()}
 function verified(name){name=norm(name);if(/^(Cream|Oxblood|Onyx|Bougie Houndstooth|Vault|Heritage Plaid) Leggings$/.test(name))return leggings;if(/^(Cream|Oxblood|Onyx|Bougie Houndstooth|Vault|Heritage Plaid) Workout Shorts$/.test(name))return shorts;return null}
 function paint(){
  const modal=document.getElementById('gbWomenQuick'),name=document.getElementById('gbWqName');if(!modal||!name)return;
  const old=document.getElementById('gbWqDetails');if(old)old.remove();
  let d=document.getElementById('gbWqDetailsV70');const copy=modal.querySelector('.gb-wq-copy');if(!copy)return;
  if(!d){d=document.createElement('details');d.id='gbWqDetailsV70';d.className='gb-wq-details';d.innerHTML='<summary>Product Details</summary><div class="gb-wq-details-body" id="gbWqDetailsBodyV70"></div>';const add=document.getElementById('gbWqAdd');if(add)copy.insertBefore(d,add);else copy.appendChild(d)}
  const info=verified(name.textContent);d.open=false;if(!info){d.hidden=true;return}d.hidden=false;
  const body=document.getElementById('gbWqDetailsBodyV70');if(body)body.innerHTML='<ul>'+info.map(function(x){return '<li>'+x+'</li>'}).join('')+'</ul>'
 }
 function install(){
  // Replacing this node disconnects MutationObservers attached directly to the old modal by v67/v68.
  const oldModal=document.getElementById('gbWomenQuick');
  if(oldModal&&oldModal.parentNode){const fresh=oldModal.cloneNode(true);oldModal.parentNode.replaceChild(fresh,oldModal)}
  document.addEventListener('click',function(e){if(e.target.closest('#gbWomenGrid .gb-women-view'))setTimeout(paint,0)},true);
 }
 if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',install);else install();
})();
</script>
'''
    s=s.replace('</body>',js+'\n</body>')

p.write_text(s)
