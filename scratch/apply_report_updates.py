# -*- coding: utf-8 -*-
import re

# ==========================================
# 1. UPDATE Attendance2_Defects_Gaps_and_Architecture_Inconsistencies_Report.md
# ==========================================

with open('Attendance2_Defects_Gaps_and_Architecture_Inconsistencies_Report.md', 'r', encoding='utf-8') as f:
    report_text = f.read()

# 1.1 Update Report Metadata
old_meta = """> **Report Last Updated:** **16 November 2026 (Day 12 Update — Live Re-Verification of WT - Company Default Failed Issues & Confluence Sync)** (Updated with `DEFECT-20261104-01`, `DEFECT-20261028-04`, `DEFECT-20261105-01`, `DEFECT-20261110-01`, and `DEFECT-20261103-16` re-test verification findings; synced to Confluence page `Bug Fixes Testing` [Page ID: 1567653890]; previous 14-Nov update (Day 11 Update — Live Work Assignment & Employee Lifecycle Run on Attendance 11)** (Updated with `DEFECT-20261114-01` to `DEFECT-20261114-04` — Work Assignments & Employee Lifecycle Live Audit across `Attendance 11` `3a24e5e5-302e-91bd-feaa-b07979766dfe`, **203 Master Test Cases**, Critical Inactive Employee Orphaned Header Defect, Swagger `PATCH /remove` 404 Route Gap, and Missing LocationId Bypasses; previous 13-Nov update (Day 10 Update — Extreme QA on Attendance 10 + Compass Proof)** (Updated with `DEFECT-20261112-01` to `DEFECT-20261112-13` — Shifts & Rotation — Work Plans & Work Assignments Full Regular API + `/employees` + MongoDB Audit across `ATT7`, `ATT8`, `ATT9`, **340 RTM Cases (`233` Pass, `101` Fail, `6` Blocked)**, **30 Extreme QA Cases on `Attendance 10` (`7` Pass, `23` Fail / Invariant Breaches)**, live MongoDB Compass verification of `DEFECT-20261112-06` [Evidence 72], upstream `CompanySvc` 500 crash on POST, and **Evidences 01–73**)"""

new_meta = """> **Report Last Updated:** **16 November 2026 (Day 12 Master Update — WT: Location Shifts Live Test Execution [112 TCs: 94 Pass, 1 By Design, 17 Fail] + Part 3N [DEFECT-20261116-01 to 06] + Part 3J [DEFECT-20261112-01 to 13] + Part 3K [DEFECT-20261114-01 to 04] + Multi-Tenant Re-Verification on Attendance 12 [Part 3I: 23 Defects] + 5 Sheets Failed Issues Re-Verification + Confluence Page 'Bug Fixes Testing' [Version 22 Active — Rows 1 to 84])** (Updated with comprehensive Location Shifts test suite execution across 112 TCs in [`AttendanceTestCases_Master_Consolidated.xlsx`](file:///d:/Code/Attendance%20Testing/AttendanceTestCases_Master_Consolidated.xlsx); formal logging and MongoDB Compass verification of 6 new architectural defects `DEFECT-20261116-01` to `DEFECT-20261116-06` [Confluence Rows 79 to 84]; synchronization of Shifts & Rotation Work Plans & Assignments `DEFECT-20261112-01` to `13` [Rows 62 to 74]; Work Assignments Employee Lifecycle `DEFECT-20261114-01` to `04` [Rows 75 to 78]; Part 3I 23 Work Template defects live re-verified across multi-tenant `Attendance 12`; and 5 failing sheets stamped with live re-test verification findings)."""

assert old_meta in report_text, "old_meta not found in report"
report_text = report_text.replace(old_meta, new_meta, 1)

# 1.2 Update Master Navigation & Table of Contents
old_toc_pattern = r"## 📅 Master Navigation & Table of Contents\s+Jump directly to any section, date-wise defect set, or execution summary:\s+([\s\S]+?)\n---"
match_toc = re.search(old_toc_pattern, report_text)
assert match_toc, "TOC block not found in report"

