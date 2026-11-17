# -*- coding: utf-8 -*-
import re

with open('Defects/Attendance2_Master_Defect_Log.md', 'r', encoding='utf-8') as f:
    master_text = f.read()

# 1. Update Date / Header Metadata
old_master_date = """> **Status:** **Active Master Defect Register** | **Date:** **16 November 2026 (Day 12 Update — Re-verification of WT - Company Default Failed Issues & Confluence Sync)** (Updated with `DEFECT-20261104-01`, `DEFECT-20261028-04`, `DEFECT-20261105-01`, `DEFECT-20261110-01`, and `DEFECT-20261103-16` live re-test verification notes; synced to Confluence page `Bug Fixes Testing` [Page ID: 1567653890]; previous 13-Nov update (Day 10 Update — Extreme QA on Attendance 10 + Compass Proof)** (Updated with `DEFECT-20261112-01` to `DEFECT-20261112-13` — Shifts & Rotation — Work Plans & Work Assignments Full Regular API + `/employees` + MongoDB Audit across `ATT7`, `ATT8`, `ATT9`, **340 RTM Cases (`233` Pass, `101` Fail, `6` Blocked)**, **30 Extreme QA Cases on `Attendance 10` (`7` Pass, `23` Fail / Invariant Breaches)**, live MongoDB Compass verification of `DEFECT-20261112-06` [Evidence 72], upstream `CompanySvc` 500 crash on POST, and **Evidences 01–73**)"""

new_master_date = """> **Status:** **Active Master Defect Register** | **Date:** **16 November 2026 (Day 12 Master Update — Location Shifts Full Suite Live Execution [112 TCs: 94 Pass, 1 By Design, 17 Fail] + Part 3N [DEFECT-20261116-01 to 06] + Part 3J [DEFECT-20261112-01 to 13] + Part 3K [DEFECT-20261114-01 to 04] + Multi-Tenant Re-Verification on Attendance 12 [Part 3I: 23 Defects] + 5 Sheets Failed Issues Re-Verification + Confluence Master Sync [Rows 1 to 84 Active — Version 22])** (Updated with complete Location Shifts test suite execution across 112 TCs in [`AttendanceTestCases_Master_Consolidated.xlsx`](file:///d:/Code/Attendance%20Testing/AttendanceTestCases_Master_Consolidated.xlsx); formal logging and MongoDB Compass verification of 6 new architectural defects `DEFECT-20261116-01` to `DEFECT-20261116-06` [Confluence Rows 79 to 84]; synchronization of Shifts & Rotation Work Plans & Assignments `DEFECT-20261112-01` to `13` [Rows 62 to 74]; Work Assignments Employee Lifecycle `DEFECT-20261114-01` to `04` [Rows 75 to 78]; Part 3I 23 Work Template defects live re-verified across multi-tenant `Attendance 12`; and 5 failing sheets stamped with live re-test verification findings)."""

assert old_master_date in master_text, "old_master_date not found in master log"
master_text = master_text.replace(old_master_date, new_master_date, 1)

# 2. Update Table of Contents
old_master_toc_pattern = r"## 📑 Table of Contents\s+([\s\S]+?)\n---"
match_master_toc = re.search(old_master_toc_pattern, master_text)
assert match_master_toc, "Table of contents not found in master log"

