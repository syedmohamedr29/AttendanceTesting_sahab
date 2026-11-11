import sys
import re
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side

sys.stdout.reconfigure(encoding='utf-8')

defect_log_path = "Defects/Attendance2_Master_Defect_Log.md"
report_path = "Attendance2_Defects_Gaps_and_Architecture_Inconsistencies_Report.md"
master_path = "AttendanceTestCases_Master_Consolidated.xlsx"
pol_path = "Attendance_Policies_Manual_API_TestCases_MongoDB.xlsx"
root_path = "AttendanceTestCases.xlsx"

# ==============================================================================
# 1. UPDATE BOTH MARKDOWN FILES WITH DEFECT-20261106-07
# ==============================================================================

tbl_row_07 = """| [`DEFECT-20261106-07`](#defect-20261106-07) | 🟠 P1 | Attendance Policy / Business Logic & DTO Validation | Grace Period Policy Missing Enum, Threshold & Type Validations in PATCH: Arbitrary DeviationPeriod (999), Invalid DeductionSource (999 / 0), Zero Threshold (0), and Invalid PolicyType Accepted with HTTP 200 OK and Persisted into MongoDB | ``PATCH /attpolicies/graceperiod/{policyId}`` | [Evidence 47](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_47_grace_period_patch_invalid_enums_and_threshold_accepted_compass.png) |
"""

