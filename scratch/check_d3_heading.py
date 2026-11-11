import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('Attendance2_Defects_Gaps_and_Architecture_Inconsistencies_Report.md', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('#### Defect `DEFECT-20261110-03`')
if idx != -1:
    print(text[idx:idx+2500])
else:
    print("Heading not found")
