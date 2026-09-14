from pathlib import Path
p=Path('index.html')
s=p.read_text()
if 'id="build-your-fit"' not in s:
    raise SystemExit('Build Your Fit not present')

# v14: keep the good shared torso seam, but give only the two Onyx bottoms a
# slightly lower handoff so their higher waist does not intrude into the bra.
css=r'''
/* Build Your Fit — centered torso splice v14 */
#build-your-fit .byf-model{--byf-split:38.4%!important}
#build-your-fit .byf-top{clip-path:inset(0 0 calc(100% - var(--byf-split)) 0)!important}
#build-your-fit .byf-bottom{clip-path:inset(var(--byf-split) 0 0 0)!important;background-image:var(--byf-bottom-image)!important;background-position:0 0!important}
@media (min-width:700px){#build-your-fit .byf-model{--byf-split:38.4%!important}}
'''
# Remove any prior calibration block we added; otherwise append after legacy rules.
for marker in [
 '/* Build Your Fit — centered bare-torso splice calibration v13 */',
 '/* Build Your Fit — bare-torso splice calibration v12 */',
 '/* Build Your Fit — clean midriff seam calibration v11 */',
 '/* Build Your Fit — mid-torso seam calibration v10 */']:
    if marker in s:
        start=s.index(marker)
        end=s.index('</style>',start)
        # prior generated calibration is the final block before </style>
        s=s[:start]+s[end:]
        break
if '/* Build Your Fit — centered torso splice v14 */' not in s:
    s=s.replace('</style>',css+'\n</style>',1)

# Correct Houndstooth asset spelling if an old reference remains.
s=s.replace('D2DC5EB5-3654-4B80-978B-238C3C4974F0.jpeg','D2DC5FB5-3654-4B80-978B-238C3C4974F0.jpeg')

# Per-bottom seam: only Onyx leggings/shorts get the lower handoff.
old="function render(){const topUrl=`url('${tops[ti][1]}')`;const bottomUrl=`url('${bottoms[bi][1]}')`;const isHoundShort=bottoms[bi][0].toUpperCase().includes('HOUNDSTOOTH')&&bottoms[bi][0].toUpperCase().includes('SHORTS');topEl.style.backgroundImage=topUrl;bottomEl.style.setProperty('--byf-bottom-image',bottomUrl);bottomEl.style.backgroundImage=bottomUrl;bottomEl.style.setProperty('background-position','0 0','important');document.getElementById('byfTopLabel').textContent=tops[ti][0];document.getElementById('byfBottomLabel').textContent=bottoms[bi][0]}"
new="function render(){const topUrl=`url('${tops[ti][1]}')`;const bottomUrl=`url('${bottoms[bi][1]}')`;const isOnyxBottom=bottoms[bi][0]==='Onyx Leggings'||bottoms[bi][0]==='Onyx Workout Shorts';const modelEl=document.getElementById('byfModel');if(modelEl)modelEl.style.setProperty('--byf-split',isOnyxBottom?'39.2%':'38.4%','important');topEl.style.backgroundImage=topUrl;bottomEl.style.setProperty('--byf-bottom-image',bottomUrl);bottomEl.style.backgroundImage=bottomUrl;bottomEl.style.setProperty('background-position','0 0','important');document.getElementById('byfTopLabel').textContent=tops[ti][0];document.getElementById('byfBottomLabel').textContent=bottoms[bi][0]}"
if old not in s:
    raise SystemExit('Expected Build Your Fit render function not found')
s=s.replace(old,new,1)
p.write_text(s)
