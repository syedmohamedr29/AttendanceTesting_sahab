import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('Attendance2_Defects_Gaps_and_Architecture_Inconsistencies_Report.md', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if 'Overall Consolidated Test Execution Dashboard' in line:
        print(f"Line {i+1}: {line}")
        for j in range(i, min(len(lines), i+35)):
            print(lines[j], end='')
        break