new_toc = """## 📅 Master Navigation & Table of Contents

Jump directly to any section, date-wise defect set, or execution summary:

* [**📊 Overall Consolidated Test Execution Dashboard (All 18 Modules)**](#-overall-consolidated-test-execution-dashboard-all-18-modules) — *Consolidated Pass/Fail Status Across All 18 Modules (1,765 Total Test Cases — 1,013 Executed)*
* [**📅 Part 1: Defects Discovered on 26 October 2026**](#-part-1-defects-identified-on-26-october-2026) — *Core Architecture, Data Integrity & Cross-Service Synchronization (4 Issues)*
* [**🔄 Part 1 Live Re-Verification on Company 'Attendance 3'**](#-live-re-verification-of-part-1-defects-against-company-attendance-3) — *Live Re-Test Results (1 Fixed, 3 Open/Partial)*
* [**📅 Part 2: Defects Discovered on 27 October 2026**](#-part-2-defects-identified-on-27-october-2026) — *DTO Validations, Model Binding Traps & Schema Invariants (7 Issues)*
* [**🔄 Part 2 Live Re-Verification of Part 2 Defects**](#-live-re-verification-of-part-2-defects-28-oct-2026) — *Live Re-Test Results (3 Fixed, 4 Failing/Open)*
* [**🏢 Part 2B: Full Live Execution of User Scenarios (Add Here)**](#-part-2b-live-execution-of-user-scenarios-on-company-attendance-4-28-oct-2026) — *100% Executed Across All 138 Scenarios (129 Pass, 9 Fail — 93.5% Pass Rate)*
* [**📅 Part 3: Defects Discovered on 28 October 2026 (LIVE EXECUTION & USER SCENARIOS)**](#-part-3-defects-identified-on-28-october-2026-live-execution--user-scenarios) — *Live API Payloads & Re-Verification: 4 Fixed, 3 Open (7 Issues)*
* [**📅 Part 3B: Live Execution of Holiday Calendar Test Cases (Attendance 2 & 3)**](#-part-3b-live-execution-of-holiday-calendar-test-cases-attendance-2--3---29-october-2026) — *100% Executed Across All 313 TCs (305 Pass, 8 Fail — 97.4% Pass Rate)*
* [**📅 Part 3C: Defects Discovered on 29 October 2026 (SECURITY & SWAGGER ARCHITECTURE)**](#-part-3c-defects-identified-on-29-october-2026-live-api-probes-security--swagger-architecture) — *Critical JWT Validation Bypass (DEFECT-20261029-01) & Swagger Missing OAuth2 AuthorizationCode Flow (DEFECT-20261029-02) (2 Issues)*
* [**🔄 Part 4: Standardized Bug Lifecycle Procedure**](#-part-4-standardized-bug-lifecycle-procedure) — *6-Stage Protocol for Defect Discovery, Triage & Verification*
* [**📅 Part 3D: Defects Discovered on 02 November 2026 (LIVE POST & PATCH DTO VALIDATIONS & INVARIANTS)**](#-part-3d-defects-identified-on-02-november-2026-live-post--patch-dto-validations-invariants--architecture) — *Template Name Localization, ShortCode Boundaries, Duration & Time Invariants, 500 Crashes & Versioning Architecture (13 New Defects & 2 Architectural Clarifications)*
* [**📅 Part 3F: Defects Discovered on 03 November 2026 (HOLIDAY LIST MODULE: 12 DEFECTS & 2 DOMAIN CLARIFICATIONS)**](#-part-3f-defects-identified-on-03-november-2026--holiday-list--holiday-calendar-module-live-compass-verification) — *Holiday List Module Live Proofs: 12 Defects Logged + 2 Scenarios Confirmed 'Not a Bug' (Duplicate Entries & Overlapping Ranges Allowed by Design)*
* [**🏢 Part 3G: Defects Discovered on 05 November 2026 (WORK TEMPLATE MODULE: EMPTY COMPANYNAME IN MONGO)**](#-part-3g-defects-identified-on-05-november-2026--work-template-module-live-mongodb-compass-verification) — *Live MongoDB Compass Evidence: CompanyName persists as Object (empty) {} upon CDWT creation (DEFECT-20261105-01)*
* [**🏢 Part 3H: Defects Identified & Live Verified on 05, 06 & 07 November 2026 (ATTENDANCE POLICY MODULE: ATTENDANCE 6 & 7)**](#-part-3h-defects-identified--live-verified-on-05-06--07-november-2026--attendance-policy-module-live-verification-on-attendance-6--attendance-7) — *Policy Lifecycles, Negative RateFormula (-1.5), Duplicate Key 500 Crash, Empty TenantName, Invalid Request Structure & Missing Enum Validations (8 Defects)*
* [**🚨 Part 3I: Defects Discovered on 10 November 2026 (WORK TEMPLATES: FIXED, FLEXIBLE, SPLIT, DELETE & ROTATION - 23 DEFECTS)**](#-part-3i-defects-identified--live-verified-on-10-november-2026--work-template-module-fixed-flexible-split-delete--rotation-live-mongodb-compass--api-verification) — *Complete Work Template Testing: Fixed, Flexi, Split, Delete API Lifecycle & Rotation Templates (23 Defects Discovered & Live Verified)*
* [**🏢 Multi-Tenant Cross-Company Re-Verification: Part 3I Work Template Suite on Company Attendance 12 vs. Attendance 8 (16 November 2026)**](#-multi-tenant-cross-company-re-verification-part-3i-work-template-suite-on-company-attendance-12-vs-attendance-8) — *Live Multi-Tenant Persistence Audit: Confirms 100% of Active Part 3I Defects Persist Across Tenants (Row 8 & Rows 41 to 61)*
* [**🆕 Part 3J: Defects Discovered on 12 November 2026 (SHIFTS & ROTATION — WORK PLANS & WORK ASSIGNMENTS: DEFECT-20261112-01 to 13)**](#-part-3j-defects-identified-on-12-november-2026--shifts--rotation--work-plans--work-assignments-post--patch-dto-cleanup) — *DTO Cleanup (`DEFECT-20261112-01` & `-02`) Plus Full Live POST/PATCH/GET/`/employees`/Default/Delete/Propagation & Policy Audit (`DEFECT-20261112-03` to `-13`, 340 RTM Cases, Evidences 59–71 — Confluence Rows 62 to 74)*
* [**🏢 Part 3K: Defects Identified on 14 November 2026 — Work Assignments & Employee Lifecycle Live Audit on Attendance 11: DEFECT-20261114-01 to 04**](#-part-3k-defects-identified-on-14-november-2026--work-assignments--employee-lifecycle-live-audit-on-attendance-11-defect-20261114-01-to-04) — *Critical Inactive Employee Orphaned Header (`DEFECT-20261114-01`), Swagger Route Gap 404 on `PATCH /remove` (`DEFECT-20261114-02`), and Missing LocationId Scoping Bypasses on `/upcoming` & `/details` (`DEFECT-20261114-03` & `-04` — Confluence Rows 75 to 78)*
* [**📋 Part 3L: Shift Rotation & Rotation Work Plan Live Defect Log & Architectural Findings (14 November 2026)**](#part-3l-shift-rotation--rotation-work-plan-live-defect-log--architectural-findings-14-november-2026) — *Defects 64 to 69: Active Member Deletion Crash, Cross-Location Team Enrollment, Silent Integrity Corruptions*
* [**📋 Part 3M: Rotation Work Assignment Live Execution Defect Log & Architectural Findings (14 November 2026)**](#part-3m-rotation-work-assignment-live-execution-defect-log--architectural-findings-14-november-2026) — *Defects 70 to 74: Location Scoping on Schedules, Period Modification Scoping, Pagination Boundary Bypasses*
* [**🏢 Module 2 Deep Dive: WT - Location Shifts Live Test Execution & Defect Audit (16 November 2026)**](#-module-2-deep-dive-wt---location-shifts-live-test-execution--defect-audit-16-november-2026) — *112 Test Cases Executed (94 Passed, 1 Passed by Design, 17 Failed — 84.8% Pass Rate)*
* [**🏢 Part 3N: Defects Identified on 16 November 2026 — Work Template Module: Location Shifts Live API & MongoDB Audit: DEFECT-20261116-01 to 06**](#-part-3n-defects-identified-on-16-november-2026--work-template-module--location-shifts-live-api--mongodb-audit-defect-20261116-01-to-06) — *In-Place Location PATCH Audit Wipeout, 20-Quota Soft-Delete Leak, Deletion Lock, Tombstone Mutation, Model Validation Bypasses & Missing Arabic Name (Confluence Rows 79 to 84)*
* [**🔄 PART 12: Live Re-Verification of WT - Company Default Failed Issues & 5 Sheets (16 November 2026)**](#-part-12-live-re-verification-of-wt---company-default-failed-issues-16-november-2026) — *Live Re-Verification Across WT - Company Default (4 Fails), Policies - DTO Validations (18 Fails), Holiday Calendar (8 Fails), User Scenarios (9 Fails), Attendance Policies (21 Fails)*
* [**✅ Part 5: Actionable Developer Checklist (Date-Wise: Days 1 to 12)**](#-part-5-actionable-developer-checklist-date-wise) — *Consolidated Engineering Action Items for Khalid's Team (Days 1 to 12)*
* [**📊 Master Re-Verification & Confluence Defect Tracking Matrix (Rows 1 to 84 Active — Version 22)**](#-master-re-verification--deduplication-summary-rows-1-to-40--confluence-version-17) — *Comprehensive Confluence Status Matrix (84 Rows Synchronized Across Version 22)*
* [**📸 Master Visual Evidence Index (Evidences 01 to 73)**](#-master-visual-evidence-index) — *All 73 High-Resolution Screenshots, MongoDB Compass Dumps, Swagger & Retest Evidence*"""

