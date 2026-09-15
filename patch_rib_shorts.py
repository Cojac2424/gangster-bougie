from pathlib import Path

p=Path('index.html')
s=p.read_text()

# v48 — Cream and Oxblood workout-short photos were mapped to the opposite product.
# Swap only those two front/back image pairs and their cart thumbnails.
# No Build Your Fit geometry, joins, sizing, arrows, prices, descriptions or layout changed.
if 'Cream Oxblood shorts image swap v48' not in s:
    # Signature Fit product-photo mapping from v46.
    s=s.replace("'Cream Workout Shorts':{front:'IMG_0555.jpeg',back:'IMG_0556.jpeg'", "'Cream Workout Shorts':{front:'IMG_0557.jpeg',back:'IMG_0558.jpeg'")
    s=s.replace("'Oxblood Workout Shorts':{front:'IMG_0557.jpeg',back:'IMG_0558.jpeg'", "'Oxblood Workout Shorts':{front:'IMG_0555.jpeg',back:'IMG_0556.jpeg'")

    # Any existing shorts thumbnail maps from v46/v47.
    s=s.replace("'Cream Workout Shorts':'IMG_0555.jpeg','Oxblood Workout Shorts':'IMG_0557.jpeg'", "'Cream Workout Shorts':'IMG_0557.jpeg','Oxblood Workout Shorts':'IMG_0555.jpeg'")

    # Final lightweight override also guarantees the correct pair on the current live selection.
    js=r'''
<script>/* Cream Oxblood shorts image swap v48 */
(function(){
 const pairs={
  'Cream Workout Shorts':['IMG_0557.jpeg','IMG_0558.jpeg'],
  'Oxblood Workout Shorts':['IMG_0555.jpeg','IMG_0556.jpeg']
 };
 function sync(){
  const nameEl=document.getElementById('byfShopBottomName'),pair=document.getElementById('byfBottomRealProductPair');
  if(!nameEl||!pair)return;
  const name=(nameEl.textContent||'').trim(),imgs=pairs[name];
  if(!imgs)return;
  const nodes=pair.querySelectorAll('img');
  if(nodes[0]&&nodes[0].getAttribute('src')!==imgs[0])nodes[0].src=imgs[0];
  if(nodes[1]&&nodes[1].getAttribute('src')!==imgs[1])nodes[1].src=imgs[1];
 }
 const nameEl=document.getElementById('byfShopBottomName');
 if(nameEl&&window.MutationObserver)new MutationObserver(sync).observe(nameEl,{childList:true,characterData:true,subtree:true});
 const root=document.getElementById('build-your-fit');if(root)root.addEventListener('click',function(){requestAnimationFrame(sync)});
 sync();
})();
</script>
'''
    s=s.replace('</body>',js+'</body>')

p.write_text(s)
