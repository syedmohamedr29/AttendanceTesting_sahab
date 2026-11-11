import sys

sys.stdout.reconfigure(encoding='utf-8')

file_path = 'Defects/Attendance2_Master_Defect_Log.md'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update Section 2 Matrix
old_row_06 = '| [`DEFECT-20261027-06`](#defect-20261027-06) | 🟠 P1 | Work Plans / Split | Split shift overlapping intervals & zero break gap: second slot starts before first ends, accepted | ``POST /workplans`` | [Evidence 09](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_09_split_overlap_500_validation_exception.png) |'
new_row_06 = '| [`DEFECT-20261027-06`](#defect-20261027-06) | 🟢 P1 | Work Templates / Split | **[FIXED 04-Nov]** Split shift overlapping intervals: HTTP 500 crash resolved; cleanly rejected with HTTP 400 | ``POST` / `PATCH /worktemplates/split`` | 🟢 Verified Fixed (HTTP 400) |'

old_row_07 = '| [`DEFECT-20261027-07`](#defect-20261027-07) | 🟠 P1 | Work Plans | Missing 7-day calendar invariant validation: schedule with 6 or 8 days throws unhandled 500 crash | ``POST /workplans`` | [Evidence 12](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_12_calendar_sum_not_7_500_validation_exception.png) |'
new_row_07 = '| [`DEFECT-20261027-07`](#defect-20261027-07) | 🟢 P1 | Work Templates | **[FIXED 04-Nov]** 7-Day calendar invariant (workingDays + daysOff != 7): HTTP 500 crash resolved; cleanly rejected with HTTP 400 | ``POST` / `PATCH /worktemplates/*`` | 🟢 Verified Fixed (HTTP 400) |'

if old_row_06 in content:
    content = content.replace(old_row_06, new_row_06)
    print("Replaced Matrix Row 06")
else:
    print("Could not find old_row_06")

if old_row_07 in content:
    content = content.replace(old_row_07, new_row_07)
    print("Replaced Matrix Row 07")
else:
    print("Could not find old_row_07")


# 2. Update Detail Section for DEFECT-20261027-06 and add DEFECT-20261027-07
old_sec_06 = """### <a id="defect-20261027-06"></a>🔴 DEFECT-20261027-06: Split Shift Overlapping Intervals & Zero Break Gap Accepted
- **Severity:** 🟠 P1 (Critical / Shift Invariant)
- **Target Route:** `POST /api/companies/{companyId}/workplans`
- **Database Target:** ``WorkPlans.TimeSlots``
- **Status:** ❌ **Open / Verified with Evidence**

#### 1. Problem Summary
Payload defines a split shift where interval 2 (`12:00:00` to `17:00:00`) starts before interval 1 (`09:00:00` to `13:00:00`) finishes. System accepts with HTTP 200 OK without validating interval separation.

#### 2. Steps to Reproduce
1. Send `POST /workplans` with overlapping split intervals.
1. Verify MongoDB document created.

#### 3. Exact Reproduction Request Payload (JSON)
```json
{
  "companyId": "3a249870-184c-0373-f344-015d602678d7",
  "planName": { "en": "Overlapping Split Plan", "ar": "خطة فترات متداخلة" },
  "intervals": [
    { "startTime": "09:00:00", "endTime": "13:00:00" },
    { "startTime": "12:00:00", "endTime": "17:00:00" }
  ]
}
```

#### 4. Server Response / Database Impact
HTTP 200 OK. Persisted in DB with overlapping split shift intervals.

#### 5. Photographic Proof & Evidence
| Evidence Image Preview | Live Verification Reference |
| :---: | :--- |
| ![DEFECT-20261027-06](../defect_evidence/evidence_09_split_overlap_500_validation_exception.png) | **File:** `evidence_09_split_overlap_500_validation_exception.png`<br><br>[🔍 Click to Open Full-Resolution Image](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_09_split_overlap_500_validation_exception.png)<br><br>*Overlapping split intervals accepted without validation.* |

#### 6. Developer Remediation (.NET 9 C#)
```csharp
RuleFor(x => x)
    .Must(p => p.Intervals[1].StartTime >= p.Intervals[0].EndTime)
    .WithMessage("Split shift intervals cannot overlap.");
```"""

