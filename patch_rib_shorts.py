from pathlib import Path
p=Path('index.html')
s=p.read_text()
if 'id="build-your-fit"' not in s: raise SystemExit('Build Your Fit not present')

# v29: Signature Fit Oxblood real-product front + back. Preserve viewer/compositor geometry.
css=r'''
/* Build Your Fit — real product front/back v29 */
#build-your-fit .byf-fit-item{position:relative!important;padding-right:214px!important;min-height:118px!important}
#build-your-fit .byf-real-product-pair{display:none;position:absolute;right:0;top:50%;transform:translateY(-50%);gap:6px;align-items:center}
#build-your-fit .byf-real-product-pair.show{display:flex}
#build-your-fit .byf-real-product-pair img{width:98px;height:98px;object-fit:contain;background:#fff;border-radius:10px;border:1px solid rgba(217,161,30,.55);padding:3px}
@media(max-width:560px){#build-your-fit .byf-fit-item{padding-right:158px!important;min-height:96px!important}#build-your-fit .byf-real-product-pair img{width:72px;height:72px}}
'''
if '/* Build Your Fit — real product front/back v29 */' not in s:
    s=s.replace('</style>',css+'\n</style>',1)

# Upgrade the existing single Oxblood real-product slot to a compact front/back pair.
old='<img class="byf-real-product" id="byfTopRealProduct" alt="Actual product">'
new='<div class="byf-real-product-pair" id="byfTopRealProductPair"><img src="IMG_0547.jpeg" alt="Oxblood Sports Bra front"><img src="IMG_0548.jpeg" alt="Oxblood Sports Bra back"></div>'
if old in s:
    s=s.replace(old,new,1)

# Replace v28 single-image render control with pair visibility. Do not alter fit/model rendering.
oldjs="const rp=document.getElementById('byfTopRealProduct');if(rp){const ox=tops[ti][0]==='Oxblood Sports Bra';rp.classList.toggle('show',ox);if(ox){rp.src='IMG_0547.jpeg';rp.alt='Actual Oxblood Sports Bra product'}}}"
newjs="const rpp=document.getElementById('byfTopRealProductPair');if(rpp){rpp.classList.toggle('show',tops[ti][0]==='Oxblood Sports Bra')}}"
if oldjs in s:
    s=s.replace(oldjs,newjs,1)

p.write_text(s)
