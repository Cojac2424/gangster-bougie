from pathlib import Path

p=Path('index.html')
s=p.read_text()

# v54 — correct only the Classic four-view MODEL board mapping.
# The Printify View This Fit photos are already correct and are not changed here.
# Existing compositor geometry, split points, arrows, sizing and layout are untouched.
if 'Classic model board colour mapping v54' not in s:
    swaps={
      "['GB Classic Sports Bra – Cream','BB251A6A-A1C5-4955-AD45-12977154FDD1.jpeg']":"['GB Classic Sports Bra – Cream','71EA0B6E-ADAC-48A9-972B-6F8B9B4CF6AA.jpeg']",
      "['GB Classic Sports Bra – Grey','48A8992E-44EE-4EA0-9216-6151AA482183.jpeg']":"['GB Classic Sports Bra – Grey','BB251A6A-A1C5-4955-AD45-12977154FDD1.jpeg']",
      "['GB Classic Sports Bra – Black','6A0433B5-2CB5-487C-BF0C-BA13AEBF3614.jpeg']":"['GB Classic Sports Bra – Black','5EA988CF-42B7-475B-BD47-B4E8F6D26456.jpeg']",
      "['GB Classic Sports Bra – Blue','1319CBE4-7111-42FE-AFB6-72211748DA6B.jpeg']":"['GB Classic Sports Bra – Blue','6A0433B5-2CB5-487C-BF0C-BA13AEBF3614.jpeg']",
      "['GB Classic Sports Bra – Green','7475A5C3-1000-4C72-9498-153934E2DE66.jpeg']":"['GB Classic Sports Bra – Green','1319CBE4-7111-42FE-AFB6-72211748DA6B.jpeg']",
      "['GB Classic Sports Bra – Red','71EA0B6E-ADAC-48A9-972B-6F8B9B4CF6AA.jpeg']":"['GB Classic Sports Bra – Red','7475A5C3-1000-4C72-9498-153934E2DE66.jpeg']",
      "['GB Classic Sports Bra – Espresso','5EA988CF-42B7-475B-BD47-B4E8F6D26456.jpeg']":"['GB Classic Sports Bra – Espresso','48A8992E-44EE-4EA0-9216-6151AA482183.jpeg']",
      "['GB Classic High-Waisted Leggings – Cream','BB251A6A-A1C5-4955-AD45-12977154FDD1.jpeg']":"['GB Classic High-Waisted Leggings – Cream','71EA0B6E-ADAC-48A9-972B-6F8B9B4CF6AA.jpeg']",
      "['GB Classic High-Waisted Leggings – Grey','48A8992E-44EE-4EA0-9216-6151AA482183.jpeg']":"['GB Classic High-Waisted Leggings – Grey','BB251A6A-A1C5-4955-AD45-12977154FDD1.jpeg']",
      "['GB Classic High-Waisted Leggings – Black','6A0433B5-2CB5-487C-BF0C-BA13AEBF3614.jpeg']":"['GB Classic High-Waisted Leggings – Black','5EA988CF-42B7-475B-BD47-B4E8F6D26456.jpeg']",
      "['GB Classic High-Waisted Leggings – Blue','1319CBE4-7111-42FE-AFB6-72211748DA6B.jpeg']":"['GB Classic High-Waisted Leggings – Blue','6A0433B5-2CB5-487C-BF0C-BA13AEBF3614.jpeg']",
      "['GB Classic High-Waisted Leggings – Green','7475A5C3-1000-4C72-9498-153934E2DE66.jpeg']":"['GB Classic High-Waisted Leggings – Green','1319CBE4-7111-42FE-AFB6-72211748DA6B.jpeg']",
      "['GB Classic High-Waisted Leggings – Red','71EA0B6E-ADAC-48A9-972B-6F8B9B4CF6AA.jpeg']":"['GB Classic High-Waisted Leggings – Red','7475A5C3-1000-4C72-9498-153934E2DE66.jpeg']",
      "['GB Classic High-Waisted Leggings – Espresso','5EA988CF-42B7-475B-BD47-B4E8F6D26456.jpeg']":"['GB Classic High-Waisted Leggings – Espresso','48A8992E-44EE-4EA0-9216-6151AA482183.jpeg']"
    }
    for old,new in swaps.items():
        if old in s:s=s.replace(old,new,1)
    s=s.replace('</body>','<script>/* Classic model board colour mapping v54 */</script>\n</body>')

p.write_text(s)
