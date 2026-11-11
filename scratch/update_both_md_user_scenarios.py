import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

# ==============================================================================
# 1. Update Attendance2_Defects_Gaps_and_Architecture_Inconsistencies_Report.md
# ==============================================================================
file1 = "Attendance2_Defects_Gaps_and_Architecture_Inconsistencies_Report.md"
with open(file1, "r", encoding="utf-8") as f:
    text1 = f.read()

# Replace line 185 & Row 15 & Total row in report
old_dash = """> **Live Execution Progress to Date:** **598 Test Cases Executed** (546 Passed, 52 Failed, 929 Not-Run) — **91.3% Pass Rate on Executed Tests**

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
| **TOTAL** | **All 17 Modules Combined** | **1,579** | **686** | **667** | **213** | **13** | **546** | **52** | **981** | **37.9%** | 🎯 **598 Executed (546 Pass, 52 Fail — 91.3% Pass Rate)** |"""

new_dash = """> **Live Execution Progress to Date:** **598 Test Cases Executed** (563 Passed, 35 Failed, 929 Not-Run) — **94.1% Pass Rate on Executed Tests**

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
| **15** | **User Scenarios (Add Here)** | 138 | 31 | 80 | 27 | 0 | **129** | **9** | **0** | **100.0%** | 🟢 **100% Executed (93.5% Pass Rate)** |
| **16** | **Holiday Calendar - Test Cases** | 310 | 172 | 130 | 8 | 0 | **288** | **22** | **0** | **100.0%** | 🚀 **100% Executed (92.9% Pass Rate)** |
| **17** | **CDWT - Manual DTO Validations** | 52 | 27 | 20 | 5 | 0 | 0 | 0 | 52 | 0.0% | 📝 Ready for Manual Testing |
| **TOTAL** | **All 17 Modules Combined** | **1,579** | **686** | **667** | **213** | **13** | **563** | **35** | **981** | **37.9%** | 🎯 **598 Executed (563 Pass, 35 Fail — 94.1% Pass Rate)** |"""

if old_dash in text1:
    text1 = text1.replace(old_dash, new_dash)
    print("Replaced execution dashboard in report.")
else:
    print("WARNING: old_dash not found in report.")

# Replace Finding 2
old_f2 = """> 2. **`User Scenarios (Add Here)` (Module 15):** **100% completed across all 138 test cases** covering Company Default setup, type migrations, immutability locks, boundary conditions, Part 1 & 2 defect re-verifications, and Attendance 4 real-world lifecycle runs, with **112 Passed and 26 Failed (81.2% Pass Rate)**."""
new_f2 = """> 2. **`User Scenarios (Add Here)` (Module 15):** **100% completed across all 138 test cases**. Live re-verification confirmed that **17 historical validation defects have been resolved** (empty PATCH returns 400 validation, 25h duration returns 400, 7-day math invariants return 400, negative grace/break return 400, and split overlapping intervals return 400 instead of HTTP 500 crash). The module now stands at **129 Passed and 9 Failed (93.5% Pass Rate)**, with the remaining 9 failures tied to 4 core architectural defects (`DEFECT-20261026-01` through `04`)."""

if old_f2 in text1:
    text1 = text1.replace(old_f2, new_f2)
    print("Replaced Finding 2 in report.")
else:
    print("WARNING: old_f2 not found in report.")

with open(file1, "w", encoding="utf-8") as f:
    f.write(text1)
print(f"Updated {file1} successfully.")


# ==============================================================================
# 2. Update Defects/Attendance2_Master_Defect_Log.md
# ==============================================================================
file2 = "Defects/Attendance2_Master_Defect_Log.md"
with open(file2, "r", encoding="utf-8") as f:
    text2 = f.read()

# Replace Section 1.1 dashboard table in Master Defect Log
old_m_dash = """> **Live Execution Progress to Date:** **598 Test Cases Executed** (546 Passed, 52 Failed, 929 Not-Run) — **91.3% Pass Rate on Executed Tests**

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
| **TOTAL** | **All 17 Modules Combined** | **1,579** | **686** | **667** | **213** | **13** | **546** | **52** | **981** | **37.9%** | 🎯 **598 Executed (546 Pass, 52 Fail — 91.3% Pass Rate)** |"""

new_m_dash = """> **Live Execution Progress to Date:** **598 Test Cases Executed** (563 Passed, 35 Failed, 929 Not-Run) — **94.1% Pass Rate on Executed Tests**

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
| **15** | **User Scenarios (Add Here)** | 138 | 31 | 80 | 27 | 0 | **129** | **9** | **0** | **100.0%** | 🟢 **100% Executed (93.5% Pass Rate)** |
| **16** | **Holiday Calendar - Test Cases** | 310 | 172 | 130 | 8 | 0 | **288** | **22** | **0** | **100.0%** | 🚀 **100% Executed (92.9% Pass Rate)** |
| **17** | **CDWT - Manual DTO Validations** | 52 | 27 | 20 | 5 | 0 | 0 | 0 | 52 | 0.0% | 📝 Ready for Manual Testing |
| **TOTAL** | **All 17 Modules Combined** | **1,579** | **686** | **667** | **213** | **13** | **563** | **35** | **981** | **37.9%** | 🎯 **598 Executed (563 Pass, 35 Fail — 94.1% Pass Rate)** |"""

if old_m_dash in text2:
    text2 = text2.replace(old_m_dash, new_m_dash)
    print("Replaced dashboard in master defect log.")
