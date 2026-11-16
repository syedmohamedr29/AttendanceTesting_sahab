# -*- coding: utf-8 -*-
with open('Attendance2_Defects_Gaps_and_Architecture_Inconsistencies_Report.md', 'r', encoding='utf-8') as f:
    content = f.read()

with open('scratch/update_master_defect_report.py', 'r', encoding='utf-8') as f:
    script_txt = f.read()

import re
part_3k_match = re.search(r'part_3k = """(.*?)"""', script_txt, re.DOTALL)
if part_3k_match:
    part_3k = part_3k_match.group(1)
    target = '# ✅ Part 5: Actionable Developer Checklist (Date-Wise)'
    if target in content:
        content = content.replace(target, part_3k + '\n\n' + target, 1)
        with open('Attendance2_Defects_Gaps_and_Architecture_Inconsistencies_Report.md', 'w', encoding='utf-8') as f:
            f.write(content)
        print('SUCCESSFULLY INSERTED PART 3K!')
    else:
        print('Target not found!')
else:
    print('part_3k not extracted!')
