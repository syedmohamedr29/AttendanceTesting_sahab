import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('Attendance2_Defects_Gaps_and_Architecture_Inconsistencies_Report.md', 'r', encoding='utf-8') as f:
    text = f.read()

# 1. New Section 1
new_sec1 = """## 1. Summary of Gaps, Bugs & DTO Validation Issues

Below is the consolidated matrix categorized by discovery date:

### A. Core Architecture & Synchronization Defects (Identified: 26-Oct-2026)

| Defect ID | Priority | Module & API Affected | Observed Issue (Actual Behavior) | Expected Engineering Behavior |
|:---:|:---:|:---|:---|:---|
| **`USER-01`** | **P1 (Blocker)** | `POST /worktemplates/{fixed|flexi|split}`<br>*(Cross-Svc to `SP.CompanySvc`)* | After successfully creating the Company Default Work Schedule, `CompaniesMaster.CompanyChecklist.WorkSchedulesCreated` remains **`false`** in `DEV > CompanySvcNET8test`. | Attendance Service must emit an integration event or execute an internal callback to update `WorkSchedulesCreated = true` in Company Service. |
| **`USER-02`** | **P1 (Data)** | `POST /worktemplates/fixed`<br>`Sahab > ERP.Attendance.WorkTemplates` | `TenantName` is stored with a hardcoded mock dictionary:<br>`{"en": "Placeholder Tenant", "ar": "شركة افتراضية"}`. | Must dynamically resolve and persist the real tenant name (e.g. `{"en": "Attendance", ...}`) from Identity Server / Company Service. |
| **`USER-03`** | **P2 (Design)** | All Modules (`WorkTemplates`, `WorkPlans`, `Policies`) | `CreatedBy` only stores the caller's email string (`syed.mohamed@comm-it.in`). Lacks user GUID or unified audit object. | Standardize audit identity across all collections (either keep standard email or enrich with `{ userId, email, loginId }`). |
| **`USER-04`** | **P2 (Design)** | `POST /worktemplates/fixed` | Request body DTO expects `tenantId`, `tenantName`, `companyId`, `locationId`, conflicting with REST standards used in other modules. | Deprecate body scoping parameters. Derive `companyId` from Route, `locationId` from Query, and `tenantId` from JWT. |

---

### B. DTO Validation Soft Spots & Schema Gaps (Identified: 27-Oct-2026)

| DTO Issue ID | Priority | Module & API Affected | Observed DTO Issue (Actual Behavior) | Required FluentValidation Fix |
|:---:|:---:|:---|:---|:---|
| **`DTO-VAL-01`**<br>*(KI-1 Plans)* | **P1 (Crash)** | `POST /workplans` | Omitting `?locationId=` in Query/DTO causes unhandled 500 **`SimpleException`** instead of 400 Bad Request. | Add `RuleFor(x => x.LocationId).NotEmpty().WithMessage("LocationId is required.");` in `CreateWorkPlanCommandValidator`. |
| **`DTO-VAL-02`**<br>*(KI-1 Policies)* | **P2 (Contract)** | `POST /attpolicies/*` | Command validator strictly mandates `createdBy` email in body DTO, even though backend handler discards it and overwrites from JWT. | Remove `RuleFor(x => x.CreatedBy)` from `Create*PolicyCommandValidator` to eliminate redundant payload requirements. |
| **`DTO-VAL-03`**<br>*(DOC-C-07)* | **P2 (Boundary)** | `POST /attpolicies/grace-period` | Submitting negative grace minutes (e.g. `lateCheckInGraceMinutes: -5`) in DTO is accepted without validation error. | Add `RuleFor(x => x.LateCheckInGraceMinutes).GreaterThanOrEqualTo(0);` in command validator. |
| **`DTO-VAL-04`**<br>*(DOC-B-08)* | **P2 (Boundary)** | `POST /attpolicies/break` | Submitting negative break duration (e.g. `durationMinutes: -10`) in DTO is accepted without validation error. | Add `RuleFor(x => x.DurationMinutes).GreaterThan(0);` for all break items in command validator. |
| **`DTO-VAL-05`**<br>*(USER-51-53)* | **P0 (Deadlock)** | `POST /worktemplates/{fixed|flexi|split}` | In CDWT creation, passing `LocationId` in HTTP Header binds into DTO as Location Template, triggering `Cit.Attendance:1205` deadlock. | In CDWT handlers, explicitly ignore or reject `LocationId` in headers with clear 400 message. |
| **`DTO-VAL-06`**<br>*(USER-59-60)* | **P0 (Integrity)** | `POST/PATCH /worktemplates/split` | Split Shift DTO allows overlapping intervals (e.g. 08:00-13:00 & 12:00-17:00) or zero break gap (contiguous shift). | Add validator ensuring `Interval2.StartTime >= Interval1.EndTime + MinimumBreakGap`. |
| **`DTO-VAL-07`**<br>*(USER-69-70)* | **P0 (Integrity)** | `POST/PATCH /worktemplates/*` | DTO accepts invalid day sums (e.g. `totalWorkingDays: 5, totalDaysOff: 1`, sum = 6) or arrays with missing days. | Add cross-field validator enforcing `totalWorkingDays + totalDaysOff == 7` and exactly 7 items in time slots array. |

---
"""