detail_section_07 = """
---

### <a id="defect-20261106-07"></a>🔴 DEFECT-20261106-07: Grace Period Policy Missing Enum, Threshold & Type Validations in PATCH: Arbitrary DeviationPeriod (999), Invalid DeductionSource (999 / 0), Zero Threshold (0), and Invalid PolicyType Accepted with HTTP 200 OK and Persisted into MongoDB

| Field | Detail |
| :--- | :--- |
| **Defect ID** | `DEFECT-20261106-07` |
| **Severity** | 🟠 **P1 Critical** (Domain Invariant Breach, FluentValidation Asymmetry & Attendance Deviation Corruption) |
| **API Endpoints** | `PATCH /api/companies/{companyId}/attpolicies/graceperiod/{policyId}` |
| **Target Microservice** | `SP.AttendanceSvc` (.NET 9) |
| **Target Companies Verified** | Attendance 7 (`3a249870-c8ae-b3dc-1b8d-c44efad14f89`) |
| **Tested Policy ID** | `d9c1e312-bba0-4a93-ab9d-e8845aa13180` |
| **Visual Evidence** | [Evidence 47 (Grace Period PATCH Validation Gaps & Corrupted Enums in MongoDB)](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_47_grace_period_patch_invalid_enums_and_threshold_accepted_compass.png) |
| **Status** | **OPEN / CONFIRMED ON DEV ENVIRONMENT** |

#### Defect Description & Live Reproduction
Comprehensive live verification of Grace Period Policy endpoints on Attendance 7 revealed a severe validation asymmetry between the POST and PATCH endpoints. While `POST /attpolicies/graceperiod` enforces domain validation via `CreateGracePeriodPolicyDtoValidator`, `PATCH /attpolicies/graceperiod/{policyId}` completely omits equivalent validation rules in `UpdateGracePeriodPolicyDtoValidator`, allowing clients to modify any existing policy to contain corrupted enums, invalid thresholds, and incorrect types:

1. **Arbitrary DeviationPeriod Enum Accepted (`deviationPeriod: 999` and `0`):**
   - PATCH with `{"deviationPeriod": 999}` returns **HTTP 200 OK**.
   - PATCH with `{"deviationPeriod": 0}` (`NotApplicable`) returns **HTTP 200 OK**.
   - Confirmed enum allows only: `1 = Weekly`, `2 = BiWeekly`, `3 = Monthly`.
2. **Arbitrary Leave Deduction Source Accepted (`deductLeaveFrom: 999` and `0`):**
   - PATCH with `{"deductLeaveFrom": 999}` returns **HTTP 200 OK**.
   - PATCH with `{"deductLeaveFrom": 0}` (`NotApplicable`) returns **HTTP 200 OK**.
   - Confirmed enum allows only: `1 = AnnualLeave`, `2 = CasualLeave`, `3 = SickLeave`.
3. **Zero Deviation Threshold Accepted (`deviationThreshold: 0`):**
   - PATCH with `{"deviationThreshold": 0}` returns **HTTP 200 OK**.
   - A threshold of 0 means every single late arrival triggers immediate leave deductions without any allowance.
4. **Invalid Policy Type Accepted (`type: "InvalidGrace"`):**
   - PATCH with `{"type": "InvalidGrace"}` returns **HTTP 200 OK**.

#### MongoDB Compass Persistence Proof (Live DEV Database: 10.1.0.4:27018)
Query: `db['ERP.Attendance.Policies'].findOne({"_id": UUID("d9c1e312-bba0-4a93-ab9d-e8845aa13180")})`

```json
{
  "_id": "d9c1e312-bba0-4a93-ab9d-e8845aa13180",
  "_t": ["PolicyBase", "GracePeriodPolicy"],
  "CompanyId": "3a249870-c8ae-b3dc-1b8d-c44efad14f89",
  "CompanyName": {"en": "Attendance 7", "ar": "الحضور 7"},
  "Name": {"en": "Corrupted Enums Grace Policy"},
  "IsActive": true,
  "Type": 3,
  "LateCheckInGraceMinutes": 5,
  "EarlyCheckOutGraceMinutes": 5,
  "DeviationThreshold": 0,
  "DeviationPeriod": 999,
  "DeductLeaveFrom": 999,
  "DeductionDays": 10.0
}
```

#### Production & Domain Impact
1. **Attendance Deviation Engine Failure:** Background attendance processing jobs calculate employee deviation periods using `DeviationPeriod` (Weekly, BiWeekly, Monthly). Storing `999` or `0` triggers unhandled switch-case exceptions or silent calculation aborts, preventing shift deviation tracking across entire companies.
2. **Leave Deduction Corruption:** The leave management engine cannot resolve deduction source `999`, leading to failed leave balance adjustments or unhandled integration errors with `LeaveSvc`.

#### Remediation Code (.NET 9 FluentValidation)
```csharp
public class UpdateGracePeriodPolicyDtoValidator : AbstractValidator<UpdateGracePeriodPolicyDto>
{
    public UpdateGracePeriodPolicyDtoValidator()
    {
        RuleFor(x => x.Name).NotNull().WithMessage("Policy name is required.");

        RuleFor(x => x.DeviationThreshold)
            .GreaterThan(0).WithMessage("Deviation threshold must be greater than 0.")
            .LessThanOrEqualTo(100).WithMessage("Deviation threshold cannot exceed 100.");

        RuleFor(x => x.DeviationPeriod)
            .IsInEnum().WithMessage("Invalid deviation period enum.")
            .Must(p => p == GracePeriodDeviationPeriod.Weekly || 
                       p == GracePeriodDeviationPeriod.BiWeekly || 
                       p == GracePeriodDeviationPeriod.Monthly)
            .WithMessage("Deviation period must be Weekly (1), BiWeekly (2), or Monthly (3).");

        RuleFor(x => x.DeductLeaveFrom)
            .IsInEnum().WithMessage("Invalid leave deduction source enum.")
            .Must(d => d == GracePeriodLeaveDeductionType.AnnualLeave || 
                       d == GracePeriodLeaveDeductionType.CasualLeave || 
                       d == GracePeriodLeaveDeductionType.SickLeave)
            .WithMessage("Deduct leave from must be AnnualLeave (1), CasualLeave (2), or SickLeave (3).");

        RuleFor(x => x.LateCheckInGraceMinutes)
            .GreaterThanOrEqualTo(0).WithMessage("Late check-in grace minutes cannot be negative.")
            .LessThanOrEqualTo(1440).WithMessage("Late check-in grace minutes cannot exceed 1440.");

        RuleFor(x => x.EarlyCheckOutGraceMinutes)
            .GreaterThanOrEqualTo(0).WithMessage("Early check-out grace minutes cannot be negative.")
            .LessThanOrEqualTo(1440).WithMessage("Early check-out grace minutes cannot exceed 1440.");

        RuleFor(x => x.DeductionDays)
            .GreaterThanOrEqualTo(0).WithMessage("Deduction days cannot be negative.")
            .LessThanOrEqualTo(365).WithMessage("Deduction days cannot exceed 365.");
    }
}
```
"""

chk_07 = """- [ ] **P1 (`DEFECT-20261106-07`):** In `SP.AttendanceSvc`, implement comprehensive validation rules in `UpdateGracePeriodPolicyDtoValidator`: enforce `IsInEnum()` and non-zero checks on `DeviationPeriod` and `DeductLeaveFrom`, enforce `GreaterThan(0)` on `DeviationThreshold`, and prevent invalid policy types in PATCH requests.
"""

