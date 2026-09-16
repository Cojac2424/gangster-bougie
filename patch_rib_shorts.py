from pathlib import Path
import re

p=Path('index.html')
s=p.read_text()

# v74 — verified image-orientation repair.
# The live screenshots proved the stored Women Shop pairs were semantically reversed:
# first file was the BACK view and second file was the FRONT view.
# Normalize the native product array itself so there is one source of truth:
# p[5] = FRONT (catalogue card + View Item left)
# p[6] = BACK  (View Item right)
# This does not add another controller, observer, or modal layer.

# Preserve the v72 singleton protections.
needle="<script>/* Women Shop preview catalog v63 */\n(function(){"
if needle in s and '__gbWomenCatalogInit' not in s:
    s=s.replace(needle,needle+"\n if(window.__gbWomenCatalogInit)return;window.__gbWomenCatalogInit=true;",1)
needle2="<script>/* Homepage hierarchy v64 */\n(function(){"
if needle2 in s and '__gbWomenHierarchyInit' not in s:
    s=s.replace(needle2,needle2+"\n if(window.__gbWomenHierarchyInit)return;window.__gbWomenHierarchyInit=true;",1)

# Exact pairs as they currently exist in the native Women Shop array: BACK, FRONT.
# Swap them to FRONT, BACK. Exact replacement makes the patch idempotent.
pairs=[
 ('IMG_0589.jpeg','IMG_0590.jpeg'),('IMG_0586.jpeg','IMG_0588.jpeg'),
 ('IMG_0597.jpeg','IMG_0598.jpeg'),('IMG_0591.jpeg','IMG_0592.jpeg'),
 ('IMG_0595.jpeg','IMG_0596.jpeg'),('IMG_0593.jpeg','IMG_0594.jpeg'),
 ('IMG_0611.jpeg','IMG_0612.jpeg'),('IMG_0584.jpeg','IMG_0585.jpeg'),
 ('IMG_0607.jpeg','IMG_0608.jpeg'),('IMG_0605.jpeg','IMG_0606.jpeg'),
 ('IMG_0603.jpeg','IMG_0604.jpeg'),('IMG_0601.jpeg','IMG_0602.jpeg'),
 ('IMG_0599.jpeg','IMG_0600.jpeg'),('IMG_0609.jpeg','IMG_0610.jpeg'),
 ('IMG_0553.jpeg','IMG_0554.jpeg'),('IMG_0549.jpeg','IMG_0550.jpeg'),
 ('IMG_0541.jpeg','IMG_0542.jpeg'),('IMG_0534.jpeg','IMG_0535.jpeg'),
 ('IMG_0525.jpeg','IMG_0526.jpeg'),('IMG_0520.jpeg','IMG_0521.jpeg'),
 ('IMG_0557.jpeg','IMG_0558.jpeg'),('IMG_0555.jpeg','IMG_0556.jpeg'),
 ('IMG_0543.jpeg','IMG_0544.jpeg'),('IMG_0536.jpeg','IMG_0537.jpeg'),
 ('IMG_0529.jpeg','IMG_0530.jpeg'),('IMG_0515.jpeg','IMG_0516.jpeg')
]

# Restrict swaps to the one native Women Shop product array only.
m=re.search(r'(const P=\[)(.*?)(\n \];)',s,re.S)
if m:
    body=m.group(2)
    for back,front in pairs:
        old="'"+back+"','"+front+"'"
        new="'"+front+"','"+back+"'"
        if old in body:
            body=body.replace(old,new,1)
    s=s[:m.start(2)]+body+s[m.end(2):]

# Native rendering contract. No fallback scripts and no duplicated event handlers.
s=s.replace("document.getElementById('gbWqFront').src=current[6];document.getElementById('gbWqBack').src=current[5];",
            "document.getElementById('gbWqFront').src=current[5];document.getElementById('gbWqBack').src=current[6];")

# Remove the experimental content-visibility rule from modal images; Safari/iPad should
# load the two selected images normally. Lazy decoding remains on the markup.
s=s.replace('#gbWomenQuick .gb-wq-pics img{content-visibility:auto}\n','')

# Keep the proven v72 close cleanup and freeze protection.
oldclose="function close(){modal.classList.remove('open');modal.setAttribute('aria-hidden','true')}"
newclose="function close(){modal.classList.remove('open');modal.setAttribute('aria-hidden','true');var f=document.getElementById('gbWqFront'),b=document.getElementById('gbWqBack');if(f)f.removeAttribute('src');if(b)b.removeAttribute('src')}"
if oldclose in s:s=s.replace(oldclose,newclose,1)

p.write_text(s)
