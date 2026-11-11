import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('Attendance2_Defects_Gaps_and_Architecture_Inconsistencies_Report.md', 'r', encoding='utf-8') as f:
    lines = f.readlines()

print(f"Total lines in report: {len(lines)}")
for i in range(1140, 1175):
    print(lines[i], end='')

