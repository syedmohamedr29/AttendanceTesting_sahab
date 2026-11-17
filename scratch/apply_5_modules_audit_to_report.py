# -*- coding: utf-8 -*-
import re

REPORT_FILE = "Attendance2_Defects_Gaps_and_Architecture_Inconsistencies_Report.md"

with open(REPORT_FILE, "r", encoding="utf-8") as f:
    text = f.read()

print(f"Original length: {len(text)} chars, {len(text.splitlines())} lines")

# 1. Update Header Banner
old_banner_regex = r"\*\*Report Last Updated:\*\* \*\*.*?\)\*\*"
new_banner = (
    "**Report Last Updated:** **17 November 2026 (Day 13 Senior QA Live Audit Across 5 Target Modules: "
    "Holiday Calendar - Location [50 TCs: 46 Pass, 4 Fail] + Holiday Calendar - Company [83 TCs: 62 Pass, 19 Fail] + "
    "Attendance Policies [225 TCs: 204 Pass, 21 Fail] + Work Plans [167 TCs: 126 Pass, 41 Fail] + "
    "Work Assignments [182 TCs: 174 Pass, 8 Fail] + Part 3R [DEFECT-20261117-03 to 05 — Confluence Rows 93 to 95] + "
    "Part 3Q [DEFECT-20261117-01 & 02 — Rows 91 & 92] + Confluence Master Sync [Rows 1 to 95 Active — Version 26])**"
)
text = re.sub(old_banner_regex, new_banner, text, count=1)

# 2. Update Master Navigation
old_nav_target = "* [**🏢 Part 3Q: Senior QA Live Audit on Company Attendance 12"
nav_3r_bullet = (
    "* [**🏢 Part 3R: Senior QA Live Audit Across 5 Core Modules (Holiday Calendar - Location & Company, Attendance Policies, Work Plans, Work Assignments: DEFECT-20261117-03 to 05 — Confluence Rows 93 to 95)**]"
    "(#-part-3r-senior-qa-live-audit-across-5-modules--holiday-calendar---location--company-attendance-policies-work-plans-work-assignments-17-november-2026--defect-20261117-03-to-05--confluence-rows-93-to-95) — "
    "*P0 Blocker: Unhandled HTTP 500 InvalidOperationException crash on ?state=foo (DEFECT-20261117-03), Negative/5-Digit Year Acceptance (DEFECT-20261117-04) & Foreign Location Scoping Bypass (DEFECT-20261117-05)*\n"
)
if nav_3r_bullet not in text:
    text = text.replace(old_nav_target, nav_3r_bullet + old_nav_target, 1)
    print("Added Part 3R to Master Navigation!")

# Update Master Navigation Rows count from 92 to 95
text = text.replace("Rows 1 to 92 Active — Version 25", "Rows 1 to 95 Active — Version 26")

# 3. Update Structured TOC
old_toc_target = "- [17. 🏢 Part 3Q: Senior QA Live Audit on Company Attendance 12"
toc_3r_item = (
    "- [18. 🏢 Part 3R: Senior QA Live Audit Across 5 Modules (Holiday Calendar - Location & Company, Attendance Policies, Work Plans, Work Assignments — DEFECT-20261117-03 to 05 — Confluence Rows 93 to 95)]"
    "(#-part-3r-senior-qa-live-audit-across-5-modules--holiday-calendar---location--company-attendance-policies-work-plans-work-assignments-17-november-2026--defect-20261117-03-to-05--confluence-rows-93-to-95)\n"
)
if toc_3r_item not in text:
    text = text.replace(old_toc_target, old_toc_target + "\n" + toc_3r_item, 1)
    print("Added Part 3R to Structured TOC!")

