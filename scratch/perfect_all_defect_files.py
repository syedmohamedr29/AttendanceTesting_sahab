import sys
import re

sys.stdout.reconfigure(encoding='utf-8')

defect_log_path = "Defects/Attendance2_Master_Defect_Log.md"
report_path = "Attendance2_Defects_Gaps_and_Architecture_Inconsistencies_Report.md"

# ==============================================================================
# 1. UPDATE Defects/Attendance2_Master_Defect_Log.md
# ==============================================================================
with open(defect_log_path, "r", encoding="utf-8") as f:
    log_text = f.read()

# 1a. Ensure Photographic Evidence table has Evidence 45
ev45_entry = """| ![DEFECT-20261106-03](../defect_evidence/evidence_45_api_request_body_invalid_structure_id_tenantname_comparison.png) | **File:** `evidence_45_api_request_body_invalid_structure_id_tenantname_comparison.png`<br>**Defect:** [`DEFECT-20261106-03`](#defect-20261106-03)<br>**Description:** Direct visual comparison showing invalid request body structure: `id` (`00000000-0000-0000-0000-000000000000`) and `tenantName` (`{"en": "Attendance", "ar": "Attendance"}`) must both be removed from API request DTOs. Entity IDs are strictly server-generated and tenant context is derived from JWT authentication headers. |
"""
if "evidence_45_api_request_body_invalid_structure" not in log_text:
    target_ev = "| ![DEFECT-20261106-01-ATT7](../defect_evidence/evidence_44_attendance7_reverification_defects_compass.png)"
    if target_ev in log_text:
        log_text = log_text.replace(target_ev, ev45_entry + target_ev)
        print("Inserted Evidence 45 into Master Defect Log Photographic Proof table.")

# 1b. Ensure Checklist has DEFECT-20261106-03 and DEFECT-20261106-02
chk_03 = "- [ ] **P1 (`DEFECT-20261106-03`):** In `SP.AttendanceSvc` DTO models, completely remove `id` and `tenantName` properties from all Policy Create and Update request DTOs (`CreateBreakPolicyDto`, `CreateGracePeriodPolicyDto`, `CreateOvertimePolicyDto`). Client payloads must strictly omit both fields.\n"
chk_02 = "- [ ] **P1 (`DEFECT-20261106-02`):** In `CompanyServiceIntegrationHandler.cs`, wrap `CompanySvc` client calls in a resilient guard and map lookup failures to clean HTTP 404 Not Found (`Cit.Attendance:CompanyNotFound`) instead of unhandled HTTP 500 `HttpRequestException`.\n"

target_chk_head = "### Priority 1: Critical Domain & Architecture Fixes\n"
if "DEFECT-20261106-03`):** In `SP.AttendanceSvc` DTO models" not in log_text:
    log_text = log_text.replace(target_chk_head, target_chk_head + chk_03 + chk_02)
    print("Inserted DEFECT-20261106-03 & 02 into Master Defect Log Priority 1 checklist.")

with open(defect_log_path, "w", encoding="utf-8") as f:
    f.write(log_text)


# ==============================================================================
# 2. UPDATE Attendance2_Defects_Gaps_and_Architecture_Inconsistencies_Report.md
# ==============================================================================
with open(report_path, "r", encoding="utf-8") as f:
    rep_text = f.read()

# 2a. Update TOC Part 3H title
rep_text = re.sub(
    r'\* \[.*Part 3H: Defects Identified & Live Verified on 05 & 06 November 2026.*?\n',
    '* [**🏢 Part 3H: Defects Identified & Live Verified on 05 & 06 November 2026 (ATTENDANCE POLICY MODULE: ATTENDANCE 6 & 7)**](#-part-3h-defects-identified--live-verified-on-05--06-november-2026--attendance-policy-module-live-verification-on-attendance-6--attendance-7) — *Policy Lifecycles, Negative RateFormula (-1.5), Duplicate Key 500 Crash, Empty TenantName & Invalid Request Body Structure (7 Defects)*\n',
    rep_text
)

