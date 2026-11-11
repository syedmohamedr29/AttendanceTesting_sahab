import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

# ==============================================================================
# 1. Update Attendance2_Defects_Gaps_and_Architecture_Inconsistencies_Report.md
# ==============================================================================
file1 = "Attendance2_Defects_Gaps_and_Architecture_Inconsistencies_Report.md"
with open(file1, "r", encoding="utf-8") as f:
    text1 = f.read()

# Target 1: Dashboard header
dash_old = """> **Live Execution Progress to Date:** **598 Test Cases Executed** (541 Passed, 57 Failed, 929 Not-Run) — **90.5% Pass Rate on Executed Tests**

| # | Module / Sheet Name | Total TCs | P0 (Blocker) | P1 (Must) | P2 (Should) | P3 (Nice) | Passed | Failed | Not-Run | Exec % | Execution Health Status |
|:---:|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|---|
| **1** | **WT - Company Default** | 150 | 67 | 53 | 27 | 3 | **141** | **9** | **0** | **100.0%** | 🟢 **100% Executed (94.0% Pass Rate)** |"""

dash_new = """> **Live Execution Progress to Date:** **598 Test Cases Executed** (546 Passed, 52 Failed, 929 Not-Run) — **91.3% Pass Rate on Executed Tests**

| # | Module / Sheet Name | Total TCs | P0 (Blocker) | P1 (Must) | P2 (Should) | P3 (Nice) | Passed | Failed | Not-Run | Exec % | Execution Health Status |
|:---:|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|---|
| **1** | **WT - Company Default** | 150 | 67 | 53 | 27 | 3 | **146** | **4** | **0** | **100.0%** | 🟢 **100% Executed (97.3% Pass Rate)** |"""

if dash_old in text1:
    text1 = text1.replace(dash_old, dash_new)
    print("Replaced dashboard row 1 in report.")
else:
    print("WARNING: dash_old not found in report.")

# Target 2: Dashboard total row
total_old = """| **TOTAL** | **All 17 Modules Combined** | **1,579** | **686** | **667** | **213** | **13** | **541** | **57** | **981** | **37.9%** | 🎯 **598 Executed (541 Pass, 57 Fail — 90.5% Pass Rate)** |"""
total_new = """| **TOTAL** | **All 17 Modules Combined** | **1,579** | **686** | **667** | **213** | **13** | **546** | **52** | **981** | **37.9%** | 🎯 **598 Executed (546 Pass, 52 Fail — 91.3% Pass Rate)** |"""

if total_old in text1:
    text1 = text1.replace(total_old, total_new)
    print("Replaced dashboard total in report.")
else:
    print("WARNING: total_old not found in report.")

# Target 3: Key execution findings
finding_old = """> 1. **`WT - Company Default` (Module 1):** 100% completed across all 150 test cases covering Fixed, Flexible, and Split work templates, with 141 Passed and 9 Failed (**94.0% Pass Rate**)."""
finding_new = """> 1. **`WT - Company Default` (Module 1):** 100% completed across all 150 test cases covering Fixed, Flexible, and Split work templates. Live re-verification on **Attendance 8** confirmed **146 Passed and 4 Failed (97.3% Pass Rate)** — 7 historical defects (second default guard, empty PATCH validation, archive/delete guards, and version 2.0 creation) are fully functional on greenfield companies, leaving only 2 active multi-tenancy scoping defects (DOC-A-04 & DOC-A-05 / ROOT-E-05 & ROOT-E-06)."""

if finding_old in text1:
    text1 = text1.replace(finding_old, finding_new)
    print("Replaced finding 1 in report.")
else:
    print("WARNING: finding_old not found in report.")

# Target 4: Part 3 summary
part3_old = """1. **`User Scenarios (Add Here)` (Module 15):** **138 Total TCs — 112 Passed, 26 Failed, 0 Not-Run (100% Executed, 81.2% Pass Rate)**
2. **`WT - Company Default` (Module 1):** **150 Total TCs — 141 Passed, 9 Failed, 0 Not-Run (100% Executed, 94.0% Pass Rate)**"""

part3_new = """1. **`User Scenarios (Add Here)` (Module 15):** **138 Total TCs — 112 Passed, 26 Failed, 0 Not-Run (100% Executed, 81.2% Pass Rate)**
2. **`WT - Company Default` (Module 1):** **150 Total TCs — 146 Passed, 4 Failed, 0 Not-Run (100% Executed, 97.3% Pass Rate)** *(Re-verified on Attendance 8)*"""

if part3_old in text1:
    text1 = text1.replace(part3_old, part3_new)
    print("Replaced Part 3 summary in report.")
else:
    print("WARNING: part3_old not found in report.")

