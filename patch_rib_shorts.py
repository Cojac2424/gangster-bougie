from pathlib import Path
p=Path('index.html')
s=p.read_text()
if 'id="build-your-fit"' not in s:
    raise SystemExit('Build Your Fit not present')

# v5: final waist calibration. The normal boards are already close, so move the
# shared join slightly upward. Houndstooth workout shorts need their own source
# offset because that board's model/waist sits lower than the other bottom boards.
css=r'''
/* Build Your Fit — waist calibration v5 */
#build-your-fit .byf-model{--byf-split:39.65%!important}
#build-your-fit .byf-top{clip-path:inset(0 0 calc(100% - var(--byf-split)) 0)!important}
#build-your-fit .byf-bottom{clip-path:inset(var(--byf-split) 0 0 0)!important}
'''
if '/* Build Your Fit — waist calibration v5 */' not in s:
    s=s.replace('</style>',css+'\n</style>',1)
else:
    raise SystemExit('v5 already present')

# Give the exceptional Houndstooth shorts board a small independent upward
# background shift while preserving the same scale and x coordinate.
needle="const bottomUrl=`url('${bottoms[bi][1]}')`;topEl.style.backgroundImage=topUrl;bottomEl.style.setProperty('--byf-bottom-image',bottomUrl);bottomEl.style.backgroundImage=bottomUrl;"
replacement="const bottomUrl=`url('${bottoms[bi][1]}')`;const isHoundShort=bottoms[bi][0].toUpperCase().includes('HOUNDSTOOTH')&&bottoms[bi][0].toUpperCase().includes('SHORTS');topEl.style.backgroundImage=topUrl;bottomEl.style.setProperty('--byf-bottom-image',bottomUrl);bottomEl.style.backgroundImage=bottomUrl;bottomEl.style.setProperty('background-position',isHoundShort?'0 -0.85%':'0 0','important');"
if needle in s:
    s=s.replace(needle,replacement,1)
elif replacement not in s:
    raise SystemExit('render geometry marker not found')

p.write_text(s)
