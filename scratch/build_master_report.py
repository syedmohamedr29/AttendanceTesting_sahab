# -*- coding: utf-8 -*-
import os
import re

# Read source from Defects/Attendance2_Master_Defect_Log.md
with open('Defects/Attendance2_Master_Defect_Log.md', 'r', encoding='utf-8') as f:
    master_content = f.read()

# Define the Master Header for Attendance2_Defects_Gaps_and_Architecture_Inconsistencies_Report.md
header = '''# Attendance 2: Technical Defect Report, API Design Gaps & Architecture Consistency Review

> **Target Microservices:** `SP.AttendanceSvc` (.NET 9 / ASP.NET Core) & `SP.CompanySvc` (.NET 8)
> **Environment:** Sahab DEV (`https://attendance2.dev.zoolwork.com`, `sp.dev.zoolwork.com` & `https://company8.dev.zoolwork.com`)
> **Databases:**
> • Attendance 2: MongoDB `Sahab` on `10.1.0.4:27018` (Collections: `ERP.Attendance.*`)
> • Company Service: MongoDB `CompanySvcNET8test` (Collection: `CompaniesMaster`)
> **Review Stakeholders:** QA Team (Shivam, Naushad, Syed Mohamed), Engineering Lead (Khalid)
> **Master Test Suite Reference:** [`AttendanceTestCases_Master_Consolidated.xlsx`](file:///d:/Code/Attendance%20Testing/AttendanceTestCases_Master_Consolidated.xlsx)
> **Report Last Updated:** **16 November 2026 (Day 12 Master Update — Location Shifts Full Suite Live Execution [112 TCs: 94 Pass, 1 By Design, 17 Fail] + Part 3N [DEFECT-20261116-01 to 06] + Part 3J [DEFECT-20261112-01 to 13] + Part 3K [DEFECT-20261114-01 to 04] + Multi-Tenant Re-Verification on Attendance 12 [Part 3I: 23 Defects] + 5 Sheets Failed Issues Re-Verification + Confluence Master Sync [Rows 1 to 84 Active — Version 22])** (Updated with complete Location Shifts test suite execution across 112 TCs in [`AttendanceTestCases_Master_Consolidated.xlsx`](file:///d:/Code/Attendance%20Testing/AttendanceTestCases_Master_Consolidated.xlsx); formal logging and MongoDB Compass verification of 6 new architectural defects `DEFECT-20261116-01` to `DEFECT-20261116-06` [Confluence Rows 79 to 84]; synchronization of Shifts & Rotation Work Plans & Assignments `DEFECT-20261112-01` to `13` [Rows 62 to 74]; Work Assignments Employee Lifecycle `DEFECT-20261114-01` to `04` [Rows 75 to 78]; Part 3I 23 Work Template defects live re-verified across multi-tenant `Attendance 12`; and 5 failing sheets stamped with live re-test verification findings).

---
'''

# Find where Table of Contents starts in master_content
toc_idx = master_content.find('## 📑 Table of Contents')
if toc_idx == -1:
    raise ValueError("TOC not found in master_content")

body = master_content[toc_idx:]

# In root directory, relative image paths should be defect_evidence/... instead of ../defect_evidence/...
body = body.replace('../defect_evidence/', 'defect_evidence/')

# Also ensure file links to Attendance2_Master_Defect_Log.md are rewritten to internal anchors in the report
body = body.replace('file:///d:/Code/Attendance%20Testing/Defects/Attendance2_Master_Defect_Log.md#', '#')
body = body.replace('[Attendance2_Master_Defect_Log.md](#', '[Master Technical Report](#')

full_report = header + '\n' + body

output_path = 'Attendance2_Defects_Gaps_and_Architecture_Inconsistencies_Report.md'
with open(output_path, 'w', encoding='utf-8') as f:
    f.write(full_report)

print(f"Successfully generated {output_path}")
print(f"Total lines: {len(full_report.splitlines())}")
print(f"Total characters: {len(full_report)}")
