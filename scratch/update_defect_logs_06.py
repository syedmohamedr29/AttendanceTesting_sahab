import sys
import re

sys.stdout.reconfigure(encoding='utf-8')

defect_log_path = "Defects/Attendance2_Master_Defect_Log.md"
report_path = "Attendance2_Defects_Gaps_and_Architecture_Inconsistencies_Report.md"

# 1. Update Defects/Attendance2_Master_Defect_Log.md
with open(defect_log_path, "r", encoding="utf-8") as f:
    log_content = f.read()

# Update counts in header if present
log_content = re.sub(r'Total Defects:\s*\*\*\d+\*\*', 'Total Defects: **60**', log_content)
log_content = re.sub(r'P1 Critical:\s*\*\*\d+\*\*', 'P1 Critical: **47**', log_content)

# Add row to Master Defect Table (right after DEFECT-20261105-04)
table_row = """| [`DEFECT-20261106-01`](#defect-20261106-01) | 🟠 P1 | Attendance Policy / Database Integrity | Client-Dictated `id` in POST Body Accepted into MongoDB; Duplicate Key Causes HTTP 500 Crash `MongoWriteException` Leaking DB Internals | ``POST /attpolicies/*`` | [Evidence 43](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_43_policy_duplicate_id_mongo_500_crash.png) |
"""
target_tbl_str = "| [`DEFECT-20261105-04`](#defect-20261105-04)"
if target_tbl_str in log_content:
    log_content = log_content.replace(target_tbl_str, table_row + target_tbl_str)

# Add detail section right after DEFECT-20261105-04 detail block
detail_section = """
---

### <a id="defect-20261106-01"></a>🔴 DEFECT-20261106-01: Client-Dictated `id` in POST Request Body Accepted into MongoDB; Duplicate Key Causes Unhandled HTTP 500 Crash `MongoWriteException` Leaking Database Index and Collection Names

| Field | Detail |
| :--- | :--- |
| **Defect ID** | `DEFECT-20261106-01` |
| **Severity** | 🟠 **P1 Critical** (Database Integrity Violation, Data Injection & Information Disclosure) |
| **API Endpoints** | `POST /api/companies/{companyId}/attpolicies/break`<br>`POST /api/companies/{companyId}/attpolicies/graceperiod`<br>`POST /api/companies/{companyId}/attpolicies/overtime` |
| **Target Microservice** | `SP.AttendanceSvc` (.NET 9) |
| **MongoDB Collection** | `Sahab > ERP.Attendance.Policies` |
| **Target Company Tested** | Attendance 6 (`3a249870-184c-0373-f344-015d602678d7`) |
| **Visual Evidence** | [Evidence 43: Client Dictated ID Duplicate Crash](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_43_policy_duplicate_id_mongo_500_crash.png) |

#### 1. Issue Description & Live Reproduction
1. In Swagger UI and schema definitions, `id` (GUID) is exposed as a writable property in the `POST` request body.
2. When a client explicitly submits a custom GUID (e.g. `"id": "40321957-cf6e-456f-a548-4e3f20e5acae"`), the backend accepts it and writes that exact GUID into MongoDB `_id: UUID("40321957-cf6e-456f-a548-4e3f20e5acae")`.
3. When the client transmits a POST request containing an `id` that already exists in the collection, the .NET service fails to handle the key collision, and MongoDB throws an unhandled `MongoWriteException: E11000 duplicate key error`.
4. The service crashes with **HTTP 500 Internal Server Error**, completely exposing internal database cluster schema, collection names, and index names to the external client.

#### 2. Request Payload (Duplicate ID Attempt)
```json
POST /api/companies/3a249870-184c-0373-f344-015d602678d7/attpolicies/break HTTP/1.1
Host: attendance2.dev.zoolwork.com
Authorization: Bearer eyJhbGciOi...
__tenant: Attendance
Content-Type: application/json

{
  "id": "40321957-cf6e-456f-a548-4e3f20e5acae",
  "name": {
    "en": "Duplicate ID Attempt"
  },
  "breaks": [
    {
      "name": "Lunch-Unique-99",
      "type": "Unpaid",
      "durationMinutes": 45
    }
  ]
}
```

#### 3. Actual Response Body (HTTP 500 Internal Server Error)
```json
HTTP/1.1 500 Internal Server Error
Content-Type: application/json; charset=utf-8

{
  "error": {
    "code": "MongoWriteException",
    "message": "A write operation resulted in an error. WriteError: { Category : \"DuplicateKey\", Code : 11000, Message : \"E11000 duplicate key error collection: Sahab.ERP.Attendance.Policies index: _id_ dup key: { _id: UUID(\"40321957-cf6e-456f-a548-4e3f20e5acae\") }\" }.",
    "details": null,
    "data": null,
    "validationErrors": null
  }
}
```

#### 4. MongoDB Document Persistence Proof (`DEV > Sahab > ERP.Attendance.Policies`)
```javascript
// Query in MongoDB Compass:
{ "_id": UUID("40321957-cf6e-456f-a548-4e3f20e5acae") }

// Persisted Document:
{
  "_id": UUID("40321957-cf6e-456f-a548-4e3f20e5acae"),
  "Type": 1,
  "Name": { "en": "Break ID Client Dictated" },
  "CompanyId": UUID("3a249870-184c-0373-f344-015d602678d7"),
  "CompanyName": { "en": "Attendance 6", "ar": "الحضور 6" },
  "TenantId": UUID("3a24741e-2667-1223-f12e-62a69fab3838"),
  "TenantName": {},
  "IsActive": true,
  "CreatedAt": ISODate("2026-11-06T05:42:03.584Z"),
  "CreatedBy": "syed.mohamed@comm-it.in"
}
```

#### 5. Security & Architectural Impact
- **ID Injection & Collision Attack:** Malicious or buggy clients can dictate database keys or intentionally cause HTTP 500 denial-of-service conditions by passing colliding GUIDs.
- **Information Disclosure:** Raw database collection name (`Sahab.ERP.Attendance.Policies`) and primary index name (`_id_`) are leaked in the error response.
- **Contract Ambiguity:** Clients are misled into believing they must generate GUIDs before creation.

#### 6. Recommended Fix
1. Remove `id` from all Policy Create DTOs (`CreateBreakPolicyDto`, `CreateGracePeriodPolicyDto`, `CreateOvertimePolicyDto`).
2. In Command Handlers (`CreateBreakPolicyCommandHandler`, etc.), strictly generate `_id = Guid.NewGuid()` server-side.
3. Catch any underlying `MongoWriteException` in the global exception filter and return a standardized, sanitized client error (`HTTP 400 Bad Request` or `HTTP 409 Conflict`).
"""

