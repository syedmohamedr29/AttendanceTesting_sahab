import sys

sys.stdout.reconfigure(encoding='utf-8')

report_path = 'Attendance2_Defects_Gaps_and_Architecture_Inconsistencies_Report.md'
with open(report_path, 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Update Top Banner Alert
banner_old = "Defects Logged Today (05 November 2026): DEFECT-20261105-01 & DEFECT-20261105-02"
banner_new = "Defects Logged Today (05 November 2026): DEFECT-20261105-01, DEFECT-20261105-02, DEFECT-20261105-03 & DEFECT-20261105-04"
text = text.replace(banner_old, banner_new)

tbl_marker = "| **`DEFECT-20261105-02`** | **P2 (Architecture & DTO Flaw)**"
new_rows = (
    "| **`DEFECT-20261105-03`** | **P1 (Business Logic & Payroll Invariant)** | **Attendance Policies Module**<br>(Overtime) | `ERP.Attendance.Policies`<br>(`POST` & `PATCH` `/attpolicies/overtime`) | **Overtime Policy Allows Negative `rateFormula` Multiplier (`-1.5`) with HTTP 200 OK:** Missing domain validation corrupts employee overtime pay calculations. | [Evidence 41](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_41_overtime_policy_negative_rateformula_accepted_compass.png) |\n"
    "| **`DEFECT-20261105-04`** | **P1 (Master Data Integrity & Multi-Tenancy)** | **Attendance Policies Module**<br>(Data Integrity) | `ERP.Attendance.Policies`<br>(`POST` & `PATCH` `/attpolicies/*`) | **`TenantName` Persists as `Object (empty)` `{}` in MongoDB:** Empty tenant object persisted across Break, Grace Period, and Overtime Policies while CompanyName is populated. | [Evidence 42](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_42_policy_tenantname_empty_object_compass.png) |\n"
)

if tbl_marker in text and "DEFECT-20261105-03" not in text:
    idx = text.find(tbl_marker)
    line_end = text.find("\n", idx) + 1
    text = text[:line_end] + new_rows + text[line_end:]
    print("Added DEFECT-20261105-03 and 04 to Report Top Banner Table.")

# 2. Add Deep-Dive sections before Part 4
deep_dive_report = """---

### Defect `DEFECT-20261105-03`: Overtime Policy Allows Negative `rateFormula` Multiplier (`-1.5`) with HTTP 200 OK Resulting in Corrupted Payroll Calculations (Missing Math & Payroll Invariant Validation)
- **Severity:** 🟠 **P1 (Critical / Business Logic & Payroll Invariant)**
- **Affected Endpoint:** `POST /api/companies/{companyId}/attpolicies/overtime` & `PATCH ...`
- **Affected MongoDB Collection:** `DEV > Sahab > ERP.Attendance.Policies`
- **Tested Company:** Attendance 6 (`3a249870-184c-0373-f344-015d602678d7`)
- **Document ID in MongoDB:** `UUID("77213223-d4ef-4767-ad6c-ebb778c77056")`
- **Evidence Reference:** [Evidence 41 (`evidence_41_overtime_policy_negative_rateformula_accepted_compass.png`)](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_41_overtime_policy_negative_rateformula_accepted_compass.png)

#### Detailed Technical Analysis
During live manual API test execution on Company **Attendance 6**, submitting an Overtime Policy with a negative overtime multiplier (`rateFormula: -1.5`) was **accepted with HTTP 200 OK** and persisted into MongoDB collection `Sahab.ERP.Attendance.Policies`:

```json
// POST /api/companies/3a249870-184c-0373-f344-015d602678d7/attpolicies/overtime
{
  "name": {
    "en": "Negative Multiplier"
  },
  "rates": [
    {
      "dayRate": "WorkingDay",
      "rateFormula": -1.5
    }
  ]
}
```

The validator for `OvertimePolicyDto` validates buffer minutes (`BufferMinutes >= 0`), but completely lacks FluentValidation rules for the nested `rates[].rateFormula` property. Consequently:
- Negative multipliers (e.g., `-1.5`, `-2.0`) are persisted without validation.
- When payroll calculations or attendance log pipeline L3 overtime calculations run, multiplying overtime hours by `-1.5` will **deduct pay from the employee** instead of granting overtime pay!

#### Evidence
| Screenshot | Description |
| :--- | :--- |
| ![DEFECT-20261105-03](defect_evidence/evidence_41_overtime_policy_negative_rateformula_accepted_compass.png) | **Evidence 41:** MongoDB Compass live inspection of document `77213223-d4ef-4767-ad6c-ebb778c77056` on Company Attendance 6. Highlighted in red: RateFormula: -1.5 accepted with HTTP 200 OK. |

#### Developer Remediation Steps
In `SP.AttendanceSvc` validators, add:
```csharp
RuleForEach(x => x.Rates).ChildRules(rate => {
    rate.RuleFor(r => r.RateFormula)
        .GreaterThan(0.0)
        .WithMessage("Overtime rate multiplier must be greater than 0.");
});
```

---

### Defect `DEFECT-20261105-04`: `TenantName` Persists as `Object (empty)` `{}` in MongoDB Collection `ERP.Attendance.Policies` Across All Policy Types (Break, Grace Period, Overtime) During Creation and Updates
- **Severity:** 🟠 **P1 (Critical / Master Data Integrity & Multi-Tenancy)**
- **Affected Endpoints:** `POST` & `PATCH` `/api/companies/{companyId}/attpolicies/*`, `GET`
- **Affected MongoDB Collection:** `DEV > Sahab > ERP.Attendance.Policies`
- **Tested Company:** Attendance 6 (`3a249870-184c-0373-f344-015d602678d7`)
- **Evidence Reference:** [Evidence 42 (`evidence_42_policy_tenantname_empty_object_compass.png`)](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_42_policy_tenantname_empty_object_compass.png)

#### Detailed Technical Analysis
During live API verification on Company **Attendance 6**, creating Break, Grace Period, and Overtime policies resulted in `TenantName` persisting as an empty JSON object `{}`:

```json
"tenantId": "3a24741e-2667-1223-f12e-62a69fab3838",
"tenantName": {},
"companyId": "3a249870-184c-0373-f344-015d602678d7",
"companyName": {
  "en": "Attendance 6",
  "ar": "الحضور 6"
}
```

The domain entity constructors for `BreakPolicy`, `GracePeriodPolicy`, and `OvertimePolicy` instantiate `TenantName = new MultilingualString()` without populating `En` or `Ar` strings from `_currentTenant.Name` and `_currentTenant.ArabicName`.

#### Evidence
| Screenshot | Description |
| :--- | :--- |
| ![DEFECT-20261105-04](defect_evidence/evidence_42_policy_tenantname_empty_object_compass.png) | **Evidence 42:** MongoDB Compass live inspection of collection ERP.Attendance.Policies on Company Attendance 6. Highlighted in red: TenantName: Object (empty) {} while CompanyName is populated. |

#### Developer Remediation Steps
In all policy command handlers (`CreateBreakPolicyCommandHandler`, etc.):
```csharp
policy.TenantName = new MultilingualString
{
    En = !string.IsNullOrWhiteSpace(_currentTenant.Name) ? _currentTenant.Name : "Attendance",
    Ar = !string.IsNullOrWhiteSpace(_currentTenant.ArabicName) ? _currentTenant.ArabicName : "الحضور"
};
```
"""

next_part_marker = "## Part 4:"
if next_part_marker in text and "DEFECT-20261105-03" not in text:
    idx = text.find(next_part_marker)
    text = text[:idx] + deep_dive_report + "\n\n" + text[idx:]
    print("Added DEFECT-20261105-03 and 04 deep-dives before Part 4.")

# 3. Add to Part 5 Actionable Checklist
chk_marker = "- [ ] **P2 (`DEFECT-20261105-02`):**"
new_chk_items = (
    "- [ ] **P1 (`DEFECT-20261105-03`):** In `SP.AttendanceSvc` Overtime Policy validators, add rule enforcing `rates[].rateFormula > 0.0`. Reject negative or zero multipliers with HTTP 400.\n"
    "- [ ] **P1 (`DEFECT-20261105-04`):** In `SP.AttendanceSvc` policy command handlers, pre-populate `TenantName` (`MultilingualString { En, Ar }`) from `_currentTenant` into MongoDB `ERP.Attendance.Policies` across all policy types.\n"
)

if chk_marker in text and "DEFECT-20261105-03" not in text:
    idx = text.find(chk_marker)
    text = text[:idx] + new_chk_items + text[idx:]
    print("Added DEFECT-20261105-03 and 04 to Part 5 Checklist.")

with open(report_path, 'w', encoding='utf-8') as f:
    f.write(text)

print(f"Successfully updated {report_path}!")
