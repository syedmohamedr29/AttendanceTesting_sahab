# -*- coding: utf-8 -*-
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('Attendance2_Defects_Gaps_and_Architecture_Inconsistencies_Report.md', 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Update Top Alert Banner Table
banner_row_target = """| **`DEFECT-20261103-05`** | **P1 (Data Integrity / Localization)**| **Holiday List Module**<br>(DTO Validation) | `ERP.Attendance.HolidayCalendars`<br>(`POST /holidaycalendars`) | **Holiday List: Calendar Created with Arabic Name Only (Missing Mandatory English `name.en`):** Server allows creating calendar `"HOLP07"` with only `"ar"` name; `"en"` is completely omitted in MongoDB (`Name: Object (1)`). | ❌ **OPEN (COMPASS PROOF)** |"""

banner_row_new = banner_row_target + """\n| **`DEFECT-20261103-06`** | **P1 (Business / Validation)**| **Holiday List Module**<br>(Collection Invariant) | `ERP.Attendance.HolidayCalendars`<br>(`POST /holidaycalendars`) | **Holiday List: Empty `holidayLists: []` Array Accepted with HTTP 200 OK:** Server allows creating calendar `"HOLP12"` with 0 holidays; persisted in MongoDB as `HolidayLists: Array (empty)`. | ❌ **OPEN (COMPASS PROOF)** |"""

if banner_row_target in text and "DEFECT-20261103-06" not in text:
    text = text.replace(banner_row_target, banner_row_new)

# 2. Update Photographic Preview Table in Top Alert Banner
photo_target = """| `evidence_23`: Arabic Name Only Accepted (English `en` Omitted in MongoDB Compass) |
| :---: |
| ![Arabic Name Only Accepted](defect_evidence/evidence_23_holiday_calendar_arabic_only_name_accepted.jpg) |
| [🔍 View Evidence 23 (Compass Inspection)](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_23_holiday_calendar_arabic_only_name_accepted.jpg) |"""

photo_new = photo_target + """\n\n| `evidence_24`: Empty `holidayLists: []` Array Accepted (Stored as Empty Array in Compass) |
| :---: |
| ![Empty HolidayLists Array Accepted](defect_evidence/evidence_24_holiday_calendar_empty_holidaylists_array_accepted.jpg) |
| [🔍 View Evidence 24 (Compass Inspection)](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_24_holiday_calendar_empty_holidaylists_array_accepted.jpg) |"""

if photo_target in text and "evidence_24_holiday_calendar" not in text:
    text = text.replace(photo_target, photo_new)

# 3. Add DEFECT-20261103-06 Deep-Dive right before Part 4
pos_p4 = text.find('# 🔄 Part 4: Standardized Bug Lifecycle Procedure', 4000)

defect_06_deep_dive = """---

### Defect `DEFECT-20261103-06`: Holiday List Module — Empty `holidayLists: []` Array Accepted with HTTP 200 OK
* **Severity:** **P1 (Business Logic / Collection Invariant)**
* **Target Module & Collection:** **Holiday List Module** (`ERP.Attendance.HolidayCalendars`)
* **Endpoint:** `POST /api/companies/{companyId}/holidaycalendars` (and `PATCH /holidaycalendars/{id}`)
* **Exact Request Payload Sent by QA:**
  ```json
  {
    "isActive": true,
    "shortCode": "HOLP12",
    "name": {
      "en": "Empty Holiday Calendar",
      "ar": "تقويم بدون عطلات"
    },
    "calendarType": 1,
    "isLocked": false,
    "isDeleted": false,
    "year": 2026,
    "yearlyCalendar": {
      "year": 2026,
      "holidayLists": []
    }
  }
  ```

* **Live Photographic Proof from MongoDB Compass (03-Nov-2026):**

![MongoDB Compass Evidence - Empty HolidayLists Array Accepted](defect_evidence/evidence_24_holiday_calendar_empty_holidaylists_array_accepted.jpg)
*Figure: Live document inspection in MongoDB Compass on `ERP.Attendance.HolidayCalendars` — Document `01488ec3-3f0c-4e74-a858-9a169854112a` created at 2026-11-03 06:44:54 UTC persists `YearlyCalendar.HolidayLists: Array (empty)` with 0 holidays.*

* **Observed Behavior:**
  The server responds with HTTP 200/201 OK and successfully creates document `01488ec3-3f0c-4e74-a858-9a169854112a` in MongoDB with `HolidayLists: Array (empty)`.

* **Root Cause Analysis:**
  In `CreateHolidayCalendarCommandValidator.cs`:
  The validator checks that `YearlyCalendar` is not null, but completely lacks a collection count check (`.NotEmpty()` or `.Must(list => list.Count > 0)`) on `YearlyCalendar.HolidayLists`. An empty JSON array `[]` passes without any validation error.

* **Business & Architectural Impact:**
  1. **Phantom Empty Calendar:** A holiday calendar containing zero holidays is a meaningless empty container. When assigned to a company, location, or employee, it misleads HR admins into believing a holiday schedule is active, but attendance calculation will never recognize any public holidays, incorrectly flagging employees as absent or denying them holiday overtime rates.
  2. **Publishing Inconsistency:** If an admin publishes an empty calendar, downstream systems receive an empty list event, leading to zero holiday exemptions across the company.

* **Developer Remediation (.NET 9 C# FluentValidation):**
  In `CreateHolidayCalendarCommandValidator.cs` and `UpdateHolidayCalendarCommandValidator.cs`:
  ```csharp
  RuleFor(x => x.YearlyCalendar)
      .NotNull().WithMessage("YearlyCalendar object is required.");

  RuleFor(x => x.YearlyCalendar.HolidayLists)
      .NotNull().WithMessage("holidayLists array is mandatory.")
      .Must(list => list != null && list.Count > 0)
      .WithMessage("A holiday calendar must contain at least one holiday in holidayLists. Empty holiday calendars are strictly disallowed.");
  ```

---

"""

if pos_p4 != -1 and "DEFECT-20261103-06" not in text:
    text = text[:pos_p4] + defect_06_deep_dive + text[pos_p4:]

# 4. Update Part 5 Developer Checklist
checklist_target = """- [ ] **P1 (`DEFECT-20261103-05`):** In `CreateHolidayCalendarCommandValidator.cs` and `UpdateHolidayCalendarCommandValidator.cs`, enforce `RuleFor(x => x.Name.En).NotEmpty()` and `RuleFor(h => h.HolidayName.En).NotEmpty()`. Reject payloads containing Arabic name only without English."""

checklist_new = checklist_target + """\n- [ ] **P1 (`DEFECT-20261103-06`):** In `CreateHolidayCalendarCommandValidator.cs` and `UpdateHolidayCalendarCommandValidator.cs`, enforce `RuleFor(x => x.YearlyCalendar.HolidayLists).Must(list => list != null && list.Count > 0)`. Reject empty `holidayLists: []` arrays."""

if checklist_target in text and "DEFECT-20261103-06" not in text:
    text = text.replace(checklist_target, checklist_new)

with open('Attendance2_Defects_Gaps_and_Architecture_Inconsistencies_Report.md', 'w', encoding='utf-8') as f:
    f.write(text)

print(f"SUCCESS: Logged DEFECT-20261103-06 in Defect Report ({len(text)} characters)!")

