import re, sys, openpyxl

sys.stdout.reconfigure(encoding='utf-8')

report_path = "Attendance2_Defects_Gaps_and_Architecture_Inconsistencies_Report.md"
master_path = "Defects/Attendance2_Master_Defect_Log.md"

# Table rows for Report MD (ordered 18 down to 15 before 14)
table_rows_report = """| **`DEFECT-20261110-18`** | **🟡 P2 (Quota Architecture)** | **Work Template & Quota**<br>(Location Quota Calculation) | `ERP.Attendance.WorkTemplates`<br>(`POST /worktemplates/fixed`) | **Location 20-Quota Calculation Includes Soft-Deleted Templates:** Deleting templates does not release quota slots because `count_documents` omits `{ IsDeleted: false }`, permanently exhausting location capacity once 20 templates have ever been created. | ❌ **FAIL ([Evidence 57](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_57_worktemplate_delete_lifecycle_and_bypasses.png))** |
| **`DEFECT-20261110-17`** | **🟠 P1 (Referential Integrity)** | **Work Template & Work Plan**<br>(Delete Dependency Filter) | `ERP.Attendance.WorkTemplates`<br>(`PATCH /worktemplates/{id}/delete`) | **Soft-Deleted Work Plans Permanently Lock Work Template Deletion:** `DeleteAsync` checks for referencing work plans without filtering `{ IsDeleted: false }`, permanently returning `Cit.Attendance:1007` even after all plans referencing the template are deleted. | ❌ **FAIL ([Evidence 57](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_57_worktemplate_delete_lifecycle_and_bypasses.png))** |
| **`DEFECT-20261110-16`** | **🟠 P1 (Data Integrity)** | **Work Plan Creation**<br>(Work Template Reference Check) | `ERP.Attendance.WorkPlans`<br>(`POST /workplans`) | **Work Plan Creation Allows Referencing Soft-Deleted Templates:** `POST /workplans` does not validate that `workTemplate.IsDeleted == false`, successfully creating active work plans that embed and reference tombstoned templates with HTTP 200 OK. | ❌ **FAIL ([Evidence 57](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_57_worktemplate_delete_lifecycle_and_bypasses.png))** |
| **`DEFECT-20261110-15`** | **🟠 P1 (Data Integrity)** | **Work Template Mutation**<br>(PATCH Deletion State Check) | `ERP.Attendance.WorkTemplates`<br>(`PATCH /worktemplates/{type}/{id}`) | **In-Place PATCH Allows Modifying Soft-Deleted Templates:** Endpoint does not verify `!template.IsDeleted` before applying in-place updates, allowing mutations to tombstoned documents with HTTP 200 OK. | ❌ **FAIL ([Evidence 57](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_57_worktemplate_delete_lifecycle_and_bypasses.png))** |
"""

