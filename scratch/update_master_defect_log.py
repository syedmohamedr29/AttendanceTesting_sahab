import sys

with open('Defects/Attendance2_Master_Defect_Log.md', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update Executive Summary metrics
old_exec = """During rigorous manual, Swagger, Web UI (`sp.dev.zoolwork.com`), and MongoDB Compass testing of the Attendance 2 microservice, a total of **55 defects and architecture gaps** were identified and verified with photographic proof.

### Defect Severity Breakdown

| Severity Level | Count | Impact Summary |
| :--- | :---: | :--- |
| 🔴 **P0 (Blocker)** | **7** | **System Blockers:** Blocks operations entirely. Expired JWT bypass, inverted shifts, PATCH deadlock (`1706`), publishing empty calendar, missing holiday names/types. |
| 🟠 **P1 (Critical)** | **43** | **Critical Domain / Data Integrity:** Unassigned location templates (Delhi gap), HTTP 500 server crashes, negative durations, broken math invariants, empty tenant persistence. |
| 🟡 **P2 (Major)** | **4** | **Audit / DX / Contracts:** Audit fields stored as plain emails instead of composite user objects, redundant DTO fields, missing Swagger OAuth2 login flow. |
| **TOTAL** | **55** | **100% Verified with live screenshots & MongoDB Compass records.** |

### Defect Distribution by Functional Module

| Module | Target Collection / Component | Total | P0 Blocker | P1 Critical | P2 Major |
| :--- | :--- | :---: | :---: | :---: | :---: |
| **Module 1: Holiday Calendars** | `ERP.Attendance.HolidayCalendars` | **15** | 5 | 9 | 1 |
| **Module 2: Work Templates & Location Cascade** | `ERP.Attendance.WorkTemplates` | **26** | 1 | 24 | 1 |
| **Module 3: Work Plans, Rosters & Policies** | `ERP.Attendance.WorkPlans`, `Policies` | **7** | 0 | 6 | 1 |
| **Module 4: Security, Auth & Multi-Tenancy** | Kestrel JWT Middleware, Multi-Tenancy | **6** | 1 | 4 | 1 |
| **TOTAL** | **All 4 Modules Combined** | **55** | **7** | **43** | **4** |"""

new_exec = """During rigorous manual, Swagger, Web UI (`sp.dev.zoolwork.com`), and MongoDB Compass testing of the Attendance 2 microservice, a total of **56 defects and architecture gaps** were identified and verified with photographic proof.

### Defect Severity Breakdown

| Severity Level | Count | Impact Summary |
| :--- | :---: | :--- |
| 🔴 **P0 (Blocker)** | **7** | **System Blockers:** Blocks operations entirely. Expired JWT bypass, inverted shifts, PATCH deadlock (`1706`), publishing empty calendar, missing holiday names/types. |
| 🟠 **P1 (Critical)** | **44** | **Critical Domain / Data Integrity:** Unassigned location templates (Delhi gap), HTTP 500 server crashes, negative durations, broken math invariants, empty tenant persistence, empty company name persistence. |
| 🟡 **P2 (Major)** | **4** | **Audit / DX / Contracts:** Audit fields stored as plain emails instead of composite user objects, redundant DTO fields, missing Swagger OAuth2 login flow. |
| **TOTAL** | **56** | **100% Verified with live screenshots & MongoDB Compass records.** |

### Defect Distribution by Functional Module

| Module | Target Collection / Component | Total | P0 Blocker | P1 Critical | P2 Major |
| :--- | :--- | :---: | :---: | :---: | :---: |
| **Module 1: Holiday Calendars** | `ERP.Attendance.HolidayCalendars` | **15** | 5 | 9 | 1 |
| **Module 2: Work Templates & Location Cascade** | `ERP.Attendance.WorkTemplates` | **27** | 1 | 25 | 1 |
| **Module 3: Work Plans, Rosters & Policies** | `ERP.Attendance.WorkPlans`, `Policies` | **7** | 0 | 6 | 1 |
| **Module 4: Security, Auth & Multi-Tenancy** | Kestrel JWT Middleware, Multi-Tenancy | **6** | 1 | 4 | 1 |
| **TOTAL** | **All 4 Modules Combined** | **56** | **7** | **44** | **4** |"""

assert old_exec.replace('\r\n', '\n') in content.replace('\r\n', '\n'), "old_exec not found"

# 2. Add DEFECT-20261105-01 row to Section 2 matrix right after DEFECT-20261103-16
target_row = '| [`DEFECT-20261103-16`](#defect-20261103-16) | 🟠 P1 | Work Template / Sync | **MAJOR GAP:** Newly created location (Delhi) NOT auto-assigned Company Default Work Template | ``CompanySvc` & `AttendanceSvc`` | [Evidence 37 & 38](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_37_cdwt_compass_only_4_templates_missing_delhi.jpg) |'

new_row = """| [`DEFECT-20261103-16`](#defect-20261103-16) | 🟠 P1 | Work Template / Sync | **MAJOR GAP:** Newly created location (Delhi) NOT auto-assigned Company Default Work Template | ``CompanySvc` & `AttendanceSvc`` | [Evidence 37 & 38](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_37_cdwt_compass_only_4_templates_missing_delhi.jpg) |
| [`DEFECT-20261105-01`](#defect-20261105-01) | 🟠 P1 | Work Template / Master Data | `CompanyName` persists as `Object (empty)` `{}` in MongoDB upon Work Template creation | ``POST /worktemplates/*`` | [Evidence 39](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_39_companyname_empty_object_compass.jpg) |"""

assert target_row in content, "target_row not found"

# 3. Add full defect section in Module 2 right after DEFECT-20261103-16
target_section_marker = "### <a id=\"defect-20261103-16\"></a>🔴 DEFECT-20261103-16: MAJOR ARCHITECTURE GAP: Newly Created Location ('Delhi') Not Auto-Assigned Company Default Work Template"

defect_20261105_01_body = """### <a id="defect-20261105-01"></a>🔴 DEFECT-20261105-01: `CompanyName` Persists as `Object (empty)` `{}` in MongoDB Upon Work Template Creation (Missing Company Metadata Resolution from `SP.CompanySvc`)
- **Severity:** 🟠 P1 (Critical / Data Integrity & Master Data)
- **Target Route:** `POST /api/companies/{companyId}/worktemplates/{fixed|flexi|split}`, `GET /api/companies/{companyId}/worktemplates`
- **Database Target:** `Sahab.ERP.Attendance.WorkTemplates`
- **Status:** 🔴 **Open / Verified with Photographic Evidence in MongoDB Compass**

#### 1. Problem Summary
When a Company Default Work Template is created for a company (e.g., Company `Attendance 9`, ID: `3a249872-2d69-f931-41f6-d8db086b09b8`), the service properly persists `CompanyId: UUID('3a249872-2d69-f931-41f6-d8db086b09b8')`. However, the localized `CompanyName` field in MongoDB is saved as an empty object: `CompanyName: Object (empty)` (`{}`).
Furthermore, in the API response (`POST /worktemplates/*` and `GET /worktemplates/{id}`), `companyName` is returned as empty JSON: `"companyName": {}`.
`SP.AttendanceSvc` never resolves or queries the company's localized names (`{"en": "Attendance 9", "ar": "الحضور 9"}`) from `SP.CompanySvc` (`https://company8.dev.zoolwork.com`), nor does it populate `CompanyName` during document creation. This leads to broken UI rendering (where company name is displayed blank or raw GUID fallback is shown), data loss in downstream reporting and integration events, and inconsistent database records across Sahab ERP.

#### 2. Steps to Reproduce
1. Onboard a fresh company in `SP.CompanySvc` (e.g. `Attendance 9`, `3a249872-2d69-f931-41f6-d8db086b09b8`).
2. Call `POST /api/companies/3a249872-2d69-f931-41f6-d8db086b09b8/worktemplates/fixed` (or `/flexi`) to create Company Default Work Template.
3. Observe API response: `"companyId": "3a249872-2d69-f931-41f6-d8db086b09b8"`, `"companyName": {}`.
4. Open MongoDB Compass, connect to `DEV > Sahab > ERP.Attendance.WorkTemplates`, and filter by:
   ```json
   { "CompanyId": UUID("3a249872-2d69-f931-41f6-d8db086b09b8") }
   ```
5. Inspect document `d5abe5c4-d51f-4287-9baf-38e2e4f547c8`:
   - `CompanyId`: `UUID('3a249872-2d69-f931-41f6-d8db086b09b8')`
   - `CompanyName`: `Object (empty)` 🔴 **DEFECT**

#### 3. Exact Reproduction Request Payload (JSON)
```http
POST /api/companies/3a249872-2d69-f931-41f6-d8db086b09b8/worktemplates/fixed HTTP/1.1
Host: attendance2.dev.zoolwork.com
Authorization: Bearer <JWT>
Content-Type: application/json

{
  "templateName": {
    "en": "Attendance 9 Fixed Template",
    "ar": "قالب الحضور 9 الثابت"
  },
  "shortCode": "ATT9FIX",
  "templateType": 1,
  "totalWorkDurationInMinutes": 480,
  "totalWorkingDays": 5,
  "totalDaysOff": 2,
  "fixedTimeSlots": [
    { "dayEnum": 1, "isWorkingDay": true, "workDurationInMinutes": 480, "startTime": "08:00:00", "endTime": "16:00:00", "recurrenceOfMonth": [1, 2, 3, 4, 5] },
    { "dayEnum": 2, "isWorkingDay": true, "workDurationInMinutes": 480, "startTime": "08:00:00", "endTime": "16:00:00", "recurrenceOfMonth": [1, 2, 3, 4, 5] },
    { "dayEnum": 3, "isWorkingDay": true, "workDurationInMinutes": 480, "startTime": "08:00:00", "endTime": "16:00:00", "recurrenceOfMonth": [1, 2, 3, 4, 5] },
    { "dayEnum": 4, "isWorkingDay": true, "workDurationInMinutes": 480, "startTime": "08:00:00", "endTime": "16:00:00", "recurrenceOfMonth": [1, 2, 3, 4, 5] },
    { "dayEnum": 5, "isWorkingDay": true, "workDurationInMinutes": 480, "startTime": "08:00:00", "endTime": "16:00:00", "recurrenceOfMonth": [1, 2, 3, 4, 5] },
    { "dayEnum": 6, "isWorkingDay": false, "workDurationInMinutes": 0, "startTime": "00:00:00", "endTime": "00:00:00", "recurrenceOfMonth": [1, 2, 3, 4, 5] },
    { "dayEnum": 7, "isWorkingDay": false, "workDurationInMinutes": 0, "startTime": "00:00:00", "endTime": "00:00:00", "recurrenceOfMonth": [1, 2, 3, 4, 5] }
  ]
}
```

#### 4. Photographic Evidence from MongoDB Compass
| Visual Evidence | Description |
| :--- | :--- |
| ![DEFECT-20261105-01](../defect_evidence/evidence_39_companyname_empty_object_compass.jpg) | **File:** `evidence_39_companyname_empty_object_compass.jpg`<br><br>[🔍 Click to Open Full-Resolution Image](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_39_companyname_empty_object_compass.jpg)<br><br>*Evidence 39: MongoDB Compass live inspection of document `d5abe5c4-d51f-4287-9baf-38e2e4f547c8` on Company `Attendance 9` (`3a249872-2d69-f931-41f6-d8db086b09b8`). Highlighted in red: `CompanyName: Object (empty)`.* |

#### 5. Technical Root Cause & Architecture Analysis
In `CreateFixedWorkTemplateCommandHandler.cs` (and corresponding Flexi / Split handlers):
1. The command handler receives `companyId` from the route and sets `workTemplate.CompanyId = command.CompanyId;`.
2. The entity property `workTemplate.CompanyName` is instantiated as `new MultilingualString()` (or left empty `{}`).
3. There is NO integration call, gRPC query, or distributed event lookup to `SP.CompanySvc` to fetch the company's localized title.
4. Consequently, `CompanyName` remains `{}` and is stored directly into MongoDB as `CompanyName: {}`.
5. This is an identical architecture gap to `DEFECT-20261026-02` / `DEFECT-20261103-02` (where `TenantName` is stored as `{}`).

#### 6. Developer Remediation & C# Code Fix
In `SP.AttendanceSvc`:
1. Inject `ICompanyServiceClient` into `Create*WorkTemplateCommandHandler` (or query internal company master cache).
2. Prior to saving the `WorkTemplate` entity:
   ```csharp
   var companyInfo = await _companyServiceClient.GetCompanyByIdAsync(request.CompanyId, cancellationToken);
   if (companyInfo != null)
   {
       template.CompanyName = new MultilingualString
       {
           En = companyInfo.Name.En,
           Ar = companyInfo.Name.Ar
       };
   }
   ```
3. Update `WorkTemplateDto` mapping to ensure `CompanyName` returns the populated multilingual object.

---
"""

# 4. Add checklist item in Section 8 (Developer Action Checklist)
target_checklist = "- [ ] **P1 (`DEFECT-20261103-16`):** In `SP.AttendanceSvc`,"
new_checklist = """- [ ] **P1 (`DEFECT-20261105-01`):** In `SP.AttendanceSvc`, resolve and populate `CompanyName` (`MultilingualString { En, Ar }`) from `SP.CompanySvc` when creating/updating Work Templates so MongoDB `ERP.Attendance.WorkTemplates` and API responses do not persist `CompanyName: Object (empty)` `{}`.
- [ ] **P1 (`DEFECT-20261103-16`):** In `SP.AttendanceSvc`,"""

assert target_checklist in content, "target_checklist not found"

# Apply all replacements
content = content.replace(target_row, new_row)
content = content.replace(target_section_marker, defect_20261105_01_body + "\n" + target_section_marker)
content = content.replace(target_checklist, new_checklist)

# Normalize and replace exec summary
c_norm = content.replace('\r\n', '\n')
old_e_norm = old_exec.replace('\r\n', '\n')
new_e_norm = new_exec.replace('\r\n', '\n')
c_norm = c_norm.replace(old_e_norm, new_e_norm, 1)

with open('Defects/Attendance2_Master_Defect_Log.md', 'w', encoding='utf-8') as f:
    f.write(c_norm)

print("Defects/Attendance2_Master_Defect_Log.md updated successfully!")
