from pathlib import Path
import re, json

p=Path('index.html')
s=p.read_text()

# v79 — Product Details bridge fix.
# The dropdown shell from v78 works, but the body population hook did not match the native
# minified openQuick implementation. Fix the connection without observers, cloning, or
# per-card listeners. Existing Build Your Fit details remain the source of truth.

# Ensure the one permanent dropdown exists.
old='<div class="gb-wq-sizes" id="gbWqSizes"></div><button class="gb-wq-add" id="gbWqAdd">Add to Cart</button>'
new='<div class="gb-wq-sizes" id="gbWqSizes"></div><details class="gb-wq-details" id="gbWqDetails"><summary>Product Details</summary><div class="gb-wq-details-body" id="gbWqDetailsBody"></div></details><button class="gb-wq-add" id="gbWqAdd">Add to Cart</button>'
if old in s:s=s.replace(old,new,1)

# Harvest every explicit details:`...` entry already stored in Build Your Fit.
# This makes Shop Women reuse repository content instead of maintaining a second description set.
detail_map={}
for m in re.finditer(r"['\"]([^'\"]+)['\"]\s*:\s*\{(?:(?!\n\s*['\"][^'\"]+['\"]\s*:).)*?details\s*:\s*`(.*?)`",s,re.S):
    name=m.group(1).strip(); body=m.group(2).strip()
    if body and name not in detail_map: detail_map[name]=body

# Add aliases used by Shop Women vs Build Your Fit naming.
for a,b in {
 'Vault High-Waisted Leggings':'Vault Leggings',
 'Heritage Plaid High-Waisted Leggings':'Heritage Plaid Leggings',
 'Bougie Houndstooth High-Waisted Leggings':'Bougie Houndstooth Leggings',
 'Onyx High-Waisted Leggings':'Onyx Leggings',
 'Oxblood High-Waisted Leggings':'Oxblood Leggings',
 'Cream High-Waisted Leggings':'Cream Leggings'
}.items():
    if b in detail_map and a not in detail_map: detail_map[a]=detail_map[b]

# Replace the failed v78 bridge with one deterministic map + Classic resolver.
s=re.sub(r'<script>/\* Women Shop details bridge v78 \*/.*?</script>\s*','',s,flags=re.S)

bridge="""<script>/* Women Shop details bridge v79 */
(function(){
 var existing=%s;
 window.gbWomenDetailsFor=function(name){
  name=(name||'').trim();
  if(existing[name])return existing[name];
  var m=name.match(/^GB Classic (Sports Bra|High-Waisted Leggings) – (Cream|Grey|Black|Blue|Green|Red|Espresso)$/);
  if(m){
   var kind=m[1],c=m[2];
   var tone={Cream:'a refined cream',Grey:'a sleek grey',Black:'a sleek black',Blue:'a rich blue',Green:'a rich green',Red:'a bold red',Espresso:'a rich espresso-brown'}[c];
   if(kind==='Sports Bra')return '<p>Luxury meets performance. The GB Classic Sports Bra combines '+tone+' athletic silhouette with signature gold lattice detailing and the crowned GB emblem for an elevated Gangster Bougie look.</p><ul><li>100%% polyester</li><li>U-shaped back</li><li>Size tolerance up to 1.2 in (3 cm)</li><li>Made to order</li></ul>';
   return '<p>Luxury meets performance. The GB Classic High-Waisted Leggings combine '+tone+' silhouette with signature gold lattice detailing running down the outer legs and the crowned GB emblem for an elevated Gangster Bougie look.</p><ul><li>83%% polyester, 17%% spandex</li><li>Skinny fit</li><li>Double-layer waistband</li><li>Runs small — consider sizing up</li><li>Outside seam thread is colour-matched to the design</li><li>Interior seam thread is white</li><li>Slightly see-through when stretched; undyed white may show at seams and sewn areas</li><li>Assembled in the USA from globally sourced parts</li><li>Made to order</li></ul>';
  }
  return '';
 };
})();
</script>
""" % json.dumps(detail_map,ensure_ascii=False,separators=(',',':'))
marker='<script>/* Women Shop preview catalog v63 */'
if 'Women Shop details bridge v79' not in s and marker in s:s=s.replace(marker,bridge+marker,1)

# Remove any partial v78 inline population fragments so there is one population path.
s=re.sub(r"var det=document\.getElementById\('gbWqDetails'\),detBody=document\.getElementById\('gbWqDetailsBody'\);if\(det\)\{det\.open=false;if\(detBody\)detBody\.innerHTML=window\.gbWomenDetailsFor\?window\.gbWomenDetailsFor\(current\[0\]\):'<p>Made to order\.</p>';\}", '', s)

# One delegated hook for the entire catalogue. It runs after the already-working native View Item
# handler, reads the product name actually placed in the modal, and fills the existing dropdown.
# No MutationObserver and no listener accumulation when filters/View More rerender cards.
s=re.sub(r'<script>/\* Women Shop details population v79 \*/.*?</script>\s*','',s,flags=re.S)
hook=r'''<script>/* Women Shop details population v79 */
(function(){
 if(window.__gbWomenDetailsPopulation79)return;window.__gbWomenDetailsPopulation79=true;
 function populate(){
  var nameEl=document.getElementById('gbWqName'),det=document.getElementById('gbWqDetails'),body=document.getElementById('gbWqDetailsBody');
  if(!nameEl||!det||!body)return;
  det.open=false;
  var html=window.gbWomenDetailsFor?window.gbWomenDetailsFor(nameEl.textContent):'';
  body.innerHTML=html||'<p>Made to order.</p>';
 }
 document.addEventListener('click',function(e){
  if(e.target.closest('#gbWomenGrid .gb-women-view'))setTimeout(populate,0);
 },false);
})();
</script>
'''
s=s.replace('</body>',hook+'\n</body>',1)

# Keep the v78 styling if already present; add it only if missing.
if 'Women Shop Product Details stable v78' not in s:
    css='''<style>/* Women Shop Product Details stable v78 */
#gbWomenQuick .gb-wq-details{margin:18px 0 4px;border-top:1px solid rgba(216,169,40,.34);border-bottom:1px solid rgba(216,169,40,.34);padding:0}
#gbWomenQuick .gb-wq-details summary{list-style:none;cursor:pointer;padding:14px 2px;color:#f4cf63;font-weight:900;text-transform:uppercase;letter-spacing:.09em;font-size:.78rem;display:flex;align-items:center;justify-content:space-between}
#gbWomenQuick .gb-wq-details summary::-webkit-details-marker{display:none}
#gbWomenQuick .gb-wq-details summary:after{content:'+';font-size:1.25rem;line-height:1}
#gbWomenQuick .gb-wq-details[open] summary:after{content:'−'}
#gbWomenQuick .gb-wq-details-body{padding:2px 2px 15px;color:#d1d1d1;font-size:.86rem;line-height:1.55}
#gbWomenQuick .gb-wq-details-body p{margin:0 0 10px}#gbWomenQuick .gb-wq-details-body ul{margin:4px 0 10px 20px;padding:0}#gbWomenQuick .gb-wq-details-body li{margin:3px 0}
</style>'''
    s=s.replace('</head>',css+'</head>',1)

p.write_text(s)
