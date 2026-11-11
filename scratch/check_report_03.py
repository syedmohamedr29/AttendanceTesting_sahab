import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('Attendance2_Defects_Gaps_and_Architecture_Inconsistencies_Report.md', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if 'DEFECT-20261027-03' in line:
        print(f"Line {i+1}: {line}", end='')
        for j in range(i, min(len(lines), i+20)):
            print(lines[j], end='')
        break

