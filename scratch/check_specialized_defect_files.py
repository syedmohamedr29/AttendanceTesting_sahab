import os
import re
from collections import defaultdict

defect_files = [
    'Defects/REGULAR_WORK_PLAN_DEFECTS.md',
    'Defects/ROTATION_WORK_TEMPLATE_DEFECTS.md',
    'Defects/WORK_TEMPLATE_DEFECTS.md',
    'Defects/WORK_TEMPLATE_DELETE_DEFECTS.md'
]

for fp in defect_files:
    if not os.path.exists(fp):
        continue
    with open(fp, 'r', encoding='utf-8') as f:
        text = f.read()
    
    headers = re.findall(r'^#+\s+(.*)', text, re.MULTILINE)
    h_counts = defaultdict(int)
    for h in headers:
        # ignore generic headers like Steps to Reproduce
        if any(w in h.lower() for w in ['steps', 'summary', 'payload', 'impact', 'expected', 'actual', 'database', 'remediation', 'evidence', 'table of contents']):
            continue
        h_counts[h] += 1
    
    dupes = {k: v for k, v in h_counts.items() if v > 1}
    print(f"File {fp}: Total headers={len(headers)}, Duplicate custom headings={len(dupes)}")
    for k, v in dupes.items():
        print(f"  {k} (x{v})")
