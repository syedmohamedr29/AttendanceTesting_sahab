import sys
import re

sys.stdout.reconfigure(encoding='utf-8')

report_path = "Attendance2_Defects_Gaps_and_Architecture_Inconsistencies_Report.md"

with open(report_path, "r", encoding="utf-8") as f:
    text = f.read()

# 1. Update top heading
text = text.replace(
    "## 🚨 Defects Logged on 05 & 06 November 2026: DEFECT-20261105-01 to DEFECT-20261106-04",
    "## 🚨 Defects Logged on 05 & 06 November 2026: DEFECT-20261105-01 to DEFECT-20261106-06"
)

# 2. Update table row in top table
tbl_rows_rep = """| **`DEFECT-20261106-05`** | **🟠 P1 (Unhandled Crash)** | **Break Policy Module**<br>(ASP.NET Core Null Dereference) | `PATCH /attpolicies/break/{policyId}` | `{"breaks": [null]}` triggers unhandled HTTP 500 `NullReferenceException` crashing worker instead of returning 400 validation error. | ❌ **FAIL ([Evidence 46](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_46_break_policy_500_crash_null_break_and_duplicate_breaks_compass.png))** |
| **`DEFECT-20261106-06`** | **🟠 P1 (Domain Invariant)** | **Break Policy Module**<br>(FluentValidation Gaps) | `ERP.Attendance.Policies`<br>(`PATCH /attpolicies/break/{policyId}`) | PATCH accepts arbitrary break type (999), blank break name (""), and duplicate break entries with HTTP 200 OK, doubling break duration and corrupting work hours. | ❌ **FAIL ([Evidence 46](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_46_break_policy_500_crash_null_break_and_duplicate_breaks_compass.png))** |
"""

target_tbl_rep = "| **`DEFECT-20261106-04`** |"
if target_tbl_rep in text and "DEFECT-20261106-05" not in text:
    text = text.replace(target_tbl_rep, tbl_rows_rep + target_tbl_rep)

# 3. Add detail sections after DEFECT-20261106-04 detail
detail_sections_rep = """

#### Defect `DEFECT-20261106-05`: Break Policy PATCH with Null Break Item (`[null]`) Triggers Unhandled HTTP 500 NullReferenceException Crashing Service Worker

- **Severity:** 🟠 **P1 Critical** (Unhandled Server Crash, Denial-of-Service Risk & Contract Breach)
- **Affected Endpoints:** `PATCH /api/companies/{companyId}/attpolicies/break/{policyId}`
- **Target Microservice:** `SP.AttendanceSvc` (.NET 9)
- **Target Companies Verified:** Attendance 7 (`3a249870-c8ae-b3dc-1b8d-c44efad14f89`), Policy `46675ad6-978d-4c02-b676-73193e48c32b`
- **Live Server Response (HTTP 500 Internal Server Error):**
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
- **Visual Evidence:** [Evidence 46](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_46_break_policy_500_crash_null_break_and_duplicate_breaks_compass.png)
- **Developer Remediation:**
  In `UpdateBreakPolicyDtoValidator`, add `RuleForEach(x => x.Breaks).NotNull().WithMessage("Break entry cannot be null.");`.


#### Defect `DEFECT-20261106-06`: Break Policy Invariant & FluentValidation Gaps in PATCH — Arbitrary BreakType Enum (999), Blank Break Name (""), and Duplicate Break Items Accepted with HTTP 200 OK and Stored into MongoDB

- **Severity:** 🟠 **P1 Critical** (Domain Invariant Breach, Incomplete Validation & Attendance Metrics Corruption)
- **Affected Endpoints:** `PATCH /api/companies/{companyId}/attpolicies/break/{policyId}`
- **Target Microservice:** `SP.AttendanceSvc` (.NET 9)
- **Target Companies Verified:** Attendance 7 (`3a249870-c8ae-b3dc-1b8d-c44efad14f89`), Policy `46675ad6-978d-4c02-b676-73193e48c32b`
- **Live Proof in MongoDB (`Sahab.ERP.Attendance.Policies`):**
  - Document `46675ad6-978d-4c02-b676-73193e48c32b`: Duplicate `{"Name": "Tea Break", "Type": 1, "DurationMinutes": 15}` accepted twice with HTTP 200 OK, doubling `TotalBreakDurationInMinutes: 30`!
  - `type: 999` accepted with HTTP 200 OK (Missing `IsInEnum()`).
  - `name: ""` blank string accepted with HTTP 200 OK (Missing `NotEmpty()`).
- **Visual Evidence:** [Evidence 46](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_46_break_policy_500_crash_null_break_and_duplicate_breaks_compass.png)
- **Developer Remediation:**
  In `BreakItemDtoValidator`, enforce `RuleFor(x => x.Name).NotEmpty();` and `RuleFor(x => x.Type).IsInEnum().Must(t => t == BreakType.Paid || t == BreakType.Unpaid);`. In `UpdateBreakPolicyDtoValidator`, enforce distinct break names within the collection.
"""

target_detail_rep = "#### Defect `DEFECT-20261106-04`:"
if target_detail_rep in text and "DEFECT-20261106-05" not in text:
    text = text.replace(target_detail_rep, detail_sections_rep.strip() + "\n\n" + target_detail_rep)

# 4. Update metrics in File 1
text = re.sub(r'Total Defects:\s*\*\*\d+\*\*', 'Total Defects: **65**', text)
text = re.sub(r'P1 Critical:\s*\*\*\d+\*\*', 'P1 Critical: **52**', text)
text = text.replace("Total Defects: 63", "Total Defects: 65")
text = text.replace("Total Defects Logged: 63", "Total Defects Logged: 65")
text = text.replace("All 63 Defects", "All 65 Defects")

with open(report_path, "w", encoding="utf-8") as f:
    f.write(text)

print(f"Applied updates to {report_path}")
