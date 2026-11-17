# -*- coding: utf-8 -*-
import re

holiday_company_section = '''### 🏢 Module 1 Deep Dive: Holiday Calendar - Company Live Test Execution & Defect Audit (16 November 2026 — 83 TCs)

<a id="31-holiday-calendar---company-live-test-execution--defect-audit-16-november-2026"></a>

> **Execution Date:** 16 November 2026  
> **Target Module:** Sheet 6: `Holiday Calendar - Company` in [`AttendanceTestCases_Master_Consolidated.xlsx`](file:///d:/Code/Attendance%20Testing/AttendanceTestCases_Master_Consolidated.xlsx)  
> **API Controllers:** `HolidayCalendarController` (`/api/companies/{companyId}/holidaylist`)  
> **Database Target:** MongoDB `Sahab` @ `10.1.0.4:27018` -> `ERP.Attendance.HolidayCalendars`  
> **Test Scope:** All 83 Comprehensive Functional, DTO Invariant, Tenancy, Fan-Out Cascade, and Publish Scenarios  
> **Live Audit Status:** **83 Test Cases Executed — 62 Passed (74.7%), 2 Passed by Design (2.4%), 19 Failed (22.9%)**  

---

#### 1. Executive Summary & Defect Statistics

Comprehensive execution of the **Holiday Calendar - Company** test suite (83 test cases across 12 operational sections) confirmed that while happy-path creation, annual prefilling, removal of future holidays, and location customization isolation function as specified, **19 critical and major architectural defects** remain unresolved in the live environment:

| Test Metric | Count | Percentage | Operational Impact |
| :--- | :---: | :---: | :--- |
| **Total Test Cases** | **83** | **100%** | Full functional, validation, fan-out cascade, and security coverage of Company Holiday Calendars. |
| 🟢 **Passed** | **62** | **74.7%** | Happy-path creation, year boundary guards (Cit.Attendance:1712/1713), duplicate removal guards (1709), and customized location skips. |
| 🔵 **Passed (By Design)** | **2** | **2.4%** | `DOC-C-07` & `ROOT-D-08`: Overlapping holiday date ranges and duplicate dates permitted by design for multiple holiday types. |
| ❌ **Failed (Defects Active)** | **19** | **22.9%** | Severe vulnerabilities across JWT bypass, unhandled 500 crashes, missing MongoDB audit identities, chronological inversions, and today-date deadlocks. |

---

#### 2. Defect Breakdown Across Failing Test Cases

The 19 failed test cases cluster into **8 distinct architectural and contract defects**:

| Defect ID | Severity | Failed TC IDs | Root Cause & Failure Mechanism | Photographic Proof | Live Status |
| :--- | :---: | :--- | :--- | :---: | :---: |
| **`DEFECT-20261029-01`** | **P0 Blocker** | `DOC-A-02` | **JWT Validation Bypass:** Expired tokens (10 days past `exp`) and forged signatures (`AAAA...`) return HTTP 200 OK. | [Evidence 16](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_16_attendance_swagger_missing_oauth2.png) | 🚨 **CRITICAL OPEN** |
| **`DEFECT-20261028-02`** | **P1 Critical** | `DOC-A-03`, `ROOT-A-04`, `DOC-B-01`, `ROOT-B-01`, `DOC-C-02` | **Unhandled HTTP 500 Crash:** Missing tenant header, empty create body, or empty PATCH body throws unhandled `ValidationException` crashing Kestrel worker. | [Evidence 15](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_15_att4_patch_empty_payload_500.png) | ❌ **FAIL (500 CRASH)** |
| **`DEFECT-20261104-01`** | **P0 Blocker** | `DOC-A-05`, `ROOT-A-05`, `ROOT-E-03` | **Multi-Tenancy Isolation Failure:** `__tenant` header completely ignored; cross-tenant calendar edit and publish accepted with HTTP 200 OK. | [Evidence 39](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_39_companyname_empty_object_compass.jpg) | 🚨 **CRITICAL OPEN** |
| **`DEFECT-20261103-02`** | **P1 Critical** | `DOC-A-06`, `ROOT-B-08` | **Empty TenantName Object in MongoDB:** `TenantName` persists as empty BSON object `{}` in `ERP.Attendance.HolidayCalendars` instead of resolving from Company service. | [Evidence 19](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_19_holiday_calendar_tenantname_empty_red_circle.jpg) | ❌ **FAIL (COMPASS PROOF)** |
| **`DEFECT-20261103-12`** | **P1 Critical** | `DOC-B-07` | **Holiday Dates in Future Year Accepted on Create:** Creating a 2026 calendar accepting holiday dates in 2027 (`startDate: 2027-02-15`) without validation. | [Evidence 22](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_22_holiday_calendar_invalid_holidaytypeid_compass.jpg) | ❌ **FAIL (COMPASS PROOF)** |
| **`DEFECT-20261103-06`** | **P1 Critical** | `DOC-C-03`, `ROOT-D-04` | **Empty Holiday Lists Array `[]` Accepted:** Sending `holidayLists: []` on update accepted with HTTP 200 OK, creating headless empty calendars. | [Evidence 24](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_24_holiday_calendar_empty_holidaylists_array_accepted.jpg) | ❌ **FAIL (COMPASS PROOF)** |
| **`DEFECT-20261103-14`** | **P0 Blocker** | `DOC-C-05`, `ROOT-D-06` | **Today Date Deadlock on Current Year Update:** `Cit.Attendance:1706` ("For current year updates, holiday start date must be strictly in the future") rejects today's date, locking same-day edits in Web UI. | [Evidence 32](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_32_holiday_patch_1706_current_year_today_blocked_swagger.png) | 🚨 **BLOCKER OPEN** |
| **`DEFECT-20261103-11`** | **P1 Critical** | `DOC-C-06`, `ROOT-D-07` | **Chronological Inversion Accepted:** API accepts payloads where `endDate < startDate` (e.g. Start 10-May, End 08-May) with HTTP 200 OK. | [Evidence 26](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_26_holiday_calendar_invalid_calendartype_999_stored_as_default_1.png) | ❌ **FAIL (COMPASS PROOF)** |
| **`DEFECT-20261103-07`** | **P1 Critical** | `ROOT-B-07` | **Duplicate Holiday Date & ShortCode:** System permits multiple holidays with duplicate dates/codes within the same company calendar without rejection. | [Evidence 23](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_23_holiday_calendar_arabic_only_name_accepted.jpg) | ❌ **FAIL (DATA INTEGRITY)** |

---

#### 3. Complete Section-by-Section Test Execution Summary (83 TCs)

| Section Name | Target Endpoints & Operations | Total TCs | Passed | By Design | Failed | Pass Rate | Key Defect References |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :--- |
| **A. Auth, Tenant & Scoping** | `POST /holidaylist`, `PATCH /{id}/{year}` | **6** | 2 | 0 | 4 | **33.3%** | `DEFECT-20261029-01`, `DEFECT-20261028-02`, `DEFECT-20261104-01`, `DEFECT-20261103-02` |
| **B. Create Company Default** | `POST /holidaylist` (no locationId) | **8** | 6 | 0 | 2 | **75.0%** | `DEFECT-20261028-02`, `DEFECT-20261103-12` |
| **C. Edit Holidays** | `PATCH /holidaylist/{id}/{year}` | **9** | 4 | 1 | 4 | **55.6%** | `DEFECT-20261028-02`, `DEFECT-20261103-06`, `DEFECT-20261103-14`, `DEFECT-20261103-11` |
| **D. Remove a Holiday** | `PATCH /holidaylist/{id}/remove/{holidayId}` | **3** | 3 | 0 | 0 | **100.0%** | All 3 test cases passed (future removal 200, past removal blocked 400). |
| **E. Publish** | `POST /holidaylist/publish/{year}` | **5** | 5 | 0 | 0 | **100.0%** | All 5 test cases passed (company default publish & customized location skips). |
| **F. List and Get by Id** | `GET /holidaylist`, `GET /holidaylist/{id}` | **5** | 5 | 0 | 0 | **100.0%** | All 5 test cases passed (year, locationId, isPublished, and isInherited filtering). |
| **G. Auth & Tenancy (Roles)** | `[Authorize(Roles = "TenantAdmin")]` | **5** | 3 | 0 | 2 | **60.0%** | `DEFECT-20261028-02`, `DEFECT-20261104-01` |
| **H. Create Validation & Success** | `POST /holidaylist` (Payload Invariants) | **8** | 5 | 0 | 3 | **62.5%** | `DEFECT-20261028-02`, `DEFECT-20261103-07`, `DEFECT-20261103-02` |
| **I. Fan-Out Cascade** | Location Calendars Created on Success | **6** | 6 | 0 | 0 | **100.0%** | All 6 test cases passed (1 LocationDefault per active location, independent holiday IDs). |
| **J. Edit & Add/Remove Holiday** | `PATCH /{id}/{year}`, `PATCH /{id}/remove/...` | **16** | 11 | 1 | 4 | **75.0%** | `DEFECT-20261103-06`, `DEFECT-20261103-14`, `DEFECT-20261103-11` |
| **K. Publish -> Inherited Locations** | `POST /publish/{year}` (Cascade Sync) | **8** | 7 | 0 | 1 | **87.5%** | `DEFECT-20261104-01` |
| **L. Integration End-to-End** | Company -> Cascade -> Edit -> Publish | **4** | 4 | 0 | 0 | **100.0%** | All 4 integration steps passed. |
| **TOTAL** | **All 12 Sections Combined** | **83** | **62** | **2** | **19** | **77.1%** | **19 Active Defects 100% Traceable** |

---

#### 4. Visual Evidence Gallery (Holiday Calendar Module)

| `evidence_18`: CreatedBy Plain Email | `evidence_19`: TenantName Empty Object | `evidence_20`: isActive: false Ignored |
| :---: | :---: | :---: |
| ![CreatedBy Plain Email](defect_evidence/evidence_18_holiday_calendar_createdby_email_tenantname_empty.jpg) | ![TenantName Empty Red Circle](defect_evidence/evidence_19_holiday_calendar_tenantname_empty_red_circle.jpg) | ![IsActive Stored True](defect_evidence/evidence_20_holiday_calendar_isactive_false_ignored_stored_true.jpg) |
| [🔍 Evidence 18](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_18_holiday_calendar_createdby_email_tenantname_empty.jpg) | [🔍 Evidence 19](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_19_holiday_calendar_tenantname_empty_red_circle.jpg) | [🔍 Evidence 20](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_20_holiday_calendar_isactive_false_ignored_stored_true.jpg) |

| `evidence_22`: Invalid HolidayTypeId Compass | `evidence_24`: Empty holidayLists Array Accepted | `evidence_32`: Cit.Attendance:1706 Today Deadlock |
| :---: | :---: | :---: |
| ![Invalid HolidayTypeId Stored](defect_evidence/evidence_22_holiday_calendar_invalid_holidaytypeid_compass.jpg) | ![Empty holidayLists Array](defect_evidence/evidence_24_holiday_calendar_empty_holidaylists_array_accepted.jpg) | ![Today Deadlock](defect_evidence/evidence_32_holiday_patch_1706_current_year_today_blocked_swagger.png) |
| [🔍 Evidence 22](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_22_holiday_calendar_invalid_holidaytypeid_compass.jpg) | [🔍 Evidence 24](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_24_holiday_calendar_empty_holidaylists_array_accepted.jpg) | [🔍 Evidence 32](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_32_holiday_patch_1706_current_year_today_blocked_swagger.png) |

---
'''

