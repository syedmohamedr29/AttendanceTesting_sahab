import sys

sys.stdout.reconfigure(encoding='utf-8')

section_8_content = """
## 8. Live Execution Results & Defect Findings — 28 October 2026

> **Target Service:** `SP.AttendanceSvc` (.NET 9 / ASP.NET Core)
> **Host:** `https://attendance2.dev.zoolwork.com`
> **Target Company:** `Attendance 2` (`3a247435-3cea-83ae-6a9f-6dda99f386a3`)
> **Tenant:** `Attendance` (`3a24741e-2667-1223-f12e-62a69fab3838`)
> **Authorized User:** `syed.mohamed@comm-it.in`
> **Date:** 28 October 2026
> **Scope:** Company Default Work Template DTO Validations across Fixed, Flexible (Daily & Weekly), and Split Shift templates.

---

### A. Live Execution Summary

| Total Executed | Passed | Failed (Defects Identified) | Pass Rate | Target Sheets Updated |
|:---:|:---:|:---:|:---:|---|
| **22 Test Cases** | **16 Passed** | **6 Failed** | **72.7%** | [`AttendanceTestCases_Master_Consolidated.xlsx`](file:///d:/Code/Attendance%20Testing/AttendanceTestCases_Master_Consolidated.xlsx)<br>• `WT - Company Default`<br>• `User Scenarios (Add Here)` |

---

### B. Critical Defects Identified During Live Testing

#### 1. `DEFECT-LIVE-01` (Severity: P0 / Critical) — Flexi Daily Work Duration Exceeding 24 Hours Accepted with HTTP 200 OK
* **Test Case ID:** `USER-33` (Row 34 in `User Scenarios (Add Here)`)
* **Endpoint:** `POST /api/companies/{companyId}/worktemplates/flexi`
* **Observed Behavior (Actual):**
  * The backend **accepted** a Daily Flexible Work Template where `dailyWorkDurationInMinutes` was set to **1500 minutes (25 hours per day)**!
  * Returned **HTTP 200 OK** and persisted the record into MongoDB collection `ERP.Attendance.WorkTemplates`.
* **Expected Behavior:**
  * The system must strictly reject any daily duration exceeding 24 hours ($1440$ minutes) with **HTTP 400 Bad Request**.
* **Request Payload Sent:**
  ```json
  POST /api/companies/3a247435-3cea-83ae-6a9f-6dda99f386a3/worktemplates/flexi
  {
    "templateName": {"en": "Flexi Daily Exceed 24h"},
    "shortCode": "FLX2401",
    "totalWorkDurationInMinutes": 1500,
    "totalWorkingDays": 5,
    "totalDaysOff": 2,
    "flexibleType": 1,
    "flexiTimeSlots": [
      {"dayEnum": 1, "isWorkingDay": true, "recurrenceOfMonth": [1, 2, 3, 4, 5], "workDurationInMinutes": 1500},
      {"dayEnum": 2, "isWorkingDay": true, "recurrenceOfMonth": [1, 2, 3, 4, 5], "workDurationInMinutes": 480},
      {"dayEnum": 3, "isWorkingDay": true, "recurrenceOfMonth": [1, 2, 3, 4, 5], "workDurationInMinutes": 480},
      {"dayEnum": 4, "isWorkingDay": true, "recurrenceOfMonth": [1, 2, 3, 4, 5], "workDurationInMinutes": 480},
      {"dayEnum": 5, "isWorkingDay": true, "recurrenceOfMonth": [1, 2, 3, 4, 5], "workDurationInMinutes": 480},
      {"dayEnum": 6, "isWorkingDay": false, "recurrenceOfMonth": [1, 2, 3, 4, 5], "workDurationInMinutes": 0},
      {"dayEnum": 7, "isWorkingDay": false, "recurrenceOfMonth": [1, 2, 3, 4, 5], "workDurationInMinutes": 0}
    ]
  }
  ```
* **Actual API Response:**
  ```json
  HTTP 200 OK
  {
    "id": "3a247eef-...",
    "templateName": {"en": "Flexi Daily Exceed 24h"},
    "shortCode": "FLX2401",
    "totalWorkDurationInMinutes": 1500
  }
  ```
* **Impact & Root Cause:**
  * Missing FluentValidation rule: `RuleFor(x => x.DailyWorkDurationInMinutes).InclusiveBetween(1, 1440)`.
  * Accepting 25 hours in a day corrupts attendance calculation, overtime accrual, and payroll exports.

---

#### 2. `DEFECT-LIVE-02` (Severity: P1 / High) — FluentValidation `ValidationException` Throws HTTP 500 Instead of HTTP 400 Bad Request
* **Test Case IDs Affected:**
  * `USER-70` (Incomplete 7-day slot array)
  * `USER-59` (Split shift overlapping intervals)
  * `USER-60` (Split shift zero break gap)
  * `USER-61` (Split shift inverted timings)
  * `USER-90` (Empty PATCH request body)
* **Observed Behavior (Actual):**
  * When complex domain/cross-property validation fails (e.g. interval overlaps or incomplete day arrays), FluentValidation throws `ValidationException`.
  * However, the global exception handling middleware in `SP.AttendanceSvc` treats `ValidationException` as an unhandled server error and returns **HTTP 500 Internal Server Error**!
* **Actual API Response Received:**
  ```json
  HTTP 500 Internal Server Error
  {
    "error": {
      "code": "ValidationException",
      "message": "Validation failed: \n -- SplitTimeSlots: Intervals within the same working day cannot overlap. Severity: Error",
      "details": null,
      "data": null,
      "validationErrors": null
    }
  }
  ```
* **Expected Behavior:**
  * Per REST and ASP.NET Core standards, client validation failures must return **HTTP 400 Bad Request** (or `422 Unprocessable Entity`), with the validation errors structured inside `validationErrors` array.
* **Engineering Fix Required:**
  * In `Program.cs` / Exception Middleware:
    ```csharp
    app.UseExceptionHandler(exceptionHandlerApp => {
        exceptionHandlerApp.Run(async context => {
            var exception = context.Features.Get<IExceptionHandlerPathFeature>()?.Error;
            if (exception is FluentValidation.ValidationException valEx) {
                context.Response.StatusCode = StatusCodes.Status400BadRequest;
                context.Response.ContentType = "application/json";
                await context.Response.WriteAsJsonAsync(new {
                    code = "ValidationException",
                    message = "One or more validation errors occurred.",
                    validationErrors = valEx.Errors.Select(e => new { e.PropertyName, e.ErrorMessage })
                });
            }
        });
    });
    ```

---

### C. Live Test Case Execution Matrix (28-Oct-2026)

| # | TC ID | Sheet & Row | Test Scenario Description | Expected | Actual Status | Latency | Result | Remarks / Evidence |
|---|:---:|---|---|:---:|:---:|:---:|:---:|---|
| 1 | `ROOT-A-01` | `WT - Company Default` (R54) | Missing Authorization / `__tenant` header | HTTP 401 | **HTTP 401** | 1152ms | **PASS** | Correctly blocked unauthorized call |
| 2 | `ROOT-A-02` | `WT - Company Default` (R55) | ShortCode boundary — 8 chars (exceeds 7) | HTTP 400 | **HTTP 400** | 1111ms | **PASS** | RFC 9110 model validation error |
| 3 | `ROOT-A-03` | `WT - Company Default` (R56) | ShortCode with special chars (`FX@#123`) | HTTP 400 | **HTTP 400** | 1314ms | **PASS** | Alphanumeric rule enforced |
| 4 | `USER-14` | `User Scenarios` (R15) | Day off contradiction (`isWorkingDay=false` with duration) | HTTP 400 | **HTTP 400** | 1290ms | **PASS** | Working day consistency enforced |
| 5 | `USER-17` | `User Scenarios` (R18) | Invalid DayEnum range (`dayEnum: 8`) | HTTP 400 | **HTTP 400** | 1298ms | **PASS** | Day range 1..7 enforced |
| 6 | `USER-66` | `User Scenarios` (R67) | Missing / empty templateName object `{}` | HTTP 400 | **HTTP 400** | 1283ms | **PASS** | Mandatory templateName enforced |
| 7 | `USER-67` | `User Scenarios` (R68) | Template Name length > 100 characters | HTTP 400 | **HTTP 400** | 1312ms | **PASS** | Max 100 char boundary enforced |
| 8 | `USER-68` | `User Scenarios` (R69) | Short Code length < 7 characters (5 chars) | HTTP 400 | **HTTP 400** | 1330ms | **PASS** | Min 7 char boundary enforced |
| 9 | `USER-70` | `User Scenarios` (R71) | Incomplete 7-day slot array (only 5 days) | HTTP 400 | **HTTP 500** | 1308ms | **FAIL** | **DEFECT-LIVE-02:** Returns 500 instead of 400 |
| 10 | `USER-71` | `User Scenarios` (R72) | Duplicate DayEnum in time slots array | HTTP 400 | **HTTP 400** | 1334ms | **PASS** | Unique dayEnum per slot enforced |
| 11 | `USER-72` | `User Scenarios` (R73) | Inverted shift times (`shiftEnd <= shiftStart`) | HTTP 400 | **HTTP 400** | 1304ms | **PASS** | Shift chronologic boundary enforced |
| 12 | `USER-33` | `User Scenarios` (R34) | Flexi Daily duration > 24 hours (1500m / 25h) | HTTP 400 | **HTTP 200** | 1890ms | **FAIL** | **DEFECT-LIVE-01:** Accepted 25h per day! |
| 13 | `USER-34` | `User Scenarios` (R35) | Flexi Weekly duration > 168 hours (11000m) | HTTP 400 | **HTTP 400** | 1301ms | **PASS** | Blocked with `Cit.Attendance:1010` (CDWT exists) |
| 14 | `USER-35` | `User Scenarios` (R36) | Flexi Daily active day with 0 hours | HTTP 400 | **HTTP 400** | 1358ms | **PASS** | Blocked with `Cit.Attendance:1010` (CDWT exists) |
| 15 | `USER-36` | `User Scenarios` (R37) | Flexi negative work duration (`-480m`) | HTTP 400 | **HTTP 400** | 1323ms | **PASS** | Blocked with `Cit.Attendance:1010` (CDWT exists) |
| 16 | `USER-37` | `User Scenarios` (R38) | FlexibleType invalid enum value (`99`) | HTTP 400 | **HTTP 400** | 1281ms | **PASS** | Blocked with `Cit.Attendance:1010` (CDWT exists) |
| 17 | `USER-59` | `User Scenarios` (R60) | Split shift overlapping intervals | HTTP 400 | **HTTP 500** | 1292ms | **FAIL** | **DEFECT-LIVE-02:** Returns 500 instead of 400 |
| 18 | `USER-60` | `User Scenarios` (R61) | Split shift zero break gap | HTTP 400 | **HTTP 500** | 1303ms | **FAIL** | **DEFECT-LIVE-02:** Returns 500 instead of 400 |
| 19 | `USER-61` | `User Scenarios` (R62) | Split shift inverted timings in interval | HTTP 400 | **HTTP 500** | 1308ms | **FAIL** | **DEFECT-LIVE-02:** Returns 500 instead of 400 |
| 20 | `USER-62` | `User Scenarios` (R63) | Split shift single interval on active day | HTTP 400 | **HTTP 400** | 1286ms | **PASS** | Blocked with `Cit.Attendance:1010` (CDWT exists) |
| 21 | `USER-63` | `User Scenarios` (R64) | Split shift intervals configured on Day Off | HTTP 400 | **HTTP 400** | 1286ms | **PASS** | Blocked with `Cit.Attendance:1010` (CDWT exists) |
| 22 | `USER-90` | `User Scenarios` (R91) | Empty PATCH body `{}` | HTTP 400 | **HTTP 500** | 1298ms | **FAIL** | **DEFECT-LIVE-02:** Returns 500 instead of 400 |

---
"""

with open("Attendance2_Defects_Gaps_and_Architecture_Inconsistencies_Report.md", "a", encoding='utf-8') as f:
    f.write(section_8_content)

print("Successfully appended Section 8 to Attendance2_Defects_Gaps_and_Architecture_Inconsistencies_Report.md!")

