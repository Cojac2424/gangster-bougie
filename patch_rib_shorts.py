from pathlib import Path
import re

p=Path('index.html')
s=p.read_text()

# v72 — master stability fix for Shop Women.
# Root cause found: versioned <style>/<script> blocks (including Women Shop v63,
# Homepage hierarchy v64 and stable modal v71) existed more than once in index.html.
# That meant duplicate catalogue initializers, duplicate click handlers and duplicate
# MutationObservers were all acting on the same Shop Women grid/modal. Repeated View Item,
# filters and View More compounded the work until mobile Safari could freeze.
#
# This repair is deliberately architecture-level and idempotent:
#   1) de-duplicate ALL version-marked style/script blocks by their marker comment;
#   2) add singleton guards to the Women Shop catalogue and hierarchy initializers;
#   3) remove the v71 extra cleanup layer (native catalogue owns the modal again);
#   4) clear modal image sources on close so repeated product viewing releases references;
#   5) preserve Build Your Fit geometry, product data, cart behavior and appearance.

# De-duplicate version-marked blocks globally. A marker is the opening /* ... */ comment.
# Keep the first block for each marker and remove later copies.
def dedupe_marked_blocks(text, tag):
    pat=re.compile(r'<'+tag+r'>\s*/\*\s*([^*]+?)\s*\*/.*?</'+tag+r'>\s*', re.S)
    seen=set()
    def repl(m):
        marker=' '.join(m.group(1).split())
        if marker in seen:
            return ''
        seen.add(marker)
        return m.group(0)
    return pat.sub(repl,text)

s=dedupe_marked_blocks(s,'style')
s=dedupe_marked_blocks(s,'script')

# Remove the temporary v71 cleanup layer entirely. It is unnecessary once the duplicate
# catalogue initializers are gone, and keeping one owner for the modal is safer.
s=re.sub(r'<script>\s*/\*\s*Women Shop stable modal v71\s*\*/.*?</script>\s*','',s,flags=re.S)

# Add a hard singleton guard to the native Women Shop v63 initializer. Even if a future
# deployment accidentally duplicates this block, only one copy can attach listeners.
needle="<script>/* Women Shop preview catalog v63 */\n(function(){"
replacement="<script>/* Women Shop preview catalog v63 */\n(function(){\n if(window.__gbWomenCatalogInit)return;window.__gbWomenCatalogInit=true;"
if needle in s and '__gbWomenCatalogInit' not in s:
    s=s.replace(needle,replacement,1)

# Same protection for the hierarchy/View More layer, which owns the grid observer.
needle2="<script>/* Homepage hierarchy v64 */\n(function(){"
replacement2="<script>/* Homepage hierarchy v64 */\n(function(){\n if(window.__gbWomenHierarchyInit)return;window.__gbWomenHierarchyInit=true;"
if needle2 in s and '__gbWomenHierarchyInit' not in s:
    s=s.replace(needle2,replacement2,1)

# Make modal close release its two large product-image references. The next View Item
# assigns the selected front/back images again. This changes no visible appearance.
old="function close(){modal.classList.remove('open');modal.setAttribute('aria-hidden','true')}"
new="function close(){modal.classList.remove('open');modal.setAttribute('aria-hidden','true');var f=document.getElementById('gbWqFront'),b=document.getElementById('gbWqBack');if(f)f.removeAttribute('src');if(b)b.removeAttribute('src')}"
if old in s:
    s=s.replace(old,new,1)

# Add a tiny nonvisual performance safeguard: hidden catalogue cards do not participate
# in layout/paint, and modal images remain asynchronously decoded.
if 'Women Shop stability v72' not in s:
    css=r'''\n<style>/* Women Shop stability v72 */
#gbWomenCatalog .gb-women-card.gb-women-collapsed{display:none!important}
#gbWomenQuick .gb-wq-pics img{content-visibility:auto}
</style>\n'''
    s=s.replace('</head>',css+'</head>',1)

p.write_text(s)
