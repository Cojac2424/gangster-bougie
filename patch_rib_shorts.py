from pathlib import Path

p=Path('index.html')
s=p.read_text()

# v63 — reversible Women's Shop preview catalog.
# IMPORTANT rollback point: commit 42d2253b6833446c40daedf24a2c9580a8c9c9ba is the approved pre-catalog state.
# This adds a storefront preview using only already-confirmed real Printify images/prices.
# It does not alter Build Your Fit geometry, boards, joins, arrows, or existing cart logic.
if 'Women Shop preview catalog v63' not in s:
    css=r'''
<style>/* Women Shop preview catalog v63 */
#gbWomenCatalog{padding:68px 0;background:#080808;border-top:1px solid var(--border);border-bottom:1px solid var(--border)}
#gbWomenCatalog .gb-women-head{display:flex;justify-content:space-between;gap:28px;align-items:end;margin-bottom:26px}
#gbWomenCatalog h2{font-family:'Bodoni Moda',serif;font-size:clamp(2rem,5vw,3.4rem);text-transform:uppercase}
#gbWomenCatalog .gb-women-head p{max-width:520px;color:var(--muted)}
#gbWomenCatalog .gb-women-filters{display:flex;gap:9px;flex-wrap:wrap;margin-bottom:22px}
#gbWomenCatalog .gb-women-filter{border:1px solid #343434;background:#0d0d0d;color:#ddd;border-radius:999px;padding:8px 13px;font-size:.72rem;font-weight:900;text-transform:uppercase;letter-spacing:.06em;cursor:pointer}
#gbWomenCatalog .gb-women-filter.active{border-color:var(--gold);background:var(--gold-light);color:#111}
#gbWomenCatalog .gb-women-grid{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:16px}
#gbWomenCatalog .gb-women-card{background:#0d0d0d;border:1px solid #242424;overflow:hidden;display:flex;flex-direction:column}
#gbWomenCatalog .gb-women-img{aspect-ratio:1;background:#f4f3ef;overflow:hidden}
#gbWomenCatalog .gb-women-img img{width:100%;height:100%;object-fit:contain}
#gbWomenCatalog .gb-women-info{padding:15px;display:flex;flex-direction:column;flex:1}
#gbWomenCatalog .gb-women-tag{color:var(--gold-light);font-size:.65rem;font-weight:900;letter-spacing:.13em;text-transform:uppercase;margin-bottom:7px}
#gbWomenCatalog .gb-women-name{font-family:'Bodoni Moda',serif;font-size:.94rem;font-weight:900;line-height:1.2;text-transform:uppercase;min-height:2.4em}
#gbWomenCatalog .gb-women-price{font-weight:900;margin-top:9px}
#gbWomenCatalog .gb-women-view{margin-top:13px;width:100%;padding:10px;border:1px solid var(--gold);background:transparent;color:var(--gold-light);font-size:.7rem;font-weight:900;text-transform:uppercase;letter-spacing:.09em;cursor:pointer}
#gbWomenQuick{position:fixed;inset:0;z-index:120;background:rgba(0,0,0,.88);display:none;padding:22px;overflow:auto}
#gbWomenQuick.open{display:grid;place-items:center}
#gbWomenQuick .gb-wq-box{width:min(850px,100%);background:#0b0b0b;border:1px solid var(--border);padding:22px;position:relative;display:grid;grid-template-columns:1fr 1fr;gap:26px}
#gbWomenQuick .gb-wq-close{position:absolute;right:12px;top:12px;width:38px;height:38px;border-radius:50%;border:1px solid var(--gold);background:#080808;color:var(--gold-light);font-size:1.25rem;cursor:pointer;z-index:2}
#gbWomenQuick .gb-wq-pics{display:grid;grid-template-columns:1fr 1fr;gap:8px;align-content:start}
#gbWomenQuick .gb-wq-pics img{width:100%;aspect-ratio:1;object-fit:contain;background:#f4f3ef}
#gbWomenQuick h3{font-family:'Bodoni Moda',serif;font-size:clamp(1.5rem,4vw,2.25rem);line-height:1.05;margin:12px 40px 8px 0}
#gbWomenQuick .gb-wq-price{font-size:1.2rem;font-weight:900;color:var(--gold-light);margin-bottom:14px}
#gbWomenQuick .gb-wq-label{display:block;margin:16px 0 8px;font-size:.72rem;font-weight:900;text-transform:uppercase;letter-spacing:.1em}
#gbWomenQuick .gb-wq-sizes{display:flex;gap:8px;flex-wrap:wrap}
#gbWomenQuick .gb-wq-size{min-width:42px;height:42px;padding:0 9px;border:1px solid #555;background:#111;color:#fff;cursor:pointer}
#gbWomenQuick .gb-wq-size.active{border-color:var(--gold);color:var(--gold-light)}
#gbWomenQuick .gb-wq-add{margin-top:20px;width:100%;padding:14px;border:0;background:linear-gradient(135deg,#f6d56c,#d8a928);color:#111;font-weight:900;text-transform:uppercase;cursor:pointer}
#gbWomenQuick .gb-wq-note{color:#999;font-size:.78rem;margin-top:10px}
@media(max-width:900px){#gbWomenCatalog .gb-women-grid{grid-template-columns:repeat(3,1fr)}}
@media(max-width:650px){#gbWomenCatalog{padding:42px 0}#gbWomenCatalog .gb-women-head{display:block}#gbWomenCatalog .gb-women-head p{margin-top:8px}#gbWomenCatalog .gb-women-grid{grid-template-columns:repeat(2,1fr);gap:10px}#gbWomenCatalog .gb-women-info{padding:11px}#gbWomenCatalog .gb-women-name{font-size:.8rem}#gbWomenQuick{padding:10px}#gbWomenQuick .gb-wq-box{grid-template-columns:1fr;padding:14px;gap:12px}#gbWomenQuick .gb-wq-copy{padding-bottom:8px}}
</style>
'''
    html=r'''
<section id="gbWomenCatalog">
 <div class="container">
  <div class="gb-women-head"><div><div class="eyebrow">Gangster Bougie Women</div><h2>Shop Women</h2></div><p>Shop the pieces behind the fits. Start with the collection, then choose your exact size before adding it to your bag.</p></div>
  <div class="gb-women-filters"><button class="gb-women-filter active" data-filter="all">All</button><button class="gb-women-filter" data-filter="signature">Signature</button><button class="gb-women-filter" data-filter="classic">Classic</button><button class="gb-women-filter" data-filter="bra">Sports Bras</button><button class="gb-women-filter" data-filter="leggings">Leggings</button><button class="gb-women-filter" data-filter="shorts">Workout Shorts</button></div>
  <div class="gb-women-grid" id="gbWomenGrid"></div>
 </div>
</section>
<div id="gbWomenQuick" aria-hidden="true"><div class="gb-wq-box"><button class="gb-wq-close" aria-label="Close">×</button><div class="gb-wq-pics"><img id="gbWqFront" loading="lazy" decoding="async"><img id="gbWqBack" loading="lazy" decoding="async"></div><div class="gb-wq-copy"><div class="gb-women-tag" id="gbWqTag"></div><h3 id="gbWqName"></h3><div class="gb-wq-price" id="gbWqPrice"></div><span class="gb-wq-label">Choose size</span><div class="gb-wq-sizes" id="gbWqSizes"></div><button class="gb-wq-add" id="gbWqAdd">Add to Cart</button><div class="gb-wq-note">Made to order. Select your size before adding to cart.</div></div></div></div>
'''
    js=r'''
<script>/* Women Shop preview catalog v63 */
(function(){
 const P=[
  ['GB Classic Sports Bra – Cream','classic bra',39.99,['S','M','L','XL','2XL'],'IMG_0589.jpeg','IMG_0590.jpeg'],
  ['GB Classic Sports Bra – Grey','classic bra',39.99,['S','M','L','XL','2XL'],'IMG_0586.jpeg','IMG_0588.jpeg'],
  ['GB Classic Sports Bra – Black','classic bra',39.99,['S','M','L','XL','2XL'],'IMG_0597.jpeg','IMG_0598.jpeg'],
  ['GB Classic Sports Bra – Blue','classic bra',39.99,['S','M','L','XL','2XL'],'IMG_0591.jpeg','IMG_0592.jpeg'],
  ['GB Classic Sports Bra – Green','classic bra',39.99,['S','M','L','XL','2XL'],'IMG_0595.jpeg','IMG_0596.jpeg'],
  ['GB Classic Sports Bra – Red','classic bra',39.99,['S','M','L','XL','2XL'],'IMG_0593.jpeg','IMG_0594.jpeg'],
  ['GB Classic Sports Bra – Espresso','classic bra',39.99,['S','M','L','XL','2XL'],'IMG_0611.jpeg','IMG_0612.jpeg'],
  ['GB Classic High-Waisted Leggings – Cream','classic leggings',69.99,['XS','S','M','L','XL','2XL'],'IMG_0584.jpeg','IMG_0585.jpeg'],
  ['GB Classic High-Waisted Leggings – Grey','classic leggings',69.99,['XS','S','M','L','XL','2XL'],'IMG_0607.jpeg','IMG_0608.jpeg'],
  ['GB Classic High-Waisted Leggings – Black','classic leggings',69.99,['XS','S','M','L','XL','2XL'],'IMG_0605.jpeg','IMG_0606.jpeg'],
  ['GB Classic High-Waisted Leggings – Blue','classic leggings',69.99,['XS','S','M','L','XL','2XL'],'IMG_0603.jpeg','IMG_0604.jpeg'],
  ['GB Classic High-Waisted Leggings – Green','classic leggings',69.99,['XS','S','M','L','XL','2XL'],'IMG_0601.jpeg','IMG_0602.jpeg'],
  ['GB Classic High-Waisted Leggings – Red','classic leggings',69.99,['XS','S','M','L','XL','2XL'],'IMG_0599.jpeg','IMG_0600.jpeg'],
  ['GB Classic High-Waisted Leggings – Espresso','classic leggings',69.99,['XS','S','M','L','XL','2XL'],'IMG_0609.jpeg','IMG_0610.jpeg'],
  ['Cream Leggings','signature leggings',69.99,['XS','S','M','L','XL','2XL'],'IMG_0553.jpeg','IMG_0554.jpeg'],
  ['Oxblood Leggings','signature leggings',69.99,['XS','S','M','L','XL','2XL'],'IMG_0549.jpeg','IMG_0550.jpeg'],
  ['Onyx Leggings','signature leggings',69.99,['XS','S','M','L','XL','2XL'],'IMG_0541.jpeg','IMG_0542.jpeg'],
  ['Bougie Houndstooth Leggings','signature leggings',69.99,['XS','S','M','L','XL','2XL'],'IMG_0534.jpeg','IMG_0535.jpeg'],
  ['Vault Leggings','signature leggings',69.99,['XS','S','M','L','XL','2XL'],'IMG_0525.jpeg','IMG_0526.jpeg'],
  ['Heritage Plaid Leggings','signature leggings',69.99,['XS','S','M','L','XL','2XL'],'IMG_0520.jpeg','IMG_0521.jpeg'],
  ['Cream Workout Shorts','signature shorts',54.99,['XS','S','M','L','XL'],'IMG_0557.jpeg','IMG_0558.jpeg'],
  ['Oxblood Workout Shorts','signature shorts',54.99,['XS','S','M','L','XL'],'IMG_0555.jpeg','IMG_0556.jpeg'],
  ['Onyx Workout Shorts','signature shorts',54.99,['XS','S','M','L','XL'],'IMG_0543.jpeg','IMG_0544.jpeg'],
  ['Bougie Houndstooth Workout Shorts','signature shorts',54.99,['XS','S','M','L','XL'],'IMG_0536.jpeg','IMG_0537.jpeg'],
  ['Vault Workout Shorts','signature shorts',54.99,['XS','S','M','L','XL'],'IMG_0529.jpeg','IMG_0530.jpeg'],
  ['Heritage Plaid Workout Shorts','signature shorts',54.99,['XS','S','M','L','XL'],'IMG_0515.jpeg','IMG_0516.jpeg']
 ];
 const grid=document.getElementById('gbWomenGrid'),modal=document.getElementById('gbWomenQuick');if(!grid||!modal)return;
 let current=null,size='';
 function money(v){return 'US$'+v.toFixed(2)}
 function render(filter){grid.innerHTML='';P.forEach(function(p,i){if(filter!=='all'&&!p[1].split(' ').includes(filter))return;const c=document.createElement('article');c.className='gb-women-card';c.innerHTML='<div class="gb-women-img"><img loading="lazy" decoding="async" src="'+p[5]+'" alt="'+p[0]+'"></div><div class="gb-women-info"><div class="gb-women-tag">'+p[1].split(' ')[0]+' Collection</div><div class="gb-women-name">'+p[0]+'</div><div class="gb-women-price">'+money(p[2])+'</div><button class="gb-women-view" data-i="'+i+'">View Item</button></div>';grid.appendChild(c)})}
 function openItem(i){current=P[i];size='';document.getElementById('gbWqFront').src=current[5];document.getElementById('gbWqBack').src=current[6];document.getElementById('gbWqName').textContent=current[0];document.getElementById('gbWqTag').textContent=current[1].split(' ')[0]+' Collection';document.getElementById('gbWqPrice').textContent=money(current[2]);const s=document.getElementById('gbWqSizes');s.innerHTML='';current[3].forEach(function(x){const b=document.createElement('button');b.className='gb-wq-size';b.textContent=x;b.onclick=function(){size=x;s.querySelectorAll('button').forEach(q=>q.classList.remove('active'));b.classList.add('active')};s.appendChild(b)});modal.classList.add('open');modal.setAttribute('aria-hidden','false')}
 function close(){modal.classList.remove('open');modal.setAttribute('aria-hidden','true')}
 grid.addEventListener('click',function(e){const b=e.target.closest('.gb-women-view');if(b)openItem(Number(b.dataset.i))});
 document.querySelectorAll('.gb-women-filter').forEach(function(b){b.onclick=function(){document.querySelectorAll('.gb-women-filter').forEach(x=>x.classList.remove('active'));b.classList.add('active');render(b.dataset.filter)}});
 modal.querySelector('.gb-wq-close').onclick=close;modal.addEventListener('click',function(e){if(e.target===modal)close()});
 document.getElementById('gbWqAdd').onclick=function(){if(!current)return;if(!size){alert('Please choose a size first.');return}try{let cart=JSON.parse(localStorage.getItem('gbCart')||'[]');const hit=cart.find(x=>x.name===current[0]&&x.size===size);if(hit)hit.qty=(hit.qty||1)+1;else cart.push({name:current[0],size:size,price:current[2],qty:1,image:current[5]});localStorage.setItem('gbCart',JSON.stringify(cart));if(window.gbCartRefresh)window.gbCartRefresh();close();const link=document.getElementById('gbCartLink');if(link)link.click()}catch(e){}};
 render('all');
})();
</script>
'''
    s=s.replace('</head>',css+'\n</head>')
    # Place the preview immediately before Build Your Fit when possible; otherwise before footer.
    marker='<section id="build-your-fit"'
    if marker in s:
        s=s.replace(marker,html+'\n'+marker,1)
    else:
        s=s.replace('</footer>',html+'\n</footer>',1)
    s=s.replace('</body>',js+'\n</body>')

p.write_text(s)
