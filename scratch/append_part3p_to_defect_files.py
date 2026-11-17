# -*- coding: utf-8 -*-
import re

FILES = [
    'Attendance2_Defects_Gaps_and_Architecture_Inconsistencies_Report.md',
    'Defects/Attendance2_Master_Defect_Log.md'
]

PART_3P_CONTENT = """

---

### 🏢 Part 3P: Defects Identified on 16 November 2026 — Holiday Calendar Module: Company Calendar Live API & MongoDB Audit (`DEFECT-20261116-07` to `DEFECT-20261116-12`)

<a id="-part-3p-defects-identified-on-16-november-2026--holiday-calendar-module--company-calendar-live-api--mongodb-audit-defect-20261116-07-to-12"></a>

> **Audit Execution Date:** **16 November 2026 (Day 12 Update — Holiday Calendar - Company Full Suite Live Audit)**  
> **Target Environment:** DEV (`https://attendance2.dev.zoolwork.com` / `https://company8.dev.zoolwork.com`)  
> **Database Collections Inspected:** MongoDB `10.1.0.4:27018` — `Sahab.ERP.Attendance.HolidayCalendars`  
> **Test Suite Executed:** `Holiday Calendar - Company` Sheet 6 in `AttendanceTestCases_Master_Consolidated.xlsx` (83 Test Cases: `DOC-A-01` to `DOC-F-05`, `ROOT-A-01` to `ROOT-F-01`)  
> **Confluence Sync:** Published to Confluence Page [**`Bug Fixes Testing`** (Page ID: `1567653890`)](https://zoolworks.atlassian.net/wiki/spaces/AM/pages/1567653890/Bug+Fixes+Testing) as **Rows 85 to 90** (Version 24 Active)  
> **Handover Status:** ⚠️ **Pending Developer Handover (Not Fixed / Live Reproduced on 16-Nov-2026)**  

📸 **Visual Evidence Gallery (Holiday Calendar Live Probes — 16 November 2026):**

| `evidence_29`: Chronological Inversion Accepted | `evidence_32`: Today Deadlock `1706` | `evidence_24`: Empty `holidayLists: []` Array |
| :---: | :---: | :---: |
| [![Evidence 29](defect_evidence/evidence_29_holiday_calendar_end_date_before_start_date_accepted.png)](defect_evidence/evidence_29_holiday_calendar_end_date_before_start_date_accepted.png) | [![Evidence 32](defect_evidence/evidence_32_holiday_patch_1706_current_year_today_blocked_swagger.png)](defect_evidence/evidence_32_holiday_patch_1706_current_year_today_blocked_swagger.png) | [![Evidence 24](defect_evidence/evidence_24_holiday_calendar_empty_holidaylists_array_accepted.jpg)](defect_evidence/evidence_24_holiday_calendar_empty_holidaylists_array_accepted.jpg) |

| `evidence_30`: Future Year Infiltration | `evidence_25`: Duplicate ShortCode Allowed | `evidence_19`: TenantName Empty / 500 Crash |
| :---: | :---: | :---: |
| [![Evidence 30](defect_evidence/evidence_30_holiday_calendar_holiday_outside_calendar_year.jpg)](defect_evidence/evidence_30_holiday_calendar_holiday_outside_calendar_year.jpg) | [![Evidence 25](defect_evidence/evidence_25_holiday_calendar_duplicate_shortcode_allowed.jpg)](defect_evidence/evidence_25_holiday_calendar_duplicate_shortcode_allowed.jpg) | [![Evidence 19](defect_evidence/evidence_19_holiday_calendar_tenantname_empty_red_circle.jpg)](defect_evidence/evidence_19_holiday_calendar_tenantname_empty_red_circle.jpg) |

---

#### 1. Summary of Defects Formally Logged from Holiday Calendar - Company (Rows 85 to 90)

| Confluence Row | Defect ID | Severity | Component | Defect Title & Architectural Gap | Failed Test Cases | Live MongoDB Impact | Dev Status |
| :---: | :--- | :---: | :--- | :--- | :--- | :--- | :---: |
| **Row 85** | `DEFECT-20261116-07` | 🔴 **P0 Blocker** | Holiday Invariant | **Holiday Calendar Chronological Inversion Accepted (`endDate < startDate`):** Calling PATCH with `endDate` before `startDate` succeeds with HTTP 200 OK. Persists negative duration holidays in MongoDB. | `DOC-C-06`<br>`ROOT-D-07` | Corrupted date range persisted in `YearlyCalendar.HolidayLists` | ❌ Not Fixed |
| **Row 86** | `DEFECT-20261116-08` | 🔴 **P0 Blocker** | Business Logic | **Current-Year Update Deadlock (`Cit.Attendance:1706`):** Rule rejects today's date during PATCH updates of current year, treating today as 'past' and deadlocking emergency same-day edits. | `DOC-C-05`<br>`ROOT-D-06` | Valid same-day calendar edits blocked with HTTP 400 | ❌ Not Fixed |
| **Row 87** | `DEFECT-20261116-09` | 🟠 **P1 Critical** | Business Invariant | **Empty `holidayLists: []` Array Accepted on Calendar Edit:** PATCH accepts empty array, wiping all holidays from calendar and creating an empty active calendar shell in MongoDB. | `DOC-C-03`<br>`ROOT-D-04` | `HolidayLists: []` persisted in MongoDB | ❌ Not Fixed |
| **Row 88** | `DEFECT-20261116-10` | 🟠 **P1 Critical** | Model Invariant | **Future Year Date Infiltration on Calendar Creation:** `POST /holidaylist` for 2026 accepts holidays scheduled in 2027 (`2027-01-01`) without asserting dates match declared calendar year. | `DOC-B-07` | Out-of-year dates stored in 2026 calendar document | ❌ Not Fixed |
| **Row 89** | `DEFECT-20261116-11` | 🟠 **P1 Critical** | Uniqueness Constraint | **Duplicate Holiday Date & ShortCode Allowed:** Submitting multiple holidays with identical dates and shortCodes within same calendar succeeds with HTTP 200 OK without uniqueness check. | `ROOT-B-07` | Duplicate items stored in `YearlyCalendar.HolidayLists` | ❌ Not Fixed |
| **Row 90** | `DEFECT-20261116-12` | 🟠 **P1 Critical** | Middleware Stability | **Missing `__tenant` Header & Empty Body Triggers HTTP 500 Crash:** Missing header or `{}` payload crashes Kestrel request pipeline with unhandled 500 instead of structured 400 ProblemDetails. | `DOC-A-03`<br>`ROOT-A-04`<br>`DOC-B-01`<br>`ROOT-B-01`<br>`DOC-C-02` | Unhandled `ValidationException` in Kestrel logs | ❌ Not Fixed |

---

#### Defect `DEFECT-20261116-07`: Holiday Calendar Chronological Inversion Accepted (`endDate < startDate`)

<a id="defect-20261116-07"></a>

- **Defect ID:** `DEFECT-20261116-07` | **Confluence Tracking:** **Row 85**
- **Severity:** 🔴 **P0 Blocker** (Chronological Domain Invariant & Shift Calculation Corruption)
- **Component:** Holiday Modification (`PATCH /api/companies/{companyId}/holidaylist/{id}/{year}`)
- **Microservices Involved:** `SP.AttendanceSvc` (.NET 9 Web API)
- **Database Collection:** `Sahab.ERP.Attendance.HolidayCalendars`
- **Visual Evidence:** [Evidence 29 (End Date Before Start Date Accepted)](<file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_29_holiday_calendar_end_date_before_start_date_accepted.png>)
- **Related Test Cases:** `DOC-C-06`, `ROOT-D-07`

##### 1. Defect Summary & Root Cause
Calling `PATCH /api/companies/{companyId}/holidaylist/{id}/{year}` with `endDate` earlier than `startDate` (e.g., `startDate: "2026-06-15T00:00:00Z"` and `endDate: "2026-06-10T00:00:00Z"`) succeeds with HTTP 200 OK. The backend handler lacks a FluentValidation rule `RuleFor(x => x.EndDate).GreaterThanOrEqualTo(x => x.StartDate)`, storing inverted chronological boundaries in MongoDB and causing downstream attendance engines to fail or produce negative holiday durations.

##### 2. Live Reproduction Steps & Payloads
```bash
curl -X PATCH "https://attendance2.dev.zoolwork.com/api/companies/3a249871-7a8d-dec5-2d72-47795dd2662d/holidaylist/c9e2b144-884b-4b82-9ef1-8a9d12345678/2026" \
  -H "Authorization: Bearer $TOKEN" \
  -H "__tenant: 3a249871-7a8d-dec5-2d72-47795dd2662d" \
  -H "Content-Type: application/json" \
  -d '{
    "yearlyCalendar": {
      "year": 2026,
      "holidayLists": [
        {
          "holidayName": { "en": "Inverted Holiday", "ar": "عطلة معكوسة" },
          "holidayTypeId": "3a249870-18c5-eb35-b782-7b26f5f35ccd",
          "startDate": "2026-06-15T00:00:00Z",
          "endDate": "2026-06-10T00:00:00Z"
        }
      ]
    }
  }'
```
* **Observed Server Response:** `HTTP 200 OK`.
* **Database State:** MongoDB persists `StartDate: ISODate("2026-06-15T00:00:00Z")` and `EndDate: ISODate("2026-06-10T00:00:00Z")`.

##### 3. Developer Remediation (.NET 9 C#)
```csharp
// In UpdateHolidayCalendarCommandValidator.cs
RuleForEach(x => x.YearlyCalendar.HolidayLists)
    .Must(h => h.EndDate >= h.StartDate)
    .WithMessage("Cit.Attendance:Validation", "Holiday end date must be greater than or equal to start date.");
```

---

#### Defect `DEFECT-20261116-08`: Current-Year Update Deadlock — Today's Date Rejected with `Cit.Attendance:1706`

<a id="defect-20261116-08"></a>

- **Defect ID:** `DEFECT-20261116-08` | **Confluence Tracking:** **Row 86**
- **Severity:** 🔴 **P0 Blocker** (Business Logic Deadlock & Calendar Update Block)
- **Component:** Holiday Modification Guard (`PATCH /api/companies/{companyId}/holidaylist/{id}/{year}`)
- **Microservices Involved:** `SP.AttendanceSvc` (.NET 9 Web API)
- **Database Collection:** `Sahab.ERP.Attendance.HolidayCalendars`
- **Visual Evidence:** [Evidence 32 (Cit.Attendance:1706 Current Year Today Blocked)](<file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_32_holiday_patch_1706_current_year_today_blocked_swagger.png>)
- **Related Test Cases:** `DOC-C-05`, `ROOT-D-06`

##### 1. Defect Summary & Root Cause
Current-year holiday calendar edit rule `Cit.Attendance:1706` ("You can not edit or remove past holidays") compares `item.StartDate <= DateTime.UtcNow`. Because UTC time includes hours/minutes, any holiday falling on Today's date is evaluated as past. This creates a severe operational deadlock: administrators cannot modify or adjust holiday details on the day the holiday occurs.

##### 2. Live Reproduction Steps & Payloads
Submit a PATCH request modifying a holiday where `startDate` is the current date (Today).
* **Observed Server Response:**
  ```json
  HTTP/1.1 400 Bad Request
  {
    "error": {
      "code": "Cit.Attendance:1706",
      "message": "You can not edit or remove past holidays."
    }
  }
  ```

##### 3. Developer Remediation (.NET 9 C#)
```csharp
// In UpdateHolidayCalendarCommandHandler.cs
// Fix: Compare date portions only (exclusive of today)
if (holiday.EndDate.Date < DateTime.UtcNow.Date)
{
    throw new BusinessRuleException("Cit.Attendance:1706", "You can not edit or remove past holidays.");
}
```

---

#### Defect `DEFECT-20261116-09`: Empty `holidayLists: []` Array Accepted on Calendar Edit / PATCH

<a id="defect-20261116-09"></a>

- **Defect ID:** `DEFECT-20261116-09` | **Confluence Tracking:** **Row 87**
- **Severity:** 🟠 **P1 Critical** (Business Invariant & Data Integrity)
- **Component:** Holiday List Mutation (`PATCH /api/companies/{companyId}/holidaylist/{id}/{year}`)
- **Microservices Involved:** `SP.AttendanceSvc` (.NET 9 Web API)
- **Database Collection:** `Sahab.ERP.Attendance.HolidayCalendars`
- **Visual Evidence:** [Evidence 24 (Empty holidayLists Array Accepted)](<file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_24_holiday_calendar_empty_holidaylists_array_accepted.jpg>)
- **Related Test Cases:** `DOC-C-03`, `ROOT-D-04`

##### 1. Defect Summary & Root Cause
While `POST /holidaylist` enforces a non-empty list rule on creation, `PATCH /holidaylist/{id}/{year}` completely lacks this check. Sending `"holidayLists": []` succeeds with HTTP 200 OK and overwrites the calendar's holiday list with an empty array in MongoDB, creating a hollow calendar shell that can be erroneously published.

##### 2. Live Reproduction Steps & Payloads
```bash
curl -X PATCH "https://attendance2.dev.zoolwork.com/api/companies/3a249871-7a8d-dec5-2d72-47795dd2662d/holidaylist/c9e2b144-884b-4b82-9ef1-8a9d12345678/2026" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "yearlyCalendar": {
      "year": 2026,
      "holidayLists": []
    }
  }'
```
* **Observed Server Response:** `HTTP 200 OK`.
* **Database State:** MongoDB persists `YearlyCalendar.HolidayLists: []`.

##### 3. Developer Remediation (.NET 9 C#)
```csharp
// In UpdateHolidayCalendarCommandValidator.cs
RuleFor(x => x.YearlyCalendar.HolidayLists)
    .NotEmpty()
    .WithMessage("Cit.Attendance:1704", "A holiday calendar needs at least one holiday.");
```

---

#### Defect `DEFECT-20261116-10`: Future Year Date Infiltration on Calendar Creation

<a id="defect-20261116-10"></a>

- **Defect ID:** `DEFECT-20261116-10` | **Confluence Tracking:** **Row 88**
- **Severity:** 🟠 **P1 Critical** (Model Boundary Invariant)
- **Component:** Calendar Ingestion (`POST /api/companies/{companyId}/holidaylist`)
- **Microservices Involved:** `SP.AttendanceSvc` (.NET 9 Web API)
- **Database Collection:** `Sahab.ERP.Attendance.HolidayCalendars`
- **Visual Evidence:** [Evidence 30 (Holiday Outside Calendar Year)](<file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_30_holiday_calendar_holiday_outside_calendar_year.jpg>)
- **Related Test Cases:** `DOC-B-07`

##### 1. Defect Summary & Root Cause
`POST /api/companies/{companyId}/holidaylist` declaring `year: 2026` accepts child holiday items scheduled in year 2027 (e.g. `startDate: "2027-01-01T00:00:00Z"`) with HTTP 200 OK. The service does not assert that all child holiday dates strictly match the declared calendar year, leading to year boundary leakage.

##### 2. Live Reproduction Steps & Payloads
Submit a 2026 calendar payload containing a holiday with `startDate: "2027-01-01T00:00:00Z"`.
* **Observed Server Response:** `HTTP 200 OK`.
* **Database State:** 2027 holidays stored inside a 2026 calendar document.

##### 3. Developer Remediation (.NET 9 C#)
```csharp
// In CreateHolidayCalendarCommandValidator.cs
RuleForEach(x => x.YearlyCalendar.HolidayLists)
    .Must((cmd, item) => item.StartDate.Year == cmd.Year && item.EndDate.Year == cmd.Year)
    .WithMessage("Cit.Attendance:Validation", "Holiday dates must fall strictly within the declared calendar year.");
```

---

#### Defect `DEFECT-20261116-11`: Duplicate Holiday Date & ShortCode Within Same Company Calendar Accepted

<a id="defect-20261116-11"></a>

- **Defect ID:** `DEFECT-20261116-11` | **Confluence Tracking:** **Row 89**
- **Severity:** 🟠 **P1 Critical** (Data Integrity & Uniqueness Constraint)
- **Component:** Holiday Ingestion (`POST /api/companies/{companyId}/holidaylist`)
- **Microservices Involved:** `SP.AttendanceSvc` (.NET 9 Web API)
- **Database Collection:** `Sahab.ERP.Attendance.HolidayCalendars`
- **Visual Evidence:** [Evidence 25 (Duplicate ShortCode Allowed)](<file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_25_holiday_calendar_duplicate_shortcode_allowed.jpg>)
- **Related Test Cases:** `ROOT-B-07`

##### 1. Defect Summary & Root Cause
Creating a holiday calendar with two identical holiday items sharing the same date and shortCode succeeds with HTTP 200 OK without uniqueness constraint validation.

##### 2. Live Reproduction Steps & Payloads
Submit `POST /holidaylist` with two identical holiday entries in `holidayLists: [ { ... date: 2026-05-01 }, { ... date: 2026-05-01 } ]`.
* **Observed Server Response:** `HTTP 200 OK`.
* **Database State:** Duplicate holiday documents stored in array.

##### 3. Developer Remediation (.NET 9 C#)
```csharp
// In CreateHolidayCalendarCommandValidator.cs
RuleFor(x => x.YearlyCalendar.HolidayLists)
    .Must(list => list.Select(h => h.StartDate.Date).Distinct().Count() == list.Count)
    .WithMessage("Cit.Attendance:Validation", "Duplicate holiday dates are not permitted within the same calendar.");
```

---

#### Defect `DEFECT-20261116-12`: Missing `__tenant` Header & Empty Body Triggers Unhandled HTTP 500 Crash

<a id="defect-20261116-12"></a>

- **Defect ID:** `DEFECT-20261116-12` | **Confluence Tracking:** **Row 90**
- **Severity:** 🟠 **P1 Critical** (Middleware Stability & Crash Prevention)
- **Component:** Kestrel Request Pipeline (`POST /holidaylist`, `PATCH /holidaylist/{id}/{year}`)
- **Microservices Involved:** `SP.AttendanceSvc` (.NET 9 Web API)
- **Visual Evidence:** [Evidence 19 (TenantName Empty / Crash Indicator)](<file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_19_holiday_calendar_tenantname_empty_red_circle.jpg>)
- **Related Test Cases:** `DOC-A-03`, `ROOT-A-04`, `DOC-B-01`, `ROOT-B-01`, `DOC-C-02`

##### 1. Defect Summary & Root Cause
Sending `POST /holidaylist` or `PATCH /holidaylist/{id}/{year}` without the mandatory `__tenant` header or with an empty `{}` JSON body crashes the request pipeline with unhandled HTTP 500 `ValidationException` / `NullReferenceException` instead of structured 400 ProblemDetails.

##### 2. Live Reproduction Steps & Payloads
```bash
curl -X POST "https://attendance2.dev.zoolwork.com/api/companies/3a249871-7a8d-dec5-2d72-47795dd2662d/holidaylist" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{}'
```
* **Observed Server Response:** `HTTP 500 Internal Server Error`.

##### 3. Developer Remediation (.NET 9 C#)
```csharp
// In ExceptionHandlingMiddleware.cs
public async Task InvokeAsync(HttpContext context)
{
    if (!context.Request.Headers.ContainsKey("__tenant"))
    {
        context.Response.StatusCode = StatusCodes.Status400BadRequest;
        await context.Response.WriteAsJsonAsync(new ProblemDetails
        {
            Status = 400,
            Title = "Missing required __tenant header.",
            Detail = "The __tenant header is mandatory for all multi-tenant API requests."
        });
        return;
    }
    await _next(context);
}
```

---
"""

