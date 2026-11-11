import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('Defects/Attendance2_Master_Defect_Log.md', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i in range(1705, min(len(lines), 1760)):
    print(lines[i], end='')

