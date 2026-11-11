import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('Attendance2_Defects_Gaps_and_Architecture_Inconsistencies_Report.md', 'r', encoding='utf-8') as f:
    text = f.read()

s1 = text.find('#### Defect `DEFECT-20261105-04`')
e1 = text.find('#### Defect `DEFECT-20261106-03`', s1)
print("=== DEFECT-20261105-04 in Report ===")
print(text[s1:e1])

e2 = text.find('### 7.6', e1)
if e2 == -1:
    e2 = text.find('### 7.7', e1)
if e2 == -1:
    e2 = text.find('---', e1 + 1000)
print("=== DEFECT-20261106-03 in Report ===")
print(text[e1:e2])
