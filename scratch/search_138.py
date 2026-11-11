import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('Attendance2_Defects_Gaps_and_Architecture_Inconsistencies_Report.md', 'r', encoding='utf-8') as f:
    text = f.read()

for idx, line in enumerate(text.splitlines()):
    if '138' in line:
        print(f"{idx+1}: {line}")

