import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('Attendance2_Defects_Gaps_and_Architecture_Inconsistencies_Report.md', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, l in enumerate(lines):
    if 'Defect `DEFECT-20261028-02`' in l:
        print(f"Line {i+1}: {l.strip()}")
        for k in range(i, min(i+50, len(lines))):
            print(f"{k+1}: {lines[k]}", end='')
        break

