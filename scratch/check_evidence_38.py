import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('Defects/Attendance2_Master_Defect_Log.md', 'r', encoding='utf-8') as f:
    text = f.read()

import re
matches = [m.start() for m in re.finditer('evidence_38', text)]
print('Occurrences of evidence_38:', len(matches))
for pos in matches:
    print('---')
    print(text[pos-100:pos+250])

