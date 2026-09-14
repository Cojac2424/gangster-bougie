from pathlib import Path
p=Path('index.html')
s=p.read_text()
if 'id="build-your-fit"' not in s:
    raise SystemExit('Build Your Fit not present')

# v6: preserve the current full-body sizing, but let the selected bottom begin
# higher in the torso so the join is made through matching skin rather than at
# the waistband. Houndstooth workout shorts require a larger upward correction.
css=r'''
/* Build Your Fit — torso overlap calibration v6 */
#build-your-fit .byf-model{--byf-split:38.85%!important}
#build-your-fit .byf-top{clip-path:inset(0 0 calc(100% - var(--byf-split)) 0)!important}
#build-your-fit .byf-bottom{clip-path:inset(var(--byf-split) 0 0 0)!important}
'''
if '/* Build Your Fit — torso overlap calibration v6 */' not in s:
    s=s.replace('</style>',css+'\n</style>',1)
else:
    raise SystemExit('v6 already present')

# v5 already introduced the per-item Houndstooth correction. Increase it enough
# to expose the skin/torso above that shorts waistband, while leaving other
# bottoms on the shared coordinate system.
old="bottomEl.style.setProperty('background-position',isHoundShort?'0 -0.85%':'0 0','important');"
new="bottomEl.style.setProperty('background-position',isHoundShort?'0 -2.15%':'0 0','important');"
if old in s:
    s=s.replace(old,new,1)
elif new not in s:
    raise SystemExit('Houndstooth offset marker not found')

p.write_text(s)