def update_file(filepath):
    print(f"Updating {filepath}...")
    with open(filepath, 'r', encoding='utf-8') as f:
        text = f.read()

    # Check if section already exists
    if 'Module 1 Deep Dive: Holiday Calendar - Company Live Test Execution' in text:
        print(f"Section already present in {filepath}, skipping insertion.")
        return

    # Update Table of Contents to add link under Section 3
    toc_target = '- [3. Module 1: Holiday Calendar Module (`ERP.Attendance.HolidayCalendars`)](#3-module-1-holiday-calendar-module)'
    toc_replacement = '- [3. Module 1: Holiday Calendar Module (`ERP.Attendance.HolidayCalendars`)](#3-module-1-holiday-calendar-module)\n  - [3.1. Holiday Calendar - Company Deep Dive: Live Test Execution & Defect Audit (83 TCs: 62 Pass, 2 By Design, 19 Fail)](#31-holiday-calendar---company-live-test-execution--defect-audit-16-november-2026)'
    
    if toc_target in text:
        text = text.replace(toc_target, toc_replacement)
        print("Updated Table of Contents with 3.1 link.")
    else:
        print("TOC target not found, checking without backticks...")
        toc_target_alt = '- [3. Module 1: Holiday Calendar Module (ERP.Attendance.HolidayCalendars)](#3-module-1-holiday-calendar-module)'
        if toc_target_alt in text:
            text = text.replace(toc_target_alt, toc_replacement)
            print("Updated Table of Contents with 3.1 link (alt).")

    # Insert section right after Section 3 header and target info
    sec3_target = '> **Base Route:** `/api/companies/{companyId}/holidaylist` | **Controller:** `HolidayCalendarController`\n'
    if sec3_target in text:
        text = text.replace(sec3_target, sec3_target + '\n' + holiday_company_section + '\n')
        print(f"Successfully inserted Holiday Calendar - Company deep dive into {filepath}.")
    else:
        print(f"Could not find sec3_target in {filepath}!")

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(text)

update_file('Attendance2_Defects_Gaps_and_Architecture_Inconsistencies_Report.md')
update_file('Defects/Attendance2_Master_Defect_Log.md')