# Detail entries for Report MD
defect_entries_report = """
#### Defect `DEFECT-20261110-15`: `PATCH /worktemplates/{type}/{id}` Validation Gap — In-Place Update Allows Modifying Soft-Deleted Work Templates (`IsDeleted: true`) with HTTP 200 OK

- **Severity:** 🟠 **P1 Critical** (Data Integrity Violation, Tombstone Mutation & State Machine Bypass)
- **Module / Feature:** Module 2: Work Template In-Place PATCH / Deletion Lifecycle
- **Affected Endpoints:** `PATCH /api/companies/{companyId}/worktemplates/{fixed|flexi|split}/{id}?locationId={locationId}`
- **Target Collection:** `Sahab.ERP.Attendance.WorkTemplates`
- **Target Company:** Attendance 8 (`3a249871-7a8d-dec5-2d72-47795dd2662d`)
- **Target Location:** Location 2 (`3a24d646-b3cf-b1d4-61bb-1adf094b52fc`)
- **Target Document:** `cf3ef115-b548-436b-afd1-568be4f5ebfa` (`DLPOS01`)
- **Visual Evidence:** [Evidence 57 (Work Template Delete Lifecycle & Critical Integrity Gaps)](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_57_worktemplate_delete_lifecycle_and_bypasses.png)

##### 1. Problem Description & Direct Evidence Analysis
- Document `cf3ef115-b548-436b-afd1-568be4f5ebfa` was soft-deleted via `PATCH /worktemplates/cf3ef115.../delete` (`IsDeleted: True` in MongoDB).
- A subsequent `PATCH /worktemplates/fixed/cf3ef115...` was submitted with payload changing template name to `"Revived Shift"`.
- The endpoint returned **HTTP 200 OK** and modified the document in MongoDB while retaining `IsDeleted: True`.
- The in-place PATCH command handler fetches the document by ID but fails to assert `if (template.IsDeleted) throw new DomainException(...)`.

##### 2. Developer Remediation (.NET 9 C#)
- In `UpdateFixedWorkTemplateCommandHandler.cs`, `UpdateFlexiWorkTemplateCommandHandler.cs`, and `UpdateSplitWorkTemplateCommandHandler.cs`:
  `if (template.IsDeleted) throw new BusinessRuleException("Cit.Attendance:1109", "Cannot modify a deleted work template.");`

---

#### Defect `DEFECT-20261110-16`: `POST /workplans` Validation Gap — Work Plan Creation Allows Referencing and Embedding Soft-Deleted Work Templates (`IsDeleted: true`) with HTTP 200 OK

- **Severity:** 🟠 **P1 Critical** (Referential Integrity Violation, Tombstone Resurrection & Schedule Engine Corruption)
- **Module / Feature:** Module 2: Work Plan Creation / Template Association Lifecycle
- **Affected Endpoints:** `POST /api/companies/{companyId}/workplans?locationId={locationId}`
- **Target Collections:** `Sahab.ERP.Attendance.WorkPlans` & `Sahab.ERP.Attendance.WorkTemplates`
- **Target Company:** Attendance 8 (`3a249871-7a8d-dec5-2d72-47795dd2662d`)
- **Target Location:** Location 2 (`3a24d646-b3cf-b1d4-61bb-1adf094b52fc`)
- **Target Document:** Work Plan `0dea229a-7c98-4cf2-a819-06279481efac` referencing deleted template `cf3ef115-b548-436b-afd1-568be4f5ebfa`
- **Visual Evidence:** [Evidence 57 (Work Template Delete Lifecycle & Critical Integrity Gaps)](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_57_worktemplate_delete_lifecycle_and_bypasses.png)

##### 1. Problem Description & Direct Evidence Analysis
- `POST /workplans` was submitted with `"workTemplateId": "cf3ef115-b548-436b-afd1-568be4f5ebfa"`, which was previously soft-deleted (`IsDeleted: True`).
- The API returned **HTTP 200 OK** and created a live, active Work Plan embedding the snapshot of the deleted template.
- Employees assigned to this work plan will be linked to a deleted template, creating inconsistent timesheet reconciliations and preventing proper template management.

##### 2. Developer Remediation (.NET 9 C#)
- In `CreateWorkPlanCommandHandler.cs`:
  `var template = await _templateRepository.GetActiveByIdAsync(request.WorkTemplateId, cancellationToken);`
  `if (template == null || template.IsDeleted) throw new BusinessRuleException("Cit.Attendance:1110", "Referenced work template is deleted or does not exist.");`

---

#### Defect `DEFECT-20261110-17`: `PATCH /worktemplates/{id}/delete` Architecture Invariant Failure — Soft-Deleted Work Plans (`IsDeleted: true`) Permanently Block Work Template Deletion with `Cit.Attendance:1007`

- **Severity:** 🟠 **P1 Critical** (Referential Integrity Bug, Incomplete Dependency Filtering & Permanent Document Lockout)
- **Module / Feature:** Module 2: Work Template Deletion / Dependency Evaluation
- **Affected Endpoints:** `PATCH /api/companies/{companyId}/worktemplates/{id}/delete?locationId={locationId}`
- **Target Collections:** `Sahab.ERP.Attendance.WorkTemplates` & `Sahab.ERP.Attendance.WorkPlans`
- **Target Company:** Attendance 8 (`3a249871-7a8d-dec5-2d72-47795dd2662d`)
- **Target Location:** Location 2 (`3a24d646-b3cf-b1d4-61bb-1adf094b52fc`)
- **Visual Evidence:** [Evidence 57 (Work Template Delete Lifecycle & Critical Integrity Gaps)](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_57_worktemplate_delete_lifecycle_and_bypasses.png)

##### 1. Problem Description & Direct Evidence Analysis
- Work Plan `0dea229a-7c98-4cf2-a819-06279481efac` referencing template `cf3ef115-b548-436b-afd1-568be4f5ebfa` was soft-deleted (`IsDeleted: true`).
- Subsequently attempting to delete template `cf3ef115...` (`DEL-P08`) failed with:
  `HTTP 400 Bad Request` | `{"error": {"code": "Cit.Attendance:1007", "message": "Company default in use cannot be deactivated."}}`
- The dependency check query in `WorkTemplateService.DeleteAsync` checks for any Work Plan with `WorkTemplate._id == templateId` without filtering `{ IsDeleted: false }`.
- Consequently, once a template has been referenced by a work plan, even after that work plan is deleted, the template is permanently undeletable!

##### 2. Developer Remediation (.NET 9 C#)
- In `DeleteWorkTemplateCommandHandler.cs`, filter only active Work Plans:
  `var hasActiveWorkPlans = await _workPlanRepository.AnyAsync(wp => wp.WorkTemplate.Id == templateId && !wp.IsDeleted, cancellationToken);`
  `if (hasActiveWorkPlans) throw new BusinessRuleException("Cit.Attendance:1007", "Cannot delete a template that is in use by an active work plan.");`

---

#### Defect `DEFECT-20261110-18`: Location Work Template Quota Calculation Counts Soft-Deleted Templates (`IsDeleted: true`), Permanently Exhausting Location Capacity

- **Severity:** 🟡 **P2 Major** (Architectural Quota Constraint, Capacity Leakage & Silent Provisioning Failure)
- **Module / Feature:** Module 2: Work Template Creation / Quota Enforcement Lifecycle
- **Affected Endpoints:** `POST /api/companies/{companyId}/worktemplates/{fixed|flexi|split}?locationId={locationId}`
- **Target Collection:** `Sahab.ERP.Attendance.WorkTemplates`
- **Target Company:** Attendance 8 (`3a249871-7a8d-dec5-2d72-47795dd2662d`)
- **Target Location:** Location 1 (`3a24d629-0d56-a428-baa1-98493a77e614`)
- **Visual Evidence:** [Evidence 57 (Work Template Delete Lifecycle & Critical Integrity Gaps)](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_57_worktemplate_delete_lifecycle_and_bypasses.png)

##### 1. Problem Description & Direct Evidence Analysis
- In Location 1, MongoDB holds 20 total documents: 19 active (`IsDeleted: false`) and 1 soft-deleted (`IsDeleted: true`).
- When attempting to create the 20th active template (`POST-P09`), the API blocked creation with:
  `HTTP 400 Bad Request` | `Cit.Attendance:1203 Location maximum limit reached.`
- The quota check counts all documents matching `{ LocationId: locationId }` without filtering `{ IsDeleted: false }`.
- Deleting templates never frees up quota. Once 20 templates have ever been created in a location, no further templates can ever be provisioned.

##### 2. Developer Remediation (.NET 9 C#)
- In `CreateFixedWorkTemplateCommandHandler.cs`, `CreateFlexiWorkTemplateCommandHandler.cs`, and `CreateSplitWorkTemplateCommandHandler.cs`:
  `var count = await _workTemplateRepository.CountAsync(wt => wt.LocationId == locationId && !wt.IsDeleted, cancellationToken);`
  `if (count >= 20) throw new BusinessRuleException("Cit.Attendance:1203", "Location maximum limit of 20 active work templates reached.");`
"""