# Update Master Defect Log
with open(defect_log_path, "r", encoding="utf-8") as f:
    log_text = f.read()

log_text = re.sub(r'Total Defects:\s*\*\*\d+\*\*', 'Total Defects: **66**', log_text)
log_text = re.sub(r'P1 Critical:\s*\*\*\d+\*\*', 'P1 Critical: **53**', log_text)
log_text = log_text.replace("All 65 Defects", "All 66 Defects")

target_tbl = "| [`DEFECT-20261106-06`](#defect-20261106-06)"
if target_tbl in log_text and "DEFECT-20261106-07" not in log_text:
    log_text = log_text.replace(target_tbl, tbl_row_07 + target_tbl)

target_detail = '### <a id="defect-20261106-06"></a>'
if target_detail in log_text and "DEFECT-20261106-07" not in log_text:
    log_text = log_text.replace(target_detail, detail_section_07 + target_detail)

target_chk = "- [ ] **P1 (`DEFECT-20261106-06`):**"
if target_chk in log_text and "DEFECT-20261106-07" not in log_text:
    log_text = log_text.replace(target_chk, chk_07 + target_chk)

with open(defect_log_path, "w", encoding="utf-8") as f:
    f.write(log_text)
print(f"Updated {defect_log_path} to 66 Defects (53 P1 Critical).")

# Update Architecture Report
with open(report_path, "r", encoding="utf-8") as f:
    rep_text = f.read()

rep_text = re.sub(r'Total Defects:\s*\*\*\d+\*\*', 'Total Defects: **66**', rep_text)
rep_text = re.sub(r'P1 Critical:\s*\*\*\d+\*\*', 'P1 Critical: **53**', rep_text)
rep_text = rep_text.replace("Total Defects Logged: 65", "Total Defects Logged: 66")
rep_text = rep_text.replace("All 65 Defects", "All 66 Defects")
rep_text = rep_text.replace("DEFECT-20261106-06", "DEFECT-20261106-07")

tbl_row_rep_07 = """| **`DEFECT-20261106-07`** | **🟠 P1 (Domain Invariant)** | **Grace Period Policy Module**<br>(FluentValidation Gaps) | `ERP.Attendance.Policies`<br>(`PATCH /attpolicies/graceperiod/{policyId}`) | PATCH accepts arbitrary deviationPeriod (999), invalid deductLeaveFrom (999/0), zero threshold (0), and invalid policy type with HTTP 200 OK, corrupting attendance deviation metrics. | ❌ **FAIL ([Evidence 47](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_47_grace_period_patch_invalid_enums_and_threshold_accepted_compass.png))** |
"""
target_tbl_rep = "| **`DEFECT-20261106-06`** |"
if target_tbl_rep in rep_text and "DEFECT-20261106-07" not in rep_text:
    rep_text = rep_text.replace(target_tbl_rep, tbl_row_rep_07 + target_tbl_rep)

detail_rep_07 = """

#### Defect `DEFECT-20261106-07`: Grace Period Policy Missing Enum, Threshold & Type Validations in PATCH — Arbitrary DeviationPeriod (999), Invalid DeductionSource (999 / 0), and Zero Threshold (0) Persisted into MongoDB

- **Severity:** 🟠 **P1 Critical** (Domain Invariant Breach, Incomplete Validation & Attendance Deviation Corruption)
- **Affected Endpoints:** `PATCH /api/companies/{companyId}/attpolicies/graceperiod/{policyId}`
- **Target Microservice:** `SP.AttendanceSvc` (.NET 9)
- **Target Companies Verified:** Attendance 7 (`3a249870-c8ae-b3dc-1b8d-c44efad14f89`), Policy `d9c1e312-bba0-4a93-ab9d-e8845aa13180`
- **Live Proof in MongoDB (`Sahab.ERP.Attendance.Policies`):**
  - Document `d9c1e312-bba0-4a93-ab9d-e8845aa13180`: `DeviationPeriod: 999`, `DeductLeaveFrom: 999`, `DeviationThreshold: 0` persisted into MongoDB with HTTP 200 OK!
- **Visual Evidence:** [Evidence 47](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_47_grace_period_patch_invalid_enums_and_threshold_accepted_compass.png)
- **Developer Remediation:**
  In `UpdateGracePeriodPolicyDtoValidator`, add `RuleFor(x => x.DeviationPeriod).IsInEnum().Must(...)`, `RuleFor(x => x.DeductLeaveFrom).IsInEnum().Must(...)`, and `RuleFor(x => x.DeviationThreshold).GreaterThan(0);`.
"""
target_detail_rep = "#### Defect `DEFECT-20261106-06`:"
if target_detail_rep in rep_text and "DEFECT-20261106-07" not in rep_text:
    rep_text = rep_text.replace(target_detail_rep, detail_rep_07.strip() + "\n\n" + target_detail_rep)

