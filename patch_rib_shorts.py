from pathlib import Path
p=Path('index.html')
s=p.read_text()

marker='''</script>\n</body></html>'''
if marker not in s:
    raise SystemExit('Closing script marker not found')

swipe='''

// Touch swipe for every View Item image stage. Existing left/right arrows remain unchanged.
(function(){
 const modals=[...document.querySelectorAll('.modal')];
 modals.forEach(modal=>{
   const buttons=[...modal.querySelectorAll('button')];
   const prev=buttons.find(b=>/prev|previous/i.test((b.id||'')+' '+(b.getAttribute('aria-label')||''))) ||
              buttons.find(b=>['‹','←'].includes((b.textContent||'').trim()));
   const next=buttons.find(b=>/next/i.test((b.id||'')+' '+(b.getAttribute('aria-label')||''))) ||
              buttons.find(b=>['›','→'].includes((b.textContent||'').trim()));
   if(!prev||!next) return;
   let stage=prev.parentElement;
   if(!stage||!stage.contains(next)){
     stage=prev.closest('.sports-stage,.product-stage,.modal-stage')||modal.querySelector('.sports-stage,.product-stage,.modal-stage');
   }
   if(!stage||stage.dataset.gbSwipe==='1') return;
   stage.dataset.gbSwipe='1';
   stage.style.touchAction='pan-y';
   let startX=null,startY=null;
   stage.addEventListener('pointerdown',e=>{
     if(e.pointerType==='mouse') return;
     startX=e.clientX;startY=e.clientY;
   });
   stage.addEventListener('pointerup',e=>{
     if(startX===null) return;
     const dx=e.clientX-startX,dy=e.clientY-startY;
     startX=null;startY=null;
     if(Math.abs(dx)<45||Math.abs(dx)<=Math.abs(dy)) return;
     (dx<0?next:prev).click();
   });
   stage.addEventListener('pointercancel',()=>{startX=null;startY=null;});
 });
})();
'''

if 'dataset.gbSwipe' in s:
    raise SystemExit('Product swipe support already present')
s=s.replace(marker,swipe+marker,1)
p.write_text(s)
