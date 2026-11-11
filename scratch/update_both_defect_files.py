import os
import sys

# Ensure UTF-8 output
sys.stdout.reconfigure(encoding='utf-8')

# ==============================================================================
# RICH CONTENT BLOCKS FOR REPORT MD (Attendance2_Defects_Gaps_and_Architecture_Inconsistencies_Report.md)
# ==============================================================================

report_block = """#### Defect `DEFECT-20261110-15`: `PATCH /worktemplates/{type}/{id}` Validation Gap — In-Place Update Allows Modifying Soft-Deleted Work Templates (`IsDeleted: true`) with HTTP 200 OK

- **Severity:** 🟠 **P1 Critical** (Data Integrity Violation, Tombstone Mutation & State Machine Bypass)
- **Module / Feature:** Module 2: Work Template In-Place PATCH / Deletion Lifecycle
- **Affected Endpoints:** `PATCH /api/companies/{companyId}/worktemplates/{fixed|flexi|split}/{id}?locationId={locationId}`
- **Target Collection:** `Sahab.ERP.Attendance.WorkTemplates`
- **Target Company:** Attendance 8 (`3a249871-7a8d-dec5-2d72-47795dd2662d`)
- **Target Location:** Location 2 (`3a24d646-b3cf-b1d4-61bb-1adf094b52fc`) / Location 1 (`3a24d629-0d56-a428-baa1-98493a77e614`)
- **Target Document:** `cf3ef115-b548-436b-afd1-568be4f5ebfa` (`DLPOS01`)
- **Visual Evidence:**
  * [Evidence 57 (Work Template Delete Lifecycle & Critical Integrity Gaps)](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_57_worktemplate_delete_lifecycle_and_bypasses.png)
  * [Swagger Delete Endpoint](file:///d:/Code/Attendance%20Testing/defect_evidence/media_1794302386426_bac6f77d.png)

![Evidence 57](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_57_worktemplate_delete_lifecycle_and_bypasses.png)

##### 1. Problem Description & Direct Evidence Analysis
1. Work template `cf3ef115-b548-436b-afd1-568be4f5ebfa` was soft-deleted via `PATCH /worktemplates/cf3ef115.../delete` (`IsDeleted: true` in MongoDB).
2. A subsequent in-place update was sent to `PATCH /worktemplates/fixed/cf3ef115-b548-436b-afd1-568be4f5ebfa?locationId=3a24d646-b3cf-b1d4-61bb-1adf094b52fc` renaming the template to `"Revived Mutated Shift"`.
3. The API returned **HTTP 200 OK**, modified the document in MongoDB (`WorkTemplateName`, slots, durations), and updated `ModifiedAt`, while preserving `IsDeleted: true`.
4. The PATCH command handler retrieves the document by ID without asserting `!template.IsDeleted`, completely bypassing the deleted state barrier.

##### 2. Tested Payload & Request Details
```json
PATCH /api/companies/3a249871-7a8d-dec5-2d72-47795dd2662d/worktemplates/fixed/cf3ef115-b548-436b-afd1-568be4f5ebfa?locationId=3a24d646-b3cf-b1d4-61bb-1adf094b52fc
Content-Type: application/json

{
  "templateName": {
    "en": "Revived Mutated Shift",
    "ar": "تعديل بعد الحذف المنطقي"
  },
  "shortCode": "DLPOS01",
  "templateType": 1,
  "totalWorkDurationInMinutes": 2700,
  "totalWorkingDays": 5,
  "totalDaysOff": 2,
  "timeZoneId": "Asia/Riyadh",
  "fixedTimeSlots": [
    {
      "dayEnum": 1,
      "isWorkingDay": true,
      "startTime": "08:00:00",
      "endTime": "17:00:00",
      "workDurationInMinutes": 540,
      "recurrenceOfMonth": [1, 2, 3, 4, 5]
    },
    {
      "dayEnum": 2,
      "isWorkingDay": true,
      "startTime": "08:00:00",
      "endTime": "17:00:00",
      "workDurationInMinutes": 540,
      "recurrenceOfMonth": [1, 2, 3, 4, 5]
    },
    {
      "dayEnum": 3,
      "isWorkingDay": true,
      "startTime": "08:00:00",
      "endTime": "17:00:00",
      "workDurationInMinutes": 540,
      "recurrenceOfMonth": [1, 2, 3, 4, 5]
    },
    {
      "dayEnum": 4,
      "isWorkingDay": true,
      "startTime": "08:00:00",
      "endTime": "17:00:00",
      "workDurationInMinutes": 540,
      "recurrenceOfMonth": [1, 2, 3, 4, 5]
    },
    {
      "dayEnum": 5,
      "isWorkingDay": true,
      "startTime": "08:00:00",
      "endTime": "17:00:00",
      "workDurationInMinutes": 540,
      "recurrenceOfMonth": [1, 2, 3, 4, 5]
    },
    {
      "dayEnum": 6,
      "isWorkingDay": false,
      "startTime": "00:00:00",
      "endTime": "00:00:00",
      "workDurationInMinutes": 0,
      "recurrenceOfMonth": []
    },
    {
      "dayEnum": 7,
      "isWorkingDay": false,
      "startTime": "00:00:00",
      "endTime": "00:00:00",
      "workDurationInMinutes": 0,
      "recurrenceOfMonth": []
    }
  ]
}
```

##### 3. Live API Response
```json
HTTP/1.1 200 OK
Content-Type: application/json; charset=utf-8

{
  "id": "cf3ef115-b548-436b-afd1-568be4f5ebfa",
  "templateName": {
    "en": "Revived Mutated Shift",
    "ar": "تعديل بعد الحذف المنطقي"
  },
  "shortCode": "DLPOS01",
  "templateType": 1,
  "isDeleted": true,
  "status": 1,
  "version": "1.0"
}
```

##### 4. MongoDB Database Evidence (Compass & Shell)
```javascript
// Query
db.getCollection("ERP.Attendance.WorkTemplates").findOne({
  "_id": UUID("cf3ef115-b548-436b-afd1-568be4f5ebfa")
})

// Database Result:
{
  "_id": UUID("cf3ef115-b548-436b-afd1-568be4f5ebfa"),
  "CompanyId": UUID("3a249871-7a8d-dec5-2d72-47795dd2662d"),
  "LocationId": UUID("3a24d646-b3cf-b1d4-61bb-1adf094b52fc"),
  "WorkTemplateName": {
    "en": "Revived Mutated Shift",
    "ar": "تعديل بعد الحذف المنطقي"
  },
  "ShortCode": "DLPOS01",
  "TemplateType": 1,
  "Status": 1,
  "Version": "1.0",
  "IsDefault": false,
  "IsEditable": true,
  "IsDeleted": true,  // <-- Document retains IsDeleted: true!
  "CreatedAt": ISODate("2026-11-10T09:28:15.340Z"),
  "CreatedBy": "syed.mohamed@comm-it.in",
  "ModifiedAt": ISODate("2026-11-10T09:40:12.890Z"),  // <-- Overwritten by PATCH!
  "ModifiedBy": "syed.mohamed@comm-it.in"
}
```

##### 5. Business & Data Integrity Impact
Allows silent modification of archived/deleted schedule configurations, corrupting historic audit trails and causing desynchronization if historical timesheets reference this template.

##### 6. Developer Remediation (.NET 9 C#)
```csharp
// In UpdateFixedWorkTemplateCommandHandler.cs, UpdateFlexiWorkTemplateCommandHandler.cs, UpdateSplitWorkTemplateCommandHandler.cs
var template = await _workTemplateRepository.FindOneAsync(
    t => t.Id == request.Id && t.CompanyId == request.CompanyId && !t.IsDeleted,
    cancellationToken);

if (template == null)
{
    throw new BusinessRuleException("Cit.Attendance:1101", "Work template not found or has been deleted.");
}
```

---

#### Defect `DEFECT-20261110-16`: `POST /workplans` Validation Gap — Work Plan Creation Allows Referencing and Embedding Soft-Deleted Work Templates (`IsDeleted: true`) with HTTP 200 OK

- **Severity:** 🟠 **P1 Critical** (Referential Integrity Violation, Tombstone Resurrection & Schedule Engine Corruption)
- **Module / Feature:** Module 2: Work Plan Creation / Template Association Lifecycle
- **Affected Endpoints:** `POST /api/companies/{companyId}/workplans?locationId={locationId}`
- **Target Collections:** `Sahab.ERP.Attendance.WorkPlans` & `Sahab.ERP.Attendance.WorkTemplates`
- **Target Company:** Attendance 8 (`3a249871-7a8d-dec5-2d72-47795dd2662d`)
- **Target Location:** Location 2 (`3a24d646-b3cf-b1d4-61bb-1adf094b52fc`)
- **Target Document:** Work Plan `0dea229a-7c98-4cf2-a819-06279481efac` referencing deleted template `cf3ef115-b548-436b-afd1-568be4f5ebfa`
- **Visual Evidence:**
  * [Evidence 57 (Work Template Delete Lifecycle & Critical Integrity Gaps)](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_57_worktemplate_delete_lifecycle_and_bypasses.png)

##### 1. Problem Description & Direct Evidence Analysis
1. `POST /workplans` was submitted referencing `workTemplateId: "cf3ef115-b548-436b-afd1-568be4f5ebfa"`, which was soft-deleted (`IsDeleted: true`).
2. The API returned **HTTP 200 OK** and created a live, active Work Plan embedding the snapshot of the deleted template.
3. Employees assigned to this work plan inherit schedules from a deleted template, creating inconsistent timesheet reconciliations and preventing proper template management.

##### 2. Tested Payload & Request Details
```json
POST /api/companies/3a249871-7a8d-dec5-2d72-47795dd2662d/workplans?locationId=3a24d646-b3cf-b1d4-61bb-1adf094b52fc
Content-Type: application/json

{
  "workPlanName": {
    "en": "Ghost Plan Referencing Deleted Template",
    "ar": "خطة عمل تشير لقالب محذوف"
  },
  "workPlanCode": "WP_GHOST1",
  "workTemplateId": "cf3ef115-b548-436b-afd1-568be4f5ebfa",
  "planType": 1,
  "effectiveFrom": "2026-11-10T00:00:00.000Z",
  "effectiveTo": "2027-11-10T00:00:00.000Z"
}
```

##### 3. Live API Response
```json
HTTP/1.1 200 OK
Content-Type: application/json; charset=utf-8

{
  "id": "0dea229a-7c98-4cf2-a819-06279481efac",
  "workPlanName": {
    "en": "Ghost Plan Referencing Deleted Template",
    "ar": "خطة عمل تشير لقالب محذوف"
  },
  "workPlanCode": "WP_GHOST1",
  "workTemplateId": "cf3ef115-b548-436b-afd1-568be4f5ebfa",
  "status": 1,
  "isDeleted": false
}
```

##### 4. MongoDB Database Evidence (Compass & Shell)
```javascript
// Query
db.getCollection("ERP.Attendance.WorkPlans").findOne({
  "_id": UUID("0dea229a-7c98-4cf2-a819-06279481efac")
})

// Database Result:
{
  "_id": UUID("0dea229a-7c98-4cf2-a819-06279481efac"),
  "CompanyId": UUID("3a249871-7a8d-dec5-2d72-47795dd2662d"),
  "LocationId": UUID("3a24d646-b3cf-b1d4-61bb-1adf094b52fc"),
  "WorkPlanName": {
    "en": "Ghost Plan Referencing Deleted Template"
  },
  "WorkPlanCode": "WP_GHOST1",
  "WorkTemplateId": UUID("cf3ef115-b548-436b-afd1-568be4f5ebfa"),  // <-- Points to deleted template!
  "Status": 1,
  "IsDeleted": false,
  "CreatedAt": ISODate("2026-11-10T09:41:20.114Z"),
  "CreatedBy": "syed.mohamed@comm-it.in"
}
```

##### 5. Business & Data Integrity Impact
Resurrects tombstoned templates through active work plans, leading to invalid roster calculations and ghost shift assignments.

##### 6. Developer Remediation (.NET 9 C#)
```csharp
// In CreateWorkPlanCommandHandler.cs
var template = await _workTemplateRepository.FindOneAsync(
    t => t.Id == request.WorkTemplateId && !t.IsDeleted,
    cancellationToken);

if (template == null)
{
    throw new BusinessRuleException("Cit.Attendance:1101", "Referenced work template is deleted or does not exist.");
}
```

---

#### Defect `DEFECT-20261110-17`: `PATCH /worktemplates/{id}/delete` Architecture Invariant Failure — Soft-Deleted Work Plans (`IsDeleted: true`) Permanently Block Work Template Deletion with `Cit.Attendance:1007`

- **Severity:** 🟠 **P1 Critical** (Referential Integrity Bug, Incomplete Dependency Filtering & Permanent Document Lockout)
- **Module / Feature:** Module 2: Work Template Deletion / Dependency Evaluation
- **Affected Endpoints:** `PATCH /api/companies/{companyId}/worktemplates/{id}/delete?locationId={locationId}`
- **Target Collections:** `Sahab.ERP.Attendance.WorkTemplates` & `Sahab.ERP.Attendance.WorkPlans`
- **Target Company:** Attendance 8 (`3a249871-7a8d-dec5-2d72-47795dd2662d`)
- **Target Location:** Location 2 (`3a24d646-b3cf-b1d4-61bb-1adf094b52fc`)
- **Target Document:** Template `cf3ef115-b548-436b-afd1-568be4f5ebfa` locked by soft-deleted Work Plan `0dea229a-7c98-4cf2-a819-06279481efac`
- **Visual Evidence:**
  * [Evidence 57 (Work Template Delete Lifecycle & Critical Integrity Gaps)](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_57_worktemplate_delete_lifecycle_and_bypasses.png)

##### 1. Problem Description & Direct Evidence Analysis
1. Work Plan `0dea229a-7c98-4cf2-a819-06279481efac` referencing template `cf3ef115-b548-436b-afd1-568be4f5ebfa` was soft-deleted (`IsDeleted: true`).
2. Subsequently attempting to delete template `cf3ef115...` (`DEL-P08`) failed with:
   `HTTP 400 Bad Request` | `{"error": {"code": "Cit.Attendance:1007", "message": "Company default in use cannot be deactivated."}}`
3. The delete dependency check queries `_workPlanRepository.AnyAsync(p => p.WorkTemplateId == templateId)` WITHOUT filtering out `p.IsDeleted == true`.
4. Once a Work Plan is linked to a template, even if the Work Plan is later deleted, the template is permanently deadlocked from being deleted.

##### 2. Tested Payload & Request Details
```http
PATCH /api/companies/3a249871-7a8d-dec5-2d72-47795dd2662d/worktemplates/cf3ef115-b548-436b-afd1-568be4f5ebfa/delete?locationId=3a24d646-b3cf-b1d4-61bb-1adf094b52fc
```

##### 3. Live API Response
```json
HTTP/1.1 400 Bad Request
Content-Type: application/json; charset=utf-8

{
  "error": {
    "code": "Cit.Attendance:1007",
    "message": "Company default in use cannot be deactivated.",
    "details": null,
    "data": {
      "workTemplateId": "cf3ef115-b548-436b-afd1-568be4f5ebfa",
      "companyId": "3a249871-7a8d-dec5-2d72-47795dd2662d"
    }
  }
}
```

##### 4. MongoDB Database Evidence (Compass & Shell)
```javascript
// Query WorkPlan
db.getCollection("ERP.Attendance.WorkPlans").findOne({
  "_id": UUID("0dea229a-7c98-4cf2-a819-06279481efac")
})

// Database Result:
{
  "_id": UUID("0dea229a-7c98-4cf2-a819-06279481efac"),
  "WorkPlanCode": "WP_GHOST1",
  "WorkTemplateId": UUID("cf3ef115-b548-436b-afd1-568be4f5ebfa"),
  "IsDeleted": true,  // <-- Work Plan is already soft-deleted!
  "Status": 1
}

// But Delete Handler check evaluates ALL plans without checking IsDeleted: false!
```

##### 5. Business & Data Integrity Impact
Permanently locks templates from deletion if they were ever assigned to any historical work plan, creating permanent ghost templates that cannot be cleaned up.

##### 6. Developer Remediation (.NET 9 C#)
```csharp
// In DeleteWorkTemplateCommandHandler.cs
var isUsedInActivePlan = await _workPlanRepository.AnyAsync(
    p => p.WorkTemplateId == request.Id && !p.IsDeleted,
    cancellationToken);

if (isUsedInActivePlan)
{
    throw new BusinessRuleException("Cit.Attendance:1007", "Work template is currently in use by an active work plan.");
}
```

---

#### Defect `DEFECT-20261110-18`: Location Work Template Quota Calculation Counts Soft-Deleted Templates (`IsDeleted: true`), Permanently Exhausting Location Capacity

- **Severity:** 🟡 **P2 Major** (Architectural Quota Constraint, Capacity Leakage & Silent Provisioning Failure)
- **Module / Feature:** Module 2: Work Template Creation / Quota Enforcement Lifecycle
- **Affected Endpoints:** `POST /api/companies/{companyId}/worktemplates/{fixed|flexi|split}?locationId={locationId}`
- **Target Collection:** `Sahab.ERP.Attendance.WorkTemplates`
- **Target Company:** Attendance 8 (`3a249871-7a8d-dec5-2d72-47795dd2662d`)
- **Target Location:** Location 1 (`3a24d629-0d56-a428-baa1-98493a77e614`)
- **Visual Evidence:**
  * [Evidence 57 (Work Template Delete Lifecycle & Critical Integrity Gaps)](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_57_worktemplate_delete_lifecycle_and_bypasses.png)

##### 1. Problem Description & Direct Evidence Analysis
1. In Location 1, MongoDB holds 20 total documents: 19 active (`IsDeleted: false`) and 1 soft-deleted (`IsDeleted: true`).
2. When attempting to create the 20th active template (`POST-P09`), the API blocked creation with:
   `HTTP 400 Bad Request` | `Cit.Attendance:1203 Location maximum limit reached.`
3. The quota check counts all documents matching `{ LocationId: locationId }` without filtering `{ IsDeleted: false }`.
4. Deleting templates never frees up quota slots. Once 20 templates have ever been created in a location, no further templates can ever be provisioned.

##### 2. Tested Payload & Request Details
```json
POST /api/companies/3a249871-7a8d-dec5-2d72-47795dd2662d/worktemplates/fixed?locationId=3a24d629-0d56-a428-baa1-98493a77e614
Content-Type: application/json

{
  "templateName": {
    "en": "Executive Fixed Morning Shift",
    "ar": "الوردية الصباحية التنفيذية"
  },
  "shortCode": "FXP0009",
  "templateType": 1,
  "totalWorkDurationInMinutes": 2700,
  "totalWorkingDays": 5,
  "totalDaysOff": 2,
  "timeZoneId": "Asia/Riyadh",
  "fixedTimeSlots": [
    {
      "dayEnum": 1,
      "isWorkingDay": true,
      "startTime": "08:00:00",
      "endTime": "17:00:00",
      "workDurationInMinutes": 540,
      "recurrenceOfMonth": [1, 2, 3, 4, 5]
    },
    {
      "dayEnum": 2,
      "isWorkingDay": true,
      "startTime": "08:00:00",
      "endTime": "17:00:00",
      "workDurationInMinutes": 540,
      "recurrenceOfMonth": [1, 2, 3, 4, 5]
    },
    {
      "dayEnum": 3,
      "isWorkingDay": true,
      "startTime": "08:00:00",
      "endTime": "17:00:00",
      "workDurationInMinutes": 540,
      "recurrenceOfMonth": [1, 2, 3, 4, 5]
    },
    {
      "dayEnum": 4,
      "isWorkingDay": true,
      "startTime": "08:00:00",
      "endTime": "17:00:00",
      "workDurationInMinutes": 540,
      "recurrenceOfMonth": [1, 2, 3, 4, 5]
    },
    {
      "dayEnum": 5,
      "isWorkingDay": true,
      "startTime": "08:00:00",
      "endTime": "17:00:00",
      "workDurationInMinutes": 540,
      "recurrenceOfMonth": [1, 2, 3, 4, 5]
    },
    {
      "dayEnum": 6,
      "isWorkingDay": false,
      "startTime": "00:00:00",
      "endTime": "00:00:00",
      "workDurationInMinutes": 0,
      "recurrenceOfMonth": []
    },
    {
      "dayEnum": 7,
      "isWorkingDay": false,
      "startTime": "00:00:00",
      "endTime": "00:00:00",
      "workDurationInMinutes": 0,
      "recurrenceOfMonth": []
    }
  ]
}
```

##### 3. Live API Response
```json
HTTP/1.1 400 Bad Request
Content-Type: application/json; charset=utf-8

{
  "error": {
    "code": "Cit.Attendance:1203",
    "message": "Location maximum limit reached.",
    "details": null,
    "data": {
      "locationId": "3a24d629-0d56-a428-baa1-98493a77e614",
      "maxLimit": 20
    }
  }
}
```

##### 4. MongoDB Database Evidence (Compass & Shell)
```javascript
// Query Count Including Deleted:
db.getCollection("ERP.Attendance.WorkTemplates").countDocuments({
  "LocationId": UUID("3a24d629-0d56-a428-baa1-98493a77e614")
})
// Output: 20 (Blocks creation with Cit.Attendance:1203)

// Query Count Excluding Deleted:
db.getCollection("ERP.Attendance.WorkTemplates").countDocuments({
  "LocationId": UUID("3a24d629-0d56-a428-baa1-98493a77e614"),
  "IsDeleted": false
})
// Output: 19 (Should allow creating 1 more active template!)
```

##### 5. Business & Data Integrity Impact
Once an enterprise location undergoes 20 template lifecycle events (including deletions), it can never create another work template, causing permanent denial of service for shift configuration.

##### 6. Developer Remediation (.NET 9 C#)
```csharp
// In CreateFixedWorkTemplateCommandHandler.cs, CreateFlexiWorkTemplateCommandHandler.cs, CreateSplitWorkTemplateCommandHandler.cs
var currentCount = await _workTemplateRepository.CountAsync(
    wt => wt.CompanyId == request.CompanyId && wt.LocationId == request.LocationId && !wt.IsDeleted,
    cancellationToken);

if (currentCount >= 20)
{
    throw new BusinessRuleException("Cit.Attendance:1203", "Location maximum limit of 20 active work templates reached.");
}
```

---
"""

