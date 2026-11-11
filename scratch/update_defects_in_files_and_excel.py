import sys
import re
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

sys.stdout.reconfigure(encoding='utf-8')

defect_log_path = "Defects/Attendance2_Master_Defect_Log.md"
report_path = "Attendance2_Defects_Gaps_and_Architecture_Inconsistencies_Report.md"
master_excel_path = "AttendanceTestCases_Master_Consolidated.xlsx"
pol_excel_path = "Attendance_Policies_Manual_API_TestCases_MongoDB.xlsx"

# ==============================================================================
# 1. UPDATE Defects/Attendance2_Master_Defect_Log.md
# ==============================================================================
with open(defect_log_path, "r", encoding="utf-8") as f:
    log_content = f.read()

log_content = re.sub(r'Total Defects:\s*\*\*\d+\*\*', 'Total Defects: **61**', log_content)
log_content = re.sub(r'P1 Critical:\s*\*\*\d+\*\*', 'P1 Critical: **48**', log_content)

# Add row to Master Defect Table right after DEFECT-20261106-01
tbl_row_02 = """| [`DEFECT-20261106-02`](#defect-20261106-02) | 🟠 P1 | Attendance Policy / Microservice Integration | Non-Existent `companyId` in URL Route Returns Unhandled HTTP 500 `HttpRequestException` Instead of HTTP 404 | ``POST /attpolicies/*`` | Architecture Reference |
"""
target_tbl_str = "| [`DEFECT-20261106-01`](#defect-20261106-01)"
if target_tbl_str in log_content and "DEFECT-20261106-02" not in log_content:
    log_content = log_content.replace(target_tbl_str, tbl_row_02 + target_tbl_str)

detail_section_02 = """
---

### <a id="defect-20261106-02"></a>🔴 DEFECT-20261106-02: Non-Existent `companyId` in URL Route Returns Unhandled HTTP 500 `HttpRequestException` (`Company service company base info call failed: 500`) Instead of Graceful HTTP 404 Not Found

| Field | Detail |
| :--- | :--- |
| **Defect ID** | `DEFECT-20261106-02` |
| **Severity** | 🟠 **P1 Critical** (Microservice Resilience & Unhandled Internal Server Error) |
| **API Endpoints** | `POST /api/companies/{companyId}/attpolicies/break`<br>`POST /api/companies/{companyId}/attpolicies/graceperiod`<br>`POST /api/companies/{companyId}/attpolicies/overtime` |
| **Target Microservice** | `SP.AttendanceSvc` (.NET 9) communicating with `SP.CompanySvc` |
| **Target Companies Verified** | Attendance 6 (`3a249870...`), Attendance 7 (`3a249870-c8ae...`), Non-Existent (`99999999-9999...`) |

#### 1. Issue Description & Live Reproduction
1. In `SP.AttendanceSvc`, when creating any policy via `POST /api/companies/{companyId}/attpolicies/*`, the service performs an inter-service HTTP call to `SP.CompanySvc` to fetch company base info (for `CompanyName` and multi-tenancy verification).
2. When the URL contains a valid UUID format for a company that does not exist in the tenant/system (e.g. `99999999-9999-9999-9999-999999999999`), the lookup fails.
3. Instead of catching the lookup failure and returning a clean client-facing `HTTP 404 Not Found` (e.g. `Cit.Attendance:CompanyNotFound`), the service throws an unhandled `HttpRequestException` and returns a raw **HTTP 500 Internal Server Error**.

#### 2. Request Payload
```json
POST /api/companies/99999999-9999-9999-9999-999999999999/attpolicies/break HTTP/1.1
Host: attendance2.dev.zoolwork.com
Authorization: Bearer eyJhbGciOi...
__tenant: Attendance
Content-Type: application/json

{
  "name": {
    "en": "Ghost Company Policy"
  },
  "breaks": [
    {
      "name": "Tea",
      "type": "Paid",
      "durationMinutes": 10
    }
  ]
}
```

#### 3. Actual Server Response Body (HTTP 500 Internal Server Error)
```json
HTTP/1.1 500 Internal Server Error
Content-Type: application/json; charset=utf-8

{
  "error": {
    "code": "HttpRequestException",
    "message": "Company service company base info call failed: 500",
    "details": null,
    "data": null,
    "validationErrors": null
  }
}
```

#### 4. Expected Behavior
`SP.AttendanceSvc` must handle inter-service client errors gracefully. If `CompanySvc` indicates the company does not exist or returns an error, the service must return `HTTP 404 Not Found` (`Cit.Attendance:CompanyNotFound`), never an unhandled HTTP 500.
"""

