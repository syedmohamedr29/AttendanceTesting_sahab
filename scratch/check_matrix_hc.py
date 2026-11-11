import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('Defects/Attendance2_Master_Defect_Log.md', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if 'DEFECT-20261103-04' in line:
        for j in range(max(0, i-2), min(len(lines), i+15)):
            print(lines[j], end='')
        break

