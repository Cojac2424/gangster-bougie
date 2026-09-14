from pathlib import Path
p=Path('index.html')
s=p.read_text()
if 'id="build-your-fit"' not in s:
    raise SystemExit('Build Your Fit not present')

# v17: keep the proven 42.2% splice for every bottom except the two Onyx
# bottoms. Their source boards leave a tiny sports-bra sliver at 42.2%, so only
# those two get a fractionally lower-on-body clip at 42.8%. No image is shifted.
css=r'''
/* Build Your Fit — bare-abdomen handoff with Onyx-only trim v17 */
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
 '/* Build Your Fit — true bare-abdomen handoff v16 */',
 '/* Build Your Fit — shared bare-torso splice v15 */']:
    if marker in s:
        start=s.index(marker)
        end=s.index('</style>',start)
        s=s[:start]+s[end:]
        break
if '/* Build Your Fit — bare-abdomen handoff with Onyx-only trim v17 */' not in s:
    s=s.replace('</style>',css+'\n</style>',1)

s=s.replace('D2DC5EB5-3654-4B80-978B-238C3C4974F0.jpeg','D2DC5FB5-3654-4B80-978B-238C3C4974F0.jpeg')

old="function render(){const topUrl=`url('${tops[ti][1]}')`;const bottomUrl=`url('${bottoms[bi][1]}')`;const modelEl=document.getElementById('byfModel');if(modelEl)modelEl.style.setProperty('--byf-split','42.2%','important');topEl.style.setProperty('background-position','0 0','important');topEl.style.backgroundImage=topUrl;bottomEl.style.setProperty('--byf-bottom-image',bottomUrl);bottomEl.style.backgroundImage=bottomUrl;bottomEl.style.setProperty('background-position','0 0','important');document.getElementById('byfTopLabel').textContent=tops[ti][0];document.getElementById('byfBottomLabel').textContent=bottoms[bi][0]}"
new="function render(){const topUrl=`url('${tops[ti][1]}')`;const bottomUrl=`url('${bottoms[bi][1]}')`;const bottomName=bottoms[bi][0];const isOnyxBottom=bottomName==='Onyx Leggings'||bottomName==='Onyx Workout Shorts';const split=isOnyxBottom?'42.8%':'42.2%';const modelEl=document.getElementById('byfModel');if(modelEl)modelEl.style.setProperty('--byf-split',split,'important');topEl.style.setProperty('background-position','0 0','important');topEl.style.backgroundImage=topUrl;bottomEl.style.setProperty('--byf-bottom-image',bottomUrl);bottomEl.style.backgroundImage=bottomUrl;bottomEl.style.setProperty('background-position','0 0','important');document.getElementById('byfTopLabel').textContent=tops[ti][0];document.getElementById('byfBottomLabel').textContent=bottomName}"
if old not in s:
    raise SystemExit('Expected v16 Build Your Fit render function not found')
s=s.replace(old,new,1)
p.write_text(s)