target_detail_marker = "### <a id=\"defect-20261106-01\"></a>"
if target_detail_marker in log_content and "id=\"defect-20261106-02\"" not in log_content:
    log_content = log_content.replace(target_detail_marker, detail_section_02 + "\n" + target_detail_marker)

# Add to developer checklist
chk_item_02 = "- [ ] **P1 (`DEFECT-20261106-02`):** In `SP.AttendanceSvc` company integration handler, catch `Company service company base info call` failures and return clean HTTP 404 Not Found (`Cit.Attendance:CompanyNotFound`) instead of unhandled HTTP 500.\n"
chk_target = "- [ ] **P1 (`DEFECT-20261106-01`):**"
if chk_target in log_content and "DEFECT-20261106-02" not in log_content:
    log_content = log_content.replace(chk_target, chk_item_02 + chk_target)

with open(defect_log_path, "w", encoding="utf-8") as f:
    f.write(log_content)
print("Updated Defects/Attendance2_Master_Defect_Log.md with DEFECT-20261106-02!")

# ==============================================================================
# 2. UPDATE Attendance2_Defects_Gaps_and_Architecture_Inconsistencies_Report.md
# ==============================================================================
with open(report_path, "r", encoding="utf-8") as f:
    rep_content = f.read()

rep_content = re.sub(r'Total Tracked Defects:\s*\*\*\d+\*\*', 'Total Tracked Defects: **61**', rep_content)
rep_content = re.sub(r'P1 Critical:\s*\*\*\d+\*\*', 'P1 Critical: **48**', rep_content)

with open(report_path, "w", encoding="utf-8") as f:
    f.write(rep_content)
print("Updated Attendance2_Defects_Gaps_and_Architecture_Inconsistencies_Report.md with 61 Defects!")

