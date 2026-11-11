import sys

sys.stdout.reconfigure(encoding='utf-8')

for path in ['Attendance2_Defects_Gaps_and_Architecture_Inconsistencies_Report.md', 'Defects/Attendance2_Master_Defect_Log.md']:
    with open(path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    print(f"\n==================== {path} ====================")
    for i, line in enumerate(lines):
        if 'DEFECT-20261027-07' in line:
            print(f"Line {i+1}: {line.strip()}")
            # print surrounding 5 lines
            for j in range(max(0, i-2), min(len(lines), i+6)):
                print(f"   [{j+1}] {lines[j].strip()}")
            print("-" * 50)

