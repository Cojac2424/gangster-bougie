from pathlib import Path
p=Path('index.html')
s=p.read_text()
if 'id="build-your-fit"' not in s:
    raise SystemExit('Build Your Fit not present')

# v23: responsive presentation + shared two-model swipe zones.
# LOCKED compositor geometry remains untouched: 42.2%, Onyx 42.8%, front 0,
# back second quarter 33.333333%. Front/back model dimensions remain equal.
css=r'''
/* Build Your Fit — responsive joined viewer + shared controls v23 */
#build-your-fit .byf-shell{grid-template-columns:minmax(250px,330px) minmax(0,1fr)!important;gap:28px!important;align-items:start!important}
#build-your-fit .byf-copy{min-width:0!important;padding-right:4px!important}
#build-your-fit .byf-builder{min-width:0!important;width:100%!important}
#build-your-fit .byf-model-pair{position:relative!important;display:flex!important;justify-content:center!important;align-items:flex-start!important;gap:0!important;width:max-content!important;max-width:100%!important;margin:0 auto!important;background:#efede9!important;overflow:hidden!important;border-radius:16px!important;padding:0 38px!important}
#build-your-fit .byf-view{display:flex!important;flex-direction:column!important;align-items:center!important;gap:0!important;overflow:visible!important;width:auto!important}
#build-your-fit .byf-view-name{display:none!important}
#build-your-fit .byf-model-pair .byf-model{border:0!important;border-radius:0!important;overflow:visible!important;box-shadow:none!important;max-width:none!important;margin:0!important;width:clamp(150px,18vw,210px)!important}
#build-your-fit .byf-back-model .byf-half{background-position:33.333333% 0!important}
#build-your-fit .byf-back-model .byf-top,#build-your-fit .byf-back-model .byf-bottom{pointer-events:none!important}
#build-your-fit .byf-back-model .byf-arrow,#build-your-fit .byf-back-model .byf-label{display:none!important}
#build-your-fit .byf-model-pair #byfModel .byf-arrow{position:fixed!important;z-index:12!important}
#build-your-fit .byf-model-pair #byfTop .byf-arrow.prev,#build-your-fit .byf-model-pair #byfBottom .byf-arrow.prev{left:max(10px,calc(50vw - min(360px,46vw)))!important;right:auto!important}
#build-your-fit .byf-model-pair #byfTop .byf-arrow.next,#build-your-fit .byf-model-pair #byfBottom .byf-arrow.next{right:max(10px,calc(50vw - min(360px,46vw)))!important;left:auto!important}
#build-your-fit .byf-model-pair #byfTop .byf-arrow.prev,#build-your-fit .byf-model-pair #byfTop .byf-arrow.next{top:42%!important}
#build-your-fit .byf-model-pair #byfBottom .byf-arrow.prev,#build-your-fit .byf-model-pair #byfBottom .byf-arrow.next{top:66%!important}
@media(min-width:761px) and (max-width:1180px){#build-your-fit .byf-shell{grid-template-columns:minmax(220px,30%) minmax(0,70%)!important;gap:18px!important}#build-your-fit .byf-model-pair{padding:0 34px!important}#build-your-fit .byf-model-pair .byf-model{width:min(190px,18vw,22svh)!important}}
@media(max-width:760px){#build-your-fit{padding-top:20px!important;padding-bottom:20px!important}#build-your-fit .byf-shell{grid-template-columns:1fr!important;gap:12px!important}#build-your-fit .byf-model-pair{width:max-content!important;max-width:100%!important;padding:0 12px!important}#build-your-fit .byf-model-pair .byf-model,#build-your-fit .byf-model-pair .byf-view:first-child .byf-model,#build-your-fit .byf-model-pair .byf-view:last-child .byf-model{width:min(154px,42vw,14svh)!important}#build-your-fit .byf-model-pair #byfTop .byf-arrow.prev,#build-your-fit .byf-model-pair #byfBottom .byf-arrow.prev{left:8px!important}#build-your-fit .byf-model-pair #byfTop .byf-arrow.next,#build-your-fit .byf-model-pair #byfBottom .byf-arrow.next{right:8px!important}}
'''
for marker in ['/* Build Your Fit — synchronized equal-scale restore v22 */']:
    if marker in s:
        start=s.index(marker)
        end=s.index('</style>',start)
        s=s[:start]+s[end:]
        break
if '/* Build Your Fit — responsive joined viewer + shared controls v23 */' not in s:
    s=s.replace('</style>',css+'\n</style>',1)

# Replace front-only swipe listeners with two shared horizontal gesture zones
# spanning BOTH front and back. Existing arrow handlers still call the same move().
old="swipe(topEl,'top');swipe(bottomEl,'bottom');render();"
new="""const pair=document.querySelector('#build-your-fit .byf-model-pair');
 if(pair){let sx=null,sy=null,which=null;pair.style.touchAction='pan-y';pair.addEventListener('pointerdown',e=>{if(e.pointerType==='mouse')return;const r=pair.getBoundingClientRect();sx=e.clientX;sy=e.clientY;which=((e.clientY-r.top)/r.height)<0.5?'top':'bottom'});pair.addEventListener('pointerup',e=>{if(sx===null)return;const dx=e.clientX-sx,dy=e.clientY-sy,w=which;sx=sy=which=null;if(Math.abs(dx)>=45&&Math.abs(dx)>Math.abs(dy))move(w,dx<0?1:-1)});pair.addEventListener('pointercancel',()=>{sx=sy=which=null})}
 render();"""
if old in s:
    s=s.replace(old,new,1)
elif new not in s:
    raise SystemExit('Expected Build Your Fit swipe hook not found')

p.write_text(s)
