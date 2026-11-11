import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('Defects/Attendance2_Master_Defect_Log.md', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for idx, line in enumerate(lines):
    if 'DEFECT-20261027-06' in line or 'DEFECT-20261027-07' in line or 'DTO-VAL-06' in line or 'DTO-VAL-07' in line or 'USER-137' in line or 'USER-138' in line:
        print(f"Line {idx+1}: {line.strip()[:120]}")

