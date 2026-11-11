import sys
import re

sys.stdout.reconfigure(encoding='utf-8')

report_path = 'Attendance2_Defects_Gaps_and_Architecture_Inconsistencies_Report.md'
with open(report_path, 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Update top banner summary
top_banner_search = "Critical Defect Logged Today (05 November 2026): DEFECT-20261105-01"
top_banner_replace = "Defects Logged Today (05 November 2026): DEFECT-20261105-01 & DEFECT-20261105-02"
text = text.replace(top_banner_search, top_banner_replace)

# 2. Add DEFECT-20261105-02 to the top banner alert table
tbl_marker = "| **`DEFECT-20261105-01`** | **P1 (Master Data Integrity)**"
new_tbl_row = "| **`DEFECT-20261105-02`** | **P2 (Architecture & DTO Flaw)** | **Attendance Policies Module**<br>(API Contracts) | `ERP.Attendance.Policies`<br>(`POST` & `PATCH` `/attpolicies/*`) | **Policy DTOs Expose `tenantName` & `id` in Swagger Request Body:** Request body schemas reuse entity DTOs, exposing client-writable `tenantName` and `id`. Client must not send `tenantName`; server must pre-populate `TenantName` and `TenantId` in MongoDB. | [Evidence 40](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_40_swagger_policy_tenantname_id_in_request_body.png) |\n"

if tbl_marker in text and "DEFECT-20261105-02" not in text:
    idx = text.find(tbl_marker)
    line_end = text.find("\n", idx) + 1
    text = text[:line_end] + new_tbl_row + text[line_end:]
    print("Added DEFECT-20261105-02 to Top Banner Table.")

# 3. Add Deep-Dive section after DEFECT-20261105-01 deep-dive
deep_dive = """
---

### Defect `DEFECT-20261105-02`: `tenantName` and `id` Exposed in OpenAPI / Swagger Request Body Schema Across All Attendance Policy Endpoints (`POST` & `PATCH` for Break, Grace Period, Overtime) Instead of Dedicated Command DTOs
- **Severity:** 🟡 **P2 (Major / Architecture & DTO Contract Flaw)**
- **Affected Endpoints:**
  - `POST /api/companies/{companyId}/attpolicies/break`
  - `POST /api/companies/{companyId}/attpolicies/graceperiod`
  - `POST /api/companies/{companyId}/attpolicies/overtime`
  - `PATCH /api/companies/{companyId}/attpolicies/break/{policyId}`
  - `PATCH /api/companies/{companyId}/attpolicies/graceperiod/{policyId}`
  - `PATCH /api/companies/{companyId}/attpolicies/overtime/{policyId}`
- **Affected MongoDB Collection:** `DEV > Sahab > ERP.Attendance.Policies`
- **Evidence Reference:** [Evidence 40 (`evidence_40_swagger_policy_tenantname_id_in_request_body.png`)](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_40_swagger_policy_tenantname_id_in_request_body.png)

#### Detailed Technical Analysis
In `SP.AttendanceSvc`, the OpenAPI / Swagger contract and ASP.NET Core controller actions reuse the entity response DTOs (`GracePeriodPolicyDto`, `BreakPolicyDto`, `OvertimePolicyDto`) directly as the request body parameter types for both `POST` (creation) and `PATCH` (update) endpoints.

Consequently, Swagger UI displays client-writable fields:
```json
{
  "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
  "name": {
    "additionalProp1": "string"
  },
  "isActive": true,
  "tenantName": {
    "additionalProp1": "string",
    "additionalProp2": "string",
    "additionalProp3": "string"
  },
  "lateCheckInGraceMinutes": 0,
  "earlyCheckOutGraceMinutes": 0,
  "deviationThreshold": 0,
  "deviationPeriod": "NotApplicable",
  "deductLeaveFrom": "NotApplicable",
  "deductionDays": 0
}
```

#### Architectural & Production Impact
1. **Client Should Not Send `tenantName`:** In multi-tenant architecture, `tenantName` (and `TenantId`) are system-owned context properties. They must be resolved and pre-populated server-side from `ICurrentTenant` or the authenticated JWT claims. Requiring or exposing `tenantName` in request DTOs violates tenant encapsulation and creates a tenant spoofing vulnerability (`DEFECT-20261026-04`).
2. **Client Should Not Send `id`:** The entity identifier `_id` is generated server-side (UUIDv4) upon creation. Exposing `id` in `POST` body confuses API consumers into thinking client-supplied IDs are honored.
3. **Server Pre-Population Requirement:** When a policy is created omitting `tenantName` and `id`, the backend must automatically pre-populate `TenantName: {"en": "<tenant>", "ar": "..."}` and `TenantId: UUID(...)` in MongoDB Compass collection `ERP.Attendance.Policies`.
4. **Unified DTO Anti-Pattern:** Using the same DTO for commands (`Create`/`Update`) and queries (`Get`) creates parameter pollution and breaks API contract versioning.

#### Evidence
| Screenshot | Description |
| :--- | :--- |
| ![DEFECT-20261105-02](defect_evidence/evidence_40_swagger_policy_tenantname_id_in_request_body.png) | **Evidence 40:** Live Swagger UI inspection of `POST /api/companies/{companyId}/attpolicies/graceperiod`. Highlighted in red circle: `tenantName` object and client-supplied `id` exposed in request body schema. |

#### Developer Remediation Steps
1. Introduce dedicated command DTOs:
   - `CreateBreakPolicyDto`, `CreateGracePeriodPolicyDto`, `CreateOvertimePolicyDto` (remove `id`, `tenantName`, `isActive`).
   - `UpdateBreakPolicyDto`, `UpdateGracePeriodPolicyDto`, `UpdateOvertimePolicyDto` (remove `id`, `tenantName`, `companyId`, `tenantId`).
2. In command handlers, inject `ICurrentTenant` and pre-populate `TenantName` and `TenantId` server-side before persisting into `ERP.Attendance.Policies`.
3. In test cases, strictly omit `tenantName` and `id` from request payloads, and verify server pre-population in MongoDB Compass.
"""

target_sec = "### Defect `DEFECT-20261105-01`:"
if target_sec in text and "DEFECT-20261105-02" not in text:
    # Find end of DEFECT-20261105-01 section
    next_sec_marker = "## Part 4:"
    if next_sec_marker in text:
        idx = text.find(next_sec_marker)
        text = text[:idx] + deep_dive + "\n\n" + text[idx:]
        print("Added DEFECT-20261105-02 deep-dive before Part 4.")

# 4. Add to Part 5: Actionable Developer Checklist
chk_marker = "- [ ] **P1 (`DEFECT-20261105-01`):**"
new_chk_item = "- [ ] **P2 (`DEFECT-20261105-02`):** In `SP.AttendanceSvc`, create dedicated `Create*PolicyDto` and `Update*PolicyDto` removing `id` and `tenantName` from request body schemas. Pre-populate `TenantName` and `TenantId` server-side from `ICurrentTenant` context into MongoDB `ERP.Attendance.Policies`.\n"
if chk_marker in text and "DEFECT-20261105-02" not in text:
    idx = text.find(chk_marker)
    text = text[:idx] + new_chk_item + text[idx:]
    print("Added DEFECT-20261105-02 to Part 5 Checklist.")

with open(report_path, 'w', encoding='utf-8') as f:
    f.write(text)
print(f"Successfully updated {report_path}!")