# 2. New Section 6 Checklist
new_sec6 = """## 6. Actionable Developer Checklist

Share this checklist with Khalid and the engineering team:

### Core Architecture & Sync (26-Oct-2026):
- [ ] **P1 (Defect `USER-01`):** Publish integration event from `SP.AttendanceSvc` to `SP.CompanySvc` to set `CompaniesMaster.CompanyChecklist.WorkSchedulesCreated = true`.
- [ ] **P1 (Defect `USER-02`):** Remove hardcoded `"Placeholder Tenant"` in `CreateFixedWTCommandHandler` and resolve the actual tenant name dynamically.
- [ ] **P2 (Design `USER-04`):** Deprecate `tenantId`, `tenantName`, `companyId`, and `locationId` from `POST /worktemplates/fixed` body DTO; read them strictly from Route, Query, and JWT token.
- [ ] **P3 (Audit `USER-03`):** Schedule architectural alignment on whether to enrich string `CreatedBy` email into a composite `AuditIdentity` object across all microservices.

### DTO & Validation Pipeline (27-Oct-2026):
- [ ] **P1 (DTO `DTO-VAL-01` / `KI-1`):** Add FluentValidation in `CreateWorkPlanCommandValidator` for missing `locationId` to prevent raw unhandled 500 `SimpleException`.
- [ ] **P2 (DTO `DTO-VAL-02` / `KI-1`):** Remove redundant `createdBy` email validation rule from `Create*PolicyCommandValidator`.
- [ ] **P2 (DTO `DTO-VAL-03` / `DOC-C-07`):** Add `.GreaterThanOrEqualTo(0)` validation for `lateCheckInGraceMinutes` and early departure grace in Grace Policy DTO.
- [ ] **P2 (DTO `DTO-VAL-04` / `DOC-B-08`):** Add `.GreaterThan(0)` validation for break durations in Break Policy DTO.
- [ ] **P0 (DTO `DTO-VAL-05` / `USER-51`):** Sanitize CDWT DTO binding to prevent location header binding from triggering `Cit.Attendance:1205` deadlock during initial company setup.
- [ ] **P0 (DTO `DTO-VAL-06` / `USER-59`):** Implement interval chronologic and non-overlapping validation in `SplitWorkTemplateCommandValidator`.
- [ ] **P0 (DTO `DTO-VAL-07` / `USER-69`):** Implement calendar invariant validator: `RuleFor(x => x).Must(x => x.TotalWorkingDays + x.TotalDaysOff == 7)`.

---
"""

