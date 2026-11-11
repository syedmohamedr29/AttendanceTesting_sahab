import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

for fname in ['Attendance2_Defects_Gaps_and_Architecture_Inconsistencies_Report.md', 'Defects/Attendance2_Master_Defect_Log.md']:
    print(f"\n==================== {fname} ====================")
    with open(fname, 'r', encoding='utf-8') as f:
        content = f.read()
    
    matches = re.finditer(r'(DEFECT-20261027-0[1-7])', content)
    found_lines = set()
    for m in matches:
        d_id = m.group(1)
        start = m.start()
        line_start = content.rfind('\n', 0, start) + 1
        line_end = content.find('\n', start)
        line_num = content.count('\n', 0, start) + 1
        if line_num not in found_lines:
            found_lines.add(line_num)
            print(f"Line {line_num:4d} [{d_id}]: {content[line_start:line_end].strip()[:100]}")

