from pathlib import Path
p=Path('index.html')
s=p.read_text()
if 'id="build-your-fit"' not in s: raise SystemExit('Build Your Fit not present')

# v30: Cream Leggings real front/back + product details for first complete Signature Fit.
# Preserve all Build Your Fit viewer/compositor geometry.
css=r'''
/* Build Your Fit — Signature Fit product details v30 */
#build-your-fit .byf-product-details{margin-top:11px;border-top:1px solid rgba(217,161,30,.28);padding-top:9px}
#build-your-fit .byf-product-details summary{cursor:pointer;color:#f4d06f;font-weight:800;font-size:.88rem;letter-spacing:.03em;list-style:none;user-select:none}
#build-your-fit .byf-product-details summary::-webkit-details-marker{display:none}
#build-your-fit .byf-product-details summary:before{content:'+ ';color:#d9a11e}
#build-your-fit .byf-product-details[open] summary:before{content:'− '}
#build-your-fit .byf-product-details-body{padding:10px 0 2px;color:#ddd;font-size:.84rem;line-height:1.5}
#build-your-fit .byf-product-details-body p{margin:0 0 7px}
#build-your-fit .byf-product-details-body ul{margin:6px 0 0;padding-left:18px}
#build-your-fit .byf-product-details-body .byf-warning{color:#f4d06f;font-weight:800}
#build-your-fit .byf-bottom-real-product-pair{display:none;position:absolute;right:0;top:50%;transform:translateY(-50%);gap:6px;align-items:center}
#build-your-fit .byf-bottom-real-product-pair.show{display:flex}
#build-your-fit .byf-bottom-real-product-pair img{width:98px;height:98px;object-fit:contain;background:#fff;border-radius:10px;border:1px solid rgba(217,161,30,.55);padding:3px}
@media(max-width:560px){#build-your-fit .byf-bottom-real-product-pair img{width:72px;height:72px}#build-your-fit .byf-product-details-body{font-size:.8rem}}
'''
if '/* Build Your Fit — Signature Fit product details v30 */' not in s:
    s=s.replace('</style>',css+'\n</style>',1)

# Add Oxblood bra details after top sizes, before its real product pair.
top_sizes='<div class="byf-sizes" id="byfTopSizes"></div>'
top_details='''<div class="byf-sizes" id="byfTopSizes"></div><details class="byf-product-details" id="byfTopDetails"><summary>Product Details</summary><div class="byf-product-details-body"><p><strong>Oxblood Sports Bra</strong> — rich Oxblood red with gold GB front detail and signature gold crown + “What Hustle Looks Like” back detail.</p><ul><li>Material: 100% polyester</li><li>U-shaped back</li><li>Designed for training and everyday wear</li><li>Made to order</li><li>Size tolerance up to 1.2 in (3 cm)</li></ul></div></details>'''
if top_sizes in s and 'id="byfTopDetails"' not in s:
    s=s.replace(top_sizes,top_details,1)

# Add Cream Leggings real front/back and details after bottom sizes.
bottom_sizes='<div class="byf-sizes" id="byfBottomSizes"></div>'
bottom_details='''<div class="byf-sizes" id="byfBottomSizes"></div><details class="byf-product-details" id="byfBottomDetails"><summary>Product Details</summary><div class="byf-product-details-body"><p><strong>Cream High-Waisted Leggings</strong> — soft Cream foundation with understated gold Gangster Bougie detailing.</p><p class="byf-warning">Runs small — consider sizing up.</p><ul><li>83% polyester, 17% spandex</li><li>Skinny fit</li><li>Double-layer waistband</li><li>Outside seam thread is colour-matched to design</li><li>Interior white seam thread</li><li>Slightly see-through when stretched; undyed white material may become visible at seams or where sewn</li><li>Assembled in the USA from globally sourced parts</li><li>Made to order</li></ul></div></details><div class="byf-bottom-real-product-pair" id="byfBottomRealProductPair"><img src="IMG_0553.jpeg" alt="Cream Leggings front"><img src="IMG_0554.jpeg" alt="Cream Leggings back"></div>'''
if bottom_sizes in s and 'id="byfBottomRealProductPair"' not in s:
    s=s.replace(bottom_sizes,bottom_details,1)

# Show details only for products whose verified Printify details were supplied.
# Show Cream real-product pair only when Cream Leggings is selected.
needle="const rpp=document.getElementById('byfTopRealProductPair');if(rpp){rpp.classList.toggle('show',tops[ti][0]==='Oxblood Sports Bra')}}"
repl="const rpp=document.getElementById('byfTopRealProductPair');if(rpp){rpp.classList.toggle('show',tops[ti][0]==='Oxblood Sports Bra')}const td=document.getElementById('byfTopDetails');if(td){td.style.display=tops[ti][0]==='Oxblood Sports Bra'?'block':'none';if(tops[ti][0]!=='Oxblood Sports Bra')td.open=false}const brp=document.getElementById('byfBottomRealProductPair');if(brp){brp.classList.toggle('show',bottomName==='Cream Leggings')}const bd=document.getElementById('byfBottomDetails');if(bd){bd.style.display=bottomName==='Cream Leggings'?'block':'none';if(bottomName!=='Cream Leggings')bd.open=false}}"
if needle in s and "brp.classList.toggle('show',bottomName==='Cream Leggings')" not in s:
    s=s.replace(needle,repl,1)

p.write_text(s)
