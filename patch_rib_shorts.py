from pathlib import Path
p=Path('index.html')
s=p.read_text()

marker='''</script>\n</body></html>'''
if marker not in s:
    raise SystemExit('Closing script marker not found')

swipe='''

// Touch swipe for product View Item main-image stages. Existing arrow buttons remain unchanged.
(function(){
 const arrowSelector='.sports-arrow,.luxe-arrow,.leggings-arrow,.shorts-arrow,.cap-arrow,.bandana-arrow,.mens-jersey-arrow,.built-jersey-arrow,.muscle-tank-arrow,.sweatpants-arrow,.rib-shorts-arrow,.fashion-hoodie-arrow,.performance-tee-arrow,.gym-bottle-arrow,.travel-bag-arrow,.yoga-mat-arrow,.gym-bag-arrow,.gym-towel-arrow';
 const stages=[...new Set([...document.querySelectorAll(arrowSelector)].map(a=>a.parentElement).filter(Boolean))];
 stages.forEach(stage=>{
   if(stage.dataset.gbSwipe==='1') return;
   const arrows=[...stage.querySelectorAll(arrowSelector)];
   if(arrows.length<2) return;
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
     const arrow=dx<0?arrows[arrows.length-1]:arrows[0];
     if(arrow) arrow.click();
   });
   stage.addEventListener('pointercancel',()=>{startX=null;startY=null;});
 });
})();
'''

if 'dataset.gbSwipe' in s:
    raise SystemExit('Product swipe support already present')
s=s.replace(marker,swipe+marker,1)
p.write_text(s)
