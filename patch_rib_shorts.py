from pathlib import Path
p=Path('index.html')
s=p.read_text()

if 'data-filter="womens"' in s:
    raise SystemExit('Women filter already present')

# Add Women's filter immediately before Men's, keeping the existing filter styling/markup.
old='<button class="filter-btn" data-filter="mens">Men’s</button>'
new='<button class="filter-btn" data-filter="womens">Women’s</button>'+old
if old not in s:
    raise SystemExit('Men filter button not found')
s=s.replace(old,new,1)

# Mark the established women-specific products with a womens category token.
women_products=[
    'Women’s Baby Tee',
    'Gangster Bougie Women’s Luxe Bra',
    'Gangster Bougie Sports Bra',
    'Gangster Bougie Women’s Workout Shorts',
    'Gangster Bougie High-Waisted Leggings',
    'Women’s Laguna Cropped Hoodie',
    'Gangster Bougie Women’s Varsity Jacket',
]
for name in women_products:
    name_pos=s.find(f'<div class="product-name">{name}</div>')
    if name_pos < 0:
        continue
    article_start=s.rfind('<article class="product-card"',0,name_pos)
    tag_end=s.find('>',article_start)
    opening=s[article_start:tag_end+1]
    if 'data-category=' not in opening or 'womens' in opening:
        continue
    opening_new=opening.replace('data-category="','data-category="womens ',1)
    s=s[:article_start]+opening_new+s[tag_end+1:]

# Organize the shop grid once on load: women first, men second, accessories third,
# then any remaining products. Existing product cards/viewers are not redesigned.
organizer='''
(function(){
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
'''
sp=s.rfind('</script>')
if sp<0:
    raise SystemExit('script close not found')
s=s[:sp]+organizer+s[sp:]

p.write_text(s)
