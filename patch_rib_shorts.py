from pathlib import Path
p=Path('index.html')
s=p.read_text()
if 'id="build-your-fit"' not in s: raise SystemExit('Build Your Fit not present')

# v27: shopping layer ONLY. Preserve v26 viewer, arrows, swipes and locked splice geometry.
css=r'''
/* Build Your Fit — View This Fit shopping layer v27 */
#build-your-fit .byf-fit-shop{width:min(620px,100%);margin:18px auto 0;text-align:center}
#build-your-fit .byf-view-fit{border:1px solid #d9a11e;background:#111;color:#f4d06f;border-radius:999px;padding:13px 28px;font-weight:800;letter-spacing:.08em;text-transform:uppercase;cursor:pointer}
#build-your-fit .byf-fit-panel{display:none;margin-top:14px;background:#0d0d0d;border:1px solid rgba(217,161,30,.7);border-radius:16px;padding:18px;color:#fff;text-align:left;box-shadow:0 12px 32px rgba(0,0,0,.35)}
#build-your-fit .byf-fit-panel.open{display:block}
#build-your-fit .byf-fit-title{text-align:center;color:#f4d06f;font-family:Georgia,serif;letter-spacing:.08em;margin:0 0 4px}
#build-your-fit .byf-fit-tag{text-align:center;color:#bbb;margin:0 0 16px}
#build-your-fit .byf-fit-item{border-top:1px solid rgba(217,161,30,.35);padding:14px 0}.byf-fit-item:first-of-type{border-top:0}
#build-your-fit .byf-fit-name{font-weight:800;font-size:1.02rem}#build-your-fit .byf-fit-price{color:#f4d06f;font-weight:800;margin:4px 0 9px}
#build-your-fit .byf-size-label{font-size:.82rem;color:#bbb;margin-bottom:7px}
#build-your-fit .byf-sizes{display:flex;gap:7px;flex-wrap:wrap}
#build-your-fit .byf-size{min-width:42px;padding:8px 9px;border-radius:8px;border:1px solid #666;background:#191919;color:#fff;cursor:pointer}
#build-your-fit .byf-size.active{border-color:#d9a11e;color:#f4d06f;box-shadow:0 0 0 1px #d9a11e inset}
#build-your-fit .byf-fit-actions{display:flex;gap:10px;margin-top:15px;flex-wrap:wrap}
#build-your-fit .byf-fit-actions button{flex:1 1 180px;padding:12px;border-radius:10px;font-weight:800;cursor:pointer}
#build-your-fit .byf-add-fit{background:#d9a11e;color:#080808;border:1px solid #d9a11e}.byf-view-products{background:#151515;color:#f4d06f;border:1px solid #d9a11e}
#build-your-fit .byf-fit-note{font-size:.8rem;color:#aaa;margin:10px 0 0;text-align:center}
@media(max-width:760px){#build-your-fit .byf-fit-shop{margin-top:14px}#build-your-fit .byf-fit-panel{padding:14px}}
'''
if '/* Build Your Fit — View This Fit shopping layer v27 */' not in s:
    s=s.replace('</style>',css+'\n</style>',1)

# Add shopping host immediately after the existing swipe hint, without touching viewer markup.
host='''<div class="byf-fit-shop" id="byfFitShop"><button type="button" class="byf-view-fit" id="byfViewFit">View This Fit</button><div class="byf-fit-panel" id="byfFitPanel" aria-hidden="true"><h3 class="byf-fit-title">YOUR SIGNATURE FIT</h3><p class="byf-fit-tag">You built it. Now make it yours.</p><div class="byf-fit-item"><div class="byf-fit-name" id="byfShopTopName"></div><div class="byf-fit-price">US$39.99</div><div class="byf-size-label">Choose top size</div><div class="byf-sizes" id="byfTopSizes"></div></div><div class="byf-fit-item"><div class="byf-fit-name" id="byfShopBottomName"></div><div class="byf-fit-price" id="byfShopBottomPrice"></div><div class="byf-size-label">Choose bottom size</div><div class="byf-sizes" id="byfBottomSizes"></div></div><div class="byf-fit-actions"><button type="button" class="byf-view-products" id="byfViewProducts">View Items</button><button type="button" class="byf-add-fit" id="byfAddFit">Add Both to Cart</button></div><p class="byf-fit-note" id="byfFitNote">Choose a size for each piece.</p></div></div>'''
needle='<div class="byf-swipe-hint">Swipe top and bottom independently — front &amp; back change together</div>'
if 'id="byfFitShop"' not in s:
    if needle not in s: raise SystemExit('swipe hint host not found')
    s=s.replace(needle,needle+host,1)

