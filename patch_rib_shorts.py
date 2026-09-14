from pathlib import Path
p=Path('index.html')
s=p.read_text()
if 'id="build-your-fit"' not in s:
    raise SystemExit('Build Your Fit not present')

# v16: the screenshots prove 38.4% is cutting through garment pixels. Move the
# actual shared clip boundary DOWN the registered full-body boards into the
# exposed abdomen. Both layers use the identical boundary; images themselves
# stay at 0 0 so the body remains registered. This is a clip change, not an
# image-position shift.
css=r'''
/* Build Your Fit — true bare-abdomen handoff v16 */
#build-your-fit .byf-model{--byf-split:42.2%!important}
#build-your-fit .byf-top{clip-path:inset(0 0 calc(100% - var(--byf-split)) 0)!important;background-position:0 0!important}
#build-your-fit .byf-bottom{clip-path:inset(var(--byf-split) 0 0 0)!important;background-image:var(--byf-bottom-image)!important;background-position:0 0!important}
@media (min-width:700px){
 #build-your-fit .byf-model{--byf-split:42.2%!important}
 #build-your-fit .byf-top{clip-path:inset(0 0 calc(100% - var(--byf-split)) 0)!important;background-position:0 0!important}
 #build-your-fit .byf-bottom{clip-path:inset(var(--byf-split) 0 0 0)!important;background-position:0 0!important}
}
'''
for marker in [
 '/* Build Your Fit — shared bare-torso splice v15 */',
 '/* Build Your Fit — centered torso splice v14 */',
 '/* Build Your Fit — centered bare-torso splice calibration v13 */',
 '/* Build Your Fit — bare-torso splice calibration v12 */',
 '/* Build Your Fit — clean midriff seam calibration v11 */',
 '/* Build Your Fit — mid-torso seam calibration v10 */']:
    if marker in s:
        start=s.index(marker)
        end=s.index('</style>',start)
        s=s[:start]+s[end:]
        break
if '/* Build Your Fit — true bare-abdomen handoff v16 */' not in s:
    s=s.replace('</style>',css+'\n</style>',1)

s=s.replace('D2DC5EB5-3654-4B80-978B-238C3C4974F0.jpeg','D2DC5FB5-3654-4B80-978B-238C3C4974F0.jpeg')

old="function render(){const topUrl=`url('${tops[ti][1]}')`;const bottomUrl=`url('${bottoms[bi][1]}')`;const modelEl=document.getElementById('byfModel');if(modelEl)modelEl.style.setProperty('--byf-split','38.4%','important');topEl.style.backgroundImage=topUrl;bottomEl.style.setProperty('--byf-bottom-image',bottomUrl);bottomEl.style.backgroundImage=bottomUrl;bottomEl.style.setProperty('background-position','0 0','important');document.getElementById('byfTopLabel').textContent=tops[ti][0];document.getElementById('byfBottomLabel').textContent=bottoms[bi][0]}"
new="function render(){const topUrl=`url('${tops[ti][1]}')`;const bottomUrl=`url('${bottoms[bi][1]}')`;const modelEl=document.getElementById('byfModel');if(modelEl)modelEl.style.setProperty('--byf-split','42.2%','important');topEl.style.setProperty('background-position','0 0','important');topEl.style.backgroundImage=topUrl;bottomEl.style.setProperty('--byf-bottom-image',bottomUrl);bottomEl.style.backgroundImage=bottomUrl;bottomEl.style.setProperty('background-position','0 0','important');document.getElementById('byfTopLabel').textContent=tops[ti][0];document.getElementById('byfBottomLabel').textContent=bottoms[bi][0]}"
if old not in s:
    raise SystemExit('Expected v15 Build Your Fit render function not found')
s=s.replace(old,new,1)
p.write_text(s)
