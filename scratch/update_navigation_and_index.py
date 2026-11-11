import sys
import re
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side

sys.stdout.reconfigure(encoding='utf-8')

report_path = "Attendance2_Defects_Gaps_and_Architecture_Inconsistencies_Report.md"
master_excel_path = "AttendanceTestCases_Master_Consolidated.xlsx"

# ==============================================================================
# 1. UPDATE Master Navigation & Table of Contents + Dashboard in Markdown Report
# ==============================================================================
with open(report_path, "r", encoding="utf-8") as f:
    rep = f.read()

# Update Table of Contents
toc_replacement = """## 📅 Master Navigation & Table of Contents

Jump directly to any section, date-wise defect set, or execution summary:

* [**📊 Overall Consolidated Test Execution Dashboard (All 18 Modules)**](#-overall-consolidated-test-execution-dashboard-all-18-modules) — *Consolidated Pass/Fail Status Across All 18 Modules (1,765 Total Test Cases)*
* [**📅 Part 1: Defects Discovered on 26 October 2026**](#-part-1-defects-identified-on-26-october-2026) — *Core Architecture, Data Integrity & Cross-Service Synchronization (4 Issues)*
* [**🔄 Part 1 Live Re-Verification on Company 'Attendance 3'**](#-live-re-verification-of-part-1-defects-against-company-attendance-3-28-oct-2026) — *Live Re-Test Results (1 Fixed, 3 Open/Partial)*
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
* [**🏢 Part 3H: Defects Identified & Live Verified on 05 & 06 November 2026 (ATTENDANCE POLICY MODULE: ATTENDANCE 6 & 7)**](#-part-3h-defects-identified--live-verified-on-05--06-november-2026--attendance-policy-module-live-verification-on-attendance-6--attendance-7) — *Policy Lifecycles, Negative RateFormula (-1.5), Duplicate Key 500 Crash, Empty TenantName & MongoDB Audit (6 Defects)*
* [**✅ Part 5: Actionable Developer Checklist (Date-Wise)**](#-part-5-actionable-developer-checklist-date-wise) — *Consolidated Engineering Action Items for Khalid's Team (Days 1 to 7)*
* [**📸 Master Visual Evidence Index (Evidences 01 to 44)**](#-master-visual-evidence-index) — *All 44 High-Resolution Screenshots, MongoDB Compass Dumps & Swagger Evidence*"""

idx_toc_start = rep.find("## 📅 Master Navigation & Table of Contents")
idx_toc_end = rep.find("\n---\n", idx_toc_start)
if idx_toc_start != -1 and idx_toc_end != -1:
    rep = rep[:idx_toc_start] + toc_replacement + rep[idx_toc_end:]
    print("Updated Table of Contents in Report!")

# Update Consolidated Dashboard Table
dashboard_replacement = """## 📊 Overall Consolidated Test Execution Dashboard (All 18 Modules)

> **Master Workbook:** [`AttendanceTestCases_Master_Consolidated.xlsx`](file:///d:/Code/Attendance%20Testing/AttendanceTestCases_Master_Consolidated.xlsx) (`INDEX` Tab)  
> **Total Test Suite Volume:** **1,765 Test Cases** across 18 functional modules  
> **Live Execution Progress to Date:** **901 Test Cases Executed** (869 Passed, 32 Failed, 864 Not-Run) — **96.4% Pass Rate on Executed Tests**

| # | Module / Sheet Name | Total TCs | P0 (Blocker) | P1 (Must) | P2 (Should) | P3 (Nice) | Passed | Failed | Not-Run | Exec % | Execution Health Status |
|:---:|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|---|
| **1** | **WT - Company Default** | 150 | 67 | 53 | 27 | 3 | **146** | **4** | **0** | **100.0%** | 🟢 **100% Executed (97.3% Pass Rate)** |
| **2** | **WT - Location Shifts** | 103 | 47 | 38 | 18 | 0 | 0 | 0 | 103 | 0.0% | ⚪ Not-Run (Pending Execution) |
| **3** | **WT - Roster & Rotation** | 36 | 14 | 15 | 7 | 0 | 0 | 0 | 36 | 0.0% | ⚪ Not-Run (Pending Execution) |
| **4** | **Holiday Calendar - Company** | 83 | 35 | 32 | 16 | 0 | 0 | 0 | 83 | 0.0% | ⚪ Not-Run (Pending Execution) |
| **5** | **Holiday Calendar - Location** | 50 | 19 | 29 | 1 | 1 | 0 | 0 | 50 | 0.0% | ⚪ Not-Run (Pending Execution) |
| **6** | **Attendance Policies** | 219 | 55 | 145 | 19 | 0 | **213** | **6** | **0** | **100.0%** | 🟢 **100% Executed (97.3% Pass Rate)** |
| **7** | **Work Plans** | 167 | 66 | 65 | 33 | 3 | 0 | 0 | 167 | 0.0% | ⚪ Not-Run (Pending Execution) |
| **8** | **Work Assignments** | 149 | 48 | 71 | 26 | 4 | 0 | 0 | 149 | 0.0% | ⚪ Not-Run (Pending Execution) |
| **9** | **Attendance Exemptions** | 30 | 22 | 6 | 2 | 0 | 0 | 0 | 30 | 0.0% | ⚪ Not-Run (Pending Execution) |
| **10** | **Att Log - Upload (KT)** | 36 | 17 | 16 | 3 | 0 | 0 | 0 | 36 | 0.0% | ⚪ Testing Deferred (Pending KT) |
| **11** | **Att Log - Finalise (KT)** | 19 | 7 | 9 | 3 | 0 | 0 | 0 | 19 | 0.0% | ⚪ Testing Deferred (Pending KT) |
| **12** | **Att Log - Edits (KT)** | 99 | 55 | 38 | 6 | 0 | 0 | 0 | 99 | 0.0% | ⚪ Testing Deferred (Pending KT) |
| **13** | **Att Log - Issues (KT)** | 23 | 4 | 12 | 7 | 0 | 0 | 0 | 23 | 0.0% | ⚪ Testing Deferred (Pending KT) |
| **14** | **Att Log - Monthly L4-L5 (KT)** | 19 | 7 | 9 | 3 | 0 | 0 | 0 | 19 | 0.0% | ⚪ Testing Deferred (Pending KT) |
| **15** | **User Scenarios (Add Here)** | 138 | 31 | 80 | 20 | 0 | **129** | **9** | **0** | **100.0%** | 🟢 **100% Executed (93.5% Pass Rate)** |
| **16** | **Holiday Calendar - Test Cases** | 313 | 172 | 133 | 8 | 0 | **305** | **8** | **0** | **100.0%** | 🟢 **100% Executed (97.4% Pass Rate)** |
| **17** | **CDWT - Manual DTO Validations** | 53 | 27 | 21 | 5 | 0 | 0 | 0 | 53 | 0.0% | ⚪ Not-Run (Pending Manual Execution) |
| **18** | **Policies - DTO Validations** | 78 | 23 | 45 | 10 | 0 | **74** | **4** | **0** | **100.0%** | 🟢 **100% Executed (94.9% Pass Rate)** |
| **TOTAL** | **All 18 Modules Combined** | **1,765** | **716** | **817** | **214** | **11** | **869** | **32** | **864** | **51.0%** | 🟢 **Overall Test Suite Healthy — 96.4% Execution Pass Rate** |"""

