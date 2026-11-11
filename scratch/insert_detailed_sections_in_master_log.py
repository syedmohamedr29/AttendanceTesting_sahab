import sys

sys.stdout.reconfigure(encoding='utf-8')

defect_log_path = "Defects/Attendance2_Master_Defect_Log.md"

with open(defect_log_path, "r", encoding="utf-8") as f:
    text = f.read()

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
During live manual API testing on Attendance 7, a PATCH request was submitted with a `breaks` array containing a `null` item (`"breaks": [null]`). Instead of returning HTTP 400 Bad Request (`Cit.Attendance:Validation`), the microservice suffered an unhandled runtime crash and returned **HTTP 500 Internal Server Error**.

```http
PATCH /api/companies/3a249870-c8ae-b3dc-1b8d-c44efad14f89/attpolicies/break/46675ad6-978d-4c02-b676-73193e48c32b HTTP/1.1
Host: attendance2.dev.zoolwork.com
Authorization: Bearer <JWT_TOKEN>
Content-Type: application/json

{
  "type": "Break",
  "name": {"en": "Null Break Item Update", "ar": "تحديث عنصر استراحة فارغ"},
  "isActive": true,
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
In `SP.AttendanceSvc`, `UpdateBreakPolicyDtoValidator` lacks `RuleForEach(x => x.Breaks).NotNull()`. When deserializing `[null]`, ASP.NET Core places a null reference inside `List<BreakItemDto> Breaks`. Iterating over the collection without a null check throws `System.NullReferenceException`.

#### Remediation Code (.NET 9 FluentValidation)
```csharp
RuleForEach(x => x.Breaks)
    .NotNull().WithMessage("Break entry cannot be null.")
    .SetValidator(new BreakItemDtoValidator());
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
`PATCH /attpolicies/break/{policyId}` bypasses critical domain invariants and input validation rules, accepting corrupted data with **HTTP 200 OK** and persisting it into MongoDB `ERP.Attendance.Policies`:
1. `type: 999` accepted with HTTP 200 OK (Missing `IsInEnum()` on `BreakType`).
2. `name: ""` blank string accepted with HTTP 200 OK (Missing `NotEmpty()`).
3. **Duplicate Break Entries Accepted in PATCH:** Submitting two identical `"Tea Break"` items was accepted with HTTP 200 OK, doubling `TotalBreakDurationInMinutes` from 15 to 30.

#### MongoDB Compass Persistence Proof (Live DEV Database: 10.1.0.4:27018)
Query: `db['ERP.Attendance.Policies'].findOne({"_id": UUID("46675ad6-978d-4c02-b676-73193e48c32b")})`

```json
{
  "_id": "46675ad6-978d-4c02-b676-73193e48c32b",
  "_t": ["PolicyBase", "BreakPolicy"],
  "CompanyId": "3a249870-c8ae-b3dc-1b8d-c44efad14f89",
  "CompanyName": {"en": "Attendance 7", "ar": "الحضور 7"},
  "Name": {"en": "Duplicate Break Update", "ar": "تحديث استراحات مكررة"},
  "TotalBreakDurationInMinutes": 30,
  "TotalPaidBreakDurationInMinutes": 30,
  "Breaks": [
    { "Name": "Tea Break", "Type": 1, "DurationMinutes": 15 },
    { "Name": "Tea Break", "Type": 1, "DurationMinutes": 15 }
  ]
}
```

#### Remediation Code (.NET 9 FluentValidation)
```csharp
RuleFor(x => x.Breaks)
    .Must(breaks => breaks == null || breaks.Select(b => b.Name?.Trim().ToLowerInvariant()).Distinct().Count() == breaks.Count)
    .WithMessage("Duplicate break names are not allowed within the same policy.");
```
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
`PATCH /attpolicies/graceperiod/{policyId}` completely omits equivalent validation rules enforced in POST, allowing clients to modify any existing policy to contain corrupted enums, invalid thresholds, and incorrect types:
1. `deviationPeriod: 999` and `0` accepted with HTTP 200 OK (`GracePeriodDeviationPeriod` allows only 1=Weekly, 2=BiWeekly, 3=Monthly).
2. `deductLeaveFrom: 999` and `0` accepted with HTTP 200 OK (`GracePeriodLeaveDeductionType` allows only 1=AnnualLeave, 2=CasualLeave, 3=SickLeave).
3. `deviationThreshold: 0` accepted with HTTP 200 OK.
4. `type: "InvalidGrace"` accepted with HTTP 200 OK.

#### MongoDB Compass Persistence Proof (Live DEV Database: 10.1.0.4:27018)
Query: `db['ERP.Attendance.Policies'].findOne({"_id": UUID("d9c1e312-bba0-4a93-ab9d-e8845aa13180")})`

```json
{
  "_id": "d9c1e312-bba0-4a93-ab9d-e8845aa13180",
  "_t": ["PolicyBase", "GracePeriodPolicy"],
  "CompanyId": "3a249870-c8ae-b3dc-1b8d-c44efad14f89",
  "CompanyName": {"en": "Attendance 7", "ar": "الحضور 7"},
  "Name": {"en": "Corrupted Enums Grace Policy"},
  "DeviationThreshold": 0,
  "DeviationPeriod": 999,
  "DeductLeaveFrom": 999,
  "DeductionDays": 10.0
}
```

#### Remediation Code (.NET 9 FluentValidation)
```csharp
RuleFor(x => x.DeviationThreshold).GreaterThan(0).WithMessage("Deviation threshold must be greater than 0.");
RuleFor(x => x.DeviationPeriod).IsInEnum().Must(p => (int)p >= 1 && (int)p <= 3).WithMessage("Deviation period must be Weekly (1), BiWeekly (2), or Monthly (3).");
RuleFor(x => x.DeductLeaveFrom).IsInEnum().Must(d => (int)d >= 1 && (int)d <= 3).WithMessage("Deduct leave from must be AnnualLeave (1), CasualLeave (2), or SickLeave (3).");
```
"""

target_detail = '### <a id="defect-20261106-04"></a>'
if "### <a id=\"defect-20261106-07\"></a>" not in text:
    combined_new = detail_section_07 + detail_section_06 + detail_section_05 + "\n\n"
    text = text.replace(target_detail, combined_new + target_detail)

with open(defect_log_path, "w", encoding="utf-8") as f:
    f.write(text)

print(f"Inserted detail sections into {defect_log_path}!")
