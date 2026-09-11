from pathlib import Path
p=Path('index.html')
s=p.read_text()

# Remove the older pre-carousel DOM reordering block. The carousel will be the sole owner
# of product ordering/filtering so two scripts no longer manage the same Shop cards.
old_reorder="""(function(){
 const grid=document.querySelector('#shop .products');
 if(!grid) return;
 const cards=[...grid.querySelectorAll('.product-card')];
 const rank=card=>{
   const cats=(card.dataset.category||'').split(/\\s+/);
   if(cats.includes('womens')) return 1;
   if(cats.includes('mens')) return 2;
   if(cats.includes('accessories')) return 3;
   return 4;
 };
 cards.map((card,index)=>({card,index,rank:rank(card)}))
      .sort((a,b)=>a.rank-b.rank||a.index-b.index)
      .forEach(x=>grid.appendChild(x.card));
})();

"""
if old_reorder not in s:
    raise SystemExit('Old pre-carousel reorder block not found')
s=s.replace(old_reorder,'',1)

old_pointer=""" grid.addEventListener('pointerdown',e=>{if(e.pointerType==='mouse'&&e.button!==0)return;startX=e.clientX;dragged=false;});
 grid.addEventListener('pointermove',e=>{if(startX===null)return;if(Math.abs(e.clientX-startX)>12)dragged=true;});
 grid.addEventListener('pointerup',e=>{if(startX===null)return;const dx=e.clientX-startX;startX=null;if(Math.abs(dx)>45)move(dx<0?1:-1);});
 grid.addEventListener('pointercancel',()=>{startX=null});
"""
new_pointer=""" let gestureToken=0;
 grid.addEventListener('pointerdown',e=>{
   if(e.pointerType==='mouse'&&e.button!==0)return;
   startX=e.clientX;dragged=false;
   grid.dataset.gesture=String(++gestureToken);
 });
 grid.addEventListener('pointermove',e=>{if(startX===null)return;if(Math.abs(e.clientX-startX)>12)dragged=true;});
 grid.addEventListener('pointerup',e=>{
   if(startX===null)return;
   const dx=e.clientX-startX;
   startX=null;
   if(Math.abs(dx)>45)move(dx<0?1:-1);
 });
 grid.addEventListener('pointercancel',()=>{startX=null;dragged=false;++gestureToken;});
"""
if old_pointer not in s:
    raise SystemExit('Current pointer block not found')
s=s.replace(old_pointer,new_pointer,1)

old_filter=""" // Use the site's existing filter buttons, but render matching cards in the carousel.
 // Own category selection at the button level so the older filter-row handler cannot
 // run first and leave the previously scrolled Accessories cards visible.
 filterRow.querySelectorAll('.filter-btn').forEach(btn=>{
   btn.addEventListener('click',e=>{
     e.preventDefault();
     e.stopImmediatePropagation();
     const filter=btn.dataset.filter||'all';
     filterRow.querySelectorAll('.filter-btn').forEach(b=>b.classList.toggle('active',b===btn));
     // Hard reset the complete carousel before building the newly selected category.
     allCards.forEach(card=>{
       card.classList.remove('gb-center','gb-far');
       card.style.display='none';
       card.style.transform='';
       card.style.opacity='';
       card.style.filter='';
       card.style.zIndex='';
       card.style.pointerEvents='';
     });
     startX=null;
     dragged=false;
     active=0;
     applyFilter(filter);
   },true);
 });
"""
new_filter=""" // Category changes are atomic: cancel any unfinished carousel gesture first,
 // then rebuild the selected category exactly once.
 function selectCategory(btn){
   const filter=btn.dataset.filter||'all';
   startX=null;
   dragged=false;
   ++gestureToken;
   filterRow.querySelectorAll('.filter-btn').forEach(b=>b.classList.toggle('active',b===btn));
   allCards.forEach(card=>{
     card.classList.remove('gb-center','gb-far');
     card.style.display='none';
     card.style.transform='';
     card.style.opacity='';
     card.style.filter='';
     card.style.zIndex='';
     card.style.pointerEvents='';
   });
   active=0;
   applyFilter(filter);
 }
 filterRow.querySelectorAll('.filter-btn').forEach(btn=>{
   // pointerdown runs before click on touch devices. Cancel the old carousel gesture here,
   // before the category tap can inherit the last swipe state.
   btn.addEventListener('pointerdown',()=>{startX=null;dragged=false;++gestureToken;},true);
   btn.addEventListener('click',e=>{
     e.preventDefault();
     e.stopImmediatePropagation();
     selectCategory(btn);
   },true);
 });
"""
if old_filter not in s:
    raise SystemExit('Current carousel filter block not found')
s=s.replace(old_filter,new_filter,1)
p.write_text(s)
