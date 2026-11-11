import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('Attendance2_Defects_Gaps_and_Architecture_Inconsistencies_Report.md', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('DEFECT-20261110-10')
if idx != -1:
    print("=== DEFECT-10 in Report MD ===")
    print(text[idx:idx+2500])

with open('Defects/Attendance2_Master_Defect_Log.md', 'r', encoding='utf-8') as f:
    text2 = f.read()

idx2 = text2.find('DEFECT-20261110-10')
if idx2 != -1:
    print("\n=== DEFECT-10 in Master Log ===")
    print(text2[idx2:idx2+2500])