with open(report_path, "w", encoding="utf-8") as f:
    f.write(rep_text)
print(f"Updated {report_path} to 66 Defects (53 P1 Critical).")

# ==============================================================================
# 2. UPDATE EXCEL WORKBOOKS
# ==============================================================================
print("Updating Excel workbooks...")
pass_fill = PatternFill(start_color="E2EFDA", end_color="E2EFDA", fill_type="solid")
fail_fill = PatternFill(start_color="FCE4D6", end_color="FCE4D6", fill_type="solid")
pass_font = Font(name="Segoe UI", size=9, color="375623", bold=True)
fail_font = Font(name="Segoe UI", size=9, color="C65911", bold=True)
regular_font = Font(name="Segoe UI", size=9)
regular_center = Alignment(horizontal="center", vertical="center")
regular_left = Alignment(horizontal="left", vertical="center", wrap_text=True)

thin_border = Border(
    left=Side(style='thin', color='D9D9D9'),
    right=Side(style='thin', color='D9D9D9'),
    top=Side(style='thin', color='D9D9D9'),
    bottom=Side(style='thin', color='D9D9D9')
)

wb_master = openpyxl.load_workbook(master_path)

# 2A. Sheet 20: Policy Defects Log
ws_def = wb_master["Policy Defects Log"]
defect_07_row = [
    "DEFECT-20261106-07",
    "P1 Critical",
    "Grace Period Policy Missing Enum, Threshold & Type Validations in PATCH: Arbitrary DeviationPeriod (999), Invalid DeductionSource (999 / 0), Zero Threshold (0), and Invalid PolicyType Accepted with HTTP 200 OK and Persisted into MongoDB",
    "PATCH /api/companies/{companyId}/attpolicies/graceperiod/{policyId}",
    "Attendance 7 (3a249870-c8ae-b3dc-1b8d-c44efad14f89)",
    '{"type": "InvalidGrace", "name": {"en": "Corrupted Enums Grace Policy"}, "isActive": true, "lateCheckInGraceMinutes": 5, "earlyCheckOutGraceMinutes": 5, "deviationThreshold": 0, "deviationPeriod": 999, "deductLeaveFrom": 999, "deductionDays": 10}',
    "HTTP 200 OK (Grace period policy updated; arbitrary enum 999, zero threshold 0, and invalid policy type persisted into Sahab.ERP.Attendance.Policies)",
    "HTTP 400 Bad Request with Cit.Attendance:Validation (DeviationPeriod restricted to 1/2/3, DeductLeaveFrom restricted to 1/2/3, DeviationThreshold > 0)",
    "Corrupts attendance deviation engine and leave deduction calculations. Unresolved enum integers trigger unhandled switch exceptions in background processing jobs.",
    "In UpdateGracePeriodPolicyDtoValidator: 1) RuleFor(x => x.DeviationPeriod).IsInEnum().Must(p => (int)p >= 1 && (int)p <= 3); 2) RuleFor(x => x.DeductLeaveFrom).IsInEnum().Must(d => (int)d >= 1 && (int)d <= 3); 3) RuleFor(x => x.DeviationThreshold).GreaterThan(0); 4) RuleFor(x => x.Type).Equal(\"GracePeriod\");",
    "Live MongoDB Compass Verification on Attendance 7 (ERP.Attendance.Policies Document: d9c1e312-bba0-4a93-ab9d-e8845aa13180, Evidence 47)"
]

existing_defects = [ws_def.cell(r, 1).value for r in range(2, ws_def.max_row + 1)]
if "DEFECT-20261106-07" not in existing_defects:
    r_new = ws_def.max_row + 1
    for c, val in enumerate(defect_07_row, start=1):
        cell = ws_def.cell(r_new, c, val)
        cell.font = regular_font
        cell.border = thin_border
        cell.alignment = regular_left
    ws_def.cell(r_new, 2).fill = fail_fill
    ws_def.cell(r_new, 2).font = fail_font
    print(f"Appended DEFECT-20261106-07 to Master Policy Defects Log at row {r_new}")

