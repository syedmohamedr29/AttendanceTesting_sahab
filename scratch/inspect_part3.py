import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('Attendance2_Defects_Gaps_and_Architecture_Inconsistencies_Report.md', 'r', encoding='utf-8') as f:
    lines = f.readlines()

start_line = None
end_line = None
for i, line in enumerate(lines):
    if '# 📅 Part 3: Defects Identified on 28 October 2026' in line:
        start_line = i
    if '# 📅 Part 3B:' in line:
        end_line = i
        break

print(f"Part 3 starts at line {start_line+1}, ends at line {end_line+1}")

for i in range(start_line, min(start_line + 65, len(lines))):
    print(f"{i+1}: {lines[i]}", end='')

