from pathlib import Path
import re

p=Path('index.html')
s=p.read_text()
if 'id="build-your-fit"' not in s: raise SystemExit('Build Your Fit not present')

# v34 production-speed cleanup.
# Keep only the user's selected Lookbook images in the live page.
# Originals remain in the repository. Build Your Fit geometry and product imagery are untouched.

# Women's keepers from the original numbered selection: 1, 5, 9, 11.
women_keep=[
 '09D6C9A9-6759-4A5E-8C29-87A00A34A157.png',
 '55CF2A2E-AA03-4D2F-9D7B-2E523AEC0041.png',
 'C30C5493-EC0F-4DC6-B74D-FC2CC515FEB4.png',
 'ECA29DBD-304E-493E-8A51-76E7CB5E4BC8.png'
]
# Men's keepers from the numbered selection: 1, 13, 16, 17.
men_keep=['IMG_2021.jpeg','IMG_2028.jpeg','IMG_2029.jpeg','IMG_2030.jpeg']

lookbook=s.index('<section class="lookbook"')
shop=s.index('<section id="shop"',lookbook) if '<section id="shop"' in s[lookbook:] else s.index('<section',lookbook+30)
block=s[lookbook:shop]

# Replace all existing Lookbook windows with two lightweight keeper-only rows.
first_window=block.find('<div class="lookbook-window">')
if first_window!=-1:
    hint=block.find('<div class="lookbook-hint">',first_window)
    if hint!=-1:
        prefix=block[:first_window]
        suffix=block[hint:]
        def row(files, cls=''):
            c=(' '+cls) if cls else ''
            imgs=''.join(f'<div class="lookbook-item"><img src="{f}" alt="Gangster Bougie lookbook" loading="lazy" decoding="async"></div>' for f in files)
            # Repeat the four keepers once for the existing seamless ticker animation; browsers reuse the same files from cache.
            return f'<div class="lookbook-window"><div class="lookbook-grid{c}">{imgs}{imgs}</div></div>'
        block=prefix+row(women_keep)+row(men_keep,'men-ticker')+suffix
        s=s[:lookbook]+block+s[shop:]

# Parse-time native lazy loading for ordinary HTML images.
def optimize_img(m):
    tag=m.group(0)
    if re.search(r'\bloading\s*=', tag, re.I): return tag
    return tag[:-1]+' loading="lazy" decoding="async">'
s=re.sub(r'<img\b[^>]*>', optimize_img, s, flags=re.I)

# Remove older JS lazy-loader if still present.
s=re.sub(r'\n?<script>\s*/\* Safe native lazy loading v31 \*/.*?</script>\s*','\n',s,flags=re.S)

p.write_text(s)
