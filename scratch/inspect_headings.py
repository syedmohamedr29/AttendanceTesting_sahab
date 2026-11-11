import sys

sys.stdout.reconfigure(encoding='utf-8')

with open("Attendance2_Defects_Gaps_and_Architecture_Inconsistencies_Report.md", "r", encoding="utf-8") as f:
    lines = f.readlines()

print(f"Total lines: {len(lines)}")
for idx, l in enumerate(lines):
    if l.startswith("#"):
        print(f"Line {idx+1:4d}: {l.strip()}")

