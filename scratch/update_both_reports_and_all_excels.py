import sys
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

sys.stdout.reconfigure(encoding='utf-8')

report_path = "Attendance2_Defects_Gaps_and_Architecture_Inconsistencies_Report.md"
defect_log_path = "Defects/Attendance2_Master_Defect_Log.md"
root_excel_path = "AttendanceTestCases.xlsx"

# ==============================================================================
# 1. ADD PART 3H TO Attendance2_Defects_Gaps_and_Architecture_Inconsistencies_Report.md
# ==============================================================================
with open(report_path, "r", encoding="utf-8") as f:
    rep = f.read()

part_3h_text = """
# 🏢 Part 3H: Defects Identified & Live Verified on 05 & 06 November 2026 — Attendance Policy Module (Live Verification on Attendance 6 & Attendance 7)

### Summary Matrix: Attendance Policy Defects (Live Verified 05-06 Nov 2026)

| Defect ID | Severity | Module & Endpoint | Summary / Behavior | Target Companies Verified | Live Proof & Evidence |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **`DEFECT-20261105-02`** | 🟡 P2 Major | `POST / PATCH /attpolicies/*` | Swagger UI request body schema defectively exposes client-writable `id` and `tenantName` across Break, Grace Period, and Overtime DTOs | Attendance 6 & Attendance 7 | [Evidence 40](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_40_swagger_policy_tenantname_id_in_request_body.png) |
| **`DEFECT-20261105-03`** | 🟠 P1 Critical | `POST /attpolicies/overtime` | API accepts negative overtime rate multiplier (`rateFormula: -1.5`) with HTTP 200 OK, corrupting automated payroll engine math | Attendance 6 (Doc `77213223...`) & Attendance 7 (Doc `59a1ed42...`) | [Evidence 41](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_41_overtime_policy_negative_rateformula_accepted_compass.png) & [Evidence 44](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_44_attendance7_reverification_defects_compass.png) |
| **`DEFECT-20261105-04`** | 🟠 P1 Critical | `POST / PATCH /attpolicies/*` | `TenantName` persists as `Object (empty)` `{}` in MongoDB `ERP.Attendance.Policies` across all Break, Grace Period, and Overtime documents | Attendance 6 & Attendance 7 (all 7 docs) | [Evidence 42](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_42_policy_tenantname_empty_object_compass.png) & [Evidence 44](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_44_attendance7_reverification_defects_compass.png) |
| **`DEFECT-20261106-01`** | 🟠 P1 Critical | `POST /attpolicies/*` | Client-dictated `id` in POST request body is accepted into MongoDB; duplicate key collision causes unhandled HTTP 500 crash `MongoWriteException: E11000 duplicate key error` leaking collection name | Attendance 6 & Attendance 7 | [Evidence 43](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_43_policy_duplicate_id_mongo_500_crash.png) & [Evidence 44](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_44_attendance7_reverification_defects_compass.png) |
| **`DEFECT-20261106-02`** | 🟠 P1 Critical | `POST /attpolicies/*` | Calling policy endpoint with non-existent `companyId` in URL route returns unhandled HTTP 500 `HttpRequestException` (`Company service company base info call failed: 500`) instead of clean HTTP 404 | Attendance 6, Attendance 7 & Ghost Company | `POL-DTO-77` |

---

### Detailed Defect Deep-Dives (05-06 Nov 2026)

#### Defect `DEFECT-20261105-02`: Swagger UI Request Body Schema Exposes Client-Writable `id` and `tenantName`
- **Affected Endpoints:** `POST / PATCH /api/companies/{companyId}/attpolicies/break`, `.../graceperiod`, `.../overtime`
- **Issue:** Swagger UI displays `id` (GUID) and `tenantName` (`MultilingualString`) in the request body schema. In reality, the client should never send `id` (server auto-generates) nor `tenantName` (derived from auth context).
- **Consequence:** Misleads API callers into believing they must generate GUIDs, enabling the critical duplicate collision crash (`DEFECT-20261106-01`).
- **Visual Evidence:** [Evidence 40](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_40_swagger_policy_tenantname_id_in_request_body.png)

#### Defect `DEFECT-20261105-03`: `POST /attpolicies/overtime` Accepts Negative Rate Multiplier (`rateFormula: -1.5`) with HTTP 200 OK
- **Affected Endpoint:** `POST /api/companies/{companyId}/attpolicies/overtime`
- **Issue:** The service accepts negative `rateFormula: -1.5` in rates array with HTTP 200 OK and persists into MongoDB `Sahab.ERP.Attendance.Policies`.
- **Live Proof on Attendance 6:** Document `77213223-d4ef-4767-ad6c-ebb778c77056` created with `Rates: [{ DayRate: 1, RateFormula: -1.5 }]`.
- **Live Proof on Attendance 7:** Document `59a1ed42-4425-493f-9db9-4fca6d91d411` created with `Rates: [{ DayRate: 1, RateFormula: -1.5 }]`.
- **Business Impact:** Directly corrupts payroll math. When payroll runs, working overtime docks salary instead of compensating.
- **Visual Evidence:** [Evidence 41](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_41_overtime_policy_negative_rateformula_accepted_compass.png) & [Evidence 44](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_44_attendance7_reverification_defects_compass.png)
- **Fix:** Add FluentValidation rule: `RuleFor(r => r.RateFormula).GreaterThanOrEqualTo(0);`.

#### Defect `DEFECT-20261105-04`: `TenantName` Persists as `Object (empty)` `{}` in MongoDB `ERP.Attendance.Policies`
- **Affected Endpoints:** All Break, Grace Period, and Overtime endpoints.
- **Issue:** In MongoDB `Sahab.ERP.Attendance.Policies`, `CompanyName` is populated (e.g. `{"en": "Attendance 7", "ar": "الحضور 7"}`), but `TenantName` persists as `Object (empty)` `{}` across all documents.
- **Live Proof:** Verified across all 8 documents of Attendance 6 and all 7 documents of Attendance 7.
- **Visual Evidence:** [Evidence 42](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_42_policy_tenantname_empty_object_compass.png) & [Evidence 44](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_44_attendance7_reverification_defects_compass.png)
- **Fix:** In policy command handlers, inject `ICurrentTenant` and populate `TenantName` multilingual object.

#### Defect `DEFECT-20261106-01`: Client-Dictated `id` in POST Body Accepted into MongoDB; Duplicate Key Causes HTTP 500 Crash `MongoWriteException`
- **Affected Endpoints:** `POST /api/companies/{companyId}/attpolicies/*`
- **Issue:** The command handler writes the client's submitted `id` into MongoDB `_id`. When a duplicate `id` is transmitted, MongoDB throws `E11000 duplicate key error`. The .NET 9 service fails to catch it, crashing with **HTTP 500 Internal Server Error** and leaking collection name `Sahab.ERP.Attendance.Policies` and index `_id_`.
- **Live Reproduction on Attendance 7:**
  ```json
  POST /api/companies/3a249870-c8ae-b3dc-1b8d-c44efad14f89/attpolicies/break
  { "id": "12b68f6d-9a31-4de9-8184-f812c42de412", "name": { "en": "Duplicate Attempt" }, "breaks": [...] }
  Response: HTTP 500 MongoWriteException
  ```
- **Visual Evidence:** [Evidence 43](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_43_policy_duplicate_id_mongo_500_crash.png) & [Evidence 44](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_44_attendance7_reverification_defects_compass.png)
- **Fix:** Remove `id` from Create DTOs. Enforce `_id = Guid.NewGuid()` server-side. Catch `MongoWriteException` and return sanitized HTTP 400/409.

#### Defect `DEFECT-20261106-02`: Non-Existent `companyId` in URL Route Returns Unhandled HTTP 500 `HttpRequestException`
- **Affected Endpoints:** `POST /api/companies/{companyId}/attpolicies/*`
- **Issue:** When `companyId` does not exist in `CompanySvc`, inter-service lookup fails. `AttendanceSvc` returns unhandled HTTP 500 `HttpRequestException: Company service company base info call failed: 500` instead of clean HTTP 404 Not Found (`Cit.Attendance:CompanyNotFound`).
- **Fix:** Wrap `CompanySvc` client call in try-catch and map lookup errors to HTTP 404.
"""

