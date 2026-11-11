import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('Attendance2_Defects_Gaps_and_Architecture_Inconsistencies_Report.md', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i in range(3740, min(len(lines), 3780)):
    print(f"Line {i+1}: {lines[i]}", end='')

