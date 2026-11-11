import sys

sys.stdout.reconfigure(encoding='utf-8')

file_path = 'Attendance2_Defects_Gaps_and_Architecture_Inconsistencies_Report.md'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update Matrix
old_m6 = '| **`DEFECT-20261027-06`**<br>(`DTO-VAL-06` / `USER-137`) | **P0 (Integrity)** | `POST/PATCH /worktemplates/split` | Split shift permits overlapping intervals and contiguous 0-gap intervals | Strictly enforce chronological gap between intervals | **❌ STILL FAILING (HTTP 500)** (Unhandled Exception) |'
new_m6 = '| **`DEFECT-20261027-06`**<br>(`DTO-VAL-06` / `USER-137`) | **P0 (Integrity)** | `POST/PATCH /worktemplates/split` | Split shift permits overlapping intervals and contiguous 0-gap intervals | Strictly enforce chronological gap between intervals | **🟢 FIXED** (HTTP 400 Bad Request with Cit.Attendance:Validation) |'

old_m7 = '| **`DEFECT-20261027-07`**<br>(`DTO-VAL-07` / `USER-138`) | **P0 (Invariant)** | `POST/PATCH /worktemplates/*` | Payload accepting `totalWorkingDays + totalDaysOff != 7` without rejection | Enforce calendar invariant sum == 7 | **🟢 FIXED** (HTTP 400 Bad Request with Cit.Attendance:Validation) |'

if old_m6 in content:
    content = content.replace(old_m6, new_m6)
    print("Replaced Matrix Row 06")
else:
    print("Could not find old_m6")

# Note: Check if old_m7 was already replaced or is still present
old_m7_prev = '| **`DEFECT-20261027-07`**<br>(`DTO-VAL-07` / `USER-138`) | **P0 (Invariant)** | `POST/PATCH /worktemplates/*` | Payload accepting `totalWorkingDays + totalDaysOff != 7` without rejection | Enforce calendar invariant sum == 7 | **❌ STILL FAILING (HTTP 500)** (Unhandled Exception) |'
if old_m7_prev in content:
    content = content.replace(old_m7_prev, old_m7)
    print("Replaced Matrix Row 07")
else:
    print("Could not find old_m7_prev")


# 2. Update Live Re-Test Section 6 (DEFECT-20261027-06)
old_sec6 = """#### 6. `DEFECT-20261027-06` (`USER-137`): Split Shift Overlapping Intervals & Zero Break Gap
* **Defect Description:** Split shifts previously allowed overlapping intervals (e.g. `08:00-12:00` and `11:00-15:00`).
* **Live Test Execution:**
  ```http
  POST /api/companies/3a247435-e31d-ef15-8cc9-62c587f4eb3f/worktemplates/split HTTP/1.1
  Host: attendance2.dev.zoolwork.com
  Authorization: Bearer <JWT>
  Content-Type: application/json

  {
    "templateName": { "en": "Split Overlap Proof UI" },
    "shortCode": "SPLOV3",
    "totalWorkDurationInMinutes": 480,
    "totalWorkingDays": 5,
    "totalDaysOff": 2,
    "splitTimeSlots": [
      {
        "dayEnum": 1,
        "isWorkingDay": true,
        "recurrenceOfMonth": [1,2,3,4,5],
        "workDurationInMinutes": 480,
        "noOfInterval": 2,
        "timeSlots": [
          { "startTime": "08:00", "endTime": "12:00", "workDurationInMinutes": 240 },
          { "startTime": "11:00", "endTime": "15:00", "workDurationInMinutes": 240 }
        ]
      },
      ...
    ]
  }
  ```
* **Actual Server Response Received:**
  ```http
  HTTP/1.1 500 Internal Server Error
  Content-Type: text/plain; charset=utf-8

  FluentValidation.ValidationException: Validation failed: 
   -- SplitTimeSlots[0]: Split intervals on a working day must not overlap and must have a break gap. Severity: Error
     at MediatR.Pipeline.RequestValidationBehavior`2.Handle(...)
     at SP.AttendanceSvc.Infrastructure.Middlewares.GlobalExceptionHandlerMiddleware.InvokeAsync(...)
  ```
* **Root Cause & Diagnosis:**
  The developer correctly wrote the domain rule: `"Split intervals on a working day must not overlap and must have a break gap."`. However, because the global exception middleware does not catch `ValidationException`, it triggers an **unhandled HTTP 500 Server Crash** instead of returning HTTP 400 Bad Request!
* **Status:** **❌ STILL FAILING (HTTP 500 CRASH)**. Blocked by missing middleware exception mapping (`DEFECT-20261028-02`).
* **Visual Evidence:**

![Split Overlap HTTP 500 ValidationException](defect_evidence/evidence_09_split_overlap_500_validation_exception.png)"""

