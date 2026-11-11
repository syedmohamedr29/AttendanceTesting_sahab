import sys
import re

sys.stdout.reconfigure(encoding='utf-8')

defect_log_path = "Defects/Attendance2_Master_Defect_Log.md"
report_path = "Attendance2_Defects_Gaps_and_Architecture_Inconsistencies_Report.md"

tbl_rows = """| [`DEFECT-20261106-06`](#defect-20261106-06) | 🟠 P1 | Attendance Policy / Business Logic & DTO Validation | Break Policy Invariant & FluentValidation Gaps in PATCH: Arbitrary BreakType Enum (999), Blank Break Name (""), and Duplicate Break Items Accepted with HTTP 200 OK and Stored into MongoDB Corrupting Shift Duration Metrics | ``PATCH /attpolicies/break/{policyId}`` | [Evidence 46](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_46_break_policy_500_crash_null_break_and_duplicate_breaks_compass.png) |
| [`DEFECT-20261106-05`](#defect-20261106-05) | 🟠 P1 | Attendance Policy / Unhandled Exception & System Crash | Break Policy PATCH with Null Break Item ([null]) Triggers Unhandled HTTP 500 NullReferenceException Crashing Service Worker Instead of Returning HTTP 400 Validation Error | ``PATCH /attpolicies/break/{policyId}`` | [Evidence 46](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_46_break_policy_500_crash_null_break_and_duplicate_breaks_compass.png) |
"""

detail_section_05 = """
---

### <a id="defect-20261106-05"></a>🔴 DEFECT-20261106-05: Break Policy PATCH with Null Break Item (`[null]`) Triggers Unhandled HTTP 500 NullReferenceException Crashing Service Worker Instead of Returning HTTP 400 Validation Error

| Field | Detail |
| :--- | :--- |
| **Defect ID** | `DEFECT-20261106-05` |
| **Severity** | 🟠 **P1 Critical** (Unhandled Server Crash, Null Dereference & Microservice Denial-of-Service Risk) |
| **API Endpoints** | `PATCH /api/companies/{companyId}/attpolicies/break/{policyId}` |
| **Target Microservice** | `SP.AttendanceSvc` (.NET 9) |
| **Target Companies Verified** | Attendance 7 (`3a249870-c8ae-b3dc-1b8d-c44efad14f89`) |
| **Tested Policy ID** | `46675ad6-978d-4c02-b676-73193e48c32b` |
| **Visual Evidence** | [Evidence 46 (Break Policy Live Server Crash & MongoDB Proof)](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_46_break_policy_500_crash_null_break_and_duplicate_breaks_compass.png) |
| **Status** | **OPEN / CONFIRMED ON DEV ENVIRONMENT** |

#### Defect Description & Live Reproduction
During comprehensive live manual API testing on Attendance 7, a PATCH request was submitted with a `breaks` array containing a `null` item (`"breaks": [null]`). Instead of intercepting this invalid payload with a standard HTTP 400 Bad Request (`Cit.Attendance:Validation`), the microservice suffered an unhandled runtime crash and returned **HTTP 500 Internal Server Error**.

```http
PATCH /api/companies/3a249870-c8ae-b3dc-1b8d-c44efad14f89/attpolicies/break/46675ad6-978d-4c02-b676-73193e48c32b HTTP/1.1
Host: attendance2.dev.zoolwork.com
Authorization: Bearer <JWT_TOKEN>
Content-Type: application/json

{
  "type": "Break",
  "name": {
    "en": "Null Break Item Update",
    "ar": "تحديث عنصر استراحة فارغ"
  },
  "isActive": true,
  "tenantName": {
    "en": "Attendance",
    "ar": "Attendance"
  },
  "breaks": [null]
}
```

#### Actual Server Response (Live HTTP 500 Internal Server Error)
```json
{
  "error": {
    "code": "NullReferenceException",
    "message": "Object reference not set to an instance of an object.",
    "details": null,
    "data": null,
    "validationErrors": null
  }
}
```

#### Root Cause Analysis
In `SP.AttendanceSvc`, the `UpdateBreakPolicyDtoValidator` lacks an element-level null check for the `Breaks` collection. When ASP.NET Core deserializes `[null]`, it places a null reference inside `List<BreakItemDto> Breaks`. The application service or domain entity subsequently iterates over the collection (e.g., `Breaks.Sum(b => b.DurationMinutes)` or mapping code) and attempts to access properties on a `null` object reference without a null check, resulting in an unhandled `System.NullReferenceException`.

#### Production & Architecture Impact
1. **Denial-of-Service / Worker Instability:** Unhandled 500 exceptions pollute application logs, bypass API error reporting contracts, and can degrade worker process stability in high-throughput production clusters.
2. **Contract Breach:** Violates standard REST API contracts where malformed or invalid client inputs must return HTTP 400 with structured validation messages.

#### Remediation Code (.NET 9 FluentValidation)
```csharp
public class UpdateBreakPolicyDtoValidator : AbstractValidator<UpdateBreakPolicyDto>
{
    public UpdateBreakPolicyDtoValidator()
    {
        RuleFor(x => x.Breaks)
            .NotNull().WithMessage("Breaks collection cannot be null.")
            .NotEmpty().WithMessage("At least one break item is required.");

        RuleForEach(x => x.Breaks)
            .NotNull().WithMessage("Break entry cannot be null.")
            .SetValidator(new BreakItemDtoValidator());
    }
}
```
"""

