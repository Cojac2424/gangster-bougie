from pathlib import Path
p=Path('index.html')
s=p.read_text()
if 'id="build-your-fit"' not in s:
    raise SystemExit('Build Your Fit not present')

# v20: presentation only. Keep the proven vertical splice values and synchronized
# front/back image logic untouched. Make the pair read as one continuous viewer
# and place top/bottom navigation at the far left and far right edges.
css=r'''
/* Build Your Fit — continuous two-model viewer + outer controls v20 */
#build-your-fit .byf-model-pair{position:relative!important;display:flex!important;justify-content:center!important;align-items:flex-start!important;gap:0!important;background:#efede9!important;overflow:hidden!important;border-radius:16px!important;padding:0 42px!important}
#build-your-fit .byf-view{display:flex!important;flex-direction:column!important;align-items:center!important;gap:0!important;overflow:visible!important}
#build-your-fit .byf-view-name{display:none!important}
#build-your-fit .byf-model-pair .byf-model{border:0!important;border-radius:0!important;overflow:visible!important;box-shadow:none!important}
#build-your-fit .byf-model-pair .byf-view:first-child .byf-model{margin-right:0!important}
#build-your-fit .byf-model-pair .byf-view:last-child .byf-model{margin-left:0!important}
#build-your-fit .byf-back-model .byf-half{background-position:33.333333% 0!important}
#build-your-fit .byf-back-model .byf-top,#build-your-fit .byf-back-model .byf-bottom{pointer-events:none!important}
#build-your-fit .byf-back-model .byf-arrow,#build-your-fit .byf-back-model .byf-label{display:none!important}
#build-your-fit .byf-model-pair #byfModel .byf-arrow{position:fixed!important;z-index:12!important}
#build-your-fit .byf-model-pair #byfTop .byf-arrow.prev,#build-your-fit .byf-model-pair #byfBottom .byf-arrow.prev{left:max(10px,calc(50vw - min(360px,46vw)))!important;right:auto!important}
#build-your-fit .byf-model-pair #byfTop .byf-arrow.next,#build-your-fit .byf-model-pair #byfBottom .byf-arrow.next{right:max(10px,calc(50vw - min(360px,46vw)))!important;left:auto!important}
#build-your-fit .byf-model-pair #byfTop .byf-arrow.prev,#build-your-fit .byf-model-pair #byfTop .byf-arrow.next{top:42%!important}
#build-your-fit .byf-model-pair #byfBottom .byf-arrow.prev,#build-your-fit .byf-model-pair #byfBottom .byf-arrow.next{top:66%!important}
@media(max-width:760px){#build-your-fit .byf-model-pair{gap:0!important;padding:0 30px!important}#build-your-fit .byf-model-pair .byf-model{width:min(154px,38vw,14svh)!important}#build-your-fit .byf-model-pair #byfTop .byf-arrow.prev,#build-your-fit .byf-model-pair #byfBottom .byf-arrow.prev{left:8px!important}#build-your-fit .byf-model-pair #byfTop .byf-arrow.next,#build-your-fit .byf-model-pair #byfBottom .byf-arrow.next{right:8px!important}}
'''
for marker in ['/* Build Your Fit — joined front + back viewer v19 */']:
    if marker in s:
        start=s.index(marker)
        end=s.index('</style>',start)
        s=s[:start]+s[end:]
        break
if '/* Build Your Fit — continuous two-model viewer + outer controls v20 */' not in s:
    s=s.replace('</style>',css+'\n</style>',1)
p.write_text(s)