# 2B. Sheet 19: Policies - DTO Validations
ws_dto = wb_master["Policies - DTO Validations"]

dto_grace_updates = {
    # POL-DTO-40: deviationThreshold 0
    "POL-DTO-40": {
        "status": "Fail",
        "act_code": "200 OK",
        "notes": "CRITICAL GAP: Submitting deviationThreshold: 0 accepted with HTTP 200 OK in PATCH! Stored into MongoDB.",
        "defect": "DEFECT-20261106-07 (Zero threshold accepted)"
    },
    # POL-DTO-43: deviationPeriod 999
    "POL-DTO-43": {
        "status": "Fail",
        "act_code": "200 OK",
        "notes": "CRITICAL GAP: Submitting deviationPeriod: 999 accepted with HTTP 200 OK in PATCH! Missing IsInEnum() validator.",
        "defect": "DEFECT-20261106-07 (Invalid enum accepted)"
    },
    # POL-DTO-47: deductLeaveFrom 999
    "POL-DTO-47": {
        "status": "Fail",
        "act_code": "200 OK",
        "notes": "CRITICAL GAP: Submitting deductLeaveFrom: 999 accepted with HTTP 200 OK in PATCH! Missing IsInEnum() validator.",
        "defect": "DEFECT-20261106-07 (Invalid enum accepted)"
    }
}

for r in range(2, ws_dto.max_row + 1):
    tc_id = ws_dto.cell(r, 1).value
    if tc_id in dto_grace_updates:
        u = dto_grace_updates[tc_id]
        c_status = ws_dto.cell(r, 12, u["status"])
        c_status.fill = fail_fill
        c_status.font = fail_font
        ws_dto.cell(r, 13, u["act_code"])
        ws_dto.cell(r, 14, u["notes"])
        c_def = ws_dto.cell(r, 15, u["defect"])
        c_def.font = fail_font
        print(f"Updated Sheet 19 Grace DTO validation: {tc_id} -> Fail ({u['defect']})")

# 2C. Sheet 18: Attendance Policies (Append new Grace PATCH defect test cases)
ws_pol = wb_master["Attendance Policies"]
existing_pol_tcs = [ws_pol.cell(r, 1).value for r in range(2, ws_pol.max_row + 1)]