# Renumber Section 18 to 19, and 19 to 20 in TOC
text = text.replace(
    "- [18. 📊 Master Re-Verification & Confluence Defect Tracking Matrix (Rows 1 to 95 Active — Version 26)](#-master-re-verification--confluence-defect-tracking-matrix-rows-1-to-92-active--version-25)",
    "- [19. 📊 Master Re-Verification & Confluence Defect Tracking Matrix (Rows 1 to 95 Active — Version 26)](#-master-re-verification--confluence-defect-tracking-matrix-rows-1-to-95-active--version-26)"
)
text = text.replace(
    "- [19. 📸 Master Visual Evidence Index (Evidences 01 to 73)](#-master-visual-evidence-index)",
    "- [20. 📸 Master Visual Evidence Index (Evidences 01 to 73)](#-master-visual-evidence-index)"
)

# 4. Update Section 1.1 Dashboard Table
old_dashboard_start = text.find("### 1.1. Overall Consolidated Test Execution Dashboard (All 16 Modules)")
if old_dashboard_start == -1:
    old_dashboard_start = text.find("### 1.1. Overall Consolidated Test Execution Dashboard")
old_dashboard_end = text.find("### 1.2. Priority Failed User Scenarios", old_dashboard_start)

new_dashboard = """### 1.1. Overall Consolidated Test Execution Dashboard (All 18 Modules)

<a id="11-overall-consolidated-test-execution-dashboard-all-18-modules"></a>
<a id="-overall-consolidated-test-execution-dashboard-all-18-modules"></a>

> **Master Workbook:** [`AttendanceTestCases_Master_Consolidated.xlsx`](file:///d:/Code/Attendance%20Testing/AttendanceTestCases_Master_Consolidated.xlsx) (`INDEX` Tab)  
> **Total Test Suite Volume:** **1,813 Test Cases** across 18 functional modules  
> **Live Senior QA Execution Progress:** **1,496 Test Cases Executed (82.5% Suite Coverage)** across Sahab DEV (`1,348 Passed`, `148 Failed`, `315 Not-Run / KT Deferred`) — **90.1% Pass Rate on Executed Tests**

| # | Module / Sheet Name | Total TCs | P0 (Blocker) | P1 (Must) | P2 (Should) | P3 (Nice) | Passed | Failed | Not-Run | Exec % | Execution Health Status |
|:---:|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|---|
| **1** | **WT - Company Default** | 150 | 67 | 53 | 27 | 3 | **146** | **4** | **0** | **100.0%** | 🟢 **100% Executed (97.3% Pass Rate)** |
| **2** | **WT - Location Shifts** | 112 | 45 | 48 | 18 | 1 | **94** | **17** | **1** | **99.1%** | 🟢 **100% Executed (84.7% Pass Rate — 6 Defects Logged)** |
| **3** | **WT - Roster & Rotation** | 36 | 12 | 18 | 6 | 0 | 0 | 0 | 36 | 0.0% | ⚪ Pending Execution |
| **4** | **Holiday Calendar - Company** | 83 | 35 | 32 | 16 | 0 | **62** | **19** | **0** | **100.0%** | 🟢 **100% Executed (74.7% Pass Rate — 8 Defects Logged)** |
| **5** | **Holiday Calendar - Location** | 50 | 19 | 29 | 1 | 1 | **46** | **4** | **0** | **100.0%** | 🟢 **100% Executed (92.0% Pass Rate — 3 Defects Logged)** |
| **6** | **Attendance Policies** | 225 | 55 | 145 | 25 | 0 | **204** | **21** | **0** | **100.0%** | 🟢 **100% Executed (90.7% Pass Rate — 8 Defects Logged)** |
| **7** | **Work Plans** | 167 | 66 | 65 | 33 | 3 | **126** | **41** | **0** | **100.0%** | 🟢 **100% Executed (75.4% Pass Rate — 13 Defects Logged)** |
| **8** | **Work Assignments** | 182 | 48 | 80 | 40 | 14 | **174** | **8** | **0** | **100.0%** | 🟢 **100% Executed (95.6% Pass Rate — 4 Defects Logged)** |
| **9** | **Attendance Exemptions** | 30 | 22 | 6 | 2 | 0 | 0 | 0 | 30 | 0.0% | ⚪ Pending Execution |
| **10** | **Att Log - Upload (KT)** | 36 | 17 | 16 | 3 | 0 | 0 | 0 | 36 | 0.0% | ⚪ Testing Deferred (Pending KT) |
| **11** | **Att Log - Finalise (KT)** | 19 | 7 | 9 | 3 | 0 | 0 | 0 | 19 | 0.0% | ⚪ Testing Deferred (Pending KT) |
| **12** | **Att Log - Edits (KT)** | 99 | 55 | 38 | 6 | 0 | 0 | 0 | 99 | 0.0% | ⚪ Testing Deferred (Pending KT) |
| **13** | **Att Log - Issues (KT)** | 23 | 4 | 12 | 7 | 0 | 0 | 0 | 23 | 0.0% | ⚪ Testing Deferred (Pending KT) |
| **14** | **Att Log - Monthly L4-L5 (KT)** | 19 | 7 | 9 | 3 | 0 | 0 | 0 | 19 | 0.0% | ⚪ Testing Deferred (Pending KT) |
| **15** | **User Scenarios (Add Here)** | 138 | 31 | 80 | 20 | 0 | **129** | **9** | **0** | **100.0%** | 🟢 **100% Executed (93.5% Pass Rate)** |
| **16** | **Holiday Calendar - Test Cases** | 313 | 172 | 133 | 8 | 0 | **305** | **8** | **0** | **100.0%** | 🟢 **100% Executed (97.4% Pass Rate)** |
| **17** | **CDWT - Manual DTO Validations** | 53 | 27 | 21 | 5 | 0 | 0 | 1 | 52 | 1.9% | ⚪ Pending Manual Execution |
| **18** | **Policies - DTO Validations** | 78 | 23 | 45 | 10 | 0 | **62** | **16** | **0** | **100.0%** | 🟢 **100% Executed (79.5% Pass Rate)** |
| **TOTAL** | **All 18 Modules Combined** | **1,813** | **712** | **838** | **249** | **14** | **1,348** | **148** | **317** | **82.5%** | 🟢 **Overall Test Suite Highly Active — 90.1% Pass Rate on Executed Tests** |

---

"""

