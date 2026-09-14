from pathlib import Path
p=Path('index.html')
s=p.read_text()
if 'id="build-your-fit"' not in s:
    raise SystemExit('Build Your Fit not present')

# v26: dedicated viewer-level controls. Stop moving the old arrows that live
# inside the front model. Create four controls owned by the COMPLETE two-model
# viewer, outside its white border. Preserve shared swipe, synchronization and
# LOCKED compositor geometry (42.2%, Onyx 42.8%, front 0, back 33.333333%).
css=r'''
/* Build Your Fit — dedicated outer viewer controls v26 */
#build-your-fit .byf-shell{grid-template-columns:minmax(250px,330px) minmax(0,1fr)!important;gap:28px!important;align-items:start!important}
#build-your-fit .byf-copy{min-width:0!important;padding-right:4px!important}
#build-your-fit .byf-builder{min-width:0!important;width:100%!important}
#build-your-fit .byf-model-pair{position:relative!important;display:flex!important;justify-content:center!important;align-items:flex-start!important;gap:0!important;width:max-content!important;max-width:100%!important;margin:0 auto!important;background:#efede9!important;overflow:visible!important;border-radius:16px!important;padding:0 38px!important}
#build-your-fit .byf-view{display:flex!important;flex-direction:column!important;align-items:center!important;gap:0!important;overflow:visible!important;width:auto!important}
#build-your-fit .byf-view-name{display:none!important}
#build-your-fit .byf-model-pair .byf-model{border:0!important;border-radius:0!important;overflow:visible!important;box-shadow:none!important;max-width:none!important;margin:0!important;width:clamp(150px,18vw,210px)!important}
#build-your-fit .byf-back-model .byf-half{background-position:33.333333% 0!important}
#build-your-fit .byf-back-model .byf-top,#build-your-fit .byf-back-model .byf-bottom{pointer-events:none!important}
#build-your-fit .byf-model .byf-arrow{display:none!important}
#build-your-fit .byf-outer-arrow{display:flex!important;position:absolute!important;z-index:50!important;width:44px!important;height:44px!important;align-items:center!important;justify-content:center!important;background:#111!important;color:#d9a11e!important;border:2px solid #d9a11e!important;border-radius:50%!important;font-size:1.75rem!important;line-height:1!important;padding:0!important;margin:0!important;box-shadow:0 3px 10px rgba(0,0,0,.45)!important;cursor:pointer!important;touch-action:manipulation!important}
#build-your-fit .byf-outer-arrow.left{left:-52px!important}
#build-your-fit .byf-outer-arrow.right{right:-52px!important}
#build-your-fit .byf-outer-arrow.top{top:28%!important;transform:translateY(-50%)!important}
#build-your-fit .byf-outer-arrow.bottom{top:68%!important;transform:translateY(-50%)!important}
@media(min-width:761px) and (max-width:1180px){#build-your-fit .byf-shell{grid-template-columns:minmax(220px,30%) minmax(0,70%)!important;gap:18px!important}#build-your-fit .byf-model-pair{padding:0 34px!important}#build-your-fit .byf-model-pair .byf-model{width:min(190px,18vw,22svh)!important}#build-your-fit .byf-outer-arrow.left{left:-50px!important}#build-your-fit .byf-outer-arrow.right{right:-50px!important}}
@media(max-width:760px){#build-your-fit{padding-top:20px!important;padding-bottom:20px!important}#build-your-fit .byf-shell{grid-template-columns:1fr!important;gap:12px!important}#build-your-fit .byf-model-pair{width:max-content!important;max-width:calc(100% - 100px)!important;padding:0 12px!important}#build-your-fit .byf-model-pair .byf-model,#build-your-fit .byf-model-pair .byf-view:first-child .byf-model,#build-your-fit .byf-model-pair .byf-view:last-child .byf-model{width:min(154px,34vw,14svh)!important}#build-your-fit .byf-outer-arrow{width:40px!important;height:40px!important;font-size:1.55rem!important}#build-your-fit .byf-outer-arrow.left{left:-46px!important}#build-your-fit .byf-outer-arrow.right{right:-46px!important}}
'''
for marker in ['/* Build Your Fit — responsive joined viewer + outer panel controls v25 */']:
    if marker in s:
        start=s.index(marker)
        end=s.index('</style>',start)
        s=s[:start]+s[end:]
        break
if '/* Build Your Fit — dedicated outer viewer controls v26 */' not in s:
    s=s.replace('</style>',css+'\n</style>',1)

# Remove v25 viewport-position helper if present; dedicated controls are now
# children of the complete pair and therefore naturally follow it responsively.
helper=""" function placeByfEdgeControls(){if(!pair)return;const r=pair.getBoundingClientRect();pair.style.setProperty('--byf-panel-left',r.left+'px');pair.style.setProperty('--byf-panel-right',r.right+'px');pair.style.setProperty('--byf-panel-top-control',(r.top+r.height*.28)+'px');pair.style.setProperty('--byf-panel-bottom-control',(r.top+r.height*.68)+'px')}
 placeByfEdgeControls();window.addEventListener('resize',placeByfEdgeControls,{passive:true});window.addEventListener('scroll',placeByfEdgeControls,{passive:true});"""
s=s.replace(helper,'')

# Add four actual viewer-level buttons once. They call the same move() function,
# so top controls update front+back tops and bottom controls update both bottoms.
needle="const pair=document.querySelector('#build-your-fit .byf-model-pair');"
add="""const pair=document.querySelector('#build-your-fit .byf-model-pair');
 if(pair&&!pair.querySelector('.byf-outer-arrow')){
  [['top','left','‹',-1],['top','right','›',1],['bottom','left','‹',-1],['bottom','right','›',1]].forEach(([which,side,glyph,dir])=>{const b=document.createElement('button');b.type='button';b.className=`byf-outer-arrow ${which} ${side}`;b.textContent=glyph;b.setAttribute('aria-label',`${dir<0?'Previous':'Next'} ${which==='top'?'sports bra':'bottom'}`);b.addEventListener('click',e=>{e.preventDefault();e.stopPropagation();move(which,dir)});pair.appendChild(b)})
 }"""
if needle in s and "pair.querySelector('.byf-outer-arrow')" not in s:
    s=s.replace(needle,add,1)

p.write_text(s)
