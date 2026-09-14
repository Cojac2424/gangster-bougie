from pathlib import Path
p=Path('index.html')
s=p.read_text()
if 'id="build-your-fit"' not in s:
    raise SystemExit('Build Your Fit not present')

# Build Your Fit v13: standardized boards use one bare-torso handoff.
# The previous 39% splice was still close enough to garment edges that some
# high-waisted bottoms could intrude upward. Move the shared cut slightly toward
# the center of the exposed abdomen, and explicitly keep the same calibration
# at tablet/desktop widths so responsive CSS cannot restore an older split.
css=r'''
/* Build Your Fit — centered bare-torso splice calibration v13 */
#build-your-fit .byf-model{--byf-split:38.4%!important}
#build-your-fit .byf-top{clip-path:inset(0 0 calc(100% - var(--byf-split)) 0)!important}
#build-your-fit .byf-bottom{clip-path:inset(var(--byf-split) 0 0 0)!important;background-image:var(--byf-bottom-image)!important;background-position:0 0!important}
@media (min-width:700px){
  #build-your-fit .byf-model{--byf-split:38.4%!important}
  #build-your-fit .byf-top{clip-path:inset(0 0 calc(100% - var(--byf-split)) 0)!important}
  #build-your-fit .byf-bottom{clip-path:inset(var(--byf-split) 0 0 0)!important;background-position:0 0!important}
}
'''
old=r'''/* Build Your Fit — bare-torso splice calibration v12 */
#build-your-fit .byf-model{--byf-split:39%!important}
#build-your-fit .byf-top{clip-path:inset(0 0 calc(100% - var(--byf-split)) 0)!important}
#build-your-fit .byf-bottom{clip-path:inset(var(--byf-split) 0 0 0)!important;background-image:var(--byf-bottom-image)!important;background-position:0 0!important}
'''
if old in s:
    s=s.replace(old,css,1)
elif '/* Build Your Fit — centered bare-torso splice calibration v13 */' not in s:
    s=s.replace('</style>',css+'\n</style>',1)

s=s.replace('D2DC5EB5-3654-4B80-978B-238C3C4974F0.jpeg','D2DC5FB5-3654-4B80-978B-238C3C4974F0.jpeg')
oldpos="bottomEl.style.setProperty('background-position',isHoundShort?'0 -2.15%':'0 0','important');"
newpos="bottomEl.style.setProperty('background-position','0 0','important');"
if oldpos in s:
    s=s.replace(oldpos,newpos,1)
p.write_text(s)
