import sys

sys.stdout.reconfigure(encoding='utf-8')

report_path = "Attendance2_Defects_Gaps_and_Architecture_Inconsistencies_Report.md"
master_path = "Defects/Attendance2_Master_Defect_Log.md"

# 1. Detail section for Report MD
defect_1003_report_details = """
#### Defect `DEFECT-20261110-03`: In-Place Location Work Template PATCH Wipes Out Creation Audit Metadata — `CreatedAt` Overwritten with `0001-01-01T00:00:00.000Z` (DateTime.MinValue) and `CreatedBy` Reset to `null` in MongoDB

- **Severity:** 🟠 **P1 Critical** (Audit Trail Corruption, Temporal Invariant Breach & Historical Creation Wipeout)
- **Module / Feature:** Module 2: Work Template & Location Cascade / Regular Shift In-Place PATCH Lifecycle
- **Affected Endpoints:** `PATCH /api/companies/{companyId}/worktemplates/fixed/{id}?locationId={locationId}`, `PATCH .../flexi/{id}`, `PATCH .../split/{id}`
- **Target Collection:** `Sahab.ERP.Attendance.WorkTemplates`
- **Target Company:** Attendance 8 (`3a249871-7a8d-dec5-2d72-47795dd2662d`)
- **Target Location:** Location 1 (`3a24d629-0d56-a428-baa1-98493a77e614`)
- **Target Document:** `0ba519c8-c2e2-4bce-8a70-23b1616ed5f7`
- **Visual Evidence:** [Evidence 54 (Regular Shift Location-Assigned In-Place PATCH Wipes Out CreatedAt/CreatedBy)](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_54_regular_shift_location_post_patch_audit_wipeout_compass.png)<br>*(User Verification Screenshots: [evidence_54_user_post_fixed_location_swagger.png](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_54_user_post_fixed_location_swagger.png), [evidence_54_user_patch_fixed_location_swagger.png](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_54_user_patch_fixed_location_swagger.png), [evidence_54_user_ui_regular_shift_locations.png](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_54_user_ui_regular_shift_locations.png), [evidence_54_user_mongodb_patch_location_wiped_createdat.jpg](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_54_user_mongodb_patch_location_wiped_createdat.jpg))*

##### 1. Problem Description & Direct Evidence Analysis
1. **In-Place Location Update:** When a location-assigned regular work template (`IsDefault == false`, `LocationId == 3a24d629-0d56-a428-baa1-98493a77e614`) is edited via `PATCH /worktemplates/fixed/{id}?locationId={locationId}`, the microservice performs an in-place edit (retaining document `_id: 0ba519c8-c2e2-4bce-8a70-23b1616ed5f7` and Version `1.0`).
2. **Creation Metadata Destruction in MongoDB:**
   - While `ModifiedAt` (`2026-11-10T06:55:26.818Z`) and `ModifiedBy` (`syed.mohamed@comm-it.in`) are stamped correctly, the handler **completely destroys the creation audit trail**:
     * `CreatedAt: ISODate('0001-01-01T00:00:00.000+00:00')` (January 1, 1 at 12:00:00 AM UTC - .NET `DateTime.MinValue`)
     * `CreatedBy: null`
3. **Cross-Type Subtype Mutation Gap:**
   - In MongoDB, document `0ba519c8-c2e2-4bce-8a70-23b1616ed5f7` exhibits `TemplateType: 3` (Split Shift). Yet calling `PATCH /api/companies/{companyId}/worktemplates/fixed/{id}` accepted and updated the entity with HTTP 200 OK without validating that the template matches the `/fixed` subtype (Test Case `PN31`).
4. **URL Query Param Discrepancy:**
   - The route requires `locationId` as a query parameter (`?locationId=...`). Passing `/locationId/{id}/` as a URL path segment triggers HTTP 404 Not Found.

##### 2. Business Impact & Regulatory Risk
- **Statutory Audit Invalidation:** Erasing `CreatedAt` and `CreatedBy` renders the shift schedule legally unverifiable under GCC labour audit regulations and ISO/IEC 27001 data integrity standards.
- **Forensic Non-Repudiation Failure:** HR cannot determine when the shift was originally created or who authorized it.

##### 3. Developer Action & Remediation (.NET 9 C#)
- In `UpdateFixedWorkTemplateCommandHandler.cs`, use atomic MongoDB `$set` updates for mutable fields only:
  ```csharp
  var update = Builders<WorkTemplate>.Update
      .Set(x => x.WorkTemplateName, request.TemplateName)
      .Set(x => x.FixedTimeSlots, request.FixedTimeSlots)
      .Set(x => x.TotalWorkDurationInMinutes, request.TotalWorkDurationInMinutes)
      .Set(x => x.ModifiedAt, DateTime.UtcNow)
      .Set(x => x.ModifiedBy, currentUser.Email);
  ```
- Explicitly enforce that `CreatedAt` and `CreatedBy` are NEVER modified or defaulted during in-place PATCH operations.
- Add subtype validation: `if (entity.TemplateType != WorkTemplateType.Fixed) throw new BusinessException("Cit.Attendance:TemplateTypeMismatch", "Cannot update a non-Fixed template via Fixed endpoint.");`
"""

