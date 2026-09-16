from pathlib import Path
import re

p=Path('index.html')
s=p.read_text()

# v81 — exactly one cart icon where requested.
# 1) Carousel/product-detail windows already have their own native cart icon: remove the extra
#    emoji inserted by v80 from ordinary Add to Cart buttons.
# 2) Build Your Fit's Add Both to Cart gets one cart icon.
# No purchase logic, layout, product data, images, details, filters, or builder geometry changes.

# Remove v80 runtime injector so it cannot re-add duplicate icons.
s=re.sub(r'<script>/\* Global Add to Cart icons v80 \*/.*?</script>\s*','',s,flags=re.S)

# Remove only the v80 emoji prefix from ordinary Add to Cart labels, preserving existing/native
# cart artwork or symbols already supplied by those product windows.
s=s.replace('🛒&nbsp;&nbsp;ADD TO CART','ADD TO CART')
s=s.replace('🛒&nbsp;&nbsp;Add to Cart','Add to Cart')
s=s.replace('🛒  ADD TO CART','ADD TO CART')
s=s.replace('🛒  Add to Cart','Add to Cart')
s=s.replace('🛒 ADD TO CART','ADD TO CART')
s=s.replace('🛒 Add to Cart','Add to Cart')

# Normalize Build Your Fit purchase label to exactly one cart icon.
# Cover static HTML and JS-generated variants without touching its click handler.
s=re.sub(r'>(?:\s*🛒\s*)?Add Both to Cart\s*</button>', '>🛒&nbsp;&nbsp;Add Both to Cart</button>', s, flags=re.I)
s=re.sub(r"(['\"])(?:🛒\s*)?Add Both to Cart\1", lambda m:m.group(1)+'🛒  Add Both to Cart'+m.group(1), s, flags=re.I)

# If the native button text is generated later, scope the fallback ONLY to the Build Your Fit
# combined-purchase button. No site-wide scanning and no carousel/product-window changes.
if 'Build Your Fit cart icon v81' not in s:
    js=r'''<script>/* Build Your Fit cart icon v81 */
(function(){
 function apply(){
  var candidates=document.querySelectorAll('#build-your-fit button');
  candidates.forEach(function(b){
   var t=(b.textContent||'').replace(/\s+/g,' ').trim();
   if(/^add both to cart$/i.test(t))b.textContent='🛒  '+t;
  });
 }
 if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',apply,{once:true});else apply();
 document.addEventListener('click',function(e){
  if(e.target.closest('#build-your-fit'))setTimeout(apply,0);
 },false);
})();
</script>
'''
    s=s.replace('</body>',js+'\n</body>',1)

p.write_text(s)
