import sys

sys.stdout.reconfigure(encoding='utf-8')

content = """# Attendance 2: Technical Defect Report, API Design Gaps & Architecture Consistency Review

> **Target Microservices:** `SP.AttendanceSvc` (.NET 9 / ASP.NET Core) & `SP.CompanySvc` (.NET 8)  
> **Environment:** DEV (`https://attendance2.dev.zoolwork.com` & `https://company8.dev.zoolwork.com`)  
> **Databases:**  
> • Attendance 2: MongoDB `Sahab` on `10.1.0.4:27018` (Collections: `ERP.Attendance.*`)  
> • Company Service: MongoDB `CompanySvcNET8test` (Collection: `CompaniesMaster`)  
> **Review Stakeholders:** QA Team (Shivam, Naushad, Syed Mohamed), Engineering Lead (Khalid)  
> **Master Test Suite Reference:** [`AttendanceTestCases_Master_Consolidated.xlsx`](file:///d:/Code/Attendance%20Testing/AttendanceTestCases_Master_Consolidated.xlsx)  
> **Current Status Date:** 28 October 2026  

---

## 📅 Quick Navigation — Date-Wise Defect Index

Jump directly to any date's findings, payloads, and code fixes:

* [**📅 Part 1: Defects Discovered on 26 October 2026**](#-part-1-defects-identified-on-26-october-2026) — *Core Architecture, Data Integrity & Cross-Service Synchronization (4 Issues)*
* [**📅 Part 2: Defects Discovered on 27 October 2026**](#-part-2-defects-identified-on-27-october-2026) — *DTO Validations, Model Binding Traps & Schema Gaps (7 Issues)*
* [**📅 Part 3: Defects Discovered on 28 October 2026 (LIVE EXECUTION)**](#-part-3-defects-identified-on-28-october-2026-live-execution) — *Live API Payloads, 25h/day Acceptance, HTTP 500 Validation Exceptions & Full CDWT Run (4 Issues)*
* [**🔄 Part 4: Standardized Bug Lifecycle Procedure**](#-part-4-standardized-bug-lifecycle-procedure) — *6-Stage Protocol for Defect Discovery, Triage & Verification*
* [**✅ Part 5: Actionable Developer Checklist (Date-Wise)**](#-part-5-actionable-developer-checklist-date-wise) — *Consolidated Engineering Action Items for Khalid's Team*

---

# 📅 Part 1: Defects Identified on 26 October 2026
**Theme:** Core Architecture, Data Integrity & Cross-Service Synchronization

### Summary Matrix (26-Oct-2026)

| Defect ID | Severity | Module & Endpoint | Summary of Defect | Expected Behavior | Status |
|:---:|:---:|---|---|---|:---:|
| **`DEFECT-20261026-01`**<br>(`USER-01`) | **P1 (Blocker)** | `POST /worktemplates/{fixed\|flexi\|split}`<br>*(Cross-Svc to `SP.CompanySvc`)* | Creating a CDWT does **not** update `CompaniesMaster.CompanyChecklist.WorkSchedulesCreated` | Auto-publish event to set `WorkSchedulesCreated = true` in Company Service | **Open** |
| **`DEFECT-20261026-02`**<br>(`USER-02`) | **P1 (Data)** | `POST /worktemplates/fixed`<br>`Sahab > ERP.Attendance.WorkTemplates` | `TenantName` is hardcoded as string `"Placeholder Tenant"` in Mongo | Read real tenant name from JWT / Identity Service | **Open** |
| **`DEFECT-20261026-03`**<br>(`USER-03`) | **P2 (Design)** | All Modules (`WorkTemplates`, `WorkPlans`, `Policies`) | `CreatedBy` only stores plain email string instead of composite object | Harmonize with ERP standard composite identity object | **Open** |
| **`DEFECT-20261026-04`**<br>(`USER-04`) | **P2 (Design)** | `POST /worktemplates/fixed` | Request body DTO expects `tenantId`, `tenantName`, `companyId`, `locationId` | Deprecate body fields; read from Route, Query & JWT | **Open** |

---

### Detailed Defect Deep-Dives (26-Oct-2026)

#### Defect `DEFECT-20261026-01` (`USER-01`): Cross-Service Synchronization Failure
* **Affected Endpoint:** `POST /api/companies/{companyId}/worktemplates/{fixed|flexi|split}`
* **Observed Issue:** 
  Creating a Company Default Work Template successfully stores the template in Attendance 2 DB (`ERP.Attendance.WorkTemplates`), but **fails** to notify Company Service. In `CompanySvcNET8test > CompaniesMaster`, `CompanyChecklist.WorkSchedulesCreated` remains `false`.
* **Photographic Evidence:**
  ![WorkSchedulesCreated is false](defect_evidence/evidence_02_companiesmaster_checklist_false.png)
* **Impact:** 
  The Company Onboarding Wizard in the Portal displays the Work Schedule step as incomplete, blocking tenant configuration progression.
* **Developer Fix Required (`SP.AttendanceSvc`):**
  Publish an asynchronous integration event `CompanyWorkScheduleCreatedIntegrationEvent` via MassTransit/RabbitMQ:
  ```csharp
  await _publishEndpoint.Publish(new CompanyWorkScheduleCreatedIntegrationEvent
  {
      CompanyId = command.CompanyId,
      TenantId = currentTenant.Id,
      WorkScheduleId = createdTemplate.Id,
      Timestamp = DateTime.UtcNow
  });
  ```

---

#### Defect `DEFECT-20261026-02` (`USER-02`): Hardcoded `TenantName = "Placeholder Tenant"`
* **Affected Endpoint:** `POST /api/companies/{companyId}/worktemplates/fixed`
* **Observed Issue:**
  In MongoDB collection `Sahab > ERP.Attendance.WorkTemplates`, newly created records persist the literal string `"Placeholder Tenant"` in `TenantName.en.name`.
* **Photographic Evidence:**
  ![Hardcoded Placeholder Tenant](defect_evidence/evidence_01_worktemplates_created_with_placeholder.png)
  ![Detail of Placeholder Tenant](defect_evidence/evidence_03_tenantname_placeholder_detail.png)
* **Technical Root Cause:**
  In `CreateFixedWTCommandHandler.cs`:
  ```csharp
  // BUG: Hardcoded dummy fallback
  var tenantName = new MultilingualString { En = new LocalizedString { Name = "Placeholder Tenant" } };
  ```
* **Developer Fix Required:**
  Inject `ICurrentTenant` and resolve tenant name dynamically from Identity / SaaS context:
  ```csharp
  var tenantName = new MultilingualString { 
      En = new LocalizedString { Name = _currentTenant.Name ?? "Default Tenant" } 
  };
  ```

---

#### Defect `DEFECT-20261026-03` (`USER-03`): `CreatedBy` Audit Field Formatting Inconsistency
* **Affected Scope:** All Attendance 2 MongoDB collections (`ERP.Attendance.*`).
* **Observed Issue:**
  Attendance 2 persists `CreatedBy` as a raw string (e.g. `"syed.mohamed@comm-it.in"`). In contrast, benchmark ERP modules (`TaskApprovals`, Identity Service) persist structured identity objects.
* **Photographic Evidence:**
  ![Raw String in Attendance 2](defect_evidence/evidence_05_createdby_plain_email_highlighted.png)
  ![Composite Identity Object in Benchmark](defect_evidence/evidence_04_benchmark_createdby_composite_object.png)
* **Architectural Recommendation:**
  Align with engineering lead Khalid on whether to retain string email for CQRS simplicity or enrich with `UserId` and `FullName`.

---

#### Defect `DEFECT-20261026-04` (`USER-04`): Body vs. Route/JWT Parameter Redundancy
* **Affected Endpoint:** `POST /api/companies/{companyId}/worktemplates/fixed`
* **Observed Issue:**
  The request body DTO `FixedWorkTemplateDto` expects `tenantId`, `tenantName`, `companyId`, and `locationId`, which are already specified in the URL route and JWT claims.
* **Developer Fix Required:**
  Mark these fields `[JsonIgnore]` or remove them from the command DTO.

---

# 📅 Part 2: Defects Identified on 27 October 2026
**Theme:** DTO Validation Soft Spots, Model Binding Traps & Schema Invariants

### Summary Matrix (27-Oct-2026)

| Defect ID | Severity | Module & Endpoint | Summary of Defect | Expected Behavior | Status |
|:---:|:---:|---|---|---|:---:|
| **`DEFECT-20261027-01`**<br>(`DTO-VAL-01`) | **P1 (Crash)** | `POST /workplans` | Omitting `?locationId=` query parameter throws unhandled HTTP 500 `SimpleException` | Validate query with HTTP 400 Bad Request | **Open** |
| **`DEFECT-20261027-02`**<br>(`DTO-VAL-02`) | **P2 (Contract)** | `POST /attpolicies/*` | Command validator validates `CreatedBy` string format, causing false 400 errors | Read `CreatedBy` from JWT; remove DTO validation | **Open** |
| **`DEFECT-20261027-03`**<br>(`DTO-VAL-03`) | **P2 (Boundary)** | `POST /attpolicies/grace-period` | Submitting negative grace minutes (`-15`) accepted into DB without validation | Reject negative numbers with HTTP 400 (`>= 0`) | **Open** |
| **`DEFECT-20261027-04`**<br>(`DTO-VAL-04`) | **P2 (Boundary)** | `POST /attpolicies/break` | Submitting negative break duration (`-60`) accepted into DB without validation | Reject non-positive duration with HTTP 400 (`> 0`) | **Open** |
| **`DEFECT-20261027-05`**<br>(`DTO-VAL-05`) | **P0 (Deadlock)** | `POST /worktemplates/{fixed\|flexi\|split}` | Request Header `Location: {guid}` auto-binds to `locationId`, triggering `Cit.Attendance:1205` | Sanitize location binding during initial CDWT setup | **Open** |
| **`DEFECT-20261027-06`**<br>(`DTO-VAL-06`) | **P0 (Integrity)** | `POST/PATCH /worktemplates/split` | Split shift permits overlapping intervals and contiguous 0-gap intervals | Strictly enforce chronological gap between intervals | **Open** |
| **`DEFECT-20261027-07`**<br>(`DTO-VAL-07`) | **P0 (Invariant)** | `POST/PATCH /worktemplates/*` | Payload accepting `totalWorkingDays + totalDaysOff != 7` without rejection | Enforce calendar invariant sum == 7 | **Open** |

---

### Detailed Defect Deep-Dives (27-Oct-2026)

#### Defect `DEFECT-20261027-01`: Missing `locationId` in Work Plan DTO Causes HTTP 500 Crash
* **Endpoint:** `POST /api/companies/{companyId}/workplans`
* **Root Cause:**
  The command handler expects `locationId` without checking for `Guid.Empty` or null:
  ```csharp
  // Causes unhandled NullReferenceException / SimpleException (HTTP 500)
  var location = await _locationRepo.GetByIdAsync(request.LocationId);
  ```
* **Required Fix:** Add rule in `CreateWorkPlanCommandValidator`:
  ```csharp
  RuleFor(x => x.LocationId).NotEmpty().WithMessage("LocationId query parameter is mandatory.");
  ```

---

#### Defect `DEFECT-20261027-05`: Header Location Model Binding Trap during First-Time CDWT Setup
* **Endpoint:** `POST /api/companies/{companyId}/worktemplates/{fixed|flexi|split}`
* **Root Cause:**
  When browser UI passes header `Location: {guid}`, ASP.NET Core model binder incorrectly binds the header value to the `locationId` parameter. Because company default requires `locationId == Guid.Empty`, Attendance 2 rejects with:
  `Cit.Attendance:1205: Company Default Work Template must be created before location templates.`
  This creates an onboarding deadlock!
* **Required Fix:** In controller action, explicitly bind from query only:
  ```csharp
  [HttpPost("fixed")]
  public async Task<IActionResult> CreateFixed([FromRoute] Guid companyId, [FromQuery] Guid? locationId, [FromBody] FixedWorkTemplateDto dto)
  ```

---

#### Defect `DEFECT-20261027-06`: Split Shift Overlapping Intervals & Zero Break Gap
* **Endpoint:** `POST/PATCH /api/companies/{companyId}/worktemplates/split`
* **Root Cause:**
  Missing interval cross-validation allows contiguous slots (e.g. 08:00-12:00 and 12:00-16:00) which should be configured as a continuous fixed shift, or overlapping slots (08:00-12:00 and 11:00-15:00).
* **Required Fix:** In `SplitWorkTemplateCommandValidator`:
  ```csharp
  RuleFor(x => x.SplitTimeSlots)
      .Must(slots => slots.All(s => s.Intervals.Zip(s.Intervals.Skip(1), (a, b) => a.ShiftEnd < b.ShiftStart).All(x => x)))
      .WithMessage("Split intervals within the same working day cannot overlap and must have a break gap.");
  ```

---

# 📅 Part 3: Defects Identified on 28 October 2026 (LIVE EXECUTION)
**Theme:** Live API Execution, Real Payloads, 25h/day Acceptance, HTTP 500 Validation Exceptions & Full CDWT Run

### Live Execution Summary Dashboard (28-Oct-2026)
* **Target Company:** `Attendance 2` (`3a247435-3cea-83ae-6a9f-6dda99f386a3`)
* **Tenant:** `Attendance` (`3a24741e-2667-1223-f12e-62a69fab3838`)
* **Authorized User:** `syed.mohamed@comm-it.in`
* **Live Test Executions:** 172 Total (22 Granular DTO Tests + 150 Full CDWT Sheet Tests)
* **Master Excel Updated:** [`AttendanceTestCases_Master_Consolidated.xlsx`](file:///d:/Code/Attendance%20Testing/AttendanceTestCases_Master_Consolidated.xlsx)

### Summary Matrix (28-Oct-2026)

| Defect ID | Severity | Module & Endpoint | Summary of Defect | Expected Behavior | Status |
|:---:|:---:|---|---|---|:---:|
| **`DEFECT-20261028-01`**<br>(`USER-33` / `LIVE-01`) | **P0 (Blocker)** | `POST /worktemplates/flexi` | Backend accepts 1500m (25h/day) with **HTTP 200 OK** | Reject with HTTP 400 (`DailyWorkDuration <= 1440`) | **Open** |
| **`DEFECT-20261028-02`**<br>(`USER-70`, `59-61`, `90`, `DOC-D-05`) | **P1 (Critical)** | `POST /worktemplates/*`<br>`PATCH /worktemplates/*` | FluentValidation `ValidationException` throws **HTTP 500** instead of 400 | Map `ValidationException` to HTTP 400 Bad Request | **Open** |
| **`DEFECT-20261028-03`**<br>(`DOC-F-01`, `DOC-F-02`) | **P1 (Guard)** | `PATCH /{id}/archive`<br>`PATCH /{id}/delete` | Active Company Default can be archived/deleted (**HTTP 200 OK**) without guard | Block with HTTP 400 (`Cit.Attendance:1202 Active CDWT protected`) | **Open** |
| **`DEFECT-20261028-04`**<br>(`DOC-A-05`) | **P2 (Scoping)** | `GET /worktemplates` | Cross-company query with zero/invalid GUID returns **HTTP 200 `[]`** | Return HTTP 404 Company Not Found | **Open** |

---

### Detailed Defect Deep-Dives (28-Oct-2026)

#### Defect `DEFECT-20261028-01`: Flexi Daily Work Duration Exceeding 24 Hours Accepted with HTTP 200 OK
* **Severity:** **P0 (Blocker)**
* **Endpoint:** `POST /api/companies/{companyId}/worktemplates/flexi`
* **Test Case:** `USER-33`
* **Exact Request Payload Sent:**
  ```http
  POST /api/companies/3a247435-3cea-83ae-6a9f-6dda99f386a3/worktemplates/flexi HTTP/1.1
  Host: attendance2.dev.zoolwork.com
  Authorization: Bearer <JWT>
  __tenant: Attendance
  Content-Type: application/json

  {
    "templateName": { "en": "Flexi Daily Exceed 24h" },
    "shortCode": "FLX2401",
    "totalWorkDurationInMinutes": 1500,
    "totalWorkingDays": 5,
    "totalDaysOff": 2,
    "flexibleType": 1,
    "flexiTimeSlots": [
      { "dayEnum": 1, "isWorkingDay": true, "recurrenceOfMonth": [1,2,3,4,5], "workDurationInMinutes": 1500 },
      { "dayEnum": 2, "isWorkingDay": true, "recurrenceOfMonth": [1,2,3,4,5], "workDurationInMinutes": 480 },
      { "dayEnum": 3, "isWorkingDay": true, "recurrenceOfMonth": [1,2,3,4,5], "workDurationInMinutes": 480 },
      { "dayEnum": 4, "isWorkingDay": true, "recurrenceOfMonth": [1,2,3,4,5], "workDurationInMinutes": 480 },
      { "dayEnum": 5, "isWorkingDay": true, "recurrenceOfMonth": [1,2,3,4,5], "workDurationInMinutes": 480 },
      { "dayEnum": 6, "isWorkingDay": false, "recurrenceOfMonth": [1,2,3,4,5], "workDurationInMinutes": 0 },
      { "dayEnum": 7, "isWorkingDay": false, "recurrenceOfMonth": [1,2,3,4,5], "workDurationInMinutes": 0 }
    ]
  }
  ```
* **Actual Server Response Received:**
  ```http
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
* **Database Verification (MongoDB `ERP.Attendance.WorkTemplates`):**
  Document `99a56911-0d30-40e6-8fa4-ca64da88930c` was persisted with `TotalWorkDurationInMinutes: 1500` and `isDefault: true`.
* **Impact:** 
  A day has only 24 hours (1440 minutes). Accepting 25 hours per day corrupts attendance calculation and causes payroll overtime errors.
* **Required Code Patch (`CreateFlexiWorkTemplateCommandValidator.cs`):**
  ```csharp
  RuleFor(x => x.TotalWorkDurationInMinutes)
      .InclusiveBetween(1, 1440)
      .When(x => x.FlexibleType == FlexibleType.Daily)
      .WithMessage("Daily flexible work duration cannot exceed 1440 minutes (24 hours).");
  ```

---

#### Defect `DEFECT-20261028-02`: FluentValidation `ValidationException` Throws HTTP 500 Instead of HTTP 400 Bad Request
* **Severity:** **P1 (Critical)**
* **Endpoints:** `POST/PATCH /api/companies/{companyId}/worktemplates/{fixed|split}`
* **Test Cases:** `USER-70`, `USER-59`, `USER-60`, `USER-61`, `USER-90`, `DOC-D-05`
* **Exact Request Payload Sent (Empty PATCH Body — `DOC-D-05`):**
  ```http
  PATCH /api/companies/3a247435-3cea-83ae-6a9f-6dda99f386a3/worktemplates/flexi/99a56911-0d30-40e6-8fa4-ca64da88930c HTTP/1.1
  Host: attendance2.dev.zoolwork.com
  Authorization: Bearer <JWT>
  __tenant: Attendance
  Content-Type: application/json

  {}
  ```
* **Actual Server Response Received:**
  ```http
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
* **Root Cause & Impact:**
  ASP.NET Core global exception middleware does not catch `FluentValidation.ValidationException`, bubbling it up as an unhandled 500 server crash.
* **Required Middleware Fix (`Program.cs` / `GlobalExceptionHandler.cs`):**
  ```csharp
  if (exception is FluentValidation.ValidationException valEx)
  {
      context.Response.StatusCode = StatusCodes.Status400BadRequest;
      context.Response.ContentType = "application/json";
      await context.Response.WriteAsJsonAsync(new
      {
          statusCode = StatusCodes.Status400BadRequest,
          error = "Cit.Attendance:ValidationException",
          message = "One or more validation errors occurred.",
          validationErrors = valEx.Errors.Select(e => new { field = e.PropertyName, message = e.ErrorMessage })
      });
      return;
  }
  ```

---

#### Defect `DEFECT-20261028-03`: Active Company Default Can Be Archived / Deleted Without Guard
* **Severity:** **P1 (Critical / Data Integrity)**
* **Endpoints:** `PATCH /api/companies/{companyId}/worktemplates/{id}/archive` & `delete`
* **Test Cases:** `DOC-F-01`, `DOC-F-02`
* **Raw Request Sent:**
  ```http
  PATCH /api/companies/3a247435-3cea-83ae-6a9f-6dda99f386a3/worktemplates/99a56911-0d30-40e6-8fa4-ca64da88930c/archive HTTP/1.1
  Host: attendance2.dev.zoolwork.com
  Authorization: Bearer <JWT>
  __tenant: Attendance
  ```
* **Actual Server Response Received:** `HTTP/1.1 200 OK`
* **Observed Database State:**
  Document `99a56911-0d30-40e6-8fa4-ca64da88930c` transitioned to `State: Archived`, `IsDeleted: true`, leaving the company with **no active default work schedule**. Subsequent edits threw `Cit.Attendance:1104 ("Invalid work template state transition")`.
* **Required Handler Guard (`ArchiveWorkTemplateCommandHandler.cs`):**
  ```csharp
  if (template.IsDefault && template.LocationId == Guid.Empty)
  {
      throw new BusinessException("Cit.Attendance:1202", "Active Company Default Work Template cannot be archived or deleted.");
  }
  ```

---

### Full Sheet Execution Results for `WT - Company Default` (150 Test Cases)

| Section Name | Total TCs | Passed | Failed | Pass Rate | Key Verification Notes |
|---|:---:|:---:|:---:|:---:|---|
| **A. Authentication, Tenant & Company Scoping** | 6 | 4 | 2 | 66.7% | No token / forged token return 401; cross-tenant header ignored in favor of JWT claim |
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

# 🔄 Part 4: Standardized Bug Lifecycle Procedure

Every bug logged in Attendance 2 follows this strict 6-stage lifecycle:

```mermaid
flowchart LR
    A["1. Detection & Reproduction<br>(Automated Suite Execution)"] --> B["2. Context & Payload Isolation<br>(Raw Request & Headers Captured)"]
    B --> C["3. Root Cause Analysis<br>(Contract vs Domain vs Middleware)"]
    C --> D["4. Severity & Priority Triage<br>(P0 Blocker to P3 Minor)"]
    D --> E["5. Remediation Patch<br>(C# Code & FluentValidation Fix)"]
    E --> F["6. Regression Verification<br>(Closed in Master Excel Suite)"]
```

1. **Stage 1: Detection & Automated Reproduction** — Triggered via automated test runner against DEV endpoints.
2. **Stage 2: Context & Payload Isolation** — Raw request JSON, route params, query params, headers, and latencies logged.
3. **Stage 3: Root Cause Layer Analysis** — Isolated to Controller/Binding, Validator, Handler, Middleware, or MongoDB.
4. **Stage 4: Severity & Priority Triage** — Classified as P0 (Blocker), P1 (Critical), P2 (Major), or P3 (Minor).
5. **Stage 5: Remediation Strategy & Code Patch** — Actionable C# code patch documented for engineering team.
6. **Stage 6: Regression Verification & Tracking** — Verified on subsequent builds and updated from `Fail` to `Pass` in Excel.

---

# ✅ Part 5: Actionable Developer Checklist (Date-Wise)

Share this actionable checklist with Khalid and the engineering team:

### 📅 Day 1: 26 October 2026 Checklist (Core Architecture & Sync)
- [ ] **P1 (`DEFECT-20261026-01`):** Publish integration event from `SP.AttendanceSvc` to `SP.CompanySvc` to set `CompaniesMaster.CompanyChecklist.WorkSchedulesCreated = true`.
- [ ] **P1 (`DEFECT-20261026-02`):** Remove hardcoded `"Placeholder Tenant"` in `CreateFixedWTCommandHandler` and resolve actual tenant name dynamically.
- [ ] **P2 (`DEFECT-20261026-04`):** Deprecate `tenantId`, `tenantName`, `companyId`, and `locationId` from `POST /worktemplates/fixed` body DTO; read strictly from Route, Query, and JWT token.
- [ ] **P3 (`DEFECT-20261026-03`):** Schedule architectural alignment on standardizing `CreatedBy` email into a composite `AuditIdentity` object across all microservices.

### 📅 Day 2: 27 October 2026 Checklist (DTO & Validation Pipeline)
- [ ] **P1 (`DEFECT-20261027-01`):** Add FluentValidation in `CreateWorkPlanCommandValidator` for missing `locationId` to prevent raw unhandled 500 `SimpleException`.
- [ ] **P2 (`DEFECT-20261027-02`):** Remove redundant `createdBy` email validation rule from `Create*PolicyCommandValidator`.
- [ ] **P2 (`DEFECT-20261027-03`):** Add `.GreaterThanOrEqualTo(0)` validation for `lateCheckInGraceMinutes` and early departure grace in Grace Policy DTO.
- [ ] **P2 (`DEFECT-20261027-04`):** Add `.GreaterThan(0)` validation for break durations in Break Policy DTO.
- [ ] **P0 (`DEFECT-20261027-05`):** Sanitize CDWT DTO binding to prevent location header binding from triggering `Cit.Attendance:1205` deadlock during initial company setup.
- [ ] **P0 (`DEFECT-20261027-06`):** Implement interval chronologic and non-overlapping validation in `SplitWorkTemplateCommandValidator`.
- [ ] **P0 (`DEFECT-20261027-07`):** Implement calendar invariant validator: `RuleFor(x => x).Must(x => x.TotalWorkingDays + x.TotalDaysOff == 7)`.

### 📅 Day 3: 28 October 2026 Checklist (Live Execution & Exception Middleware)
- [ ] **P0 (`DEFECT-20261028-01`):** Add `.InclusiveBetween(1, 1440)` rule in `CreateFlexiWorkTemplateCommandValidator` to reject daily work duration exceeding 24 hours.
- [ ] **P1 (`DEFECT-20261028-02`):** In global exception middleware (`GlobalExceptionHandlerMiddleware.cs`), catch `FluentValidation.ValidationException` and map it to `StatusCodes.Status400BadRequest` instead of returning HTTP 500.
- [ ] **P1 (`DEFECT-20261028-03`):** Add guard in `ArchiveWorkTemplateCommandHandler` and `DeleteWorkTemplateCommandHandler` rejecting archiving/deletion of active Company Default Work Template (`Cit.Attendance:1202`).
- [ ] **P2 (`DEFECT-20261028-04`):** Return HTTP 404 Not Found when querying `/api/companies/{companyId}/worktemplates` with a non-existent or zero GUID company.
"""

with open("Attendance2_Defects_Gaps_and_Architecture_Inconsistencies_Report.md", "w", encoding="utf-8") as f:
    f.write(content)

print("Successfully restructured Attendance2_Defects_Gaps_and_Architecture_Inconsistencies_Report.md into clean Date-Wise format!")

