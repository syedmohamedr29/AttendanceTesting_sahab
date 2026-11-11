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
root_excel_path = "AttendanceTestCases.xlsx"

# ==============================================================================
# 1. UPDATE Defects/Attendance2_Master_Defect_Log.md
# ==============================================================================
with open(defect_log_path, "r", encoding="utf-8") as f:
    log_text = f.read()

# Update metric counters
log_text = re.sub(r'Total Defects:\s*\*\*\d+\*\*', 'Total Defects: **62**', log_text)
log_text = re.sub(r'P1 Critical:\s*\*\*\d+\*\*', 'P1 Critical: **49**', log_text)

# Table row for DEFECT-20261106-03
tbl_row_03 = """| [`DEFECT-20261106-03`](#defect-20261106-03) | 🟠 P1 | Attendance Policy / API Contract & DTO Design | Invalid API Request Body Structure: `id` and `tenantName` Exposed in Request DTOs Across All Policy APIs — Both Fields Must Be Removed from Client Payload | ``POST / PATCH /attpolicies/*`` | [Evidence 45](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_45_api_request_body_invalid_structure_id_tenantname_comparison.png) |
"""
target_tbl = "| [`DEFECT-20261106-02`](#defect-20261106-02)"
if target_tbl in log_text and "DEFECT-20261106-03" not in log_text:
    log_text = log_text.replace(target_tbl, tbl_row_03 + target_tbl)

# Detail section for DEFECT-20261106-03
detail_section_03 = """
---

### <a id="defect-20261106-03"></a>🔴 DEFECT-20261106-03: Invalid API Request Body Structure: `id` and `tenantName` Exposed in Request DTOs Across All Policy APIs — Both Fields Must Be Removed from Client Payload Structure

| Field | Detail |
| :--- | :--- |
| **Defect ID** | `DEFECT-20261106-03` |
| **Severity** | 🟠 **P1 Critical** (API Contract Architecture Violation, Invalid Request Structure & Multi-Tenant Security) |
| **API Endpoints** | `POST & PATCH /api/companies/{companyId}/attpolicies/break`<br>`POST & PATCH /api/companies/{companyId}/attpolicies/graceperiod`<br>`POST & PATCH /api/companies/{companyId}/attpolicies/overtime` |
| **Target Microservice** | `SP.AttendanceSvc` (.NET 9) |
| **Target Companies Verified** | Attendance 6 (`3a249870...`), Attendance 7 (`3a249870-c8ae...`) |
| **Visual Evidence** | [Evidence 45: API Request Body Invalid Structure Comparison](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_45_api_request_body_invalid_structure_id_tenantname_comparison.png) |

#### 1. Problem Description & User Feedback Analysis
Direct inspection of Swagger contracts and API client payloads confirms an invalid request body design structure across all policy creation and update endpoints:

1. **`id` Must Be Removed from Request Body:**
   - The API DTO expects `id: "00000000-0000-0000-0000-000000000000"` or client-dictated GUIDs in the POST body.
   - **Why this structure is invalid:** Entity IDs are strictly server-managed identifiers (`Guid.NewGuid()`). Exposing `id` in request DTOs forces callers to pass dummy IDs or custom GUIDs, directly triggering unhandled `MongoWriteException: E11000 duplicate key error` crashes on duplicate key collisions (`DEFECT-20261106-01`).
2. **`tenantName` Must Be Removed from Request Body:**
   - The API DTO expects `"tenantName": { "en": "Attendance", "ar": "Attendance" }` in the client request body.
   - **Why this structure is invalid:** In a multi-tenant SaaS architecture, tenant identity is derived strictly from the authenticated token or `__tenant` context header. Forcing the client to transmit `tenantName` is redundant, error-prone, and opens an anti-spoofing security vector (`TC-POL-SEC-12`).

#### 2. Side-by-Side Comparison of Invalid Request Structure (Captured in Evidence 45)

```
====================================================================================================
INVALID STRUCTURE (CURRENT API SCHEMA)                  VALID CLEAN STRUCTURE (EXPECTED REST DESIGN)
====================================================================================================
POST /api/companies/{companyId}/attpolicies/overtime     POST /api/companies/{companyId}/attpolicies/overtime
{                                                       {
  "id": "00000000-0000-0000-0000-000000000000", <--- ❌ REMOVE   "name": {
  "name": {                                               "en": "Standard Overtime Policy",
    "en": "Standard Overtime Policy",                     "ar": "سياسة العمل الإضافي القياسية"
    "ar": "سياسة العمل الإضافي القياسية"                  },
  },                                                      "isActive": true,
  "isActive": true,                                       "overtimeRule": 2,
  "tenantName": {                                <--- ❌ REMOVE   "hasBufferBeforeOvertime": false,
    "en": "Attendance",                                   "bufferMinutes": 0,
    "ar": "Attendance"                                    "rates": [
  },                                                        { "dayRate": 1, "rateFormula": 1.5 },
  "overtimeRule": 2,                                        { "dayRate": 2, "rateFormula": 1.5 },
  "hasBufferBeforeOvertime": false,                         { "dayRate": 3, "rateFormula": 1.5 }
  "bufferMinutes": 0,                                     ]
  "rates": [ ... ]                                      }
}
====================================================================================================
```

#### 3. Root Cause Analysis
- `CreateBreakPolicyDto`, `CreateGracePeriodPolicyDto`, and `CreateOvertimePolicyDto` in `SP.AttendanceSvc` inherit from or declare properties for `Id` (Guid) and `TenantName` (`MultilingualString`).
- ASP.NET Core model binding exposes these properties in Swagger OpenAPI specifications, making client libraries and consumers think they must provide them.

#### 4. Developer Action & Remediation
1. **Remove `Id` Property:** Strip `public Guid Id { get; set; }` from all Policy Create/Update request DTOs.
2. **Remove `TenantName` Property:** Strip `public MultilingualString TenantName { get; set; }` from all Policy Create/Update request DTOs.
3. **Server Auto-Population:**
   - In command handlers, generate `_id = Guid.NewGuid()`.
   - Resolve `TenantName` server-side from `_currentTenant.Name` and `_currentTenant.ArabicName`.
"""