# Table rows for Master Defect Log MD
table_rows_master = """| [`DEFECT-20261110-18`](#defect-20261110-18) | 🟡 P2 | Work Template / Quota Architecture | Location 20-Quota Calculation Counts Soft-Deleted Templates (`IsDeleted: true`), Permanently Exhausting Location Quota | ``POST /worktemplates/{type}`` | [Evidence 57](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_57_worktemplate_delete_lifecycle_and_bypasses.png) |
| [`DEFECT-20261110-17`](#defect-20261110-17) | 🟠 P1 | Work Template / Referential Integrity | Soft-Deleted Work Plans (`IsDeleted: true`) Permanently Block Work Template Deletion with `Cit.Attendance:1007` | ``PATCH /worktemplates/{id}/delete`` | [Evidence 57](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_57_worktemplate_delete_lifecycle_and_bypasses.png) |
| [`DEFECT-20261110-16`](#defect-20261110-16) | 🟠 P1 | Work Plan / Referential Integrity | Work Plan Creation Allows Referencing and Embedding Soft-Deleted Work Templates (`IsDeleted: true`) with HTTP 200 OK | ``POST /workplans`` | [Evidence 57](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_57_worktemplate_delete_lifecycle_and_bypasses.png) |
| [`DEFECT-20261110-15`](#defect-20261110-15) | 🟠 P1 | Work Template / Data Integrity | In-Place PATCH Allows Modifying Soft-Deleted Work Templates (`IsDeleted: true`) with HTTP 200 OK | ``PATCH /worktemplates/{type}/{id}`` | [Evidence 57](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_57_worktemplate_delete_lifecycle_and_bypasses.png) |
"""