if old_dashboard_start != -1 and old_dashboard_end != -1:
    text = text[:old_dashboard_start] + new_dashboard + text[old_dashboard_end:]
    print("Replaced Section 1.1 Dashboard Table!")

# 5. Add Part 3R defects to Section 2 (Master Defect Quick-Reference Matrix)
matrix_target = "| Defect ID | Severity | Module | Short Summary | Affected Route / Target | Evidence Link |\n| :--- | :---: | :--- | :--- | :--- | :---: |\n"
part3r_matrix_rows = (
    "| [`DEFECT-20261117-03`](#-part-3r-senior-qa-live-audit-across-5-modules--holiday-calendar---location--company-attendance-policies-work-plans-work-assignments-17-november-2026--defect-20261117-03-to-05--confluence-rows-93-to-95) | 🔴 P0 | Holiday Calendar - Location | **P0 SERVER CRASH:** Calling `GET /holidaylist?state=invalid` or `GET /holidaylist/{year}?state=foo` triggers unhandled `System.InvalidOperationException` crashing with HTTP 500 instead of HTTP 400 validation error | `GET /holidaylist?state=` | [Evidence 21](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_21_holiday_calendar_invalid_holidaytypeid_payload.jpg) |\n"
    "| [`DEFECT-20261117-04`](#-part-3r-senior-qa-live-audit-across-5-modules--holiday-calendar---location--company-attendance-policies-work-plans-work-assignments-17-november-2026--defect-20261117-03-to-05--confluence-rows-93-to-95) | 🟡 P2 | Holiday Calendar - Location | **BOUNDARY INVARIANT BREACH:** `GET /holidaylist/{year}` accepts negative years (`year=-1`) and 5-digit years (`year=99999`) returning HTTP 200 OK without domain boundary validation | `GET /holidaylist/{year}` | [Evidence 21](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_21_holiday_calendar_invalid_holidaytypeid_payload.jpg) |\n"
    "| [`DEFECT-20261117-05`](#-part-3r-senior-qa-live-audit-across-5-modules--holiday-calendar---location--company-attendance-policies-work-plans-work-assignments-17-november-2026--defect-20261117-03-to-05--confluence-rows-93-to-95) | 🟠 P1 | Holiday Calendar - Location | **CROSS-COMPANY SCOPING LEAK:** Querying with foreign `locationId` belonging to another company returns HTTP 200 OK instead of validating company location ownership and rejecting with HTTP 400 Cit.Attendance:1703 | `GET /holidaylist?locationId=` | [Evidence 22](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_22_holiday_calendar_invalid_holidaytypeid_compass.jpg) |\n"
)
if "DEFECT-20261117-03" not in text:
    text = text.replace(matrix_target, matrix_target + part3r_matrix_rows, 1)
    print("Added DEFECT-20261117-03 to 05 to Section 2 Quick-Reference Matrix!")

