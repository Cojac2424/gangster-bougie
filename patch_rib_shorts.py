from pathlib import Path
p=Path('index.html')
s=p.read_text()
if 'id="build-your-fit"' not in s:
    raise SystemExit('Build Your Fit not present')

# The source boards are four equal vertical views. At background-size 400% auto,
# the first/front panel is exactly one model-width wide and six model-widths tall
# (1024x1536 board => 256x1536 front panel). Keep BOTH selectable images on the
# same full-body 1:6 coordinate system and clip them at one shared waist seam.
css=r'''
/* Build Your Fit — shared full-body coordinate system v2 */
.byf-model{--byf-split:43%;position:relative;width:min(150px,25vw,14.5vh);height:auto;aspect-ratio:1/6;min-height:0!important;max-height:none!important;background:#ddd;overflow:hidden}
.byf-half{position:absolute!important;inset:0!important;width:100%!important;height:100%!important;background-repeat:no-repeat!important;background-size:400% 100%!important;background-position:left top!important;touch-action:pan-y;cursor:grab}
.byf-top{clip-path:inset(0 0 calc(100% - var(--byf-split)) 0);z-index:1}
.byf-bottom{clip-path:inset(var(--byf-split) 0 0 0);z-index:2;background-image:var(--byf-bottom-image)!important}
.byf-bottom::before{display:none!important;content:none!important}
.byf-seam{top:var(--byf-split)!important;height:0!important;background:transparent!important}
.byf-top .byf-arrow{top:24%!important}.byf-bottom .byf-arrow{top:70%!important}
.byf-top .byf-label{top:calc(var(--byf-split) - 44px)!important;bottom:auto!important}
.byf-bottom .byf-label{top:auto!important;bottom:12px!important}
@media(max-width:760px){#build-your-fit{padding-top:28px;padding-bottom:28px}.byf-shell{grid-template-columns:1fr;gap:16px}.byf-model{width:min(150px,36vw,14vh)}.byf-swipe-hint{margin-top:7px}}
@media(min-width:761px){.byf-model{width:min(150px,22vw,14.5vh)}}
'''
s=s.replace('</style>',css+'\n</style>',1)

# Keep the selected bottom board available to CSS while the element itself
# occupies the SAME full model rectangle as the top board.
old_direct="function render(){topEl.style.backgroundImage=`url('${tops[ti][1]}')`;bottomEl.style.backgroundImage=`url('${bottoms[bi][1]}')`;document.getElementById('byfTopLabel').textContent=tops[ti][0];document.getElementById('byfBottomLabel').textContent=bottoms[bi][0]}"
old_var="function render(){topEl.style.backgroundImage=`url('${tops[ti][1]}')`;bottomEl.style.setProperty('--byf-bottom-image',`url('${bottoms[bi][1]}')`);document.getElementById('byfTopLabel').textContent=tops[ti][0];document.getElementById('byfBottomLabel').textContent=bottoms[bi][0]}"
new="function render(){topEl.style.backgroundImage=`url('${tops[ti][1]}')`;bottomEl.style.setProperty('--byf-bottom-image',`url('${bottoms[bi][1]}')`);bottomEl.style.backgroundImage=`url('${bottoms[bi][1]}')`;document.getElementById('byfTopLabel').textContent=tops[ti][0];document.getElementById('byfBottomLabel').textContent=bottoms[bi][0]}"
if old_var in s:
    s=s.replace(old_var,new,1)
elif old_direct in s:
    s=s.replace(old_direct,new,1)
elif new not in s:
    raise SystemExit('Build Your Fit render marker not found')

p.write_text(s)