# Detail entries for Master Defect Log MD
defect_entries_master = """
### <a id="defect-20261110-15"></a>🔴 DEFECT-20261110-15: `PATCH /worktemplates/{type}/{id}` Validation Gap — In-Place Update Allows Modifying Soft-Deleted Work Templates (`IsDeleted: true`) with HTTP 200 OK

| Field | Detail |
| :--- | :--- |
| **Defect ID** | `DEFECT-20261110-15` |
| **Severity** | 🟠 **P1 Critical** (Data Integrity Violation, Tombstone Mutation & State Machine Bypass) |
| **Module / Sub-Feature** | Module 2: Work Template In-Place PATCH / Deletion Lifecycle |
| **API Endpoints** | `PATCH /api/companies/{companyId}/worktemplates/{fixed|flexi|split}/{id}?locationId={locationId}` |
| **Target Collection** | `Sahab.ERP.Attendance.WorkTemplates` |
| **Target Companies Verified** | Attendance 8 (`3a249871-7a8d-dec5-2d72-47795dd2662d`) |
| **Target Location Tested** | Location 2 (`3a24d646-b3cf-b1d4-61bb-1adf094b52fc`) |
| **Target Document Verified** | `cf3ef115-b548-436b-afd1-568be4f5ebfa` (`DLPOS01`) |
| **Live Status** | ❌ **FAIL / OPEN (Verified via Automated Live API Execution & MongoDB Evidence 57)** |
| **Visual Evidence** | [Evidence 57 (Work Template Delete Lifecycle & Critical Integrity Gaps)](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_57_worktemplate_delete_lifecycle_and_bypasses.png) |

#### 1. Problem Description & Direct Evidence Analysis
- Submitting in-place update on soft-deleted template `cf3ef115...` returned HTTP 200 OK and modified fields in MongoDB while retaining `IsDeleted: True`.
- Missing validation check `if (template.IsDeleted) throw new BusinessRuleException(...)`.

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
- Location 1 had 19 active templates and 1 soft-deleted template. Attempting to create the 20th active template failed with `Cit.Attendance:1203 Location maximum limit reached.`.
- Soft-deleted templates are not excluded from quota calculation, making quota loss permanent.
"""

# Update Report MD
with open(report_path, "r", encoding="utf-8") as f:
    text_r = f.read()

target_row_r = '| **`DEFECT-20261110-14`** |'
if target_row_r in text_r and 'DEFECT-20261110-18' not in text_r:
    text_r = text_r.replace(target_row_r, table_rows_report + target_row_r)
    print("Report MD: Added table rows 15-18 before DEFECT-20261110-14.")

target_detail_r = '#### Defect `DEFECT-20261110-10`:'
if target_detail_r in text_r and 'DEFECT-20261110-18' not in text_r:
    idx = text_r.find(target_detail_r)
    text_r = text_r[:idx] + defect_entries_report.strip() + "\n\n---\n\n" + text_r[idx:]
    print("Report MD: Added detail sections 15-18.")

with open(report_path, "w", encoding="utf-8") as f:
    f.write(text_r)
print("Saved Report MD.")

# Update Master Defect Log MD
with open(master_path, "r", encoding="utf-8") as f:
    text_m = f.read()

target_row_m = '| [`DEFECT-20261110-14`]'
if target_row_m in text_m and 'DEFECT-20261110-18' not in text_m:
    text_m = text_m.replace(target_row_m, table_rows_master + target_row_m)
    print("Master Log: Added table rows 15-18 before DEFECT-20261110-14.")

target_detail_m = '### <a id="defect-20261110-10"></a>'
if target_detail_m in text_m and 'DEFECT-20261110-18' not in text_m:
    idx_m = text_m.find(target_detail_m)
    text_m = text_m[:idx_m] + defect_entries_master.strip() + "\n\n---\n\n" + text_m[idx_m:]
    print("Master Log: Added detail sections 15-18.")

with open(master_path, "w", encoding="utf-8") as f:
    f.write(text_m)
print("Saved Master Log.")

# Update Excel workbooks
workbooks = [
    "AttendanceTestCases_Master_Consolidated.xlsx",
    "Attendance_Policies_Manual_API_TestCases_MongoDB.xlsx",
    "AttendanceTestCases.xlsx"
]

