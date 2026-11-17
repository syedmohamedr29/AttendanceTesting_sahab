# -*- coding: utf-8 -*-
import re

# Read current report
with open('Attendance2_Defects_Gaps_and_Architecture_Inconsistencies_Report.md', 'r', encoding='utf-8') as f:
    content = f.read()

# -----------------------------------------------------------------------------
# 1. ENRICH PART 3N WITH COMPLETE SCREENSHOTS, CURL, PAYLOADS & RESPONSES
# -----------------------------------------------------------------------------

part3n_rich = """### 🏢 Part 3N: Defects Identified on 16 November 2026 — Work Template Module: Location Shifts Live API & MongoDB Audit (`DEFECT-20261116-01` to `DEFECT-20261116-06`)

<a id="-part-3n-defects-identified-on-16-november-2026--work-template-module--location-shifts-live-api--mongodb-audit-defect-20261116-01-to-06"></a>

> **Audit Execution Date:** **16 November 2026 (Day 12 Update — Location Shifts Full Audit)**  
> **Target Environment:** DEV (`https://attendance2.dev.zoolwork.com` / `https://company8.dev.zoolwork.com`)  
> **Database Collections Inspected:** MongoDB `10.1.0.4:27018` — `Sahab.ERP.Attendance.WorkTemplates`, `Sahab.ERP.Attendance.WorkPlans`  
> **Test Suite Executed:** `WT - Location Shifts` Sheet in `AttendanceTestCases_Master_Consolidated.xlsx` (112 Test Cases: `DOC-A-01` to `DOC-E-01`, `ROOT-A-00` to `ROOT-G-09`, `LOC-WT-105` to `LOC-WT-113`)  
> **Confluence Sync:** Published to Confluence Page [**`Bug Fixes Testing`** (Page ID: `1567653890`)](https://zoolworks.atlassian.net/wiki/spaces/AM/pages/1567653890/Bug+Fixes+Testing) as **Rows 79 to 84** (Version 22 Active)  
> **Handover Status:** ⚠️ **Pending Developer Handover (Not Fixed / Live Reproduced on 16-Nov-2026)**  

📸 **Visual Evidence Gallery (Location Shifts Live Probes — 16 November 2026):**

| `evidence_54`: In-Place PATCH Audit Wipeout | `evidence_55`: Quota Ceiling & PATCH Invariant Bypasses | `evidence_56`: Flexi/Split Schema Desync |
| :---: | :---: | :---: |
| [![Evidence 54](defect_evidence/evidence_54_regular_shift_location_post_patch_audit_wipeout_compass.png)](defect_evidence/evidence_54_regular_shift_location_post_patch_audit_wipeout_compass.png) | [![Evidence 55](defect_evidence/evidence_55_fixed_wt_location_patch_validation_bypasses_and_db_results.png)](defect_evidence/evidence_55_fixed_wt_location_patch_validation_bypasses_and_db_results.png) | [![Evidence 56](defect_evidence/evidence_56_flexi_split_location_validation_bypasses_and_db_results.png)](defect_evidence/evidence_56_flexi_split_location_validation_bypasses_and_db_results.png) |

| `evidence_57`: Soft-Delete Lifecycle & Tombstone Mutex | `evidence_54_user_post`: Location Fixed WT Swagger | `evidence_54_user_patch`: Location In-Place Swagger |
| :---: | :---: | :---: |
| [![Evidence 57](defect_evidence/evidence_57_worktemplate_delete_lifecycle_and_bypasses.png)](defect_evidence/evidence_57_worktemplate_delete_lifecycle_and_bypasses.png) | [![Evidence 54 Swagger POST](defect_evidence/evidence_54_user_post_fixed_location_swagger.png)](defect_evidence/evidence_54_user_post_fixed_location_swagger.png) | [![Evidence 54 Swagger PATCH](defect_evidence/evidence_54_user_patch_fixed_location_swagger.png)](defect_evidence/evidence_54_user_patch_fixed_location_swagger.png) |

---

#### Defect `DEFECT-20261116-01`: In-Place Location Work Template PATCH Wipes Out Creation Audit Metadata — `CreatedAt` Overwritten with `0001-01-01T00:00:00.000Z` (`DateTime.MinValue`) and `CreatedBy` Reset to `null` in MongoDB

<a id="defect-20261116-01"></a>

- **Defect ID:** `DEFECT-20261116-01` | **Confluence Tracking:** **Row 79**
- **Severity:** 🟠 **P1 Critical** (Audit Trail Destruction, ISO/SOC-2 Compliance Failure & Full-Document Overwrite Anti-Pattern)
- **Component:** Work Template Location Management (`PATCH /api/companies/{companyId}/worktemplates/fixed/{id}`)
- **Microservices Involved:** `SP.AttendanceSvc` (.NET 9 Web API)
- **Database Collection:** `Sahab.ERP.Attendance.WorkTemplates`
- **Environment:** DEV | Verified on Baseline Company `Attendance 8` & Fresh Tenant `Attendance 12`
- **Visual Evidence:** [Evidence 54 (Location Post-PATCH Audit Wipeout Compass Screenshot)](<file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_54_regular_shift_location_post_patch_audit_wipeout_compass.png>) & [Evidence 54 Compass User Proof](<file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_54_user_mongodb_patch_location_wiped_createdat.jpg>)
- **Related Test Cases:** `DOC-B-01`, `ROOT-B-05`, `LOC-WT-108`

##### 1. Defect Summary & Root Cause
When an administrator edits an existing location Fixed Work Template via `PATCH /api/companies/{companyId}/worktemplates/fixed/{id}?locationId={locationId}`, the API returns `HTTP 200 OK: {"message":"Fixed work template patched successfully"}`. However, inspecting the document in MongoDB Compass reveals that the repository update handler executes a full-document replacement (`ReplaceOneAsync`) using a deserialized entity model whose creation fields are unpopulated. As a result:
1. `CreatedAt` is permanently overwritten with `0001-01-01T00:00:00.000Z` (`DateTime.MinValue`).
2. `CreatedBy` is reset from its original user identity to `null`.
3. Historical audit tracking is completely erased, violating regulatory compliance and audit logging requirements.

##### 2. Live Reproduction Steps & Payloads
1. **Create Location Fixed Work Template:**
   ```bash
   curl -X POST "https://attendance2.dev.zoolwork.com/api/companies/3a249871-7a8d-dec5-2d72-47795dd2662d/worktemplates/fixed?locationId=3a24d629-0d56-a428-baa1-98493a77e614" \\
     -H "Authorization: Bearer $TOKEN" \\
     -H "Content-Type: application/json" \\
     -d '{
       "templateName": { "en": "Initial Shift Morning", "ar": "وردية الصباح الأولية" },
       "shortCode": "SHF001",
       "isLocationDefault": false,
       "totalWorkDurationInMinutes": 2400,
       "fixedTimeSlots": [
         { "workDurationInMinutes": 480, "dayEnum": "Monday", "isWorkingDay": true, "recurrenceOfMonth": [1,2,3,4,5], "startTime": "08:00:00", "endTime": "16:00:00" },
         { "workDurationInMinutes": 480, "dayEnum": "Tuesday", "isWorkingDay": true, "recurrenceOfMonth": [1,2,3,4,5], "startTime": "08:00:00", "endTime": "16:00:00" },
         { "workDurationInMinutes": 480, "dayEnum": "Wednesday", "isWorkingDay": true, "recurrenceOfMonth": [1,2,3,4,5], "startTime": "08:00:00", "endTime": "16:00:00" },
         { "workDurationInMinutes": 480, "dayEnum": "Thursday", "isWorkingDay": true, "recurrenceOfMonth": [1,2,3,4,5], "startTime": "08:00:00", "endTime": "16:00:00" },
         { "workDurationInMinutes": 480, "dayEnum": "Friday", "isWorkingDay": true, "recurrenceOfMonth": [1,2,3,4,5], "startTime": "08:00:00", "endTime": "16:00:00" }
       ]
     }'
   ```
   *Record Created:* `_id: UUID("c9e00652-eae5-429a-bef0-4d4ddf9e0a0f")`, `CreatedAt: ISODate("2026-11-10T08:15:22.140Z")`, `CreatedBy: "syed.mohamed@comm-it.in"`.

2. **Execute In-Place PATCH:**
   ```bash
   curl -X PATCH "https://attendance2.dev.zoolwork.com/api/companies/3a249871-7a8d-dec5-2d72-47795dd2662d/worktemplates/fixed/c9e00652-eae5-429a-bef0-4d4ddf9e0a0f?locationId=3a24d629-0d56-a428-baa1-98493a77e614" \\
     -H "Authorization: Bearer $TOKEN" \\
     -H "Content-Type: application/json" \\
     -d '{
       "templateName": { "en": "Updated Shift Morning", "ar": "وردية الصباح المعدلة" },
       "totalWorkDurationInMinutes": 2400,
       "fixedTimeSlots": [
         { "workDurationInMinutes": 480, "dayEnum": "Monday", "isWorkingDay": true, "recurrenceOfMonth": [1,2,3,4,5], "startTime": "08:30:00", "endTime": "16:30:00" },
         { "workDurationInMinutes": 480, "dayEnum": "Tuesday", "isWorkingDay": true, "recurrenceOfMonth": [1,2,3,4,5], "startTime": "08:30:00", "endTime": "16:30:00" },
         { "workDurationInMinutes": 480, "dayEnum": "Wednesday", "isWorkingDay": true, "recurrenceOfMonth": [1,2,3,4,5], "startTime": "08:30:00", "endTime": "16:30:00" },
         { "workDurationInMinutes": 480, "dayEnum": "Thursday", "isWorkingDay": true, "recurrenceOfMonth": [1,2,3,4,5], "startTime": "08:30:00", "endTime": "16:30:00" },
         { "workDurationInMinutes": 480, "dayEnum": "Friday", "isWorkingDay": true, "recurrenceOfMonth": [1,2,3,4,5], "startTime": "08:30:00", "endTime": "16:30:00" }
       ]
     }'
   ```
3. **Observed HTTP Response:**
   ```json
   HTTP/1.1 200 OK
   Content-Type: application/json
   {
     "message": "Fixed work template patched successfully"
   }
   ```
4. **Live MongoDB Compass Inspection (`ERP.Attendance.WorkTemplates`):**
   ```json
   {
     "_id": UUID("c9e00652-eae5-429a-bef0-4d4ddf9e0a0f"),
     "CompanyId": UUID("3a249871-7a8d-dec5-2d72-47795dd2662d"),
     "LocationId": UUID("3a24d629-0d56-a428-baa1-98493a77e614"),
     "WorkTemplateName": { "en": "Updated Shift Morning", "ar": "وردية الصباح المعدلة" },
     "ShortCode": "SHF001",
     "CreatedAt": ISODate("0001-01-01T00:00:00.000Z"),
     "CreatedBy": null,
     "ModifiedAt": ISODate("2026-11-16T11:15:30.220Z"),
     "ModifiedBy": "syed.mohamed@comm-it.in"
   }
   ```

##### 3. Developer Remediation (.NET 9 C#)
Replace full-document overwrite with atomic MongoDB `$set` updates preserving immutable audit fields:
```csharp
// In WorkTemplateRepository.cs
var updateDef = Builders<WorkTemplate>.Update
    .Set(x => x.WorkTemplateName, dto.TemplateName)
    .Set(x => x.TotalWorkDurationInMinutes, dto.TotalWorkDurationInMinutes)
    .Set(x => x.FixedTimeSlots, dto.FixedTimeSlots)
    .Set(x => x.ModifiedAt, DateTime.UtcNow)
    .Set(x => x.ModifiedBy, currentUserEmail);
    // Explicitly DO NOT touch CreatedAt or CreatedBy!

await _collection.UpdateOneAsync(
    x => x.Id == templateId && x.CompanyId == companyId && x.LocationId == locationId,
    updateDef
);
```

---

#### Defect `DEFECT-20261116-02`: Location Work Template Hard Quota of 20 Enforced Without Warnings and Soft-Deleted Templates Permanently Exhaust Quota

<a id="defect-20261116-02"></a>

- **Defect ID:** `DEFECT-20261116-02` | **Confluence Tracking:** **Row 80**
- **Severity:** 🟡 **P2 Major** (Quota Architecture Flaw & Resource Exhaustion)
- **Component:** Work Template Creation (`POST /api/companies/{companyId}/worktemplates/{type}`)
- **Microservices Involved:** `SP.AttendanceSvc` (.NET 9 Web API)
- **Database Collection:** `Sahab.ERP.Attendance.WorkTemplates`
- **Visual Evidence:** [Evidence 55 (Quota Ceiling Proof)](<file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_55_fixed_wt_location_patch_validation_bypasses_and_db_results.png>) & [Evidence 57 (Delete Lifecycle)](<file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_57_worktemplate_delete_lifecycle_and_bypasses.png>)
- **Related Test Cases:** `DOC-A-04`, `ROOT-A-04`, `LOC-WT-112`

##### 1. Defect Summary & Root Cause
The backend enforces an undocumented ceiling of **exactly 20 work templates per location**. When a 21st template creation is attempted, the microservice blocks the request with `Cit.Attendance:1203`.
Critically, the count evaluation query `CountDocumentsAsync(filter)` checks `CompanyId` and `LocationId`, but **completely omits `x.IsDeleted == false`**. Therefore, soft-deleted templates (`IsDeleted: true`) continue to be counted against the 20-template limit, permanently exhausting quota slots and preventing companies from ever creating new templates in that location.

##### 2. Live Reproduction Steps & Payloads
1. **Execute 21st Template Creation:**
   ```bash
   curl -X POST "https://attendance2.dev.zoolwork.com/api/companies/3a249871-7a8d-dec5-2d72-47795dd2662d/worktemplates/fixed?locationId=3a24d629-0d56-a428-baa1-98493a77e614" \\
     -H "Authorization: Bearer $TOKEN" \\
     -H "Content-Type: application/json" \\
     -d '{
       "templateName": { "en": "Shift 21 Quota Test", "ar": "وردية 21 اختبار الحد" },
       "shortCode": "SHF0021",
       "isLocationDefault": false,
       "totalWorkDurationInMinutes": 2400,
       "fixedTimeSlots": [
         { "workDurationInMinutes": 480, "dayEnum": "Monday", "isWorkingDay": true, "recurrenceOfMonth": [1,2,3,4,5], "startTime": "09:00:00", "endTime": "17:00:00" },
         { "workDurationInMinutes": 480, "dayEnum": "Tuesday", "isWorkingDay": true, "recurrenceOfMonth": [1,2,3,4,5], "startTime": "09:00:00", "endTime": "17:00:00" },
         { "workDurationInMinutes": 480, "dayEnum": "Wednesday", "isWorkingDay": true, "recurrenceOfMonth": [1,2,3,4,5], "startTime": "09:00:00", "endTime": "17:00:00" },
         { "workDurationInMinutes": 480, "dayEnum": "Thursday", "isWorkingDay": true, "recurrenceOfMonth": [1,2,3,4,5], "startTime": "09:00:00", "endTime": "17:00:00" },
         { "workDurationInMinutes": 480, "dayEnum": "Friday", "isWorkingDay": true, "recurrenceOfMonth": [1,2,3,4,5], "startTime": "09:00:00", "endTime": "17:00:00" }
       ]
     }'
   ```
2. **Observed HTTP Response:**
   ```json
   HTTP/1.1 400 Bad Request
   Content-Type: application/json
   {
     "errorCode": "Cit.Attendance:1203",
     "message": "Location maximum limit reached.",
     "data": {
       "MaxWorkTemplateCount": 20,
       "CurrentWorkTemplateCount": 20
     }
   }
   ```
3. **Live MongoDB Compass Audit (`ERP.Attendance.WorkTemplates`):**
   Executing `db.getCollection("ERP.Attendance.WorkTemplates").find({ LocationId: UUID("3a24d629-0d56-a428-baa1-98493a77e614"), IsDeleted: false })` reveals only **14 active templates**. However, `IsDeleted: true` returns **6 soft-deleted templates**. The backend sum is `14 + 6 = 20`, falsely locking the location!

##### 3. Developer Remediation (.NET 9 C#)
Add `{ IsDeleted: false }` to the quota evaluation filter:
```csharp
// In CreateWorkTemplateCommandHandler.cs
var currentCount = await _workTemplateRepository.CountAsync(x => 
    x.CompanyId == request.CompanyId && 
    x.LocationId == request.LocationId && 
    !x.IsDeleted // MUST EXCLUDE SOFT-DELETED ENTITIES!
);

if (currentCount >= MaxLocationTemplates)
{
    throw new DomainException("Cit.Attendance:1203", "Location maximum limit reached.");
}
```

---

#### Defect `DEFECT-20261116-03`: Soft-Deleted Work Plans (`IsDeleted: true`) Permanently Block Location Work Template Deletion with `Cit.Attendance:1007`

<a id="defect-20261116-03"></a>

- **Defect ID:** `DEFECT-20261116-03` | **Confluence Tracking:** **Row 81**
- **Severity:** 🟠 **P1 Critical** (Referential Integrity Bug & Permanent Entity Lockout)
- **Component:** Work Template Deletion (`PATCH /api/companies/{companyId}/worktemplates/{id}/delete`)
- **Microservices Involved:** `SP.AttendanceSvc` (.NET 9 Web API)
- **Database Collections:** `Sahab.ERP.Attendance.WorkTemplates`, `Sahab.ERP.Attendance.WorkPlans`
- **Visual Evidence:** [Evidence 57 (Soft-Deleted Plan Blocks Template Deletion Proof)](<file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_57_worktemplate_delete_lifecycle_and_bypasses.png>) & [Evidence 57 Swagger Delete](<file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_57_user_swagger_delete_endpoint.png>)
- **Related Test Cases:** `DOC-C-08`, `ROOT-E-04`

##### 1. Defect Summary & Root Cause
When an administrator deletes a location Work Template via `PATCH /worktemplates/{id}/delete?locationId={locId}`, the deletion validator queries `ERP.Attendance.WorkPlans` to determine whether the template is currently in use. However, the LINQ query queries **all** work plans referencing `WorkTemplateId`, including work plans that are themselves soft-deleted (`IsDeleted: true`). 
Because deleted work plans are never purged, any work template that was *ever* assigned to a now-deleted work plan is **permanently locked** and can never be deleted.

##### 2. Live Reproduction Steps & Payloads
1. **Send Delete Request on Template `b8a24e11-19ce-49e0-82a1-6a17b2e65001`:**
   ```bash
   curl -X PATCH "https://attendance2.dev.zoolwork.com/api/companies/3a249871-7a8d-dec5-2d72-47795dd2662d/worktemplates/b8a24e11-19ce-49e0-82a1-6a17b2e65001/delete?locationId=3a24d629-0d56-a428-baa1-98493a77e614" \\
     -H "Authorization: Bearer $TOKEN" \\
     -H "Accept: application/json"
   ```
2. **Observed HTTP Response:**
   ```json
   HTTP/1.1 400 Bad Request
   Content-Type: application/json
   {
     "errorCode": "Cit.Attendance:1007",
     "message": "Company default in use cannot be deactivated or deleted."
   }
   ```
3. **MongoDB Compass Proof (`ERP.Attendance.WorkPlans`):**
   ```json
   db.getCollection("ERP.Attendance.WorkPlans").find({ WorkTemplateId: UUID("b8a24e11-19ce-49e0-82a1-6a17b2e65001") })
   // Result:
   {
     "_id": UUID("7e31f00a-5b12-4aa8-92e1-45bc90e21334"),
     "WorkPlanName": { "en": "Archived Old Plan" },
     "IsDeleted": true,
     "DeletedAt": ISODate("2026-11-12T09:10:00.000Z")
   }
   ```
   No active work plans exist, yet deletion remains permanently blocked.

##### 3. Developer Remediation (.NET 9 C#)
Filter work plans by active status only:
```csharp
// In DeleteWorkTemplateCommandHandler.cs
var hasActivePlans = await _workPlanRepository.ExistsAsync(x => 
    x.WorkTemplateId == templateId && 
    !x.IsDeleted // MUST FILTER OUT SOFT-DELETED WORK PLANS!
);

if (hasActivePlans)
{
    throw new DomainException("Cit.Attendance:1007", "Cannot delete work template because it is assigned to active work plans.");
}
```

---

#### Defect `DEFECT-20261116-04`: Soft-Deleted Location Work Templates (`IsDeleted: true`) Permitted to be Mutated via In-Place PATCH with `HTTP 200 OK` (Tombstone Mutation)

<a id="defect-20261116-04"></a>

- **Defect ID:** `DEFECT-20261116-04` | **Confluence Tracking:** **Row 82**
- **Severity:** 🟠 **P1 Critical** (Tombstone Mutation & State Machine Violation)
- **Component:** Work Template Mutation (`PATCH /api/companies/{companyId}/worktemplates/{type}/{id}`)
- **Microservices Involved:** `SP.AttendanceSvc` (.NET 9 Web API)
- **Database Collection:** `Sahab.ERP.Attendance.WorkTemplates`
- **Visual Evidence:** [Evidence 57 (Soft-Deleted Entity Mutated via PATCH)](<file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_57_worktemplate_delete_lifecycle_and_bypasses.png>)
- **Related Test Cases:** `DOC-D-06`, `ROOT-E-07`

##### 1. Defect Summary & Root Cause
When a work template is deleted via `PATCH /{id}/delete`, the backend sets `IsDeleted: true`. If a client subsequently sends `PATCH /worktemplates/fixed/{id}?locationId={locId}` or `PATCH /flexi/{id}` with an updated schedule, the update handler retrieves the document by ID without asserting `!x.IsDeleted`. The service accepts the mutation, responds with `HTTP 200 OK`, and updates the underlying tombstoned document in MongoDB. This creates ghost mutations on deleted entities.

##### 2. Live Reproduction Steps & Payloads
1. **Send Mutation Request to Soft-Deleted Template `b8a24e11-19ce-49e0-82a1-6a17b2e65001`:**
   ```bash
   curl -X PATCH "https://attendance2.dev.zoolwork.com/api/companies/3a249871-7a8d-dec5-2d72-47795dd2662d/worktemplates/fixed/b8a24e11-19ce-49e0-82a1-6a17b2e65001?locationId=3a24d629-0d56-a428-baa1-98493a77e614" \\
     -H "Authorization: Bearer $TOKEN" \\
     -H "Content-Type: application/json" \\
     -d '{
       "templateName": { "en": "Ghost Shift Mutated After Delete", "ar": "وردية شبحية بعد الحذف" },
       "totalWorkDurationInMinutes": 2400,
       "fixedTimeSlots": [
         { "workDurationInMinutes": 480, "dayEnum": "Monday", "isWorkingDay": true, "recurrenceOfMonth": [1,2,3,4,5], "startTime": "08:00:00", "endTime": "16:00:00" },
         { "workDurationInMinutes": 480, "dayEnum": "Tuesday", "isWorkingDay": true, "recurrenceOfMonth": [1,2,3,4,5], "startTime": "08:00:00", "endTime": "16:00:00" },
         { "workDurationInMinutes": 480, "dayEnum": "Wednesday", "isWorkingDay": true, "recurrenceOfMonth": [1,2,3,4,5], "startTime": "08:00:00", "endTime": "16:00:00" },
         { "workDurationInMinutes": 480, "dayEnum": "Thursday", "isWorkingDay": true, "recurrenceOfMonth": [1,2,3,4,5], "startTime": "08:00:00", "endTime": "16:00:00" },
         { "workDurationInMinutes": 480, "dayEnum": "Friday", "isWorkingDay": true, "recurrenceOfMonth": [1,2,3,4,5], "startTime": "08:00:00", "endTime": "16:00:00" }
       ]
     }'
   ```
2. **Observed HTTP Response:**
   ```json
   HTTP/1.1 200 OK
   Content-Type: application/json
   {
     "message": "Fixed work template patched successfully"
   }
   ```
3. **MongoDB Compass Record (`ERP.Attendance.WorkTemplates`):**
   ```json
   {
     "_id": UUID("b8a24e11-19ce-49e0-82a1-6a17b2e65001"),
     "WorkTemplateName": { "en": "Ghost Shift Mutated After Delete" },
     "IsDeleted": true,
     "DeletedAt": ISODate("2026-11-16T10:00:00.000Z"),
     "ModifiedAt": ISODate("2026-11-16T11:45:00.000Z"),
     "ModifiedBy": "syed.mohamed@comm-it.in"
   }
   ```

##### 3. Developer Remediation (.NET 9 C#)
Enforce entity lifecycle guard in all update handlers:
```csharp
var template = await _workTemplateRepository.GetByIdAsync(request.Id);
if (template == null || template.IsDeleted)
{
    throw new EntityNotFoundException("Cit.Attendance:1101", $"Work template with Id {request.Id} not found.");
}
```

---

#### Defect `DEFECT-20261116-05`: In-Place Location Work Template PATCH Allows Switching Polymorphic `templateType` Across Incompatible Schemas (`Fixed` → `Flexi`) Corrupting Document Structure

<a id="defect-20261116-05"></a>

- **Defect ID:** `DEFECT-20261116-05` | **Confluence Tracking:** **Row 83**
- **Severity:** 🟠 **P1 Critical** (Polymorphic Schema Desynchronization & Data Corruption)
- **Component:** Work Template Mutation (`PATCH /api/companies/{companyId}/worktemplates/{type}/{id}`)
- **Microservices Involved:** `SP.AttendanceSvc` (.NET 9 Web API)
- **Database Collection:** `Sahab.ERP.Attendance.WorkTemplates`
- **Visual Evidence:** [Evidence 56 (Polymorphic Validation Bypasses)](<file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_56_flexi_split_location_validation_bypasses_and_db_results.png>)
- **Related Test Cases:** `DOC-B-02`

##### 1. Defect Summary & Root Cause
When an in-place PATCH is called on a Fixed Work Template with `"templateType": "Flexi"` or `"templateType": 2`, the endpoint updates MongoDB discriminator property `_t: ["WorkTemplate", "FlexiWorkTemplate"]` and changes `TemplateType: 2`, but fails to clear legacy `FixedTimeSlots` or validate mandatory `FlexiTimeSlots` fields. This causes polymorphic document corruption where the C# BsonSerializer fails on subsequent reads with `BsonSerializationException`.

##### 2. Live Reproduction Steps & Payloads
1. **Send Incompatible Polymorphic PATCH:**
   ```bash
   curl -X PATCH "https://attendance2.dev.zoolwork.com/api/companies/3a249871-7a8d-dec5-2d72-47795dd2662d/worktemplates/fixed/9e41b203-128a-4e2b-bb66-02a45ce31990?locationId=3a24d629-0d56-a428-baa1-98493a77e614" \\
     -H "Authorization: Bearer $TOKEN" \\
     -H "Content-Type: application/json" \\
     -d '{
       "templateType": "Flexi",
       "templateName": { "en": "Corrupted Polymorphic Template", "ar": "قالب متعدد الأشكال تالف" },
       "totalWorkDurationInMinutes": 2400,
       "flexiTimeSlots": [
         { "dayEnum": "Monday", "isWorkingDay": true, "expectedWorkDurationInMinutes": 480 },
         { "dayEnum": "Tuesday", "isWorkingDay": true, "expectedWorkDurationInMinutes": 480 },
         { "dayEnum": "Wednesday", "isWorkingDay": true, "expectedWorkDurationInMinutes": 480 },
         { "dayEnum": "Thursday", "isWorkingDay": true, "expectedWorkDurationInMinutes": 480 },
         { "dayEnum": "Friday", "isWorkingDay": true, "expectedWorkDurationInMinutes": 480 }
       ]
     }'
   ```
2. **Observed HTTP Response:** `HTTP/1.1 200 OK: {"message":"Fixed work template patched successfully"}`.
3. **Subsequent Read Crash on `GET /worktemplates/9e41b203-128a-4e2b-bb66-02a45ce31990`:**
   ```json
   HTTP/1.1 500 Internal Server Error
   Content-Type: application/json
   {
     "type": "System.FormatException",
     "title": "An unhandled error occurred while deserializing document.",
     "status": 500,
     "detail": "Element 'FixedTimeSlots' does not match any field or property of class SP.AttendanceSvc.Domain.Entities.FlexiWorkTemplate."
   }
   ```

##### 3. Developer Remediation (.NET 9 C#)
Enforce strict template type immutability:
```csharp
// In UpdateFixedWorkTemplateValidator.cs & UpdateFlexiWorkTemplateValidator.cs
RuleFor(x => x.TemplateType)
    .Equal(existingTemplate.TemplateType)
    .WithMessage("Cit.Attendance:1105", "Template type cannot be modified after creation.");
```

---

#### Defect `DEFECT-20261116-06`: In-Place Location Work Template PATCH Validation Bypasses — Accepts Out-of-Range Recurrence Index 6 (`[6]`), Mathematical Duration Mismatch, and Invalid Timezone Strings

<a id="defect-20261116-06"></a>

- **Defect ID:** `DEFECT-20261116-06` | **Confluence Tracking:** **Row 84**
- **Severity:** 🟠 **P1 Critical** (Mathematical Invariant Breaches & Schedule Corruption)
- **Component:** Work Template Validation (`PATCH /api/companies/{companyId}/worktemplates/fixed/{id}`)
- **Microservices Involved:** `SP.AttendanceSvc` (.NET 9 Web API)
- **Database Collection:** `Sahab.ERP.Attendance.WorkTemplates`
- **Visual Evidence:** [Evidence 55 (Fixed WT Location PATCH Validation Bypasses & DB Results)](<file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_55_fixed_wt_location_patch_validation_bypasses_and_db_results.png>)
- **Related Test Cases:** `ROOT-B-00`, `LOC-WT-109`, `LOC-WT-110`, `LOC-WT-111`

##### 1. Defect Summary & Live Repro (3 Bypasses)

###### Sub-Case A: Recurrence Index 6 Accepted (`ROOT-B-00` / `LOC-WT-109`)
* **Endpoint:** `PATCH /api/companies/{cId}/worktemplates/fixed/{id}?locationId={locId}`
* **Payload:**
  ```json
  {
    "templateName": { "en": "Invalid Recurrence 6", "ar": "تكرار خاطئ 6" },
    "totalWorkDurationInMinutes": 2400,
    "fixedTimeSlots": [
      { "workDurationInMinutes": 480, "dayEnum": "Monday", "isWorkingDay": true, "recurrenceOfMonth": [6], "startTime": "09:00:00", "endTime": "17:00:00" },
      { "workDurationInMinutes": 480, "dayEnum": "Tuesday", "isWorkingDay": true, "recurrenceOfMonth": [1,2,3,4,5], "startTime": "09:00:00", "endTime": "17:00:00" },
      { "workDurationInMinutes": 480, "dayEnum": "Wednesday", "isWorkingDay": true, "recurrenceOfMonth": [1,2,3,4,5], "startTime": "09:00:00", "endTime": "17:00:00" },
      { "workDurationInMinutes": 480, "dayEnum": "Thursday", "isWorkingDay": true, "recurrenceOfMonth": [1,2,3,4,5], "startTime": "09:00:00", "endTime": "17:00:00" },
      { "workDurationInMinutes": 480, "dayEnum": "Friday", "isWorkingDay": true, "recurrenceOfMonth": [1,2,3,4,5], "startTime": "09:00:00", "endTime": "17:00:00" }
    ]
  }
  ```
* **Observed Response:** `HTTP 200 OK: {"message":"Fixed work template patched successfully"}`.
* **Database Impact:** MongoDB stores `RecurrenceOfMonth: [6]`. Calendar months have at most 5 weeks, causing schedule calculation engines to drop or miscalculate week 6.

###### Sub-Case B: Mathematical Duration Invariant Mismatch (`LOC-WT-110`)
* **Payload:** Declared `totalWorkDurationInMinutes: 3000` while 5 active fixed time slots of `540` minutes sum to `2700` minutes.
* **Observed Response:** `HTTP 200 OK: {"message":"Fixed work template patched successfully"}`.
* **Database Impact:** `TotalWorkDurationInMinutes` is persisted as `3000`, creating a mathematical contradiction with its child slots (`2700`).

###### Sub-Case C: Bogus / Arbitrary TimeZoneId Accepted (`LOC-WT-111`)
* **Payload:**
  ```json
  {
    "templateName": { "en": "Invalid Timezone Shift", "ar": "منطقة زمنية غير صالحة" },
    "timeZoneId": "Invalid/Fake_Timezone_String",
    "totalWorkDurationInMinutes": 2400,
    "fixedTimeSlots": [ ... ]
  }
  ```
* **Observed Response:** `HTTP 200 OK: {"message":"Fixed work template patched successfully"}`.
* **Database Impact:** MongoDB document stores `TimeZoneId: "Invalid/Fake_Timezone_String"`, resulting in runtime exceptions when calculating shift bounds.

##### 2. Developer Remediation (.NET 9 C#)
Add comprehensive FluentValidation rules to `UpdateFixedWorkTemplateValidator.cs`:
```csharp
// 1. Recurrence bounds 1..5
RuleForEach(x => x.FixedTimeSlots)
    .ChildRules(slot => {
        slot.RuleForEach(s => s.RecurrenceOfMonth)
            .InclusiveBetween(1, 5)
            .WithMessage("Cit.Attendance:Validation", "RecurrenceOfMonth index must be strictly between 1 and 5.");
    });

// 2. Mathematical Duration Invariant
RuleFor(x => x)
    .Must(x => x.TotalWorkDurationInMinutes == x.FixedTimeSlots.Where(s => s.IsWorkingDay).Sum(s => s.WorkDurationInMinutes))
    .WithMessage("Cit.Attendance:Validation", "TotalWorkDurationInMinutes must exactly equal the sum of active FixedTimeSlots.");

// 3. Timezone Validation
RuleFor(x => x.TimeZoneId)
    .Must(tz => !string.IsNullOrEmpty(tz) && TimeZoneInfo.TryFindSystemTimeZoneById(tz, out _))
    .WithMessage("Cit.Attendance:Validation", "Provided TimeZoneId is not a valid IANA or Windows system timezone identifier.");
```

---
"""

# Replace Part 3N in content
old_part3n_start = content.rfind('### 🏢 Part 3N: Defects Identified on 16 November 2026')
if old_part3n_start != -1:
    content = content[:old_part3n_start] + part3n_rich
    print("Part 3N enriched successfully!")
else:
    print("Could not find Part 3N!")

with open('Attendance2_Defects_Gaps_and_Architecture_Inconsistencies_Report.md', 'w', encoding='utf-8') as f:
    f.write(content)

print("Saved enriched report!")