# 2. Table row for Report MD
table_row_report = '| **`DEFECT-20261110-03`** | **🟠 P1 (Audit Trail Corruption)** | **Work Template Module**<br>(Regular Shift In-Place PATCH) | `ERP.Attendance.WorkTemplates`<br>(`PATCH /worktemplates/fixed/{id}`) | **In-Place Location Work Template PATCH Wipes Out Creation Metadata:** In-place edit sets `CreatedAt` to `0001-01-01T00:00:00.000Z` (`DateTime.MinValue`) and `CreatedBy` to `null` in MongoDB, destroying compliance audit trails. | ❌ **FAIL ([Evidence 54](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_54_regular_shift_location_post_patch_audit_wipeout_compass.png))** |\n'

with open(report_path, "r", encoding="utf-8") as f:
    report_text = f.read()

# Insert table row before DEFECT-20261110-02
target_row_marker = '| **`DEFECT-20261110-02`**'
if target_row_marker in report_text and "DEFECT-20261110-03" not in report_text:
    report_text = report_text.replace(target_row_marker, table_row_report + target_row_marker)
    print("Report MD: Added table row for DEFECT-20261110-03.")

# Insert detail section before DEFECT-20261110-02 details
target_detail_marker = '#### Defect `DEFECT-20261110-02`:'
if target_detail_marker in report_text and "#### Defect `DEFECT-20261110-03`:" not in report_text:
    report_text = report_text.replace(target_detail_marker, defect_1003_report_details + "\n---\n\n" + target_detail_marker)
    print("Report MD: Added details for DEFECT-20261110-03.")

with open(report_path, "w", encoding="utf-8") as f:
    f.write(report_text)
print("Saved Report MD successfully.")

# 3. Master Defect Log MD updates
table_row_master = '| [`DEFECT-20261110-03`](#defect-20261110-03) | 🟠 P1 | Work Template / Audit Trail Integrity | In-Place Location Work Template PATCH Wipes Out Creation Metadata: `CreatedAt` Overwritten with `0001-01-01T00:00:00.000Z` and `CreatedBy` Reset to `null` in MongoDB | ``PATCH /worktemplates/fixed/{id}`` | [Evidence 54](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_54_regular_shift_location_post_patch_audit_wipeout_compass.png) |\n'

