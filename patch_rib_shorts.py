from pathlib import Path
p=Path('index.html')
s=p.read_text()
if 'id="build-your-fit"' not in s:
    raise SystemExit('Build Your Fit not present')

# Build Your Fit v10: all 12 standardized boards share the same geometry.
# The seam belongs in the exposed midriff, not at either garment edge.  This
# lets the selected bottom provide its own upper torso + waistband while the
# selected top stops before any leggings/shorts from its source board appear.
css=r'''
/* Build Your Fit — mid-torso seam calibration v10 */
#build-your-fit .byf-model{--byf-split:37.6%!important}
#build-your-fit .byf-top{clip-path:inset(0 0 calc(100% - var(--byf-split)) 0)!important}
#build-your-fit .byf-bottom{clip-path:inset(var(--byf-split) 0 0 0)!important;background-image:var(--byf-bottom-image)!important;background-position:0 0!important}
'''
if '/* Build Your Fit — mid-torso seam calibration v10 */' not in s:
    s=s.replace('</style>',css+'\n</style>',1)

# Keep the corrected Houndstooth workout-shorts asset reference.
s=s.replace('D2DC5EB5-3654-4B80-978B-238C3C4974F0.jpeg','D2DC5FB5-3654-4B80-978B-238C3C4974F0.jpeg')

# Never apply a one-off vertical shift: standardized boards use identical coordinates.
old="bottomEl.style.setProperty('background-position',isHoundShort?'0 -2.15%':'0 0','important');"
new="bottomEl.style.setProperty('background-position','0 0','important');"
if old in s:
    s=s.replace(old,new,1)

p.write_text(s)
