import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('Attendance2_Defects_Gaps_and_Architecture_Inconsistencies_Report.md', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for idx, line in enumerate(lines):
    if 'holiday' in line.lower() or 'checklist' in line.lower() or '1704' in line or '1705' in line:
        print(f"Line {idx+1}: {line.strip()[:100]}")