# 3. New Section 8: Dedicated DTO Validation Defect Log
new_sec8 = """
---

## 8. Dedicated DTO Validation & Command Pipeline Defect Log (Discovered 27-Oct-2026)

This section documents the specific DTO model and validation bugs identified during exploratory testing on **27-Oct-2026**, along with the required C# FluentValidation code implementations.

```mermaid
graph TD
    Request["Incoming API Request (JSON Body + Headers)"] --> Binder["ASP.NET Core Model Binder"]
    Binder --> DTO["Command DTO (MediatR)"]
    DTO --> FV["FluentValidation Pipeline"]
    
    FV -- "Missing locationId on WorkPlan" --> Bug1["BUG DTO-VAL-01: Unhandled 500 SimpleException"]
    FV -- "Negative Grace (-5m) / Break (-10m)" --> Bug2["BUG DTO-VAL-03/04: Negative Values Accepted into DB"]
    FV -- "Header Location on CDWT" --> Bug3["BUG DTO-VAL-05: 1205 Deadlock (Prerequisite Error)"]
    FV -- "Split Overlapping Intervals" --> Bug4["BUG DTO-VAL-06: Corrupt Shift Times in MongoDB"]
    FV -- "Sum of Days != 7" --> Bug5["BUG DTO-VAL-07: Incomplete Week Calendar Calculation"]
```

---

### 8.1 Detailed Code-Level Analysis & Required Developer Fixes

#### Issue `DTO-VAL-01`: Missing `locationId` in Work Plan DTO/Query causes HTTP 500 Crash
* **Module:** `SP.AttendanceSvc > WorkPlans` | **Severity:** P1 (Reliability)
* **Problem:** `CreateWorkPlanCommand` expects `LocationId`. When omitted by the caller, the command handler invokes a downstream repository method passing `Guid.Empty`, which throws an unhandled `SimpleException` resulting in a raw 500 response.
* **Developer Fix in `CreateWorkPlanCommandValidator.cs`:**
  ```csharp
  public class CreateWorkPlanCommandValidator : AbstractValidator<CreateWorkPlanCommand>
  {
      public CreateWorkPlanCommandValidator()
      {
          RuleFor(x => x.CompanyId)
              .NotEmpty()
              .WithMessage("CompanyId is required.");

          RuleFor(x => x.LocationId)
              .NotEmpty()
              .WithMessage("LocationId is required in query or command.");

          RuleFor(x => x.WorkPlanName)
              .NotNull()
              .WithMessage("WorkPlanName object is required.");
      }
  }
  ```

---

#### Issue `DTO-VAL-02`: Redundant `CreatedBy` Validation Rule in Policy DTO
* **Module:** `SP.AttendanceSvc > AttendancePolicies` | **Severity:** P2 (Contract Hygiene)
* **Problem:** `CreateGracePeriodPolicyCommandValidator` enforces `RuleFor(x => x.CreatedBy).NotEmpty()`. However, the handler does:
  ```csharp
  policy.CreatedBy = _currentUserService.Email ?? "system";
  ```
  The caller-provided value is completely ignored. Requiring it in the DTO forces frontend/API clients to send duplicate boilerplate audit data.
* **Developer Fix:** Remove `RuleFor(x => x.CreatedBy)` from all `Create*PolicyCommandValidator.cs` files.

---

#### Issue `DTO-VAL-03` & `DTO-VAL-04`: Negative Numeric Durations Accepted into DB
* **Module:** `SP.AttendanceSvc > Policies` | **Severity:** P2 (Data Integrity)
* **Problem:** DTOs accept negative integers for minutes:
  * `POST /attpolicies/grace-period`: accepts `lateCheckInGraceMinutes: -5`.
  * `POST /attpolicies/break`: accepts `durationMinutes: -10`.
* **Developer Fix:**
  ```csharp
  // In CreateGracePeriodPolicyCommandValidator.cs
  RuleFor(x => x.LateCheckInGraceMinutes)
      .GreaterThanOrEqualTo(0)
      .WithMessage("Late check-in grace minutes cannot be negative.");

  RuleFor(x => x.EarlyCheckOutGraceMinutes)
      .GreaterThanOrEqualTo(0)
      .WithMessage("Early check-out grace minutes cannot be negative.");

  // In CreateBreakPolicyCommandValidator.cs
  RuleForEach(x => x.Breaks)
      .ChildRules(b => {
          b.RuleFor(x => x.DurationMinutes)
              .GreaterThan(0)
              .WithMessage("Break duration must be greater than 0 minutes.");
      });
  ```

---

#### Issue `DTO-VAL-05`: Header Location Model Binding Trap during First-Time CDWT Setup
* **Module:** `SP.AttendanceSvc > WorkTemplates` | **Severity:** P0 (Setup Blocker)
* **Problem:** When `LocationId` is present in HTTP request headers, ASP.NET Core binds it to `CreateFixedWTCommand.LocationId`. The handler assumes this is a location-specific template and checks if CDWT exists. Since CDWT = 0, it aborts with `Cit.Attendance:1205`.
* **Developer Fix:** In `CreateFixedWTCommandHandler.cs`, `CreateFlexiWTCommandHandler.cs`, and `CreateSplitWTCommandHandler.cs`:
  ```csharp
  // When executing on the company-level route (no locationId query):
  if (!httpContext.Request.Query.ContainsKey("locationId"))
  {
      command.LocationId = Guid.Empty; // Force Company Default scope
  }
  ```

---

#### Issue `DTO-VAL-06`: Split Shift Overlapping Intervals & Zero Break Validation Gap
* **Module:** `SP.AttendanceSvc > WorkTemplates (Split)` | **Severity:** P0 (Data Integrity)
* **Problem:** The Split shift DTO accepts intervals that overlap or have zero gap.
* **Developer Fix in `CreateSplitWTCommandValidator.cs`:**
  ```csharp
  RuleForEach(x => x.SplitTimeSlots)
      .Where(s => s.IsWorkingDay)
      .Custom((slot, context) => {
          if (slot.TimeSlots.Count < 2)
          {
              context.AddFailure("Split shift working days must contain at least 2 time intervals.");
              return;
          }
          var slot1 = slot.TimeSlots[0];
          var slot2 = slot.TimeSlots[1];
          if (slot2.StartTime < slot1.EndTime)
          {
              context.AddFailure("Split intervals within the same working day cannot overlap.");
          }
          if (slot2.StartTime == slot1.EndTime)
          {
              context.AddFailure("Split shift requires a distinct break duration between intervals.");
          }
      });
  ```

---

#### Issue `DTO-VAL-07`: Calendar Invariant Enforcement (`totalWorkingDays + totalDaysOff == 7`)
* **Module:** `SP.AttendanceSvc > WorkTemplates` | **Severity:** P0 (Calendar Integrity)
* **Problem:** DTO accepts mismatched day counts (e.g. 5 working days + 1 day off = 6 total days).
* **Developer Fix in `Create*WTCommandValidator.cs`:**
  ```csharp
  RuleFor(x => x)
      .Must(x => (x.TotalWorkingDays + x.TotalDaysOff) == 7)
      .WithMessage("Total working days and total days off must sum to exactly 7 days.");

  RuleFor(x => x.FixedTimeSlots) // or FlexiTimeSlots / SplitTimeSlots
      .Must(slots => slots != null && slots.Count == 7)
      .WithMessage("All 7 days of the week must be defined in the schedule.");
  ```

---
"""

# Replace Section 1
sec1_start = text.find('## 1. Summary of Gaps & Bugs to Share with Developers')
sec2_start = text.find('## 2. API Design Inconsistency')
updated_text = text[:sec1_start] + new_sec1 + text[sec2_start:]

# Replace Section 6
sec6_start = updated_text.find('## 6. Actionable Developer Checklist')
sec7_start = updated_text.find('## 7. Dynamic Work Template Lifecycle')
updated_text = updated_text[:sec6_start] + new_sec6 + updated_text[sec7_start:]

# Append Section 8
updated_text += new_sec8

with open('Attendance2_Defects_Gaps_and_Architecture_Inconsistencies_Report.md', 'w', encoding='utf-8') as f:
    f.write(updated_text)

print("Successfully updated Defect Report with complete DTO issues log!")