for filepath in FILES:
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 1. Update TOC
    old_toc = "- [15. 🏢 Part 3N: Defects Identified on 16 November 2026 — Work Template Module: Location Shifts Live API & MongoDB Audit (DEFECT-20261116-01 to 06 — Confluence Rows 79 to 84)](#-part-3n-defects-identified-on-16-november-2026--work-template-module--location-shifts-live-api--mongodb-audit-defect-20261116-01-to-06)\n- [16. 📊 Master Re-Verification & Confluence Defect Tracking Matrix (Rows 1 to 84 Active — Version 22)](#-master-re-verification--deduplication-summary-rows-1-to-40--confluence-version-17)\n- [17. 📸 Master Visual Evidence Index (Evidences 01 to 73)](#-master-visual-evidence-index)"
    new_toc = "- [15. 🏢 Part 3N: Defects Identified on 16 November 2026 — Work Template Module: Location Shifts Live API & MongoDB Audit (DEFECT-20261116-01 to 06 — Confluence Rows 79 to 84)](#-part-3n-defects-identified-on-16-november-2026--work-template-module--location-shifts-live-api--mongodb-audit-defect-20261116-01-to-06)\n- [16. 🏢 Part 3P: Defects Identified on 16 November 2026 — Holiday Calendar Module: Company Calendar Live API & MongoDB Audit (DEFECT-20261116-07 to 12 — Confluence Rows 85 to 90)](#-part-3p-defects-identified-on-16-november-2026--holiday-calendar-module--company-calendar-live-api--mongodb-audit-defect-20261116-07-to-12)\n- [17. 📊 Master Re-Verification & Confluence Defect Tracking Matrix (Rows 1 to 90 Active — Version 24)](#-master-re-verification--deduplication-summary-rows-1-to-40--confluence-version-17)\n- [18. 📸 Master Visual Evidence Index (Evidences 01 to 73)](#-master-visual-evidence-index)"
    
    if old_toc in content:
        content = content.replace(old_toc, new_toc)
        print(f"Updated TOC in {filepath}")
    else:
        print(f"Warning: Old TOC not found exactly in {filepath}")

    # 2. Append Part 3P at end of file (or before section 16)
    if "### 🏢 Part 3P: Defects Identified on 16 November 2026" not in content:
        content = content.rstrip() + PART_3P_CONTENT
        print(f"Appended Part 3P to {filepath}")
    else:
        print(f"Part 3P already in {filepath}")
        
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

print("Done updating both defect files!")