new_master_toc = """## 📑 Table of Contents
- [1. Executive Summary & Defect Metrics Dashboard](#1-executive-summary--defect-metrics-dashboard)
  - [1.1. Overall Consolidated Test Execution Dashboard (All 18 Modules)](#11-overall-consolidated-test-execution-dashboard-all-18-modules)
  - [1.2. Priority Failed User Scenarios (Module 15 Audit & Live Reproduction)](#12-priority-failed-user-scenarios-module-15-audit--live-reproduction)
- [2. Master Defect Quick-Reference Matrix (All 84+ Active Defects)](#2-master-defect-quick-reference-matrix)
- [3. Module 1: Holiday Calendar Module (`ERP.Attendance.HolidayCalendars`)](#3-module-1-holiday-calendar-module)
- [4. Module 2: Work Template & Location Cascade Module (`ERP.Attendance.WorkTemplates`)](#4-module-2-work-template--location-cascade-module)
- [5. Module 3: Work Plans, Shift Rosters & Attendance Policies](#5-module-3-work-plans-shift-rosters--attendance-policies)
- [6. Module 4: Security, Authentication & Multi-Tenancy Architecture](#6-module-4-security-authentication--multi-tenancy-architecture)
- [7. Verified Business Scenarios Confirmed as 'Not a Bug' (By Design)](#7-verified-business-scenarios-confirmed-as-not-a-bug)
- [8. Developer Remediation Action Checklist (Days 1 to 12)](#8-developer-remediation-action-checklist)
- [9. 🚨 Part 3I: Defects Identified & Live Verified on 10 November 2026 (Work Template Module: 23 Defects)](#-part-3i-defects-identified--live-verified-on-10-november-2026--work-template-module-fixed-flexible-split-delete--rotation-live-mongodb-compass--api-verification--re-verification-audit)
- [10. 🏢 Multi-Tenant Cross-Company Re-Verification: Part 3I Work Template Suite on Attendance 12 vs. Attendance 8](#-multi-tenant-cross-company-re-verification-part-3i-work-template-suite-on-company-attendance-12-vs-attendance-8)
- [11. 🆕 Part 3J: Defects Identified on 12 November 2026 — Shifts & Rotation: Work Plans & Work Assignments (Confluence Rows 62 to 74)](#-part-3j-defects-identified-on-12-november-2026--shifts--rotation--work-plans--work-assignments-post--patch-dto-cleanup-confluence-rows-62-to-74)
- [12. 🏢 Part 3K: Defects Identified on 14 November 2026 — Work Assignments & Employee Lifecycle Live Audit on Attendance 11 (Confluence Rows 75 to 78)](#-part-3k-defects-identified-on-14-november-2026--work-assignments--employee-lifecycle-live-audit-on-attendance-11-confluence-rows-75-to-78)
- [13. 📋 Part X: Shift Rotation Work Plan & Work Assignment Defects (Defects 64 to 74)](#part-x-shift-rotation-work-plan-defects--architectural-gaps-live-attendance-11-audit)
- [14. 🏢 Module 2 Deep Dive: WT - Location Shifts Live Test Execution & Defect Audit (16 November 2026 — 112 TCs)](#-module-2-deep-dive-wt---location-shifts-live-test-execution--defect-audit-16-november-2026)
- [15. 🏢 Part 3N: Defects Identified on 16 November 2026 — Work Template Module: Location Shifts Live API & MongoDB Audit (DEFECT-20261116-01 to 06 — Confluence Rows 79 to 84)](#-part-3n-defects-identified-on-16-november-2026--work-template-module--location-shifts-live-api--mongodb-audit-defect-20261116-01-to-06)
- [16. 📊 Master Re-Verification & Confluence Defect Tracking Matrix (Rows 1 to 84 Active — Version 22)](#-master-re-verification--deduplication-summary-rows-1-to-40--confluence-version-17)
- [17. 📸 Master Visual Evidence Index (Evidences 01 to 73)](#-master-visual-evidence-index)"""

master_text = master_text[:match_master_toc.start()] + new_master_toc + "\n\n---" + master_text[match_master_toc.end():]

# 3. Update Executive Summary count
master_text = master_text.replace(
    "a total of **104 defects and architecture gaps** were identified and verified with photographic proof.",
    "a total of **110 defects and architecture gaps (84 unique active tracking rows on Confluence Version 22)** were identified and verified with photographic proof.",
    1
)

# 4. Update Dashboard table in Master Defect Log
old_master_dash_row = "| **2** | **WT - Location Shifts** | 103 | 47 | 38 | 18 | 0 | 0 | 0 | 103 | 0.0% | ⚪ Not-Run (Pending Execution) |"
new_master_dash_row = "| **2** | **WT - Location Shifts** | 112 | 51 | 43 | 18 | 0 | **95** | **17** | **0** | **100.0%** | 🟢 **100% Executed (84.8% Pass / Pass by Design)** |"
assert old_master_dash_row in master_text, "old_master_dash_row not found in master log"
master_text = master_text.replace(old_master_dash_row, new_master_dash_row, 1)