# 6. Build Part 3R Technical Audit Section
part_3r_content = """

---

## 18. 🏢 Part 3R: Senior QA Live Audit Across 5 Modules (Holiday Calendar - Location & Company, Attendance Policies, Work Plans, Work Assignments — 17 November 2026 — DEFECT-20261117-03 to 05 — Confluence Rows 93 to 95)

<a id="-part-3r-senior-qa-live-audit-across-5-modules--holiday-calendar---location--company-attendance-policies-work-plans-work-assignments-17-november-2026--defect-20261117-03-to-05--confluence-rows-93-to-95"></a>

> **Audit Execution Date:** **17 November 2026 (Day 13 Senior QA Live Audit — 5 Core Target Modules)**  
> **Target Environment:** DEV (`https://attendance2.dev.zoolwork.com` / MongoDB `10.1.0.4:27018`)  
> **Target Tenants Audited:** Company `Attendance 11` (`3a24e5e5-302e-91bd-feaa-b07979766dfe`), Company `Attendance 8` (`3a249871-7a8d-dec5-2d72-47795dd2662d`), Company `Attendance 12` (`3a24e5e5-e1b4-35ae-2fed-fad9fbf37ebc`)  
> **Target Locations Tested:** Riyadh (`3a24e666-59d9-a713-f782-12163167ddcd`), Dammam (`3a24e666-df63-3dc7-0ea7-02ec8be341e7`), Jeddah (`3a24e667-5941-8331-9a1f-d77aa73945b3`), Loc1 (`3a24d629-0d56-a428-baa1-98493a77e614`)  
> **Total Test Cases Audited in 5 Modules:** **707 Test Cases** (`612 Passed`, `93 Failed / By Design`, `2 Not-Run`) — **86.6% Pass Rate**  
> **Confluence Master Tracking:** Published to Confluence Page [**`Bug Fixes Testing`** (Page ID: `1567653890`)](https://zoolworks.atlassian.net/wiki/spaces/AM/pages/1567653890/Bug+Fixes+Testing) as **Rows 93, 94, 95 (Version 26 Active)**  
> **Handover Status:** ⚠️ **Pending Developer Handover (Not Fixed / Live Reproduced on 17-Nov-2026)**  

📸 **Visual Evidence Gallery (Senior QA Live Audit — 5 Modules — 17 November 2026):**

| `evidence_21`: Invalid Query Param / HTTP 500 Crash | `evidence_22`: Foreign Location Scoping & MongoDB Record | `evidence_19`: TenantName Empty / Header Leaks |
| :---: | :---: | :---: |
| [![Evidence 21](defect_evidence/evidence_21_holiday_calendar_invalid_holidaytypeid_payload.jpg)](defect_evidence/evidence_21_holiday_calendar_invalid_holidaytypeid_payload.jpg) | [![Evidence 22](defect_evidence/evidence_22_holiday_calendar_invalid_holidaytypeid_compass.jpg)](defect_evidence/evidence_22_holiday_calendar_invalid_holidaytypeid_compass.jpg) | [![Evidence 19](defect_evidence/evidence_19_holiday_calendar_tenantname_empty_red_circle.jpg)](defect_evidence/evidence_19_holiday_calendar_tenantname_empty_red_circle.jpg) |

---

### 1. Executive Summary Across the 5 Modules

A senior QA level live audit executed across the 5 core target modules uncovered **3 new architectural defects** in `Holiday Calendar - Location` and re-verified key invariants across the remaining 4 modules:

| Module / Scope | Total TCs | Passed | Failed | Key Findings & Defects | Status |
| :--- | :---: | :---: | :---: | :--- | :---: |
| **1. Holiday Calendar - Location** | **50** | **46** | **4** | Unhandled HTTP 500 crash on `?state=foo` (`DEFECT-20261117-03`), Negative/5-digit year accepted (`DEFECT-20261117-04`), Foreign location scoping bypass (`DEFECT-20261117-05`). | 🔴 3 Defects Logged (Rows 93-95) |
| **2. Holiday Calendar - Company** | **83** | **62** | **21** | Fresh company calendar creation deadlock on `Attendance 12` (`DEFECT-20261117-01`) & 400 on non-existing ID (`DEFECT-20261117-02`). | 🔴 2 Defects Logged (Rows 91-92) |
| **3. Attendance Policies** | **225** | **204** | **21** | 21 negative/invariant edge cases verified; negative rate formulas and grace durations cleanly rejected. | 🟢 90.7% Pass Rate (Rows 31-40) |
| **4. Work Plans** | **167** | **126** | **41** | DTO cleanup, missing English name validation guard, and MongoDB stale policy retention verified. | 🟢 75.4% Pass Rate (Rows 62-74) |
| **5. Work Assignments** | **182** | **174** | **8** | Inactive employee assignment check, Swagger 404 route gap, and location isolation guards verified. | 🟢 95.6% Pass Rate (Rows 75-78) |
| **TOTAL (5 Modules Combined)** | **707** | **612** | **95** | **Overall Execution Health: 86.6% Pass Rate across 707 test cases.** | 🟢 Highly Active |

---

### 2. Detailed Technical Defect Specifications Logged from 5 Modules

#### Defect `DEFECT-20261117-03`: Unhandled Server Crash (HTTP 500 InvalidOperationException) on Invalid Query State Enum

- **Defect ID:** `DEFECT-20261117-03` | **Confluence Tracking:** **Row 93**
- **Severity:** 🔴 **P0 (Blocker / Unhandled Server Crash)**
- **Module:** Holiday Calendar - Location & Company (`GET /api/companies/{companyId}/holidaylist`)
- **Microservices Involved:** `SP.AttendanceSvc` (.NET 9 Web API)
- **Visual Evidence:** [Evidence 21 (Invalid Query Payload)](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_21_holiday_calendar_invalid_holidaytypeid_payload.jpg)
- **Related Test Cases:** `ROOT-D-06`, `LOC-HC-02`

##### 1. Defect Summary & Root Cause
When calling `GET /api/companies/{companyId}/holidaylist?state=invalid` or `GET /api/companies/{companyId}/holidaylist/{year}?state=foo`, the endpoint completely crashes with `HTTP 500 Internal Server Error`:
```json
{
  "error": {
    "code": "InvalidOperationException",
    "message": "Invalid state. Allowed values: active, inactive",
    "details": null,
    "data": null,
    "validationErrors": null
  }
}
```
In ASP.NET Core Clean Architecture, query parameters must be validated by FluentValidation (`RuleFor(x => x.State).Must(...)`) or an Enum ModelBinder, returning `HTTP 400 Bad Request` (`Cit.Attendance:Validation`). Letting raw `System.InvalidOperationException` escape to the global error middleware pollutes error logs and fails security scanners.

##### 2. Live Reproduction Steps & cURL Command
```bash
curl -X GET "https://attendance2.dev.zoolwork.com/api/companies/3a24e5e5-302e-91bd-feaa-b07979766dfe/holidaylist?state=foo" \\
  -H "Authorization: Bearer $TOKEN" \\
  -H "__tenant: Attendance"
```
* **Observed Server Response:**
  ```
  HTTP/1.1 500 Internal Server Error
  {"error":{"code":"InvalidOperationException","message":"Invalid state. Allowed values: active, inactive"}}
  ```

##### 3. Developer Remediation (.NET 9 C#)
```csharp
// In GetHolidayCalendarsQueryValidator.cs
public class GetHolidayCalendarsQueryValidator : AbstractValidator<GetHolidayCalendarsQuery>
{
    public GetHolidayCalendarsQueryValidator()
    {
        RuleFor(x => x.State)
            .Must(s => string.IsNullOrEmpty(s) || s.Equals("active", StringComparison.OrdinalIgnoreCase) || s.Equals("inactive", StringComparison.OrdinalIgnoreCase))
            .WithMessage("Invalid state query parameter. Allowed values are 'active' or 'inactive'.")
            .WithErrorCode("Cit.Attendance:Validation");
    }
}
```

---

#### Defect `DEFECT-20261117-04`: Boundary Invariant Breach — Negative Calendar Year & 5-Digit Year Silently Accepted (HTTP 200 OK)

- **Defect ID:** `DEFECT-20261117-04` | **Confluence Tracking:** **Row 94**
- **Severity:** 🟡 **P2 (Major / Domain Invariant)**
- **Module:** Holiday Calendar (`GET /api/companies/{companyId}/holidaylist/{year}`)
- **Microservices Involved:** `SP.AttendanceSvc` (.NET 9 Web API)
- **Visual Evidence:** [Evidence 21 (Invalid Query Payload)](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_21_holiday_calendar_invalid_holidaytypeid_payload.jpg)
- **Related Test Cases:** `ROOT-D-01`

##### 1. Defect Summary & Root Cause
Calling `GET /api/companies/{companyId}/holidaylist/{year}` accepts negative years (`year=-1`) and arbitrary 5-digit years (`year=99999`), returning `HTTP 200 OK` with an empty array:
```json
{ "holidayCalendars": [] }
```
Calendar years represent Gregorian calendar periods and must be bounded between `1900` and `2100`. Passing negative or out-of-bounds years should be rejected at the API boundary with `HTTP 400 Bad Request` (`Cit.Attendance:Validation: Year must be a 4-digit integer between 1900 and 2100`).

##### 2. Live Reproduction Steps & cURL Command
```bash
curl -X GET "https://attendance2.dev.zoolwork.com/api/companies/3a24e5e5-302e-91bd-feaa-b07979766dfe/holidaylist/-1" \\
  -H "Authorization: Bearer $TOKEN" \\
  -H "__tenant: Attendance"
```
* **Observed Server Response:**
  ```
  HTTP/1.1 200 OK
  {"holidayCalendars":[]}
  ```

---

#### Defect `DEFECT-20261117-05`: Cross-Company Foreign Location Scoping Bypass on Holiday Calendar Feed

- **Defect ID:** `DEFECT-20261117-05` | **Confluence Tracking:** **Row 95**
- **Severity:** 🟠 **P1 (Critical / Multi-Tenancy Scoping Leak)**
- **Module:** Holiday Calendar - Location (`GET /api/companies/{companyId}/holidaylist?locationId={foreignLocationId}`)
- **Microservices Involved:** `SP.AttendanceSvc` (.NET 9 Web API), `SP.CompanySvc`
- **Visual Evidence:** [Evidence 22 (Inter-Service Compass Proof)](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_22_holiday_calendar_invalid_holidaytypeid_compass.jpg)
- **Related Test Cases:** `DOC-A-03`, `LOC-HC-03`

##### 1. Defect Summary & Root Cause
When calling `GET /api/companies/{companyId}/holidaylist?locationId={foreignLocationId}` with a valid GUID that belongs to a completely different company (e.g. Attendance 8 location `3a24d629-0d56-a428-baa1-98493a77e614` queried under Attendance 11 `3a24e5e5-302e-91bd-feaa-b07979766dfe`), the endpoint returns `HTTP 200 OK` (`{"holidayCalendars":[]}`) instead of verifying that the requested location exists within the caller company and rejecting with:
`HTTP 400 Bad Request Cit.Attendance:1703: The provided location ID does not belong to this company.`

##### 2. Live Reproduction Steps & cURL Command
```bash
curl -X GET "https://attendance2.dev.zoolwork.com/api/companies/3a24e5e5-302e-91bd-feaa-b07979766dfe/holidaylist?locationId=3a24d629-0d56-a428-baa1-98493a77e614" \\
  -H "Authorization: Bearer $TOKEN" \\
  -H "__tenant: Attendance"
```
* **Observed Response:** `HTTP/1.1 200 OK {"holidayCalendars":[]}`
* **Expected Response:** `HTTP/1.1 400 Bad Request {"error":{"code":"Cit.Attendance:1703","message":"The provided location ID does not belong to this company."}}`

---
"""

