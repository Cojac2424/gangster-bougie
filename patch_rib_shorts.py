from pathlib import Path
p=Path('index.html')
s=p.read_text()
if 'id="build-your-fit"' not in s:
    raise SystemExit('Build Your Fit not present')

# Targeted refinement only: preserve the working full-body coordinate system,
# move the shared seam to the true waist, and keep controls off the clothing.
css=r'''
/* Build Your Fit — control + true-waist refinement v3 */
.byf-model{--byf-split:39.5%!important}
.byf-top{clip-path:inset(0 0 calc(100% - var(--byf-split)) 0)!important}
.byf-bottom{clip-path:inset(var(--byf-split) 0 0 0)!important;background-image:var(--byf-bottom-image)!important}
.byf-seam{top:var(--byf-split)!important;height:0!important;background:transparent!important}
.byf-arrow{width:32px!important;height:32px!important;font-size:1.25rem!important}
.byf-arrow.prev{left:4px!important}.byf-arrow.next{right:4px!important}
.byf-top .byf-arrow{top:22%!important}.byf-bottom .byf-arrow{top:70%!important}
.byf-label{left:4px!important;right:4px!important;transform:none!important;width:auto!important;max-width:none!important;text-align:center!important;white-space:normal!important;overflow:visible!important;padding:5px 4px!important;font-size:clamp(.48rem,2.1vw,.62rem)!important;line-height:1.12!important;letter-spacing:.045em!important}
.byf-top .byf-label{top:8px!important;bottom:auto!important}
.byf-bottom .byf-label{top:auto!important;bottom:8px!important}
@media(max-width:760px){.byf-arrow{width:30px!important;height:30px!important;font-size:1.15rem!important}.byf-arrow.prev{left:3px!important}.byf-arrow.next{right:3px!important}.byf-label{font-size:.5rem!important;letter-spacing:.025em!important}}
'''
marker='/* Build Your Fit — control + true-waist refinement v3 */'
if marker not in s:
    s=s.replace('</style>',css+'\n</style>',1)
else:
    raise SystemExit('v3 refinement already present')

p.write_text(s)