new_sec6 = """#### 6. `DEFECT-20261027-06` (`USER-137`): Split Shift Overlapping Intervals & Zero Break Gap
* **Defect Description:** Split shifts previously allowed overlapping intervals (e.g. `08:00-12:00` and `11:00-15:00`), which initially threw an unhandled `FluentValidation.ValidationException` (HTTP 500 crash).
* **Historical Baseline (28-Oct-2026):** `HTTP 500 Internal Server Error` (Unhandled exception in middleware).
* **Live Re-Verification (04-Nov-2026):**
  * **Test Execution:** Sent `POST` & `PATCH /api/companies/{companyId}/worktemplates/split` with Day 1 intervals: `08:00-12:00` and `11:00-15:00` (1-hour overlap).
  * **Actual Server Response Received:** 🟢 **`HTTP 400 Bad Request`**
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
* **Status:** **🟢 VERIFIED FIXED (04-Nov-2026)**. Middleware mapping is active; overlapping intervals are cleanly rejected with HTTP 400 Bad Request.
* **Historical Photographic Evidence (Prior to Fix):**

![Split Overlap HTTP 500 ValidationException](defect_evidence/evidence_09_split_overlap_500_validation_exception.png)"""

if old_sec6 in content:
    content = content.replace(old_sec6, new_sec6)
    print("Replaced Section 06")
else:
    print("Could not find old_sec6")


# 3. Update Live Re-Test Section 7 (DEFECT-20261027-07)
old_sec7 = """#### 7. `DEFECT-20261027-07` (`USER-138`): Missing 7-Day Calendar Invariant Validation
* **Defect Description:** Payload accepting `totalWorkingDays + totalDaysOff != 7` (e.g. `6 + 2 = 8`).
* **Live Test Execution:**
  ```http
  POST /api/companies/3a247435-e31d-ef15-8cc9-62c587f4eb3f/worktemplates/fixed HTTP/1.1
  Host: attendance2.dev.zoolwork.com
  Authorization: Bearer <JWT>
  Content-Type: application/json

  {
    "templateName": { "en": "Calendar Invariant Fail" },
    "shortCode": "INV8DAY",
    "totalWorkDurationInMinutes": 2880,
    "totalWorkingDays": 6,
    "totalDaysOff": 2,
    "fixedTimeSlots": [ ... ]
  }
  ```
* **Actual Server Response Received:**
  ```http
  HTTP/1.1 500 Internal Server Error
  Content-Type: text/plain; charset=utf-8

  FluentValidation.ValidationException: Validation failed: 
   -- TotalWorkingDays: Total working days and total days off must add up to 7. Severity: Error
     at MediatR.Pipeline.RequestValidationBehavior`2.Handle(...)
     at SP.AttendanceSvc.Infrastructure.Middlewares.GlobalExceptionHandlerMiddleware.InvokeAsync(...)
  ```
* **Root Cause & Diagnosis:**
  Similar to Defect 06, the calendar invariant validator was implemented by the developer (`"Total working days and total days off must add up to 7."`), but because `ValidationException` is unhandled by the middleware, it crashes with **HTTP 500 Internal Server Error** instead of returning HTTP 400 Bad Request!
* **Status:** **❌ STILL FAILING (HTTP 500 CRASH)**. Blocked by missing middleware exception mapping (`DEFECT-20261028-02`).
* **Visual Evidence:**

![Calendar Sum Not 7 HTTP 500 ValidationException](defect_evidence/evidence_12_calendar_sum_not_7_500_validation_exception.png)"""

new_sec7 = """#### 7. `DEFECT-20261027-07` (`USER-138`): Missing 7-Day Calendar Invariant Validation
* **Defect Description:** Payload accepting `totalWorkingDays + totalDaysOff != 7` (e.g. `6 + 2 = 8`), which initially threw an unhandled `FluentValidation.ValidationException` (HTTP 500 crash).
* **Historical Baseline (28-Oct-2026):** `HTTP 500 Internal Server Error` (Unhandled exception in middleware).
* **Live Re-Verification (04-Nov-2026):**
  * **Test Execution:** Sent `POST` & `PATCH /api/companies/{companyId}/worktemplates/fixed` with `totalWorkingDays: 6` and `totalDaysOff: 2` (Sum = 8 days), and `totalWorkingDays: 4` and `totalDaysOff: 2` (Sum = 6 days).
  * **Actual Server Response Received:** 🟢 **`HTTP 400 Bad Request`**
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
* **Status:** **🟢 VERIFIED FIXED (04-Nov-2026)**. Middleware mapping is active; calendar 7-day invariant is cleanly enforced with HTTP 400 Bad Request.
* **Historical Photographic Evidence (Prior to Fix):**

![Calendar Sum Not 7 HTTP 500 ValidationException](defect_evidence/evidence_12_calendar_sum_not_7_500_validation_exception.png)"""

if old_sec7 in content:
    content = content.replace(old_sec7, new_sec7)
    print("Replaced Section 07")
else:
    print("Could not find old_sec7")

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print(f"Updated {file_path} successfully.")

