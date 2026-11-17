# -*- coding: utf-8 -*-

FILES = [
    'Attendance2_Defects_Gaps_and_Architecture_Inconsistencies_Report.md',
    'Defects/Attendance2_Master_Defect_Log.md'
]

PART_3Q_CONTENT = """

---

### 🏢 Part 3Q: Senior QA Live Audit on Company Attendance 12 — Holiday Calendar - Company (17 November 2026 — `DEFECT-20261117-01` & `02` — Confluence Rows 91 & 92)

<a id="-part-3q-senior-qa-live-audit-on-company-attendance-12--holiday-calendar---company-17-november-2026--defect-20261117-01--02--confluence-rows-91--92"></a>

> **Audit Execution Date:** **17 November 2026 (Day 13 Senior QA Live Audit — Holiday Calendar - Company)**  
> **Target Environment:** DEV (`https://attendance2.dev.zoolwork.com` / `https://company8.dev.zoolwork.com`)  
> **Target Company Tenant:** Company **`Attendance 12`** (`3a24e5e5-e1b4-35ae-2fed-fad9fbf37ebc`) | Tenant ID: `3a24741e-2667-1223-f12e-62a69fab3838`  
> **Database Collections Inspected:** MongoDB `10.1.0.4:27018` — `Sahab.ERP.Attendance.HolidayCalendars`, `CompanySvcNET8test.CompaniesMaster`, `CompanySvcNET8test.HolidayCalendars`  
> **Senior QA Test Suite Executed:** 17 High-Impact Security, DTO Contract, Inter-Service Dependency, and Multi-Tenant Isolation Scenarios  
> **Confluence Sync:** Published to Confluence Page [**`Bug Fixes Testing`** (Page ID: `1567653890`)](https://zoolworks.atlassian.net/wiki/spaces/AM/pages/1567653890/Bug+Fixes+Testing) as **Rows 91 & 92** (Version 25 Active)  
> **Handover Status:** ⚠️ **Pending Developer Handover (Not Fixed / Live Reproduced on 17-Nov-2026)**  

📸 **Visual Evidence Gallery (Senior QA Live Audit — Attendance 12 — 17 November 2026):**

| `evidence_22`: Inter-Service Master Lookup Failure | `evidence_21`: Missing HolidayTypeId / 400 Status Error | `evidence_19`: TenantName Empty / Multi-Tenant Leak |
| :---: | :---: | :---: |
| [![Evidence 22](defect_evidence/evidence_22_holiday_calendar_invalid_holidaytypeid_compass.jpg)](defect_evidence/evidence_22_holiday_calendar_invalid_holidaytypeid_compass.jpg) | [![Evidence 21](defect_evidence/evidence_21_holiday_calendar_invalid_holidaytypeid_payload.jpg)](defect_evidence/evidence_21_holiday_calendar_invalid_holidaytypeid_payload.jpg) | [![Evidence 19](defect_evidence/evidence_19_holiday_calendar_tenantname_empty_red_circle.jpg)](defect_evidence/evidence_19_holiday_calendar_tenantname_empty_red_circle.jpg) |

---

#### 1. Executive Summary & Defect Statistics (Attendance 12 Senior QA Audit)

A senior QA level live audit executed against freshly provisioned company tenant **`Attendance 12`** (`3a24e5e5-e1b4-35ae-2fed-fad9fbf37ebc`) confirmed **2 critical architectural defects** and re-verified 2 longstanding security/multi-tenancy breaches:

| Test Metric | Value | Architectural Impact |
| :--- | :---: | :--- |
| **Total Senior Scenarios Executed** | **17** | Security, DTO Invariants, Cross-Tenant Isolation & Lifecycle Endpoints |
| 🟢 **Passed Scenarios** | **13 (76.5%)** | Empty body validation, missing English name validation, read queries, upcoming feed, and delete guards function properly |
| 🔴 **Failed / Active Defects** | **4 (23.5%)** | 2 New Architectural Defects logged (Rows 91 & 92) + 2 Active Multi-Tenant/JWT Bypasses re-confirmed on Attendance 12 |
| **Provisioning Status for Attendance 12** | 🔴 **BLOCKED** | Company Holiday Calendar creation is **100% blocked** for all fresh companies due to inter-service schema desynchronization |

---

#### 2. Full Test Execution Breakdown on Company Attendance 12

| Test Case ID | Category | Scenario / Test Title | Method & Endpoint | HTTP Got | HTTP Expected | Verdict | Root Cause / Note |
| :--- | :--- | :--- | :--- | :---: | :---: | :---: | :--- |
| `SR-A12-01` | Auth & Tenancy | No Authorization Header | `GET /holidaylist` | `401` | `401` | 🟢 Pass | Kestrel authentication middleware rejects unauthenticated requests |
| `SR-A12-02` | Auth & Tenancy | Expired JWT Token Accepted | `GET /holidaylist` | `200` | `401` | 🔴 **FAIL** | **`DEFECT-20261029-01` Active:** Expired JWT token (~2.8 days past expiry) accepted with HTTP 200 |
| `SR-A12-03` | Auth & Tenancy | Cross-Tenant Header Spoofing (`__tenant`) | `GET /holidaylist` | `200` | `403` | 🔴 **FAIL** | **`DEFECT-20261104-01` Active:** `__tenant: ForeignTenant_123` header ignored; request allowed |
| `SR-A12-04` | Auth & Tenancy | Missing `__tenant` Header Handled | `POST /holidaylist` | `400` | `400` | 🟢 Pass | Handled with HTTP 400 Bad Request |
| `SR-A12-05` | Create Calendar | Create with Company's Seeded HolidayType | `POST /holidaylist` | `400` | `200` | 🔴 **FAIL** | **`DEFECT-20261117-01` (Row 91):** Rejects valid company holiday type with `A holiday type does not exist for this company` |
| `SR-A12-06` | Create Calendar | Empty Request Body `{}` | `POST /holidaylist` | `400` | `400` | 🟢 Pass | Validation filter catches empty JSON body |
| `SR-A12-07` | Create Calendar | Missing English Name (Arabic Only) | `POST /holidaylist` | `400` | `400` | 🟢 Pass | English calendar name is mandatory validation rule enforced |
| `SR-A12-08` | Create Calendar | Empty `holidayLists: []` Array | `POST /holidaylist` | `400` | `400` | 🟢 Pass | `Cit.Attendance:1704` enforced on creation |
| `SR-A12-09` | Create Calendar | Chronological Inversion on Create | `POST /holidaylist` | `400` | `400` | 🟢 Pass | Create validator rejects `endDate < startDate` |
| `SR-A12-10` | Create Calendar | Future Year Infiltration (2027 in 2026) | `POST /holidaylist` | `400` | `400` | 🟢 Pass | Year mismatch rejected on create |
| `SR-A12-11` | Create Calendar | Duplicate Holiday Date in Same Calendar | `POST /holidaylist` | `400` | `400` | 🟢 Pass | Unique date constraint enforced on create |
| `SR-A12-12` | Read Endpoints | List All Company Calendars | `GET /holidaylist` | `200` | `200` | 🟢 Pass | Returns `{"holidayCalendars":[]}` cleanly |
| `SR-A12-13` | Read Endpoints | Get Calendars for Year 2026 | `GET /holidaylist/2026` | `200` | `200` | 🟢 Pass | Returns `{"holidayCalendars":[]}` cleanly |
| `SR-A12-14` | Read Endpoints | Get Upcoming Holidays Feed | `GET /holidaylist/upcoming` | `200` | `200` | 🟢 Pass | Returns `{"from":"2026-11-17","locationCount":0,"items":[]}` |
| `SR-A12-15` | Read Endpoints | Get Non-Existing Calendar ID | `GET /holidaylist/{fakeId}` | `400` | `404` | 🔴 **FAIL** | **`DEFECT-20261117-02` (Row 92):** Returns `HTTP 400 Bad Request` instead of `HTTP 404 Not Found` |
| `SR-A12-16` | Publish Lifecycle | Publish When No Calendar Exists | `POST /publish/2026` | `400` | `400` | 🟢 Pass | Correctly rejects with `Cit.Attendance:1717 Company default holiday calendar not found` |
| `SR-A12-17` | Cross-Tenant Security | Attendance 12 PATCH foreign calendar (Att 3) | `PATCH /{att3_id}/2026` | `400` | `404` | 🔴 **FAIL** | Fails before reaching entity scoping due to `holidayTypeId` pre-validation check |

---

#### Defect `DEFECT-20261117-01`: Fresh Company Calendar Creation Deadlock — Inter-Service Schema Desynchronization (`Cit.Attendance:Validation: A holiday type does not exist for this company`)

<a id="defect-20261117-01"></a>

- **Defect ID:** `DEFECT-20261117-01` | **Confluence Tracking:** **Row 91**
- **Severity:** 🔴 **P0 Blocker** (Complete Feature Deadlock for New Tenants & Inter-Service Disconnect)
- **Component:** Holiday Calendar Creation (`POST /api/companies/{companyId}/holidaylist`)
- **Microservices Involved:** `SP.AttendanceSvc` (.NET 9) & `SP.CompanySvc` (.NET 8)
- **Database Collections:** `CompanySvcNET8test.CompaniesMaster` vs `CompanySvcNET8test.HolidayCalendars`
- **Visual Evidence:** [Evidence 22 (Holiday Calendar Invalid HolidayTypeId Compass Proof)](<file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_22_holiday_calendar_invalid_holidaytypeid_compass.jpg>)
- **Related Test Cases:** `SR-A12-05`, `DOC-A-01`, `ROOT-B-05`

##### 1. Defect Summary & Root Cause
When fresh companies are provisioned in `SP.CompanySvc` (including `Attendance 6` through `Attendance 15`), `SP.CompanySvc` seeds default holiday types (Public, Religious, National, Bank, Gazette, Restricted, Federal) into `CompaniesMaster.CompanyWorkCalendar.HolidayTypes`. However, `SP.AttendanceSvc` validates holiday types by querying the legacy collection `CompanySvcNET8test.HolidayCalendars` (where newly provisioned companies have zero documents). Because it does not query `CompaniesMaster.CompanyWorkCalendar.HolidayTypes`, `SP.AttendanceSvc` concludes that no holiday types exist for the company and unconditionally rejects every `POST /holidaylist` request with `HTTP 400 Bad Request`:
```json
{
  "error": {
    "code": "Cit.Attendance:Validation",
    "message": "A holiday type does not exist for this company.",
    "details": null,
    "data": null,
    "validationErrors": [
      {
        "message": "A holiday type does not exist for this company.",
        "members": [""]
      }
    ]
  }
}
```
**Impact:** It is completely impossible to configure a Company Holiday Calendar for Company `Attendance 12` and all other newly onboarded companies.

##### 2. Live Reproduction Steps & Payloads
1. Inspect `CompanySvcNET8test.CompaniesMaster` for `Attendance 12` (`3a24e5e5-e1b4-35ae-2fed-fad9fbf37ebc`) and retrieve its valid seeded `National Holiday` type ID: `3a24e5e5-e1c2-8d87-a3e4-ed24b470243b`.
2. Send `POST /api/companies/3a24e5e5-e1b4-35ae-2fed-fad9fbf37ebc/holidaylist`:
   ```bash
   curl -X POST "https://attendance2.dev.zoolwork.com/api/companies/3a24e5e5-e1b4-35ae-2fed-fad9fbf37ebc/holidaylist" \
     -H "Authorization: Bearer $TOKEN" \
     -H "__tenant: Attendance" \
     -H "Content-Type: application/json" \
     -d '{
       "isActive": true,
       "shortCode": "A12HOL26",
       "name": { "en": "Attendance 12 Official Calendar", "ar": "تقويم رسمي 12" },
       "calendarType": 1,
       "year": 2026,
       "yearlyCalendar": {
         "year": 2026,
         "holidayLists": [
           {
             "holidayName": { "en": "National Day", "ar": "اليوم الوطني" },
             "holidayTypeId": "3a24e5e5-e1c2-8d87-a3e4-ed24b470243b",
             "startDate": "2026-09-23T00:00:00Z",
             "endDate": "2026-09-23T00:00:00Z"
           }
         ]
       }
     }'
   ```
3. **Observed Response:** `HTTP 400 Bad Request: {"error":{"code":"Cit.Attendance:Validation","message":"A holiday type does not exist for this company."}}`.

##### 3. Developer Remediation (.NET 9 C#)
Update the holiday type lookup repository in `SP.AttendanceSvc` to query `CompaniesMaster` directly:
```csharp
// In HolidayTypeValidationService.cs
public async Task<bool> HolidayTypeExistsAsync(Guid companyId, Guid holidayTypeId, CancellationToken ct)
{
    // 1. Query CompaniesMaster.CompanyWorkCalendar.HolidayTypes
    var company = await _companyRepository.GetByIdAsync(companyId, ct);
    if (company?.CompanyWorkCalendar?.HolidayTypes != null &&
        company.CompanyWorkCalendar.HolidayTypes.Any(ht => ht.Id == holidayTypeId && !ht.IsDeleted))
    {
        return true;
    }

    // 2. Fallback to global / catalog HolidayTypeMaster
    return await _holidayTypeMasterRepo.ExistsAsync(holidayTypeId, ct);
}
```

---

#### Defect `DEFECT-20261117-02`: HTTP Status Code Contract Violation — `GET /holidaylist/{id}` Returns HTTP 400 Instead of HTTP 404 for Non-Existing ID

<a id="defect-20261117-02"></a>

- **Defect ID:** `DEFECT-20261117-02` | **Confluence Tracking:** **Row 92**
- **Severity:** 🟡 **P2 Major** (REST API Contract & Standards Compliance)
- **Component:** Holiday Calendar Query (`GET /api/companies/{companyId}/holidaylist/{id}`)
- **Microservices Involved:** `SP.AttendanceSvc` (.NET 9 Web API)
- **Visual Evidence:** [Evidence 21 (Invalid HolidayTypeId Payload)](<file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_21_holiday_calendar_invalid_holidaytypeid_payload.jpg>)
- **Related Test Cases:** `SR-A12-15`

##### 1. Defect Summary & Root Cause
When querying a single holiday calendar via `GET /api/companies/{companyId}/holidaylist/{id}` with a valid GUID that does not exist in the database (e.g. `00000000-0000-0000-0000-000000000000`), the endpoint returns `HTTP 400 Bad Request` with `Cit.Attendance:1701 Holiday calendar not found` instead of `HTTP 404 Not Found`.

In standard REST architecture and OpenAPI specifications:
- `HTTP 400 Bad Request` indicates a client malformed syntax error (e.g., non-GUID string).
- `HTTP 404 Not Found` indicates a valid syntax request targeting a resource that does not exist.
Returning `400` prevents standard frontend HTTP client retry/routing logic from identifying missing entities.

##### 2. Live Reproduction Steps & Payloads
```bash
curl -X GET "https://attendance2.dev.zoolwork.com/api/companies/3a24e5e5-e1b4-35ae-2fed-fad9fbf37ebc/holidaylist/00000000-0000-0000-0000-000000000000" \
  -H "Authorization: Bearer $TOKEN" \
  -H "__tenant: Attendance"
```
* **Observed Server Response:**
  ```json
  HTTP/1.1 400 Bad Request
  {
    "error": {
      "code": "Cit.Attendance:1701",
      "message": "Holiday calendar not found.",
      "details": null,
      "data": { "holidayCalendarId": "00000000-0000-0000-0000-000000000000" },
      "validationErrors": null
    }
  }
  ```

##### 3. Developer Remediation (.NET 9 C#)
```csharp
// In GetHolidayCalendarByIdQueryHandler.cs
var calendar = await _holidayCalendarRepository.GetByIdAsync(request.Id, ct);
if (calendar == null || calendar.CompanyId != request.CompanyId || calendar.IsDeleted)
{
    // Throw EntityNotFoundException to trigger HTTP 404 ProblemDetails
    throw new EntityNotFoundException(typeof(HolidayCalendar), request.Id);
}
```

---
"""

