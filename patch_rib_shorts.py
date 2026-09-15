from pathlib import Path
import re

p=Path('index.html')
s=p.read_text()
if 'id="build-your-fit"' not in s: raise SystemExit('Build Your Fit not present')

# v39 — cart product thumbnails only. No Build Your Fit geometry changes.
# Patch the existing v38 cart renderer so each known real product gets one front image.
s=s.replace("const row=document.createElement('div');row.className='gb-cart-line';row.innerHTML='<div class=\"gb-cart-line-top\"><div><div class=\"gb-cart-line-name\"></div><div class=\"gb-cart-line-size\"></div></div><div class=\"gb-cart-line-price\"></div></div><div class=\"gb-cart-line-actions\"><div class=\"gb-cart-qty\"><button type=\"button\" data-cart-action=\"minus\" data-i=\"'+i+'\">−</button><span>'+q+'</span><button type=\"button\" data-cart-action=\"plus\" data-i=\"'+i+'\">+</button></div><button type=\"button\" class=\"gb-cart-remove\" data-cart-action=\"remove\" data-i=\"'+i+'\">Remove</button></div>';row.querySelector('.gb-cart-line-name').textContent=x.name||'Gangster Bougie Item';row.querySelector('.gb-cart-line-size').textContent='Size: '+(x.size||'—');row.querySelector('.gb-cart-line-price').textContent='US$'+(p*q).toFixed(2);lines.appendChild(row)",
"const row=document.createElement('div');row.className='gb-cart-line';const nm=x.name||'Gangster Bougie Item';const img=nm==='Oxblood Sports Bra'?'IMG_0547.jpeg':((nm==='Cream Leggings'||nm==='Cream High-Waisted Leggings'||nm==='Cream Workout Shorts')?'IMG_0553.jpeg':'');row.innerHTML='<div class=\"gb-cart-line-grid\"><div class=\"gb-cart-line-copy\"><div class=\"gb-cart-line-name\"></div><div class=\"gb-cart-line-size\"></div><div class=\"gb-cart-line-actions\"><div class=\"gb-cart-qty\"><button type=\"button\" data-cart-action=\"minus\" data-i=\"'+i+'\">−</button><span>'+q+'</span><button type=\"button\" data-cart-action=\"plus\" data-i=\"'+i+'\">+</button></div></div></div><div class=\"gb-cart-thumb-slot\"></div><div class=\"gb-cart-line-side\"><div class=\"gb-cart-line-price\"></div><button type=\"button\" class=\"gb-cart-remove\" data-cart-action=\"remove\" data-i=\"'+i+'\">Remove</button></div></div>';row.querySelector('.gb-cart-line-name').textContent=nm;row.querySelector('.gb-cart-line-size').textContent='Size: '+(x.size||'—');row.querySelector('.gb-cart-line-price').textContent='US$'+(p*q).toFixed(2);if(img){const im=document.createElement('img');im.className='gb-cart-thumb';im.src=img;im.alt=nm;im.loading='lazy';im.decoding='async';row.querySelector('.gb-cart-thumb-slot').appendChild(im)}lines.appendChild(row)")

# If v38's exact one-line renderer has shifted, fail rather than silently claiming success.
if 'gb-cart-thumb-slot' not in s:
    raise SystemExit('v38 cart renderer not found; no changes applied')

if 'Gangster Bougie cart thumbnails v39' not in s:
    css='''\n<style>/* Gangster Bougie cart thumbnails v39 */
.gb-cart-line-grid{display:grid;grid-template-columns:minmax(0,1fr) 82px auto;gap:14px;align-items:center}.gb-cart-line-copy{min-width:0}.gb-cart-thumb-slot{width:82px;height:82px;display:flex;align-items:center;justify-content:center}.gb-cart-thumb{display:block;width:82px;height:82px;object-fit:cover;border-radius:7px;background:#eee;border:1px solid rgba(216,169,40,.25)}.gb-cart-line-side{align-self:stretch;display:flex;flex-direction:column;align-items:flex-end;justify-content:space-between;gap:10px}.gb-cart-line-grid .gb-cart-line-actions{justify-content:flex-start;margin-top:12px}
@media(max-width:520px){.gb-cart-lines{padding-left:14px;padding-right:14px}.gb-cart-line-grid{grid-template-columns:minmax(0,1fr) 68px auto;gap:9px}.gb-cart-thumb-slot,.gb-cart-thumb{width:68px;height:68px}.gb-cart-line-price{font-size:.9rem}.gb-cart-remove{font-size:.72rem}.gb-cart-qty button{width:32px}.gb-cart-qty span{min-width:30px}}
</style>\n'''
    s=s.replace('</head>',css+'</head>')

p.write_text(s)
