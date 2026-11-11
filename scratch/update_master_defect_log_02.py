import sys

sys.stdout.reconfigure(encoding='utf-8')

log_path = 'Defects/Attendance2_Master_Defect_Log.md'
with open(log_path, 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Update Executive Summary counts
exec_summary_target = "| **TOTAL** | **56** |"
exec_summary_replace = "| **TOTAL** | **57** |"
if exec_summary_target in text:
    text = text.replace(exec_summary_target, exec_summary_replace)
    print("Updated Total count in Executive Summary table.")

p2_count_target = "| 🟡 **P2 (Major)** | **4** |"
p2_count_replace = "| 🟡 **P2 (Major)** | **6** |"
if p2_count_target in text:
    text = text.replace(p2_count_target, p2_count_replace)
    print("Updated P2 count in Executive Summary table.")

# 2. Add Detailed Deep Dive before defect-20261103-16
defect_02_deep_dive = """---

### <a id="defect-20261105-02"></a>🟡 DEFECT-20261105-02: `tenantName` and `id` Exposed in OpenAPI / Swagger Request Body Schema Across All Policy Endpoints (`POST` & `PATCH`) Instead of Dedicated Command DTOs
- **Severity:** 🟡 P2 (Major / Architecture & DTO Contract Flaw)
- **Target Routes:**
  - `POST /api/companies/{companyId}/attpolicies/break`
  - `POST /api/companies/{companyId}/attpolicies/graceperiod`
  - `POST /api/companies/{companyId}/attpolicies/overtime`
  - `PATCH /api/companies/{companyId}/attpolicies/break/{policyId}`
  - `PATCH /api/companies/{companyId}/attpolicies/graceperiod/{policyId}`
  - `PATCH /api/companies/{companyId}/attpolicies/overtime/{policyId}`
- **Target Collection:** `Sahab.ERP.Attendance.Policies`
- **Controller:** `GracePeriodPolicyController`, `BreakPolicyController`, `OvertimePolicyController`
- **Discovered Date:** 05 November 2026 | **Status:** Open / Unresolved
- **Evidence Reference:** [Evidence 40 (`evidence_40_swagger_policy_tenantname_id_in_request_body.png`)](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_40_swagger_policy_tenantname_id_in_request_body.png)

#### 1. Problem Summary
During API documentation audit and Swagger inspection on `https://attendance2.dev.zoolwork.com`, it was discovered that all Attendance Policy `POST` and `PATCH` endpoints expose `id` and a nested dictionary `tenantName` in their OpenAPI / Swagger request body schema:
```json
{
  "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
  "name": {
    "additionalProp1": "string",
    "additionalProp2": "string",
    "additionalProp3": "string"
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

#### 2. Root Cause Analysis
1. **Unified DTO Anti-Pattern:** The backend microservice `SP.AttendanceSvc` directly reuses entity response DTOs (`GracePeriodPolicyDto`, `BreakPolicyDto`, `OvertimePolicyDto`) as the request body parameter types (`[FromBody] GracePeriodPolicyDto dto`) for mutation endpoints (`POST` and `PATCH`).
2. **Missing Command Separation:** In CQRS / clean architecture, mutation requests must use dedicated command DTOs (`CreateGracePeriodPolicyDto`, `UpdateGracePeriodPolicyDto`) that expose only client-writable attributes.
3. **Multi-Tenancy Encapsulation Violation:** `tenantName` (and `TenantId`) are strictly server-side context attributes resolved from the authenticated JWT token / `ICurrentTenant`. The client must NEVER pass `tenantName` in a request payload. Exposing it in the Swagger schema prompts API consumers to submit spoofed or erroneous tenant names, creating potential tenant impersonation risks (`DEFECT-20261026-04`).
4. **Server Pre-Population Contract:** The backend domain handler must automatically pre-populate `TenantName: {"en": "Attendance", ...}`, `TenantId: UUID(...)`, and generate `_id: UUID(...)` server-side when persisting to MongoDB `Sahab.ERP.Attendance.Policies`.

#### 3. Reproduction Steps (Postman / Swagger)
1. Open Swagger UI at `https://attendance2.dev.zoolwork.com/swagger/index.html`.
2. Expand `POST /api/companies/{companyId}/attpolicies/graceperiod`.
3. Observe the generated request body schema under `application/json`.
4. Notice that `"id"` and `"tenantName"` are displayed as editable fields in the request template.

#### 4. Photographic Proof from Swagger UI
| Visual Evidence | Description |
| :--- | :--- |
| ![DEFECT-20261105-02](../defect_evidence/evidence_40_swagger_policy_tenantname_id_in_request_body.png) | **File:** `evidence_40_swagger_policy_tenantname_id_in_request_body.png`<br><br>[🔍 Click to Open Full-Resolution Image](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_40_swagger_policy_tenantname_id_in_request_body.png)<br><br>*Evidence 40: Swagger UI live inspection of `POST /api/companies/{companyId}/attpolicies/graceperiod`. Highlighted in red: `id` and `tenantName` exposed in the request body schema.* |

#### 5. Developer Remediation (.NET 9 C#)
1. Create separate Command DTOs:
   ```csharp
   public class CreateGracePeriodPolicyDto
   {
       public MultilingualString Name { get; set; } = new();
       public int LateCheckInGraceMinutes { get; set; }
       public int EarlyCheckOutGraceMinutes { get; set; }
       public int DeviationThreshold { get; set; }
       public string DeviationPeriod { get; set; } = "NotApplicable";
       public string DeductLeaveFrom { get; set; } = "NotApplicable";
       public double DeductionDays { get; set; }
   }
   ```
2. Update Controller Action Signatures:
   ```csharp
   [HttpPost("graceperiod")]
   public async Task<IActionResult> CreateGracePeriodPolicy(
       [FromRoute] Guid companyId,
       [FromBody] CreateGracePeriodPolicyDto dto)
   {
       // Backend automatically stamps tenant context from authenticated claims
       var tenantName = _currentTenant.Name; // Pre-populated server-side
       var tenantId = _currentTenant.Id;     // Pre-populated server-side
       ...
   }
   ```
3. Add `[JsonIgnore]` on internal properties of response DTOs or enforce command/query DTO separation.

"""

marker = '### <a id="defect-20261103-16">'
if marker in text and 'id="defect-20261105-02"' not in text[30000:]:
    idx = text.find(marker)
    text = text[:idx] + defect_02_deep_dive + "\n" + text[idx:]
    print("Added DEFECT-20261105-02 Detailed Deep Dive.")

# 3. Add to Section 8 Developer Checklist under Priority 2
chk_target = "### Priority 2: Audit, Swagger & DX Fixes"
chk_item = """### Priority 2: Audit, Swagger & DX Fixes
- [ ] **P2 (`DEFECT-20261105-02`):** In `SP.AttendanceSvc`, create dedicated `Create*PolicyDto` and `Update*PolicyDto` removing `id` and `tenantName` from request body schemas. Pre-populate `TenantName` and `TenantId` server-side from `ICurrentTenant` context into MongoDB `ERP.Attendance.Policies`."""

if chk_target in text and "DEFECT-20261105-02" not in text[100000:]:
    text = text.replace(chk_target, chk_item, 1)
    print("Added DEFECT-20261105-02 to Section 8 Priority 2 Checklist.")

with open(log_path, 'w', encoding='utf-8') as f:
    f.write(text)

print(f"Successfully updated {log_path}!")

