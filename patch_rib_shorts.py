from pathlib import Path
import re
p=Path('index.html')
s=p.read_text()

# Remove only the Outerwear filter button. Outerwear products remain available in Women's and All.
s=re.sub(r'\s*<button class="filter-btn(?: active)?" data-filter="outerwear"[^>]*>.*?</button>', '', s, count=1, flags=re.S)

# Replace the carousel's category-click handling so one click owns the state completely.
# Stop the site's older filter listener from also changing card display/classes after the carousel handles it.
old='''filterRow.addEventListener('click',e=>{
   const btn=e.target.closest('.filter-btn');if(!btn)return;
   setTimeout(()=>applyFilter(btn.dataset.filter||'all'),0);
 });'''
new='''filterRow.addEventListener('click',e=>{
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
 },true);'''
if old not in s:
    raise SystemExit('Carousel filter listener not found')
s=s.replace(old,new,1)
p.write_text(s)