# 2b. Update Part 3H Summary Table
p3h_tbl_replacement = """### Summary Matrix: Attendance Policy Defects (Live Verified 05-06 Nov 2026)

| Defect ID | Severity | Module & Endpoint | Summary / Behavior | Target Companies Verified | Live Proof & Evidence |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **`DEFECT-20261106-03`** | 🟠 P1 Critical | `POST / PATCH /attpolicies/*` | Invalid API request body structure: `id` and `tenantName` must be stripped from all policy request DTOs | Attendance 6 & Attendance 7 | [Evidence 45](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_45_api_request_body_invalid_structure_id_tenantname_comparison.png) |
| **`DEFECT-20261106-02`** | 🟠 P1 Critical | `POST /attpolicies/*` | Calling policy endpoint with non-existent companyId returns unhandled HTTP 500 instead of HTTP 404 | Attendance 7 (`3a249870...`) | Logged in Part 3H |
| **`DEFECT-20261106-01`** | 🟠 P1 Critical | `POST /attpolicies/*` | Client-dictated `id` in POST request body accepted; duplicate key collision causes unhandled HTTP 500 MongoWriteException | Attendance 6 & Attendance 7 | [Evidence 43](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_43_policy_duplicate_id_mongo_500_crash.png), [Evidence 44](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_44_attendance7_reverification_defects_compass.png) |
| **`DEFECT-20261105-04`** | 🟠 P1 Critical | `POST / PATCH /attpolicies/*` | `TenantName` persists as `Object (empty)` `{}` in MongoDB `ERP.Attendance.Policies` | Attendance 6 & Attendance 7 | [Evidence 42](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_42_policy_tenantname_empty_object_compass.png), [Evidence 44](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_44_attendance7_reverification_defects_compass.png) |
| **`DEFECT-20261105-03`** | 🟠 P1 Critical | `POST /attpolicies/overtime` | API accepts negative overtime rate multiplier (`rateFormula: -1.5`) with HTTP 200 OK | Attendance 6 & Attendance 7 | [Evidence 41](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_41_overtime_policy_negative_rateformula_accepted_compass.png), [Evidence 44](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_44_attendance7_reverification_defects_compass.png) |
| **`DEFECT-20261105-02`** | 🟡 P2 Major | `POST / PATCH /attpolicies/*` | Swagger UI request body schema defect: displays client-writable `id` and `tenantName` | Attendance 6 & Attendance 7 | [Evidence 40](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_40_swagger_policy_tenantname_id_in_request_body.png) |
| **`DEFECT-20261105-01`** | 🟡 P2 Major | `GET /attpolicies/{policyId}` | Querying non-existent policy GUID returns HTTP 400 Bad Request instead of REST standard HTTP 404 Not Found | Attendance 6 & Attendance 7 | Verified on Att 6 & Att 7 |
"""

old_tbl_pattern = r'### Summary Matrix: Attendance Policy Defects \(Live Verified 05-06 Nov 2026\)\n\n\| Defect ID \|.*?\| \*\*`DEFECT-20261106-02`\*\*.*?\|\n'
rep_text = re.sub(old_tbl_pattern, p3h_tbl_replacement, rep_text, flags=re.DOTALL)
print("Updated Part 3H Summary Matrix table in Architecture Report.")

