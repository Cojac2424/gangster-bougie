from pathlib import Path
p=Path('index.html')
s=p.read_text()

old="""filterRow.addEventListener('click',e=>{
   const btn=e.target.closest('.filter-btn');if(!btn)return;
   e.preventDefault();
   e.stopImmediatePropagation();
   const filter=btn.dataset.filter||'all';
   filterRow.querySelectorAll('.filter-btn').forEach(b=>b.classList.toggle('active',b===btn));
   // Reset every card before loading the new category so no scrolled/previous state can leak across.
   allCards.forEach(card=>{
     card.classList.remove('gb-center','gb-far');
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
 },true);"""

new="""// Own category selection at the button level so the older filter-row handler cannot
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
 });"""

if old not in s:
    raise SystemExit('Current carousel category listener not found')
s=s.replace(old,new,1)
p.write_text(s)
