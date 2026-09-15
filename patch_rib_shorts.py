from pathlib import Path
import re

p=Path('index.html')
s=p.read_text()
if 'id="build-your-fit"' not in s: raise SystemExit('Build Your Fit not present')

# v35 performance cleanup. Appearance and Build Your Fit geometry are untouched.
# Keep only the user's selected Lookbook images in the live page.
women_keep=['09D6C9A9-6759-4A5E-8C29-87A00A34A157.png','55CF2A2E-AA03-4D2F-9D7B-2E523AEC0041.png','C30C5493-EC0F-4DC6-B74D-FC2CC515FEB4.png','ECA29DBD-304E-493E-8A51-76E7CB5E4BC8.png']
men_keep=['IMG_2021.jpeg','IMG_2028.jpeg','IMG_2029.jpeg','IMG_2030.jpeg']
lookbook=s.index('<section class="lookbook"')
shop=s.index('<section id="shop"',lookbook) if '<section id="shop"' in s[lookbook:] else s.index('<section',lookbook+30)
block=s[lookbook:shop]
first_window=block.find('<div class="lookbook-window">')
if first_window!=-1:
    hint=block.find('<div class="lookbook-hint">',first_window)
    if hint!=-1:
        prefix,suffix=block[:first_window],block[hint:]
        def row(files,cls=''):
            c=(' '+cls) if cls else ''
            imgs=''.join(f'<div class="lookbook-item"><img src="{f}" alt="Gangster Bougie lookbook" loading="lazy" decoding="async"></div>' for f in files)
            return f'<div class="lookbook-window"><div class="lookbook-grid{c}">{imgs}{imgs}</div></div>'
        block=prefix+row(women_keep)+row(men_keep,'men-ticker')+suffix
        s=s[:lookbook]+block+s[shop:]

# Native lazy loading for ordinary visible-page images.
def optimize_img(m):
    tag=m.group(0)
    if re.search(r'\bloading\s*=',tag,re.I): return tag
    return tag[:-1]+' loading="lazy" decoding="async">'
s=re.sub(r'<img\b[^>]*>',optimize_img,s,flags=re.I)

# Hidden product modals previously contained real src= URLs, allowing browsers to
# discover/download large galleries during initial page load. Convert modal images
# to data-src and activate them only when that modal is actually opened.
def defer_modal(m):
    block=m.group(0)
    block=re.sub(r'<img\b([^>]*?)\bsrc="([^"]+)"([^>]*)>',lambda x:'<img'+x.group(1)+'data-src="'+x.group(2)+'"'+x.group(3)+'>',block,flags=re.I)
    return block
s=re.sub(r'<div class="modal"\b.*?(?=<div class="modal"\b|<script\b)',defer_modal,s,flags=re.S|re.I)

# One small loader watches for any modal becoming open and restores only that modal's images.
loader='''\n<script>/* Deferred modal images v35 */\n(function(){\n function loadModal(modal){if(!modal)return;modal.querySelectorAll('img[data-src]').forEach(function(img){if(!img.getAttribute('src'))img.setAttribute('src',img.dataset.src);});}\n document.addEventListener('click',function(){requestAnimationFrame(function(){document.querySelectorAll('.modal.open').forEach(loadModal);});},true);\n new MutationObserver(function(ms){ms.forEach(function(m){var el=m.target;if(el.classList&&el.classList.contains('modal')&&el.classList.contains('open'))loadModal(el);});}).observe(document.body,{subtree:true,attributes:true,attributeFilter:['class']});\n})();\n</script>\n'''
if 'Deferred modal images v35' not in s:
    s=s.replace('</body>',loader+'</body>')

s=re.sub(r'\n?<script>\s*/\* Safe native lazy loading v31 \*/.*?</script>\s*','\n',s,flags=re.S)
p.write_text(s)
