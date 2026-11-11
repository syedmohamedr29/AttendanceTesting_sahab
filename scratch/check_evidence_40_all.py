import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('Defects/Attendance2_Master_Defect_Log.md', 'r', encoding='utf-8') as f:
    text = f.read()

# find all occurrences of evidence_40
import re
matches = [m.start() for m in re.finditer('evidence_40', text)]
print('Occurrences of evidence_40 in Master Defect Log:', len(matches), matches)
for pos in matches:
    print('---')
    print(text[pos-100:pos+250])

