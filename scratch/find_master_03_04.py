import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('Defects/Attendance2_Master_Defect_Log.md', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for idx, line in enumerate(lines):
    if 'DEFECT-20261027-03' in line or 'DEFECT-20261027-04' in line or 'DTO-VAL-03' in line or 'DTO-VAL-04' in line:
        print(f"Line {idx+1}: {line.strip()[:120]}")

