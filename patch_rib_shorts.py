from pathlib import Path
import re

p=Path('index.html')
s=p.read_text()

# v78 — Shop Women Product Details, integrated into the ONE native quick-view controller.
# No MutationObserver, no modal cloning, no per-card listeners, no duplicate controller.
# Reuse the existing Build Your Fit Product Details as the single source of truth.
# Preserve v72+ freeze protection, v76 image orientation, v77 Build Your Fit default/geometry.

# Add one permanent details element to the existing quick-view modal, after sizes and before Add to Cart.
old='<div class="gb-wq-sizes" id="gbWqSizes"></div><button class="gb-wq-add" id="gbWqAdd">Add to Cart</button>'
new='<div class="gb-wq-sizes" id="gbWqSizes"></div><details class="gb-wq-details" id="gbWqDetails"><summary>Product Details</summary><div class="gb-wq-details-body" id="gbWqDetailsBody"></div></details><button class="gb-wq-add" id="gbWqAdd">Add to Cart</button>'
if old in s:s=s.replace(old,new,1)

# Style only the new dropdown. Closed by default; no layout changes elsewhere.
if 'Women Shop Product Details stable v78' not in s:
    css='''\n<style>/* Women Shop Product Details stable v78 */
#gbWomenQuick .gb-wq-details{margin:18px 0 4px;border-top:1px solid rgba(216,169,40,.34);border-bottom:1px solid rgba(216,169,40,.34);padding:0}
#gbWomenQuick .gb-wq-details summary{list-style:none;cursor:pointer;padding:14px 2px;color:#f4cf63;font-weight:900;text-transform:uppercase;letter-spacing:.09em;font-size:.78rem;display:flex;align-items:center;justify-content:space-between}
#gbWomenQuick .gb-wq-details summary::-webkit-details-marker{display:none}
#gbWomenQuick .gb-wq-details summary:after{content:'+';font-size:1.25rem;line-height:1}
#gbWomenQuick .gb-wq-details[open] summary:after{content:'−'}
#gbWomenQuick .gb-wq-details-body{padding:2px 2px 15px;color:#d1d1d1;font-size:.86rem;line-height:1.55}
#gbWomenQuick .gb-wq-details-body p{margin:0 0 10px}
#gbWomenQuick .gb-wq-details-body ul{margin:4px 0 10px 20px;padding:0}
#gbWomenQuick .gb-wq-details-body li{margin:3px 0}
</style>\n'''
    s=s.replace('</head>',css+'</head>',1)