else:
    print("WARNING: old_m_dash not found in master defect log.")

# Add Section 1.2: Priority Failed User Scenarios (Module 15 Audit)
user_audit_sec = """
### 1.2. Priority Failed User Scenarios (Module 15 Audit & Live Reproduction)

During live re-verification of the **138 User Scenarios** (`User Scenarios (Add Here)`), **17 historical validation defects were verified as FIXED** (empty PATCH, 25h duration, 7-day math invariants, and split overlapping intervals now return RFC 9110 HTTP 400 validation errors instead of HTTP 500 crashes).

Only **9 test cases remain FAILED**, representing **4 core architectural, multi-tenancy, and cross-service defects**:

| TC ID | Row | Priority | Scenario Description | Live Expected vs. Observed Failure | Target Defect ID |
| :--- | :---: | :---: | :--- | :--- | :---: |
| **`USER-01`** | Row 2 | 🟡 P2 | `CompanyChecklist.WorkSchedulesCreated` update | CDWT created with 200 OK, but `CompanyChecklist.WorkSchedulesCreated` remains `false` in `SP.CompanySvc` | [`DEFECT-20261026-01`](#defect-20261026-01) |
| **`USER-128`** | Row 129 | 🟡 P2 | Cross-service checklist sync on Attendance 3 | Same cross-service sync failure confirmed live on Attendance 3 and Attendance 8 | [`DEFECT-20261026-01`](#defect-20261026-01) |
| **`USER-02`** | Row 3 | 🟠 P1 | `TenantName` empty object in MongoDB | `TenantName` persists as `Object (empty)` `{}` in MongoDB `ERP.Attendance.WorkTemplates` | [`DEFECT-20261026-02`](#defect-20261026-02) |
| **`USER-129`** | Row 130 | 🟠 P1 | `TenantName` auto-population from JWT | Confirmed persisting `{}` on Attendance 8 v1.0 and v2.0 MongoDB documents | [`DEFECT-20261026-02`](#defect-20261026-02) |
| **`USER-03`** | Row 4 | 🟡 P2 | `CreatedBy` plain email string formatting | `CreatedBy` persists raw email `"syed.mohamed@comm-it.in"` instead of composite user object | [`DEFECT-20261026-03`](#defect-20261026-03) |
| **`USER-130`** | Row 131 | 🟡 P2 | Composite identity structure consistency | Plain string email persists across all collections (`WorkTemplates`, `HolidayCalendars`) | [`DEFECT-20261026-03`](#defect-20261026-03) |
| **`USER-04`** | Row 5 | 🟡 P2 | Request body DTO scoping parameter redundancy | `tenantName` still declared in body DTOs across 26 POST/PATCH controller actions | [`DEFECT-20261026-04`](#defect-20261026-04) |
| **`USER-122`** | Row 123 | 🟠 P1 | Client-spoofed `tenantName` accepted in PATCH | **CRITICAL:** Sending `"tenantName": {"en": "Hacked Tenant Corp"}` in PATCH returns HTTP 200 and saves into MongoDB! | [`DEFECT-20261026-04`](#defect-20261026-04) |
| **`USER-131`** | Row 132 | 🟡 P2 | Re-verify Swagger body DTO parameter pollution | Full scan confirms 26 controller endpoints still accept client-sent `tenantName` | [`DEFECT-20261026-04`](#defect-20261026-04) |

#### Live Photographic & Database Evidence for `USER-122` (`DEFECT-20261026-04`)
* **Company Tested:** `Attendance 8` (`3a249871-7a8d-dec5-2d72-47795dd2662d`)
* **Endpoint:** `PATCH /api/companies/{companyId}/worktemplates/fixed/{id}`
* **Payload Sent:**
  ```json
  {
    "tenantName": { "en": "Hacked Tenant Corp" },
    "templateName": { "en": "Attendance 8 CDWT v2.0", "ar": "دوام محدث 2.0" },
    "fixedTimeSlots": [ ... ]
  }
  ```
* **Server Response:** `HTTP 200 OK` (New document created: `9e9adec9-2b9f-4504-b43b-303f6ebd1799`, Version: `3.0`)
* **Live MongoDB Document State:**
  ```json
  {
    "_id": "9e9adec9-2b9f-4504-b43b-303f6ebd1799",
    "Version": "3.0",
    "Status": "Active",
    "TenantName": {
      "en": "Hacked Tenant Corp"
    },
    "CreatedBy": "syed.mohamed@comm-it.in"
  }
  ```
* **Impact:** Any authenticated user can overwrite tenant name branding and master data by injecting arbitrary JSON into request bodies.
"""

if "### 1.1. Overall Consolidated Test Execution Dashboard (All 16 Modules)" in text2 and "### 1.2. Priority Failed User Scenarios" not in text2:
    # Insert right after section 1.1 table
    target_pos = text2.find("---\n\n## 2. Master Defect Quick-Reference Matrix")
    if target_pos != -1:
        text2 = text2[:target_pos] + user_audit_sec + "\n---\n\n## 2. Master Defect Quick-Reference Matrix" + text2[target_pos + len("---\n\n## 2. Master Defect Quick-Reference Matrix"):]
        print("Inserted Section 1.2 in master defect log successfully.")

with open(file2, "w", encoding="utf-8") as f:
    f.write(text2)
print(f"Updated {file2} successfully.")

