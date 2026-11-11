import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('Defects/Attendance2_Master_Defect_Log.md', 'r', encoding='utf-8') as f:
    text = f.read()

for idx, line in enumerate(text.splitlines()):
    if 'Attendance 4' in line or 'Part 2B' in line or 'DEFECT-20261028-02' in line or 'USER-22' in line:
        print(f"{idx+1}: {line}")