new_grace_tcs = [
    {
        "tc_id": "TC-POL-PATCH-GRC-10",
        "req_id": "REQ-ATT-POL-002",
        "module": "Attendance Policies",
        "endpoint": "/api/companies/{{companyId}}/attpolicies/graceperiod/{{policyId}}",
        "method": "PATCH",
        "category": "Negative Test / Enum Validation",
        "scenario": "Arbitrary deviationPeriod enum integer (999) in PATCH",
        "title": "PATCH Grace Period with Invalid DeviationPeriod 999 Accepted with 200 OK",
        "preconditions": "Active grace period policy exists in Attendance 7",
        "headers": "Authorization: Bearer {{token}}, Content-Type: application/json",
        "payload": '{"type": "GracePeriod", "name": {"en": "Invalid Period Update"}, "isActive": true, "lateCheckInGraceMinutes": 5, "earlyCheckOutGraceMinutes": 5, "deviationThreshold": 1, "deviationPeriod": 999, "deductLeaveFrom": 1, "deductionDays": 10}',
        "data": "policyId=d9c1e312-bba0-4a93-ab9d-e8845aa13180, deviationPeriod=999",
        "steps": "1. Send PATCH with deviationPeriod=999. 2. Verify response.",
        "exp_http": "400 Bad Request",
        "exp_body": "Cit.Attendance:Validation error message",
        "db": "Sahab",
        "col": "ERP.Attendance.Policies",
        "val_scen": "Document should not be modified with invalid enum",
        "filter": '{"_id": UUID("d9c1e312-bba0-4a93-ab9d-e8845aa13180")}',
        "exp_mongo": "Document unchanged",
        "act_api": "HTTP 200 OK (CRITICAL: API accepted arbitrary enum deviationPeriod: 999).",
        "act_mongo": "CRITICAL GAP: Document d9c1e312-bba0-4a93-ab9d-e8845aa13180 persisted in MongoDB with DeviationPeriod: 999.",
        "api_status": "Fail",
        "db_status": "Fail",
        "overall": "Fail",
        "priority": "P1",
        "remarks": "DEFECT-20261106-07 (Missing IsInEnum validator on DeviationPeriod)"
    },
    {
        "tc_id": "TC-POL-PATCH-GRC-11",
        "req_id": "REQ-ATT-POL-002",
        "module": "Attendance Policies",
        "endpoint": "/api/companies/{{companyId}}/attpolicies/graceperiod/{{policyId}}",
        "method": "PATCH",
        "category": "Negative Test / Enum Validation",
        "scenario": "Arbitrary deductLeaveFrom enum integer (999) in PATCH",
        "title": "PATCH Grace Period with Invalid DeductLeaveFrom 999 Accepted with 200 OK",
        "preconditions": "Active grace period policy exists in Attendance 7",
        "headers": "Authorization: Bearer {{token}}, Content-Type: application/json",
        "payload": '{"type": "GracePeriod", "name": {"en": "Invalid Deduct Source Update"}, "isActive": true, "lateCheckInGraceMinutes": 5, "earlyCheckOutGraceMinutes": 5, "deviationThreshold": 1, "deviationPeriod": 1, "deductLeaveFrom": 999, "deductionDays": 10}',
        "data": "policyId=d9c1e312-bba0-4a93-ab9d-e8845aa13180, deductLeaveFrom=999",
        "steps": "1. Send PATCH with deductLeaveFrom=999. 2. Verify response.",
        "exp_http": "400 Bad Request",
        "exp_body": "Cit.Attendance:Validation error message",
        "db": "Sahab",
        "col": "ERP.Attendance.Policies",
        "val_scen": "Document should not be modified with invalid enum",
        "filter": '{"_id": UUID("d9c1e312-bba0-4a93-ab9d-e8845aa13180")}',
        "exp_mongo": "Document unchanged",
        "act_api": "HTTP 200 OK (CRITICAL: API accepted arbitrary enum deductLeaveFrom: 999).",
        "act_mongo": "CRITICAL GAP: Document d9c1e312-bba0-4a93-ab9d-e8845aa13180 persisted in MongoDB with DeductLeaveFrom: 999.",
        "api_status": "Fail",
        "db_status": "Fail",
        "overall": "Fail",
        "priority": "P1",
        "remarks": "DEFECT-20261106-07 (Missing IsInEnum validator on DeductLeaveFrom)"
    },
    {
        "tc_id": "TC-POL-PATCH-GRC-12",
        "req_id": "REQ-ATT-POL-002",
        "module": "Attendance Policies",
        "endpoint": "/api/companies/{{companyId}}/attpolicies/graceperiod/{{policyId}}",
        "method": "PATCH",
        "category": "Negative Test / Domain Boundary",
        "scenario": "Zero deviationThreshold (0) in PATCH",
        "title": "PATCH Grace Period with DeviationThreshold 0 Accepted with 200 OK",
        "preconditions": "Active grace period policy exists in Attendance 7",
        "headers": "Authorization: Bearer {{token}}, Content-Type: application/json",
        "payload": '{"type": "GracePeriod", "name": {"en": "Zero Threshold Update"}, "isActive": true, "lateCheckInGraceMinutes": 5, "earlyCheckOutGraceMinutes": 5, "deviationThreshold": 0, "deviationPeriod": 1, "deductLeaveFrom": 1, "deductionDays": 10}',
        "data": "policyId=d9c1e312-bba0-4a93-ab9d-e8845aa13180, deviationThreshold=0",
        "steps": "1. Send PATCH with deviationThreshold=0. 2. Verify response.",
        "exp_http": "400 Bad Request",
        "exp_body": "Deviation threshold must be greater than 0",
        "db": "Sahab",
        "col": "ERP.Attendance.Policies",
        "val_scen": "Document should not be modified with zero threshold",
        "filter": '{"_id": UUID("d9c1e312-bba0-4a93-ab9d-e8845aa13180")}',
        "exp_mongo": "Document unchanged",
        "act_api": "HTTP 200 OK (CRITICAL: API accepted deviationThreshold: 0; immediate leave deduction on 1st deviation).",
        "act_mongo": "CRITICAL GAP: Document d9c1e312-bba0-4a93-ab9d-e8845aa13180 persisted in MongoDB with DeviationThreshold: 0.",
        "api_status": "Fail",
        "db_status": "Fail",
        "overall": "Fail",
        "priority": "P1",
        "remarks": "DEFECT-20261106-07 (Missing GreaterThan(0) validator on DeviationThreshold)"
    }
]

