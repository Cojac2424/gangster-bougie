from pathlib import Path

p=Path('index.html')
s=p.read_text()
if 'id="build-your-fit"' not in s: raise SystemExit('Build Your Fit not present')

# v41 — stacking fix only. Keep Build Your Fit arrows below the sticky site header.
# No model dimensions, positions, split points, arrow coordinates, or compositor geometry are changed.
if 'Build Your Fit arrow stacking v41' not in s:
    css='''\n<style>/* Build Your Fit arrow stacking v41 */
/* Header is z-index:20. The arrows only need to sit above the models, not above the site navigation. */
#build-your-fit .byf-model-pair{z-index:1!important}
#build-your-fit .byf-outer-arrow{z-index:10!important}
</style>\n'''
    s=s.replace('</head>',css+'</head>')

p.write_text(s)
