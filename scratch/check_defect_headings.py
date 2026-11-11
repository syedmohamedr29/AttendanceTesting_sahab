import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('Defects/Attendance2_Master_Defect_Log.md', 'r', encoding='utf-8') as f:
    content = f.read()

# Search for the headings of DEFECT-20261103-04 to DEFECT-20261103-15
for num in range(4, 16):
    d_id = f"DEFECT-20261103-{num:02d}"
    m = re.search(rf"###.*{d_id}.*", content)
    if m:
        print(m.group(0))

