import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('Defects/Attendance2_Master_Defect_Log.md', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i in range(2410, min(len(lines), 2440)):
    print(f"Line {i+1}: {lines[i]}", end='')

