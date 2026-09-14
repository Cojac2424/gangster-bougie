from pathlib import Path
p=Path('index.html')
s=p.read_text()
if 'id="build-your-fit"' not in s:
    raise SystemExit('Build Your Fit not present')

# Build Your Fit v11: all 12 standardized boards share the same geometry.
# Keep the top/bottom handoff centered inside the bare midriff so the seam is
# away from both the sports-bra hem and every waistband. This prevents a hard
# horizontal garment-edge line from appearing across mixed outfits.
css=r'''
/* Build Your Fit — clean midriff seam calibration v11 */
#build-your-fit .byf-model{--byf-split:40%!important}
#build-your-fit .byf-top{clip-path:inset(0 0 calc(100% - var(--byf-split)) 0)!important}
#build-your-fit .byf-bottom{clip-path:inset(var(--byf-split) 0 0 0)!important;background-image:var(--byf-bottom-image)!important;background-position:0 0!important}
'''
# Replace the previous calibration rather than stacking another competing rule.
old=r'''/* Build Your Fit — mid-torso seam calibration v10 */
#build-your-fit .byf-model{--byf-split:37.6%!important}
#build-your-fit .byf-top{clip-path:inset(0 0 calc(100% - var(--byf-split)) 0)!important}
#build-your-fit .byf-bottom{clip-path:inset(var(--byf-split) 0 0 0)!important;background-image:var(--byf-bottom-image)!important;background-position:0 0!important}
'''
if old in s:
    s=s.replace(old,css,1)
elif '/* Build Your Fit — clean midriff seam calibration v11 */' not in s:
    s=s.replace('</style>',css+'\n</style>',1)

# Keep the corrected Houndstooth workout-shorts asset reference.
s=s.replace('D2DC5EB5-3654-4B80-978B-238C3C4974F0.jpeg','D2DC5FB5-3654-4B80-978B-238C3C4974F0.jpeg')

# Standardized boards use identical source coordinates; never vertically shift one bottom.
oldpos="bottomEl.style.setProperty('background-position',isHoundShort?'0 -2.15%':'0 0','important');"
newpos="bottomEl.style.setProperty('background-position','0 0','important');"
if oldpos in s:
    s=s.replace(oldpos,newpos,1)

p.write_text(s)