target_marker = "# 🔄 Part 4: Standardized Bug Lifecycle Procedure"
if target_marker in rep and "# 🏢 Part 3H:" not in rep:
    rep = rep.replace(target_marker, part_3h_text + "\n" + target_marker)
    print("Added Part 3H to Attendance2_Defects_Gaps_and_Architecture_Inconsistencies_Report.md!")

# Add Day 7 to Part 5 Developer Checklist
day7_checklist = """
### 📅 Day 7: 05 & 06 November 2026 Checklist (Attendance Policy Module)
- [ ] **P1 (`DEFECT-20261105-03`):** In `OvertimeRateValidator.cs`, add `RuleFor(r => r.RateFormula).GreaterThanOrEqualTo(0);`. Block negative rate multipliers from corrupting payroll calculations.
- [ ] **P1 (`DEFECT-20261105-04`):** In `CreateBreakPolicyCommandHandler.cs`, `CreateGracePeriodPolicyCommandHandler.cs`, and `CreateOvertimePolicyCommandHandler.cs`, inject `ICurrentTenant` and populate `TenantName` multilingual object into MongoDB.
- [ ] **P1 (`DEFECT-20261106-01`):** In all policy create command handlers, enforce server-generated `_id = Guid.NewGuid()` and strictly ignore or remove client-dictated `id`. Catch `MongoWriteException` and return sanitized HTTP 400/409.
- [ ] **P1 (`DEFECT-20261106-02`):** In `CompanyServiceIntegrationHandler.cs`, catch company lookup failures and return clean HTTP 404 Not Found (`Cit.Attendance:CompanyNotFound`) instead of unhandled HTTP 500 `HttpRequestException`.
- [ ] **P2 (`DEFECT-20261105-01`):** In `GetPolicyByIdQueryHandler.cs`, return `NotFound()` (HTTP 404) when a policy GUID does not exist instead of `BadRequest()` (HTTP 400).
- [ ] **P2 (`DEFECT-20261105-02`):** In Swagger DTO definitions, remove client-writable `id` and `tenantName` properties from POST and PATCH request body schemas.
"""
chk_target_marker = "### 📅 Day 6: 03 November 2026 Checklist (Holiday List Module)"
if chk_target_marker in rep and "Day 7: 05 & 06 November 2026 Checklist" not in rep:
    # Find next section or end of Day 6
    idx_d6 = rep.find(chk_target_marker)
    # Find next section after Day 6
    idx_next = rep.find("\n#", idx_d6 + 50)
    if idx_next != -1:
        rep = rep[:idx_next] + "\n" + day7_checklist + "\n" + rep[idx_next:]
    else:
        rep = rep + "\n" + day7_checklist
    print("Added Day 7 Developer Checklist to Report!")

