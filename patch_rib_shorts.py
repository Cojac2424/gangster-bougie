from pathlib import Path
import re

p=Path('index.html')
s=p.read_text()

# v80 — site-wide shopping cart icon for purchase buttons.
# Appearance-only enhancement: prepend the cart symbol to every button whose visible action
# is Add to Cart. No cart logic, product data, Build Your Fit geometry, modal behavior,
# filters, images, sizing, or Product Details code is changed.

# Static HTML buttons: normalize to exactly one cart symbol.
s=re.sub(r'>(?:\s*🛒\s*)?ADD TO CART\s*</button>', '>🛒&nbsp;&nbsp;ADD TO CART</button>', s, flags=re.I)
s=re.sub(r'>(?:\s*🛒\s*)?Add to Cart\s*</button>', '>🛒&nbsp;&nbsp;Add to Cart</button>', s)

# JavaScript-generated labels / innerHTML / textContent: keep one icon when buttons are rebuilt.
s=re.sub(r"(['\"])(?:🛒\s*)?ADD TO CART\1", lambda m:m.group(1)+'🛒  ADD TO CART'+m.group(1), s)
s=re.sub(r"(['\"])(?:🛒\s*)?Add to Cart\1", lambda m:m.group(1)+'🛒  Add to Cart'+m.group(1), s)

# Defensive, idempotent runtime pass for any Add to Cart buttons generated later by existing
# product controllers. One delegated click-independent scan at DOM ready; no observers.
if 'Global Add to Cart icons v80' not in s:
    js=r'''<script>/* Global Add to Cart icons v80 */
(function(){
 function apply(root){
  (root||document).querySelectorAll('button').forEach(function(b){
   var t=(b.textContent||'').replace(/\s+/g,' ').trim();
   if(/^🛒\s*/.test(t))return;
   if(/^add to cart$/i.test(t))b.textContent='🛒  '+t;
  });
 }
 if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',function(){apply(document)},{once:true});else apply(document);
 // Existing product windows can rebuild their button labels when opened. Re-apply from the
 // same global delegated event instead of attaching listeners to individual products.
 document.addEventListener('click',function(e){
  if(e.target.closest('[data-open],.view-item,.gb-women-view,[class*="view-item"],[class*="open"]'))setTimeout(function(){apply(document)},0);
 },false);
})();
</script>
'''
    s=s.replace('</body>',js+'\n</body>',1)

p.write_text(s)
