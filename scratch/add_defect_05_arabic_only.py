# -*- coding: utf-8 -*-
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('Attendance2_Defects_Gaps_and_Architecture_Inconsistencies_Report.md', 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Update Top Alert Banner Table
banner_row_target = """| **`DEFECT-20261103-04`** | **P1 (Data / Referential Integrity)**| **Holiday List Module**<br>(Master Lookup) | `ERP.Attendance.HolidayCalendars`<br>(`POST /holidaycalendars`) | **Holiday List: Invalid / Arbitrary `holidayTypeId` Accepted Without Master Validation:** Server accepts fake/invalid `holidayTypeId` (`3a249870-18c5-eb35-b782-7b26f5f35ccd`) for multiple holidays with HTTP 200 OK and persists directly into MongoDB. | ❌ **OPEN (COMPASS PROOF)** |"""

banner_row_new = banner_row_target + """\n| **`DEFECT-20261103-05`** | **P1 (Data Integrity / Localization)**| **Holiday List Module**<br>(DTO Validation) | `ERP.Attendance.HolidayCalendars`<br>(`POST /holidaycalendars`) | **Holiday List: Calendar Created with Arabic Name Only (Missing Mandatory English `name.en`):** Server allows creating calendar `"HOLP07"` with only `"ar"` name; `"en"` is completely omitted in MongoDB (`Name: Object (1)`). | ❌ **OPEN (COMPASS PROOF)** |"""

if banner_row_target in text and "DEFECT-20261103-05" not in text:
    text = text.replace(banner_row_target, banner_row_new)

# 2. Update Photographic Preview Table in Top Alert Banner
photo_target = """| `evidence_21`: Invalid `holidayTypeId` Payload | `evidence_22`: Invalid `holidayTypeId` Persisted in MongoDB Compass |
| :---: | :---: |
| ![Invalid HolidayTypeId Payload](defect_evidence/evidence_21_holiday_calendar_invalid_holidaytypeid_payload.jpg) | ![Invalid HolidayTypeId Stored in Compass](defect_evidence/evidence_22_holiday_calendar_invalid_holidaytypeid_compass.jpg) |
| [🔍 View Evidence 21 (Payload)](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_21_holiday_calendar_invalid_holidaytypeid_payload.jpg) | [🔍 View Evidence 22 (Compass)](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_22_holiday_calendar_invalid_holidaytypeid_compass.jpg) |"""

photo_new = photo_target + """\n\n| `evidence_23`: Arabic Name Only Accepted (English `en` Omitted in MongoDB Compass) |
| :---: |
| ![Arabic Name Only Accepted](defect_evidence/evidence_23_holiday_calendar_arabic_only_name_accepted.jpg) |
| [🔍 View Evidence 23 (Compass Inspection)](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_23_holiday_calendar_arabic_only_name_accepted.jpg) |"""

if photo_target in text and "evidence_23_holiday_calendar" not in text:
    text = text.replace(photo_target, photo_new)

# 3. Add DEFECT-20261103-05 Deep-Dive right before Part 4
pos_p4 = text.find('# 🔄 Part 4: Standardized Bug Lifecycle Procedure', 4000)

defect_05_deep_dive = """---

### Defect `DEFECT-20261103-05`: Holiday List Module — Calendar Created with Arabic Name Only (Missing Mandatory English `name.en`)
* **Severity:** **P1 (Data Integrity / Localization Architecture)**
* **Target Module & Collection:** **Holiday List Module** (`ERP.Attendance.HolidayCalendars`)
* **Endpoint:** `POST /api/companies/{companyId}/holidaycalendars` (and `PATCH /holidaycalendars/{id}`)
* **Exact Request Payload Sent by QA:**
  ```json
  {
    "isActive": true,
    "shortCode": "HOLP07",
    "name": {
      "ar": "تقويم العطلات باللغة العربية"
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
            "ar": "عطلة رسمية"
          },
          "holidayTypeId": "3a249870-18c5-eb35-b782-7b26f5f35ccd",
          "holidayTypeName": {
            "ar": "عطلة عامة"
          },
          "startDate": "2026-11-07T00:00:00Z",
          "endDate": "2026-11-07T00:00:00Z"
        }
      ]
    }
  }
  ```

* **Live Photographic Proof from MongoDB Compass (03-Nov-2026):**

![MongoDB Compass Evidence - Arabic Name Only Accepted](defect_evidence/evidence_23_holiday_calendar_arabic_only_name_accepted.jpg)
*Figure: Live document inspection in MongoDB Compass on `ERP.Attendance.HolidayCalendars` — Document `8fb4050e-9cf4-42a8-94a0-a244c98375df` created at 2026-11-03 06:39:03 UTC persists `Name: Object (1) { ar: "تقويم العطلات باللغة العربية" }` with English (`en`) completely missing.*

* **Observed Behavior:**
  The server responds with HTTP 200/201 OK and successfully creates document `8fb4050e-9cf4-42a8-94a0-a244c98375df`. In MongoDB:
  - `Name: Object (1)` has ONLY Arabic: `ar: "تقويم العطلات باللغة العربية"`.
  - English (`en`) was omitted entirely from both calendar name and child holiday names!

* **Core Architectural Rule (Sahab Localization Standard):**
  > [!IMPORTANT]
  > Across the entire Sahab ERP ecosystem:
  > - **English (`en`) is MANDATORY:** It is the primary system key and default fallback language for all UI portals, API integrations, and system-generated notifications.
  > - **Arabic (`ar`) is OPTIONAL:** It serves as a supplementary localized display string.
  > - An entity must **NEVER** be created with an Arabic-only name. If English is missing, the API must reject the request with `HTTP 400 Bad Request`.

* **Business & Architectural Impact:**
  - **Blank Labels in English Portals:** Any HR administrator or employee viewing the Attendance portal in English will see blank / empty calendar titles and holiday labels in dropdowns, schedules, and timesheets.
  - **Reports & Export Glitches:** Timesheet summaries, CSV/Excel holiday exports, and downstream payroll compensation engines running on English system locales will export blank holiday reasons.

* **Developer Remediation (.NET 9 C# FluentValidation):**
  In `CreateHolidayCalendarCommandValidator.cs` and `UpdateHolidayCalendarCommandValidator.cs`:
  ```csharp
  // 1. Enforce English name on Calendar root
  RuleFor(x => x.Name)
      .NotNull().WithMessage("Calendar name object is required.");

  RuleFor(x => x.Name.En)
      .NotEmpty().WithMessage("English calendar name (name.en) is mandatory.")
      .MaximumLength(100).WithMessage("English calendar name cannot exceed 100 characters.");

  RuleFor(x => x.Name.Ar)
      .MaximumLength(100).When(x => !string.IsNullOrEmpty(x.Name?.Ar))
      .WithMessage("Arabic calendar name cannot exceed 100 characters.");

  // 2. Enforce English name on child Holiday items
  RuleForEach(x => x.YearlyCalendar.HolidayLists).ChildRules(holiday =>
  {
      holiday.RuleFor(h => h.HolidayName)
          .NotNull().WithMessage("Holiday name object is required.");

      holiday.RuleFor(h => h.HolidayName.En)
          .NotEmpty().WithMessage("English holiday name (holidayName.en) is mandatory.")
          .MaximumLength(100).WithMessage("English holiday name cannot exceed 100 characters.");
  });
  ```

---

"""

if pos_p4 != -1 and "DEFECT-20261103-05" not in text:
    text = text[:pos_p4] + defect_05_deep_dive + text[pos_p4:]

# 4. Update Part 5 Developer Checklist
checklist_target = """- [ ] **P1 (`DEFECT-20261103-04`):** In `CreateHolidayCalendarCommandValidator.cs`, add `MustAsync` rule to validate that `holidayTypeId` exists in the Master Holiday Types catalog before persisting."""

checklist_new = checklist_target + """\n- [ ] **P1 (`DEFECT-20261103-05`):** In `CreateHolidayCalendarCommandValidator.cs` and `UpdateHolidayCalendarCommandValidator.cs`, enforce `RuleFor(x => x.Name.En).NotEmpty()` and `RuleFor(h => h.HolidayName.En).NotEmpty()`. Reject payloads containing Arabic name only without English."""

if checklist_target in text and "DEFECT-20261103-05" not in text:
    text = text.replace(checklist_target, checklist_new)

with open('Attendance2_Defects_Gaps_and_Architecture_Inconsistencies_Report.md', 'w', encoding='utf-8') as f:
    f.write(text)

print(f"SUCCESS: Logged DEFECT-20261103-05 in Defect Report ({len(text)} characters)!")

