import sys
sys.stdout.reconfigure(encoding='utf-8')

for fn in ['Attendance2_Defects_Gaps_and_Architecture_Inconsistencies_Report.md', 'Defects/Attendance2_Master_Defect_Log.md', 'defects/WORK_TEMPLATE_DEFECTS.md']:
    with open(fn, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    print(f"\n=================== {fn} (Total lines: {len(lines)}) ===================")
    found = False
    for i, l in enumerate(lines):
        if 'DEFECT-20261110-15' in l and ('###' in l or '##' in l):
            found = True
            print(f"Found heading at line {i+1}:")
            for j in range(i, min(i+60, len(lines))):
                print(f"{j+1}: {lines[j][:120].strip()}")
            break
    if not found:
        print("Heading for DEFECT-20261110-15 NOT found!")
