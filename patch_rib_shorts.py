from pathlib import Path

p=Path('index.html')
s=p.read_text()

# v57 — ONLY swap the two remaining mismatched Classic MODEL boards.
# User's live screenshots confirm: Espresso label currently shows blue, Blue label currently shows espresso.
# Therefore Blue uses 1319... and Espresso uses BB251....
# View This Fit / Printify photos are untouched. No geometry/layout/arrows/splits are changed.
if 'Classic Blue Espresso swap v57' not in s:
    import re
    correct={
      'Blue':'1319CBE4-7111-42FE-AFB6-72211748DA6B.jpeg',
      'Espresso':'BB251A6A-A1C5-4955-AD45-12977154FDD1.jpeg'
    }
    for colour,board in correct.items():
        for product in ('GB Classic Sports Bra','GB Classic High-Waisted Leggings'):
            pat=r"\['"+re.escape(product)+r" – "+re.escape(colour)+r"','[^']+\.jpeg'\]"
            repl="['"+product+' – '+colour+"','"+board+"']"
            s=re.sub(pat,repl,s,count=1)
    s=s.replace('</body>','<script>/* Classic Blue Espresso swap v57 */</script>\n</body>')

p.write_text(s)
