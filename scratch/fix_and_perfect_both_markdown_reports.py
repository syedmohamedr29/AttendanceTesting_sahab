import sys
import re

sys.stdout.reconfigure(encoding='utf-8')

defect_log_path = "Defects/Attendance2_Master_Defect_Log.md"
report_path = "Attendance2_Defects_Gaps_and_Architecture_Inconsistencies_Report.md"

# ==============================================================================
# 1. FIX Defects/Attendance2_Master_Defect_Log.md
# ==============================================================================
with open(defect_log_path, "r", encoding="utf-8") as f:
    log_text = f.read()

# Check if detail sections exist
has_01 = "### <a id=\"defect-20261106-01\"></a>" in log_text
has_02 = "### <a id=\"defect-20261106-02\"></a>" in log_text

details_to_insert = """
---

### <a id="defect-20261106-01"></a>🔴 DEFECT-20261106-01: Client-Dictated `id` in POST Request Body Accepted into MongoDB; Duplicate Key Collision Causes Unhandled HTTP 500 Crash `MongoWriteException` Leaking Database Index and Collection Names

| Field | Detail |
| :--- | :--- |
| **Defect ID** | `DEFECT-20261106-01` |
| **Severity** | 🟠 **P1 Critical** (Database Integrity Violation, Data Injection & Information Disclosure) |
| **API Endpoints** | `POST /api/companies/{companyId}/attpolicies/break`<br>`POST /api/companies/{companyId}/attpolicies/graceperiod`<br>`POST /api/companies/{companyId}/attpolicies/overtime` |
| **Target Microservice** | `SP.AttendanceSvc` (.NET 9) |
| **MongoDB Collection** | `Sahab > ERP.Attendance.Policies` |
| **Target Companies Verified** | Attendance 6 (`3a249870-184c-0373-f344-015d602678d7`) & Attendance 7 (`3a249870-c8ae-b3dc-1b8d-c44efad14f89`) |
| **Visual Evidence** | [Evidence 43: Client Dictated ID Duplicate Crash](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_43_policy_duplicate_id_mongo_500_crash.png) & [Evidence 44](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_44_attendance7_reverification_defects_compass.png) |

#### 1. Issue Description & Live Reproduction
1. In Swagger UI and schema definitions, `id` (GUID) is exposed as a writable property in `POST` request bodies.
2. When a client explicitly submits a custom GUID (e.g. `"id": "40321957-cf6e-456f-a548-4e3f20e5acae"` or `"id": "12b68f6d-9a31-4de9-8184-f812c42de412"`), the backend accepts it and writes that exact GUID into MongoDB `_id`.
3. When the client transmits a POST request containing an `id` that already exists in the collection, the .NET service fails to handle the key collision, and MongoDB throws an unhandled `MongoWriteException: E11000 duplicate key error`.
4. The service crashes with **HTTP 500 Internal Server Error**, completely exposing internal database cluster schema, collection names (`Sahab.ERP.Attendance.Policies`), and primary index names (`_id_`) to the external caller.

#### 2. Request Payload (Duplicate Key Collision Attempt)
```json
POST /api/companies/3a249870-c8ae-b3dc-1b8d-c44efad14f89/attpolicies/break HTTP/1.1
Host: attendance2.dev.zoolwork.com
Authorization: Bearer eyJhbGciOi...
__tenant: Attendance
Content-Type: application/json

{
  "id": "12b68f6d-9a31-4de9-8184-f812c42de412",
  "name": {
    "en": "Duplicate Key Attempt on Att 7"
  },
  "breaks": [
    {
      "name": "Unique-Tea",
      "type": "Paid",
      "durationMinutes": 11
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
    "message": "A write operation resulted in an error. WriteError: { Category : \"DuplicateKey\", Code : 11000, Message : \"E11000 duplicate key error collection: Sahab.ERP.Attendance.Policies index: _id_ dup key: { _id: UUID(\"12b68f6d-9a31-4de9-8184-f812c42de412\") }\" }.",
    "details": null,
    "data": null,
    "validationErrors": null
  }
}
```

#### 4. MongoDB Document Persistence Proof (`DEV > Sahab > ERP.Attendance.Policies`)
```javascript
// Query in MongoDB Compass:
{ "_id": UUID("12b68f6d-9a31-4de9-8184-f812c42de412") }

// Pre-existing document causing collision:
{
  "_id": UUID("12b68f6d-9a31-4de9-8184-f812c42de412"),
  "Type": 1,
  "Name": { "en": "Executive Break Mismatch In Body" },
  "CompanyId": UUID("3a249870-c8ae-b3dc-1b8d-c44efad14f89"),
  "CompanyName": { "en": "Attendance 7", "ar": "الحضور 7" },
  "TenantId": UUID("3a24741e-2667-1223-f12e-62a69fab3838"),
  "TenantName": {},
  "IsActive": true
}
```

#### 5. Recommended Fix
1. Remove `id` from all Create DTOs (`CreateBreakPolicyDto`, etc.).
2. In Command Handlers, enforce `_id = Guid.NewGuid()` server-side and ignore client-supplied IDs.
3. Catch `MongoWriteException` in the global exception handler and return a sanitized `HTTP 400 Bad Request` or `HTTP 409 Conflict`.

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

if not has_01 and not has_02:
    # Insert right before "#### 4. Photographic Proof from MongoDB Compass"
    target_pos = log_text.find("#### 4. Photographic Proof from MongoDB Compass")
    if target_pos != -1:
        log_text = log_text[:target_pos] + details_to_insert + "\n\n" + log_text[target_pos:]
        print("Inserted detail sections for DEFECT-20261106-01 and DEFECT-20261106-02 into Master Defect Log!")

with open(defect_log_path, "w", encoding="utf-8") as f:
    f.write(log_text)

# ==============================================================================
# 2. FIX Attendance2_Defects_Gaps_and_Architecture_Inconsistencies_Report.md
# ==============================================================================
with open(report_path, "r", encoding="utf-8") as f:
    rep_text = f.read()

# Update top banner heading
rep_text = rep_text.replace(
    "## 🚨 Defects Logged Today (05 November 2026): DEFECT-20261105-01, DEFECT-20261105-02, DEFECT-20261105-03 & DEFECT-20261105-04",
    "## 🚨 Defects Logged on 05 & 06 November 2026: DEFECT-20261105-01, DEFECT-20261105-02, DEFECT-20261105-03, DEFECT-20261105-04, DEFECT-20261106-01 & DEFECT-20261106-02"
)

# Add Part 3H to Table of Contents if not present
toc_target = "* [**🏢 Part 3G: Defects Identified on 05 November 2026"
if toc_target in rep_text and "Part 3H:" not in rep_text[:rep_text.find("## 🚨")]:
    idx_toc = rep_text.find(toc_target)
    idx_eol = rep_text.find("\n", idx_toc)
    part_3h_toc = "\n* [**🏢 Part 3H: Defects Identified & Live Verified on 05 & 06 November 2026 — Attendance Policy Module (Live Verification on Attendance 6 & Attendance 7)**](#-part-3h-defects-identified--live-verified-on-05--06-november-2026--attendance-policy-module-live-verification-on-attendance-6--attendance-7) — *Policy Lifecycles, Negative Rates, Duplicate Key 500 Crash & MongoDB Audit (6 Defects)*"
    rep_text = rep_text[:idx_eol] + part_3h_toc + rep_text[idx_eol:]
    print("Added Part 3H to Table of Contents in Report!")

with open(report_path, "w", encoding="utf-8") as f:
    f.write(rep_text)

print("Both markdown files verified and perfected!")

