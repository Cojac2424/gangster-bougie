from pathlib import Path

p=Path('index.html')
s=p.read_text()

# v75 — root-cause fix for Shop Women View Item second image.
# Native Women Shop rows contain SIX fields:
# [0] name, [1] category, [2] price, [3] sizes, [4] FRONT, [5] BACK.
# v74 incorrectly used current[5]/current[6]. current[6] does not exist,
# causing Safari's blue ? broken-image placeholder.

needle="<script>/* Women Shop preview catalog v63 */\n(function(){"
if needle in s and '__gbWomenCatalogInit' not in s:
    s=s.replace(needle,needle+"\n if(window.__gbWomenCatalogInit)return;window.__gbWomenCatalogInit=true;",1)
needle2="<script>/* Homepage hierarchy v64 */\n(function(){"
if needle2 in s and '__gbWomenHierarchyInit' not in s:
    s=s.replace(needle2,needle2+"\n if(window.__gbWomenHierarchyInit)return;window.__gbWomenHierarchyInit=true;",1)

# One correct renderer contract. No observer, clone, or extra controller.
for old in [
 "document.getElementById('gbWqFront').src=current[5];document.getElementById('gbWqBack').src=current[6];",
 "document.getElementById('gbWqFront').src=current[6];document.getElementById('gbWqBack').src=current[5];"
]:
    s=s.replace(old,"document.getElementById('gbWqFront').src=current[4];document.getElementById('gbWqBack').src=current[5];")

# Catalogue card must use the same front source.
s=s.replace("<img src=\"${p[5]}\" alt=\"${p[0]}\" loading=\"lazy\" decoding=\"async\">",
            "<img src=\"${p[4]}\" alt=\"${p[0]}\" loading=\"lazy\" decoding=\"async\">")

# Remove old experimental Safari image rule if present.
s=s.replace('#gbWomenQuick .gb-wq-pics img{content-visibility:auto}\n','')

# Preserve close cleanup and freeze protection.
oldclose="function close(){modal.classList.remove('open');modal.setAttribute('aria-hidden','true')}"
newclose="function close(){modal.classList.remove('open');modal.setAttribute('aria-hidden','true');var f=document.getElementById('gbWqFront'),b=document.getElementById('gbWqBack');if(f)f.removeAttribute('src');if(b)b.removeAttribute('src')}"
if oldclose in s:s=s.replace(oldclose,newclose,1)

p.write_text(s)
