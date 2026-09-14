from pathlib import Path
p=Path('index.html')
s=p.read_text()
if 'id="build-your-fit"' not in s: raise SystemExit('Build Your Fit not present')

# v31: Safe loading optimization only. Do not alter layout, Build Your Fit geometry, or image sources.
# Native browser lazy-loading is applied to ordinary below-fold <img> elements.
# Keep header/hero/brand imagery and Build Your Fit compositor backgrounds unchanged.
if '/* Safe native lazy loading v31 */' not in s:
    marker='</body>'
    js=r'''
<script>
/* Safe native lazy loading v31 */
(function(){
  const imgs=[...document.querySelectorAll('img')];
  imgs.forEach((img,index)=>{
    const inHeader=!!img.closest('header');
    const inHero=!!img.closest('.hero');
    const inBuild=!!img.closest('#build-your-fit');
    if(inHeader||inHero){
      img.loading='eager';
      img.fetchPriority='high';
      return;
    }
    if(inBuild){
      /* Signature Fit product thumbnails may be below fold, but keep the model compositor untouched. */
      if(img.closest('.byf-fit-panel')){
        img.loading='lazy';
        img.decoding='async';
        img.fetchPriority='low';
      }
      return;
    }
    img.loading='lazy';
    img.decoding='async';
    img.fetchPriority='low';
  });
})();
</script>
'''
    s=s.replace(marker,js+'\n'+marker,1)
    # Marker comment is inside the injected script above.

p.write_text(s)
