import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('Attendance2_Defects_Gaps_and_Architecture_Inconsistencies_Report.md', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, l in enumerate(lines):
    if ('20261028-01' in l or '20261028-07' in l or '20261028-03' in l) and i > 3500:
        print(f"{i+1}: {l.strip()}")

