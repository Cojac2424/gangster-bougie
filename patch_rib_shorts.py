from pathlib import Path
p=Path('index.html')
s=p.read_text()
if 'id="build-your-fit"' not in s:
    raise SystemExit('Build Your Fit not present')

# v4: replace the accumulated v2/v3 geometry with one authoritative compositor.
# Both selectable boards render in the same full-model rectangle. Only clipping
# changes at the seam, so switching top/bottom cannot change scale or position.
css=r'''
/* Build Your Fit — authoritative compositor v4 */
#build-your-fit .byf-model{
  --byf-split:40.4%;
  position:relative!important;
  width:min(170px,27vw,14.2svh)!important;
  aspect-ratio:1/6!important;
  height:auto!important;
  min-height:0!important;
  max-height:none!important;
  overflow:hidden!important;
  background:#ddd!important;
}
#build-your-fit .byf-half{
  position:absolute!important;
  inset:0!important;
  width:100%!important;
  height:100%!important;
  background-repeat:no-repeat!important;
  background-size:400% 100%!important;
  background-position:0 0!important;
  touch-action:pan-y;
}
#build-your-fit .byf-top{
  clip-path:inset(0 0 calc(100% - var(--byf-split)) 0)!important;
  z-index:1!important;
}
#build-your-fit .byf-bottom{
  clip-path:inset(var(--byf-split) 0 0 0)!important;
  z-index:2!important;
  background-image:var(--byf-bottom-image)!important;
}
#build-your-fit .byf-bottom::before{display:none!important;content:none!important}
#build-your-fit .byf-seam{display:none!important}
#build-your-fit .byf-arrow{
  position:absolute!important;
  width:30px!important;height:30px!important;
  margin:0!important;transform:translateY(-50%)!important;
  border-radius:50%!important;z-index:8!important;
  font-size:1.12rem!important;
}
#build-your-fit .byf-arrow.prev{left:3px!important;right:auto!important}
#build-your-fit .byf-arrow.next{right:3px!important;left:auto!important}
#build-your-fit .byf-top .byf-arrow{top:27%!important}
#build-your-fit .byf-bottom .byf-arrow{top:65%!important}
#build-your-fit .byf-label{
  position:absolute!important;left:5px!important;right:5px!important;
  width:auto!important;max-width:none!important;transform:none!important;
  z-index:9!important;text-align:center!important;white-space:normal!important;
  overflow:visible!important;padding:5px 3px!important;
  font-size:clamp(.46rem,1.7vw,.58rem)!important;line-height:1.08!important;
  letter-spacing:.025em!important;
}
#build-your-fit .byf-top .byf-label{top:5px!important;bottom:auto!important}
#build-your-fit .byf-bottom .byf-label{top:auto!important;bottom:5px!important}
@media(max-width:760px){
  #build-your-fit{padding-top:24px!important;padding-bottom:24px!important}
  #build-your-fit .byf-shell{grid-template-columns:1fr!important;gap:14px!important}
  #build-your-fit .byf-model{width:min(158px,38vw,13.8svh)!important}
  #build-your-fit .byf-label{font-size:.48rem!important}
}
'''
if '/* Build Your Fit — authoritative compositor v4 */' not in s:
    s=s.replace('</style>',css+'\n</style>',1)
else:
    raise SystemExit('v4 already present')

# Make rendering explicit: every change assigns the selected top and bottom URL.
old="function render(){topEl.style.backgroundImage=`url('${tops[ti][1]}')`;bottomEl.style.setProperty('--byf-bottom-image',`url('${bottoms[bi][1]}')`);bottomEl.style.backgroundImage=`url('${bottoms[bi][1]}')`;document.getElementById('byfTopLabel').textContent=tops[ti][0];document.getElementById('byfBottomLabel').textContent=bottoms[bi][0]}"
new="function render(){const topUrl=`url('${tops[ti][1]}')`;const bottomUrl=`url('${bottoms[bi][1]}')`;topEl.style.backgroundImage=topUrl;bottomEl.style.setProperty('--byf-bottom-image',bottomUrl);bottomEl.style.backgroundImage=bottomUrl;document.getElementById('byfTopLabel').textContent=tops[ti][0];document.getElementById('byfBottomLabel').textContent=bottoms[bi][0]}"
if old in s:
    s=s.replace(old,new,1)

p.write_text(s)