# Extend the existing render() with shop labels/prices. Do not alter compositor values.
old="document.getElementById('byfTopLabel').textContent=tops[ti][0];document.getElementById('byfBottomLabel').textContent=bottomName}"
new="document.getElementById('byfTopLabel').textContent=tops[ti][0];document.getElementById('byfBottomLabel').textContent=bottomName;const st=document.getElementById('byfShopTopName'),sb=document.getElementById('byfShopBottomName'),sp=document.getElementById('byfShopBottomPrice');if(st)st.textContent=tops[ti][0];if(sb)sb.textContent=bottomName;if(sp)sp.textContent=bottomName.includes('Workout Shorts')?'US$54.99':'US$69.99'}"
if old in s and new not in s: s=s.replace(old,new,1)

# Shopping behavior: independent sizes, dynamic current selection, and a local cart handoff.
anchor="if(pair){let sx=null,sy=null,which=null;"
shopjs="""const fitPanel=document.getElementById('byfFitPanel'),viewFit=document.getElementById('byfViewFit'),topSizes=document.getElementById('byfTopSizes'),bottomSizes=document.getElementById('byfBottomSizes'),fitNote=document.getElementById('byfFitNote');
 let fitTopSize='',fitBottomSize='';
 function makeSizes(el,sizes,kind){if(!el)return;el.innerHTML='';sizes.forEach(sz=>{const b=document.createElement('button');b.type='button';b.className='byf-size';b.textContent=sz;b.onclick=()=>{el.querySelectorAll('.byf-size').forEach(x=>x.classList.remove('active'));b.classList.add('active');if(kind==='top')fitTopSize=sz;else fitBottomSize=sz;if(fitNote)fitNote.textContent='Your top and bottom can be different sizes.'};el.appendChild(b)})}
 makeSizes(topSizes,['S','M','L','XL','2XL'],'top');makeSizes(bottomSizes,['XS','S','M','L','XL','2XL'],'bottom');
 if(viewFit)viewFit.onclick=()=>{fitPanel.classList.toggle('open');fitPanel.setAttribute('aria-hidden',fitPanel.classList.contains('open')?'false':'true');render()};
 const viewProducts=document.getElementById('byfViewProducts');if(viewProducts)viewProducts.onclick=()=>{document.getElementById('shop')?.scrollIntoView({behavior:'smooth',block:'start'})};
 const addFit=document.getElementById('byfAddFit');if(addFit)addFit.onclick=()=>{if(!fitTopSize||!fitBottomSize){if(fitNote)fitNote.textContent='Please choose a top size and a bottom size first.';return}const bottomName=bottoms[bi][0],items=[{name:tops[ti][0],size:fitTopSize,price:39.99},{name:bottomName,size:fitBottomSize,price:bottomName.includes('Workout Shorts')?54.99:69.99}];const cart=JSON.parse(localStorage.getItem('gbCart')||'[]');cart.push(...items);localStorage.setItem('gbCart',JSON.stringify(cart));if(fitNote)fitNote.textContent=`Added ${tops[ti][0]} (${fitTopSize}) + ${bottomName} (${fitBottomSize}) to your cart.`};
 """
if anchor in s and 'const fitPanel=document.getElementById' not in s: s=s.replace(anchor,shopjs+anchor,1)

p.write_text(s)
