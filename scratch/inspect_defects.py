import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('Attendance2_Defects_Gaps_and_Architecture_Inconsistencies_Report.md', 'r', encoding='utf-8') as f:
    lines = f.readlines()

print(f"Total lines in Defects Report: {len(lines)}")
for idx, line in enumerate(lines[:50]):
    print(f"Line {idx+1}: {line.strip()[:100]}")

