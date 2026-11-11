# -*- coding: utf-8 -*-
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('Attendance2_Defects_Gaps_and_Architecture_Inconsistencies_Report.md', 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Update Top Alert Banner Table
banner_row_target = """| **`DEFECT-20261103-03`** | **P1 (Functional / Contract)**| **Holiday List Module**<br>(State Management) | `ERP.Attendance.HolidayCalendars`<br>(`POST /holidaycalendars`) | **Holiday List: `isActive: false` Ignored by Backend Handler and Stored as `true`:** Client sends `"isActive": false`, but MongoDB persists `IsActive: true` (Document `a3f5c92f-ff7f-48e8-bea8-a4006f959b19`). | ❌ **OPEN (COMPASS PROOF)** |"""

banner_row_new = banner_row_target + """\n| **`DEFECT-20261103-04`** | **P1 (Data / Referential Integrity)**| **Holiday List Module**<br>(Master Lookup) | `ERP.Attendance.HolidayCalendars`<br>(`POST /holidaycalendars`) | **Holiday List: Invalid / Arbitrary `holidayTypeId` Accepted Without Master Validation:** Server accepts fake/invalid `holidayTypeId` (`3a249870-18c5-eb35-b782-7b26f5f35ccd`) for multiple holidays with HTTP 200 OK and persists directly into MongoDB. | ❌ **OPEN (COMPASS PROOF)** |"""

if banner_row_target in text and "DEFECT-20261103-04" not in text:
    text = text.replace(banner_row_target, banner_row_new)

# 2. Update Photographic Preview in Top Alert Banner
photo_target = """| `evidence_18`: `CreatedBy` Plain Email | `evidence_19`: `TenantName: Object (empty)` | `evidence_20`: `isActive: false` Ignored (Stored `true`) |
| :---: | :---: | :---: |
| ![CreatedBy Plain Email](defect_evidence/evidence_18_holiday_calendar_createdby_email_tenantname_empty.jpg) | ![TenantName Empty Red Circle](defect_evidence/evidence_19_holiday_calendar_tenantname_empty_red_circle.jpg) | ![IsActive Stored True](defect_evidence/evidence_20_holiday_calendar_isactive_false_ignored_stored_true.jpg) |
| [🔍 View Evidence 18](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_18_holiday_calendar_createdby_email_tenantname_empty.jpg) | [🔍 View Evidence 19](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_19_holiday_calendar_tenantname_empty_red_circle.jpg) | [🔍 View Evidence 20](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_20_holiday_calendar_isactive_false_ignored_stored_true.jpg) |"""

photo_new = photo_target + """\n\n| `evidence_21`: Invalid `holidayTypeId` Payload | `evidence_22`: Invalid `holidayTypeId` Persisted in MongoDB Compass |
| :---: | :---: |
| ![Invalid HolidayTypeId Payload](defect_evidence/evidence_21_holiday_calendar_invalid_holidaytypeid_payload.jpg) | ![Invalid HolidayTypeId Stored in Compass](defect_evidence/evidence_22_holiday_calendar_invalid_holidaytypeid_compass.jpg) |
| [🔍 View Evidence 21 (Payload)](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_21_holiday_calendar_invalid_holidaytypeid_payload.jpg) | [🔍 View Evidence 22 (Compass)](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_22_holiday_calendar_invalid_holidaytypeid_compass.jpg) |"""

if photo_target in text and "evidence_21_holiday_calendar" not in text:
    text = text.replace(photo_target, photo_new)

# 3. Add DEFECT-20261103-04 Deep-Dive right before Part 4
pos_p4 = text.find('# 🔄 Part 4: Standardized Bug Lifecycle Procedure', 4000)

defect_04_deep_dive = """---

### Defect `DEFECT-20261103-04`: Holiday List Module — Missing Foreign Key / Master Data Validation on `holidayTypeId`
* **Severity:** **P1 (Data Integrity / Referential Integrity)**
* **Target Module & Collection:** **Holiday List Module** (`ERP.Attendance.HolidayCalendars`)
* **Endpoint:** `POST /api/companies/{companyId}/holidaycalendars` (and `PATCH /holidaycalendars/{id}`)
* **Exact Request Payload Sent by QA (Multiple Holidays):**
  ```json
  {
    "isActive": true,
    "shortCode": "HOLP03",
    "name": {
      "en": "Multiple Holiday Calendar",
      "ar": "تقويم العطلات المتعددة"
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
            "en": "New Year",
            "ar": "رأس السنة"
          },
          "holidayTypeId": "3a249870-18c5-eb35-b782-7b26f5f35ccd",
          "holidayTypeName": {
            "en": "Public Holiday",
            "ar": "عطلة عامة"
          },
          "startDate": "2026-01-01T00:00:00Z",
          "endDate": "2026-01-01T00:00:00Z"
        },
        {
          "id": "00000000-0000-0000-0000-000000000000",
          "holidayName": {
            "en": "National Day",
            "ar": "اليوم الوطني"
          },
          "holidayTypeId": "3a249870-18c5-eb35-b782-7b26f5f35ccd",
          "holidayTypeName": {
            "en": "Public Holiday",
            "ar": "عطلة عامة"
          },
          "startDate": "2026-09-23T00:00:00Z",
          "endDate": "2026-09-23T00:00:00Z"
        },
        {
          "id": "00000000-0000-0000-0000-000000000000",
          "holidayName": {
            "en": "Eid Holiday",
            "ar": "إجازة العيد"
          },
          "holidayTypeId": "3a249870-18c5-eb35-b782-7b26f5f35ccd",
          "holidayTypeName": {
            "en": "Public Holiday",
            "ar": "عطلة عامة"
          },
          "startDate": "2026-11-03T00:00:00Z",
          "endDate": "2026-11-05T00:00:00Z"
        }
      ]
    }
  }
  ```

* **Live Photographic Proof:**

| Payload Inspection (Invalid `holidayTypeId`) | MongoDB Compass (Saved in Database Without Validation) |
| :---: | :---: |
| ![Invalid HolidayTypeId Payload](defect_evidence/evidence_21_holiday_calendar_invalid_holidaytypeid_payload.jpg) | ![Invalid HolidayTypeId Saved](defect_evidence/evidence_22_holiday_calendar_invalid_holidaytypeid_compass.jpg) |
| *Figure A: QA payload passing invalid `holidayTypeId`* | *Figure B: Document in Compass persisting invalid `HolidayType._id`* |

* **Observed Behavior:**
  The server responds with HTTP 200/201 OK and successfully persists the document into MongoDB `ERP.Attendance.HolidayCalendars`. In MongoDB:
  - Holiday 0 (New Year): `HolidayType._id = "3a249870-18c5-eb35-b782-7b26f5f35ccd"`
  - Holiday 1 (National Day): `HolidayType._id = "3a249870-18c5-eb35-b782-7b26f5f35ccd"`
  - Holiday 2 (Eid Holiday): `HolidayType._id = "3a249870-18c5-eb35-b782-7b26f5f35ccd"`
  The backend **completely bypassed validation** and never checked whether `3a249870-18c5-eb35-b782-7b26f5f35ccd` actually exists in the Master Holiday Types catalog!

* **Root Cause Analysis:**
  1. **Missing Master Catalog Existence Check:** In `CreateHolidayCalendarCommandValidator.cs`, validation is restricted to syntax (`Guid.TryParse` or `NotEmpty()`). It lacks an asynchronous existence check against the Holiday Type repository or Leaves service.
  2. **Blind Trust of Client-Supplied `holidayTypeName`:** The DTO accepts both `holidayTypeId` and `holidayTypeName`. Because the backend does not look up the real entity from master data, a malicious or mistaken client can supply arbitrary names and fake IDs, corrupting the attendance database.
  3. **Downstream Integration Failure:** When leave policies, holiday allowances, and punch compensation engines process timesheets for these dates, attempts to join `holidayTypeId` against master leave configurations will fail or throw unhandled `NullReferenceException`.

* **Developer Remediation (.NET 9 C# FluentValidation):**
  In `CreateHolidayCalendarCommandValidator.cs` and `UpdateHolidayCalendarCommandValidator.cs`:
  ```csharp
  // Inject IHolidayTypeRepository into validator
  RuleForEach(x => x.YearlyCalendar.HolidayLists).ChildRules(holiday =>
  {
      holiday.RuleFor(h => h.HolidayTypeId)
          .NotEmpty().WithMessage("holidayTypeId is required.")
          .MustAsync(async (typeId, cancellation) =>
          {
              // Validate foreign key existence in Master Holiday Types catalog
              return await _holidayTypeRepository.ExistsAsync(typeId, cancellation);
          })
          .WithMessage(h => $"HolidayTypeId '{h.HolidayTypeId}' does not exist in the Holiday Types master catalog.");
  });
  ```
  And in `CreateHolidayCalendarCommandHandler.cs`:
  ```csharp
  // Fetch verified holiday type from master catalog and populate canonical name:
  var masterHolidayType = await _holidayTypeRepository.GetByIdAsync(item.HolidayTypeId, cancellationToken);
  if (masterHolidayType == null)
  {
      throw new SbpValidationException($"HolidayTypeId '{item.HolidayTypeId}' is invalid.");
  }

  // Auto-populate HolidayTypeName from master catalog (do not trust raw client string):
  holidayItem.HolidayTypeName = masterHolidayType.Name;
  ```

---

"""

if pos_p4 != -1 and "DEFECT-20261103-04" not in text:
    text = text[:pos_p4] + defect_04_deep_dive + text[pos_p4:]

# 4. Update Part 5 Developer Checklist with Day 6 Checklist
day_6_checklist_target = """### 📅 Day 5: 02 November 2026 Checklist (Work Template DTO Validations & Invariants)
- [ ] **P0 (`DEFECT-20261102-10`):** Add chronological validation in `FixedTimeSlotValidator`: `RuleFor(x => x).Must(slot => TimeSpan.Parse(slot.EndTime) > TimeSpan.Parse(slot.StartTime)).When(x => !x.IsOvernightShift)`.
- [ ] **P1 (`DEFECT-20261102-01`):** In `Create*WorkTemplateCommandValidator`, enforce `RuleFor(x => x.TemplateName.En).NotEmpty().MaximumLength(100)`.
- [ ] **P1 (`DEFECT-20261102-03` & `04`):** In `Create*WorkTemplateCommandValidator`, enforce `RuleFor(x => x.ShortCode).Matches("^[A-Za-z0-9]{2,7}$")`.
- [ ] **P1 (`DEFECT-20261102-05`):** Enforce `RuleFor(x => x.TemplateType).IsInEnum().Must(t => (int)t > 0)`.
- [ ] **P1 (`DEFECT-20261102-06`):** Enforce `RuleFor(x => x.TotalWorkDurationInMinutes).GreaterThan(0).LessThanOrEqualTo(10080)`.
- [ ] **P1 (`DEFECT-20261102-07`):** Enforce `RuleFor(x => x.TotalWorkingDays).InclusiveBetween(1, 7)` and `TotalDaysOff.InclusiveBetween(0, 6)`.
- [ ] **P1 (`DEFECT-20261102-08`):** Enforce `RuleFor(x => x.WorkDurationInMinutes).GreaterThan(0).When(x => x.IsWorkingDay)`.
- [ ] **P1 (`DEFECT-20261102-09`):** Map abbreviated day strings (`"Mon"`, `"Tue"`) or enforce `1..7` in `FixedTimeSlots` 7-day validator.
- [ ] **P1 (`DEFECT-20261102-11`):** Invariant check: `(EndTime - StartTime).TotalMinutes == WorkDurationInMinutes`.
- [ ] **P1 (`DEFECT-20261102-12`):** Validate that `TotalWorkingDays == FixedTimeSlots.Count(s => s.IsWorkingDay)` and off days have 0 duration.
- [ ] **P1 (`DEFECT-20261102-13`):** Enforce `templateType` immutability in all `Update*WorkTemplateCommandValidator` classes.
"""

day_6_checklist_new = day_6_checklist_target + """
### 📅 Day 6: 03 November 2026 Checklist (Holiday List Module)
- [ ] **P2 (`DEFECT-20261103-01`):** In `SP.AttendanceSvc`, create a shared `AuditUser` composite record (`{ UserId, LoginId, Name, Email }`) populated from JWT claims. Stop storing plain email strings in `CreatedBy`.
- [ ] **P1 (`DEFECT-20261103-02` / `DEFECT-20261026-02`):** In `CreateHolidayCalendarCommandHandler.cs` and `UpdateHolidayCalendarCommandHandler.cs`, inject `ICurrentTenant` and populate `TenantName = new MultilingualString { En = _currentTenant.Name, Ar = _currentTenant.ArabicName }`. Stop persisting `TenantName: Object (empty)`.
- [ ] **P1 (`DEFECT-20261103-03`):** In `CreateHolidayCalendarCommandHandler.cs`, map `holidayCalendar.IsActive = command.IsActive;`. Do NOT hardcode `IsActive = true` when client sends `"isActive": false`.
- [ ] **P1 (`DEFECT-20261103-04`):** In `CreateHolidayCalendarCommandValidator.cs`, add `MustAsync` rule to validate that `holidayTypeId` exists in the Master Holiday Types catalog before persisting.
"""

if day_6_checklist_target in text and "Day 6: 03 November 2026 Checklist" not in text:
    text = text.replace(day_6_checklist_target, day_6_checklist_new)

with open('Attendance2_Defects_Gaps_and_Architecture_Inconsistencies_Report.md', 'w', encoding='utf-8') as f:
    f.write(text)

print(f"SUCCESS: Logged DEFECT-20261103-04 and Day 6 Checklist in Defect Report ({len(text)} characters)!")

