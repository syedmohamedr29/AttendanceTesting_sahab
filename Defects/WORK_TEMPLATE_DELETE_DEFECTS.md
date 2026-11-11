# Sahab ERP Attendance – Work Template Delete API Defect Dossier

**Document Version:** `1.0`  
**Execution Date:** `2026-11-10`  
**Total Defects Documented:** `4` (3 P1 Critical, 1 P2 Major)  
**Target Environment:** `DEV (attendance2.dev.zoolwork.com)`  
**API Endpoint:** `PATCH /api/companies/{companyId}/worktemplates/{id}/delete`  
**Target Collection:** `Sahab.ERP.Attendance.WorkTemplates` & `Sahab.ERP.Attendance.WorkPlans`  
**Visual Evidence Artifact:** [Evidence 57: Work Template Delete Lifecycle, Soft-Deletion & Architectural Gaps](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_57_worktemplate_delete_lifecycle_and_bypasses.png)  

---

## 1. Executive Defect Summary Table

| Defect ID | Severity | Module / Sub-Feature | Endpoint & Method | Defect Title | Visual Evidence |
| :--- | :---: | :--- | :--- | :--- | :--- |
| [`DEFECT-20261110-15`](#defect-20261110-15) | 🟠 P1 Critical | Work Templates (Delete Lifecycle) | `PATCH /api/companies/{companyId}/worktemplates/fixed/{id}` | Work Template In-Place PATCH Allows Modifying Soft-Deleted Templates (`IsDeleted: true`) with HTTP 200 OK | [Evidence 57](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_57_worktemplate_delete_lifecycle_and_bypasses.png) |
| [`DEFECT-20261110-16`](#defect-20261110-16) | 🟠 P1 Critical | Work Plans (Integration Integrity) | `POST /api/companies/{companyId}/workplans` | Work Plan Creation Allows Referencing and Embedding Soft-Deleted Work Templates (`IsDeleted: true`) with HTTP 200 OK | [Evidence 57](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_57_worktemplate_delete_lifecycle_and_bypasses.png) |
| [`DEFECT-20261110-17`](#defect-20261110-17) | 🟠 P1 Critical | Work Templates (Deletion Restrictions) | `PATCH /api/companies/{companyId}/worktemplates/{id}/delete` | Soft-Deleted Work Plans (`IsDeleted: true`) Permanently Block Work Template Deletion with `Cit.Attendance:1007` | [Evidence 57](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_57_worktemplate_delete_lifecycle_and_bypasses.png) |
| [`DEFECT-20261110-18`](#defect-20261110-18) | 🟡 P2 Major | Work Templates (Location Quota) | `POST /api/companies/{companyId}/worktemplates/fixed` | Location Work Template 20-Quota Count Includes Soft-Deleted Templates (`IsDeleted: true`), Permanently Exhausting Location Quota | [Evidence 57](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_57_worktemplate_delete_lifecycle_and_bypasses.png) |


---

## 2. Comprehensive Defect Dossiers


### <a id="defect-20261110-15"></a>🔴 DEFECT-20261110-15: Work Template In-Place PATCH Allows Modifying Soft-Deleted Templates (`IsDeleted: true`) with HTTP 200 OK

| Field | Value |
| :--- | :--- |
| **Defect ID** | `DEFECT-20261110-15` (Internal: `WT-DEL-FIX-001`) |
| **Severity** | **🟠 P1 Critical** |
| **Module / Flow** | Work Template Delete Lifecycle & Mutation Integrity |
| **Endpoint & Method** | `PATCH /api/companies/{companyId}/worktemplates/fixed/{id}?locationId={locationId}` |
| **Target Document ID** | `cf3ef115-b548-436b-afd1-568be4f5ebfa` |
| **Visual Evidence** | [Evidence 57 (Panel 1)](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_57_worktemplate_delete_lifecycle_and_bypasses.png) |

#### 1. Detailed Description & Root Cause Analysis
When a work template is deleted via `PATCH /api/companies/{companyId}/worktemplates/{id}/delete`, the document is marked as `IsDeleted: true` in MongoDB collection `Sahab.ERP.Attendance.WorkTemplates`. However, sending an update request via `PATCH /api/companies/{companyId}/worktemplates/fixed/{id}` (or flexi/split endpoints) against this soft-deleted template ID returns `HTTP 200 OK`, successfully mutating the deleted record's properties (`WorkTemplateName`, durations, slots, etc.) and updating `ModifiedAt` while keeping `IsDeleted: true`. The PATCH handler fails to query with `{ IsDeleted: false }` or check `if (template.IsDeleted) throw new EntityNotFoundException(...)`.

#### 2. Reproduction Steps
1. Create or identify a location custom work template `cf3ef115-b548-436b-afd1-568be4f5ebfa`.
2. Execute deletion: `PATCH /api/companies/3a249871-7a8d-dec5-2d72-47795dd2662d/worktemplates/cf3ef115-b548-436b-afd1-568be4f5ebfa/delete?locationId=3a24d629-0d56-a428-baa1-98493a77e614` -> Returns `HTTP 200 OK` (`IsDeleted: true` in MongoDB).
3. Send a mutation PATCH payload to `/api/companies/3a249871-7a8d-dec5-2d72-47795dd2662d/worktemplates/fixed/cf3ef115-b548-436b-afd1-568be4f5ebfa?locationId=3a24d629-0d56-a428-baa1-98493a77e614` with new name `"Mutated After Soft-Delete"`.
4. **Observed Result:** Returns `HTTP 200 OK`. MongoDB document is modified while `IsDeleted: true`.
5. **Expected Result:** `HTTP 404 Not Found` (`Cit.Attendance:1101 Work template not found.`) or `HTTP 400 Bad Request` (`Cannot modify a deleted work template`).

#### 3. Live API Response & MongoDB Proof
```json
{
  "status": 200,
  "body": {
    "id": "cf3ef115-b548-436b-afd1-568be4f5ebfa",
    "templateName": {"en": "Mutated After Soft-Delete"},
    "isDeleted": true
  }
}
```

#### 4. Recommended Developer Remediation (.NET 9 C#)
```csharp
// In UpdateWorkTemplateCommandHandler.cs (Fixed, Flexi, Split)
var template = await _workTemplateRepository.FindOneAsync(
    t => t.Id == request.Id && t.CompanyId == request.CompanyId && !t.IsDeleted,
    cancellationToken);
if (template == null)
{
    throw new BusinessRuleException("Cit.Attendance:1101", "Work template not found or has been deleted.");
}
```

---

### <a id="defect-20261110-16"></a>🔴 DEFECT-20261110-16: Work Plan Creation Allows Referencing and Embedding Soft-Deleted Work Templates (`IsDeleted: true`) with HTTP 200 OK

| Field | Value |
| :--- | :--- |
| **Defect ID** | `DEFECT-20261110-16` (Internal: `WT-DEL-PLAN-001`) |
| **Severity** | **🟠 P1 Critical** |
| **Module / Flow** | Work Plan Creation & Referential Integrity |
| **Endpoint & Method** | `POST /api/companies/{companyId}/workplans?locationId={locationId}` |
| **Created Work Plan ID** | `0dea229a-ee40-4180-87a7-5ca5a08993f4` |
| **Referenced Deleted Template** | `cf3ef115-b548-436b-afd1-568be4f5ebfa` |
| **Visual Evidence** | [Evidence 57 (Panel 2)](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_57_worktemplate_delete_lifecycle_and_bypasses.png) |

#### 1. Detailed Description & Root Cause Analysis
When creating a Work Plan via `POST /api/companies/{companyId}/workplans`, the caller provides `workTemplateId` in the request body. The Work Plan validator/service queries the Work Template by `_id` without filtering for `IsDeleted == false`. Consequently, a user can successfully construct and activate a new Work Plan that references and embeds an inactive, soft-deleted shift template. Any employee assigned to this work plan inherits schedules from a deleted template.

#### 2. Reproduction Steps
1. Soft-delete work template `cf3ef115-b548-436b-afd1-568be4f5ebfa` (`IsDeleted: true`).
2. Send `POST /api/companies/3a249871-7a8d-dec5-2d72-47795dd2662d/workplans?locationId=3a24d646-b3cf-b1d4-61bb-1adf094b52fc`:
```json
{
  "workPlanName": {"en": "Plan Referencing Soft-Deleted Template"},
  "workTemplateId": "cf3ef115-b548-436b-afd1-568be4f5ebfa",
  "planType": 1,
  "effectiveFrom": "2026-11-10T00:00:00Z",
  "effectiveTo": "2027-11-10T00:00:00Z"
}
```
3. **Observed Result:** Returns `HTTP 200 OK` (or `201 Created`). New Work Plan `0dea229a-ee40-4180-87a7-5ca5a08993f4` is created and embeds the deleted template.
4. **Expected Result:** `HTTP 400 Bad Request` or `HTTP 404 Not Found` (`Cit.Attendance:1101 Cannot create work plan with a deleted work template`).

#### 3. Recommended Developer Remediation (.NET 9 C#)
```csharp
// In CreateWorkPlanCommandHandler.cs
var template = await _workTemplateRepository.FindOneAsync(
    t => t.Id == request.WorkTemplateId && !t.IsDeleted,
    cancellationToken);
if (template == null)
{
    throw new BusinessRuleException("Cit.Attendance:1101", "Referenced work template does not exist or has been deleted.");
}
```

---

### <a id="defect-20261110-17"></a>🔴 DEFECT-20261110-17: Soft-Deleted Work Plans (`IsDeleted: true`) Permanently Block Work Template Deletion with `Cit.Attendance:1007`

| Field | Value |
| :--- | :--- |
| **Defect ID** | `DEFECT-20261110-17` (Internal: `WT-DEL-LOCK-001`) |
| **Severity** | **🟠 P1 Critical** |
| **Module / Flow** | Work Template Deletion Dependency Checking |
| **Endpoint & Method** | `PATCH /api/companies/{companyId}/worktemplates/{id}/delete` |
| **Affected Template ID** | `cf3ef115-b548-436b-afd1-568be4f5ebfa` |
| **Associated Soft-Deleted Plan** | `0dea229a-ee40-4180-87a7-5ca5a08993f4` (`IsDeleted: true`) |
| **Visual Evidence** | [Evidence 57 (Panel 3)](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_57_worktemplate_delete_lifecycle_and_bypasses.png) |

#### 1. Detailed Description & Root Cause Analysis
Before permitting a Work Template to be deleted, the backend checks whether any Work Plan references this template. However, the check executes a query such as `_workPlanRepository.AnyAsync(p => p.WorkTemplateId == templateId)` WITHOUT checking `!p.IsDeleted`. If a Work Plan referencing the template was previously soft-deleted, it still causes this check to return `true`. As a result, the work template is permanently deadlocked from being deleted, throwing `Cit.Attendance:1007 Company default in use cannot be deactivated.` even though no active Work Plan uses it.

#### 2. Reproduction Steps
1. Create Work Template `T1`.
2. Create Work Plan `WP1` referencing `T1`.
3. Soft-delete `WP1` via `PATCH /api/companies/{companyId}/workplans/{id}/delete` -> `WP1.IsDeleted = true`.
4. Attempt to delete `T1` via `PATCH /api/companies/{companyId}/worktemplates/{T1}/delete`.
5. **Observed Result:** Returns `HTTP 400 Bad Request` with `Cit.Attendance:1007 Company default in use cannot be deactivated.`
6. **Expected Result:** `HTTP 200 OK` (Soft-delete should succeed because all referencing work plans are deleted).

#### 3. Recommended Developer Remediation (.NET 9 C#)
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

### <a id="defect-20261110-18"></a>🟡 DEFECT-20261110-18: Location Work Template 20-Quota Count Includes Soft-Deleted Templates (`IsDeleted: true`), Permanently Exhausting Location Quota

| Field | Value |
| :--- | :--- |
| **Defect ID** | `DEFECT-20261110-18` (Internal: `WT-DEL-QUOTA-001`) |
| **Severity** | **🟡 P2 Major** |
| **Module / Flow** | Location Work Template Creation Quota Enforcement |
| **Endpoint & Method** | `POST /api/companies/{companyId}/worktemplates/fixed?locationId={locationId}` |
| **Affected Location ID** | Location 1 (`3a24d629-0d56-a428-baa1-98493a77e614`) |
| **Active Template Count** | `19` |
| **Soft-Deleted Template Count** | `1` (`cf3ef115-b548-436b-afd1-568be4f5ebfa`) |
| **Visual Evidence** | [Evidence 57 (Panel 4)](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_57_worktemplate_delete_lifecycle_and_bypasses.png) |

#### 1. Detailed Description & Root Cause Analysis
The system enforces a maximum limit of 20 work templates per location (`Cit.Attendance:1203 Location maximum limit reached.`). However, the quota counting query counts ALL documents matching `{ LocationId: locationId }` WITHOUT filtering out `{ IsDeleted: false }`. In Location 1, there are 19 active templates and 1 soft-deleted template. When attempting to create a new template, the count returns 20, permanently blocking new template creation even though only 19 active templates exist. Deleting unwanted templates fails to free up quota slots.

#### 2. Reproduction Steps
1. Accumulate 19 active templates in Location 1, plus 1 soft-deleted template.
2. Send `POST /api/companies/3a249871-7a8d-dec5-2d72-47795dd2662d/worktemplates/fixed?locationId=3a24d629-0d56-a428-baa1-98493a77e614` with a valid new template.
3. **Observed Result:** Returns `HTTP 400 Bad Request` with `Cit.Attendance:1203 Location maximum limit reached.`
4. **Expected Result:** `HTTP 200 OK` (Soft-deleted templates should not count toward the 20-template active quota).

#### 3. Recommended Developer Remediation (.NET 9 C#)
```csharp
// In CreateWorkTemplateCommandHandler.cs (Fixed, Flexi, Split)
var currentCount = await _workTemplateRepository.CountAsync(
    t => t.CompanyId == request.CompanyId && t.LocationId == request.LocationId && !t.IsDeleted,
    cancellationToken);
if (currentCount >= 20)
{
    throw new BusinessRuleException("Cit.Attendance:1203", "Location maximum limit reached.");
}
```
