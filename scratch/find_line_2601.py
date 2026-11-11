import sys
sys.stdout.reconfigure(encoding='utf-8')

file_path = 'Defects/Attendance2_Master_Defect_Log.md'
with open(file_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

for idx, line in enumerate(lines):
    if '20261026-01' in line:
        print(f"Line {idx+1}: {line.strip()[:100]}")