# Target 5: Section 1352 table
sec1352_old = """| Section Name | Total TCs | Passed | Failed | Pass Rate | Key Verification Notes |
|---|:---:|:---:|:---:|:---:|---|
| **A. Authentication, Tenant & Company Scoping** | 6 | 4 | 2 | 66.7% | No token / forged token return 401; cross-tenant header ignored in favor of JWT claim |
| **B. Create Company Default** | 7 | 7 | 0 | **100%** | Second CDWT rejected with `Cit.Attendance:1010` (one-default guard verified) |
| **C. Location-Default Cascade** | 6 | 6 | 0 | **100%** | Zero locations handled cleanly without exceptions; cascade markers verified |
| **D. Edit Company Default = New Version** | 10 | 9 | 1 | 90.0% | Version increment (v1.0 $\\rightarrow$ v2.0) verified; empty PATCH body throws 500 defect |
| **E. Version History & Restore an Old Version** | 5 | 5 | 0 | **100%** | `GET /company-default/versions` returns full version list |
| **F. Archive / Delete Guards on Company Default** | 3 | 1 | 2 | 33.3% | **DEFECT-20261028-03:** Active CDWT allowed to be archived and deleted |
| **G. Apply Latest Company Template to Locations** | 10 | 10 | 0 | **100%** | `GET /sync-status` returns `hasPendingLocSync`; `POST /apply-sync` executes cleanly |
| **H. End-to-End Flow** | 5 | 5 | 0 | **100%** | Complete lifecycle verified from setup to versioning |
| **Command Validation (Layer 1 — HTTP 400)** | 4 | 4 | 0 | **100%** | ShortCode length and alphanumeric rules return RFC 9110 HTTP 400 |
| **Business Rules & Success (Layer 2)** | 5 | 5 | 0 | **100%** | TenantId stamping, multilingual name, and single-default verified |
| **Polymorphic Types** | 3 | 3 | 0 | **100%** | Fixed, Flexi, Split templates verified |
| **Cascade Provisioning** | 9 | 9 | 0 | **100%** | LocationDefaultProvisioningService rules verified |
| **Company-Default Update / Edit (PATCH)** | 10 | 8 | 2 | 80.0% | Staged edits and sync flag verified |
| **Authentication, Authorization & Roles** | 6 | 6 | 0 | **100%** | `[Authorize(Roles = "TenantAdmin")]` enforced |
| **Sync Status (Banner)** | 4 | 4 | 0 | **100%** | Dynamic transition of `hasPendingLocSync` verified |
| **Apply Sync (Cascade)** | 12 | 12 | 0 | **100%** | Push cascade to locations verified |
| **End-to-End Integration** | 6 | 6 | 0 | **100%** | Full cycle verified |
| **GET Company-Default Versions** | 10 | 10 | 0 | **100%** | 10 versions retrieval scenarios verified |
| **Version Increment on Update** | 7 | 7 | 0 | **100%** | Semantic version incrementing verified |
| **Change Log / Diff Chips** | 17 | 17 | 0 | **100%** | `WorkTemplateChangeTracker.Diff` tracking verified |
| **Version Chain Composition & Gaps** | 5 | 5 | 0 | **100%** | Chain integrity verified |
| **TOTAL** | **150** | **141** | **9** | **94.0%** | **Full Sheet Verified & Synchronized in Excel** |"""

