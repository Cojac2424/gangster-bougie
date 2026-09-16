from pathlib import Path
import re

p=Path('index.html')
s=p.read_text()

# v77 — Build Your Fit default outfit only.
# Start on GB Classic Sports Bra – Green + GB Classic High-Waisted Leggings – Green.
# Preserve all proven compositor geometry, arrows, swipe logic, ordering and Shop Women behavior.

# The current ordered arrays place Classic Green at top index 10 and bottom index 16.
# Change only the initial selection; movement continues normally from these positions.
s=s.replace('let ti=0,bi=0;','let ti=10,bi=16;',1)

p.write_text(s)
