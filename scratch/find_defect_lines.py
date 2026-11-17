import re

def find_in_file(filepath):
    print(f"=== Searching {filepath} ===")
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    for i, line in enumerate(lines):
        if any(d in line for d in ['20261104-01', '20261105-01', '20261110-01', '20261103-16']):
            if line.startswith('#'):
                print(f"Line {i+1}: {line.strip()}")

find_in_file('Defects/Attendance2_Master_Defect_Log.md')
find_in_file('Attendance2_Defects_Gaps_and_Architecture_Inconsistencies_Report.md')
