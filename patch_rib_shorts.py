from pathlib import Path
import re

p=Path('index.html')
s=p.read_text()

# v76 — correct semantic orientation for every Shop Women View Item.
# The v75 screenshot proves the files stored in each native row are ordered:
# [4] = BACK and [5] = FRONT.
# Display contract required by storefront:
# catalogue card = FRONT ([5])
# View Item LEFT = FRONT ([5])
# View Item RIGHT = BACK ([4])
# This changes only image selection; no layout, Build Your Fit geometry,
# filters, cart, observer, modal cloning, or event architecture is touched.

needle="<script>/* Women Shop preview catalog v63 */\n(function(){"
if needle in s and '__gbWomenCatalogInit' not in s:
    s=s.replace(needle,needle+"\n if(window.__gbWomenCatalogInit)return;window.__gbWomenCatalogInit=true;",1)

# Normalize every known renderer variant to the verified orientation.
variants=[
 "document.getElementById('gbWqFront').src=current[4];document.getElementById('gbWqBack').src=current[5];",
 "document.getElementById('gbWqFront').src=current[5];document.getElementById('gbWqBack').src=current[6];",
 "document.getElementById('gbWqFront').src=current[6];document.getElementById('gbWqBack').src=current[5];"
]
correct="document.getElementById('gbWqFront').src=current[5];document.getElementById('gbWqBack').src=current[4];"
for old in variants:s=s.replace(old,correct)

# Catalogue cards use the same verified FRONT file as the left View Item image.
s=s.replace("<img src=\"${p[4]}\" alt=\"${p[0]}\" loading=\"lazy\" decoding=\"async\">",
            "<img src=\"${p[5]}\" alt=\"${p[0]}\" loading=\"lazy\" decoding=\"async\">")

# Also normalize equivalent concatenated renderer syntax if present.
s=s.replace("src=\"'+p[4]+'\" alt=\"'+p[0]+'\"", "src=\"'+p[5]+'\" alt=\"'+p[0]+'\"")

# Remove obsolete broken index-6 references anywhere in the native Women Shop block.
m=re.search(r'(<script>/\* Women Shop preview catalog v63 \*/.*?</script>)',s,re.S)
if m:
    block=m.group(1)
    block=block.replace("current[6]","current[4]")
    block=block.replace("document.getElementById('gbWqFront').src=current[4];document.getElementById('gbWqBack').src=current[5];",correct)
    s=s[:m.start()]+block+s[m.end():]

p.write_text(s)
