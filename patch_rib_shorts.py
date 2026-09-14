from pathlib import Path
p=Path('index.html')
s=p.read_text()
if 'id="build-your-fit"' in s:
    raise SystemExit('Build Your Fit already present')

css=r'''
/* Build Your Fit — Signature prototype */
#build-your-fit{background:#080808;border-top:1px solid var(--border);border-bottom:1px solid var(--border)}
.byf-shell{display:grid;grid-template-columns:minmax(280px,.8fr) minmax(320px,1.2fr);gap:54px;align-items:center}
.byf-copy h2{font-family:'Bodoni Moda',serif;font-size:clamp(2.4rem,5vw,4.3rem);line-height:.95;text-transform:uppercase;margin-bottom:16px}.byf-copy p{color:#bbb;max-width:520px}.byf-note{margin-top:18px;color:var(--gold-light)!important;font-size:.82rem;text-transform:uppercase;letter-spacing:.12em;font-weight:800}
.byf-builder{display:flex;justify-content:center}.byf-model{position:relative;width:min(270px,72vw);height:min(1080px,288vw);max-height:78vh;min-height:650px;background:#ddd;border:1px solid var(--gold);overflow:hidden;box-shadow:0 18px 50px rgba(0,0,0,.45)}
.byf-half{position:absolute;left:0;width:100%;overflow:hidden;background-repeat:no-repeat;background-size:400% auto;background-position-x:left;touch-action:pan-y;cursor:grab}.byf-half:active{cursor:grabbing}.byf-top{top:0;height:43%;background-position-y:9%}.byf-bottom{top:43%;height:57%;background-position-y:72%}.byf-seam{position:absolute;left:0;right:0;top:43%;height:1px;background:rgba(216,169,40,.65);z-index:4;pointer-events:none}
.byf-arrow{position:absolute;z-index:6;width:42px;height:42px;border-radius:50%;border:1px solid var(--gold);background:rgba(5,5,5,.88);color:var(--gold-light);display:grid;place-items:center;font-size:1.55rem;cursor:pointer}.byf-top .byf-arrow{top:52%}.byf-bottom .byf-arrow{top:38%}.byf-arrow.prev{left:8px}.byf-arrow.next{right:8px}.byf-label{position:absolute;z-index:6;left:50%;transform:translateX(-50%);background:rgba(5,5,5,.88);border:1px solid rgba(216,169,40,.55);color:#fff;padding:7px 12px;white-space:nowrap;font-size:.68rem;font-weight:900;text-transform:uppercase;letter-spacing:.08em}.byf-top .byf-label{bottom:10px}.byf-bottom .byf-label{bottom:12px}.byf-swipe-hint{text-align:center;color:#888;font-size:.72rem;margin-top:12px;letter-spacing:.08em;text-transform:uppercase}
@media(max-width:760px){.byf-shell{grid-template-columns:1fr;gap:28px}.byf-copy{text-align:center}.byf-copy p{margin-left:auto;margin-right:auto}.byf-model{width:min(230px,62vw);min-height:720px;max-height:none;height:920px}}
'''
s=s.replace('</style>',css+'\n</style>',1)

section=r'''
<section id="build-your-fit"><div class="container"><div class="byf-shell"><div class="byf-copy"><div class="eyebrow">GB Signature</div><h2>Build Your Fit</h2><p>Create your own Signature combination. Swipe the top half to change the sports bra. Swipe the bottom half independently to switch between leggings and workout shorts across Onyx, Cream, Oxblood, Heritage Plaid, Vault and Bougie Houndstooth.</p><p class="byf-note">Prototype — mix the fit your way.</p></div><div class="byf-builder"><div><div class="byf-model" id="byfModel"><div class="byf-half byf-top" id="byfTop"><button class="byf-arrow prev" type="button" aria-label="Previous top">‹</button><button class="byf-arrow next" type="button" aria-label="Next top">›</button><span class="byf-label" id="byfTopLabel">Onyx Sports Bra</span></div><div class="byf-half byf-bottom" id="byfBottom"><button class="byf-arrow prev" type="button" aria-label="Previous bottom">‹</button><button class="byf-arrow next" type="button" aria-label="Next bottom">›</button><span class="byf-label" id="byfBottomLabel">Onyx Leggings</span></div><div class="byf-seam"></div></div><div class="byf-swipe-hint">Swipe top and bottom independently</div></div></div></div></div></section>
'''
needle='<section id="shop">'
if needle not in s: raise SystemExit('Shop marker not found')
s=s.replace(needle,section+needle,1)

