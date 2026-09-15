from pathlib import Path
import re

p=Path('index.html')
s=p.read_text()
if 'id="build-your-fit"' not in s: raise SystemExit('Build Your Fit not present')

# v37: finish the first Build Your Fit purchasing template without touching compositor geometry.
# Remove the now-redundant View Items button only; View This Fit remains.
s=re.sub(r'\s*<button[^>]*id="byfViewProducts"[^>]*>.*?</button>','',s,flags=re.S|re.I)
# Remove old scroll-to-Shop handler if present.
s=re.sub(r'\s*const viewProducts=document\.getElementById\([\'\"]byfViewProducts[\'\"]\);\s*if\(viewProducts\)viewProducts\.onclick=\(\)=>\{.*?\};','',s,flags=re.S)

# Upgrade existing local cart behavior: retain the site's own cart, store exact product/size/price,
# and make repeated adds update quantities instead of creating confusing duplicate rows.
old="""const cart=JSON.parse(localStorage.getItem('gbCart')||'[]');
cart.push(...items);
localStorage.setItem('gbCart',JSON.stringify(cart));"""
new="""const cart=JSON.parse(localStorage.getItem('gbCart')||'[]');
items.forEach(function(item){
 const hit=cart.find(function(x){return x.name===item.name&&x.size===item.size;});
 if(hit)hit.qty=(hit.qty||1)+1;
 else cart.push(Object.assign({qty:1},item));
});
localStorage.setItem('gbCart',JSON.stringify(cart));"""
if old in s:s=s.replace(old,new)

# Make sure the first approved outfit has its exact real-product content/details in the inline panel.
# Existing v30 elements are reused so the visual architecture stays stable.
oxblood_details='''<details class="byf-product-details" id="byfTopDetails"><summary>Product Details</summary><div class="byf-details-body"><p>Bold, elevated and unmistakably Gangster Bougie. The Gangster Bougie Signature Essentials Oxblood Sports Bra combines a rich Oxblood red foundation with understated gold GB detailing for a luxury-athletic look.</p><p>A gold GB monogram finishes the front, while the signature gold crown and “What Hustle Looks Like” detail marks the back. Designed to stand on its own or mix effortlessly with pieces throughout the GB Signature Collection.</p><ul><li>Rich Oxblood red</li><li>Gold GB front detail</li><li>Gold crown + “What Hustle Looks Like” back detail</li><li>Clean, minimal Signature design</li><li>Designed for training and everyday wear</li><li>Made to coordinate across GB Signature Collection</li><li>Made to order</li></ul><p><strong>Material:</strong> 100% polyester</p><p><strong>Back:</strong> U-shaped back</p><p><strong>Size tolerance:</strong> up to 1.2 in (3 cm)</p></div></details>'''
cream_details='''<details class="byf-product-details" id="byfBottomDetails"><summary>Product Details</summary><div class="byf-details-body"><p>Clean luxury built for movement. The Gangster Bougie Signature Essentials Cream High-Waisted Leggings feature a soft Cream foundation finished with understated gold Gangster Bougie detailing.</p><p>A small gold GB monogram accents the front-left hip, while the signature gold crown finishes the back for a minimal, elevated look designed to coordinate effortlessly across the GB Signature Collection.</p><ul><li>Soft Cream colour</li><li>Gold GB detail at front-left hip</li><li>Signature gold crown at back</li><li>High-waisted silhouette</li><li>Clean, minimal Signature design</li><li>Designed for movement and everyday wear</li><li>Coordinates across GB Signature Collection</li><li>Made to order</li></ul><p><strong>Runs small — consider sizing up.</strong></p><p><strong>Material:</strong> 83% polyester, 17% spandex</p><p><strong>Fit:</strong> Skinny fit; double-layer waistband</p><p>Outside seam thread is colour-matched to the design; interior seam thread is white.</p><p>Slightly see-through when stretched. Some undyed white underneath material may become visible at seams or where sewn.</p><p>Assembled in the USA from globally sourced parts.</p></div></details>'''
s=re.sub(r'<details class="byf-product-details" id="byfTopDetails">.*?</details>',oxblood_details,s,flags=re.S)
s=re.sub(r'<details class="byf-product-details" id="byfBottomDetails">.*?</details>',cream_details,s,flags=re.S)

# Ensure real Oxblood and Cream product pairs are present if earlier versions were partially applied.
if 'id="byfTopRealProductPair"' not in s:
    anchor='<div class="byf-fit-price">US$39.99</div>'
    pair='<div class="byf-real-product-pair" id="byfTopRealProductPair"><img src="IMG_0547.jpeg" alt="Oxblood Sports Bra front" loading="lazy" decoding="async"><img src="IMG_0548.jpeg" alt="Oxblood Sports Bra back" loading="lazy" decoding="async"></div>'
    s=s.replace(anchor,anchor+pair,1)
if 'id="byfBottomRealProductPair"' not in s:
    anchor='<div class="byf-fit-price" id="byfShopBottomPrice"></div>'
    pair='<div class="byf-real-product-pair" id="byfBottomRealProductPair"><img src="IMG_0553.jpeg" alt="Cream High-Waisted Leggings product view 1" loading="lazy" decoding="async"><img src="IMG_0554.jpeg" alt="Cream High-Waisted Leggings product view 2" loading="lazy" decoding="async"></div>'
    s=s.replace(anchor,anchor+pair,1)

# Add safe inline details styling only if absent. No model/viewer selectors are changed.
if 'Build Your Fit product details v37' not in s:
    css='''\n<style>/* Build Your Fit product details v37 */
#build-your-fit .byf-product-details{margin-top:14px;border-top:1px solid rgba(216,169,40,.28);padding-top:10px;text-align:left}
#build-your-fit .byf-product-details summary{cursor:pointer;color:#f4cf63;font-weight:900;text-transform:uppercase;letter-spacing:.08em;font-size:.76rem;list-style:none}
#build-your-fit .byf-product-details summary::-webkit-details-marker{display:none}
#build-your-fit .byf-product-details summary:after{content:' +';float:right}
#build-your-fit .byf-product-details[open] summary:after{content:' −'}
#build-your-fit .byf-details-body{padding-top:10px;color:#d2d2d2;font-size:.84rem;line-height:1.5}
#build-your-fit .byf-details-body p{margin:0 0 9px}
#build-your-fit .byf-details-body ul{margin:0 0 10px 18px;padding:0}
#build-your-fit .byf-real-product-pair{display:flex;gap:8px;margin-top:10px;max-width:190px}
#build-your-fit .byf-real-product-pair img{width:calc(50% - 4px);aspect-ratio:1;object-fit:cover;background:#eee;border-radius:6px}
</style>\n'''
    s=s.replace('</head>',css+'</head>')

p.write_text(s)