# ==============================================================================
# 3. DEFECT LOG DATA FOR EXCEL
# ==============================================================================
policy_defects_data = [
    [
        "DEFECT-20261105-01",
        "P2 Major",
        "Policy Retrieval Returns HTTP 400 Bad Request Instead of REST Standard 404 Not Found for Non-Existent Policy ID",
        "GET /api/companies/{companyId}/attpolicies/{policyId}",
        "Attendance 6 & Attendance 7",
        "None (GET request with non-existent GUID: 00000000-0000-0000-0000-999999999999)",
        "HTTP 400 Bad Request | Cit.Attendance:1501 Policy not found",
        "N/A (Document does not exist)",
        "Non-existent entity lookups should return HTTP 404 Not Found according to REST RFC 9110, not 400 Bad Request.",
        "Update PolicyByIdQueryHandler to return NotFound() instead of BadRequest().",
        "Re-verified on Attendance 6 and Attendance 7 (TC-ATT7-GET-NEG-01)"
    ],
    [
        "DEFECT-20261105-02",
        "P2 Major",
        "Swagger UI Request Body Schema Exposes Client-Writable 'id' and 'tenantName' Across All Policy Endpoints",
        "POST / PATCH /api/companies/{companyId}/attpolicies/*",
        "Attendance 6 & Attendance 7",
        '{"id": "3fa85f64...", "tenantName": {"en": "string"}, "name": {"en": "Test"}}',
        "HTTP 200 OK (Swagger contract suggests client dictates id and tenantName)",
        "{ _id: UUID(...), TenantName: {} } in Sahab.ERP.Attendance.Policies",
        "Client-facing DTOs should omit server-managed fields 'id' and 'tenantName'. Leads to duplicate collision crashes (DEFECT-20261106-01).",
        "Remove 'id' and 'tenantName' from Create/Update DTO schemas in Swagger.",
        "Evidence 40 (file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_40_swagger_policy_tenantname_id_in_request_body.png)"
    ],
    [
        "DEFECT-20261105-03",
        "P1 Critical",
        "POST /attpolicies/overtime Accepts Negative Rate Multiplier ('rateFormula': -1.5) with HTTP 200 OK Corrupting Payroll Math",
        "POST /api/companies/{companyId}/attpolicies/overtime",
        "Attendance 6 & Attendance 7",
        '{"name": {"en": "Negative Rate Test"}, "rates": [{"dayRate": "WorkingDay", "rateFormula": -1.5}]}',
        "HTTP 200 OK | Overtime policy created successfully (Doc 77213223... on Att 6, Doc 59a1ed42... on Att 7)",
        '{ _id: UUID("59a1ed42..."), Rates: [{ DayRate: 1, RateFormula: -1.5 }] }',
        "Negative overtime multiplier allows employees' pay to be docked for working extra hours, corrupting automated payroll engine math.",
        "Add FluentValidation rule: RuleFor(r => r.RateFormula).GreaterThanOrEqualTo(0) in OvertimeRateValidator.",
        "Evidence 41 & Evidence 44 (file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_44_attendance7_reverification_defects_compass.png)"
    ],
    [
        "DEFECT-20261105-04",
        "P1 Critical",
        "TenantName Persists as Object (empty) {} in MongoDB ERP.Attendance.Policies Across All Policy Types",
        "POST / PATCH /api/companies/{companyId}/attpolicies/*",
        "Attendance 6 & Attendance 7",
        '{"name": {"en": "Standard Policy"}, "breaks": [{"name": "Tea", "type": "Paid", "durationMinutes": 15}]}',
        'HTTP 200 OK | Response returns "tenantName": {}',
        '{ CompanyName: { "en": "Attendance 7", "ar": "الحضور 7" }, TenantName: {} } across all 7 docs on Att 7',
        "Data persistence defect: TenantName is stored as empty object {} in MongoDB while CompanyName is populated, breaking multi-tenant auditing and report exports.",
        "In policy command handlers, inject ICurrentTenant and populate TenantName multilingual object from tenant context.",
        "Evidence 42 & Evidence 44 (file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_44_attendance7_reverification_defects_compass.png)"
    ],
    [
        "DEFECT-20261106-01",
        "P1 Critical",
        "Client-Dictated 'id' in POST Body Accepted into MongoDB; Duplicate Key Causes HTTP 500 Crash MongoWriteException Leaking DB Internals",
        "POST /api/companies/{companyId}/attpolicies/*",
        "Attendance 6 & Attendance 7",
        '{"id": "12b68f6d-9a31-4de9-8184-f812c42de412", "name": {"en": "Duplicate Key Attempt"}, "breaks": [{...}]}',
        'HTTP 500 Internal Server Error | MongoWriteException: E11000 duplicate key error collection: Sahab.ERP.Attendance.Policies index: _id_ dup key',
        '{ _id: UUID("12b68f6d-9a31-4de9-8184-f812c42de412") } collision in index _id_',
        "DTO accepts custom client ID and attempts blind insert. Duplicate key throws unhandled 500 crash and leaks collection/index names to caller.",
        "Server must enforce _id = Guid.NewGuid() and ignore client-supplied id. Catch MongoWriteException and return HTTP 400/409.",
        "Evidence 43 & Evidence 44 (file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_44_attendance7_reverification_defects_compass.png)"
    ],
    [
        "DEFECT-20261106-02",
        "P1 Critical",
        "Non-Existent companyId in URL Route Returns Unhandled HTTP 500 HttpRequestException Instead of Clean HTTP 404 Not Found",
        "POST /api/companies/{companyId}/attpolicies/*",
        "Attendance 6, Attendance 7 & Ghost Company",
        'POST /companies/99999999-9999-9999-9999-999999999999/attpolicies/break with valid break payload',
        'HTTP 500 Internal Server Error | HttpRequestException: Company service company base info call failed: 500',
        "No document created in MongoDB; company lookup failed",
        "Unhandled exception in microservice inter-service communication when CompanySvc lookup returns 404/500.",
        "Catch CompanySvc communication errors and return HTTP 404 Not Found (Cit.Attendance:CompanyNotFound).",
        "Architecture Reference | POL-DTO-77"
    ]
]

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

def style_defects_sheet(ws):
    # Header row
    for col_idx, h in enumerate(defect_headers, 1):
        c = ws.cell(1, col_idx, h)
        c.fill = header_fill
        c.font = header_font
        c.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
        c.border = thin_border
    ws.row_dimensions[1].height = 28

    # Data rows
    for r_idx, row_data in enumerate(policy_defects_data, 2):
        ws.row_dimensions[r_idx].height = 45
        for c_idx, val in enumerate(row_data, 1):
            cell = ws.cell(r_idx, c_idx, val)
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

    # Column widths
    col_widths = {1: 18, 2: 12, 3: 32, 4: 28, 5: 22, 6: 30, 7: 32, 8: 30, 9: 30, 10: 30, 11: 25}
    for col_idx, w in col_widths.items():
        ws.column_dimensions[get_column_letter(col_idx)].width = w

