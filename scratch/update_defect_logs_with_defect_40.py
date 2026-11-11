import sys
import re

sys.stdout.reconfigure(encoding='utf-8')

# 1. Update Defects/Attendance2_Master_Defect_Log.md
master_path = 'Defects/Attendance2_Master_Defect_Log.md'
with open(master_path, 'r', encoding='utf-8') as f:
    master_text = f.read()

# Update total count from 56 to 57, and P2 count from 5 to 6
master_text = master_text.replace(
    "total of **56 defects and architecture gaps**",
    "total of **57 defects and architecture gaps**"
)

# Update Severity table P2 count
master_text = re.sub(
    r'\|\s*🟡\s*\*\*P2\s*\(Major\)\*\*\s*\|\s*\*\*5\*\*',
    '| 🟡 **P2 (Major)** | **6**',
    master_text
)

# Add row to Section 2: Quick-Reference Defect Matrix
# Insert after DEFECT-20261105-01
target_row = "| [`DEFECT-20261105-01`](#defect-20261105-01)"
new_matrix_row = "| [`DEFECT-20261105-02`](#defect-20261105-02) | 🟡 P2 | Attendance Policy / Architecture | `tenantName` and `id` exposed in request body DTOs across all Policy POST/PATCH APIs | ``POST / PATCH /attpolicies/*`` | [Evidence 40](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_40_swagger_policy_tenantname_id_in_request_body.png) |\n"

if target_row in master_text and "DEFECT-20261105-02" not in master_text:
    idx = master_text.find(target_row)
    line_end = master_text.find("\n", idx) + 1
    master_text = master_text[:line_end] + new_matrix_row + master_text[line_end:]
    print("Added DEFECT-20261105-02 to Section 2 Quick-Reference Matrix.")

# Add Deep-Dive in Section 4
deep_dive_text = """
### <a id="defect-20261105-02"></a>🟡 DEFECT-20261105-02: `tenantName` and `id` Exposed in OpenAPI / Swagger Request Body DTOs Across All Policy Endpoints (`POST` & `PATCH` for Break, Grace Period, Overtime) Instead of Dedicated Command DTOs
- **Severity:** 🟡 P2 (Major / Architecture & DTO Contract Flaw)
- **Target Routes:**
  - `POST /api/companies/{companyId}/attpolicies/break`
  - `POST /api/companies/{companyId}/attpolicies/graceperiod`
  - `POST /api/companies/{companyId}/attpolicies/overtime`
  - `PATCH /api/companies/{companyId}/attpolicies/break/{policyId}`
  - `PATCH /api/companies/{companyId}/attpolicies/graceperiod/{policyId}`
  - `PATCH /api/companies/{companyId}/attpolicies/overtime/{policyId}`
- **Target Microservice:** `SP.AttendanceSvc` (.NET 9 Web API)
- **Target MongoDB Collection:** `DEV > Sahab > ERP.Attendance.Policies`
- **Evidence Reference:** [Evidence 40 (`evidence_40_swagger_policy_tenantname_id_in_request_body.png`)](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_40_swagger_policy_tenantname_id_in_request_body.png)

#### Description & Root Cause
In `SP.AttendanceSvc`, the OpenAPI / Swagger contract and ASP.NET Core controller actions reuse the entity response DTOs (`GracePeriodPolicyDto`, `BreakPolicyDto`, `OvertimePolicyDto`) directly as the request body parameter types for both `POST` (creation) and `PATCH` (update) endpoints.

Consequently, Swagger UI displays client-writable fields:
1. `"id": "3fa85f64-5717-4562-b3fc-2c963f66afa6"`
2. `"tenantName": {"additionalProp1": "string", "additionalProp2": "string", "additionalProp3": "string"}`

#### Architectural & Production Impact
1. **Client Should Not Send `tenantName`:** In multi-tenant architecture, `tenantName` (and `TenantId`) are system-owned context properties. They must be resolved and pre-populated server-side from `ICurrentTenant` or the authenticated JWT claims. Requiring or exposing `tenantName` in request DTOs violates tenant encapsulation and enables tenant spoofing (`DEFECT-20261026-04`).
2. **Client Should Not Send `id`:** The entity identifier `_id` is generated server-side (UUIDv4) upon creation. Exposing `id` in `POST` body confuses API consumers into thinking client-supplied IDs are honored.
3. **Server Pre-Population Requirement:** When a policy is created omitting `tenantName` and `id`, the backend must automatically pre-populate `TenantName: {"en": "<tenant>", "ar": "..."}` and `TenantId: UUID(...)` in MongoDB Compass collection `ERP.Attendance.Policies`.
4. **Unified DTO Anti-Pattern:** Using the same DTO for commands (`Create`/`Update`) and queries (`Get`) creates parameter pollution and breaks API contract versioning.

#### Evidence
| Screenshot | Description |
| :--- | :--- |
| ![DEFECT-20261105-02](../defect_evidence/evidence_40_swagger_policy_tenantname_id_in_request_body.png) | **File:** `evidence_40_swagger_policy_tenantname_id_in_request_body.png`<br><br>[🔍 Click to Open Full-Resolution Image](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_40_swagger_policy_tenantname_id_in_request_body.png)<br><br>*Swagger UI Proof: `POST /api/companies/{companyId}/attpolicies/graceperiod` exposes client-writable `id` and `tenantName` in request body schema.* |

#### Developer Remediation Steps
1. Introduce dedicated command DTOs:
   - `CreateBreakPolicyDto`, `CreateGracePeriodPolicyDto`, `CreateOvertimePolicyDto` (remove `id`, `tenantName`, `isActive`).
   - `UpdateBreakPolicyDto`, `UpdateGracePeriodPolicyDto`, `UpdateOvertimePolicyDto` (remove `id`, `tenantName`, `companyId`, `tenantId`).
2. In command handlers, inject `ICurrentTenant` and pre-populate `TenantName` and `TenantId` server-side before persisting into `ERP.Attendance.Policies`.
3. In test cases, strictly omit `tenantName` and `id` from request payloads, and verify server pre-population in MongoDB Compass.
"""

