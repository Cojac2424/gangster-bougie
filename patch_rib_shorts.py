from pathlib import Path
p=Path('index.html'); s=p.read_text()
old='<div class="sports-size-block"><span class="option-label">Size</span><div class="sizes" id="ribShortsSizes"></div></div><button class="sports-add"><span>＋</span> Add to Cart</button>'
new='<div class="sports-size-block"><span class="option-label">Size</span><div class="sizes" id="ribShortsSizes"></div></div><button class="sports-add" type="button" aria-label="Add to cart coming soon"><span>🛒</span>Add to Cart</button>'
if old not in s:
    raise SystemExit('Rib shorts cart button pattern not found')
s=s.replace(old,new,1)
p.write_text(s)
