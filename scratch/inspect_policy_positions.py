import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('Defects/Attendance2_Master_Defect_Log.md', 'r', encoding='utf-8') as f:
    text = f.read()

for d in ['DEFECT-20261106-07', 'DEFECT-20261106-06', 'DEFECT-20261106-05', 'DEFECT-20261106-04', 'DEFECT-20261106-03']:
    p = text.find(d)
    print(f'{d} position in Master Defect Log: {p}')

with open('Attendance2_Defects_Gaps_and_Architecture_Inconsistencies_Report.md', 'r', encoding='utf-8') as f:
    text2 = f.read()

for d in ['DEFECT-20261106-07', 'DEFECT-20261106-06', 'DEFECT-20261106-05', 'DEFECT-20261106-04', 'DEFECT-20261106-03']:
    p = text2.find(d)
    print(f'{d} position in Report: {p}')
