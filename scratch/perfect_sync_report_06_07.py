import sys
import re

sys.stdout.reconfigure(encoding='utf-8')

report_path = "Attendance2_Defects_Gaps_and_Architecture_Inconsistencies_Report.md"

with open(report_path, "r", encoding="utf-8") as f:
    text = f.read()

# Fix table rows in top table
clean_rows = """| **`DEFECT-20261106-05`** | **🟠 P1 (Unhandled Crash)** | **Break Policy Module**<br>(ASP.NET Core Null Dereference) | `PATCH /attpolicies/break/{policyId}` | `{"breaks": [null]}` triggers unhandled HTTP 500 `NullReferenceException` crashing worker instead of returning 400 validation error. | ❌ **FAIL ([Evidence 46](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_46_break_policy_500_crash_null_break_and_duplicate_breaks_compass.png))** |
| **`DEFECT-20261106-06`** | **🟠 P1 (Domain Invariant)** | **Break Policy Module**<br>(FluentValidation Gaps) | `ERP.Attendance.Policies`<br>(`PATCH /attpolicies/break/{policyId}`) | PATCH accepts arbitrary break type (999), blank break name (""), and duplicate break entries with HTTP 200 OK, doubling break duration and corrupting work hours. | ❌ **FAIL ([Evidence 46](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_46_break_policy_500_crash_null_break_and_duplicate_breaks_compass.png))** |
| **`DEFECT-20261106-07`** | **🟠 P1 (Domain Invariant)** | **Grace Period Policy Module**<br>(FluentValidation Gaps) | `ERP.Attendance.Policies`<br>(`PATCH /attpolicies/graceperiod/{policyId}`) | PATCH accepts arbitrary deviationPeriod (999), invalid deductLeaveFrom (999/0), zero threshold (0), and invalid policy type with HTTP 200 OK, corrupting attendance deviation metrics. | ❌ **FAIL ([Evidence 47](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_47_grace_period_patch_invalid_enums_and_threshold_accepted_compass.png))** |
"""

# Replace any existing 05, 06, 07 block in top table
pattern = r'\| \*\*`DEFECT-20261106-05`\*\*.*?(?=\| \*\*`DEFECT-20261106-04`\*\*)'
text = re.sub(pattern, clean_rows, text, flags=re.DOTALL)

# Ensure detailed section for 07 exists
detail_07 = """

#### Defect `DEFECT-20261106-07`: Grace Period Policy Missing Enum, Threshold & Type Validations in PATCH — Arbitrary DeviationPeriod (999), Invalid DeductionSource (999 / 0), Zero Threshold (0), and Invalid PolicyType Accepted with HTTP 200 OK and Persisted into MongoDB

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

if "#### Defect `DEFECT-20261106-07`" not in text:
    target_det = "#### Defect `DEFECT-20261106-06`:"
    text = text.replace(target_det, detail_07.strip() + "\n\n" + target_det)

with open(report_path, "w", encoding="utf-8") as f:
    f.write(text)

print(f"Perfected {report_path}")