with open(report_path, "w", encoding="utf-8") as f:
    f.write(rep)
print("Updated Architecture Report with complete Part 3H and Day 7 Checklist!")

# ==============================================================================
# 2. ADD POLICY DEFECTS LOG TO AttendanceTestCases.xlsx (ROOT WORKBOOK)
# ==============================================================================
wb_root = openpyxl.load_workbook(root_excel_path)
if "Policy Defects Log" in wb_root.sheetnames:
    del wb_root["Policy Defects Log"]

ws_rd = wb_root.create_sheet(title="Policy Defects Log")

defect_headers = [
    "Defect ID", "Severity", "Defect Title & Summary", "API Endpoint", "Target Companies Tested",
    "Sample Request Payload", "Actual API Response & Status", "MongoDB Compass Evidence",
    "Impact & Business Risk", "Recommended Developer Fix", "Evidence Reference"
]

header_fill = PatternFill(start_color="1F4E79", end_color="1F4E79", fill_type="solid")
header_font = Font(name="Segoe UI", size=10, bold=True, color="FFFFFF")
thin_border = Border(
    left=Side(style='thin', color='D9D9D9'),
    right=Side(style='thin', color='D9D9D9'),
    top=Side(style='thin', color='D9D9D9'),
    bottom=Side(style='thin', color='D9D9D9')
)
p1_fill = PatternFill(start_color="FCE4D6", end_color="FCE4D6", fill_type="solid")
p2_fill = PatternFill(start_color="FFF2CC", end_color="FFF2CC", fill_type="solid")

