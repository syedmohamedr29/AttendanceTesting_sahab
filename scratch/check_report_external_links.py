# -*- coding: utf-8 -*-
with open('Attendance2_Defects_Gaps_and_Architecture_Inconsistencies_Report.md', 'r', encoding='utf-8') as f:
    text = f.read()

import re
matches = re.findall(r'\[([^\]]+)\]\(([^)]*Attendance2_Master_Defect_Log[^)]*)\)', text)
print(f"Found {len(matches)} links to Attendance2_Master_Defect_Log.md inside Report:")
for m in matches:
    print(m)
