import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('Attendance2_Defects_Gaps_and_Architecture_Inconsistencies_Report.md', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i in range(1324, min(1525, len(lines))):
    if lines[i].startswith('#') or lines[i].startswith('#### Defect'):
        print(f"Line {i+1}: {lines[i].strip()}")

