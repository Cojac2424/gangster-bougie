from pathlib import Path
p=Path('index.html')
s=p.read_text()
if 'id="build-your-fit"' not in s:
    raise SystemExit('Build Your Fit not present')

# Build Your Fit v8: keep the standardized boards on one shared coordinate
# system, move the join slightly lower through the exposed torso, and correct
# the Houndstooth workout-shorts filename so that bottom actually renders.
css=r'''
/* Build Your Fit — standardized 12-board compositor v8 */
#build-your-fit .byf-model{--byf-split:46.4%!important}
#build-your-fit .byf-top{clip-path:inset(0 0 calc(100% - var(--byf-split)) 0)!important}
#build-your-fit .byf-bottom{clip-path:inset(var(--byf-split) 0 0 0)!important}
'''
if '/* Build Your Fit — standardized 12-board compositor v8 */' not in s:
    s=s.replace('</style>',css+'\n</style>',1)

# The uploaded file is D2DC5FB5... (FB5), not D2DC5EB5... (EB5).
s=s.replace('D2DC5EB5-3654-4B80-978B-238C3C4974F0.jpeg','D2DC5FB5-3654-4B80-978B-238C3C4974F0.jpeg')

# Keep every bottom on the same source coordinates. No per-item Houndstooth offset.
old="bottomEl.style.setProperty('background-position',isHoundShort?'0 -2.15%':'0 0','important');"
new="bottomEl.style.setProperty('background-position','0 0','important');"
if old in s:
    s=s.replace(old,new,1)
elif new not in s:
    raise SystemExit('bottom positioning marker not found')

p.write_text(s)
