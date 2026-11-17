# -*- coding: utf-8 -*-
with open('Attendance2_Defects_Gaps_and_Architecture_Inconsistencies_Report.md', 'r', encoding='utf-8') as f:
    text = f.read()

import re

print("=== FINAL VERIFICATION OF MASTER REPORT ===")
print(f"Total lines: {len(text.splitlines())}")
print(f"Total bytes: {len(text.encode('utf-8'))}")

# Check 17 TOC items
toc_items = [
    "1. Executive Summary & Defect Metrics Dashboard",
    "2. Master Defect Quick-Reference Matrix",
    "3. Module 1: Holiday Calendar Module",
    "4. Module 2: Work Template & Location Cascade Module",
    "5. Module 3: Work Plans, Shift Rosters & Attendance Policies",
    "6. Module 4: Security, Authentication & Multi-Tenancy Architecture",
    "7. Verified Business Scenarios Confirmed as 'Not a Bug'",
    "8. Developer Remediation Action Checklist",
    "9. 🚨 Part 3I: Defects Identified & Live Verified on 10 November 2026",
    "10. 🏢 Multi-Tenant Cross-Company Re-Verification",
    "11. 🆕 Part 3J: Defects Identified on 12 November 2026",
    "12. 🏢 Part 3K: Defects Identified on 14 November 2026",
    "13. 📋 Part X: Shift Rotation Work Plan & Work Assignment Defects",
    "14. 🏢 Module 2 Deep Dive: WT - Location Shifts Live Test Execution",
    "15. 🏢 Part 3N: Defects Identified on 16 November 2026",
    "16. 📊 Master Re-Verification & Confluence Defect Tracking Matrix",
    "17. 📸 Master Visual Evidence Index"
]

all_found = True
for item in toc_items:
    if item in text:
        print(f"  [FOUND] {item}")
    else:
        print(f"  [MISSING] {item}")
        all_found = False

print(f"All 17 TOC headers verified: {all_found}")

# Verify Defects 64 to 74 full dossiers
defects_64_74 = [f"Defect {i}:" for i in range(64, 75)]
d_found = all(d in text for d in defects_64_74)
print(f"Defects 64 to 74 full dossiers present: {d_found}")

# Verify Part 3N dossiers
part3n_defects = [f"DEFECT-20261116-0{i}" for i in range(1, 7)]
p3n_found = all(d in text for d in part3n_defects)
print(f"Part 3N (DEFECT-20261116-01 to 06) full dossiers present: {p3n_found}")

# Verify Part 3K dossiers
part3k_defects = [f"DEFECT-20261114-0{i}" for i in range(1, 5)]
p3k_found = all(d in text for d in part3k_defects)
print(f"Part 3K (DEFECT-20261114-01 to 04) full dossiers present: {p3k_found}")

# Verify Part 3J dossiers
part3j_defects = [f"DEFECT-20261112-{i:02d}" for i in range(1, 14)]
p3j_found = all(d in text for d in part3j_defects)
print(f"Part 3J (DEFECT-20261112-01 to 13) full dossiers present: {p3j_found}")
