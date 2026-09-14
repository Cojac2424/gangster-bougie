from pathlib import Path
p=Path('index.html')
s=p.read_text()
if 'id="build-your-fit"' not in s:
    raise SystemExit('Build Your Fit not present')

# Build Your Fit v9: the standardized boards all share one coordinate system.
# Put the image-change seam in the exposed midriff, above every waistband, so
# the selected bottom supplies the torso-to-waistband transition and no bottom
# garment from the selected top board can leak into the composite.
css=r'''
/* Build Your Fit — midriff seam calibration v9 */
#build-your-fit .byf-model{--byf-split:42%!important}
#build-your-fit .byf-top{clip-path:inset(0 0 calc(100% - var(--byf-split)) 0)!important}
#build-your-fit .byf-bottom{clip-path:inset(var(--byf-split) 0 0 0)!important}
'''
if '/* Build Your Fit — midriff seam calibration v9 */' not in s:
    s=s.replace('</style>',css+'\n</style>',1)

# Keep the corrected uploaded Houndstooth workout-shorts filename.
s=s.replace('D2DC5EB5-3654-4B80-978B-238C3C4974F0.jpeg','D2DC5FB5-3654-4B80-978B-238C3C4974F0.jpeg')

# Every standardized bottom uses the exact same source coordinates.
old="bottomEl.style.setProperty('background-position',isHoundShort?'0 -2.15%':'0 0','important');"
new="bottomEl.style.setProperty('background-position','0 0','important');"
if old in s:
    s=s.replace(old,new,1)
elif new not in s:
    raise SystemExit('bottom positioning marker not found')

p.write_text(s)
