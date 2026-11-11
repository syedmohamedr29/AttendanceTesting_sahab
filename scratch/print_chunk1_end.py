import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('Attendance2_Defects_Gaps_and_Architecture_Inconsistencies_Report.md', 'r', encoding='utf-8') as f:
    text = f.read()

idx1 = text.find('#### Defect `DEFECT-20261028-01`')
idx2 = text.find('#### Defect `DEFECT-20261028-02`')
lines = text[idx1:idx2].splitlines()
for l in lines[-15:]:
    print(l)