for col_idx, h in enumerate(defect_headers, 1):
    c = ws_rd.cell(1, col_idx, h)
    c.fill = header_fill
    c.font = header_font
    c.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
    c.border = thin_border
ws_rd.row_dimensions[1].height = 28

policy_defects_data = [
    [
        "DEFECT-20261105-01", "P2 Major",
        "Policy Retrieval Returns HTTP 400 Bad Request Instead of REST Standard 404 Not Found for Non-Existent Policy ID",
        "GET /api/companies/{companyId}/attpolicies/{policyId}", "Attendance 6 & Attendance 7",
        "None (GET request with non-existent GUID: 00000000-0000-0000-0000-999999999999)",
        "HTTP 400 Bad Request | Cit.Attendance:1501 Policy not found", "N/A (Document does not exist)",
        "Non-existent entity lookups should return HTTP 404 Not Found according to REST RFC 9110, not 400 Bad Request.",
        "Update PolicyByIdQueryHandler to return NotFound() instead of BadRequest().",
        "Re-verified on Attendance 6 and Attendance 7 (TC-ATT7-GET-NEG-01)"
    ],
    [
        "DEFECT-20261105-02", "P2 Major",
        "Swagger UI Request Body Schema Exposes Client-Writable 'id' and 'tenantName' Across All Policy Endpoints",
        "POST / PATCH /api/companies/{companyId}/attpolicies/*", "Attendance 6 & Attendance 7",
        '{"id": "3fa85f64...", "tenantName": {"en": "string"}, "name": {"en": "Test"}}',
        "HTTP 200 OK (Swagger contract suggests client dictates id and tenantName)",
        "{ _id: UUID(...), TenantName: {} } in Sahab.ERP.Attendance.Policies",
        "Client-facing DTOs should omit server-managed fields 'id' and 'tenantName'. Leads to duplicate collision crashes (DEFECT-20261106-01).",
        "Remove 'id' and 'tenantName' from Create/Update DTO schemas in Swagger.",
        "Evidence 40 (file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_40_swagger_policy_tenantname_id_in_request_body.png)"
    ],
    [
        "DEFECT-20261105-03", "P1 Critical",
        "POST /attpolicies/overtime Accepts Negative Rate Multiplier ('rateFormula': -1.5) with HTTP 200 OK Corrupting Payroll Math",
        "POST /api/companies/{companyId}/attpolicies/overtime", "Attendance 6 & Attendance 7",
        '{"name": {"en": "Negative Rate Test"}, "rates": [{"dayRate": "WorkingDay", "rateFormula": -1.5}]}',
        "HTTP 200 OK | Overtime policy created successfully (Doc 77213223... on Att 6, Doc 59a1ed42... on Att 7)",
        '{ _id: UUID("59a1ed42..."), Rates: [{ DayRate: 1, RateFormula: -1.5 }] }',
        "Negative overtime multiplier allows employees' pay to be docked for working extra hours, corrupting automated payroll engine math.",
        "Add FluentValidation rule: RuleFor(r => r.RateFormula).GreaterThanOrEqualTo(0) in OvertimeRateValidator.",
        "Evidence 41 & Evidence 44 (file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_44_attendance7_reverification_defects_compass.png)"
    ],
    [
        "DEFECT-20261105-04", "P1 Critical",
        "TenantName Persists as Object (empty) {} in MongoDB ERP.Attendance.Policies Across All Policy Types",
        "POST / PATCH /api/companies/{companyId}/attpolicies/*", "Attendance 6 & Attendance 7",
        '{"name": {"en": "Standard Policy"}, "breaks": [{"name": "Tea", "type": "Paid", "durationMinutes": 15}]}',
        'HTTP 200 OK | Response returns "tenantName": {}',
        '{ CompanyName: { "en": "Attendance 7", "ar": "الحضور 7" }, TenantName: {} } across all 7 docs on Att 7',
        "Data persistence defect: TenantName is stored as empty object {} in MongoDB while CompanyName is populated, breaking multi-tenant auditing and report exports.",
        "In policy command handlers, inject ICurrentTenant and populate TenantName multilingual object from tenant context.",
        "Evidence 42 & Evidence 44 (file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_44_attendance7_reverification_defects_compass.png)"
    ],
    [
        "DEFECT-20261106-01", "P1 Critical",
        "Client-Dictated 'id' in POST Body Accepted into MongoDB; Duplicate Key Causes HTTP 500 Crash MongoWriteException Leaking DB Internals",
        "POST /api/companies/{companyId}/attpolicies/*", "Attendance 6 & Attendance 7",
        '{"id": "12b68f6d-9a31-4de9-8184-f812c42de412", "name": {"en": "Duplicate Key Attempt"}, "breaks": [{...}]}',
        'HTTP 500 Internal Server Error | MongoWriteException: E11000 duplicate key error collection: Sahab.ERP.Attendance.Policies index: _id_ dup key',
        '{ _id: UUID("12b68f6d-9a31-4de9-8184-f812c42de412") } collision in index _id_',
        "DTO accepts custom client ID and attempts blind insert. Duplicate key throws unhandled 500 crash and leaks collection/index names to caller.",
        "Server must enforce _id = Guid.NewGuid() and ignore client-supplied id. Catch MongoWriteException and return HTTP 400/409.",
        "Evidence 43 & Evidence 44 (file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_44_attendance7_reverification_defects_compass.png)"
    ],
    [
        "DEFECT-20261106-02", "P1 Critical",
        "Non-Existent companyId in URL Route Returns Unhandled HTTP 500 HttpRequestException Instead of Clean HTTP 404 Not Found",
        "POST /api/companies/{companyId}/attpolicies/*", "Attendance 6, Attendance 7 & Ghost Company",
        'POST /companies/99999999-9999-9999-9999-999999999999/attpolicies/break with valid break payload',
        'HTTP 500 Internal Server Error | HttpRequestException: Company service company base info call failed: 500',
        "No document created in MongoDB; company lookup failed",
        "Unhandled exception in microservice inter-service communication when CompanySvc lookup returns 404/500.",
        "Catch CompanySvc communication errors and return HTTP 404 Not Found (Cit.Attendance:CompanyNotFound).",
        "Architecture Reference | POL-DTO-77"
    ]
]

