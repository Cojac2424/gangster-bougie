from pathlib import Path

p=Path('index.html')
s=p.read_text()

# v56 — remap ALL seven GB Classic MODEL boards from the user's complete live screenshots.
# Confirmed board colours from what each board visibly displays:
# BB251... = blue, 48A899... = red, 6A043... = green, 1319... = espresso,
# 7475... = black, 71EA... = grey, 5EA... = cream.
# View This Fit / Printify photos are NOT changed. No model geometry/layout/arrows/splits are changed.
if 'All seven Classic model colours v56' not in s:
    correct={
      'Cream':'5EA988CF-42B7-475B-BD47-B4E8F6D26456.jpeg',
      'Grey':'71EA0B6E-ADAC-48A9-972B-6F8B9B4CF6AA.jpeg',
      'Black':'7475A5C3-1000-4C72-9498-153934E2DE66.jpeg',
      'Blue':'BB251A6A-A1C5-4955-AD45-12977154FDD1.jpeg',
      'Green':'6A0433B5-2CB5-487C-BF0C-BA13AEBF3614.jpeg',
      'Red':'48A8992E-44EE-4EA0-9216-6151AA482183.jpeg',
      'Espresso':'1319CBE4-7111-42FE-AFB6-72211748DA6B.jpeg'
    }
    import re
    for colour,board in correct.items():
        for product in ('GB Classic Sports Bra','GB Classic High-Waisted Leggings'):
            pat=r"\['"+re.escape(product)+r" – "+re.escape(colour)+r"','[^']+\.jpeg'\]"
            repl="['"+product+' – '+colour+"','"+board+"']"
            s,n=re.subn(pat,repl,s,count=1)
    s=s.replace('</body>','<script>/* All seven Classic model colours v56 */</script>\n</body>')

p.write_text(s)