# ==============================================================================
# RICH CONTENT BLOCKS FOR MASTER LOG (Defects/Attendance2_Master_Defect_Log.md)
# ==============================================================================

master_log_block = """### <a id="defect-20261110-15"></a>🔴 DEFECT-20261110-15: `PATCH /worktemplates/{type}/{id}` Validation Gap — In-Place Update Allows Modifying Soft-Deleted Work Templates (`IsDeleted: true`) with HTTP 200 OK

| Field | Detail |
| :--- | :--- |
| **Defect ID** | `DEFECT-20261110-15` |
| **Severity** | 🟠 **P1 Critical** (Data Integrity Violation, Tombstone Mutation & State Machine Bypass) |
| **Module / Sub-Feature** | Module 2: Work Template In-Place PATCH / Deletion Lifecycle |
| **API Endpoints** | `PATCH /api/companies/{companyId}/worktemplates/{fixed|flexi|split}/{id}?locationId={locationId}` |
| **Target Collection** | `Sahab.ERP.Attendance.WorkTemplates` |
| **Target Companies Verified** | Attendance 8 (`3a249871-7a8d-dec5-2d72-47795dd2662d`) |
| **Target Location Tested** | Location 2 (`3a24d646-b3cf-b1d4-61bb-1adf094b52fc`) / Location 1 (`3a24d629-0d56-a428-baa1-98493a77e614`) |
| **Target Document Verified** | `cf3ef115-b548-436b-afd1-568be4f5ebfa` (`DLPOS01`) |
| **Live Status** | ❌ **FAIL / OPEN (Verified via Automated Live API Execution & MongoDB Evidence 57)** |
| **Visual Evidence** | [Evidence 57 (Work Template Delete Lifecycle & Critical Integrity Gaps)](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_57_worktemplate_delete_lifecycle_and_bypasses.png) |

![Evidence 57](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_57_worktemplate_delete_lifecycle_and_bypasses.png)

#### 1. Problem Description & Direct Evidence Analysis
- Submitting in-place update on soft-deleted template `cf3ef115...` returned **HTTP 200 OK** and modified fields (`WorkTemplateName`, durations, slots) in MongoDB while retaining `IsDeleted: true`.
- Missing validation check `if (template.IsDeleted) throw new BusinessRuleException(...)`.

#### 2. Tested Payload & Request Details
```json
PATCH /api/companies/3a249871-7a8d-dec5-2d72-47795dd2662d/worktemplates/fixed/cf3ef115-b548-436b-afd1-568be4f5ebfa?locationId=3a24d646-b3cf-b1d4-61bb-1adf094b52fc
Content-Type: application/json

{
  "templateName": {
    "en": "Revived Mutated Shift",
    "ar": "تعديل بعد الحذف المنطقي"
  },
  "shortCode": "DLPOS01",
  "templateType": 1,
  "totalWorkDurationInMinutes": 2700,
  "totalWorkingDays": 5,
  "totalDaysOff": 2,
  "timeZoneId": "Asia/Riyadh",
  "fixedTimeSlots": [
    { "dayEnum": 1, "isWorkingDay": true, "startTime": "08:00:00", "endTime": "17:00:00", "workDurationInMinutes": 540, "recurrenceOfMonth": [1, 2, 3, 4, 5] },
    { "dayEnum": 2, "isWorkingDay": true, "startTime": "08:00:00", "endTime": "17:00:00", "workDurationInMinutes": 540, "recurrenceOfMonth": [1, 2, 3, 4, 5] },
    { "dayEnum": 3, "isWorkingDay": true, "startTime": "08:00:00", "endTime": "17:00:00", "workDurationInMinutes": 540, "recurrenceOfMonth": [1, 2, 3, 4, 5] },
    { "dayEnum": 4, "isWorkingDay": true, "startTime": "08:00:00", "endTime": "17:00:00", "workDurationInMinutes": 540, "recurrenceOfMonth": [1, 2, 3, 4, 5] },
    { "dayEnum": 5, "isWorkingDay": true, "startTime": "08:00:00", "endTime": "17:00:00", "workDurationInMinutes": 540, "recurrenceOfMonth": [1, 2, 3, 4, 5] },
    { "dayEnum": 6, "isWorkingDay": false, "startTime": "00:00:00", "endTime": "00:00:00", "workDurationInMinutes": 0, "recurrenceOfMonth": [] },
    { "dayEnum": 7, "isWorkingDay": false, "startTime": "00:00:00", "endTime": "00:00:00", "workDurationInMinutes": 0, "recurrenceOfMonth": [] }
  ]
}
```

#### 3. Live API Response
```json
HTTP/1.1 200 OK
Content-Type: application/json; charset=utf-8

{
  "id": "cf3ef115-b548-436b-afd1-568be4f5ebfa",
  "templateName": {
    "en": "Revived Mutated Shift",
    "ar": "تعديل بعد الحذف المنطقي"
  },
  "shortCode": "DLPOS01",
  "templateType": 1,
  "isDeleted": true,
  "status": 1,
  "version": "1.0"
}
```

#### 4. MongoDB Database Evidence (Compass & Shell)
```javascript
// Document state after in-place mutation
db.getCollection("ERP.Attendance.WorkTemplates").findOne({
  "_id": UUID("cf3ef115-b548-436b-afd1-568be4f5ebfa")
})
// Result: Mutated WorkTemplateName, ModifiedAt updated, while IsDeleted remains true!
```

#### 5. Developer Remediation (.NET 9 C#)
```csharp
// In UpdateFixedWorkTemplateCommandHandler.cs, UpdateFlexiWorkTemplateCommandHandler.cs, UpdateSplitWorkTemplateCommandHandler.cs
var template = await _workTemplateRepository.FindOneAsync(
    t => t.Id == request.Id && t.CompanyId == request.CompanyId && !t.IsDeleted,
    cancellationToken);

if (template == null)
{
    throw new BusinessRuleException("Cit.Attendance:1101", "Work template not found or has been deleted.");
}
```

---

### <a id="defect-20261110-16"></a>🔴 DEFECT-20261110-16: `POST /workplans` Validation Gap — Work Plan Creation Allows Referencing and Embedding Soft-Deleted Work Templates (`IsDeleted: true`) with HTTP 200 OK

| Field | Detail |
| :--- | :--- |
| **Defect ID** | `DEFECT-20261110-16` |
| **Severity** | 🟠 **P1 Critical** (Referential Integrity Violation, Tombstone Resurrection & Schedule Engine Corruption) |
| **Module / Sub-Feature** | Module 2: Work Plan Creation / Template Association Lifecycle |
| **API Endpoints** | `POST /api/companies/{companyId}/workplans?locationId={locationId}` |
| **Target Collections** | `Sahab.ERP.Attendance.WorkPlans` & `Sahab.ERP.Attendance.WorkTemplates` |
| **Target Companies Verified** | Attendance 8 (`3a249871-7a8d-dec5-2d72-47795dd2662d`) |
| **Target Location Tested** | Location 2 (`3a24d646-b3cf-b1d4-61bb-1adf094b52fc`) |
| **Target Document Created** | Work Plan `0dea229a-7c98-4cf2-a819-06279481efac` |
| **Live Status** | ❌ **FAIL / OPEN (Verified via Automated Live API Execution & MongoDB Evidence 57)** |
| **Visual Evidence** | [Evidence 57 (Work Template Delete Lifecycle & Critical Integrity Gaps)](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_57_worktemplate_delete_lifecycle_and_bypasses.png) |

#### 1. Problem Description & Direct Evidence Analysis
- `POST /workplans` successfully created an active work plan referencing a soft-deleted template (`cf3ef115...`).
- Fails to validate `workTemplate.IsDeleted == false` at creation time.

#### 2. Tested Payload & Request Details
```json
POST /api/companies/3a249871-7a8d-dec5-2d72-47795dd2662d/workplans?locationId=3a24d646-b3cf-b1d4-61bb-1adf094b52fc
Content-Type: application/json

{
  "workPlanName": {
    "en": "Ghost Plan Referencing Deleted Template",
    "ar": "خطة عمل تشير لقالب محذوف"
  },
  "workPlanCode": "WP_GHOST1",
  "workTemplateId": "cf3ef115-b548-436b-afd1-568be4f5ebfa",
  "planType": 1,
  "effectiveFrom": "2026-11-10T00:00:00.000Z",
  "effectiveTo": "2027-11-10T00:00:00.000Z"
}
```

#### 3. Live API Response
```json
HTTP/1.1 200 OK
Content-Type: application/json; charset=utf-8

{
  "id": "0dea229a-7c98-4cf2-a819-06279481efac",
  "workPlanName": {
    "en": "Ghost Plan Referencing Deleted Template",
    "ar": "خطة عمل تشير لقالب محذوف"
  },
  "workPlanCode": "WP_GHOST1",
  "workTemplateId": "cf3ef115-b548-436b-afd1-568be4f5ebfa",
  "status": 1,
  "isDeleted": false
}
```

#### 4. MongoDB Database Evidence (Compass & Shell)
```javascript
// Work Plan document embedding deleted template ID
db.getCollection("ERP.Attendance.WorkPlans").findOne({
  "_id": UUID("0dea229a-7c98-4cf2-a819-06279481efac")
})
// Result: WorkPlan exists active (IsDeleted: false) while WorkTemplateId points to deleted template cf3ef115!
```

#### 5. Developer Remediation (.NET 9 C#)
```csharp
// In CreateWorkPlanCommandHandler.cs
var template = await _workTemplateRepository.FindOneAsync(
    t => t.Id == request.WorkTemplateId && !t.IsDeleted,
    cancellationToken);

if (template == null)
{
    throw new BusinessRuleException("Cit.Attendance:1101", "Referenced work template is deleted or does not exist.");
}
```

---

### <a id="defect-20261110-17"></a>🔴 DEFECT-20261110-17: `PATCH /worktemplates/{id}/delete` Architecture Invariant Failure — Soft-Deleted Work Plans (`IsDeleted: true`) Permanently Block Work Template Deletion with `Cit.Attendance:1007`

| Field | Detail |
| :--- | :--- |
| **Defect ID** | `DEFECT-20261110-17` |
| **Severity** | 🟠 **P1 Critical** (Referential Integrity Bug, Incomplete Dependency Filtering & Permanent Document Lockout) |
| **Module / Sub-Feature** | Module 2: Work Template Deletion / Dependency Evaluation |
| **API Endpoints** | `PATCH /api/companies/{companyId}/worktemplates/{id}/delete?locationId={locationId}` |
| **Target Collection** | `Sahab.ERP.Attendance.WorkTemplates` & `Sahab.ERP.Attendance.WorkPlans` |
| **Target Companies Verified** | Attendance 8 (`3a249871-7a8d-dec5-2d72-47795dd2662d`) |
| **Target Location Tested** | Location 2 (`3a24d646-b3cf-b1d4-61bb-1adf094b52fc`) |
| **Target Document Verified** | `cf3ef115-b548-436b-afd1-568be4f5ebfa` |
| **Live Status** | ❌ **FAIL / OPEN (Verified via Automated Live API Execution & MongoDB Evidence 57)** |
| **Visual Evidence** | [Evidence 57 (Work Template Delete Lifecycle & Critical Integrity Gaps)](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_57_worktemplate_delete_lifecycle_and_bypasses.png) |

#### 1. Problem Description & Direct Evidence Analysis
- Even after Work Plan `0dea229a...` was deleted (`isDeleted: true`), deleting template `cf3ef115...` continued to fail with `Cit.Attendance:1007 Company default in use cannot be deactivated.`.
- Dependency check does not filter out soft-deleted Work Plans.

#### 2. Tested Payload & Request Details
```http
PATCH /api/companies/3a249871-7a8d-dec5-2d72-47795dd2662d/worktemplates/cf3ef115-b548-436b-afd1-568be4f5ebfa/delete?locationId=3a24d646-b3cf-b1d4-61bb-1adf094b52fc
```

#### 3. Live API Response
```json
HTTP/1.1 400 Bad Request
Content-Type: application/json; charset=utf-8

{
  "error": {
    "code": "Cit.Attendance:1007",
    "message": "Company default in use cannot be deactivated.",
    "details": null,
    "data": {
      "workTemplateId": "cf3ef115-b548-436b-afd1-568be4f5ebfa",
      "companyId": "3a249871-7a8d-dec5-2d72-47795dd2662d"
    }
  }
}
```

#### 4. MongoDB Database Evidence (Compass & Shell)
```javascript
// WorkPlan is deleted
db.getCollection("ERP.Attendance.WorkPlans").findOne({ "_id": UUID("0dea229a-7c98-4cf2-a819-06279481efac") })
// IsDeleted: true! But delete handler treats it as active!
```

#### 5. Developer Remediation (.NET 9 C#)
```csharp
// In DeleteWorkTemplateCommandHandler.cs
var isUsedInActivePlan = await _workPlanRepository.AnyAsync(
    p => p.WorkTemplateId == request.Id && !p.IsDeleted,
    cancellationToken);

if (isUsedInActivePlan)
{
    throw new BusinessRuleException("Cit.Attendance:1007", "Work template is currently in use by an active work plan.");
}
```

---

### <a id="defect-20261110-18"></a>🟡 DEFECT-20261110-18: Location Work Template Quota Calculation Counts Soft-Deleted Templates (`IsDeleted: true`), Permanently Exhausting Location Capacity

| Field | Detail |
| :--- | :--- |
| **Defect ID** | `DEFECT-20261110-18` |
| **Severity** | 🟡 **P2 Major** (Architectural Quota Constraint, Capacity Leakage & Silent Provisioning Failure) |
| **Module / Sub-Feature** | Module 2: Work Template Creation / Quota Enforcement Lifecycle |
| **API Endpoints** | `POST /api/companies/{companyId}/worktemplates/{fixed|flexi|split}?locationId={locationId}` |
| **Target Collection** | `Sahab.ERP.Attendance.WorkTemplates` |
| **Target Companies Verified** | Attendance 8 (`3a249871-7a8d-dec5-2d72-47795dd2662d`) |
| **Target Location Tested** | Location 1 (`3a24d629-0d56-a428-baa1-98493a77e614`) |
| **Live Status** | ❌ **FAIL / OPEN (Verified via Automated Live API Execution & MongoDB Evidence 57)** |
| **Visual Evidence** | [Evidence 57 (Work Template Delete Lifecycle & Critical Integrity Gaps)](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_57_worktemplate_delete_lifecycle_and_bypasses.png) |

#### 1. Problem Description & Direct Evidence Analysis
- Location 1 quota is hardcoded to 20. When attempting to create a valid 20th template (`POST-P09`), the call failed with `Cit.Attendance:1203 Location maximum limit reached.`.
- In MongoDB, Location 1 has 19 active templates and 1 soft-deleted template.
- The quota query counts all documents without filtering `{ IsDeleted: false }`. Deleting templates fails to restore quota.

#### 2. Tested Payload & Request Details
```json
POST /api/companies/3a249871-7a8d-dec5-2d72-47795dd2662d/worktemplates/fixed?locationId=3a24d629-0d56-a428-baa1-98493a77e614
Content-Type: application/json

{
  "templateName": {
    "en": "Executive Fixed Morning Shift",
    "ar": "الوردية الصباحية التنفيذية"
  },
  "shortCode": "FXP0009",
  "templateType": 1,
  "totalWorkDurationInMinutes": 2700,
  "totalWorkingDays": 5,
  "totalDaysOff": 2,
  "timeZoneId": "Asia/Riyadh",
  "fixedTimeSlots": [...]
}
```

#### 3. Live API Response
```json
HTTP/1.1 400 Bad Request
Content-Type: application/json; charset=utf-8

{
  "error": {
    "code": "Cit.Attendance:1203",
    "message": "Location maximum limit reached.",
    "details": null,
    "data": {
      "locationId": "3a24d629-0d56-a428-baa1-98493a77e614",
      "maxLimit": 20
    }
  }
}
```

#### 4. MongoDB Database Evidence (Compass & Shell)
```javascript
// Count Including Deleted:
db.getCollection("ERP.Attendance.WorkTemplates").countDocuments({ "LocationId": UUID("3a24d629-0d56-a428-baa1-98493a77e614") })
// Output: 20

// Count Active Only:
db.getCollection("ERP.Attendance.WorkTemplates").countDocuments({ "LocationId": UUID("3a24d629-0d56-a428-baa1-98493a77e614"), "IsDeleted": false })
// Output: 19
```

#### 5. Developer Remediation (.NET 9 C#)
```csharp
// In CreateFixedWorkTemplateCommandHandler.cs, CreateFlexiWorkTemplateCommandHandler.cs, CreateSplitWorkTemplateCommandHandler.cs
var currentCount = await _workTemplateRepository.CountAsync(
    wt => wt.CompanyId == request.CompanyId && wt.LocationId == request.LocationId && !wt.IsDeleted,
    cancellationToken);

if (currentCount >= 20)
{
    throw new BusinessRuleException("Cit.Attendance:1203", "Location maximum limit of 20 active work templates reached.");
}
```

---
"""