detail_section_06 = """
---

### <a id="defect-20261106-06"></a>🔴 DEFECT-20261106-06: Break Policy Invariant & FluentValidation Gaps in PATCH: Arbitrary BreakType Enum (999), Blank Break Name (""), and Duplicate Break Items Accepted with HTTP 200 OK and Stored into MongoDB Corrupting Shift Duration Metrics

| Field | Detail |
| :--- | :--- |
| **Defect ID** | `DEFECT-20261106-06` |
| **Severity** | 🟠 **P1 Critical** (Domain Invariant Breach, Incomplete Validation & Attendance Metrics Corruption) |
| **API Endpoints** | `PATCH /api/companies/{companyId}/attpolicies/break/{policyId}` |
| **Target Microservice** | `SP.AttendanceSvc` (.NET 9) |
| **Target Companies Verified** | Attendance 7 (`3a249870-c8ae-b3dc-1b8d-c44efad14f89`) |
| **Tested Policy ID** | `46675ad6-978d-4c02-b676-73193e48c32b` |
| **Visual Evidence** | [Evidence 46 (Break Policy Live Server Crash & MongoDB Proof)](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_46_break_policy_500_crash_null_break_and_duplicate_breaks_compass.png) |
| **Status** | **OPEN / CONFIRMED ON DEV ENVIRONMENT** |

#### Defect Description & Live Reproduction
Comprehensive live verification of `PATCH /attpolicies/break/{policyId}` on Attendance 7 revealed that the PATCH endpoint bypasses critical domain invariants and input validation rules, accepting corrupted data with **HTTP 200 OK** and persisting it directly into MongoDB `ERP.Attendance.Policies`:

1. **Arbitrary BreakType Enum Accepted (`type: 999`):**
   - Submitting `breaks: [{"name": "Tea", "type": 999, "durationMinutes": 15}]` returns **HTTP 200 OK**.
   - The service fails to validate against the confirmed `BreakType` enum (`0 = NotApplicable`, `1 = Paid`, `2 = Unpaid`).
2. **Blank Break Item Name Accepted (`name: ""`):**
   - Submitting `breaks: [{"name": "", "type": 1, "durationMinutes": 15}]` returns **HTTP 200 OK**.
   - An unnamed break item is saved into the database, breaking UI display and reporting tables.
3. **Duplicate Break Entries Accepted in PATCH (`TotalBreakDurationInMinutes` Doubled):**
   - Submitting two identical break items:
     ```json
     {
       "type": "Break",
       "name": {"en": "Duplicate Break Update", "ar": "تحديث استراحات مكررة"},
       "isActive": true,
       "tenantName": {"en": "Attendance", "ar": "Attendance"},
       "breaks": [
         {"name": "Tea Break", "type": 1, "durationMinutes": 15},
         {"name": "Tea Break", "type": 1, "durationMinutes": 15}
       ]
     }
     ```
   - Server returned **HTTP 200 OK** and stored both identical entries in MongoDB!

#### MongoDB Compass Persistence Proof (Live DEV Database: 10.1.0.4:27018)
Query: `db['ERP.Attendance.Policies'].findOne({"_id": UUID("46675ad6-978d-4c02-b676-73193e48c32b")})`

```json
{
  "_id": "46675ad6-978d-4c02-b676-73193e48c32b",
  "_t": ["PolicyBase", "BreakPolicy"],
  "TenantId": "3a24741e-2667-1223-f12e-62a69fab3838",
  "CompanyId": "3a249870-c8ae-b3dc-1b8d-c44efad14f89",
  "CompanyName": {"en": "Attendance 7", "ar": "الحضور 7"},
  "Name": {"en": "Duplicate Break Update", "ar": "تحديث استراحات مكررة"},
  "IsActive": true,
  "Type": 1,
  "TotalBreakDurationInMinutes": 30,
  "TotalPaidBreakDurationInMinutes": 30,
  "TotalUnpaidBreakDurationInMinutes": 0,
  "Breaks": [
    {
      "Name": "Tea Break",
      "Type": 1,
      "DurationMinutes": 15
    },
    {
      "Name": "Tea Break",
      "Type": 1,
      "DurationMinutes": 15
    }
  ]
}
```

#### Production & Domain Impact
1. **Corrupted Shift Working Hours:** Because `TotalBreakDurationInMinutes` is automatically summed from `Breaks` (now 30 minutes instead of 15), every employee assigned this policy will have 15 additional minutes deducted from their work hours daily. Over a month of 22 work days, this produces a **5.5 hour discrepancy per employee**, triggering false short-time penalties or unfair payroll deductions!
2. **Invalid Enum Deserialization:** The value `999` causes unknown enum behaviors in downstream calculation engines and client frontends.

#### Remediation Code (.NET 9 FluentValidation)
```csharp
public class BreakItemDtoValidator : AbstractValidator<BreakItemDto>
{
    public BreakItemDtoValidator()
    {
        RuleFor(x => x.Name)
            .NotEmpty().WithMessage("Break name is required.")
            .MaximumLength(100).WithMessage("Break name cannot exceed 100 characters.");

        RuleFor(x => x.Type)
            .IsInEnum().WithMessage("Invalid break type.")
            .Must(t => t == BreakType.Paid || t == BreakType.Unpaid)
            .WithMessage("Break type must be either Paid (1) or Unpaid (2).");

        RuleFor(x => x.DurationMinutes)
            .GreaterThan(0).WithMessage("Break duration must be greater than 0 minutes.")
            .LessThanOrEqualTo(1440).WithMessage("Break duration cannot exceed 1440 minutes.");
    }
}

// In UpdateBreakPolicyDtoValidator:
RuleFor(x => x.Breaks)
    .Must(breaks => breaks == null || breaks.Select(b => b.Name?.Trim().ToLowerInvariant()).Distinct().Count() == breaks.Count)
    .WithMessage("Duplicate break names are not allowed within the same policy.");
```
"""

