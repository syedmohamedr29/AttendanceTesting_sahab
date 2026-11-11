import sys
sys.stdout.reconfigure(encoding='utf-8')

file_path = 'Defects/Attendance2_Master_Defect_Log.md'
with open(file_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i in range(168, 178):
    if i < len(lines):
        print(f"{i+1}: {lines[i]}", end='')

