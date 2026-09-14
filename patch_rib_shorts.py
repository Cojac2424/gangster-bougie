from pathlib import Path
import re

p=Path('index.html')
s=p.read_text()
if 'id="build-your-fit"' not in s: raise SystemExit('Build Your Fit not present')

# v32: Parse-time native lazy loading. Performance only — no layout, image-source,
# Build Your Fit compositor, sizing, crop, arrow, or visual changes.
# Keep the header brand image eager. CSS background images (header/hero and BYF boards)
# are intentionally untouched.

def optimize_img(m):
    tag=m.group(0)
    # Never rewrite an already-optimized tag.
    if re.search(r'\bloading\s*=', tag, re.I):
        return tag
    # Brand/header image is above the fold and should stay eager.
    if 'IMG_1849.jpeg' in tag:
        return tag[:-1] + ' loading="eager" fetchpriority="high">'
    # All ordinary HTML images are safe to defer until near the viewport.
    return tag[:-1] + ' loading="lazy" decoding="async">'

s=re.sub(r'<img\b[^>]*>', optimize_img, s, flags=re.I)

# Remove the older end-of-body JS lazy-loader because parse-time attributes now do the job.
s=re.sub(
    r'\n?<script>\s*/\* Safe native lazy loading v31 \*/.*?</script>\s*',
    '\n',
    s,
    flags=re.S
)

p.write_text(s)