checklist_items = """- [ ] **P1 (`DEFECT-20261106-05`):** In `SP.AttendanceSvc`, implement `RuleForEach(x => x.Breaks).NotNull()` in `UpdateBreakPolicyDtoValidator` and `CreateBreakPolicyDtoValidator` to prevent unhandled `NullReferenceException` (HTTP 500) when a client submits `[null]` in the `breaks` array.
- [ ] **P1 (`DEFECT-20261106-06`):** In `SP.AttendanceSvc`, implement strict child DTO validation on `BreakItemDto`: enforce `.NotEmpty()` on break name, enforce `IsInEnum()` for `BreakType` (restricting to Paid=1, Unpaid=2), and enforce uniqueness of break names to prevent duplicate break items from doubling total break durations and corrupting work time deductions.
"""

# ==============================================================================
# 1. UPDATE Defects/Attendance2_Master_Defect_Log.md
# ==============================================================================
with open(defect_log_path, "r", encoding="utf-8") as f:
    log_text = f.read()

# Update metrics
log_text = re.sub(r'Total Defects:\s*\*\*\d+\*\*', 'Total Defects: **65**', log_text)
log_text = re.sub(r'P1 Critical:\s*\*\*\d+\*\*', 'P1 Critical: **52**', log_text)
log_text = log_text.replace("All 63 Defects", "All 65 Defects")

# Insert table rows before DEFECT-20261106-04
target_tbl = "| [`DEFECT-20261106-04`](#defect-20261106-04)"
if target_tbl in log_text and "DEFECT-20261106-05" not in log_text:
    log_text = log_text.replace(target_tbl, tbl_rows + target_tbl)

# Insert detail sections before DEFECT-20261106-04
target_detail = '### <a id="defect-20261106-04"></a>'
if target_detail in log_text and "DEFECT-20261106-05" not in log_text:
    log_text = log_text.replace(target_detail, detail_section_05 + detail_section_06 + target_detail)

# Insert checklist items
target_chk = "- [ ] **P1 (`DEFECT-20261106-04`):**"
if target_chk in log_text and "DEFECT-20261106-05" not in log_text:
    log_text = log_text.replace(target_chk, checklist_items + target_chk)

with open(defect_log_path, "w", encoding="utf-8") as f:
    f.write(log_text)
print(f"Updated {defect_log_path}")

# ==============================================================================
# 2. UPDATE Attendance2_Defects_Gaps_and_Architecture_Inconsistencies_Report.md
# ==============================================================================
with open(report_path, "r", encoding="utf-8") as f:
    rep_text = f.read()

rep_text = re.sub(r'Total Defects:\s*\*\*\d+\*\*', 'Total Defects: **65**', rep_text)
rep_text = re.sub(r'P1 Critical:\s*\*\*\d+\*\*', 'P1 Critical: **52**', rep_text)
rep_text = rep_text.replace("Total Defects Logged: 63", "Total Defects Logged: 65")
rep_text = rep_text.replace("Total Defects Logged: 59", "Total Defects Logged: 65")
rep_text = rep_text.replace("All 63 Defects", "All 65 Defects")

# Insert table rows
if target_tbl in rep_text and "DEFECT-20261106-05" not in rep_text:
    rep_text = rep_text.replace(target_tbl, tbl_rows + target_tbl)

# Insert detail sections
if target_detail in rep_text and "DEFECT-20261106-05" not in rep_text:
    rep_text = rep_text.replace(target_detail, detail_section_05 + detail_section_06 + target_detail)

# Insert checklist items
if target_chk in rep_text and "DEFECT-20261106-05" not in rep_text:
    rep_text = rep_text.replace(target_chk, checklist_items + target_chk)

with open(report_path, "w", encoding="utf-8") as f:
    f.write(rep_text)
print(f"Updated {report_path}")

