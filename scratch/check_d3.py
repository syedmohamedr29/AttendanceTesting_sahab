import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('Attendance2_Defects_Gaps_and_Architecture_Inconsistencies_Report.md', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('DEFECT-20261110-03')
idx2 = text.find('DEFECT-20261110-04')
print(text[idx:idx2])
