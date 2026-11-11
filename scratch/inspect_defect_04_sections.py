import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('Defects/Attendance2_Master_Defect_Log.md', 'r', encoding='utf-8') as f:
    text1 = f.read()

with open('Attendance2_Defects_Gaps_and_Architecture_Inconsistencies_Report.md', 'r', encoding='utf-8') as f:
    text2 = f.read()

# Find DEFECT-20261026-04 in Master Defect Log
import re
m1 = re.search(r'(\| \[`DEFECT-20261026-04`\].*?\n)', text1)
if m1:
    print("Master Defect Log Table Row:")
    print(m1.group(0))

m1_detail = re.search(r'(#{2,4}\s+.*?DEFECT-20261026-04.*?(?=#{2,4}\s+|\Z))', text1, re.DOTALL)
if m1_detail:
    print("Master Defect Log Detail Section:")
    print(m1_detail.group(0)[:1500])

# Find in Report
m2 = re.search(r'(#### Defect `DEFECT-20261026-04`.*?(?=#### Defect|\Z))', text2, re.DOTALL)
if m2:
    print("\nReport Detail Section:")
    print(m2.group(0)[:2500])