defect_rows = [
    [
        "DEFECT-20261110-15",
        "P1 Critical",
        "Work Template In-Place PATCH Allows Modifying Soft-Deleted Templates with HTTP 200 OK",
        "PATCH /api/companies/{companyId}/worktemplates/{type}/{id}",
        "Attendance 8 (3a249871-7a8d-dec5-2d72-47795dd2662d)",
        "PATCH /worktemplates/fixed/cf3ef115... on template with IsDeleted=true",
        "HTTP 200 OK | Endpoint mutates fields on soft-deleted document without checking IsDeleted == false",
        "Document cf3ef115... updated to 'Revived Shift' in MongoDB while IsDeleted: true remained",
        "Violates entity state machine invariants and allows unmonitored mutation of tombstoned records.",
        "In UpdateWorkTemplateCommandHandler, check if (template.IsDeleted) throw new BusinessRuleException.",
        "Evidence 57 (file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_57_worktemplate_delete_lifecycle_and_bypasses.png)"
    ],
    [
        "DEFECT-20261110-16",
        "P1 Critical",
        "Work Plan Creation Allows Referencing and Embedding Soft-Deleted Work Templates with HTTP 200 OK",
        "POST /api/companies/{companyId}/workplans?locationId={locationId}",
        "Attendance 8 (3a249871-7a8d-dec5-2d72-47795dd2662d)",
        "POST /workplans with workTemplateId: cf3ef115... (soft-deleted template)",
        "HTTP 200 OK | Work Plan created successfully referencing deleted work template",
        "Document 0dea229a-7c98-4cf2-a819-06279481efac in ERP.Attendance.WorkPlans embeds deleted template snapshot",
        "Resurrects tombstoned templates into active operational employee schedules.",
        "In CreateWorkPlanCommandHandler, validate that referenced template exists and !template.IsDeleted.",
        "Evidence 57 (file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_57_worktemplate_delete_lifecycle_and_bypasses.png)"
    ],
    [
        "DEFECT-20261110-17",
        "P1 Critical",
        "Soft-Deleted Work Plans Permanently Block Work Template Deletion with Cit.Attendance:1007",
        "PATCH /api/companies/{companyId}/worktemplates/{id}/delete?locationId={locationId}",
        "Attendance 8 (3a249871-7a8d-dec5-2d72-47795dd2662d)",
        "PATCH /worktemplates/cf3ef115.../delete after referencing Work Plan 0dea229a... is soft-deleted",
        "HTTP 400 Bad Request | Cit.Attendance:1007 Company default in use cannot be deactivated.",
        "Template permanently locked from deletion even though all referencing work plans are deleted",
        "WorkTemplateService.DeleteAsync checks for any Work Plan reference without filtering { IsDeleted: false }.",
        "In DeleteWorkTemplateCommandHandler, filter only active Work Plans (!wp.IsDeleted).",
        "Evidence 57 (file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_57_worktemplate_delete_lifecycle_and_bypasses.png)"
    ],
    [
        "DEFECT-20261110-18",
        "P2 Major",
        "Location Work Template Quota Calculation Counts Soft-Deleted Templates, Permanently Exhausting Location Capacity",
        "POST /api/companies/{companyId}/worktemplates/{type}?locationId={locationId}",
        "Attendance 8 (3a249871-7a8d-dec5-2d72-47795dd2662d)",
        "POST /worktemplates/fixed in Location 1 with 19 active and 1 deleted template",
        "HTTP 400 Bad Request | Cit.Attendance:1203 Location maximum limit reached.",
        "Location 1 cannot create 20th active template because soft-deleted template consumes quota slot",
        "Deleting templates never frees up quota; location capacity is permanently lost once 20 templates are created.",
        "In quota check, filter count_documents by { LocationId: id, IsDeleted: false }.",
        "Evidence 57 (file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_57_worktemplate_delete_lifecycle_and_bypasses.png)"
    ]
]

for wb_name in workbooks:
    wb = openpyxl.load_workbook(wb_name)
    sheet = wb["Policy Defects Log"]
    for d_row in defect_rows:
        d_id = d_row[0]
        exists = any(r[0] == d_id for r in sheet.iter_rows(values_only=True) if r and r[0])
        if not exists:
            sheet.append(d_row)
            print(f"Appended {d_id} to {wb_name}")
    wb.save(wb_name)
    print(f"Saved {wb_name}")