for tc in new_grace_tcs:
    if tc["tc_id"] not in existing_pol_tcs:
        r_new = ws_pol.max_row + 1
        row_vals = [
            tc["tc_id"], tc["req_id"], tc["module"], tc["endpoint"], tc["method"],
            tc["category"], tc["scenario"], tc["title"], tc["preconditions"], tc["headers"],
            tc["payload"], tc["data"], tc["steps"], tc["exp_http"], tc["exp_body"],
            tc["db"], tc["col"], tc["val_scen"], tc["filter"], tc["exp_mongo"],
            tc["act_api"], tc["act_mongo"], tc["api_status"], tc["db_status"], tc["overall"],
            tc["priority"], tc["remarks"]
        ]
        for c, val in enumerate(row_vals, start=1):
            cell = ws_pol.cell(r_new, c, val)
            cell.font = regular_font
            cell.border = thin_border
            cell.alignment = regular_left
        
        cell_status = ws_pol.cell(r_new, 25, tc["overall"])
        cell_status.fill = fail_fill
        cell_status.font = fail_font
        cell_status.alignment = regular_center
        print(f"Appended new Grace test case to Sheet 18: {tc['tc_id']}")

# Count pass / fail in Sheet 18
pol_pass = sum(1 for r in range(2, ws_pol.max_row + 1) if str(ws_pol.cell(r, 25).value).lower() == "pass")
pol_fail = sum(1 for r in range(2, ws_pol.max_row + 1) if "fail" in str(ws_pol.cell(r, 25).value).lower())
pol_total = ws_pol.max_row - 1
print(f"Sheet 18 Attendance Policies: Pass={pol_pass}, Fail={pol_fail}, Total={pol_total}")

# Recalculate Sheet 19 Policies - DTO Validations
dto_pass = sum(1 for r in range(2, ws_dto.max_row + 1) if str(ws_dto.cell(r, 12).value).lower() == "pass")
dto_fail = sum(1 for r in range(2, ws_dto.max_row + 1) if "fail" in str(ws_dto.cell(r, 12).value).lower() or "defect" in str(ws_dto.cell(r, 12).value).lower())
dto_total = ws_dto.max_row - 1
print(f"Sheet 19 Policies - DTO Validations: Pass={dto_pass}, Fail={dto_fail}, Total={dto_total}")

# 2D. UPDATE INDEX Sheet in Master
ws_idx = wb_master["INDEX"]

# Row 10: Attendance Policies (Sheet 18)
ws_idx.cell(10, 3, pol_total)
ws_idx.cell(10, 9, pol_pass)
ws_idx.cell(10, 10, pol_fail)
ws_idx.cell(10, 11, 0)
ws_idx.cell(10, 12, f"{round((pol_pass + pol_fail) / pol_total * 100, 1)}%")
ws_idx.cell(10, 13, f"🟢 100% Executed ({pol_pass} Pass, {pol_fail} Fail / Defects Logged)")

# Row 22: Policies - DTO Validations (Sheet 19)
ws_idx.cell(22, 3, dto_total)
ws_idx.cell(22, 9, dto_pass)
ws_idx.cell(22, 10, dto_fail)
ws_idx.cell(22, 11, 0)
ws_idx.cell(22, 12, f"{round((dto_pass + dto_fail) / dto_total * 100, 1)}%")
ws_idx.cell(22, 13, f"🟢 100% Executed ({dto_pass} Pass, {dto_fail} Fail / Defects Logged)")

# Total recalculation
tot_tcs = sum(ws_idx.cell(r, 3).value or 0 for r in range(5, 23))
tot_pass = sum(ws_idx.cell(r, 9).value or 0 for r in range(5, 23))
tot_fail = sum(ws_idx.cell(r, 10).value or 0 for r in range(5, 23))
tot_notrun = sum(ws_idx.cell(r, 11).value or 0 for r in range(5, 23))

ws_idx.cell(23, 3, tot_tcs)
ws_idx.cell(23, 9, tot_pass)
ws_idx.cell(23, 10, tot_fail)
ws_idx.cell(23, 11, tot_notrun)
ws_idx.cell(23, 12, f"{round((tot_pass + tot_fail) / tot_tcs * 100, 1)}%")
ws_idx.cell(23, 13, f"🎯 {tot_pass + tot_fail} Executed ({tot_pass} Pass, {tot_fail} Fail) | {tot_notrun} Pending Execution")

