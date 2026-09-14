from pathlib import Path
p=Path('index.html')
s=p.read_text()
if 'id="build-your-fit"' not in s:
    raise SystemExit('Build Your Fit not present')

# Build Your Fit v12: all 12 standardized boards share the same geometry.
# The handoff must occur entirely on bare torso: below every sports-bra hem and
# above every leggings/shorts waistband.  Both layers meet at the identical
# coordinate so no garment pixels from either source can leak into the splice.
css=r'''
/* Build Your Fit — bare-torso splice calibration v12 */
#build-your-fit .byf-model{--byf-split:39%!important}
#build-your-fit .byf-top{clip-path:inset(0 0 calc(100% - var(--byf-split)) 0)!important}
#build-your-fit .byf-bottom{clip-path:inset(var(--byf-split) 0 0 0)!important;background-image:var(--byf-bottom-image)!important;background-position:0 0!important}
'''
old=r'''/* Build Your Fit — clean midriff seam calibration v11 */
#build-your-fit .byf-model{--byf-split:40%!important}
#build-your-fit .byf-top{clip-path:inset(0 0 calc(100% - var(--byf-split)) 0)!important}
#build-your-fit .byf-bottom{clip-path:inset(var(--byf-split) 0 0 0)!important;background-image:var(--byf-bottom-image)!important;background-position:0 0!important}
'''
if old in s:
    s=s.replace(old,css,1)
elif '/* Build Your Fit — bare-torso splice calibration v12 */' not in s:
    s=s.replace('</style>',css+'\n</style>',1)

s=s.replace('D2DC5EB5-3654-4B80-978B-238C3C4974F0.jpeg','D2DC5FB5-3654-4B80-978B-238C3C4974F0.jpeg')

oldpos="bottomEl.style.setProperty('background-position',isHoundShort?'0 -2.15%':'0 0','important');"
newpos="bottomEl.style.setProperty('background-position','0 0','important');"
if oldpos in s:
    s=s.replace(oldpos,newpos,1)

p.write_text(s)
