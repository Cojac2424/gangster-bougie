from pathlib import Path

p=Path('index.html')
s=p.read_text()

# v55 — fix the Classic MODEL-board labels confirmed by the live screenshots.
# 48A... is the red board; 7475... is the black board; 5EA... is espresso.
# This changes only the board assigned to each product name. No geometry/layout changes.
if 'Classic model label correction v55' not in s:
    fixes={
      "['GB Classic Sports Bra – Red','7475A5C3-1000-4C72-9498-153934E2DE66.jpeg']":"['GB Classic Sports Bra – Red','48A8992E-44EE-4EA0-9216-6151AA482183.jpeg']",
      "['GB Classic Sports Bra – Black','5EA988CF-42B7-475B-BD47-B4E8F6D26456.jpeg']":"['GB Classic Sports Bra – Black','7475A5C3-1000-4C72-9498-153934E2DE66.jpeg']",
      "['GB Classic Sports Bra – Espresso','48A8992E-44EE-4EA0-9216-6151AA482183.jpeg']":"['GB Classic Sports Bra – Espresso','5EA988CF-42B7-475B-BD47-B4E8F6D26456.jpeg']",
      "['GB Classic High-Waisted Leggings – Red','7475A5C3-1000-4C72-9498-153934E2DE66.jpeg']":"['GB Classic High-Waisted Leggings – Red','48A8992E-44EE-4EA0-9216-6151AA482183.jpeg']",
      "['GB Classic High-Waisted Leggings – Black','5EA988CF-42B7-475B-BD47-B4E8F6D26456.jpeg']":"['GB Classic High-Waisted Leggings – Black','7475A5C3-1000-4C72-9498-153934E2DE66.jpeg']",
      "['GB Classic High-Waisted Leggings – Espresso','48A8992E-44EE-4EA0-9216-6151AA482183.jpeg']":"['GB Classic High-Waisted Leggings – Espresso','5EA988CF-42B7-475B-BD47-B4E8F6D26456.jpeg']"
    }
    for old,new in fixes.items():
        if old in s:s=s.replace(old,new,1)
    s=s.replace('</body>','<script>/* Classic model label correction v55 */</script>\n</body>')

p.write_text(s)
