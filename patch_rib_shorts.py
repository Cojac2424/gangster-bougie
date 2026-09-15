from pathlib import Path

p=Path('index.html')
s=p.read_text()

# v47 — stop the shorts cart thumbnail observer from recursively rewriting its own DOM.
# Cart/performance fix only. No Build Your Fit geometry, joins, sizing, arrows or layout changed.
if 'Shorts cart freeze fix v47' not in s:
    js=r'''
<script>/* Shorts cart freeze fix v47 */
(function(){
 const thumbMap={
  'Cream Workout Shorts':'IMG_0555.jpeg','Oxblood Workout Shorts':'IMG_0557.jpeg','Onyx Workout Shorts':'IMG_0543.jpeg',
  'Bougie Houndstooth Workout Shorts':'IMG_0536.jpeg','Vault Workout Shorts':'IMG_0529.jpeg','Heritage Plaid Workout Shorts':'IMG_0515.jpeg'
 };
 function repair(){
  document.querySelectorAll('.gb-cart-line').forEach(function(row){
   const nameEl=row.querySelector('.gb-cart-line-name'),slot=row.querySelector('.gb-cart-thumb-slot');
   if(!nameEl||!slot)return;
   const name=(nameEl.textContent||'').trim(),src=thumbMap[name];
   if(!src)return;
   let img=slot.querySelector('img.gb-cart-thumb');
   if(!img){img=document.createElement('img');img.className='gb-cart-thumb';img.loading='lazy';img.decoding='async';slot.appendChild(img)}
   if(img.getAttribute('src')!==src)img.src=src;
   if(img.alt!==name)img.alt=name;
  });
 }
 // Disconnect the v46 body-wide observer by replacing its mutation target before it can self-loop.
 // A lightweight observer watches only cart line additions and never clears/rebuilds existing thumbnail DOM.
 const lines=document.getElementById('gbCartLines');
 if(lines&&window.MutationObserver){
   let queued=false;
   new MutationObserver(function(){if(queued)return;queued=true;requestAnimationFrame(function(){queued=false;repair()})}).observe(lines,{childList:true});
 }
 const link=document.getElementById('gbCartLink');if(link)link.addEventListener('click',function(){requestAnimationFrame(repair)});
 const add=document.getElementById('byfAddFit');if(add)add.addEventListener('click',function(){requestAnimationFrame(function(){requestAnimationFrame(repair)})});
 repair();
})();
</script>
'''
    # Remove the dangerous v46 body-wide observer line so it cannot recursively fire on its own thumbnail writes.
    s=s.replace(" document.addEventListener('click',()=>setTimeout(repairCartThumbs,0),true);\n new MutationObserver(repairCartThumbs).observe(document.body,{childList:true,subtree:true});",
                " // v47: body-wide self-mutating observer removed; cart thumbnails are handled by the lightweight cart observer below.")
    s=s.replace('</body>',js+'</body>')

p.write_text(s)
