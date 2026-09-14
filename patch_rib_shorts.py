from pathlib import Path
p=Path('index.html')
s=p.read_text()
if 'id="build-your-fit"' not in s:
    raise SystemExit('Build Your Fit not present')

# Standardized 1024-wide boards: all twelve now share the same outer canvas,
# front-view panel, model scale and vertical registration. Use one shared seam
# through the exposed torso and remove all per-item positioning corrections.
css=r'''
/* Build Your Fit — standardized 12-board compositor v7 */
#build-your-fit .byf-model{--byf-split:45.8%!important}
#build-your-fit .byf-top{clip-path:inset(0 0 calc(100% - var(--byf-split)) 0)!important}
#build-your-fit .byf-bottom{clip-path:inset(var(--byf-split) 0 0 0)!important}
'''
if '/* Build Your Fit — standardized 12-board compositor v7 */' not in s:
    s=s.replace('</style>',css+'\n</style>',1)

# Replace the two old Houndstooth boards with the newly standardized files.
s=s.replace('DB0194B3-AF6E-4964-B2F9-266330DB0A6D.jpeg','648F1080-1C4C-4FFD-BA17-C79CBE5D7309.jpeg')
s=s.replace('794DD1D2-8663-4830-9612-93E0EC9E5B03.jpeg','D2DC5EB5-3654-4B80-978B-238C3C4974F0.jpeg')

# All bottoms now use the exact same coordinate system; no Houndstooth-only offset.
old="bottomEl.style.setProperty('background-position',isHoundShort?'0 -2.15%':'0 0','important');"
new="bottomEl.style.setProperty('background-position','0 0','important');"
if old in s:
    s=s.replace(old,new,1)
elif new not in s:
    raise SystemExit('bottom positioning marker not found')

p.write_text(s)
