from pathlib import Path
p=Path('index.html')
s=p.read_text()
if 'id="build-your-fit"' not in s:
    raise SystemExit('Build Your Fit not present')

# v21: preserve v20 controls and ALL proven vertical splice values. Correct only
# the horizontal framing of the back-facing second model so its outside shoulder,
# arm and hip are not clipped. Front framing/render logic remains untouched.
css=r'''
/* Build Your Fit — continuous two-model viewer + outer controls + full back v21 */
#build-your-fit .byf-model-pair{position:relative!important;display:flex!important;justify-content:center!important;align-items:flex-start!important;gap:0!important;background:#efede9!important;overflow:hidden!important;border-radius:16px!important;padding:0 42px!important}
#build-your-fit .byf-view{display:flex!important;flex-direction:column!important;align-items:center!important;gap:0!important;overflow:visible!important}
#build-your-fit .byf-view-name{display:none!important}
#build-your-fit .byf-model-pair .byf-model{border:0!important;border-radius:0!important;overflow:visible!important;box-shadow:none!important}
#build-your-fit .byf-model-pair .byf-view:first-child .byf-model{margin-right:0!important}
#build-your-fit .byf-model-pair .byf-view:last-child{width:calc(var(--byf-model-width,154px) + 18px)!important;overflow:visible!important}
#build-your-fit .byf-model-pair .byf-view:last-child .byf-model{margin-left:0!important;width:calc(100% + 18px)!important;max-width:none!important}
#build-your-fit .byf-back-model .byf-half{background-position:32.1% 0!important}
#build-your-fit .byf-back-model .byf-top,#build-your-fit .byf-back-model .byf-bottom{pointer-events:none!important}
#build-your-fit .byf-back-model .byf-arrow,#build-your-fit .byf-back-model .byf-label{display:none!important}
#build-your-fit .byf-model-pair #byfModel .byf-arrow{position:fixed!important;z-index:12!important}
#build-your-fit .byf-model-pair #byfTop .byf-arrow.prev,#build-your-fit .byf-model-pair #byfBottom .byf-arrow.prev{left:max(10px,calc(50vw - min(360px,46vw)))!important;right:auto!important}
#build-your-fit .byf-model-pair #byfTop .byf-arrow.next,#build-your-fit .byf-model-pair #byfBottom .byf-arrow.next{right:max(10px,calc(50vw - min(360px,46vw)))!important;left:auto!important}
#build-your-fit .byf-model-pair #byfTop .byf-arrow.prev,#build-your-fit .byf-model-pair #byfTop .byf-arrow.next{top:42%!important}
#build-your-fit .byf-model-pair #byfBottom .byf-arrow.prev,#build-your-fit .byf-model-pair #byfBottom .byf-arrow.next{top:66%!important}
@media(max-width:760px){#build-your-fit .byf-model-pair{gap:0!important;padding:0 30px!important}#build-your-fit .byf-model-pair .byf-view:first-child .byf-model{width:min(154px,36vw,14svh)!important}#build-your-fit .byf-model-pair .byf-view:last-child{width:min(172px,42vw,15.6svh)!important}#build-your-fit .byf-model-pair .byf-view:last-child .byf-model{width:100%!important}#build-your-fit .byf-model-pair #byfTop .byf-arrow.prev,#build-your-fit .byf-model-pair #byfBottom .byf-arrow.prev{left:8px!important}#build-your-fit .byf-model-pair #byfTop .byf-arrow.next,#build-your-fit .byf-model-pair #byfBottom .byf-arrow.next{right:8px!important}}
'''
for marker in ['/* Build Your Fit — continuous two-model viewer + outer controls v20 */']:
    if marker in s:
        start=s.index(marker)
        end=s.index('</style>',start)
        s=s[:start]+s[end:]
        break
if '/* Build Your Fit — continuous two-model viewer + outer controls + full back v21 */' not in s:
    s=s.replace('</style>',css+'\n</style>',1)

# The render function is deliberately unchanged: 42.2% globally, 42.8% for
# Onyx Leggings/Workout Shorts, with synchronized top/bottom selection.
p.write_text(s)