sec1352_new = """| Section Name | Total TCs | Passed | Failed | Pass Rate | Key Verification Notes |
|---|:---:|:---:|:---:|:---:|---|
| **A. Authentication, Tenant & Company Scoping** | 6 | 4 | 2 | 66.7% | No token / forged token return 401; cross-tenant header ignored in favor of JWT claim (DOC-A-04 & DOC-A-05 Fail) |
| **B. Create Company Default** | 7 | 7 | 0 | **100%** | Second CDWT rejected with `Cit.Attendance:1010` (one-default guard verified live on Attendance 8) |
| **C. Location-Default Cascade** | 6 | 6 | 0 | **100%** | Zero locations handled cleanly without exceptions; cascade markers verified |
| **D. Edit Company Default = New Version** | 10 | 10 | 0 | **100%** | Version increment (v1.0 $\\rightarrow$ v2.0) verified; empty PATCH body returns HTTP 400 validation error (no 500 crash) |
| **E. Version History & Restore an Old Version** | 5 | 5 | 0 | **100%** | `GET /company-default/versions` returns full version list |
| **F. Archive / Delete Guards on Company Default** | 3 | 3 | 0 | **100%** | Active CDWT archive/delete guards verified live returning HTTP 400 `Cit.Attendance:1003` |
| **G. Apply Latest Company Template to Locations** | 10 | 10 | 0 | **100%** | `GET /sync-status` returns `hasPendingLocSync`; `POST /apply-sync` executes cleanly |
| **H. End-to-End Flow** | 5 | 5 | 0 | **100%** | Complete lifecycle verified from setup to versioning |
| **Command Validation (Layer 1 — HTTP 400)** | 4 | 4 | 0 | **100%** | ShortCode length and alphanumeric rules return RFC 9110 HTTP 400 |
| **Business Rules & Success (Layer 2)** | 5 | 5 | 0 | **100%** | TenantId stamping, multilingual name, and single-default verified |
| **Polymorphic Types** | 3 | 3 | 0 | **100%** | Fixed, Flexi, Split templates verified |
| **Cascade Provisioning** | 9 | 9 | 0 | **100%** | LocationDefaultProvisioningService rules verified |
| **Company-Default Update / Edit (PATCH)** | 10 | 10 | 0 | **100%** | Staged edits and sync flag verified (v2.0 created cleanly with HTTP 200) |
| **Authentication, Authorization & Roles** | 6 | 4 | 2 | 66.7% | Tenant isolation (ROOT-E-05) and company scoping (ROOT-E-06) Fail |
| **Sync Status (Banner)** | 4 | 4 | 0 | **100%** | Dynamic transition of `hasPendingLocSync` verified |
| **Apply Sync (Cascade)** | 12 | 12 | 0 | **100%** | Push cascade to locations verified |
| **End-to-End Integration** | 6 | 6 | 0 | **100%** | Full cycle verified |
| **GET Company-Default Versions** | 10 | 10 | 0 | **100%** | 10 versions retrieval scenarios verified |
| **Version Increment on Update** | 7 | 7 | 0 | **100%** | Semantic version incrementing verified |
| **Change Log / Diff Chips** | 17 | 17 | 0 | **100%** | `WorkTemplateChangeTracker.Diff` tracking verified |
| **Version Chain Composition & Gaps** | 5 | 5 | 0 | **100%** | Chain integrity verified |
| **TOTAL** | **150** | **146** | **4** | **97.3%** | **Full Sheet Verified & Synchronized in Excel (Attendance 8 Live Audit)** |"""

if sec1352_old in text1:
    text1 = text1.replace(sec1352_old, sec1352_new)
    print("Replaced section 1352 table in report.")
else:
    print("WARNING: sec1352_old not found in report.")

with open(file1, "w", encoding="utf-8") as f:
    f.write(text1)
print(f"Updated {file1} successfully.")


# ==============================================================================
# 2. Update Defects/Attendance2_Master_Defect_Log.md
# ==============================================================================
file2 = "Defects/Attendance2_Master_Defect_Log.md"
with open(file2, "r", encoding="utf-8") as f:
    text2 = f.read()

# Add Section 1.1: Overall Consolidated Test Execution Dashboard right after Section 1
sec1_target = """### Defect Distribution by Functional Module

| Module | Target Collection / Component | Total | P0 Blocker | P1 Critical | P2 Major |
| :--- | :--- | :---: | :---: | :---: | :---: |
| **Module 1: Holiday Calendars** | `ERP.Attendance.HolidayCalendars` | **15** | 5 | 9 | 1 |
| **Module 2: Work Templates & Location Cascade** | `ERP.Attendance.WorkTemplates` | **26** | 1 | 24 | 1 |
| **Module 3: Work Plans, Rosters & Policies** | `ERP.Attendance.WorkPlans`, `Policies` | **7** | 0 | 6 | 1 |
| **Module 4: Security, Auth & Multi-Tenancy** | Kestrel JWT Middleware, Multi-Tenancy | **6** | 1 | 4 | 1 |
| **TOTAL** | **All 4 Modules Combined** | **55** | **7** | **43** | **4** |

---"""

