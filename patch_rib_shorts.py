from pathlib import Path
import re

p=Path('index.html')
s=p.read_text()

# v73 — preserve the v72 stability architecture and restore authoritative Women Shop imagery.
# Rules: catalogue card = FRONT; View Item left = FRONT; View Item right = BACK.
# No observers, modal cloning, duplicate controllers, or Build Your Fit geometry changes.

# Keep version-marked blocks singular so the catalogue cannot accumulate duplicate controllers.
def dedupe_marked_blocks(text, tag):
    pat=re.compile(r'<'+tag+r'>\s*/\*\s*([^*]+?)\s*\*/.*?</'+tag+r'>\s*', re.S)
    seen=set()
    def repl(m):
        marker=' '.join(m.group(1).split())
        if marker in seen:return ''
        seen.add(marker);return m.group(0)
    return pat.sub(repl,text)
s=dedupe_marked_blocks(s,'style')
s=dedupe_marked_blocks(s,'script')

# Remove obsolete modal repair layers if an older generated index still contains them.
for marker in ['Women Shop front-back correction v67','Women Shop Product Details v68','Women Shop freeze fix v69','Women Shop Product Details v69','Shop Women hard freeze fix v70','Women Shop stable modal v71']:
    s=re.sub(r'<script>\s*/\*\s*'+re.escape(marker)+r'\s*\*/.*?</script>\s*','',s,flags=re.S)
    s=re.sub(r'<style>\s*/\*\s*'+re.escape(marker)+r'\s*\*/.*?</style>\s*','',s,flags=re.S)

# Singleton guards retained from v72.
needle="<script>/* Women Shop preview catalog v63 */\n(function(){"
if needle in s and '__gbWomenCatalogInit' not in s:
    s=s.replace(needle,needle+"\n if(window.__gbWomenCatalogInit)return;window.__gbWomenCatalogInit=true;",1)
needle2="<script>/* Homepage hierarchy v64 */\n(function(){"
if needle2 in s and '__gbWomenHierarchyInit' not in s:
    s=s.replace(needle2,needle2+"\n if(window.__gbWomenHierarchyInit)return;window.__gbWomenHierarchyInit=true;",1)

# Authoritative front/back Printify mappings already supplied for the shop.
products={
 'GB Classic Sports Bra – Cream':('IMG_0589.jpeg','IMG_0590.jpeg'),
 'GB Classic Sports Bra – Grey':('IMG_0586.jpeg','IMG_0588.jpeg'),
 'GB Classic Sports Bra – Black':('IMG_0597.jpeg','IMG_0598.jpeg'),
 'GB Classic Sports Bra – Blue':('IMG_0591.jpeg','IMG_0592.jpeg'),
 'GB Classic Sports Bra – Green':('IMG_0595.jpeg','IMG_0596.jpeg'),
 'GB Classic Sports Bra – Red':('IMG_0593.jpeg','IMG_0594.jpeg'),
 'GB Classic Sports Bra – Espresso':('IMG_0611.jpeg','IMG_0612.jpeg'),
 'GB Classic High-Waisted Leggings – Cream':('IMG_0584.jpeg','IMG_0585.jpeg'),
 'GB Classic High-Waisted Leggings – Grey':('IMG_0607.jpeg','IMG_0608.jpeg'),
 'GB Classic High-Waisted Leggings – Black':('IMG_0605.jpeg','IMG_0606.jpeg'),
 'GB Classic High-Waisted Leggings – Blue':('IMG_0603.jpeg','IMG_0604.jpeg'),
 'GB Classic High-Waisted Leggings – Green':('IMG_0601.jpeg','IMG_0602.jpeg'),
 'GB Classic High-Waisted Leggings – Red':('IMG_0599.jpeg','IMG_0600.jpeg'),
 'GB Classic High-Waisted Leggings – Espresso':('IMG_0609.jpeg','IMG_0610.jpeg'),
 'Cream Leggings':('IMG_0553.jpeg','IMG_0554.jpeg'),
 'Oxblood Leggings':('IMG_0549.jpeg','IMG_0550.jpeg'),
 'Onyx Leggings':('IMG_0541.jpeg','IMG_0542.jpeg'),
 'Bougie Houndstooth Leggings':('IMG_0534.jpeg','IMG_0535.jpeg'),
 'Vault Leggings':('IMG_0525.jpeg','IMG_0526.jpeg'),
 'Heritage Plaid Leggings':('IMG_0520.jpeg','IMG_0521.jpeg'),
 'Cream Workout Shorts':('IMG_0557.jpeg','IMG_0558.jpeg'),
 'Oxblood Workout Shorts':('IMG_0555.jpeg','IMG_0556.jpeg'),
 'Onyx Workout Shorts':('IMG_0543.jpeg','IMG_0544.jpeg'),
 'Bougie Houndstooth Workout Shorts':('IMG_0536.jpeg','IMG_0537.jpeg'),
 'Vault Workout Shorts':('IMG_0529.jpeg','IMG_0530.jpeg'),
 'Heritage Plaid Workout Shorts':('IMG_0515.jpeg','IMG_0516.jpeg')
}

# Rewrite only image columns inside the single native Women Shop product array.
m=re.search(r'(<script>/\* Women Shop preview catalog v63 \*/.*?const P=\[)(.*?)(\n \];)',s,re.S)
if m:
    body=m.group(2)
    for name,(front,back) in products.items():
        # Preserve category, price and sizes; replace only the last two image fields.
        pat=re.compile(r"(\['"+re.escape(name)+r"'\s*,.*?,\s*\[[^\]]*\]\s*,\s*)'[^']*'\s*,\s*'[^']*'(\])")
        body=pat.sub(lambda mm:mm.group(1)+repr(front)+','+repr(back)+mm.group(2),body,count=1)
    s=s[:m.start(2)]+body+s[m.end(2):]

# Enforce the intended semantics in the native controller itself:
# p[5] is always FRONT for cards and left modal; p[6] is BACK for right modal.
s=s.replace("src=\"'+p[6]+'\" alt=\"'+p[0]+'\"", "src=\"'+p[5]+'\" alt=\"'+p[0]+'\"")
old="document.getElementById('gbWqFront').src=current[5];document.getElementById('gbWqBack').src=current[6];"
# If an old generated file has these reversed, normalize first.
s=s.replace("document.getElementById('gbWqFront').src=current[6];document.getElementById('gbWqBack').src=current[5];",old)

# Retain v72 memory release on modal close without changing appearance.
oldclose="function close(){modal.classList.remove('open');modal.setAttribute('aria-hidden','true')}"
newclose="function close(){modal.classList.remove('open');modal.setAttribute('aria-hidden','true');var f=document.getElementById('gbWqFront'),b=document.getElementById('gbWqBack');if(f)f.removeAttribute('src');if(b)b.removeAttribute('src')}"
if oldclose in s:s=s.replace(oldclose,newclose,1)

if 'Women Shop stability v72' not in s:
    s=s.replace('</head>',"\n<style>/* Women Shop stability v72 */\n#gbWomenCatalog .gb-women-card.gb-women-collapsed{display:none!important}\n#gbWomenQuick .gb-wq-pics img{content-visibility:auto}\n</style>\n</head>",1)

p.write_text(s)