# Add a single reusable details bridge immediately before the native Women Shop controller.
# It reads the existing Build Your Fit mappings at open time, without observers.
marker='<script>/* Women Shop preview catalog v63 */'
if 'Women Shop details bridge v78' not in s and marker in s:
    bridge=r'''<script>/* Women Shop details bridge v78 */
(function(){
 window.gbWomenDetailsFor=function(name){
  name=(name||'').trim();
  // Classic details: mirror the existing Build Your Fit Classic mapping exactly.
  var m=name.match(/^GB Classic (Sports Bra|High-Waisted Leggings) – (Cream|Grey|Black|Blue|Green|Red|Espresso)$/);
  if(m){
   var kind=m[1],c=m[2];
   var tone={Cream:'a refined cream',Grey:'a sleek grey',Black:'a sleek black',Blue:'a rich blue',Green:'a rich green',Red:'a bold red',Espresso:'a rich espresso-brown'}[c];
   if(kind==='Sports Bra')return '<p>Luxury meets performance. The GB Classic Sports Bra combines '+tone+' athletic silhouette with signature gold lattice detailing and the crowned GB emblem for an elevated Gangster Bougie look.</p><ul><li>100% polyester</li><li>U-shaped back</li><li>Size tolerance up to 1.2 in (3 cm)</li><li>Made to order</li></ul>';
   return '<p>Luxury meets performance. The GB Classic High-Waisted Leggings combine '+tone+' silhouette with signature gold lattice detailing running down the outer legs and the crowned GB emblem for an elevated Gangster Bougie look.</p><ul><li>83% polyester, 17% spandex</li><li>Skinny fit</li><li>Double-layer waistband</li><li>Runs small — consider sizing up</li><li>Outside seam thread is colour-matched to the design</li><li>Interior seam thread is white</li><li>Slightly see-through when stretched; undyed white may show at seams and sewn areas</li><li>Assembled in the USA from globally sourced parts</li><li>Made to order</li></ul>';
  }
  // Signature products: copy the already-rendered Build Your Fit details when the selected
  // product is the same. The native Build Your Fit scripts remain the source of truth.
  var top=document.getElementById('byfShopTopName'),bottom=document.getElementById('byfShopBottomName');
  if(top && top.textContent.trim()===name){var d=document.querySelector('#byfTopDetails .byf-details-body');if(d)return d.innerHTML}
  if(bottom && bottom.textContent.trim()===name){var d2=document.querySelector('#byfBottomDetails .byf-details-body');if(d2)return d2.innerHTML}
  // Shared verified technical details for Signature categories when the current builder
  // selection differs from the Shop Women item.
  if(/Leggings$/.test(name))return '<p><strong>Runs small — consider sizing up.</strong></p><ul><li>83% polyester, 17% spandex</li><li>Skinny fit</li><li>Outside seam thread is colour-matched to the design</li><li>Interior seam thread is white</li><li>Double-layer waistband</li><li>Slightly see-through when stretched; undyed white may show at seams or sewn areas</li><li>Assembled in the USA from globally sourced parts</li><li>Made to order</li></ul>';
  if(/Workout Shorts$/.test(name))return '<ul><li>100% polyester</li><li>Medium-heavy fabric: 8.5 oz/yd² (290 g/m²)</li><li>Printed-in size and care label</li><li>Seam thread automatically colour-matched to the design (black or white)</li><li>Assembled in the USA from globally sourced parts</li><li>Made to order</li></ul>';
  if(/Sports Bra$/.test(name))return '<ul><li>100% polyester</li><li>U-shaped back</li><li>Size tolerance up to 1.2 in (3 cm)</li><li>Made to order</li></ul>';
  return '<p>Made to order.</p>';
 };
})();
</script>
'''
    s=s.replace(marker,bridge+marker,1)

# Integrate directly into native openQuick. This executes once per View Item open and cannot loop.
# Find the stable line that fills the sizes, then append details rendering.
size_line="sizes.innerHTML='';current[3].forEach(s=>{const b=document.createElement('button');b.textContent=s;b.onclick=()=>{[...sizes.children].forEach(x=>x.classList.remove('active'));b.classList.add('active');selectedSize=s};sizes.appendChild(b)});"
add="""sizes.innerHTML='';current[3].forEach(s=>{const b=document.createElement('button');b.textContent=s;b.onclick=()=>{[...sizes.children].forEach(x=>x.classList.remove('active'));b.classList.add('active');selectedSize=s};sizes.appendChild(b)});var det=document.getElementById('gbWqDetails'),detBody=document.getElementById('gbWqDetailsBody');if(det){det.open=false;if(detBody)detBody.innerHTML=window.gbWomenDetailsFor?window.gbWomenDetailsFor(current[0]):'<p>Made to order.</p>';}"""
if size_line in s:s=s.replace(size_line,add,1)

# If native code has a slightly different whitespace/minified form, insert after selectedSize reset/open fields.
if "window.gbWomenDetailsFor(current[0])" not in s:
    pat=re.compile(r"(function openQuick\(i\)\{.*?sizes\.innerHTML='';.*?current\[3\]\.forEach\(.*?\}\);)",re.S)
    mm=pat.search(s)
    if mm:
        ins="var det=document.getElementById('gbWqDetails'),detBody=document.getElementById('gbWqDetailsBody');if(det){det.open=false;if(detBody)detBody.innerHTML=window.gbWomenDetailsFor?window.gbWomenDetailsFor(current[0]):'<p>Made to order.</p>';}"
        s=s[:mm.end()]+ins+s[mm.end():]

p.write_text(s)
