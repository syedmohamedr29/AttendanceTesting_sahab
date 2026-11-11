import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('Defects/Attendance2_Master_Defect_Log.md', 'r', encoding='utf-8') as f:
    content = f.read()

idx_01 = content.find('id="defect-20261027-01"')
idx_03 = content.find('id="defect-20261027-03"')
print(f"DEFECT-20261027-01 at {idx_01}, DEFECT-20261027-03 at {idx_03}")