for filepath in FILES:
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 1. Update TOC
    old_toc = """- [16. 🏢 Part 3P: Defects Identified on 16 November 2026 — Holiday Calendar Module: Company Calendar Live API & MongoDB Audit (DEFECT-20261116-07 to 12 — Confluence Rows 85 to 90)](#-part-3p-defects-identified-on-16-november-2026--holiday-calendar-module--company-calendar-live-api--mongodb-audit-defect-20261116-07-to-12)
- [17. 📊 Master Re-Verification & Confluence Defect Tracking Matrix (Rows 1 to 90 Active — Version 24)](#-master-re-verification--deduplication-summary-rows-1-to-40--confluence-version-17)
- [18. 📸 Master Visual Evidence Index (Evidences 01 to 73)](#-master-visual-evidence-index)"""

    new_toc = """- [16. 🏢 Part 3P: Defects Identified on 16 November 2026 — Holiday Calendar Module: Company Calendar Live API & MongoDB Audit (DEFECT-20261116-07 to 12 — Confluence Rows 85 to 90)](#-part-3p-defects-identified-on-16-november-2026--holiday-calendar-module--company-calendar-live-api--mongodb-audit-defect-20261116-07-to-12)
- [17. 🏢 Part 3Q: Senior QA Live Audit on Company Attendance 12 — Holiday Calendar - Company (17 November 2026 — DEFECT-20261117-01 & 02 — Confluence Rows 91 & 92)](#-part-3q-senior-qa-live-audit-on-company-attendance-12--holiday-calendar---company-17-november-2026--defect-20261117-01--02--confluence-rows-91--92)
- [18. 📊 Master Re-Verification & Confluence Defect Tracking Matrix (Rows 1 to 92 Active — Version 25)](#-master-re-verification--deduplication-summary-rows-1-to-40--confluence-version-17)
- [19. 📸 Master Visual Evidence Index (Evidences 01 to 73)](#-master-visual-evidence-index)"""

    if old_toc in content:
        content = content.replace(old_toc, new_toc)
        print(f"Updated TOC in {filepath}")
    else:
        print(f"Warning: Old TOC not found exactly in {filepath}")

    # 2. Update Header banner
    content = content.replace("Rows 1 to 90 Active — Version 24", "Rows 1 to 92 Active — Version 25 (Senior QA Attendance 12 Audit: DEFECT-20261117-01 & 02 [Rows 91 & 92])")
    content = content.replace("90 unique active tracking rows on Confluence Version 24", "92 unique active tracking rows on Confluence Version 25")

    # 3. Append Part 3Q
    if "### 🏢 Part 3Q: Senior QA Live Audit on Company Attendance 12" not in content:
        content = content.rstrip() + PART_3Q_CONTENT
        print(f"Appended Part 3Q to {filepath}")
    else:
        print(f"Part 3Q already in {filepath}")
        
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

print("Done updating both defect files with Part 3Q!")