report_text = report_text[:match_toc.start()] + new_toc + "\n\n---" + report_text[match_toc.end():]

# 1.3 Update Overall Consolidated Test Execution Dashboard in Report
old_dash_row = "|   **2**   | **WT - Location Shifts**          |       103       |      47      |      38      |      18      |      0      |       0       |      0      |      103      |       0.0%       | ⚪ Not-Run (Pending Execution)                                       |"
new_dash_row = "|   **2**   | **WT - Location Shifts**          |       112       |      51      |      43      |      18      |      0      | **95** | **17** | **0** | **100.0%** | 🟢 **100% Executed (84.8% Pass / Pass by Design)** |"
assert old_dash_row in report_text, "old_dash_row not found in report"
report_text = report_text.replace(old_dash_row, new_dash_row, 1)

# Also update dashboard execution total
old_exec_summary = "> **Live Execution Progress to Date:** **901 Test Cases Executed** (869 Passed, 32 Failed, 864 Not-Run) — **96.4% Pass Rate on Executed Tests**"
new_exec_summary = "> **Live Execution Progress to Date:** **1,013 Test Cases Executed** (964 Passed, 49 Failed, 752 Not-Run) — **95.2% Pass Rate on Executed Tests**"
if old_exec_summary in report_text:
    report_text = report_text.replace(old_exec_summary, new_exec_summary, 1)

