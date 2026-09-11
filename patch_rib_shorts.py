from pathlib import Path
import re
p=Path('index.html')
s=p.read_text()

# Reorder only the existing Shop filter buttons: Women's, Men's, Accessories, Tops, Outerwear, All.
m=re.search(r'(<div class="filter-row"[^>]*>)(.*?)(</div>)',s,re.S)
if not m:
    raise SystemExit('Shop filter row not found')
body=m.group(2)
buttons=re.findall(r'<button class="filter-btn(?: active)?" data-filter="([^"]+)"[^>]*>.*?</button>',body,re.S)
wanted=['womens','mens','accessories','tops','outerwear','all']
if not all(x in buttons for x in wanted):
    raise SystemExit('Expected Shop filters not found')
parts={}
for match in re.finditer(r'<button class="filter-btn(?: active)?" data-filter="([^"]+)"[^>]*>.*?</button>',body,re.S):
    parts[match.group(1)]=match.group(0)
ordered=[]
for key in wanted:
    b=re.sub(r'class="filter-btn active"', 'class="filter-btn"', parts[key])
    if key=='womens':
        b=b.replace('class="filter-btn"','class="filter-btn active"',1)
    ordered.append(b)
newbody='\n          '+'\n          '.join(ordered)+'\n        '
s=s[:m.start(2)]+newbody+s[m.end(2):]

# The carousel should open immediately on Women's and follow whichever filter is selected afterward.
old='''// Initial page load must always open with the full All collection already rendered.
 const initialBtn=filterRow.querySelector('.filter-btn[data-filter="all"]');
 filterRow.querySelectorAll('.filter-btn').forEach(b=>b.classList.remove('active'));
 if(initialBtn) initialBtn.classList.add('active');
 applyFilter('all');'''
new='''// Initial page load opens immediately on the first Shop category: Women's.
 const initialBtn=filterRow.querySelector('.filter-btn[data-filter="womens"]');
 filterRow.querySelectorAll('.filter-btn').forEach(b=>b.classList.remove('active'));
 if(initialBtn) initialBtn.classList.add('active');
 applyFilter('womens');'''
if old not in s:
    raise SystemExit('Current carousel startup block not found')
s=s.replace(old,new,1)
p.write_text(s)