# Ensure explicit anchors exist in master_text for key targets
master_anchors = [
    ("### 1.1. Overall Consolidated Test Execution Dashboard (All 16 Modules)", '<a id="11-overall-consolidated-test-execution-dashboard-all-18-modules"></a>'),
    ("### 1.2. Priority Failed User Scenarios (Module 15 Audit & Live Reproduction)", '<a id="12-priority-failed-user-scenarios-module-15-audit--live-reproduction"></a>'),
    ("## 2. Master Defect Quick-Reference Matrix", '<a id="2-master-defect-quick-reference-matrix"></a>'),
    ("## 3. Module 1: Holiday Calendar Module (`ERP.Attendance.HolidayCalendars`)", '<a id="3-module-1-holiday-calendar-module"></a>'),
    ("## 4. Module 2: Work Template & Location Cascade Module (`ERP.Attendance.WorkTemplates`)", '<a id="4-module-2-work-template--location-cascade-module"></a>'),
    ("## 5. Module 3: Work Plans, Shift Rosters & Attendance Policies", '<a id="5-module-3-work-plans-shift-rosters--attendance-policies"></a>'),
    ("## 6. Module 4: Security, Authentication & Multi-Tenancy Architecture", '<a id="6-module-4-security-authentication--multi-tenancy-architecture"></a>'),
    ("## 7. Verified Business Scenarios Confirmed as 'Not a Bug' (By Design)", '<a id="7-verified-business-scenarios-confirmed-as-not-a-bug"></a>'),
    ("## 8. Developer Remediation Action Checklist", '<a id="8-developer-remediation-action-checklist"></a>'),
    ("### 📊 Part 3I: Defects Identified & Live Verified on 10 November 2026 — Work Template Module: Fixed, Flexible, Split, Delete & Rotation (Live MongoDB Compass & API Verification) — Re-Verification Audit", '<a id="-part-3i-defects-identified--live-verified-on-10-november-2026--work-template-module-fixed-flexible-split-delete--rotation-live-mongodb-compass--api-verification--re-verification-audit"></a>'),
    ("### 🏢 Multi-Tenant Cross-Company Re-Verification: Part 3I Work Template Suite on Company Attendance 12 vs. Attendance 8", '<a id="-multi-tenant-cross-company-re-verification-part-3i-work-template-suite-on-company-attendance-12-vs-attendance-8"></a>'),
    ("### 📊 Part 3J: Defects Identified on 12 November 2026 — Shifts & Rotation — Work Plans & Work Assignments POST & PATCH DTO Cleanup (Confluence Rows 62 to 74)", '<a id="-part-3j-defects-identified-on-12-november-2026--shifts--rotation--work-plans--work-assignments-post--patch-dto-cleanup-confluence-rows-62-to-74"></a>'),
    ("### 🏢 Part 3K: Defects Identified on 14 November 2026 — Work Assignments & Employee Lifecycle Live Audit on Attendance 11 (Confluence Rows 75 to 78)", '<a id="-part-3k-defects-identified-on-14-november-2026--work-assignments--employee-lifecycle-live-audit-on-attendance-11-confluence-rows-75-to-78"></a>'),
    ("# PART X: SHIFT ROTATION WORK PLAN DEFECTS & ARCHITECTURAL GAPS (LIVE ATTENDANCE 11 AUDIT)", '<a id="part-x-shift-rotation-work-plan-defects--architectural-gaps-live-attendance-11-audit"></a>'),
    ("### 🏢 Module 2 Deep Dive: WT - Location Shifts Live Test Execution & Defect Audit (16 November 2026)", '<a id="-module-2-deep-dive-wt---location-shifts-live-test-execution--defect-audit-16-november-2026"></a>'),
    ("### 🏢 Part 3N: Defects Identified on 16 November 2026 — Work Template Module: Location Shifts Live API & MongoDB Audit (`DEFECT-20261116-01` to `DEFECT-20261116-06`)", '<a id="-part-3n-defects-identified-on-16-november-2026--work-template-module--location-shifts-live-api--mongodb-audit-defect-20261116-01-to-06"></a>'),
    ("### 📊 Master Re-Verification & Deduplication Summary (Rows 1 to 40 — Confluence Version 17)", '<a id="-master-re-verification--deduplication-summary-rows-1-to-40--confluence-version-17"></a>'),
    ("## 📸 Master Visual Evidence Index (Evidences 01 to 73)", '<a id="-master-visual-evidence-index"></a>'),
]

for heading, anchor_tag in master_anchors:
    if heading in master_text and anchor_tag not in master_text:
        master_text = master_text.replace(heading, f"{heading}\n\n{anchor_tag}", 1)

with open('Defects/Attendance2_Master_Defect_Log.md', 'w', encoding='utf-8') as f:
    f.write(master_text)

print("Successfully updated Defects/Attendance2_Master_Defect_Log.md")
