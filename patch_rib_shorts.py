from pathlib import Path
p=Path('index.html')
s=p.read_text()
if 'id="build-your-fit"' not in s: raise SystemExit('Build Your Fit not present')

# v28: Signature Fit real-product thumbnail test. Preserve viewer/compositor geometry.
css=r'''
/* Build Your Fit — real product thumbnail v28 */
#build-your-fit .byf-fit-item{position:relative!important;padding-right:118px!important;min-height:118px!important}
#build-your-fit .byf-real-product{display:none;position:absolute;right:0;top:50%;transform:translateY(-50%);width:104px;height:104px;object-fit:contain;background:#fff;border-radius:12px;border:1px solid rgba(217,161,30,.55);padding:4px}
#build-your-fit .byf-real-product.show{display:block}
@media(max-width:480px){#build-your-fit .byf-fit-item{padding-right:92px!important}.byf-real-product{width:80px!important;height:80px!important}}
'''
if '/* Build Your Fit — real product thumbnail v28 */' not in s:
    s=s.replace('</style>',css+'\n</style>',1)

# Add one real-product slot to the top item. It stays hidden for bras whose real image has not been supplied yet.
needle='<div class="byf-sizes" id="byfTopSizes"></div></div><div class="byf-fit-item">'
repl='<div class="byf-sizes" id="byfTopSizes"></div><img class="byf-real-product" id="byfTopRealProduct" alt="Actual product"></div><div class="byf-fit-item">'
if needle in s and 'id="byfTopRealProduct"' not in s:
    s=s.replace(needle,repl,1)

# Update thumbnail from the same render() that updates the selected fit. IMG_0547 is the supplied GB-logo Oxblood mockup.
needle2="if(sp)sp.textContent=bottomName.includes('Workout Shorts')?'US$54.99':'US$69.99'}"
repl2="if(sp)sp.textContent=bottomName.includes('Workout Shorts')?'US$54.99':'US$69.99';const rp=document.getElementById('byfTopRealProduct');if(rp){const ox=tops[ti][0]==='Oxblood Sports Bra';rp.classList.toggle('show',ox);if(ox){rp.src='IMG_0547.jpeg';rp.alt='Actual Oxblood Sports Bra product'}}}"
if needle2 in s and "rp.src='IMG_0547.jpeg'" not in s:
    s=s.replace(needle2,repl2,1)

p.write_text(s)