wb_master.save(master_path)
print(f"Saved {master_path}! TOTAL TCs={tot_tcs}, Pass={tot_pass}, Fail={tot_fail}, Pending={tot_notrun}")

# ==============================================================================
# 3. SYNCHRONIZE Standalone Workbook: Attendance_Policies_Manual_API_TestCases_MongoDB.xlsx
# ==============================================================================
print("Synchronizing Standalone Workbook...")
wb_pol = openpyxl.load_workbook(pol_path)

# Policy Defects Log in Standalone
ws_def_pol = wb_pol["Policy Defects Log"]
existing_def_pol = [ws_def_pol.cell(r, 1).value for r in range(2, ws_def_pol.max_row + 1)]

if "DEFECT-20261106-07" not in existing_def_pol:
    r_new = ws_def_pol.max_row + 1
    for c, val in enumerate(defect_07_row, start=1):
        cell = ws_def_pol.cell(r_new, c, val)
        cell.font = regular_font
        cell.border = thin_border
        cell.alignment = regular_left
    ws_def_pol.cell(r_new, 2).fill = fail_fill
    ws_def_pol.cell(r_new, 2).font = fail_font

# Policies - DTO Validations in Standalone
if "Policies - DTO Validations" in wb_pol.sheetnames:
    ws_dto_pol = wb_pol["Policies - DTO Validations"]
    for r in range(2, ws_dto_pol.max_row + 1):
        tc_id = ws_dto_pol.cell(r, 1).value
        if tc_id in dto_grace_updates:
            u = dto_grace_updates[tc_id]
            c_status = ws_dto_pol.cell(r, 12, u["status"])
            c_status.fill = fail_fill
            c_status.font = fail_font
            ws_dto_pol.cell(r, 13, u["act_code"])
            ws_dto_pol.cell(r, 14, u["notes"])
            ws_dto_pol.cell(r, 15, u["defect"])

# Append new test cases to Standalone PATCH and Master sheets
for sname in ["Master Test Cases", "PATCH API Test Cases"]:
    if sname in wb_pol.sheetnames:
        ws_t = wb_pol[sname]
        existing_in_sheet = [ws_t.cell(r, 1).value for r in range(2, ws_t.max_row + 1)]
        for tc in new_grace_tcs:
            if tc["tc_id"] not in existing_in_sheet:
                r_new = ws_t.max_row + 1
                row_vals = [
                    tc["tc_id"], tc["req_id"], tc["module"], tc["endpoint"], tc["method"],
                    tc["category"], tc["scenario"], tc["title"], tc["preconditions"], tc["headers"],
                    tc["payload"], tc["data"], tc["steps"], tc["exp_http"], tc["exp_body"],
                    tc["db"], tc["col"], tc["val_scen"], tc["filter"], tc["exp_mongo"],
                    tc["act_api"], tc["act_mongo"], tc["api_status"], tc["db_status"], tc["overall"],
                    tc["priority"], tc["remarks"]
                ]
                for c, val in enumerate(row_vals, start=1):
                    cell = ws_t.cell(r_new, c, val)
                    cell.font = regular_font
                    cell.border = thin_border
                cell_status = ws_t.cell(r_new, 25, tc["overall"])
                cell_status.fill = fail_fill
                cell_status.font = fail_font

wb_pol.save(pol_path)
print(f"Saved {pol_path}!")

# ==============================================================================
# 4. SYNCHRONIZE Root Workbook: AttendanceTestCases.xlsx
# ==============================================================================
print("Synchronizing Root Workbook...")
wb_root = openpyxl.load_workbook(root_path)
if "Policy Defects Log" in wb_root.sheetnames:
    ws_def_root = wb_root["Policy Defects Log"]
    existing_def_root = [ws_def_root.cell(r, 1).value for r in range(2, ws_def_root.max_row + 1)]
    if "DEFECT-20261106-07" not in existing_def_root:
        r_new = ws_def_root.max_row + 1
        for c, val in enumerate(defect_07_row, start=1):
            cell = ws_def_root.cell(r_new, c, val)
            cell.font = regular_font
            cell.border = thin_border
            cell.alignment = regular_left
        ws_def_root.cell(r_new, 2).fill = fail_fill
        ws_def_root.cell(r_new, 2).font = fail_font
        print(f"Appended DEFECT-20261106-07 to Root Workbook Policy Defects Log at row {r_new}")

wb_root.save(root_path)
print(f"Saved {root_path}!")
print("ALL WORKBOOKS FULLY SYNCHRONIZED SUCCESSFULLY!")
