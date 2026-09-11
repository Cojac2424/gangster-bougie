from pathlib import Path
p=Path('index.html')
s=p.read_text()
if 'GB_SHOP_CAROUSEL_V1' in s:
    raise SystemExit('Shop carousel already present')

# Keep the existing product cards and View Item handlers intact; only change how
# the Shop collection is presented. This makes rollback straightforward.
css='''
/* GB_SHOP_CAROUSEL_V1 */
#shop .products.gb-coverflow{display:block;position:relative;height:590px;max-width:1160px;margin:0 auto;perspective:1400px;overflow:hidden;touch-action:pan-y;user-select:none;-webkit-user-select:none}
#shop .products.gb-coverflow .product-card{position:absolute;left:50%;top:18px;width:min(300px,72vw);height:520px;margin:0;transition:transform .48s cubic-bezier(.2,.75,.2,1),opacity .4s ease,filter .4s ease;transform-origin:center center;will-change:transform,opacity;box-shadow:0 24px 50px rgba(0,0,0,.55);border-color:#292929;cursor:grab}
#shop .products.gb-coverflow .product-card.gb-center{border-color:var(--gold);box-shadow:0 28px 65px rgba(0,0,0,.72),0 0 0 1px rgba(244,207,99,.18),0 0 30px rgba(216,169,40,.12);cursor:default}
#shop .products.gb-coverflow .product-card.gb-far{pointer-events:none}
#shop .products.gb-coverflow .product-image{flex:0 0 auto}
#shop .products.gb-coverflow .product-info{min-height:190px}
.gb-carousel-arrow{position:absolute;top:50%;transform:translateY(-50%);z-index:12;width:48px;height:48px;border-radius:50%;border:1px solid var(--gold);background:rgba(5,5,5,.92);color:var(--gold-light);font-size:1.9rem;line-height:1;cursor:pointer;display:grid;place-items:center;box-shadow:0 6px 22px rgba(0,0,0,.55)}
.gb-carousel-arrow:hover{background:var(--gold-light);color:#111}.gb-carousel-arrow.prev{left:8px}.gb-carousel-arrow.next{right:8px}
.gb-carousel-count{text-align:center;color:#8f8f8f;font-size:.72rem;letter-spacing:.12em;text-transform:uppercase;margin-top:-4px;margin-bottom:18px}
@media(max-width:680px){#shop .products.gb-coverflow{height:555px;width:100vw;margin-left:calc(50% - 50vw);overflow:hidden}#shop .products.gb-coverflow .product-card{width:min(270px,70vw);height:495px;top:12px}#shop .products.gb-coverflow .product-info{min-height:175px;padding:15px}.gb-carousel-arrow{width:40px;height:40px;font-size:1.55rem}.gb-carousel-arrow.prev{left:4px}.gb-carousel-arrow.next{right:4px}}
'''
style_end=s.index('</style>')
s=s[:style_end]+css+s[style_end:]

js=r'''
(function(){
 const shop=document.getElementById('shop');
 const grid=shop&&shop.querySelector('.products');
 const filterRow=shop&&shop.querySelector('.filter-row');
 if(!grid||!filterRow) return;
 grid.classList.add('gb-coverflow');
 const allCards=[...grid.querySelectorAll('.product-card')];
 let visible=[];
 let active=0;
 let startX=null;
 let dragged=false;

 const prev=document.createElement('button');
 prev.type='button';prev.className='gb-carousel-arrow prev';prev.setAttribute('aria-label','Previous product');prev.textContent='‹';
 const next=document.createElement('button');
 next.type='button';next.className='gb-carousel-arrow next';next.setAttribute('aria-label','Next product');next.textContent='›';
 grid.append(prev,next);
 const count=document.createElement('div');count.className='gb-carousel-count';grid.after(count);

 function ordered(cards){
   return cards.map((card,index)=>({card,index,cat:(card.dataset.category||'').split(/\s+/)}))
     .sort((a,b)=>{
       const rank=x=>x.cat.includes('womens')?1:x.cat.includes('mens')?2:x.cat.includes('accessories')?3:4;
       return rank(a)-rank(b)||a.index-b.index;
     }).map(x=>x.card);
 }
 function render(){
   const n=visible.length;
   if(!n){count.textContent='No products in this category';return;}
   active=((active%n)+n)%n;
   allCards.forEach(card=>{
     card.classList.remove('gb-center','gb-far');
     if(!visible.includes(card)){card.style.display='none';return;}
     card.style.display='flex';
     const i=visible.indexOf(card);
     let d=i-active;
     if(d>n/2)d-=n;if(d<-n/2)d+=n;
     const ad=Math.abs(d);
     if(ad>3){card.style.opacity='0';card.style.pointerEvents='none';card.style.transform='translateX(-50%) translateX('+(d*185)+'px) scale(.5)';card.style.zIndex='0';card.classList.add('gb-far');return;}
     const x=d*205;
     const scale=d===0?1:Math.max(.62,1-ad*.13);
     const rotate=d===0?0:(d<0?48:-48);
     card.style.transform=`translateX(-50%) translateX(${x}px) rotateY(${rotate}deg) scale(${scale})`;
     card.style.opacity=d===0?'1':String(Math.max(.28,.78-ad*.16));
     card.style.filter=d===0?'none':`brightness(${Math.max(.38,.72-ad*.08)})`;
     card.style.zIndex=String(10-ad);
     card.style.pointerEvents=ad<=2?'auto':'none';
     if(d===0)card.classList.add('gb-center');
   });
   count.textContent=(active+1)+' / '+n;
 }
 function applyFilter(filter){
   const cards=allCards.filter(card=>filter==='all'||(card.dataset.category||'').split(/\s+/).includes(filter));
   visible=filter==='all'?ordered(cards):cards;
   active=0;render();
 }
 function move(step){if(!visible.length)return;active=(active+step+visible.length)%visible.length;render();}
 prev.onclick=e=>{e.stopPropagation();move(-1)};next.onclick=e=>{e.stopPropagation();move(1)};

 grid.addEventListener('click',e=>{
   const card=e.target.closest('.product-card');
   if(!card||!visible.includes(card))return;
   const idx=visible.indexOf(card);
   if(idx!==active){e.preventDefault();e.stopPropagation();active=idx;render();}
 });
 grid.addEventListener('pointerdown',e=>{if(e.pointerType==='mouse'&&e.button!==0)return;startX=e.clientX;dragged=false;});
 grid.addEventListener('pointermove',e=>{if(startX===null)return;if(Math.abs(e.clientX-startX)>12)dragged=true;});
 grid.addEventListener('pointerup',e=>{if(startX===null)return;const dx=e.clientX-startX;startX=null;if(Math.abs(dx)>45)move(dx<0?1:-1);});
 grid.addEventListener('pointercancel',()=>{startX=null});

 // Use the site's existing filter buttons, but render matching cards in the carousel.
 filterRow.addEventListener('click',e=>{
   const btn=e.target.closest('.filter-btn');if(!btn)return;
   setTimeout(()=>applyFilter(btn.dataset.filter||'all'),0);
 });
 applyFilter((filterRow.querySelector('.filter-btn.active')||{}).dataset||'all');
})();
'''
sp=s.rfind('</script>')
if sp<0: raise SystemExit('script close not found')
s=s[:sp]+js+s[sp:]
p.write_text(s)
