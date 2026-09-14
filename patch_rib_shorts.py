from pathlib import Path
p=Path('index.html')
s=p.read_text()
if 'id="build-your-fit"' not in s:
    raise SystemExit('Build Your Fit not present')

# v19: keep all proven vertical splice values untouched. Join front/back into
# one continuous viewer and give each quarter-view enough horizontal room for
# the outer hands/arms/shoulders instead of clipping them at separate windows.
css=r'''
/* Build Your Fit — joined front + back viewer v19 */
#build-your-fit .byf-model-pair{display:flex!important;justify-content:center!important;align-items:flex-start!important;gap:0!important;background:#efede9!important;overflow:hidden!important;border-radius:16px!important;padding:0 5px!important}
#build-your-fit .byf-view{display:flex!important;flex-direction:column!important;align-items:center!important;gap:0!important;overflow:visible!important}
#build-your-fit .byf-view-name{display:none!important}
#build-your-fit .byf-model-pair .byf-model{border-radius:0!important;overflow:visible!important}
#build-your-fit .byf-model-pair .byf-view:first-child .byf-model{margin-right:0!important}
#build-your-fit .byf-model-pair .byf-view:last-child .byf-model{margin-left:0!important}
#build-your-fit .byf-back-model .byf-half{background-position:33.333333% 0!important}
#build-your-fit .byf-back-model .byf-top,#build-your-fit .byf-back-model .byf-bottom{pointer-events:none!important}
#build-your-fit .byf-back-model .byf-arrow,#build-your-fit .byf-back-model .byf-label{display:none!important}
@media(max-width:760px){#build-your-fit .byf-model-pair{gap:0!important;padding:0 3px!important}#build-your-fit .byf-model-pair .byf-model{width:min(154px,38vw,14svh)!important}}
'''
for marker in ['/* Build Your Fit — synchronized front + back v18 */']:
    if marker in s:
        start=s.index(marker)
        end=s.index('</style>',start)
        s=s[:start]+s[end:]
        break
if '/* Build Your Fit — joined front + back viewer v19 */' not in s:
    s=s.replace('</style>',css+'\n</style>',1)

# No render/splice logic changes: front stays 42.2%, Onyx bottoms 42.8%,
# back remains synchronized from the second view on the same source board.
p.write_text(s)
