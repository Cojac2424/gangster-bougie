from pathlib import Path
p=Path('index.html'); s=p.read_text()
marker='<button class="view-item" id="openRibShorts">VIEW ITEM</button>'
pos=s.index(marker)
start=s.rfind('<article',0,pos)
end=s.index('</article>',pos)+len('</article>')
card=s[start:end]
old='IMG_0375.jpeg'
if old not in card:
    raise SystemExit('Red rib shorts card image not found')
card=card.replace(old,'IMG_0370.jpeg',1)
s=s[:start]+card+s[end:]
p.write_text(s)
