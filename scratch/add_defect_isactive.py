# -*- coding: utf-8 -*-
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('Attendance2_Defects_Gaps_and_Architecture_Inconsistencies_Report.md', 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Update Top Alert Banner Table
banner_table_target = """| **`DEFECT-20261103-02`** | **P1 (Master Data Integrity)**| **Holiday List Module**<br>(Master Data) | `ERP.Attendance.HolidayCalendars`<br>(Holiday List) | **Holiday List: `TenantName` Persists as `Object (empty)`:** Live Holiday List document created 03-Nov-2026 persists `TenantName: {}` instead of auto-populating from `_currentTenant.Name`. | ❌ **FAIL (CONFIRMED PERSISTING)** |"""

banner_table_new = banner_table_target + """\n| **`DEFECT-20261103-03`** | **P1 (Functional / Contract)**| **Holiday List Module**<br>(State Management) | `ERP.Attendance.HolidayCalendars`<br>(`POST /holidaycalendars`) | **Holiday List: `isActive: false` Ignored by Backend Handler and Stored as `true`:** Client sends `"isActive": false`, but MongoDB persists `IsActive: true` (Document `a3f5c92f-ff7f-48e8-bea8-a4006f959b19`). | ❌ **OPEN (COMPASS PROOF)** |"""

if banner_table_target in text and "DEFECT-20261103-03" not in text:
    text = text.replace(banner_table_target, banner_table_new)

# 2. Update Photographic Preview Table in Top Alert Banner
photo_table_target = """📸 **Photographic Proof from MongoDB Compass (Holiday List Module — 03 November 2026):**

| `evidence_18`: `CreatedBy` Stored as Plain Email | `evidence_19`: `TenantName: Object (empty)` (QA Red Circle) |
| :---: | :---: |
| ![CreatedBy Plain Email](defect_evidence/evidence_18_holiday_calendar_createdby_email_tenantname_empty.jpg) | ![TenantName Empty Red Circle](defect_evidence/evidence_19_holiday_calendar_tenantname_empty_red_circle.jpg) |
| [🔍 View Evidence 18 Full Size](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_18_holiday_calendar_createdby_email_tenantname_empty.jpg) | [🔍 View Evidence 19 Full Size](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_19_holiday_calendar_tenantname_empty_red_circle.jpg) |"""

photo_table_new = """📸 **Photographic Proof from MongoDB Compass (Holiday List Module — 03 November 2026):**

| `evidence_18`: `CreatedBy` Plain Email | `evidence_19`: `TenantName: Object (empty)` | `evidence_20`: `isActive: false` Ignored (Stored `true`) |
| :---: | :---: | :---: |
| ![CreatedBy Plain Email](defect_evidence/evidence_18_holiday_calendar_createdby_email_tenantname_empty.jpg) | ![TenantName Empty Red Circle](defect_evidence/evidence_19_holiday_calendar_tenantname_empty_red_circle.jpg) | ![IsActive Stored True](defect_evidence/evidence_20_holiday_calendar_isactive_false_ignored_stored_true.jpg) |
| [🔍 View Evidence 18](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_18_holiday_calendar_createdby_email_tenantname_empty.jpg) | [🔍 View Evidence 19](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_19_holiday_calendar_tenantname_empty_red_circle.jpg) | [🔍 View Evidence 20](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_20_holiday_calendar_isactive_false_ignored_stored_true.jpg) |"""

if photo_table_target in text:
    text = text.replace(photo_table_target, photo_table_new)

# 3. Add Deep-Dive for DEFECT-20261103-03 in Part 3F
deep_dive_target = """  // In Update handlers (PATCH): Ensure TenantName is never overwritten with null/empty
  if (existingCalendar.TenantName == null || string.IsNullOrWhiteSpace(existingCalendar.TenantName.En))
  {
      existingCalendar.TenantName = new MultilingualString
      {
          En = _currentTenant.Name ?? "Attendance",
          Ar = _currentTenant.ArabicName ?? "الحضور"
      };
  }
  ```"""

defect_03_deep_dive = deep_dive_target + """\n\n---

### Defect `DEFECT-20261103-03`: Holiday List Module — `isActive: false` Ignored by Backend Handler and Persisted as `IsActive: true`
* **Severity:** **P1 (Functional Bug / Contract Violation)**
* **Target Module & Collection:** **Holiday List Module** (`ERP.Attendance.HolidayCalendars`)
* **Endpoint:** `POST /api/companies/{companyId}/holidaycalendars`
* **Exact Request Payload Sent by QA:**
  ```json
  {
    "isActive": false,
    "shortCode": "HOLP02",
    "name": {
      "en": "Inactive Holiday Calendar",
      "ar": "تقويم العطلات غير النشط"
    },
    "calendarType": 1,
    "isLocked": false,
    "isDeleted": false,
    "year": 2026,
    "yearlyCalendar": {
      "year": 2026,
      "holidayLists": [
        {
          "id": "00000000-0000-0000-0000-000000000000",
          "holidayName": {
            "en": "Inactive Calendar Holiday",
            "ar": "عطلة التقويم غير النشط"
          },
          "holidayTypeId": "3a249870-18c5-eb35-b782-7b26f5f35ccd",
          "holidayTypeName": {
            "en": "Public Holiday",
            "ar": "عطلة عامة"
          },
          "startDate": "2026-11-04T00:00:00Z",
          "endDate": "2026-11-04T00:00:00Z"
        }
      ]
    }
  }
  ```

* **Live Photographic Proof from MongoDB Compass (03-Nov-2026):**

![MongoDB Compass Evidence - IsActive stored true](defect_evidence/evidence_20_holiday_calendar_isactive_false_ignored_stored_true.jpg)
*Figure: Live document inspection in MongoDB Compass on `ERP.Attendance.HolidayCalendars` — Document `a3f5c92f-ff7f-48e8-bea8-a4006f959b19` created at 2026-11-03 06:10:42 UTC persists `IsActive: true` despite payload explicitly sending `"isActive": false`.*

* **Observed Behavior:**
  The server responds with HTTP 200/201 OK and creates document `a3f5c92f-ff7f-48e8-bea8-a4006f959b19`. However, MongoDB stores:
  ```json
  "IsActive": true
  ```
  The client's explicit input `"isActive": false` was completely ignored by the backend!

* **Root Cause Analysis:**
  In `CreateHolidayCalendarCommandHandler.cs` (or the underlying AutoMapper profile):
  1. **Hardcoded Assignment:** The handler explicitly hardcodes `holidayCalendar.IsActive = true;` during entity instantiation, ignoring `request.IsActive`.
  2. **Missing DTO Property Mapping:** Alternatively, the `CreateHolidayCalendarCommand` class does not bind `IsActive` from `CreateHolidayCalendarDto`, causing the domain entity constructor default value (`public bool IsActive { get; set; } = true;`) to overwrite the payload value.

* **Business & Architectural Impact:**
  - **Inability to Create Draft Calendars:** HR admins cannot draft holiday calendars in an inactive state to review before publishing. The calendar immediately activates, potentially altering employee working days and timesheets prematurely.
  - **Contract Violation:** A REST API must either honor the client's payload or return an error if a property cannot be modified. Silently accepting `"isActive": false` while saving `true` causes UI state desynchronization.

* **Developer Remediation (.NET 9 C#):**
  In `CreateHolidayCalendarCommandHandler.cs`:
  ```csharp
  // Fix: Explicitly map IsActive from the incoming command DTO
  var holidayCalendar = new HolidayCalendar
  {
      Id = Guid.NewGuid(),
      CompanyId = command.CompanyId,
      ShortCode = command.ShortCode,
      Name = command.Name,
      CalendarType = command.CalendarType,
      Year = command.Year,
      // Map IsActive directly from command (do NOT hardcode to true):
      IsActive = command.IsActive,
      IsLocked = command.IsLocked,
      IsDeleted = false,
      TenantId = _currentTenant.Id ?? Guid.Empty,
      TenantName = new MultilingualString
      {
          En = _currentTenant.Name ?? "Attendance",
          Ar = _currentTenant.ArabicName ?? "الحضور"
      }
  };
  ```"""

if deep_dive_target in text and "DEFECT-20261103-03" not in text:
    text = text.replace(deep_dive_target, defect_03_deep_dive)

# 4. Update Part 5 Developer Checklist
checklist_target = """- [ ] **P1 (`DEFECT-20261103-02` / `DEFECT-20261026-02`):** In `CreateHolidayCalendarCommandHandler.cs`, inject `ICurrentTenant` and populate `TenantName = new MultilingualString { En = _currentTenant.Name, Ar = _currentTenant.ArabicName }`. Stop persisting `TenantName: Object (empty)`!"""

checklist_new = checklist_target + """\n- [ ] **P1 (`DEFECT-20261103-03`):** In `CreateHolidayCalendarCommandHandler.cs`, explicitly map `holidayCalendar.IsActive = command.IsActive;`. Do NOT hardcode `IsActive = true` when client sends `"isActive": false`."""

if checklist_target in text and "DEFECT-20261103-03" not in text:
    text = text.replace(checklist_target, checklist_new)

with open('Attendance2_Defects_Gaps_and_Architecture_Inconsistencies_Report.md', 'w', encoding='utf-8') as f:
    f.write(text)

print(f"SUCCESS: Logged DEFECT-20261103-03 in Defect Report ({len(text)} characters)!")

