import sys

sys.stdout.reconfigure(encoding='utf-8')

report_path = "Attendance2_Defects_Gaps_and_Architecture_Inconsistencies_Report.md"

with open(report_path, "r", encoding="utf-8") as f:
    text = f.read()

# Check top heading
text = text.replace(
    "## 🚨 Defects Logged on 05 & 06 November 2026: DEFECT-20261105-01 to DEFECT-20261106-04",
    "## 🚨 Defects Logged on 05 & 06 November 2026: DEFECT-20261105-01 to DEFECT-20261106-07"
)
text = text.replace(
    "## 🚨 Defects Logged on 05 & 06 November 2026: DEFECT-20261105-01 to DEFECT-20261106-06",
    "## 🚨 Defects Logged on 05 & 06 November 2026: DEFECT-20261105-01 to DEFECT-20261106-07"
)

# Re-insert DEFECT-20261106-06 table row if missing
row_06 = """| **`DEFECT-20261106-06`** | **🟠 P1 (Domain Invariant)** | **Break Policy Module**<br>(FluentValidation Gaps) | `ERP.Attendance.Policies`<br>(`PATCH /attpolicies/break/{policyId}`) | PATCH accepts arbitrary break type (999), blank break name (""), and duplicate break entries with HTTP 200 OK, doubling break duration and corrupting work hours. | ❌ **FAIL ([Evidence 46](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_46_break_policy_500_crash_null_break_and_duplicate_breaks_compass.png))** |
"""

if "DEFECT-20261106-06" not in text:
    target = "| **`DEFECT-20261106-05`** |"
    text = text.replace(target, row_06 + target)

# Re-insert DEFECT-20261106-06 detail section if missing
detail_06 = """

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

if "#### Defect `DEFECT-20261106-06`" not in text:
    target_detail = "#### Defect `DEFECT-20261106-05`:"
    text = text.replace(target_detail, detail_06.strip() + "\n\n" + target_detail)

with open(report_path, "w", encoding="utf-8") as f:
    f.write(text)

print(f"Fixed {report_path}")