sec1_addition = """### Defect Distribution by Functional Module

| Module | Target Collection / Component | Total | P0 Blocker | P1 Critical | P2 Major |
| :--- | :--- | :---: | :---: | :---: | :---: |
| **Module 1: Holiday Calendars** | `ERP.Attendance.HolidayCalendars` | **15** | 5 | 9 | 1 |
| **Module 2: Work Templates & Location Cascade** | `ERP.Attendance.WorkTemplates` | **26** | 1 | 24 | 1 |
| **Module 3: Work Plans, Rosters & Policies** | `ERP.Attendance.WorkPlans`, `Policies` | **7** | 0 | 6 | 1 |
| **Module 4: Security, Auth & Multi-Tenancy** | Kestrel JWT Middleware, Multi-Tenancy | **6** | 1 | 4 | 1 |
| **TOTAL** | **All 4 Modules Combined** | **55** | **7** | **43** | **4** |

---

### 1.1. Overall Consolidated Test Execution Dashboard (All 16 Modules)

> **Master Workbook Reference:** [`AttendanceTestCases_Master_Consolidated.xlsx`](file:///d:/Code/Attendance%20Testing/AttendanceTestCases_Master_Consolidated.xlsx) (`INDEX` Tab)  
> **Total Test Suite Volume:** **1,527 Test Cases** across 16 functional modules  
> **Live Execution Progress to Date:** **598 Test Cases Executed** (546 Passed, 52 Failed, 929 Not-Run) — **91.3% Pass Rate on Executed Tests**

| # | Module / Sheet Name | Total TCs | P0 (Blocker) | P1 (Must) | P2 (Should) | P3 (Nice) | Passed | Failed | Not-Run | Exec % | Execution Health Status |
|:---:|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|---|
| **1** | **WT - Company Default** | 150 | 67 | 53 | 27 | 3 | **146** | **4** | **0** | **100.0%** | 🟢 **100% Executed (97.3% Pass Rate)** |
| **2** | **WT - Location Shifts** | 103 | 47 | 38 | 18 | 0 | 0 | 0 | 103 | 0.0% | ⚪ Not-Run (Pending Execution) |
| **3** | **WT - Roster & Rotation** | 36 | 14 | 15 | 7 | 0 | 0 | 0 | 36 | 0.0% | ⚪ Not-Run (Pending Execution) |
| **4** | **Holiday Calendar - Company** | 83 | 35 | 32 | 16 | 0 | 0 | 0 | 83 | 0.0% | ⚪ Not-Run (Pending Execution) |
| **5** | **Holiday Calendar - Location** | 50 | 19 | 29 | 1 | 1 | 0 | 0 | 50 | 0.0% | ⚪ Not-Run (Pending Execution) |
| **6** | **Attendance Policies** | 115 | 48 | 44 | 21 | 2 | 0 | 0 | 115 | 0.0% | ⚪ Not-Run (Pending Execution) |
| **7** | **Work Plans** | 167 | 66 | 65 | 33 | 3 | 0 | 0 | 167 | 0.0% | ⚪ Not-Run (Pending Execution) |
| **8** | **Work Assignments** | 149 | 48 | 71 | 26 | 4 | 0 | 0 | 149 | 0.0% | ⚪ Not-Run (Pending Execution) |
| **9** | **Attendance Exemptions** | 30 | 22 | 6 | 2 | 0 | 0 | 0 | 30 | 0.0% | ⚪ Not-Run (Pending Execution) |
| **10** | **Att Log - Upload (KT)** | 36 | 17 | 16 | 3 | 0 | 0 | 0 | 36 | 0.0% | ⚪ Testing Deferred (Pending KT) |
| **11** | **Att Log - Finalise (KT)** | 19 | 7 | 9 | 3 | 0 | 0 | 0 | 19 | 0.0% | ⚪ Testing Deferred (Pending KT) |
| **12** | **Att Log - Edits (KT)** | 99 | 55 | 38 | 6 | 0 | 0 | 0 | 99 | 0.0% | ⚪ Testing Deferred (Pending KT) |
| **13** | **Att Log - Issues (KT)** | 23 | 4 | 12 | 7 | 0 | 0 | 0 | 23 | 0.0% | ⚪ Testing Deferred (Pending KT) |
| **14** | **Att Log - Monthly L4-L5 (KT)** | 19 | 7 | 9 | 3 | 0 | 0 | 0 | 19 | 0.0% | ⚪ Testing Deferred (Pending KT) |
| **15** | **User Scenarios (Add Here)** | 138 | 31 | 80 | 27 | 0 | **112** | **26** | **0** | **100.0%** | 🟢 **100% Executed (81.2% Pass Rate)** |
| **16** | **Holiday Calendar - Test Cases** | 310 | 172 | 130 | 8 | 0 | **288** | **22** | **0** | **100.0%** | 🚀 **100% Executed (92.9% Pass Rate)** |
| **17** | **CDWT - Manual DTO Validations** | 52 | 27 | 20 | 5 | 0 | 0 | 0 | 52 | 0.0% | 📝 Ready for Manual Testing |
| **TOTAL** | **All 17 Modules Combined** | **1,579** | **686** | **667** | **213** | **13** | **546** | **52** | **981** | **37.9%** | 🎯 **598 Executed (546 Pass, 52 Fail — 91.3% Pass Rate)** |

---"""

if sec1_target in text2:
    text2 = text2.replace(sec1_target, sec1_addition)
    print("Added Section 1.1 to Defects/Attendance2_Master_Defect_Log.md successfully.")
else:
    print("WARNING: sec1_target not found in master defect log.")

with open(file2, "w", encoding="utf-8") as f:
    f.write(text2)
print(f"Updated {file2} successfully.")

