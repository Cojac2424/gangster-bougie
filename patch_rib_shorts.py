from pathlib import Path

p=Path('index.html')
s=p.read_text()

# v67 — Women Shop product image correction.
# Uses the already-confirmed Printify front/back mapping, without touching Build Your Fit geometry.
if 'Women Shop front-back correction v67' not in s:
    js=r'''
<script>/* Women Shop front-back correction v67 */
(function(){
 const products={
  'GB Classic Sports Bra – Cream':['IMG_0589.jpeg','IMG_0590.jpeg'],
  'GB Classic Sports Bra – Grey':['IMG_0586.jpeg','IMG_0588.jpeg'],
  'GB Classic Sports Bra – Black':['IMG_0597.jpeg','IMG_0598.jpeg'],
  'GB Classic Sports Bra – Blue':['IMG_0591.jpeg','IMG_0592.jpeg'],
  'GB Classic Sports Bra – Green':['IMG_0595.jpeg','IMG_0596.jpeg'],
  'GB Classic Sports Bra – Red':['IMG_0593.jpeg','IMG_0594.jpeg'],
  'GB Classic Sports Bra – Espresso':['IMG_0611.jpeg','IMG_0612.jpeg'],
  'GB Classic High-Waisted Leggings – Cream':['IMG_0584.jpeg','IMG_0585.jpeg'],
  'GB Classic High-Waisted Leggings – Grey':['IMG_0607.jpeg','IMG_0608.jpeg'],
  'GB Classic High-Waisted Leggings – Black':['IMG_0605.jpeg','IMG_0606.jpeg'],
  'GB Classic High-Waisted Leggings – Blue':['IMG_0603.jpeg','IMG_0604.jpeg'],
  'GB Classic High-Waisted Leggings – Green':['IMG_0601.jpeg','IMG_0602.jpeg'],
  'GB Classic High-Waisted Leggings – Red':['IMG_0599.jpeg','IMG_0600.jpeg'],
  'GB Classic High-Waisted Leggings – Espresso':['IMG_0609.jpeg','IMG_0610.jpeg'],
  'Cream Leggings':['IMG_0553.jpeg','IMG_0554.jpeg'],
  'Oxblood Leggings':['IMG_0549.jpeg','IMG_0550.jpeg'],
  'Onyx Leggings':['IMG_0541.jpeg','IMG_0542.jpeg'],
  'Bougie Houndstooth Leggings':['IMG_0534.jpeg','IMG_0535.jpeg'],
  'Vault Leggings':['IMG_0525.jpeg','IMG_0526.jpeg'],
  'Heritage Plaid Leggings':['IMG_0520.jpeg','IMG_0521.jpeg'],
  'Cream Workout Shorts':['IMG_0557.jpeg','IMG_0558.jpeg'],
  'Oxblood Workout Shorts':['IMG_0555.jpeg','IMG_0556.jpeg'],
  'Onyx Workout Shorts':['IMG_0543.jpeg','IMG_0544.jpeg'],
  'Bougie Houndstooth Workout Shorts':['IMG_0536.jpeg','IMG_0537.jpeg'],
  'Vault Workout Shorts':['IMG_0529.jpeg','IMG_0530.jpeg'],
  'Heritage Plaid Workout Shorts':['IMG_0515.jpeg','IMG_0516.jpeg']
 };
 function norm(v){return (v||'').replace(/\s+/g,' ').trim()}
 function pairFor(name){
  name=norm(name);if(products[name])return products[name];
  const key=Object.keys(products).find(k=>norm(k)===name);return key?products[key]:null
 }
 function fixCards(){
  document.querySelectorAll('#gbWomenGrid .gb-women-card').forEach(function(card){
   const nameEl=card.querySelector('.gb-women-name');const img=card.querySelector('.gb-women-img img');if(!nameEl||!img)return;
   const pair=pairFor(nameEl.textContent);if(pair&&img.getAttribute('src')!==pair[0])img.src=pair[0];
  })
 }
 function fixQuick(){
  const modal=document.getElementById('gbWomenQuick');if(!modal||!modal.classList.contains('open'))return;
  const name=document.getElementById('gbWqName');const front=document.getElementById('gbWqFront'),back=document.getElementById('gbWqBack');if(!name||!front||!back)return;
  const pair=pairFor(name.textContent);if(!pair)return;
  if(front.getAttribute('src')!==pair[0])front.src=pair[0];
  if(back.getAttribute('src')!==pair[1])back.src=pair[1];
  front.alt=norm(name.textContent)+' front view';back.alt=norm(name.textContent)+' back view';
 }
 function repair(){fixCards();fixQuick()}
 function install(){
  repair();
  const grid=document.getElementById('gbWomenGrid');if(grid)new MutationObserver(function(){fixCards()}).observe(grid,{childList:true,subtree:true});
  const modal=document.getElementById('gbWomenQuick');if(modal)new MutationObserver(function(){fixQuick()}).observe(modal,{attributes:true,attributeFilter:['class'],childList:true,subtree:true,characterData:true});
  document.addEventListener('click',function(e){if(e.target.closest('#gbWomenGrid .gb-women-view')){setTimeout(fixQuick,0);requestAnimationFrame(fixQuick)}},true);
 }
 if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',install);else install();
})();
</script>
'''
    s=s.replace('</body>',js+'\n</body>')

p.write_text(s)
