import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('Defects/Attendance2_Master_Defect_Log.md', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, l in enumerate(lines):
    if '20261028-01' in l or '20261028-07' in l or '20261028-03' in l:
        print(f"{i+1}: {l.strip()}")

