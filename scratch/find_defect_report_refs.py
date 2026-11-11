import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('Attendance2_Defects_Gaps_and_Architecture_Inconsistencies_Report.md', 'r', encoding='utf-8') as f:
    text = f.read()

import re
matches = [m.start() for m in re.finditer(r'20261026-04', text)]
print(f"Matches for 20261026-04 in report: {len(matches)}")
for m in matches:
    start = max(0, m - 100)
    end = min(len(text), m + 300)
    print("---")
    print(text[start:end])

