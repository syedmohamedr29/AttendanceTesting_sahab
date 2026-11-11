# -*- coding: utf-8 -*-
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('Attendance2_Defects_Gaps_and_Architecture_Inconsistencies_Report.md', 'r', encoding='utf-8') as f:
    text = f.read()

target_part_4 = "\n# 🔄 Part 4: Standardized Bug Lifecycle Procedure"

defect_03_deep_dive = """---

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
  ```

---
"""

if target_part_4 in text and "### Defect `DEFECT-20261103-03`" not in text:
    text = text.replace(target_part_4, "\n" + defect_03_deep_dive + target_part_4)
    with open('Attendance2_Defects_Gaps_and_Architecture_Inconsistencies_Report.md', 'w', encoding='utf-8') as f:
        f.write(text)
    print("SUCCESS: Inserted DEFECT-20261103-03 deep-dive right before Part 4!")
else:
    print("Target not found or already added!")

