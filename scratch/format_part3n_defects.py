# -*- coding: utf-8 -*-
part3n_content = """

---

### 🏢 Part 3N: Defects Identified on 16 November 2026 — Work Template Module: Location Shifts Live API & MongoDB Audit (`DEFECT-20261116-01` to `DEFECT-20261116-06`)

<a id="-part-3n-defects-identified-on-16-november-2026--work-template-module--location-shifts-live-api--mongodb-audit-defect-20261116-01-to-06"></a>

> **Audit Execution Date:** **16 November 2026 (Day 12 Update — Location Shifts Full Audit)**  
> **Target Environment:** DEV (`https://attendance2.dev.zoolwork.com` / `https://company8.dev.zoolwork.com`)  
> **Database Collections Inspected:** MongoDB `10.1.0.4:27018` — `Sahab.ERP.Attendance.WorkTemplates`, `Sahab.ERP.Attendance.WorkPlans`  
> **Test Suite Executed:** `WT - Location Shifts` Sheet in `AttendanceTestCases_Master_Consolidated.xlsx` (112 Test Cases: `DOC-A-01` to `DOC-E-01`, `ROOT-A-00` to `ROOT-G-09`, `LOC-WT-105` to `LOC-WT-113`)  
> **Confluence Sync:** Published to Confluence Page [**`Bug Fixes Testing`** (Page ID: `1567653890`)](https://zoolworks.atlassian.net/wiki/spaces/AM/pages/1567653890/Bug+Fixes+Testing) as **Rows 79 to 84** (Version 22 Active)  
> **Handover Status:** ⚠️ **Pending Developer Handover (Not Fixed / Live Reproduced on 16-Nov-2026)**  

---

#### Defect `DEFECT-20261116-01`: In-Place Location Work Template PATCH Wipes Out Creation Audit Metadata — `CreatedAt` Overwritten with `0001-01-01T00:00:00.000Z` (`DateTime.MinValue`) and `CreatedBy` Reset to `null` in MongoDB

<a id="defect-20261116-01"></a>

- **Defect ID:** `DEFECT-20261116-01` | **Confluence Tracking:** **Row 79**
- **Severity:** 🟠 **P1 Critical** (Audit Trail Destruction, ISO/SOC-2 Compliance Failure & Full-Document Overwrite Anti-Pattern)
- **Component:** Work Template Location Management (`PATCH /api/companies/{companyId}/worktemplates/fixed/{id}`)
- **Microservices Involved:** `SP.AttendanceSvc` (.NET 9 Web API)
- **Database Collection:** `Sahab.ERP.Attendance.WorkTemplates`
- **Environment:** DEV | Verified on Baseline Company `Attendance 8` & Fresh Tenant `Attendance 12`
- **Visual Evidence:** [Evidence 54 (Location Post-PATCH Audit Wipeout Compass Screenshot)](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_54_regular_shift_location_post_patch_audit_wipeout_compass.png)
- **Related Test Cases:** `DOC-B-01`, `ROOT-B-05`, `LOC-WT-108`

##### 1. Defect Summary & Root Cause
When an administrator edits an existing location Fixed Work Template via `PATCH /api/companies/{companyId}/worktemplates/fixed/{id}?locationId={locationId}`, the API returns `HTTP 200 OK: {"message":"Fixed work template patched successfully"}`. However, inspecting the document in MongoDB Compass reveals that the repository update handler executes a full-document replacement (`ReplaceOneAsync`) using a deserialized entity model whose creation fields are unpopulated. As a result:
1. `CreatedAt` is permanently overwritten with `0001-01-01T00:00:00.000Z` (`DateTime.MinValue`).
2. `CreatedBy` is reset from its original user identity to `null`.
3. Historical audit tracking is completely erased, violating regulatory compliance and audit logging requirements.

##### 2. Live Reproduction Steps & Payloads
1. Create a Location Fixed Work Template via `POST /worktemplates/fixed?locationId={locId}`. Note the original `CreatedAt` timestamp (e.g. `2026-11-10T08:15:22.140Z`) and `CreatedBy` (e.g. `"syed.mohamed@comm-it.in"`).
2. Execute an in-place PATCH to update working hours:
   ```http
   PATCH /api/companies/3a249871-7a8d-dec5-2d72-47795dd2662d/worktemplates/fixed/c9e00652-eae5-429a-bef0-4d4ddf9e0a0f?locationId=3a24d629-0d56-a428-baa1-98493a77e614
   Content-Type: application/json
   Authorization: Bearer <valid_jwt>

   {
     "templateName": { "en": "Updated Shift Morning", "ar": "وردية الصباح المعدلة" },
     "totalWorkDurationInMinutes": 2400,
     "fixedTimeSlots": [
       { "workDurationInMinutes": 480, "dayEnum": "Monday", "isWorkingDay": true, "recurrenceOfMonth": [1,2,3,4,5], "startTime": "08:30:00", "endTime": "16:30:00" },
       { "workDurationInMinutes": 480, "dayEnum": "Tuesday", "isWorkingDay": true, "recurrenceOfMonth": [1,2,3,4,5], "startTime": "08:30:00", "endTime": "16:30:00" },
       { "workDurationInMinutes": 480, "dayEnum": "Wednesday", "isWorkingDay": true, "recurrenceOfMonth": [1,2,3,4,5], "startTime": "08:30:00", "endTime": "16:30:00" },
       { "workDurationInMinutes": 480, "dayEnum": "Thursday", "isWorkingDay": true, "recurrenceOfMonth": [1,2,3,4,5], "startTime": "08:30:00", "endTime": "16:30:00" },
       { "workDurationInMinutes": 480, "dayEnum": "Friday", "isWorkingDay": true, "recurrenceOfMonth": [1,2,3,4,5], "startTime": "08:30:00", "endTime": "16:30:00" }
     ]
   }
   ```
3. Observe HTTP Response: `HTTP 200 OK: {"message":"Fixed work template patched successfully"}`.
4. Query document `c9e00652-eae5-429a-bef0-4d4ddf9e0a0f` in MongoDB Compass (`ERP.Attendance.WorkTemplates`):
   ```json
   {
     "_id": UUID("c9e00652-eae5-429a-bef0-4d4ddf9e0a0f"),
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
- **Visual Evidence:** [Evidence 55 (Quota Ceiling Proof)](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_55_fixed_wt_location_patch_validation_bypasses_and_db_results.png) & [Evidence 57 (Delete Lifecycle)](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_57_worktemplate_delete_lifecycle_and_bypasses.png)
- **Related Test Cases:** `DOC-A-04`, `ROOT-A-04`, `LOC-WT-112`

##### 1. Defect Summary & Root Cause
The backend enforces an arbitrary, undocumented ceiling of **exactly 20 work templates per location**. When a 21st template creation is attempted, the microservice throws:
`HTTP 400 Bad Request: {"errorCode":"Cit.Attendance:1203","message":"Location maximum limit reached.","data":{"MaxWorkTemplateCount":20,"CurrentWorkTemplateCount":20}}`.
Critically, the count query `CountDocumentsAsync(filter)` checks `CompanyId` and `LocationId`, but **omits `x.IsDeleted == false`**. Therefore, soft-deleted templates (`IsDeleted: true`) continue to be counted against the 20-template limit, permanently exhausting quota slots and preventing companies from ever creating new templates in that location.

##### 2. Developer Remediation (.NET 9 C#)
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
- **Visual Evidence:** [Evidence 57 (Soft-Deleted Plan Blocks Template Deletion Proof)](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_57_worktemplate_delete_lifecycle_and_bypasses.png)
- **Related Test Cases:** `DOC-C-08`, `ROOT-E-04`

##### 1. Defect Summary & Root Cause
When an administrator deletes a location Work Template via `PATCH /worktemplates/{id}/delete?locationId={locId}`, the deletion validator queries `ERP.Attendance.WorkPlans` to determine whether the template is currently in use. However, the LINQ query queries **all** work plans referencing `WorkTemplateId`, including work plans that are themselves soft-deleted (`IsDeleted: true`). 
Because deleted work plans are never purged, any work template that was *ever* assigned to a now-deleted work plan is **permanently locked** and can never be deleted, returning:
`HTTP 400 Bad Request: {"errorCode":"Cit.Attendance:1007","message":"Company default in use cannot be deactivated or deleted."}`.

##### 2. Developer Remediation (.NET 9 C#)
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
- **Visual Evidence:** [Evidence 57 (Soft-Deleted Entity Mutated via PATCH)](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_57_worktemplate_delete_lifecycle_and_bypasses.png)
- **Related Test Cases:** `DOC-D-06`, `ROOT-E-07`

##### 1. Defect Summary & Root Cause
When a work template is deleted via `PATCH /{id}/delete`, the backend sets `IsDeleted: true`. If a client subsequently sends `PATCH /worktemplates/fixed/{id}?locationId={locId}` or `PATCH /flexi/{id}` with an updated schedule, the update handler retrieves the document by ID without asserting `!x.IsDeleted`. The service accepts the mutation, responds with `HTTP 200 OK`, and updates the underlying tombstoned document in MongoDB. This creates ghost mutations on deleted entities.

##### 2. Developer Remediation (.NET 9 C#)
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
- **Visual Evidence:** [Evidence 56 (Polymorphic Validation Bypasses)](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_56_flexi_split_location_validation_bypasses_and_db_results.png)
- **Related Test Cases:** `DOC-B-02`

##### 1. Defect Summary & Root Cause
When an in-place PATCH is called on a Fixed Work Template with `"templateType": "Flexi"` or `"templateType": 2`, the endpoint updates MongoDB discriminator property `_t: ["WorkTemplate", "FlexiWorkTemplate"]` and changes `TemplateType: 2`, but fails to clear legacy `FixedTimeSlots` or validate mandatory `FlexiTimeSlots` fields. This causes polymorphic document corruption where the C# BsonSerializer fails on subsequent reads with `BsonSerializationException: Element 'FixedTimeSlots' does not match any field or property of class FlexiWorkTemplate`.

##### 2. Developer Remediation (.NET 9 C#)
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
- **Visual Evidence:** [Evidence 55 (Fixed WT Location PATCH Validation Bypasses & DB Results)](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_55_fixed_wt_location_patch_validation_bypasses_and_db_results.png)
- **Related Test Cases:** `ROOT-B-00`, `LOC-WT-109`, `LOC-WT-110`, `LOC-WT-111`

##### 1. Defect Summary & Root Cause
`UpdateFixedWorkTemplateValidator` omits basic domain invariants present in other services:
1. **Recurrence Index 6 Accepted:** Accepts `recurrenceOfMonth: [6]` on working days with `HTTP 200 OK`, persisting into MongoDB despite calendar months having at most 5 weeks.
2. **Duration Math Mismatch Accepted:** Accepts declared `totalWorkDurationInMinutes: 3000` while fixed time slots sum to `2700` minutes with `HTTP 200 OK`.
3. **Invalid Timezone Accepted:** Accepts arbitrary unverified timezone strings (e.g. `"timeZoneId": "Invalid/Timezone"`) with `HTTP 200 OK`, risking runtime unhandled crashes in calculation engine schedulers.

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

# Append to Defects/Attendance2_Master_Defect_Log.md
with open("Defects/Attendance2_Master_Defect_Log.md", "a", encoding="utf-8") as f:
    f.write(part3n_content)
print("Successfully appended Part 3N defects to Defects/Attendance2_Master_Defect_Log.md")

# Append to Attendance2_Defects_Gaps_and_Architecture_Inconsistencies_Report.md
with open("Attendance2_Defects_Gaps_and_Architecture_Inconsistencies_Report.md", "a", encoding="utf-8") as f:
    f.write(part3n_content)
print("Successfully appended Part 3N defects to Attendance2_Defects_Gaps_and_Architecture_Inconsistencies_Report.md")
