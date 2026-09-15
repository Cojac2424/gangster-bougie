from pathlib import Path
import re

p=Path('index.html')
s=p.read_text()
if 'id="build-your-fit"' not in s: raise SystemExit('Build Your Fit not present')

# v40 — only show the real Oxblood pair when Oxblood is the selected top.
# This intentionally mirrors the existing bottom behavior: unknown products stay blank until their real Printify images are supplied.
if 'Build Your Fit top real-image guard v40' not in s:
    js='''\n<script>/* Build Your Fit top real-image guard v40 */
(function(){
 function syncTopRealImages(){
  var name=document.getElementById('byfShopTopName');
  var pair=document.getElementById('byfTopRealProductPair');
  if(!name||!pair)return;
  var isOxblood=(name.textContent||'').trim()==='Oxblood Sports Bra';
  pair.style.display=isOxblood?'flex':'none';
 }
 var root=document.getElementById('build-your-fit');
 if(root){
  root.addEventListener('click',function(){setTimeout(syncTopRealImages,0)});
  root.addEventListener('pointerup',function(){setTimeout(syncTopRealImages,0)});
 }
 var name=document.getElementById('byfShopTopName');
 if(name&&window.MutationObserver)new MutationObserver(syncTopRealImages).observe(name,{childList:true,characterData:true,subtree:true});
 syncTopRealImages();
})();
</script>\n'''
    s=s.replace('</body>',js+'</body>')

p.write_text(s)
