# -*- coding: utf-8 -*-
with open('Attendance2_Defects_Gaps_and_Architecture_Inconsistencies_Report.md', 'r', encoding='utf-8') as f:
    text = f.read()

import re
matches = [m.start() for m in re.finditer(r'#+\s+.*Part 4', text)]
print("Part 4 matches:", matches)
for m in matches:
    print(text[m:m+500])
    print('---')