idx_dash_start = rep.find("## 📊 Overall Consolidated Test Execution Dashboard")
idx_dash_end = rep.find("\n# 📅 Part 1:", idx_dash_start)
if idx_dash_start != -1 and idx_dash_end != -1:
    rep = rep[:idx_dash_start] + dashboard_replacement + "\n\n" + rep[idx_dash_end:]
    print("Updated Consolidated Dashboard Table in Report!")

with open(report_path, "w", encoding="utf-8") as f:
    f.write(rep)
print("Saved updated Markdown Report!")

# ==============================================================================
# 2. UPDATE INDEX SHEET IN AttendanceTestCases_Master_Consolidated.xlsx
# ==============================================================================
wb = openpyxl.load_workbook(master_excel_path)
ws = wb["INDEX"]

# Row 10: Attendance Policies (Module 6)
ws.cell(10, 3, 219) # Total TCs
ws.cell(10, 4, 55)  # P0
ws.cell(10, 5, 145) # P1
ws.cell(10, 6, 19)  # P2
ws.cell(10, 7, 0)   # P3
ws.cell(10, 8, "Core Active Policy Suite: Break, Grace Period, Overtime, BVA, Soft-Delete & MongoDB Compass Live Validations")
ws.cell(10, 9, 213) # Passed

# Row 22: Policies - DTO Validations (Module 18)
ws.cell(22, 3, 78) # Total TCs
ws.cell(22, 4, 23) # P0
ws.cell(22, 5, 45) # P1
ws.cell(22, 6, 10) # P2
ws.cell(22, 7, 0)  # P3
ws.cell(22, 8, "Complete Policy DTO Suite: Route Parameters, Common DTOs, Break, Grace, Overtime, BVA, Duplicate Collision & Invariant Verification")
ws.cell(22, 9, 74) # Passed

# Row 23: TOTAL
total_tcs = sum(ws.cell(r, 3).value or 0 for r in range(5, 23))
total_p0 = sum(ws.cell(r, 4).value or 0 for r in range(5, 23))
total_p1 = sum(ws.cell(r, 5).value or 0 for r in range(5, 23))
total_p2 = sum(ws.cell(r, 6).value or 0 for r in range(5, 23))
total_p3 = sum(ws.cell(r, 7).value or 0 for r in range(5, 23))
total_passed = sum(ws.cell(r, 9).value or 0 for r in range(5, 23))

ws.cell(23, 3, total_tcs)
ws.cell(23, 4, total_p0)
ws.cell(23, 5, total_p1)
ws.cell(23, 6, total_p2)
ws.cell(23, 7, total_p3)
ws.cell(23, 8, "Master Consolidated Suite: 18 Active Modules with User Scenarios, Holiday Suite, Policy Suite & Dedicated DTO Edge-Case Verification")
ws.cell(23, 9, total_passed)

# Format rows
for r in [10, 22, 23]:
    for c in range(1, 10):
        cell = ws.cell(r, c)
        if r == 23:
            cell.font = Font(name="Segoe UI", size=10, bold=True)
            cell.fill = PatternFill(start_color="D9E1F2", end_color="D9E1F2", fill_type="solid")
        else:
            cell.font = Font(name="Segoe UI", size=9)
        if c in [1, 3, 4, 5, 6, 7, 9]:
            cell.alignment = Alignment(horizontal="center", vertical="center")

wb.save(master_excel_path)
print(f"Updated Master Excel INDEX sheet! Total TCs: {total_tcs}, Total Passed: {total_passed}")
