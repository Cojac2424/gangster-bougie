from pathlib import Path
import re

p=Path('index.html')
s=p.read_text()
if 'id="build-your-fit"' not in s: raise SystemExit('Build Your Fit not present')

# v38 — working site cart. No Build Your Fit compositor/viewer geometry changes.
# Keep v37's removal of redundant View Items.
s=re.sub(r'\s*<button[^>]*id="byfViewProducts"[^>]*>.*?</button>','',s,flags=re.S|re.I)
s=re.sub(r'\s*const viewProducts=document\.getElementById\([\'\"]byfViewProducts[\'\"]\);\s*if\(viewProducts\)viewProducts\.onclick=\(\)=>\{.*?\};','',s,flags=re.S)

# Ensure the header Cart control has a stable hook while preserving its existing appearance.
s=re.sub(r'(<a\b[^>]*class="[^"]*cart-link[^"]*"[^>]*)(>)',lambda m:m.group(1)+(' id="gbCartLink"' if 'id=' not in m.group(1) else '')+m.group(2),s,count=1,flags=re.I)

# Add the cart drawer once.
if 'id="gbCartDrawer"' not in s:
    drawer='''\n<div class="gb-cart-overlay" id="gbCartOverlay" aria-hidden="true"></div>
<aside class="gb-cart-drawer" id="gbCartDrawer" aria-hidden="true" aria-label="Shopping cart">
 <div class="gb-cart-head"><div><div class="gb-cart-kicker">Gangster Bougie</div><h2>Your Cart</h2></div><button type="button" class="gb-cart-close" id="gbCartClose" aria-label="Close cart">×</button></div>
 <div class="gb-cart-lines" id="gbCartLines"></div>
 <div class="gb-cart-empty" id="gbCartEmpty">Your cart is empty.</div>
 <div class="gb-cart-footer" id="gbCartFooter">
  <div class="gb-cart-subtotal"><span>Subtotal</span><strong id="gbCartSubtotal">US$0.00</strong></div>
  <p>Shipping and taxes are calculated at checkout.</p>
  <button type="button" class="gb-cart-checkout" id="gbCartCheckout">Checkout</button>
 </div>
</aside>\n'''
    s=s.replace('</body>',drawer+'</body>')

if 'Gangster Bougie cart v38' not in s:
    css='''\n<style>/* Gangster Bougie cart v38 */
.gb-cart-overlay{position:fixed;inset:0;background:rgba(0,0,0,.72);z-index:190;opacity:0;pointer-events:none;transition:opacity .2s}.gb-cart-overlay.open{opacity:1;pointer-events:auto}.gb-cart-drawer{position:fixed;right:0;top:0;width:min(440px,94vw);height:100dvh;background:#090909;border-left:1px solid rgba(216,169,40,.5);z-index:200;transform:translateX(105%);transition:transform .25s ease;display:flex;flex-direction:column;box-shadow:-12px 0 35px rgba(0,0,0,.55)}.gb-cart-drawer.open{transform:translateX(0)}.gb-cart-head{display:flex;align-items:center;justify-content:space-between;padding:22px;border-bottom:1px solid #282828}.gb-cart-head h2{font-family:'Bodoni Moda',serif;color:#f4cf63;text-transform:uppercase;font-size:1.65rem}.gb-cart-kicker{text-transform:uppercase;letter-spacing:.14em;font-size:.65rem;color:#aaa;font-weight:800}.gb-cart-close{width:42px;height:42px;border:1px solid #d8a928;border-radius:50%;background:#111;color:#f4cf63;font-size:1.65rem;cursor:pointer}.gb-cart-lines{overflow:auto;padding:10px 20px;flex:1}.gb-cart-line{padding:16px 0;border-bottom:1px solid #242424}.gb-cart-line-top{display:flex;justify-content:space-between;gap:16px}.gb-cart-line-name{font-weight:900}.gb-cart-line-size{font-size:.82rem;color:#aaa;margin-top:3px}.gb-cart-line-price{color:#f4cf63;font-weight:900;white-space:nowrap}.gb-cart-line-actions{display:flex;align-items:center;justify-content:space-between;margin-top:12px}.gb-cart-qty{display:flex;align-items:center;border:1px solid #444;border-radius:6px;overflow:hidden}.gb-cart-qty button{width:36px;height:34px;border:0;background:#151515;color:#fff;cursor:pointer;font-size:1.15rem}.gb-cart-qty span{min-width:36px;text-align:center;font-weight:800}.gb-cart-remove{border:0;background:transparent;color:#bbb;text-decoration:underline;cursor:pointer;font-size:.78rem}.gb-cart-empty{display:none;padding:34px 22px;color:#bbb;text-align:center}.gb-cart-footer{padding:18px 22px 24px;border-top:1px solid #282828}.gb-cart-subtotal{display:flex;justify-content:space-between;font-size:1.05rem;margin-bottom:7px}.gb-cart-subtotal strong{color:#f4cf63}.gb-cart-footer p{font-size:.75rem;color:#888;margin-bottom:14px}.gb-cart-checkout{width:100%;padding:15px;border:0;border-radius:7px;background:linear-gradient(135deg,#f6d56c,#d8a928);color:#111;font-weight:900;text-transform:uppercase;letter-spacing:.06em;cursor:pointer}.gb-cart-checkout:disabled{opacity:.45;cursor:not-allowed}
</style>\n'''
    s=s.replace('</head>',css+'</head>')

