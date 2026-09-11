from pathlib import Path
p=Path('index.html')
s=p.read_text()
old="applyFilter((filterRow.querySelector('.filter-btn.active')||{}).dataset||'all');"
new="""// Initial page load must always open with the full All collection already rendered.\n const initialBtn=filterRow.querySelector('.filter-btn[data-filter=\"all\"]');\n filterRow.querySelectorAll('.filter-btn').forEach(b=>b.classList.remove('active'));\n if(initialBtn) initialBtn.classList.add('active');\n applyFilter('all');"""
if old not in s:
    raise SystemExit('Carousel startup line not found')
s=s.replace(old,new,1)
p.write_text(s)