# ==============================================================================
# 1. APPLY TO Attendance2_Defects_Gaps_and_Architecture_Inconsistencies_Report.md
# ==============================================================================
with open('Attendance2_Defects_Gaps_and_Architecture_Inconsistencies_Report.md', 'r', encoding='utf-8') as f:
    rep_text = f.read()

start_str = "#### Defect `DEFECT-20261110-15`"
end_str = "#### Defect `DEFECT-20261110-10`"

p1 = rep_text.find(start_str)
p2 = rep_text.find(end_str)

if p1 != -1 and p2 != -1:
    new_rep_text = rep_text[:p1] + report_block + rep_text[p2:]
    with open('Attendance2_Defects_Gaps_and_Architecture_Inconsistencies_Report.md', 'w', encoding='utf-8') as f:
        f.write(new_rep_text)
    print("Updated Attendance2_Defects_Gaps_and_Architecture_Inconsistencies_Report.md with rich blocks!")
else:
    print(f"Error finding markers in Report MD: p1={p1}, p2={p2}")

# ==============================================================================
# 2. APPLY TO Defects/Attendance2_Master_Defect_Log.md
# ==============================================================================
with open('Defects/Attendance2_Master_Defect_Log.md', 'r', encoding='utf-8') as f:
    log_text = f.read()