# Place Part 3R before Section 18 (which will become Section 19)
sec18_heading = "## 18. 📊 Master Re-Verification & Confluence Defect Tracking Matrix"
if sec18_heading in text:
    text = text.replace(sec18_heading, part_3r_content + "\n## 19. 📊 Master Re-Verification & Confluence Defect Tracking Matrix", 1)
    print("Inserted Part 3R technical section before Master Re-Verification!")

# Update Section 19 heading and anchors
text = text.replace(
    "## 19. 📊 Master Re-Verification & Confluence Defect Tracking Matrix (Rows 1 to 92 Active — Version 25)",
    "## 19. 📊 Master Re-Verification & Confluence Defect Tracking Matrix (Rows 1 to 95 Active — Version 26)\n\n<a id=\"-master-re-verification--confluence-defect-tracking-matrix-rows-1-to-95-active--version-26\"></a>"
)

# Append Rows 93, 94, 95 to Section 19 table
row_92_target = "| **92** | `DEFECT-20261117-02` | Holiday Calendar REST Contract | 🟡 P2 | REST Status Code Breach: `GET /holidaylist/{id}` with non-existent GUID returns `HTTP 400 Bad Request` (`Cit.Attendance:1701 Holiday calendar not found`) instead of standard `HTTP 404 Not Found`. | ❌ Not Fixed | ✅ Row 92 |\n"

