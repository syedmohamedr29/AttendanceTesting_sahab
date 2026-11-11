import sys
sys.stdout.reconfigure(encoding='utf-8')

file_path = 'Attendance2_Defects_Gaps_and_Architecture_Inconsistencies_Report.md'
with open(file_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i in range(218, 230):
    if i < len(lines):
        print(f"{i+1}: {lines[i]}", end='')

