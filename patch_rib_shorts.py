from pathlib import Path

p=Path('index.html')
s=p.read_text()

# v69 — stop Shop Women modal freeze.
# The v68 observer watched the same subtree that paint() modified, creating a mutation feedback loop.
# Replace it with click/open lifecycle updates only. Build Your Fit remains untouched.
if 'Women Shop freeze fix v69' not in s:
    css=r'''
<style>/* Women Shop Product Details v69 */
#gbWomenQuick .gb-wq-details{margin-top:16px;border-top:1px solid #2c2c2c;border-bottom:1px solid #2c2c2c}
#gbWomenQuick .gb-wq-details summary{list-style:none;display:flex;align-items:center;justify-content:space-between;gap:12px;padding:13px 2px;cursor:pointer;font-size:.74rem;font-weight:900;text-transform:uppercase;letter-spacing:.09em;color:#f0f0f0}
#gbWomenQuick .gb-wq-details summary::-webkit-details-marker{display:none}
#gbWomenQuick .gb-wq-details summary:after{content:'+';color:var(--gold-light);font-size:1.2rem;line-height:1}
#gbWomenQuick .gb-wq-details[open] summary:after{content:'−'}
#gbWomenQuick .gb-wq-details-body{padding:0 2px 14px;color:#c5c5c5;font-size:.79rem;line-height:1.55}
#gbWomenQuick .gb-wq-details-body ul{margin:0;padding-left:18px}
#gbWomenQuick .gb-wq-details-body li+li{margin-top:5px}
</style>
'''
    js=r'''
<script>/* Women Shop freeze fix v69 */
(function(){
 const leggings=['Runs small; consider sizing up.','83% Polyester, 17% Spandex.','Skinny fit.','Outside seam thread is color-matched.','Interior seam thread is white.','Double-layer waistband.','Slightly see-through when stretched; undyed white may show at seams and sewn areas.','Assembled in the USA from globally sourced parts.'];
 const shorts=['100% polyester.','Medium-heavy fabric: 8.5 oz/yd² (290 g/m²).','Printed-in size and care label.','Seam thread is automatically matched to the design in black or white.','Assembled in the USA from globally sourced parts.'];
 function norm(v){return (v||'').replace(/\s+/g,' ').trim()}
 function verified(name){name=norm(name);if(/^(Cream|Oxblood|Onyx|Bougie Houndstooth|Vault|Heritage Plaid) Leggings$/.test(name))return leggings;if(/^(Cream|Oxblood|Onyx|Bougie Houndstooth|Vault|Heritage Plaid) Workout Shorts$/.test(name))return shorts;return null}
 function ensureBox(){
  const copy=document.querySelector('#gbWomenQuick .gb-wq-copy');if(!copy)return null;
  let d=document.getElementById('gbWqDetailsV69');
  // Hide the v68 box so its old observer has nothing new to rewrite.
  const old=document.getElementById('gbWqDetails');if(old)old.hidden=true;
  if(!d){d=document.createElement('details');d.id='gbWqDetailsV69';d.className='gb-wq-details';d.innerHTML='<summary>Product Details</summary><div class="gb-wq-details-body" id="gbWqDetailsBodyV69"></div>';const add=document.getElementById('gbWqAdd');if(add)copy.insertBefore(d,add);else copy.appendChild(d)}
  return d
 }
 function paint(){
  const modal=document.getElementById('gbWomenQuick'),name=document.getElementById('gbWqName');if(!modal||!name)return;
  const d=ensureBox();if(!d)return;const info=verified(name.textContent);d.open=false;
  if(!info){d.hidden=true;return}d.hidden=false;
  const body=document.getElementById('gbWqDetailsBodyV69');if(body)body.innerHTML='<ul>'+info.map(function(x){return '<li>'+x+'</li>'}).join('')+'</ul>'
 }
 function install(){
  // Crucially: no MutationObserver here. Update only when View Item is intentionally opened.
  document.addEventListener('click',function(e){if(e.target.closest('#gbWomenGrid .gb-women-view'))setTimeout(paint,0)},true);
 }
 if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',install);else install();
})();
</script>
'''
    s=s.replace('</head>',css+'\n</head>')
    s=s.replace('</body>',js+'\n</body>')

p.write_text(s)
