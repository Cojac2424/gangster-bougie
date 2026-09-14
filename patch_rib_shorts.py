from pathlib import Path
import re

p=Path('index.html')
s=p.read_text()
if 'id="build-your-fit"' not in s: raise SystemExit('Build Your Fit not present')

# v33 production-speed cleanup.
# Remove the legacy WOMEN'S lookbook carousel only. Those PNGs are multi-megabyte
# legacy campaign assets and are being replaced by Fall / Signature imagery.
# Men's lookbook, Shop, hero and Build Your Fit are untouched.
lookbook_start='<div class="lookbook-window"><div class="lookbook-grid"><div class="lookbook-item"><img src="09D6C9A9-6759-4A5E-8C29-87A00A34A157.png"'
if lookbook_start in s:
    start=s.index('<div class="lookbook-window">', s.index('<section class="lookbook"'))
    men=s.index('<div class="lookbook-window"><div class="lookbook-grid men-ticker">', start)
    s=s[:start]+s[men:]

# Parse-time native lazy loading for ordinary HTML images.
def optimize_img(m):
    tag=m.group(0)
    if re.search(r'\bloading\s*=', tag, re.I):
        return tag
    return tag[:-1] + ' loading="lazy" decoding="async">'

s=re.sub(r'<img\b[^>]*>', optimize_img, s, flags=re.I)

# Remove older JS lazy-loader if still present.
s=re.sub(r'\n?<script>\s*/\* Safe native lazy loading v31 \*/.*?</script>\s*','\n',s,flags=re.S)

p.write_text(s)