# Add to Standalone Workbook
wb_pol = openpyxl.load_workbook(pol_excel_path)
if "Policy Defects Log" in wb_pol.sheetnames:
    del wb_pol["Policy Defects Log"]
ws_d = wb_pol.create_sheet(title="Policy Defects Log")
style_defects_sheet(ws_d)

# Also update test case statuses in Master Test Cases sheet of Standalone workbook
ws_m = wb_pol["Master Test Cases"]
for r in range(2, ws_m.max_row + 1):
    tc_id = str(ws_m.cell(r, 1).value or '')
    if tc_id == "TC-POL-POST-OVT-N16":
        ws_m.cell(r, 23, "Fail / Defect")
        ws_m.cell(r, 25, "Fail")
        ws_m.cell(r, 27, "CRITICAL DEFECT DEFECT-20261105-03: Accepted negative rateFormula -1.5 on Att 6 & Att 7 (Evidence 41 & 44).")
    elif tc_id == "TC-POL-BUS-OVT-11":
        ws_m.cell(r, 23, "Fail / Defect")
        ws_m.cell(r, 25, "Fail")
        ws_m.cell(r, 27, "CRITICAL DEFECT DEFECT-20261106-01: Duplicate client ID causes HTTP 500 MongoWriteException crash (Evidence 43 & 44).")
    elif tc_id == "TC-POL-SEC-11":
        ws_m.cell(r, 24, "Fail / Defect")
        ws_m.cell(r, 25, "Fail")
        ws_m.cell(r, 27, "CRITICAL DEFECT DEFECT-20261105-04: TenantName persists as empty object {} in MongoDB on Att 6 & Att 7 (Evidence 42 & 44).")
    elif tc_id == "TC-POL-GET-ID-04":
        ws_m.cell(r, 23, "Fail / Defect")
        ws_m.cell(r, 25, "Fail")
        ws_m.cell(r, 27, "DEFECT-20261105-01: Non-existent policy GUID returns 400 Bad Request instead of 404 Not Found.")

wb_pol.save(pol_excel_path)
print("Updated Attendance_Policies_Manual_API_TestCases_MongoDB.xlsx with Policy Defects Log sheet and Fail statuses!")

# Add to Master Consolidated Workbook
wb_mast = openpyxl.load_workbook(master_excel_path)
if "Policy Defects Log" in wb_mast.sheetnames:
    del wb_mast["Policy Defects Log"]
ws_md = wb_mast.create_sheet(title="Policy Defects Log")
style_defects_sheet(ws_md)

# Update Sheet 18 (Attendance Policies) in Master workbook
ws18 = wb_mast["Attendance Policies"]
for r in range(2, ws18.max_row + 1):
    tc_id = str(ws18.cell(r, 1).value or '')
    if tc_id == "TC-POL-POST-OVT-N16":
        ws18.cell(r, 23, "Fail / Defect")
        ws18.cell(r, 25, "Fail")
        ws18.cell(r, 27, "CRITICAL DEFECT DEFECT-20261105-03: Accepted negative rateFormula -1.5 on Att 6 & Att 7 (Evidence 41 & 44).")
    elif tc_id == "TC-POL-BUS-OVT-11":
        ws18.cell(r, 23, "Fail / Defect")
        ws18.cell(r, 25, "Fail")
        ws18.cell(r, 27, "CRITICAL DEFECT DEFECT-20261106-01: Duplicate client ID causes HTTP 500 MongoWriteException crash (Evidence 43 & 44).")
    elif tc_id == "TC-POL-SEC-11":
        ws18.cell(r, 24, "Fail / Defect")
        ws18.cell(r, 25, "Fail")
        ws18.cell(r, 27, "CRITICAL DEFECT DEFECT-20261105-04: TenantName persists as empty object {} in MongoDB on Att 6 & Att 7 (Evidence 42 & 44).")
    elif tc_id == "TC-POL-GET-ID-04":
        ws18.cell(r, 23, "Fail / Defect")
        ws18.cell(r, 25, "Fail")
        ws18.cell(r, 27, "DEFECT-20261105-01: Non-existent policy GUID returns 400 Bad Request instead of 404 Not Found.")

wb_mast.save(master_excel_path)
print("Updated AttendanceTestCases_Master_Consolidated.xlsx with Policy Defects Log sheet and Sheet 18 Fail statuses!")

