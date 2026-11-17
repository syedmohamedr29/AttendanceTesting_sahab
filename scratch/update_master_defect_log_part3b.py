import re

filepath = 'Defects/Attendance2_Master_Defect_Log.md'

with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

target_end_part3 = """| **5** | [`DEFECT-20261026-03`](#defect-20261026-03) | `USER-03` (Row 4) & `USER-130` (Row 131) | Audit Trail / User Identity | 🟡 **P2 Major** | API / DB | **Plain Email in Audit Field `CreatedBy`:** `CreatedBy` persists as plain email string instead of standard composite user identity document `{ id, email, name }`. | ❌ **Not Fixed** | **Re-verified 2026-11-16:** Plain string email continues to persist across all collections instead of composite user identity object. | ✅ Row 3 |

---"""

part3b_section = """| **5** | [`DEFECT-20261026-03`](#defect-20261026-03) | `USER-03` (Row 4) & `USER-130` (Row 131) | Audit Trail / User Identity | 🟡 **P2 Major** | API / DB | **Plain Email in Audit Field `CreatedBy`:** `CreatedBy` persists as plain email string instead of standard composite user identity document `{ id, email, name }`. | ❌ **Not Fixed** | **Re-verified 2026-11-16:** Plain string email continues to persist across all collections instead of composite user identity object. | ✅ Row 3 |

---

### 📊 Part 3B: Live Execution of Holiday Calendar Test Cases (Attendance 2 & 3 - 29 October 2026) — Re-Verification Audit

> **Execution Date:** 16 November 2026 | **Suite:** Module 1 `Holiday Calendar - Test Cases` (313 TCs)  
> **Target Environment:** DEV (`https://attendance2.dev.zoolwork.com` / `https://company8.dev.zoolwork.com`) | **DB:** MongoDB `Sahab` on `10.1.0.4:27018`  
> **Confluence Sync:** Synced to Confluence Page **`Bug Fixes Testing`** (Page ID `1567653890`) under folder **`Attendance company testing`** (Rows 10 to 14)  
> **Suite Status:** **305 Passed (97.4%) | 8 Failed (2.6%)** across 29 functional sections.

#### Summary of Re-Verification Status:
- **🟢 Confirmed Fixed Live (29 Test Scenarios / 11 Defects):**
  - Unhandled `ValidationException` 500 crashes eliminated via `GlobalExceptionHandlerMiddleware` returning RFC 9110 HTTP 400 (`Cit.Attendance:Validation`).
  - Mandatory English calendar name (`name.en` & `holidayName.en`) strictly enforced with HTTP 400 (`DEFECT-20261103-05` / `-10`).
  - Empty `holidayLists: []` array creation rejected with HTTP 400 `Cit.Attendance:1704` (`DEFECT-20261103-06`).
  - Duplicate `shortCode` within same company rejected with HTTP 400 (`DEFECT-20261103-07`).
  - Outer `year` vs inner `yearlyCalendar.year` mismatch rejected with HTTP 400 (`DEFECT-20261103-09`).
  - Chronological inversion `endDate < startDate` blocked with HTTP 400 (`DEFECT-20261103-11`).
  - Holiday dates outside calendar year rejected with HTTP 400 (`DEFECT-20261103-12`).
  - Missing `holidayTypeId` or `Guid.Empty` rejected with HTTP 400 (`DEFECT-20261103-13`).
  - Operational deadlock on today's date resolved; today's date allowed (200), past dates blocked (400) (`DEFECT-20261103-14`).
- **❌ Confirmed STILL NOT FIXED / FAILED (8 Test Scenarios / 5 Defects):**
  The table below details all persistent failed test cases and defects in the Holiday Calendar suite.

#### 📊 Part 3B Failed & Unfixed Defects Matrix:

| S.No | Defect ID | Associated Test Cases | Module & Route | Severity | FE / API | Defect Description & Invariant Breach | Dev Status | Live Re-Test Verification Finding (16-Nov-2026) | Confluence Sync |
| :---: | :--- | :--- | :--- | :---: | :---: | :--- | :---: | :--- | :---: |
| **1** | [`DEFECT-20261103-08`](#defect-20261103-08) | `HC-DTO-145` (Row 313) | Part 3B / DTO Validations | 🟠 **P1 Critical** | API / DB | **Invalid `calendarType` Enum Coerced to 1:** Sending `"calendarType": 999` is silently accepted, coerced to `1 (CompanyDefault)` in MongoDB, and triggers `Cit.Attendance:1713` conflict instead of returning HTTP 400 DTO enum validation. | ❌ **Not Fixed** | **Re-verified 2026-11-16:** DTO model binder lacks Enum range validation; silently mutates invalid enum to 1 in MongoDB Compass (`evidence_26_holiday_calendar_invalid_calendartype_999_stored_as_default_1.png`). | ✅ Row 10 |
| **2** | [`DEFECT-20261103-15`](#defect-20261103-15) | `HC-PUB-01` (Row 268) & `HC-PUB-18` (Row 285) | Part 3B / Publishing Lifecycle | 🔴 **P0 Blocker** | API / Guard | **Empty Holiday Calendar Published (0 Holidays):** `PublishHolidayCalendarCommandHandler` lacks defense-in-depth guard; calling `POST /holidaylist/publish/2026` on a calendar with 0 holidays succeeds with `HTTP 200 OK` and marks `IsPublished: true`. | ❌ **Not Fixed** | **Re-verified 2026-11-16:** Calling publish endpoint on 0-holiday calendar returns 200 OK without asserting that at least one holiday exists. Confirmed via MongoDB Compass (`evidence_34_holiday_publish_empty_calendar_compass_proof.jpg`). | ✅ Row 11 |
| **3** | [`DEFECT-20261103-03`](#defect-20261103-03) | Part 3B State Lifecycle | Part 3B / Calendar State | 🟠 **P1 Critical** | API / DB | **`isActive: false` Overwritten to True:** Submitting `"isActive": false` in request payload is completely ignored by backend handler and persisted as `IsActive: true` in MongoDB. | ❌ **Not Fixed** | **Re-verified 2026-11-16:** Command handler unconditionally sets `IsActive = true`, ignoring client payload configuration. Confirmed via MongoDB Compass (`evidence_20_holiday_calendar_isactive_false_ignored_stored_true.jpg`). | ✅ Row 12 |
| **4** | Route Constraints | `HC-DTO-01` (Row 2), `HC-DTO-74` (Row 75), `HC-DTO-127` (Row 128), `HC-DTO-129` (Row 130) | Part 3B / API Routing & Error Standards | 🟡 **P2 Major** | API / Routing | **Route Constraint Mismatch (HTTP 404 Instead of HTTP 400):** ASP.NET Core route constraints (`{companyId:guid}`, `{year:int}`) reject malformed route parameters before reaching the controller, returning `HTTP 404 Not Found` instead of RFC 9110 `HTTP 400 Bad Request`. | ❌ **Not Fixed** | **Re-verified 2026-11-16:** Route constraints short-circuit request pipeline without structured 400 ProblemDetails. | ✅ Row 13 |
| **5** | [`DEFECT-20261026-01`](#defect-20261026-01) | `HC-PUB-16` (Row 283) | Part 3B / Cross-Service Sync | 🟠 **P1 Critical** | API / Integration | **Publish Does Not Synchronize Company Checklist:** Publishing a holiday calendar does not update `CompanyChecklist.HolidayCalendarPublished` in `SP.CompanySvc`; remains `false`. | ❌ **Not Fixed** | **Re-verified 2026-11-16:** Missing domain event publisher; checklist status remains `false` in `CompaniesMaster`. [Evidence 02] | ✅ Row 14 |

---"""

if target_end_part3 in content:
    content = content.replace(target_end_part3, part3b_section, 1)
    print("Inserted Part 3B section into Master Defect Log.")
else:
    print("Warning: target_end_part3 not found in Master Defect Log!")

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)

print(f"Successfully wrote updated {filepath}!")