new_sec_06_and_07 = """### <a id="defect-20261027-06"></a>🟢 DEFECT-20261027-06: Split Shift Overlapping Intervals & Zero Break Gap Cleanly Rejected with HTTP 400
- **Severity:** 🟠 P1 (Critical / Shift Invariant)
- **Target Route:** `POST` & `PATCH /api/companies/{companyId}/worktemplates/split`
- **Database Target:** `ERP.Attendance.WorkTemplates.SplitTimeSlots`
- **Related Test Case:** `USER-137` (`DTO-VAL-06`)
- **Status:** 🟢 **RESOLVED / VERIFIED FIXED LIVE (2026-11-04)**

#### 1. Problem Summary
Previously, sending split shift intervals where interval 2 overlaps interval 1 (e.g. `08:00-12:00` and `11:00-15:00`) triggered an unhandled `FluentValidation.ValidationException` crash with `HTTP 500 Internal Server Error` because the exception middleware failed to map validation exceptions to HTTP 400.

#### 2. Live Re-Verification Findings (04-Nov-2026)
* **Target Routes Tested:** `POST /worktemplates/split` and `PATCH /worktemplates/split/{id}`.
* **Payload Tested:** Working day interval 1: `08:00-12:00` and interval 2: `11:00-15:00` (1-hour overlap).
* **Live Server Response Received:** 🟢 **`HTTP 400 Bad Request`**
  ```json
  {
    "error": {
      "code": "Cit.Attendance:Validation",
      "message": "Split intervals must be in shift order, must not overlap, need a break between them and must fit within 23 hours 59 minutes. An interval may cross midnight.",
      "details": null,
      "data": null,
      "validationErrors": [
        {
          "message": "Split intervals must be in shift order, must not overlap, need a break between them and must fit within 23 hours 59 minutes. An interval may cross midnight.",
          "members": [ "SplitTimeSlots[0]" ]
        }
      ]
    }
  }
  ```
* **Verdict:** HTTP 500 crash eliminated; domain invariant strictly enforced with clean HTTP 400 Bad Request.

#### 3. Photographic Proof & Evidence
| Evidence Image Preview | Live Verification Reference |
| :---: | :--- |
| ![DEFECT-20261027-06](../defect_evidence/evidence_09_split_overlap_500_validation_exception.png) | **File:** `evidence_09_split_overlap_500_validation_exception.png`<br><br>[🔍 Click to Open Full-Resolution Image](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_09_split_overlap_500_validation_exception.png)<br><br>*Historical Proof: Original unhandled HTTP 500 ValidationException prior to middleware remediation.* |

---

### <a id="defect-20261027-07"></a>🟢 DEFECT-20261027-07: Missing 7-Day Calendar Invariant Validation (Sum != 7) Cleanly Rejected with HTTP 400
- **Severity:** 🟠 P1 (Critical / Calendar Invariant)
- **Target Route:** `POST` & `PATCH /api/companies/{companyId}/worktemplates/{fixed|flexi|split}`
- **Database Target:** `ERP.Attendance.WorkTemplates.TotalWorkingDays` & `TotalDaysOff`
- **Related Test Case:** `USER-138` (`DTO-VAL-07`)
- **Status:** 🟢 **RESOLVED / VERIFIED FIXED LIVE (2026-11-04)**

#### 1. Problem Summary
Previously, submitting work templates where `totalWorkingDays + totalDaysOff != 7` (e.g. `6 + 2 = 8` days, or `4 + 2 = 6` days) triggered an unhandled `FluentValidation.ValidationException` crash with `HTTP 500 Internal Server Error`.

#### 2. Live Re-Verification Findings (04-Nov-2026)
* **Target Routes Tested:** `POST /worktemplates/fixed` and `PATCH /worktemplates/fixed/{id}`.
* **Payloads Tested:**
  * Test Case 1: `totalWorkingDays: 6, totalDaysOff: 2` (Sum = 8 days)
  * Test Case 2: `totalWorkingDays: 4, totalDaysOff: 2` (Sum = 6 days)
* **Live Server Response Received:** 🟢 **`HTTP 400 Bad Request`**
  ```json
  {
    "error": {
      "code": "Cit.Attendance:Validation",
      "message": "Total working days and total days off must add up to 7. Total working days and total days off must match the number of working and off days in the week.",
      "details": null,
      "data": null,
      "validationErrors": [
        {
          "message": "Total working days and total days off must add up to 7.",
          "members": [ "" ]
        },
        {
          "message": "Total working days and total days off must match the number of working and off days in the week.",
          "members": [ "" ]
        }
      ]
    }
  }
  ```
* **Verdict:** HTTP 500 crash eliminated; calendar 7-day invariant strictly enforced with clean HTTP 400 Bad Request.

#### 3. Photographic Proof & Evidence
| Evidence Image Preview | Live Verification Reference |
| :---: | :--- |
| ![DEFECT-20261027-07](../defect_evidence/evidence_12_calendar_sum_not_7_500_validation_exception.png) | **File:** `evidence_12_calendar_sum_not_7_500_validation_exception.png`<br><br>[🔍 Click to Open Full-Resolution Image](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_12_calendar_sum_not_7_500_validation_exception.png)<br><br>*Historical Proof: Original unhandled HTTP 500 ValidationException crash prior to middleware remediation.* |"""

if old_sec_06 in content:
    content = content.replace(old_sec_06, new_sec_06_and_07)
    print("Replaced Section 06 & Added Section 07 successfully.")
else:
    print("Could not find old_sec_06")


# 3. Update Checklist
old_chk_06 = "- [ ] **P1 (`DEFECT-20261027-06`):** Assert non-overlapping split shift intervals in Work Plans."
new_chk_06 = "- [x] **P1 (`DEFECT-20261027-06`):** Assert non-overlapping split shift intervals in Work Plans & Templates. *(Verified Fixed Live 2026-11-04 with HTTP 400)*"

old_chk_07 = "- [ ] **P1 (`DEFECT-20261027-07`):** Assert exactly 7 calendar days in weekly Work Plan schedules."
new_chk_07 = "- [x] **P1 (`DEFECT-20261027-07`):** Assert exactly 7 calendar days in weekly schedules. *(Verified Fixed Live 2026-11-04 with HTTP 400)*"

if old_chk_06 in content:
    content = content.replace(old_chk_06, new_chk_06)
    print("Replaced Checklist 06")
else:
    print("Could not find old_chk_06")

if old_chk_07 in content:
    content = content.replace(old_chk_07, new_chk_07)
    print("Replaced Checklist 07")
else:
    print("Could not find old_chk_07")

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print(f"Updated {file_path} successfully.")