# Insert detail section before Evidence Screenshots Table
evidence_table_marker = "## 📸 Evidence Screenshots & Verification Artifacts"
if evidence_table_marker in log_content:
    log_content = log_content.replace(evidence_table_marker, detail_section + "\n" + evidence_table_marker)

# Add evidence 43 to Evidence table
evidence_row = """| ![DEFECT-20261106-01](../defect_evidence/evidence_43_policy_duplicate_id_mongo_500_crash.png) | **File:** `evidence_43_policy_duplicate_id_mongo_500_crash.png`<br>**Defect:** [`DEFECT-20261106-01`](#defect-20261106-01)<br>**Description:** Client-dictated `id` in POST body accepted into MongoDB `ERP.Attendance.Policies`; duplicate key throws unhandled HTTP 500 `MongoWriteException` leaking collection name. |
"""
ev_marker = "| ![DEFECT-20261105-04]"
if ev_marker in log_content:
    log_content = log_content.replace(ev_marker, evidence_row + ev_marker)

# Add to developer checklist
chk_item = "- [ ] **P1 (`DEFECT-20261106-01`):** In `SP.AttendanceSvc` policy create command handlers, remove `id` from Create DTOs and enforce server-side `_id = Guid.NewGuid()`. Catch any duplicate key write exceptions and return clean HTTP 400/409 instead of unhandled 500.\n"
chk_marker = "- [ ] **P1 (`DEFECT-20261105-04`):**"
if chk_marker in log_content:
    log_content = log_content.replace(chk_marker, chk_item + chk_marker)

with open(defect_log_path, "w", encoding="utf-8") as f:
    f.write(log_content)
print("Updated Defects/Attendance2_Master_Defect_Log.md successfully!")

# 2. Update Attendance2_Defects_Gaps_and_Architecture_Inconsistencies_Report.md
with open(report_path, "r", encoding="utf-8") as f:
    report_content = f.read()

report_content = re.sub(r'Total Tracked Defects:\s*\*\*\d+\*\*', 'Total Tracked Defects: **60**', report_content)
report_content = re.sub(r'P1 Critical:\s*\*\*\d+\*\*', 'P1 Critical: **47**', report_content)

with open(report_path, "w", encoding="utf-8") as f:
    f.write(report_content)
print("Updated Attendance2_Defects_Gaps_and_Architecture_Inconsistencies_Report.md successfully!")

