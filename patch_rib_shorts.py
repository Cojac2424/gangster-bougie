from pathlib import Path
p=Path('index.html')
s=p.read_text()
if 'id="build-your-fit"' not in s:
    raise SystemExit('Build Your Fit not present')

# v18: preserve the proven front compositor exactly and add a synchronized
# back-view compositor beside it. Each standardized source board contains
# front/back/left/right views; front is quarter 1 and back is quarter 2.
css=r'''
/* Build Your Fit — synchronized front + back v18 */
#build-your-fit .byf-builder>div{width:100%}
#build-your-fit .byf-model-pair{display:flex;justify-content:center;align-items:flex-start;gap:12px}
#build-your-fit .byf-view{display:flex;flex-direction:column;align-items:center;gap:5px}
#build-your-fit .byf-view-name{color:#8f8f8f;font-size:.56rem;letter-spacing:.12em;text-transform:uppercase;font-weight:800}
#build-your-fit .byf-back-model .byf-half{background-position:33.333333% 0!important}
#build-your-fit .byf-back-model .byf-top,#build-your-fit .byf-back-model .byf-bottom{pointer-events:none!important}
#build-your-fit .byf-back-model .byf-arrow,#build-your-fit .byf-back-model .byf-label{display:none!important}
@media(max-width:760px){#build-your-fit .byf-model-pair{gap:8px}#build-your-fit .byf-model-pair .byf-model{width:min(145px,35vw,13.2svh)!important}}
'''
if '/* Build Your Fit — synchronized front + back v18 */' not in s:
    s=s.replace('</style>',css+'\n</style>',1)

old_html='<div class="byf-builder"><div><div class="byf-model" id="byfModel"><div class="byf-half byf-top" id="byfTop"><button class="byf-arrow prev" type="button" aria-label="Previous top">‹</button><button class="byf-arrow next" type="button" aria-label="Next top">›</button><span class="byf-label" id="byfTopLabel">Onyx Sports Bra</span></div><div class="byf-half byf-bottom" id="byfBottom"><button class="byf-arrow prev" type="button" aria-label="Previous bottom">‹</button><button class="byf-arrow next" type="button" aria-label="Next bottom">›</button><span class="byf-label" id="byfBottomLabel">Onyx Leggings</span></div><div class="byf-seam"></div></div><div class="byf-swipe-hint">Swipe top and bottom independently</div></div></div>'
new_html='<div class="byf-builder"><div><div class="byf-model-pair"><div class="byf-view"><div class="byf-view-name">Front</div><div class="byf-model" id="byfModel"><div class="byf-half byf-top" id="byfTop"><button class="byf-arrow prev" type="button" aria-label="Previous top">‹</button><button class="byf-arrow next" type="button" aria-label="Next top">›</button><span class="byf-label" id="byfTopLabel">Onyx Sports Bra</span></div><div class="byf-half byf-bottom" id="byfBottom"><button class="byf-arrow prev" type="button" aria-label="Previous bottom">‹</button><button class="byf-arrow next" type="button" aria-label="Next bottom">›</button><span class="byf-label" id="byfBottomLabel">Onyx Leggings</span></div><div class="byf-seam"></div></div></div><div class="byf-view"><div class="byf-view-name">Back</div><div class="byf-model byf-back-model" id="byfBackModel"><div class="byf-half byf-top" id="byfBackTop"></div><div class="byf-half byf-bottom" id="byfBackBottom"></div><div class="byf-seam"></div></div></div></div><div class="byf-swipe-hint">Swipe top and bottom independently — front &amp; back change together</div></div></div>'
if old_html not in s:
    raise SystemExit('Expected current Build Your Fit HTML not found')
s=s.replace(old_html,new_html,1)

old_render="function render(){const topUrl=`url('${tops[ti][1]}')`;const bottomUrl=`url('${bottoms[bi][1]}')`;const bottomName=bottoms[bi][0];const isOnyxBottom=bottomName==='Onyx Leggings'||bottomName==='Onyx Workout Shorts';const split=isOnyxBottom?'42.8%':'42.2%';const modelEl=document.getElementById('byfModel');if(modelEl)modelEl.style.setProperty('--byf-split',split,'important');topEl.style.setProperty('background-position','0 0','important');topEl.style.backgroundImage=topUrl;bottomEl.style.setProperty('--byf-bottom-image',bottomUrl);bottomEl.style.backgroundImage=bottomUrl;bottomEl.style.setProperty('background-position','0 0','important');document.getElementById('byfTopLabel').textContent=tops[ti][0];document.getElementById('byfBottomLabel').textContent=bottomName}"
new_render="function render(){const topUrl=`url('${tops[ti][1]}')`;const bottomUrl=`url('${bottoms[bi][1]}')`;const bottomName=bottoms[bi][0];const isOnyxBottom=bottomName==='Onyx Leggings'||bottomName==='Onyx Workout Shorts';const split=isOnyxBottom?'42.8%':'42.2%';const modelEl=document.getElementById('byfModel');if(modelEl)modelEl.style.setProperty('--byf-split',split,'important');topEl.style.setProperty('background-position','0 0','important');topEl.style.backgroundImage=topUrl;bottomEl.style.setProperty('--byf-bottom-image',bottomUrl);bottomEl.style.backgroundImage=bottomUrl;bottomEl.style.setProperty('background-position','0 0','important');const backModel=document.getElementById('byfBackModel'),backTop=document.getElementById('byfBackTop'),backBottom=document.getElementById('byfBackBottom');if(backModel)backModel.style.setProperty('--byf-split',split,'important');if(backTop){backTop.style.backgroundImage=topUrl;backTop.style.setProperty('background-position','33.333333% 0','important')}if(backBottom){backBottom.style.setProperty('--byf-bottom-image',bottomUrl);backBottom.style.backgroundImage=bottomUrl;backBottom.style.setProperty('background-position','33.333333% 0','important')}document.getElementById('byfTopLabel').textContent=tops[ti][0];document.getElementById('byfBottomLabel').textContent=bottomName}"
if old_render not in s:
    raise SystemExit('Expected v17 Build Your Fit render function not found')
s=s.replace(old_render,new_render,1)
p.write_text(s)