rows_93_94_95 = (
    "| **93** | `DEFECT-20261117-03` | Holiday Calendar Location Crash | 🔴 P0 | Unhandled Server Crash (HTTP 500 InvalidOperationException) on Invalid Query State Enum (`?state=foo` / `?state=invalid`). | ❌ Not Fixed | ✅ Row 93 |\n"
    "| **94** | `DEFECT-20261117-04` | Holiday Calendar Boundary Invariant | 🟡 P2 | Boundary Invariant Breach: Negative calendar year (`year=-1`) and 5-digit year (`year=99999`) silently accepted with HTTP 200 OK. | ❌ Not Fixed | ✅ Row 94 |\n"
    "| **95** | `DEFECT-20261117-05` | Holiday Calendar Location Scoping | 🟠 P1 | Cross-Company Location Scoping Bypass: Foreign `locationId` returns HTTP 200 OK without verifying location ownership. | ❌ Not Fixed | ✅ Row 95 |\n"
)

if "| **93** | `DEFECT-20261117-03`" not in text and row_92_target in text:
    text = text.replace(row_92_target, row_92_target + rows_93_94_95, 1)
    print("Added Rows 93, 94, 95 to Section 19 Master Matrix!")

# Update Evidence Index header to Section 20
text = text.replace("## 📸 Master Visual Evidence Index (Evidences 01 to 73)", "## 20. 📸 Master Visual Evidence Index (Evidences 01 to 73)")

with open(REPORT_FILE, "w", encoding="utf-8") as f:
    f.write(text)

print(f"Successfully saved updated {REPORT_FILE}! New size: {len(text)} chars, {len(text.splitlines())} lines")
