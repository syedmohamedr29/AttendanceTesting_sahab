import sys

sys.stdout.reconfigure(encoding='utf-8')

file_path = 'Defects/Attendance2_Master_Defect_Log.md'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

old_block = """| [`DEFECT-20261026-01`](#defect-20261026-01) | 🟠 P1 | Cross-Service Sync | Cross-service sync failure: Company Service `Checklist: false` not reflected in Attendance Service | ``CompanySvc` Sync` | [Evidence 02](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_02_companiesmaster_checklist_false.png) |
| [`DEFECT-20261026-02`](#defect-20261026-02) | 🟠 P1 | Multi-Tenancy | `TenantName` persisted as empty object `{}` across MongoDB documents (`WorkTemplates`, `HolidayCalendars`) | `MongoDB `TenantName`` | [Evidence 06](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_06_tenantname_empty_object_compass.png) |
| [`DEFECT-20261026-03`](#defect-20261026-03) | 🟡 P2 | Audit Infrastructure | `CreatedBy` audit field stores plain email string instead of composite user identity object | `MongoDB Audit Fields` | [Evidence 04 & 05](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_05_createdby_plain_email_highlighted.png) |
| [`DEFECT-20261026-04`](#defect-20261026-04) | 🟠 P1 | API Contracts | `tenantName` still exposed in request body DTOs across 26 POST & PATCH APIs instead of auto-injected | `26 Controller Endpoints` | [Evidence 07](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_07_swagger_tenantname_still_present.png) |"""

new_block = """| [`DEFECT-20261026-01`](#defect-20261026-01) | 🟠 P1 | Cross-Service Sync | **[NOT FIXED]** Cross-service sync failure: `CompanyChecklist.WorkSchedulesCreated` remains `false` in `CompanySvc` | ``CompanySvc` Sync` | [Evidence 02](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_02_companiesmaster_checklist_false.png) |
| [`DEFECT-20261026-02`](#defect-20261026-02) | 🟠 P1 | Multi-Tenancy | **[NOT FIXED]** `TenantName` persisted as empty object `{}` in MongoDB (`WorkTemplates`, `HolidayCalendars`) | `MongoDB `TenantName`` | [Evidence 06](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_06_tenantname_empty_object_compass.png) |
| [`DEFECT-20261026-03`](#defect-20261026-03) | 🟡 P2 | Audit Infrastructure | **[NOT FIXED]** `CreatedBy` audit field stores plain email string instead of composite user identity object | `MongoDB Audit Fields` | [Evidence 04 & 05](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_05_createdby_plain_email_highlighted.png) |
| [`DEFECT-20261026-04`](#defect-20261026-04) | 🟠 P1 | API Contracts | **[NOT FIXED]** `tenantName` exposed in DTOs; client spoofing accepted with 200 OK across all 6 Work Template APIs | `26 Controller Endpoints` | [Evidence 07](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_07_swagger_tenantname_still_present.png) |"""

if old_block in content:
    content = content.replace(old_block, new_block)
    print("Replaced Section 2 matrix block for 26-Oct defects.")
else:
    print("Could not find old_block in content!")

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print(f"Updated {file_path} successfully.")