for r_idx, row_data in enumerate(policy_defects_data, 2):
    ws_rd.row_dimensions[r_idx].height = 45
    for c_idx, val in enumerate(row_data, 1):
        cell = ws_rd.cell(r_idx, c_idx, val)
        cell.font = Font(name="Segoe UI", size=9)
        cell.border = thin_border
        cell.alignment = Alignment(vertical="center", wrap_text=True)
        if c_idx == 1:
            cell.font = Font(name="Segoe UI", size=9, bold=True)
            cell.alignment = Alignment(horizontal="center", vertical="center")
        elif c_idx == 2:
            cell.alignment = Alignment(horizontal="center", vertical="center")
            if "P1" in str(val):
                cell.fill = p1_fill
                cell.font = Font(name="Segoe UI", size=9, bold=True, color="C00000")
            elif "P2" in str(val):
                cell.fill = p2_fill
                cell.font = Font(name="Segoe UI", size=9, bold=True, color="7F6000")

col_widths = {1: 18, 2: 12, 3: 32, 4: 28, 5: 22, 6: 30, 7: 32, 8: 30, 9: 30, 10: 30, 11: 25}
for col_idx, w in col_widths.items():
    ws_rd.column_dimensions[get_column_letter(col_idx)].width = w

wb_root.save(root_excel_path)
print("Updated root AttendanceTestCases.xlsx with Policy Defects Log sheet!")

print("\n=== ALL FILES SUCCESSFULLY UPDATED WITH DEFECT LOGS ===")