old_dash_total = "| **TOTAL** | **All 18 Modules Combined**       | **1,765** | **716** | **817** | **214** | **11** | **869** | **32** | **864** | **51.0%** | 🟢 **Overall Test Suite Healthy — 96.4% Execution Pass Rate** |"
new_dash_total = "| **TOTAL** | **All 18 Modules Combined**       | **1,765** | **720** | **822** | **214** | **11** | **964** | **49** | **752** | **57.4%** | 🟢 **Overall Test Suite Healthy — 95.2% Execution Pass Rate (1,013 Executed)** |"
if old_dash_total in report_text:
    report_text = report_text.replace(old_dash_total, new_dash_total, 1)

# Ensure explicit anchors exist in report_text for section targets
anchors_to_ensure = [
    ("## 📊 Overall Consolidated Test Execution Dashboard (All 18 Modules)", '<a id="-overall-consolidated-test-execution-dashboard-all-18-modules"></a>'),
    ("# 📅 Part 1: Defects Identified on 26 October 2026", '<a id="-part-1-defects-identified-on-26-october-2026"></a>'),
    ("### 🔄 Live Re-Verification of Part 1 Defects Against Company 'Attendance 3'", '<a id="-live-re-verification-of-part-1-defects-against-company-attendance-3"></a>'),
    ("# 📅 Part 2: Defects Identified on 27 October 2026", '<a id="-part-2-defects-identified-on-27-october-2026"></a>'),
    ("## 🔄 Live Re-Verification of Part 2 Defects (28-Oct-2026)", '<a id="-live-re-verification-of-part-2-defects-28-oct-2026"></a>'),
    ("# 🏢 Part 2B: Live Execution of User Scenarios on Company 'Attendance 4' (28-Oct-2026)", '<a id="-part-2b-live-execution-of-user-scenarios-on-company-attendance-4-28-oct-2026"></a>'),
    ("# 📅 Part 3: Defects Identified on 28 October 2026 (LIVE EXECUTION & USER SCENARIOS)", '<a id="-part-3-defects-identified-on-28-october-2026-live-execution--user-scenarios"></a>'),
    ("# 📅 Part 3B: Live Execution of Holiday Calendar Test Cases (Attendance 2 & 3 - 29 October 2026)", '<a id="-part-3b-live-execution-of-holiday-calendar-test-cases-attendance-2--3---29-october-2026"></a>'),
    ("# 📅 Part 3C: Defects Identified on 29 October 2026 (Live API Probes, Security & Swagger Architecture)", '<a id="-part-3c-defects-identified-on-29-october-2026-live-api-probes-security--swagger-architecture"></a>'),
    ("# 🔄 Part 4: Standardized Bug Lifecycle Procedure", '<a id="-part-4-standardized-bug-lifecycle-procedure"></a>'),
    ("# 📅 Part 3D: Defects Identified on 02 November 2026 (Live POST & PATCH DTO Validations, Invariants & Architecture)", '<a id="-part-3d-defects-identified-on-02-november-2026-live-post--patch-dto-validations-invariants--architecture"></a>'),
    ("# 📅 Part 3F: Defects Identified on 03 November 2026 — Holiday List / Holiday Calendar Module (Live Compass Verification)", '<a id="-part-3f-defects-identified-on-03-november-2026--holiday-list--holiday-calendar-module-live-compass-verification"></a>'),
    ("# 🏢 Part 3G: Defects Identified on 05 November 2026 — Work Template Module (Live MongoDB Compass Verification)", '<a id="-part-3g-defects-identified-on-05-november-2026--work-template-module-live-mongodb-compass-verification"></a>'),
    ("# 🏢 Part 3H: Defects Identified & Live Verified on 05, 06 & 07 November 2026 — Attendance Policy Module (Live Verification on Attendance 6 & Attendance 7)", '<a id="-part-3h-defects-identified--live-verified-on-05-06--07-november-2026--attendance-policy-module-live-verification-on-attendance-6--attendance-7"></a>'),
    ("# 🏢 Part 3I: Defects Identified & Live Verified on 10 November 2026 — Work Template Module: Fixed, Flexible, Split, Delete & Rotation (Live MongoDB Compass & API Verification)", '<a id="-part-3i-defects-identified--live-verified-on-10-november-2026--work-template-module-fixed-flexible-split-delete--rotation-live-mongodb-compass--api-verification"></a>'),
    ("### 🏢 Multi-Tenant Cross-Company Re-Verification: Part 3I Work Template Suite on Company Attendance 12 vs. Attendance 8", '<a id="-multi-tenant-cross-company-re-verification-part-3i-work-template-suite-on-company-attendance-12-vs-attendance-8"></a>'),
    ("# 🆕 Part 3J: Defects Identified on 12 November 2026 — Shifts & Rotation — Work Plans & Work Assignments POST & PATCH DTO Cleanup", '<a id="-part-3j-defects-identified-on-12-november-2026--shifts--rotation--work-plans--work-assignments-post--patch-dto-cleanup"></a>'),
    ("## Part 3L: Shift Rotation & Rotation Work Plan Live Defect Log & Architectural Findings (14 November 2026)", '<a id="part-3l-shift-rotation--rotation-work-plan-live-defect-log--architectural-findings-14-november-2026"></a>'),
    ("## Part 3M: Rotation Work Assignment Live Execution Defect Log & Architectural Findings (14 November 2026)", '<a id="part-3m-rotation-work-assignment-live-execution-defect-log--architectural-findings-14-november-2026"></a>'),
    ("### 🏢 Module 2 Deep Dive: WT - Location Shifts Live Test Execution & Defect Audit (16 November 2026)", '<a id="-module-2-deep-dive-wt---location-shifts-live-test-execution--defect-audit-16-november-2026"></a>'),
    ("## 🔄 PART 12: LIVE RE-VERIFICATION OF WT - COMPANY DEFAULT FAILED ISSUES (16 NOVEMBER 2026)", '<a id="-part-12-live-re-verification-of-wt---company-default-failed-issues-16-november-2026"></a>'),
    ("# ✅ Part 5: Actionable Developer Checklist (Date-Wise)", '<a id="-part-5-actionable-developer-checklist-date-wise"></a>'),
    ("### 📊 Master Re-Verification & Deduplication Summary (Rows 1 to 40 — Confluence Version 17)", '<a id="-master-re-verification--deduplication-summary-rows-1-to-40--confluence-version-17"></a>'),
]

for heading, anchor_tag in anchors_to_ensure:
    if heading in report_text and anchor_tag not in report_text:
        report_text = report_text.replace(heading, f"{heading}\n\n{anchor_tag}", 1)

with open('Attendance2_Defects_Gaps_and_Architecture_Inconsistencies_Report.md', 'w', encoding='utf-8') as f:
    f.write(report_text)

print("Successfully updated Attendance2_Defects_Gaps_and_Architecture_Inconsistencies_Report.md")
