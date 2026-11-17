# -*- coding: utf-8 -*-
import re

REPORT_FILE = "Attendance2_Defects_Gaps_and_Architecture_Inconsistencies_Report.md"

with open(REPORT_FILE, "r", encoding="utf-8") as f:
    text = f.read()

# Anchors to ensure exist
anchor_mappings = [
    ("### 1.1. Overall Consolidated Test Execution Dashboard (All 16 Modules)", '<a id="-overall-consolidated-test-execution-dashboard-all-18-modules"></a>\n'),
    ("## 8. Developer Remediation Action Checklist", '<a id="-part-5-actionable-developer-checklist-date-wise"></a>\n'),
    ("### 📊 Part 3: Defects Identified on 28 October 2026", '<a id="-part-3-defects-identified-on-28-october-2026-live-execution--user-scenarios"></a>\n'),
    ("### 📊 Part 3B: Live Execution of Holiday Calendar Test Cases", '<a id="-part-3b-live-execution-of-holiday-calendar-test-cases-attendance-2--3---29-october-2026"></a>\n'),
    ("### 📊 Part 3C: Defects Identified on 29 October 2026", '<a id="-part-3c-defects-identified-on-29-october-2026-live-api-probes-security--swagger-architecture"></a>\n'),
    ("### 📊 Part 3D: Defects Identified on 02 November 2026", '<a id="-part-3d-defects-identified-on-02-november-2026-live-post--patch-dto-validations-invariants--architecture"></a>\n'),
    ("### 📊 Part 3F: Defects Identified on 03 November 2026", '<a id="-part-3f-defects-identified-on-03-november-2026--holiday-list--holiday-calendar-module-live-compass-verification"></a>\n'),
    ("### 📊 Part 3G: Defects Identified on 05 November 2026", '<a id="-part-3g-defects-identified-on-05-november-2026--work-template-module-live-mongodb-compass-verification"></a>\n'),
    ("### 📊 Part 3H: Defects Identified & Live Verified on 05, 06 & 07 November 2026", '<a id="-part-3h-defects-identified--live-verified-on-05--06-november-2026--attendance-policy-module-live-verification-on-attendance-6--attendance-7"></a>\n'),
]

# For Part 1, 2, 2B, 4, let's find relevant headers or place anchors
# Part 1 defects were from 26 Oct (USER-01 etc.)
# Let's check where DEFECT-20261026-01 is described:
pos_p1 = text.find("DEFECT-20261026-01")
if pos_p1 != -1:
    line_start = text.rfind("\n", 0, pos_p1) + 1
    # Check if anchor exists
    if "-part-1-defects-identified-on-26-october-2026" not in text:
        text = text[:line_start] + '<a id="-part-1-defects-identified-on-26-october-2026"></a>\n<a id="-live-re-verification-of-part-1-defects-against-company-attendance-3-28-oct-2026"></a>\n' + text[line_start:]

pos_p2 = text.find("DEFECT-20261027-01")
if pos_p2 != -1:
    line_start = text.rfind("\n", 0, pos_p2) + 1
    if "-part-2-defects-identified-on-27-october-2026" not in text:
        text = text[:line_start] + '<a id="-part-2-defects-identified-on-27-october-2026"></a>\n<a id="-live-re-verification-of-part-2-defects-28-oct-2026"></a>\n<a id="-part-2b-live-execution-of-user-scenarios-on-company-attendance-4-28-oct-2026"></a>\n' + text[line_start:]

if "-part-4-standardized-bug-lifecycle-procedure" not in text:
    pos_sec8 = text.find("## 8. Developer Remediation Action Checklist")
    if pos_sec8 != -1:
        text = text[:pos_sec8] + '<a id="-part-4-standardized-bug-lifecycle-procedure"></a>\n' + text[pos_sec8:]

for target, anchor in anchor_mappings:
    if target in text and anchor.strip() not in text:
        text = text.replace(target, anchor + target, 1)
        print(f"Added anchor for: {target[:40]}")

with open(REPORT_FILE, "w", encoding="utf-8") as f:
    f.write(text)

print("Saved report with all navigation anchors added!")