# Add one cart controller. It deliberately uses the existing gbCart localStorage data.
s=re.sub(r'\n?<script>\s*/\* Gangster Bougie cart controller v38 \*/.*?</script>\s*','\n',s,flags=re.S)
cartjs='''\n<script>/* Gangster Bougie cart controller v38 */
(function(){
 const KEY='gbCart';
 const link=document.getElementById('gbCartLink')||document.querySelector('.cart-link');
 const drawer=document.getElementById('gbCartDrawer'),overlay=document.getElementById('gbCartOverlay'),close=document.getElementById('gbCartClose');
 const lines=document.getElementById('gbCartLines'),empty=document.getElementById('gbCartEmpty'),footer=document.getElementById('gbCartFooter'),subtotal=document.getElementById('gbCartSubtotal'),checkout=document.getElementById('gbCartCheckout');
 function read(){try{return JSON.parse(localStorage.getItem(KEY)||'[]')}catch(e){return []}}
 function write(c){localStorage.setItem(KEY,JSON.stringify(c));render()}
 function price(x){if(typeof x.price==='number')return x.price;var m=String(x.price||'').match(/[0-9]+(?:\.[0-9]+)?/);return m?Number(m[0]):0}
 function count(c){return c.reduce((n,x)=>n+(Number(x.qty)||1),0)}
 function render(){
  const c=read(),n=count(c); if(link)link.textContent='CART ('+n+')';
  if(!lines)return; lines.innerHTML=''; let total=0;
  c.forEach(function(x,i){const q=Number(x.qty)||1,p=price(x);total+=p*q;const row=document.createElement('div');row.className='gb-cart-line';row.innerHTML='<div class="gb-cart-line-top"><div><div class="gb-cart-line-name"></div><div class="gb-cart-line-size"></div></div><div class="gb-cart-line-price"></div></div><div class="gb-cart-line-actions"><div class="gb-cart-qty"><button type="button" data-cart-action="minus" data-i="'+i+'">−</button><span>'+q+'</span><button type="button" data-cart-action="plus" data-i="'+i+'">+</button></div><button type="button" class="gb-cart-remove" data-cart-action="remove" data-i="'+i+'">Remove</button></div>';row.querySelector('.gb-cart-line-name').textContent=x.name||'Gangster Bougie Item';row.querySelector('.gb-cart-line-size').textContent='Size: '+(x.size||'—');row.querySelector('.gb-cart-line-price').textContent='US$'+(p*q).toFixed(2);lines.appendChild(row)});
  if(subtotal)subtotal.textContent='US$'+total.toFixed(2);if(empty)empty.style.display=c.length?'none':'block';if(footer)footer.style.display=c.length?'block':'none';if(checkout)checkout.disabled=!c.length;
 }
 function openCart(e){if(e)e.preventDefault();render();drawer&&drawer.classList.add('open');overlay&&overlay.classList.add('open');drawer&&drawer.setAttribute('aria-hidden','false');overlay&&overlay.setAttribute('aria-hidden','false')}
 function closeCart(){drawer&&drawer.classList.remove('open');overlay&&overlay.classList.remove('open');drawer&&drawer.setAttribute('aria-hidden','true');overlay&&overlay.setAttribute('aria-hidden','true')}
 if(link)link.addEventListener('click',openCart);if(close)close.addEventListener('click',closeCart);if(overlay)overlay.addEventListener('click',closeCart);
 if(lines)lines.addEventListener('click',function(e){const b=e.target.closest('[data-cart-action]');if(!b)return;const i=Number(b.dataset.i),c=read(),a=b.dataset.cartAction;if(!c[i])return;if(a==='plus')c[i].qty=(Number(c[i].qty)||1)+1;if(a==='minus'){c[i].qty=(Number(c[i].qty)||1)-1;if(c[i].qty<=0)c.splice(i,1)}if(a==='remove')c.splice(i,1);write(c)});
 // Checkout is intentionally not wired to fulfillment yet; don't fake an order submission.
 if(checkout)checkout.addEventListener('click',function(){alert('Checkout setup is the next step. Your cart is saved.');});
 window.gbCartRefresh=render;
 window.addEventListener('storage',render);
 document.addEventListener('click',function(e){if(e.target&&e.target.id==='byfAddFit')setTimeout(render,0)},true);
 render();
})();
</script>\n'''
s=s.replace('</body>',cartjs+'</body>')

p.write_text(s)