js=r'''

// GB Signature Build Your Fit prototype
(function(){
 const topEl=document.getElementById('byfTop'), bottomEl=document.getElementById('byfBottom');
 if(!topEl||!bottomEl) return;
 const tops=[
  ['Onyx Sports Bra','AB4D5CF7-F989-484D-8D0C-CB45C5C978F1.jpeg'],
  ['Cream Sports Bra','5B84C627-F0D4-483B-A7BB-8F162A2C86B8.jpeg'],
  ['Oxblood Sports Bra','9BDD8A40-2E5B-4FEC-9F3B-1230228AE272.jpeg'],
  ['Heritage Plaid Sports Bra','4AC0E501-7790-4599-95A0-A3C03ACF75FF.jpeg'],
  ['Vault Sports Bra','E7B6B7E4-0AE0-4B06-934F-B86D40991E04.jpeg'],
  ['Bougie Houndstooth Sports Bra','DB0194B3-AF6E-4964-B2F9-266330DB0A6D.jpeg']
 ];
 const bottoms=[
  ['Onyx Leggings','AB4D5CF7-F989-484D-8D0C-CB45C5C978F1.jpeg'],['Onyx Workout Shorts','EF619902-FCBF-4544-A37C-5E2D9524430A.jpeg'],
  ['Cream Leggings','5B84C627-F0D4-483B-A7BB-8F162A2C86B8.jpeg'],['Cream Workout Shorts','7DD0F31D-E8CE-4095-8275-9510E30100C2.jpeg'],
  ['Oxblood Leggings','9BDD8A40-2E5B-4FEC-9F3B-1230228AE272.jpeg'],['Oxblood Workout Shorts','E65C197F-ACC4-425B-A093-DE5434320D6E.jpeg'],
  ['Heritage Plaid Leggings','4AC0E501-7790-4599-95A0-A3C03ACF75FF.jpeg'],['Heritage Plaid Workout Shorts','75EA90E3-7637-406D-BB67-1D52B365AA54.jpeg'],
  ['Vault Leggings','E7B6B7E4-0AE0-4B06-934F-B86D40991E04.jpeg'],['Vault Workout Shorts','6475C168-80DB-4112-A004-708F8A4EECCA.jpeg'],
  ['Bougie Houndstooth Leggings','DB0194B3-AF6E-4964-B2F9-266330DB0A6D.jpeg'],['Bougie Houndstooth Workout Shorts','794DD1D2-8663-4830-9612-93E0EC9E5B03.jpeg']
 ];
 let ti=0,bi=0;
 function render(){topEl.style.backgroundImage=`url('${tops[ti][1]}')`;bottomEl.style.backgroundImage=`url('${bottoms[bi][1]}')`;document.getElementById('byfTopLabel').textContent=tops[ti][0];document.getElementById('byfBottomLabel').textContent=bottoms[bi][0]}
 function move(which,dir){if(which==='top')ti=(ti+dir+tops.length)%tops.length;else bi=(bi+dir+bottoms.length)%bottoms.length;render()}
 topEl.querySelector('.prev').onclick=()=>move('top',-1);topEl.querySelector('.next').onclick=()=>move('top',1);bottomEl.querySelector('.prev').onclick=()=>move('bottom',-1);bottomEl.querySelector('.next').onclick=()=>move('bottom',1);
 function swipe(el,which){let x=null,y=null;el.addEventListener('pointerdown',e=>{if(e.pointerType==='mouse')return;x=e.clientX;y=e.clientY});el.addEventListener('pointerup',e=>{if(x===null)return;const dx=e.clientX-x,dy=e.clientY-y;x=y=null;if(Math.abs(dx)>=45&&Math.abs(dx)>Math.abs(dy))move(which,dx<0?1:-1)});el.addEventListener('pointercancel',()=>{x=y=null})}
 swipe(topEl,'top');swipe(bottomEl,'bottom');render();
})();
'''
marker='</script>\n</body></html>'
if marker not in s: raise SystemExit('Closing script marker not found')
s=s.replace(marker,js+marker,1)
p.write_text(s)
