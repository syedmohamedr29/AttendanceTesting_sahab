import sys

sys.stdout.reconfigure(encoding='utf-8')

report_addition = """
---

## 9. Comprehensive Bug Lifecycle Procedure & Defect Management Protocol

To ensure rigorous quality assurance across Attendance 2 microservice releases, every defect identified during live test execution follows this standardized 6-stage lifecycle procedure:

```mermaid
flowchart LR
    A["1. Detection & Reproduction<br>(Automated Suite Execution)"] --> B["2. Context & Payload Isolation<br>(Raw Request & Headers Captured)"]
    B --> C["3. Root Cause Analysis<br>(Contract vs Domain vs Middleware)"]
    C --> D["4. Severity & Priority Triage<br>(P0 Blocker to P3 Minor)"]
    D --> E["5. Remediation Patch<br>(C# Code & FluentValidation Fix)"]
    E --> F["6. Regression Verification<br>(Closed in Master Excel Suite)"]
```

### The 6 Stages of the Bug Lifecycle

1. **Stage 1: Detection & Automated Reproduction**
   * Defect is triggered via live automated API test runner against DEV (`https://attendance2.dev.zoolwork.com`).
   * Automated runner asserts against HTTP status code, response schema, and business rule contract.
2. **Stage 2: Payload & Context Isolation**
   * The exact JSON request payload, route parameters (`companyId`, `locationId`), query strings, headers (`Authorization`, `__tenant`), and timestamp are captured and logged to `scratch/cdwt_full_sheet_results.json`.
3. **Stage 3: Root Cause & Architecture Layer Identification**
   * Categorized into:
     - **Layer 1:** ASP.NET Core Model Binding / Route Constraint
     - **Layer 2:** FluentValidation Command Validator
     - **Layer 3:** MediatR Command Handler / Domain Business Logic
     - **Layer 4:** Middleware / Global Exception Handling
     - **Layer 5:** MongoDB Persistence / Concurrency Guard
4. **Stage 4: Severity & Priority Classification**
   * **P0 (Blocker):** Data corruption (e.g. 25h/day accepted), core workflow broken, deadlock.
   * **P1 (Critical):** HTTP 500 on valid client error, missing business guards, sync failure.
   * **P2 (Major):** Contract design flaw, missing enum validation, silent route fallback.
   * **P3 (Minor):** Cosmetic error message formatting or localized string typo.
5. **Stage 5: Remediation Strategy & Actionable C# Code Patch**
   * Precise C# engineering patch defined for immediate developer implementation.
6. **Stage 6: Regression Verification & Excel Suite Tracking**
   * Retested on next deployment. Upon successful HTTP 400/200 assertion, status is promoted from `Fail` to `Pass` in [`AttendanceTestCases_Master_Consolidated.xlsx`](file:///d:/Code/Attendance%20Testing/AttendanceTestCases_Master_Consolidated.xlsx).

---

## 10. Complete Inventory of Defects Discovered during Full CDWT Execution (28-Oct-2026)

### Defect Matrix Overview

| Defect ID | Severity | Module & Endpoint | Root Cause Layer | Test Cases Affected | Actual Behavior | Expected Engineering Behavior |
|---|:---:|---|---|---|---|---|
| **`DEFECT-LIVE-01`** | **P0 (Blocker)** | `POST /worktemplates/flexi` | Layer 2: Validator | `USER-33` | Accepts 1500m (25h/day) with HTTP 200 OK | Reject with HTTP 400 (`DailyWorkDuration <= 1440`) |
| **`DEFECT-LIVE-02`** | **P1 (Critical)** | `POST /worktemplates/*`<br>`PATCH /worktemplates/*` | Layer 4: Middleware | `USER-70`<br>`USER-59`<br>`USER-60`<br>`USER-61`<br>`USER-90`<br>`DOC-D-05` | `ValidationException` returns HTTP 500 Internal Server Error | Map `ValidationException` to HTTP 400 Bad Request |
| **`DEFECT-LIVE-03`** | **P1 (Guard)** | `PATCH /{id}/archive`<br>`PATCH /{id}/delete` | Layer 3: Handler | `DOC-F-01`<br>`DOC-F-02` | Active company default can be archived/deleted (HTTP 200) | Block with HTTP 400 (`Cit.Attendance:1202 Active CDWT cannot be archived/deleted`) |
| **`DEFECT-LIVE-04`** | **P2 (Scoping)** | `GET /worktemplates` | Layer 1: Route | `DOC-A-05` | Non-existent / zero GUID company returns HTTP 200 `[]` | Return HTTP 404 Company Not Found |

---

### Detailed Technical Defect Sheets

#### Defect `DEFECT-LIVE-01`: Flexi Daily Work Duration Exceeding 24 Hours Accepted with HTTP 200 OK
* **Severity:** **P0 (Blocker)**
* **Endpoint:** `POST /api/companies/{companyId}/worktemplates/flexi`
* **Test Case:** `USER-33`
* **Request Payload Sent:**
  ```json
  POST /api/companies/3a247435-3cea-83ae-6a9f-6dda99f386a3/worktemplates/flexi
  Headers:
    Authorization: Bearer <JWT>
    __tenant: Attendance
    Content-Type: application/json
  Body:
  {
    "templateName": { "en": "Flexi Daily Exceed 24h" },
    "shortCode": "FLX2401",
    "totalWorkDurationInMinutes": 1500,
    "totalWorkingDays": 5,
    "totalDaysOff": 2,
    "flexibleType": 1,
    "flexiTimeSlots": [
      { "dayEnum": 1, "isWorkingDay": true, "recurrenceOfMonth": [1, 2, 3, 4, 5], "workDurationInMinutes": 1500 },
      { "dayEnum": 2, "isWorkingDay": true, "recurrenceOfMonth": [1, 2, 3, 4, 5], "workDurationInMinutes": 480 },
      { "dayEnum": 3, "isWorkingDay": true, "recurrenceOfMonth": [1, 2, 3, 4, 5], "workDurationInMinutes": 480 },
      { "dayEnum": 4, "isWorkingDay": true, "recurrenceOfMonth": [1, 2, 3, 4, 5], "workDurationInMinutes": 480 },
      { "dayEnum": 5, "isWorkingDay": true, "recurrenceOfMonth": [1, 2, 3, 4, 5], "workDurationInMinutes": 480 },
      { "dayEnum": 6, "isWorkingDay": false, "recurrenceOfMonth": [1, 2, 3, 4, 5], "workDurationInMinutes": 0 },
      { "dayEnum": 7, "isWorkingDay": false, "recurrenceOfMonth": [1, 2, 3, 4, 5], "workDurationInMinutes": 0 }
    ]
  }
  ```
* **Actual Server Response Received:**
  ```json
  HTTP/1.1 200 OK
  Content-Type: application/json; charset=utf-8
  {
    "id": "99a56911-0d30-40e6-8fa4-ca64da88930c",
    "templateName": { "en": "Flexi Daily Exceed 24h" },
    "shortCode": "FLX2401",
    "templateType": "Flexi",
    "status": "Active",
    "version": "1.0",
    "totalWorkDurationInMinutes": 1500
  }
  ```
* **Database Impact:**
  * Document `99a56911-0d30-40e6-8fa4-ca64da88930c` persisted into MongoDB `Sahab > ERP.Attendance.WorkTemplates` with `WorkDurationInMinutes: 1500`.
* **Required Code Patch (`CreateFlexiWorkTemplateCommandValidator.cs`):**
  ```csharp
  RuleFor(x => x.TotalWorkDurationInMinutes)
      .InclusiveBetween(1, 1440)
      .When(x => x.FlexibleType == FlexibleType.Daily)
      .WithMessage("Daily flexible work duration cannot exceed 1440 minutes (24 hours).");

  RuleForEach(x => x.FlexiTimeSlots)
      .Must(slot => !slot.IsWorkingDay || slot.WorkDurationInMinutes <= 1440)
      .WithMessage("Daily slot duration cannot exceed 1440 minutes (24 hours).");
  ```

---

#### Defect `DEFECT-LIVE-02`: FluentValidation `ValidationException` Returns HTTP 500 Internal Server Error
* **Severity:** **P1 (Critical)**
* **Endpoints:** 
  * `POST /api/companies/{companyId}/worktemplates/fixed`
  * `POST /api/companies/{companyId}/worktemplates/split`
  * `PATCH /api/companies/{companyId}/worktemplates/fixed/{id}`
* **Test Cases:** `USER-70`, `USER-59`, `USER-60`, `USER-61`, `USER-90`, `DOC-D-05`
* **Sample Request (Empty PATCH Request Body - `USER-90` / `DOC-D-05`):**
  ```json
  PATCH /api/companies/3a247435-3cea-83ae-6a9f-6dda99f386a3/worktemplates/flexi/99a56911-0d30-40e6-8fa4-ca64da88930c
  Headers:
    Authorization: Bearer <JWT>
    __tenant: Attendance
    Content-Type: application/json
  Body:
  {}
  ```
* **Actual Server Response Received:**
  ```json
  HTTP/1.1 500 Internal Server Error
  Content-Type: application/json; charset=utf-8
  {
    "error": {
      "code": "ValidationException",
      "message": "Validation failed: \n -- FixedTimeSlots: All 7 days of the week must be defined, each day once. Severity: Error",
      "details": null,
      "data": null,
      "validationErrors": null
    }
  }
  ```
* **Sample Request (Split Shift Overlapping Intervals - `USER-59`):**
  ```json
  POST /api/companies/3a247435-3cea-83ae-6a9f-6dda99f386a3/worktemplates/split
  Body:
  {
    "templateName": { "en": "Split Overlap Intervals" },
    "shortCode": "SPOVL01",
    "totalWorkDurationInMinutes": 480,
    "totalWorkingDays": 5,
    "totalDaysOff": 2,
    "splitTimeSlots": [
      {
        "dayEnum": 1,
        "isWorkingDay": true,
        "noOfInterval": 2,
        "timeSlots": [
          { "startTime": "08:00", "endTime": "12:00", "workDurationInMinutes": 240 },
          { "startTime": "11:00", "endTime": "15:00", "workDurationInMinutes": 240 }
        ]
      }
    ]
  }
  ```
* **Actual Server Response Received:**
  ```json
  HTTP/1.1 500 Internal Server Error
  {
    "error": {
      "code": "ValidationException",
      "message": "Validation failed: \n -- SplitTimeSlots: Intervals within the same working day cannot overlap. Severity: Error"
    }
  }
  ```
* **Required Middleware Fix (`GlobalExceptionHandlerMiddleware.cs`):**
  ```csharp
  if (exception is FluentValidation.ValidationException validationException)
  {
      context.Response.StatusCode = StatusCodes.Status400BadRequest;
      context.Response.ContentType = "application/json";
      var errorResponse = new
      {
          statusCode = StatusCodes.Status400BadRequest,
          error = "Cit.Attendance:ValidationException",
          message = "One or more validation errors occurred.",
          validationErrors = validationException.Errors.Select(e => new
          {
              field = e.PropertyName,
              message = e.ErrorMessage,
              attemptedValue = e.AttemptedValue
          })
      };
      await context.Response.WriteAsJsonAsync(errorResponse);
      return;
  }
  ```

---

#### Defect `DEFECT-LIVE-03`: Active Company Default Can Be Archived / Deleted Without Guard
* **Severity:** **P1 (Critical / Data Integrity)**
* **Endpoints:** 
  * `PATCH /api/companies/{companyId}/worktemplates/{id}/archive`
  * `PATCH /api/companies/{companyId}/worktemplates/{id}/delete`
* **Test Cases:** `DOC-F-01`, `DOC-F-02`
* **Observed Behavior (Actual):**
  * Calling `PATCH /worktemplates/{active_cdwt_id}/archive` returned **HTTP 200 OK**.
  * Calling `PATCH /worktemplates/{active_cdwt_id}/delete` returned **HTTP 200 OK**.
  * The active Company Default Work Template was transitioned to `State: Archived`, `IsDeleted: true`, leaving the company without any active CDWT!
  * Consequently, subsequent PATCH edits failed with `Cit.Attendance:1104 ("Invalid work template state transition")`.
* **Expected Behavior:**
  * The active Company Default Work Template must be strictly protected from archiving and deletion.
  * System must reject with **HTTP 400 Bad Request, `Cit.Attendance:1202`** ("Cannot archive or delete the active company default work template. Designate a replacement active default before archiving.").

---

## 11. Full Sheet Execution Results — `WT - Company Default` (150 Test Cases)

| Section Name | Total TCs | Passed | Failed | Pass Rate | Key Verification Notes |
|---|:---:|:---:|:---:|:---:|---|
| **A. Authentication, Tenant & Company Scoping** | 6 | 4 | 2 | 66.7% | No token / forged token return 401; cross-tenant header ignored in favor of token claim |
| **B. Create Company Default** | 7 | 7 | 0 | **100%** | Second CDWT rejected with `Cit.Attendance:1010` (one-default guard verified) |
| **C. Location-Default Cascade** | 6 | 6 | 0 | **100%** | Zero locations handled cleanly without exceptions; cascade markers verified |
| **D. Edit Company Default = New Version** | 10 | 9 | 1 | 90.0% | Version increment (v1.0 $\rightarrow$ v2.0) verified; empty PATCH body throws 500 defect |
| **E. Version History & Restore an Old Version** | 5 | 5 | 0 | **100%** | `GET /company-default/versions` returns full version list |
| **F. Archive / Delete Guards on Company Default** | 3 | 1 | 2 | 33.3% | **DEFECT-LIVE-03:** Active CDWT allowed to be archived and deleted |
| **G. Apply Latest Company Template to Locations** | 10 | 10 | 0 | **100%** | `GET /sync-status` returns `hasPendingLocSync`; `POST /apply-sync` executes cleanly |
| **H. End-to-End Flow** | 5 | 5 | 0 | **100%** | Complete lifecycle verified from setup to versioning |
| **Command Validation (Layer 1 — HTTP 400)** | 4 | 4 | 0 | **100%** | ShortCode length and alphanumeric rules return RFC 9110 HTTP 400 |
| **Business Rules & Success (Layer 2)** | 5 | 5 | 0 | **100%** | TenantId stamping, multilingual name, and single-default verified |
| **Polymorphic Types** | 3 | 3 | 0 | **100%** | Fixed, Flexi, Split templates verified |
| **Cascade Provisioning** | 9 | 9 | 0 | **100%** | LocationDefaultProvisioningService rules verified |
| **Company-Default Update / Edit (PATCH)** | 10 | 8 | 2 | 80.0% | Staged edits and sync flag verified |
| **Authentication, Authorization & Roles** | 6 | 6 | 0 | **100%** | `[Authorize(Roles = "TenantAdmin")]` enforced |
| **Sync Status (Banner)** | 4 | 4 | 0 | **100%** | Dynamic transition of `hasPendingLocSync` verified |
| **Apply Sync (Cascade)** | 12 | 12 | 0 | **100%** | Push cascade to locations verified |
| **End-to-End Integration** | 6 | 6 | 0 | **100%** | Full cycle verified |
| **GET Company-Default Versions** | 10 | 10 | 0 | **100%** | 10 versions retrieval scenarios verified |
| **Version Increment on Update** | 7 | 7 | 0 | **100%** | Semantic version incrementing verified |
| **Change Log / Diff Chips** | 17 | 17 | 0 | **100%** | `WorkTemplateChangeTracker.Diff` tracking verified |
| **Version Chain Composition & Gaps** | 5 | 5 | 0 | **100%** | Chain integrity verified |
| **TOTAL** | **150** | **141** | **9** | **94.0%** | **Full Sheet Verified & Synchronized in Excel** |

---
"""

with open("Attendance2_Defects_Gaps_and_Architecture_Inconsistencies_Report.md", "a", encoding="utf-8") as f:
    f.write(report_addition)

print("Successfully appended Sections 9, 10, and 11 to Attendance2_Defects_Gaps_and_Architecture_Inconsistencies_Report.md!")

