# -*- coding: utf-8 -*-
with open('Defects/Attendance2_Master_Defect_Log.md', 'r', encoding='utf-8') as f:
    text = f.read()

# Add a prominent banner at the very top of Attendance2_Master_Defect_Log.md
banner = '''> 🚨 **OFFICIAL MASTER REPORT NOTICE:** The single authoritative Master Defect & Architecture Review Report is **[`Attendance2_Defects_Gaps_and_Architecture_Inconsistencies_Report.md`](file:///d:/Code/Attendance%20Testing/Attendance2_Defects_Gaps_and_Architecture_Inconsistencies_Report.md)** located in the project root directory. All updates, complete payloads, MongoDB Compass screenshots, and C# remediations are actively maintained there.\n\n'''

if 'OFFICIAL MASTER REPORT NOTICE' not in text:
    # insert right after H1
    idx = text.find('\n\n> **Service:**')
    if idx != -1:
        text = text[:idx] + '\n\n' + banner + text[idx+2:]
        with open('Defects/Attendance2_Master_Defect_Log.md', 'w', encoding='utf-8') as f:
            f.write(text)
        print("Banner added to Defects/Attendance2_Master_Defect_Log.md")
    else:
        print("Target pattern not found")
else:
    print("Banner already present")
