import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('Defects/Attendance2_Master_Defect_Log.md', 'r', encoding='utf-8') as f:
    lines = f.readlines()
for i, l in enumerate(lines):
    if '20261028-02' in l.lower() or '20261028_02' in l.lower() or '20261028' in l.lower():
        print(f'{i+1}: {l.strip()}')

