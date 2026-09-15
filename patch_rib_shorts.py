from pathlib import Path

p=Path('index.html')
s=p.read_text()

# v45 — add a secondary Clear Cart control. Cart behavior only; no Build Your Fit geometry changes.
if 'Clear Cart control v45' not in s:
    css='''
<style>/* Clear Cart control v45 */
.gb-cart-clear{display:block;margin:0 0 12px auto;padding:7px 0;border:0;background:transparent;color:#aaa;text-decoration:underline;text-underline-offset:3px;font:inherit;font-size:.78rem;cursor:pointer}
.gb-cart-clear:hover,.gb-cart-clear:focus{color:#fff}
</style>
'''
    s=s.replace('</head>',css+'</head>')
    js=r'''
<script>/* Clear Cart control v45 */
(function(){
 const KEY='gbCart';
 function install(){
  const footer=document.getElementById('gbCartFooter');
  if(!footer||document.getElementById('gbCartClear'))return;
  const b=document.createElement('button');
  b.type='button'; b.id='gbCartClear'; b.className='gb-cart-clear'; b.textContent='Clear Cart';
  b.addEventListener('click',function(){
   const cart=(()=>{try{return JSON.parse(localStorage.getItem(KEY)||'[]')}catch(e){return []}})();
   if(!cart.length)return;
   if(!window.confirm('Remove all items from your cart?'))return;
   localStorage.setItem(KEY,'[]');
   if(window.gbCartRefresh)window.gbCartRefresh();
   else window.dispatchEvent(new Event('storage'));
  });
  const subtotal=footer.querySelector('.gb-cart-subtotal');
  footer.insertBefore(b,subtotal||footer.firstChild);
 }
 if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',install);else install();
})();
</script>
'''
    s=s.replace('</body>',js+'</body>')

p.write_text(s)
