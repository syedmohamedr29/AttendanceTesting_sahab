import sys

sys.stdout.reconfigure(encoding='utf-8')

log_path = 'Defects/Attendance2_Master_Defect_Log.md'
with open(log_path, 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Update Executive Summary
text = text.replace("| **TOTAL** | **57** |", "| **TOTAL** | **59** |")
text = text.replace("total of **57 defects and architecture gaps**", "total of **59 defects and architecture gaps**")
text = text.replace("| 🟠 **P1 (Critical)** | **44** |", "| 🟠 **P1 (Critical)** | **46** |")
text = text.replace("(All 54 Defects)", "(All 59 Defects)")

# 2. Add to Section 2 Matrix
matrix_marker = "| [`DEFECT-20261105-02`](#defect-20261105-02) | 🟡 P2 | Attendance Policy / Architecture | `tenantName` and `id` exposed in request body DTOs across all Policy POST/PATCH APIs | ``POST / PATCH /attpolicies/*`` | [Evidence 40](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_40_swagger_policy_tenantname_id_in_request_body.png) |\n"

new_matrix_rows = (
    "| [`DEFECT-20261105-03`](#defect-20261105-03) | 🟠 P1 | Attendance Policy / Business Logic | Overtime Policy allows negative `rateFormula` multiplier (`-1.5`) with HTTP 200 OK | ``POST / PATCH /attpolicies/overtime`` | [Evidence 41](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_41_overtime_policy_negative_rateformula_accepted_compass.png) |\n"
    "| [`DEFECT-20261105-04`](#defect-20261105-04) | 🟠 P1 | Attendance Policy / Master Data | `TenantName` persists as `Object (empty)` `{}` in MongoDB across Break, Grace Period & Overtime Policies | ``POST / PATCH /attpolicies/*`` | [Evidence 42](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_42_policy_tenantname_empty_object_compass.png) |\n"
)

if matrix_marker in text and "DEFECT-20261105-03" not in text:
    idx = text.find(matrix_marker) + len(matrix_marker)
    text = text[:idx] + new_matrix_rows + text[idx:]
    print("Added DEFECT-20261105-03 and 04 to Defect Matrix.")

# 3. Add Deep-Dive sections before defect-20261103-16
defect_03_04_deep_dive = """---

### <a id="defect-20261105-03"></a>🔴 DEFECT-20261105-03: Overtime Policy Allows Negative `rateFormula` Multiplier (`-1.5`) with HTTP 200 OK Resulting in Corrupted Payroll Calculations (Missing Math & Payroll Invariant Validation)
- **Severity:** 🟠 P1 (Critical / Business Logic & Payroll Invariant)
- **Target Route:** `POST /api/companies/{companyId}/attpolicies/overtime` & `PATCH /api/companies/{companyId}/attpolicies/overtime/{policyId}`
- **Target Collection:** `Sahab.ERP.Attendance.Policies`
- **Controller:** `OvertimePolicyController`
- **Discovered Date:** 05 November 2026 | **Tested Company:** Attendance 6 (`3a249870-184c-0373-f344-015d602678d7`)
- **Document ID Created in MongoDB:** `UUID("77213223-d4ef-4767-ad6c-ebb778c77056")`
- **Status:** Open / Unresolved
- **Evidence Reference:** [Evidence 41 (`evidence_41_overtime_policy_negative_rateformula_accepted_compass.png`)](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_41_overtime_policy_negative_rateformula_accepted_compass.png)

#### 1. Problem Summary
During live manual API testing on Company **Attendance 6**, submitting an Overtime Policy with a negative overtime multiplier (`rateFormula: -1.5`) was **accepted with HTTP 200 OK** and persisted into MongoDB collection `Sahab.ERP.Attendance.Policies`:

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

#### 2. Root Cause Analysis
The validator for `OvertimePolicyDto` validates buffer minutes (`BufferMinutes >= 0`), but completely lacks FluentValidation rules for the nested `rates[].rateFormula` property. Consequently:
- Negative multipliers (e.g., `-1.5`, `-2.0`) are persisted without validation.
- Zero multipliers (`0.0`) are accepted.
- When payroll calculations or attendance log pipeline L3 overtime calculations run, multiplying overtime hours by `-1.5` will **deduct pay from the employee** instead of granting overtime pay!

#### 3. Reproduction Steps (Postman / Swagger)
1. Send `POST /api/companies/3a249870-184c-0373-f344-015d602678d7/attpolicies/overtime` with the payload above.
2. Observe status code `200 OK` (Expected: `400 Bad Request`).
3. Query MongoDB Compass:
   ```javascript
   { "_id": UUID("77213223-d4ef-4767-ad6c-ebb778c77056") }
   ```
4. Observe `Rates[0].RateFormula: -1.5` stored in the database.

#### 4. Photographic Proof from MongoDB Compass
| Visual Evidence | Description |
| :--- | :--- |
| ![DEFECT-20261105-03](../defect_evidence/evidence_41_overtime_policy_negative_rateformula_accepted_compass.png) | **File:** `evidence_41_overtime_policy_negative_rateformula_accepted_compass.png`<br><br>[🔍 Click to Open Full-Resolution Image](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_41_overtime_policy_negative_rateformula_accepted_compass.png)<br><br>*Evidence 41: MongoDB Compass live inspection of document `77213223-d4ef-4767-ad6c-ebb778c77056` on Company Attendance 6. Highlighted in red: RateFormula: -1.5 accepted with HTTP 200 OK.* |

#### 5. Developer Remediation (.NET 9 C#)
In `SP.AttendanceSvc` validators, add:
```csharp
RuleForEach(x => x.Rates).ChildRules(rate => {
    rate.RuleFor(r => r.RateFormula)
        .GreaterThan(0.0)
        .WithMessage("Overtime rate multiplier must be greater than 0.");
});
```

---

### <a id="defect-20261105-04"></a>🔴 DEFECT-20261105-04: `TenantName` Persists as `Object (empty)` `{}` in MongoDB Collection `ERP.Attendance.Policies` Across All Policy Types (Break, Grace Period, Overtime) During Creation and Updates
- **Severity:** 🟠 P1 (Critical / Master Data Integrity & Multi-Tenancy)
- **Target Routes:**
  - `POST` & `PATCH` `/api/companies/{companyId}/attpolicies/break`
  - `POST` & `PATCH` `/api/companies/{companyId}/attpolicies/graceperiod`
  - `POST` & `PATCH` `/api/companies/{companyId}/attpolicies/overtime`
  - `GET /api/companies/{companyId}/attpolicies`
  - `GET /api/companies/{companyId}/attpolicies/{policyId}`
- **Target Collection:** `Sahab.ERP.Attendance.Policies`
- **Discovered Date:** 05 November 2026 | **Tested Company:** Attendance 6 (`3a249870-184c-0373-f344-015d602678d7`)
- **Sample Document IDs:**
  - Break Policy: `UUID("88a26cf7-54bc-42a1-9624-5fba47cc3587")`
  - Grace Period Policy: `UUID("8b38971d-e9b2-4776-96d9-c6fae1da652b")`
  - Overtime Policy: `UUID("6aa93a26-73ca-40af-b725-3faa28d8f4c1")`
- **Status:** Open / Unresolved
- **Evidence Reference:** [Evidence 42 (`evidence_42_policy_tenantname_empty_object_compass.png`)](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_42_policy_tenantname_empty_object_compass.png)

#### 1. Problem Summary
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

While `CompanyName` and `TenantId` are populated correctly, `TenantName` is left unpopulated across all policy types.

#### 2. Root Cause Analysis
The domain entity constructors for `BreakPolicy`, `GracePeriodPolicy`, and `OvertimePolicy` instantiate `TenantName = new MultilingualString()` without populating `En` or `Ar` strings from `_currentTenant.Name` and `_currentTenant.ArabicName`.

#### 3. Reproduction Steps (Postman / Swagger)
1. Send `POST /api/companies/3a249870-184c-0373-f344-015d602678d7/attpolicies/break`.
2. Inspect response JSON: `"tenantName": {}`.
3. Open MongoDB Compass > `Sahab` > `ERP.Attendance.Policies`.
4. Filter by:
   ```javascript
   { "CompanyId": UUID("3a249870-184c-0373-f344-015d602678d7") }
   ```
5. Observe `TenantName: Object (empty)` across all created policy documents.

#### 4. Photographic Proof from MongoDB Compass
| Visual Evidence | Description |
| :--- | :--- |
| ![DEFECT-20261105-04](../defect_evidence/evidence_42_policy_tenantname_empty_object_compass.png) | **File:** `evidence_42_policy_tenantname_empty_object_compass.png`<br><br>[🔍 Click to Open Full-Resolution Image](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_42_policy_tenantname_empty_object_compass.png)<br><br>*Evidence 42: MongoDB Compass live inspection of collection ERP.Attendance.Policies on Company Attendance 6. Highlighted in red: TenantName: Object (empty) {} while CompanyName is populated.* |

#### 5. Developer Remediation (.NET 9 C#)
In all policy command handlers (`CreateBreakPolicyCommandHandler`, etc.):
```csharp
policy.TenantName = new MultilingualString
{
    En = !string.IsNullOrWhiteSpace(_currentTenant.Name) ? _currentTenant.Name : "Attendance",
    Ar = !string.IsNullOrWhiteSpace(_currentTenant.ArabicName) ? _currentTenant.ArabicName : "الحضور"
};
```
"""

marker_next = '### <a id="defect-20261103-16">'
if marker_next in text and 'id="defect-20261105-03"' not in text:
    idx = text.find(marker_next)
    text = text[:idx] + defect_03_04_deep_dive + "\n" + text[idx:]
    print("Added DEFECT-20261105-03 and 04 Detailed Deep Dives.")

# 4. Add to Section 8 Priority 1 Checklist
chk_p1_marker = "- [ ] **P1 (`DEFECT-20261105-01`):**"
new_chk_p1 = (
    "- [ ] **P1 (`DEFECT-20261105-03`):** In `SP.AttendanceSvc` Overtime Policy validators, add rule enforcing `rates[].rateFormula > 0.0`. Reject negative or zero multipliers with HTTP 400.\n"
    "- [ ] **P1 (`DEFECT-20261105-04`):** In `SP.AttendanceSvc` policy command handlers, pre-populate `TenantName` (`MultilingualString { En, Ar }`) from `_currentTenant` into MongoDB `ERP.Attendance.Policies` across all policy types.\n"
)

if chk_p1_marker in text and "DEFECT-20261105-03" not in text[100000:]:
    idx = text.find(chk_p1_marker)
    text = text[:idx] + new_chk_p1 + text[idx:]
    print("Added DEFECT-20261105-03 and 04 to Section 8 Priority 1 Checklist.")

with open(log_path, 'w', encoding='utf-8') as f:
    f.write(text)

print("Updated Defects/Attendance2_Master_Defect_Log.md successfully!")