target_detail_anchor = "### <a id=\"defect-20261106-01\"></a>"
if target_detail_anchor in log_text and "id=\"defect-20261106-03\"" not in log_text:
    log_text = log_text.replace(target_detail_anchor, detail_section_03 + "\n" + target_detail_anchor)

# Add Evidence 45 row to Evidence table
ev45_row = """| ![DEFECT-20261106-03](../defect_evidence/evidence_45_api_request_body_invalid_structure_id_tenantname_comparison.png) | **File:** `evidence_45_api_request_body_invalid_structure_id_tenantname_comparison.png`<br>**Defect:** [`DEFECT-20261106-03`](#defect-20261106-03)<br>**Description:** Direct visual comparison showing invalid request body structure: `id` (00000000-0000-...) and `tenantName` ({"en": "Attendance"}) must be removed from API request DTOs. |
"""
target_ev_tbl = "| ![DEFECT-20261106-01-ATT7]"
if target_ev_tbl in log_text and "evidence_45" not in log_text:
    log_text = log_text.replace(target_ev_tbl, ev45_row + target_ev_tbl)

# Add to developer checklist
chk_item_03 = "- [ ] **P1 (`DEFECT-20261106-03`):** In `SP.AttendanceSvc` DTO models, remove `id` and `tenantName` from `CreateBreakPolicyDto`, `CreateGracePeriodPolicyDto`, and `CreateOvertimePolicyDto`. Clients must not transmit either field.\n"
chk_target = "- [ ] **P1 (`DEFECT-20261106-02`):**"
if chk_target in log_text and "DEFECT-20261106-03" not in log_text:
    log_text = log_text.replace(chk_target, chk_item_03 + chk_target)

with open(defect_log_path, "w", encoding="utf-8") as f:
    f.write(log_text)
print("Updated Defects/Attendance2_Master_Defect_Log.md with DEFECT-20261106-03 & Evidence 45!")

# ==============================================================================
# 2. UPDATE Attendance2_Defects_Gaps_and_Architecture_Inconsistencies_Report.md
# ==============================================================================
with open(report_path, "r", encoding="utf-8") as f:
    rep_text = f.read()

rep_text = re.sub(r'Total Tracked Defects:\s*\*\*\d+\*\*', 'Total Tracked Defects: **62**', rep_text)
rep_text = re.sub(r'P1 Critical:\s*\*\*\d+\*\*', 'P1 Critical: **49**', rep_text)

# Update Banner
rep_text = rep_text.replace(
    "DEFECT-20261106-01 & DEFECT-20261106-02",
    "DEFECT-20261106-01, DEFECT-20261106-02 & DEFECT-20261106-03"
)

# Add row to Part 3H summary table
p3h_row_03 = """| **`DEFECT-20261106-03`** | 🟠 P1 Critical | `POST / PATCH /attpolicies/*` | Invalid request body structure: `id` and `tenantName` must be removed from all policy request DTOs | Attendance 6 & Attendance 7 | [Evidence 45](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_45_api_request_body_invalid_structure_id_tenantname_comparison.png) |
"""
p3h_tbl_marker = "| **`DEFECT-20261106-02`**"
if p3h_tbl_marker in rep_text and "DEFECT-20261106-03" not in rep_text:
    rep_text = rep_text.replace(p3h_tbl_marker, p3h_row_03 + p3h_tbl_marker)

