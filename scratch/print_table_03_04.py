import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('Defects/Attendance2_Master_Defect_Log.md', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i in range(153, 166):
    if i < len(lines):
        print(f"{i+1}: {lines[i]}", end='')

