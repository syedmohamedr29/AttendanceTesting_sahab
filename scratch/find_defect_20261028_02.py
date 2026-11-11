import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('Defects/Attendance2_Master_Defect_Log.md', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for idx, line in enumerate(lines):
    if 'DEFECT-20261028-02' in line:
        print(f"{idx+1}: {line.strip()}")

