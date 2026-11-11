import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('Attendance2_Defects_Gaps_and_Architecture_Inconsistencies_Report.md', 'r', encoding='utf-8') as f:
    lines = f.readlines()

print(f"Total lines: {len(lines)}")
for i, l in enumerate(lines):
    if '# 📅 Part 3B:' in l:
        for k in range(i, min(i+45, len(lines))):
            print(f"{k+1}: {lines[k]}", end='')
        break