# 2c. Update Part 3H Deep Dive for DEFECT-20261106-03 with full side-by-side comparison
full_p3h_deepdive_03 = """#### Defect `DEFECT-20261106-03`: Invalid API Request Body Structure — `id` and `tenantName` Exposed in Request DTOs Across All Policy APIs; Both Fields Must Be Stripped from Client Payloads

- **Severity:** 🟠 **P1 Critical** (API Contract Architecture Violation, Invalid Request Structure & Multi-Tenant Security)
- **Affected Endpoints:** `POST & PATCH /api/companies/{companyId}/attpolicies/break`, `.../graceperiod`, `.../overtime`
- **Target Microservice:** `SP.AttendanceSvc` (.NET 9)
- **Target Companies Verified:** Attendance 6 (`3a249870...`), Attendance 7 (`3a249870-c8ae...`)
- **Visual Evidence:** [Evidence 45: API Request Body Invalid Structure Comparison](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_45_api_request_body_invalid_structure_id_tenantname_comparison.png)

##### 1. Problem Description & Direct Evidence Analysis
Direct inspection of Swagger contracts and API client payloads (captured in [Evidence 45](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_45_api_request_body_invalid_structure_id_tenantname_comparison.png)) reveals an invalid request body design structure:

1. **`id` Must Be Removed from Request Body:**
   - The API DTO expects `id: "00000000-0000-0000-0000-000000000000"` or client-dictated GUIDs in POST bodies.
   - **Why this structure is invalid:** Entity IDs are strictly server-managed identifiers (`Guid.NewGuid()`). Exposing `id` in request DTOs forces callers to transmit dummy zero-GUIDs or custom GUIDs, directly triggering unhandled `MongoWriteException: E11000 duplicate key error` HTTP 500 crashes on duplicate key collisions (`DEFECT-20261106-01`). In PATCH/PUT APIs, the entity ID belongs in the URL route, not the payload body.
2. **`tenantName` Must Be Removed from Request Body:**
   - The API DTO expects `"tenantName": { "en": "Attendance", "ar": "Attendance" }` in client request payloads.
   - **Why this structure is invalid:** In multi-tenant cloud architecture, tenant identity is derived strictly from the authenticated token or `__tenant` context header. Forcing the client to transmit `tenantName` is redundant, error-prone, and opens an anti-spoofing security vector (`TC-POL-SEC-12`). Furthermore, backend command handlers fail to map it, leaving `TenantName: {}` empty in MongoDB (`DEFECT-20261105-04`).

##### 2. Side-by-Side Request Body Structure Comparison (Captured in Evidence 45)

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

##### 3. Root Cause Analysis
`CreateBreakPolicyDto`, `CreateGracePeriodPolicyDto`, and `CreateOvertimePolicyDto` in `SP.AttendanceSvc` include properties for `Id` (Guid) and `TenantName` (`MultilingualString`). ASP.NET Core model binding exposes these properties in Swagger OpenAPI specifications, forcing clients to construct malformed payloads.

##### 4. Developer Action & Remediation
1. **Remove `Id` Property:** Strip `public Guid Id { get; set; }` from all Policy Create/Update request DTOs.
2. **Remove `TenantName` Property:** Strip `public MultilingualString TenantName { get; set; }` from all Policy Create/Update request DTOs.
3. **Server Auto-Population:**
   - In command handlers, generate `_id = Guid.NewGuid()`.
   - Resolve `TenantName` server-side from `_currentTenant.Name` and `_currentTenant.ArabicName`.
"""

old_deepdive_03_pattern = r'#### Defect `DEFECT-20261106-03`:.*?- \*\*Resolution:\*\* Remove both `id` and `tenantName` from all Policy Create/Update request body DTOs\.\n'
rep_text = re.sub(old_deepdive_03_pattern, full_p3h_deepdive_03 + "\n", rep_text, flags=re.DOTALL)
print("Updated DEFECT-20261106-03 Deep-Dive in Architecture Report.")

# 2d. Update Day 7 Checklist
d7_chk_03 = "- [ ] **P1 (`DEFECT-20261106-03`):** In `SP.AttendanceSvc` DTO models, completely remove `id` and `tenantName` properties from all Policy Create and Update request DTOs (`CreateBreakPolicyDto`, `CreateGracePeriodPolicyDto`, `CreateOvertimePolicyDto`). Client payloads must omit both fields.\n"
d7_target_head = "### 📅 Day 7: 05 & 06 November 2026 Checklist (Attendance Policy Module)\n"
if "DEFECT-20261106-03`):** In `SP.AttendanceSvc` DTO models" not in rep_text:
    rep_text = rep_text.replace(d7_target_head, d7_target_head + d7_chk_03)
    print("Inserted DEFECT-20261106-03 into Day 7 checklist in Architecture Report.")

with open(report_path, "w", encoding="utf-8") as f:
    f.write(rep_text)

print("\n=== COMPLETED PERFECTING MARKDOWN FILES ===")