defect_1003_master_details = """
### <a id="defect-20261110-03"></a>🔴 DEFECT-20261110-03: In-Place Location Work Template PATCH Wipes Out Creation Audit Metadata — `CreatedAt` Overwritten with `0001-01-01T00:00:00.000Z` (DateTime.MinValue) and `CreatedBy` Reset to `null` in MongoDB

| Field | Detail |
| :--- | :--- |
| **Defect ID** | `DEFECT-20261110-03` |
| **Severity** | 🟠 **P1 Critical** (Audit Trail Corruption, Temporal Invariant Breach & Historical Creation Wipeout) |
| **Module / Sub-Feature** | Module 2: Work Template & Location Cascade / Regular Shift In-Place PATCH Lifecycle |
| **API Endpoints** | `PATCH /api/companies/{companyId}/worktemplates/fixed/{id}?locationId={locationId}`, `PATCH .../flexi/{id}`, `PATCH .../split/{id}` |
| **Target Collection** | `Sahab.ERP.Attendance.WorkTemplates` |
| **Target Companies Verified** | Attendance 8 (`3a249871-7a8d-dec5-2d72-47795dd2662d`) |
| **Target Location Tested** | Location 1 (`3a24d629-0d56-a428-baa1-98493a77e614`) |
| **Target Document Verified** | `0ba519c8-c2e2-4bce-8a70-23b1616ed5f7` |
| **Live Status** | ❌ **FAIL / OPEN (Verified via MongoDB Compass Evidence 54)** |
| **Visual Evidence** | [Evidence 54 (Regular Shift In-Place PATCH Wipes Out CreatedAt/CreatedBy)](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_54_regular_shift_location_post_patch_audit_wipeout_compass.png)<br>*(User Verification Screenshots: [evidence_54_user_post_fixed_location_swagger.png](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_54_user_post_fixed_location_swagger.png), [evidence_54_user_patch_fixed_location_swagger.png](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_54_user_patch_fixed_location_swagger.png), [evidence_54_user_ui_regular_shift_locations.png](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_54_user_ui_regular_shift_locations.png), [evidence_54_user_mongodb_patch_location_wiped_createdat.jpg](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_54_user_mongodb_patch_location_wiped_createdat.jpg))* |

#### 1. Problem Description & Direct Evidence Analysis
1. **In-Place Location Update:** When a location-assigned regular work template (`IsDefault == false`, `LocationId == 3a24d629-0d56-a428-baa1-98493a77e614`) is edited via `PATCH /worktemplates/fixed/{id}?locationId={locationId}`, the microservice performs an in-place edit (retaining document `_id: 0ba519c8-c2e2-4bce-8a70-23b1616ed5f7` and Version `1.0`).
2. **Creation Metadata Destruction in MongoDB:**
   - While `ModifiedAt` (`2026-11-10T06:55:26.818Z`) and `ModifiedBy` (`syed.mohamed@comm-it.in`) are stamped correctly, the handler **completely destroys the creation audit trail**:
     * `CreatedAt: ISODate('0001-01-01T00:00:00.000+00:00')` (January 1, 1 at 12:00:00 AM UTC - .NET `DateTime.MinValue`)
     * `CreatedBy: null`
3. **Cross-Type Subtype Mutation Gap:**
   - In MongoDB, document `0ba519c8-c2e2-4bce-8a70-23b1616ed5f7` exhibits `TemplateType: 3` (Split Shift). Yet calling `PATCH /api/companies/{companyId}/worktemplates/fixed/{id}` accepted and updated the entity with HTTP 200 OK without validating that the template matches the `/fixed` subtype.

| Evidence Image Preview | Live Verification Reference |
| :---: | :--- |
| ![Evidence 54](../defect_evidence/evidence_54_regular_shift_location_post_patch_audit_wipeout_compass.png) | **File:** `evidence_54_regular_shift_location_post_patch_audit_wipeout_compass.png`<br><br>[🔍 Click to Open Full-Resolution Image](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_54_regular_shift_location_post_patch_audit_wipeout_compass.png)<br><br>*Evidence 54: MongoDB Compass audit of Sahab.ERP.Attendance.WorkTemplates on Attendance 8 showing Document 0ba519c8... with CreatedAt wiped out to 0001-01-01T00:00:00.000Z and CreatedBy reset to null after in-place PATCH execution.* |

#### 2. Developer Remediation (.NET 9 C#)
1. Use atomic MongoDB `$set` updates for mutable fields only:
   ```csharp
   var update = Builders<WorkTemplate>.Update
       .Set(x => x.WorkTemplateName, request.TemplateName)
       .Set(x => x.FixedTimeSlots, request.FixedTimeSlots)
       .Set(x => x.TotalWorkDurationInMinutes, request.TotalWorkDurationInMinutes)
       .Set(x => x.ModifiedAt, DateTime.UtcNow)
       .Set(x => x.ModifiedBy, currentUser.Email);
   ```
2. Never overwrite or default `CreatedAt` or `CreatedBy` during in-place PATCH operations.
3. Enforce subtype integrity: reject PATCH operations where the URL endpoint type does not match `entity.TemplateType`.
"""

with open(master_path, "r", encoding="utf-8") as f:
    master_text = f.read()

# Insert table row before DEFECT-20261110-02
target_master_row_marker = '| [`DEFECT-20261110-02`]'
if target_master_row_marker in master_text and "DEFECT-20261110-03" not in master_text:
    master_text = master_text.replace(target_master_row_marker, table_row_master + target_master_row_marker)
    print("Master Defect Log: Added table row for DEFECT-20261110-03.")

# Insert details before DEFECT-20261110-02
target_master_detail_marker = '### <a id="defect-20261110-02"></a>'
if target_master_detail_marker in master_text and "DEFECT-20261110-03" not in master_text:
    master_text = master_text.replace(target_master_detail_marker, defect_1003_master_details + "\n---\n\n" + target_master_detail_marker)
    print("Master Defect Log: Added details for DEFECT-20261110-03.")

with open(master_path, "w", encoding="utf-8") as f:
    f.write(master_text)
print("Saved Master Defect Log MD successfully.")