# Add detail block in Part 3H
p3h_detail_03 = """
#### Defect `DEFECT-20261106-03`: Invalid API Request Body Structure — `id` and `tenantName` Must Be Removed from All Policy Request DTOs
- **Affected Endpoints:** `POST & PATCH /api/companies/{companyId}/attpolicies/*` (Break, Grace Period, Overtime)
- **Problem:** As demonstrated in [Evidence 45](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_45_api_request_body_invalid_structure_id_tenantname_comparison.png), the current API request body expects:
  1. `id: "00000000-0000-0000-0000-000000000000"`: Invalid for entity creation. IDs are server-generated (`Guid.NewGuid()`). Transmitting client IDs causes `MongoWriteException` duplicate key collision crashes (`DEFECT-20261106-01`).
  2. `"tenantName": { "en": "Attendance", "ar": "Attendance" }`: Invalid for client payloads. Multi-tenant architecture requires tenant identity to be established from the authenticated session context, not arbitrary client strings.
- **Resolution:** Remove both `id` and `tenantName` from all Policy Create/Update request body DTOs.
"""
p3h_detail_marker = "#### Defect `DEFECT-20261106-01`:"
if p3h_detail_marker in rep_text and "Defect `DEFECT-20261106-03`:" not in rep_text:
    rep_text = rep_text.replace(p3h_detail_marker, p3h_detail_03 + "\n" + p3h_detail_marker)

# Add Day 7 checklist item
chk_d7_03 = "- [ ] **P1 (`DEFECT-20261106-03`):** In `SP.AttendanceSvc` DTO models, completely remove `id` and `tenantName` properties from all Policy Create and Update request DTOs. Enforce clean request structures.\n"
chk_d7_target = "- [ ] **P1 (`DEFECT-20261106-01`):**"
if chk_d7_target in rep_text and "DEFECT-20261106-03" not in rep_text:
    rep_text = rep_text.replace(chk_d7_target, chk_d7_03 + chk_d7_target)

with open(report_path, "w", encoding="utf-8") as f:
    f.write(rep_text)
print("Updated Architecture Report with DEFECT-20261106-03 & Evidence 45!")

# ==============================================================================
# 3. UPDATE EXCEL WORKBOOKS (Master, Standalone & Root)
# ==============================================================================
new_defect_row_excel = [
    "DEFECT-20261106-03",
    "P1 Critical",
    "Invalid API Request Body Structure: 'id' and 'tenantName' Exposed in Request DTOs Across All Policy APIs — Both Fields Must Be Removed from Client Payload",
    "POST / PATCH /api/companies/{companyId}/attpolicies/*",
    "Attendance 6 & Attendance 7",
    '{"id": "00000000-0000-...", "tenantName": {"en": "Attendance"}, "name": {...}, "rates": [...]}',
    "HTTP 200 OK (API accepts invalid request structure; leads to duplicate collision crashes and spoofing)",
    "Document created with server or client ID; TenantName persists as empty object {} due to backend gap",
    "Forces clients to transmit dummy/all-zero GUIDs and redundant tenant strings. Causes duplicate key crashes (DEFECT-20261106-01) and security spoofing risks.",
    "Remove 'id' and 'tenantName' properties from all Policy Create and Update request DTOs in SP.AttendanceSvc.",
    "Evidence 45 (file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_45_api_request_body_invalid_structure_id_tenantname_comparison.png)"
]

thin_border = Border(
    left=Side(style='thin', color='D9D9D9'),
    right=Side(style='thin', color='D9D9D9'),
    top=Side(style='thin', color='D9D9D9'),
    bottom=Side(style='thin', color='D9D9D9')
)
p1_fill = PatternFill(start_color="FCE4D6", end_color="FCE4D6", fill_type="solid")

def add_defect_to_excel(excel_file):
    wb = openpyxl.load_workbook(excel_file)
    if "Policy Defects Log" not in wb.sheetnames:
        print(f"Sheet Policy Defects Log not in {excel_file}!")
        return
    ws = wb["Policy Defects Log"]
    
    # Check if already added
    exists = False
    for r in range(2, ws.max_row + 1):
        if ws.cell(r, 1).value == "DEFECT-20261106-03":
            exists = True
            break
            
    if not exists:
        new_row_idx = ws.max_row + 1
        ws.row_dimensions[new_row_idx].height = 45
        for c_idx, val in enumerate(new_defect_row_excel, 1):
            cell = ws.cell(new_row_idx, c_idx, val)
            cell.font = Font(name="Segoe UI", size=9)
            cell.border = thin_border
            cell.alignment = Alignment(vertical="center", wrap_text=True)
            if c_idx == 1:
                cell.font = Font(name="Segoe UI", size=9, bold=True)
                cell.alignment = Alignment(horizontal="center", vertical="center")
            elif c_idx == 2:
                cell.alignment = Alignment(horizontal="center", vertical="center")
                cell.fill = p1_fill
                cell.font = Font(name="Segoe UI", size=9, bold=True, color="C00000")
        wb.save(excel_file)
        print(f"Added DEFECT-20261106-03 to {excel_file} (Row {new_row_idx})!")
    else:
        print(f"DEFECT-20261106-03 already present in {excel_file}!")

add_defect_to_excel(master_excel_path)
add_defect_to_excel(pol_excel_path)
add_defect_to_excel(root_excel_path)

print("\n=== COMPLETED LOGGING DEFECT-20261106-03 ACROSS ALL FILES ===")
