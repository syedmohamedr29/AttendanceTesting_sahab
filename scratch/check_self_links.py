# -*- coding: utf-8 -*-
with open('Defects/Attendance2_Master_Defect_Log.md', 'r', encoding='utf-8') as f:
    text = f.read()

import re
matches = re.findall(r'\[([^\]]+)\]\(([^)]*Attendance2_Master_Defect_Log[^)]*)\)', text)
print(f"Found {len(matches)} links to Attendance2_Master_Defect_Log.md inside itself:")
for m in matches[:10]:
    print(m)
