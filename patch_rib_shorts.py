from pathlib import Path
p=Path('index.html')
s=p.read_text()
if 'id="build-your-fit"' not in s:
    raise SystemExit('Build Your Fit not present')

# Override the prototype's original independent crop system. Both halves now
# share one coordinate system: identical full-board dimensions and position,
# clipped at the exact same seam. The whole assembly also scales to viewport.
css=r'''
/* Build Your Fit — continuous model alignment fix */
.byf-model{--byf-split:43%;width:min(270px,46.5vh,72vw);height:auto;aspect-ratio:1/4;max-height:none;min-height:0;background:#ddd}
.byf-half{left:0;width:100%;background-size:400% auto;background-position-x:left;background-position-y:top}
.byf-top{top:0;height:var(--byf-split)}
.byf-bottom{top:var(--byf-split);height:calc(100% - var(--byf-split));background-position-y:top}
.byf-bottom::before{content:"";position:absolute;z-index:0;left:0;top:calc(-1 * var(--byf-split) / (1 - var(--byf-split)) * 100%);width:100%;height:calc(100% / (1 - var(--byf-split)));background-image:inherit;background-repeat:no-repeat;background-size:400% auto;background-position:left top;pointer-events:none}
.byf-bottom{background-image:none!important}
.byf-bottom .byf-arrow,.byf-bottom .byf-label{z-index:6}
.byf-seam{top:var(--byf-split);background:transparent}
@media(max-width:760px){.byf-model{width:min(250px,44vh,68vw);height:auto;min-height:0;max-height:none}.byf-shell{gap:18px}.byf-swipe-hint{margin-top:8px}}
@media(min-width:761px){.byf-model{width:min(270px,47vh,32vw)}}
'''
s=s.replace('</style>',css+'\n</style>',1)

# The bottom needs the same source image on its pseudo-element. Store it in a
# CSS custom property instead of assigning a separately cropped background.
old="function render(){topEl.style.backgroundImage=`url('${tops[ti][1]}')`;bottomEl.style.backgroundImage=`url('${bottoms[bi][1]}')`;document.getElementById('byfTopLabel').textContent=tops[ti][0];document.getElementById('byfBottomLabel').textContent=bottoms[bi][0]}"
new="function render(){topEl.style.backgroundImage=`url('${tops[ti][1]}')`;bottomEl.style.setProperty('--byf-bottom-image',`url('${bottoms[bi][1]}')`);document.getElementById('byfTopLabel').textContent=tops[ti][0];document.getElementById('byfBottomLabel').textContent=bottoms[bi][0]}"
if old not in s:
    raise SystemExit('Build Your Fit render marker not found')
s=s.replace(old,new,1)
# pseudo-element cannot directly read JS background-image because bottom itself
# is deliberately blank; bind the variable here.
s=s.replace('.byf-bottom::before{content:', '.byf-bottom::before{background-image:var(--byf-bottom-image)!important;content:',1)
p.write_text(s)
