import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('Defects/Attendance2_Master_Defect_Log.md', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i in range(158, 164):
    if i < len(lines):
        print(f"Matrix Line {i+1}: {lines[i]}", end='')

for i in range(1675, 1720):
    if i < len(lines):
        print(f"Detail Line {i+1}: {lines[i]}", end='')

