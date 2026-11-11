import sys
sys.stdout.reconfigure(encoding='utf-8')

for fn in ['Attendance2_Defects_Gaps_and_Architecture_Inconsistencies_Report.md', 'Defects/Attendance2_Master_Defect_Log.md']:
    with open(fn, 'r', encoding='utf-8') as f:
        text = f.read()
    
    print(f"\n=================== {fn} ===================")
    idx = text.find('DEFECT-20261110-19')
    while idx != -1:
        line_start = text.rfind('\n', 0, idx)
        line_end = text.find('\n', idx)
        line = text[line_start:line_end].strip()
        if '###' in line or '####' in line:
            print("Found heading:", line)
            print(text[line_start:line_start+1500])
            break
        idx = text.find('DEFECT-20261110-19', idx+1)
