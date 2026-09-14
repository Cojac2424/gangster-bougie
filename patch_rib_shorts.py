from pathlib import Path
p=Path('index.html')
s=p.read_text()
if 'id="build-your-fit"' not in s:
    raise SystemExit('Build Your Fit not present')

# v24: keep v23 responsive layout/shared swipe and LOCKED compositor geometry.
# Only fix arrow presentation: four visible controls centered directly on the
# left/right panel edges, upper pair = tops, lower pair = bottoms.
css=r'''
/* Build Your Fit — responsive joined viewer + edge controls v24 */
#build-your-fit .byf-shell{grid-template-columns:minmax(250px,330px) minmax(0,1fr)!important;gap:28px!important;align-items:start!important}
#build-your-fit .byf-copy{min-width:0!important;padding-right:4px!important}
#build-your-fit .byf-builder{min-width:0!important;width:100%!important}
#build-your-fit .byf-model-pair{position:relative!important;display:flex!important;justify-content:center!important;align-items:flex-start!important;gap:0!important;width:max-content!important;max-width:100%!important;margin:0 auto!important;background:#efede9!important;overflow:visible!important;border-radius:16px!important;padding:0 38px!important}
#build-your-fit .byf-view{display:flex!important;flex-direction:column!important;align-items:center!important;gap:0!important;overflow:visible!important;width:auto!important}
#build-your-fit .byf-view-name{display:none!important}
#build-your-fit .byf-model-pair .byf-model{border:0!important;border-radius:0!important;overflow:visible!important;box-shadow:none!important;max-width:none!important;margin:0!important;width:clamp(150px,18vw,210px)!important}
#build-your-fit .byf-back-model .byf-half{background-position:33.333333% 0!important}
#build-your-fit .byf-back-model .byf-top,#build-your-fit .byf-back-model .byf-bottom{pointer-events:none!important}
#build-your-fit .byf-back-model .byf-arrow,#build-your-fit .byf-back-model .byf-label{display:none!important}
#build-your-fit .byf-model-pair #byfModel .byf-arrow{display:flex!important;position:absolute!important;z-index:30!important;width:42px!important;height:42px!important;align-items:center!important;justify-content:center!important;background:#111!important;color:#d9a11e!important;border:1.5px solid #d9a11e!important;border-radius:50%!important;font-size:1.65rem!important;line-height:1!important;margin:0!important;transform:translateY(-50%)!important;box-shadow:0 2px 8px rgba(0,0,0,.35)!important}
#build-your-fit .byf-model-pair #byfTop .byf-arrow.prev,#build-your-fit .byf-model-pair #byfBottom .byf-arrow.prev{left:-21px!important;right:auto!important}
#build-your-fit .byf-model-pair #byfTop .byf-arrow.next,#build-your-fit .byf-model-pair #byfBottom .byf-arrow.next{right:-21px!important;left:auto!important}
#build-your-fit .byf-model-pair #byfTop .byf-arrow.prev,#build-your-fit .byf-model-pair #byfTop .byf-arrow.next{top:28%!important}
#build-your-fit .byf-model-pair #byfBottom .byf-arrow.prev,#build-your-fit .byf-model-pair #byfBottom .byf-arrow.next{top:68%!important}
@media(min-width:761px) and (max-width:1180px){#build-your-fit .byf-shell{grid-template-columns:minmax(220px,30%) minmax(0,70%)!important;gap:18px!important}#build-your-fit .byf-model-pair{padding:0 34px!important}#build-your-fit .byf-model-pair .byf-model{width:min(190px,18vw,22svh)!important}}
@media(max-width:760px){#build-your-fit{padding-top:20px!important;padding-bottom:20px!important}#build-your-fit .byf-shell{grid-template-columns:1fr!important;gap:12px!important}#build-your-fit .byf-model-pair{width:max-content!important;max-width:calc(100% - 24px)!important;padding:0 12px!important}#build-your-fit .byf-model-pair .byf-model,#build-your-fit .byf-model-pair .byf-view:first-child .byf-model,#build-your-fit .byf-model-pair .byf-view:last-child .byf-model{width:min(154px,40vw,14svh)!important}#build-your-fit .byf-model-pair #byfModel .byf-arrow{width:38px!important;height:38px!important;font-size:1.5rem!important}#build-your-fit .byf-model-pair #byfTop .byf-arrow.prev,#build-your-fit .byf-model-pair #byfBottom .byf-arrow.prev{left:-19px!important}#build-your-fit .byf-model-pair #byfTop .byf-arrow.next,#build-your-fit .byf-model-pair #byfBottom .byf-arrow.next{right:-19px!important}}
'''
for marker in ['/* Build Your Fit — responsive joined viewer + shared controls v23 */']:
    if marker in s:
        start=s.index(marker)
        end=s.index('</style>',start)
        s=s[:start]+s[end:]
        break
if '/* Build Your Fit — responsive joined viewer + edge controls v24 */' not in s:
    s=s.replace('</style>',css+'\n</style>',1)

# Preserve v23 shared front+back swipe zones exactly.
p.write_text(s)
