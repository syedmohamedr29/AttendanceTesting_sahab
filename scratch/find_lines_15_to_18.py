import sys
sys.stdout.reconfigure(encoding='utf-8')

for fn in ['Attendance2_Defects_Gaps_and_Architecture_Inconsistencies_Report.md', 'Defects/Attendance2_Master_Defect_Log.md']:
    with open(fn, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    print(f"\n=================== {fn} ===================")
    for i, l in enumerate(lines):
        if 'DEFECT-20261110-15' in l and ('###' in l or '####' in l):
            print(f"DEFECT-15 heading at line {i+1}")
            for j in range(i, min(i+150, len(lines))):
                if 'DEFECT-20261110-18' in lines[j] and ('###' in lines[j] or '####' in lines[j]):
                    print(f"DEFECT-18 heading at line {j+1}")
                    end_idx = min(j+60, len(lines))
                    print(f"Section continues to line {end_idx}")
                    break