# Insert Deep-Dive before Section 5
s5_marker = "## 5. Architectural Gaps & Non-Functional Inconsistencies"
if s5_marker in master_text and "defect-20261105-02" not in master_text:
    s5_idx = master_text.find(s5_marker)
    master_text = master_text[:s5_idx] + deep_dive_text + "\n---\n\n" + master_text[s5_idx:]
    print("Added DEFECT-20261105-02 deep-dive before Section 5.")

# Add to Section 7: Photographic Evidence Directory
evidence_row = "| ![DEFECT-20261105-02](../defect_evidence/evidence_40_swagger_policy_tenantname_id_in_request_body.png) | **File:** `evidence_40_swagger_policy_tenantname_id_in_request_body.png`<br><br>[🔍 Click to Open Full-Resolution Image](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_40_swagger_policy_tenantname_id_in_request_body.png)<br><br>*Swagger UI Proof: `POST /api/companies/{companyId}/attpolicies/graceperiod` exposes client-writable `id` and `tenantName` in request body schema.* |\n"

ev_marker = "evidence_39_companyname_empty_object_compass.jpg) |"
if ev_marker in master_text and "evidence_40" not in master_text:
    idx = master_text.find(ev_marker)
    line_end = master_text.find("\n", idx) + 1
    master_text = master_text[:line_end] + evidence_row + master_text[line_end:]
    print("Added Evidence 40 to Section 7 Evidence Gallery.")

# Add to Section 8: Checklist
chk_marker = "- [ ] **P1 (`DEFECT-20261105-01`):**"
new_chk_item = "- [ ] **P2 (`DEFECT-20261105-02`):** In `SP.AttendanceSvc`, create dedicated `Create*PolicyDto` and `Update*PolicyDto` removing `id` and `tenantName` from request body schemas. Pre-populate `TenantName` and `TenantId` server-side from `ICurrentTenant` context into MongoDB `ERP.Attendance.Policies`.\n"
if chk_marker in master_text and "DEFECT-20261105-02" not in master_text:
    idx = master_text.find(chk_marker)
    master_text = master_text[:idx] + new_chk_item + master_text[idx:]
    print("Added DEFECT-20261105-02 to Section 8 Checklist.")

with open(master_path, 'w', encoding='utf-8') as f:
    f.write(master_text)
print(f"Successfully updated {master_path}!")

