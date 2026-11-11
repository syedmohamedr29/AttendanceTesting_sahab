import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('Attendance2_Defects_Gaps_and_Architecture_Inconsistencies_Report.md', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for idx, line in enumerate(lines):
    if 'Part 2B' in line or 'Attendance 4' in line or 'Part 2' in line or 'Part 3' in line:
        print(f'{idx+1}: {line.strip()}')