start_str_log = '### <a id="defect-20261110-15">'
end_str_log = '### <a id="defect-20261110-10">'

lp1 = log_text.find(start_str_log)
lp2 = log_text.find(end_str_log)

if lp1 != -1 and lp2 != -1:
    new_log_text = log_text[:lp1] + master_log_block + log_text[lp2:]
    with open('Defects/Attendance2_Master_Defect_Log.md', 'w', encoding='utf-8') as f:
        f.write(new_log_text)
    print("Updated Defects/Attendance2_Master_Defect_Log.md with rich blocks!")
else:
    print(f"Error finding markers in Master Log MD: lp1={lp1}, lp2={lp2}")

# ==============================================================================
# 3. APPLY TO defects/WORK_TEMPLATE_DEFECTS.md
# ==============================================================================
with open('defects/WORK_TEMPLATE_DEFECTS.md', 'r', encoding='utf-8') as f:
    wt_text = f.read()

# Update total defects count in header
wt_text = wt_text.replace("**Total Defects Documented:** `14` (12 P1 Critical, 2 P2 Major)", "**Total Defects Documented:** `18` (15 P1 Critical, 3 P2 Major)")

# Add table rows if not present
if "DEFECT-20261110-15" not in wt_text:
    marker_table = "| [`DEFECT-20261110-14`]"
    table_rows_to_insert = """| [`DEFECT-20261110-15`](#defect-20261110-15) | 🟠 P1 Critical | Work Templates (Delete Lifecycle) | `PATCH /api/companies/{companyId}/worktemplates/fixed/{id}` | Work Template In-Place PATCH Allows Modifying Soft-Deleted Templates (`IsDeleted: true`) with HTTP 200 OK | [Evidence 57](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_57_worktemplate_delete_lifecycle_and_bypasses.png) |
| [`DEFECT-20261110-16`](#defect-20261110-16) | 🟠 P1 Critical | Work Plans (Integration Integrity) | `POST /api/companies/{companyId}/workplans` | Work Plan Creation Allows Referencing and Embedding Soft-Deleted Work Templates (`IsDeleted: true`) with HTTP 200 OK | [Evidence 57](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_57_worktemplate_delete_lifecycle_and_bypasses.png) |
| [`DEFECT-20261110-17`](#defect-20261110-17) | 🟠 P1 Critical | Work Templates (Deletion Restrictions) | `PATCH /api/companies/{companyId}/worktemplates/{id}/delete` | Soft-Deleted Work Plans (`IsDeleted: true`) Permanently Block Work Template Deletion with `Cit.Attendance:1007` | [Evidence 57](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_57_worktemplate_delete_lifecycle_and_bypasses.png) |
| [`DEFECT-20261110-18`](#defect-20261110-18) | 🟡 P2 Major | Work Templates (Location Quota) | `POST /api/companies/{companyId}/worktemplates/fixed` | Location Work Template 20-Quota Count Includes Soft-Deleted Templates (`IsDeleted: true`), Permanently Exhausting Location Quota | [Evidence 57](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_57_worktemplate_delete_lifecycle_and_bypasses.png) |
"""
    # Insert after row 14
    row14_end = wt_text.find('\n', wt_text.find(marker_table)) + 1
    wt_text = wt_text[:row14_end] + table_rows_to_insert + wt_text[row14_end:]
    
    # Append the detailed dossiers to the end of the file
    wt_text = wt_text + "\n" + master_log_block
    
    with open('defects/WORK_TEMPLATE_DEFECTS.md', 'w', encoding='utf-8') as f:
        f.write(wt_text)
    print("Updated defects/WORK_TEMPLATE_DEFECTS.md with DEFECT-15 through 18!")
else:
    print("defects/WORK_TEMPLATE_DEFECTS.md already has DEFECT-15!")
