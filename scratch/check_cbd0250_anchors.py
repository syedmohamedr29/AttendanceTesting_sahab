# -*- coding: utf-8 -*-
import subprocess
import re

out = subprocess.check_output(['git', 'show', 'cbd0250:Attendance2_Defects_Gaps_and_Architecture_Inconsistencies_Report.md'], text=True, errors='ignore')

anchors = re.findall(r'<a\s+id=["\']([^"\']+)["\']', out)
print("All anchors in cbd0250:")
for a in anchors:
    if 'part' in a.lower() or 'checklist' in a.lower():
        print(" ", a)
