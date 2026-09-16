from pathlib import Path
import re

p=Path('index.html')
s=p.read_text()

# v71 — stabilize EVERY Shop Women View Item button.
# Remove the experimental v67-v70 modal repair layers that accumulated in index.html.
# Those layers attached competing observers/listeners and v70 cloned the modal, which can
# strip the catalogue's original modal listeners. Return Shop Women to its native modal logic.
# Product Details will be re-added cleanly only after the catalogue is stable.
markers=[
 'Women Shop front-back correction v67',
 'Women Shop Product Details v68',
 'Women Shop freeze fix v69',
 'Women Shop Product Details v69',
 'Shop Women hard freeze fix v70'
]
for marker in markers:
    # Remove complete script/style blocks containing each experimental marker.
    s=re.sub(r'<script>[^<]*?/\*\s*'+re.escape(marker)+r'\s*\*/.*?</script>\s*','',s,flags=re.S)
    s=re.sub(r'<style>[^<]*?/\*\s*'+re.escape(marker)+r'\s*\*/.*?</style>\s*','',s,flags=re.S)

# Defensive cleanup for any Product Details nodes left in static markup (normally JS-created only).
s=re.sub(r'<details[^>]+id=["\']gbWqDetails(?:V69|V70)?["\'][^>]*>.*?</details>\s*','',s,flags=re.S)

# Lightweight safety reset: no MutationObserver, no modal cloning, no per-card handlers.
# One delegated close cleanup prevents stale detail nodes from surviving between items.
if 'Women Shop stable modal v71' not in s:
    js=r'''
<script>/* Women Shop stable modal v71 */
(function(){
 function clean(){
  var ids=['gbWqDetails','gbWqDetailsV69','gbWqDetailsV70'];
  for(var i=0;i<ids.length;i++){var n=document.getElementById(ids[i]);if(n)n.remove()}
 }
 document.addEventListener('click',function(e){
  if(e.target.closest('#gbWomenGrid .gb-women-view'))clean();
  if(e.target.closest('#gbWomenQuick .gb-wq-close'))clean();
 },true);
})();
</script>
'''
    s=s.replace('</body>',js+'\n</body>')

p.write_text(s)
