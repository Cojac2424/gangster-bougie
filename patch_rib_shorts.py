from pathlib import Path

p=Path('index.html')
s=p.read_text()

# v64 — homepage hierarchy refinement.
# Rollback reference: 42d2253b6833446c40daedf24a2c9580a8c9c9ba is the approved pre-catalog state.
# Keeps all proven Build Your Fit geometry untouched.
if 'Homepage hierarchy v64' not in s:
    css=r'''
<style>/* Homepage hierarchy v64 */
.nav-links .byf-nav-link{position:relative;overflow:hidden;border:1px solid var(--gold);border-radius:999px;padding:9px 13px;color:var(--gold-light);white-space:nowrap;box-shadow:0 0 0 rgba(244,207,99,0)}
.nav-links .byf-nav-link::after{content:'';position:absolute;inset:-45% auto -45% -45%;width:32%;transform:skewX(-20deg);background:linear-gradient(90deg,transparent,rgba(255,245,185,.8),transparent);animation:gbByfShine 5.5s ease-in-out infinite;pointer-events:none}
@keyframes gbByfShine{0%,72%{left:-45%;opacity:0}76%{opacity:1}91%{left:125%;opacity:1}100%{left:125%;opacity:0}}
#gbWomenCatalog .gb-women-more-wrap{text-align:center;margin-top:24px}
#gbWomenCatalog .gb-women-more{padding:12px 22px;border:1px solid var(--gold);background:transparent;color:var(--gold-light);font-weight:900;text-transform:uppercase;letter-spacing:.09em;cursor:pointer}
#gbWomenCatalog .gb-women-card.gb-women-collapsed{display:none!important}
@media(max-width:760px){.nav-links .byf-nav-link{padding:8px 10px;font-size:.68rem}.nav{gap:8px}.nav-links{gap:9px}}
@media(prefers-reduced-motion:reduce){.nav-links .byf-nav-link::after{animation:none}}
</style>
'''
    js=r'''
<script>/* Homepage hierarchy v64 */
(function(){
 function install(){
  const nav=document.querySelector('.nav-links');
  if(nav&&!nav.querySelector('.byf-nav-link')){
   const cart=nav.querySelector('#gbCartLink');
   const a=document.createElement('a');a.className='byf-nav-link';a.href='#build-your-fit';a.textContent='Build Your Fit';
   nav.insertBefore(a,cart||null);
  }
  const byf=document.getElementById('build-your-fit'),catalog=document.getElementById('gbWomenCatalog');
  if(byf&&catalog&&byf.parentNode===catalog.parentNode){byf.insertAdjacentElement('afterend',catalog)}
  if(!catalog)return;
  const container=catalog.querySelector('.container'),grid=document.getElementById('gbWomenGrid');
  if(!container||!grid)return;
  let more=container.querySelector('.gb-women-more');
  if(!more){const wrap=document.createElement('div');wrap.className='gb-women-more-wrap';more=document.createElement('button');more.className='gb-women-more';more.type='button';more.textContent='View More';wrap.appendChild(more);grid.insertAdjacentElement('afterend',wrap)}
  let expanded=false;
  function applyLimit(){
   const cards=[...grid.querySelectorAll('.gb-women-card')];
   cards.forEach((card,i)=>card.classList.toggle('gb-women-collapsed',!expanded&&i>=8));
   more.style.display=cards.length>8?'inline-block':'none';
   more.textContent=expanded?'Show Less':'View More';
  }
  more.onclick=function(){expanded=!expanded;applyLimit();if(!expanded)catalog.scrollIntoView({behavior:'smooth',block:'start'})};
  const observer=new MutationObserver(applyLimit);observer.observe(grid,{childList:true});
  catalog.querySelectorAll('.gb-women-filter').forEach(function(b){b.addEventListener('click',function(){expanded=false;setTimeout(applyLimit,0)})});
  applyLimit();
 }
 if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',install);else install();
})();
</script>
'''
    s=s.replace('</head>',css+'\n</head>')
    s=s.replace('</body>',js+'\n</body>')

p.write_text(s)
