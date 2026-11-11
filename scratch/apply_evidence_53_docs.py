import sys

sys.stdout.reconfigure(encoding='utf-8')

report_path = "Attendance2_Defects_Gaps_and_Architecture_Inconsistencies_Report.md"
master_path = "Defects/Attendance2_Master_Defect_Log.md"

evidence_53_section_report = """
##### 3. Live Verification & Architecture Audit: Location Synchronization via API vs MongoDB HasPendingLocSync (Evidence 53)
- **Target Company:** Attendance 8 (`3a249871-7a8d-dec5-2d72-47795dd2662d`)
- **Target Collection:** `Sahab.ERP.Attendance.WorkTemplates`
- **Visual Evidence:** [Evidence 53 (Work Template Location Synchronization & API Status Verification)](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_53_flexi_templates_location_sync_verification_compass.png)<br>*(User Verification Screenshot: [evidence_53_user_flexi_sync_verification.jpg](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_53_user_flexi_sync_verification.jpg))*

###### A. MongoDB Compass Findings vs Creation Default
1. **User Observation:** In company `3a249871-7a8d-dec5-2d72-47795dd2662d`, all three Flexible work templates (`TemplateType: 2`, e.g. `LOC0002` at Location `3a24d646-b3cf-b1d4-61bb-1adf094b52fc`) exhibit `HasPendingLocSync: false` and `IsCompanyLinked: true`.
2. **Invariant Analysis:** In MongoDB, every newly created work template initializes `HasPendingLocSync = false` by default. Having `HasPendingLocSync: false` in the database does NOT indicate that the active Company Default Work Template (CDWT Version 2.0 with 2160 min / 4 days) was synchronized to the location.

###### B. Step-by-Step API Verification Flow
1. **Query Company Default Sync Status:**
   - `GET /api/companies/3a249871-7a8d-dec5-2d72-47795dd2662d/worktemplates/company-default/sync-status`
   - Single source of truth driving the Web UI banner. If CDWT Version 2.0 edits have not cascaded, returns `hasPendingLocSync: true`. If all locations are synced, returns `hasPendingLocSync: false`.
2. **Query Location Work Templates Listing:**
   - `GET /api/companies/3a249871-7a8d-dec5-2d72-47795dd2662d/worktemplates?locationId=3a24d646-b3cf-b1d4-61bb-1adf094b52fc`
   - Inspects `isCompanyLinked` (drives 'Company WT' chip), `hasPendingLocSync`, and template `version` (Version 1.0 vs CDWT Version 2.0).
3. **Execute Manual Cascade Sync (if required):**
   - `POST /api/companies/3a249871-7a8d-dec5-2d72-47795dd2662d/worktemplates/apply-sync`
   - Pushes Version 2.0 down to inheriting locations and resets `hasPendingLocSync = false`.

###### C. Critical Polymorphic Risk: IsCompanyLinked = true on Flexible Templates
- The Company Default Work Template is **Fixed** (`TemplateType: 1`), while `LOC0002` is **Flexible** (`TemplateType: 2`, 1800 min, 5 days).
- Because `LOC0002` is tagged with `IsCompanyLinked: true`, invoking `POST /apply-sync` risks attempting to overwrite the flexible schedule with fixed slots or throwing a polymorphic conversion exception. Location-specific custom templates should have `IsCompanyLinked: false`.
"""

evidence_53_section_master = """
#### 5. Live Verification Audit & Evidence 53: Location Synchronization Verification via API vs MongoDB HasPendingLocSync

| Verification Field | Detail |
| :--- | :--- |
| **Microservice** | `SP.AttendanceSvc` (.NET 9) |
| **Target Company** | Attendance 8 (`3a249871-7a8d-dec5-2d72-47795dd2662d`) |
| **Target Collection** | `Sahab.ERP.Attendance.WorkTemplates` |
| **Visual Evidence** | [Evidence 53 (Work Template Location Synchronization & API Status Verification)](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_53_flexi_templates_location_sync_verification_compass.png)<br>*(User Verification Screenshot: [evidence_53_user_flexi_sync_verification.jpg](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_53_user_flexi_sync_verification.jpg))* |

| Evidence Image Preview | Live Verification Reference |
| :---: | :--- |
| ![Evidence 53](../defect_evidence/evidence_53_flexi_templates_location_sync_verification_compass.png) | **File:** `evidence_53_flexi_templates_location_sync_verification_compass.png`<br><br>[🔍 Click to Open Full-Resolution Image](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_53_flexi_templates_location_sync_verification_compass.png)<br><br>*Evidence 53: MongoDB Compass audit of Sahab.ERP.Attendance.WorkTemplates on Attendance 8 showing Flexible template LOC0002 with HasPendingLocSync: false and IsCompanyLinked: true alongside API sync-status verification protocol.* |

##### Detailed Verification Findings & API Audit Protocol
1. **MongoDB Creation Default vs Sync Status:**
   - In MongoDB, every newly created template document initializes `HasPendingLocSync: false`.
   - In Evidence 52, CDWT was edited to Version 2.0 (4 days / 2160 min) and marked with `HasPendingLocSync: true`.
   - Therefore, `HasPendingLocSync: false` on Flexible location templates is merely an initial document state, not confirmation of synchronization with CDWT Version 2.0.
2. **API Verification Steps:**
   - Step 1: `GET /api/companies/3a249871-7a8d-dec5-2d72-47795dd2662d/worktemplates/company-default/sync-status` -> returns `hasPendingLocSync: true` if CDWT v2.0 is pending application.
   - Step 2: `GET /api/companies/3a249871-7a8d-dec5-2d72-47795dd2662d/worktemplates?locationId=3a24d646-b3cf-b1d4-61bb-1adf094b52fc` -> verifies `isCompanyLinked: true` and current version `1.0`.
   - Step 3: `POST /api/companies/3a249871-7a8d-dec5-2d72-47795dd2662d/worktemplates/apply-sync` -> executes cascade and clears sync flag.
3. **Polymorphic Overwrite Conflict:**
   - CDWT is Fixed (Type 1), while LOC0002 is Flexible (Type 2). Because LOC0002 has `IsCompanyLinked: true`, `POST /apply-sync` risks overwriting flexible schedules with fixed time slots. Custom location templates must maintain `IsCompanyLinked: false`.
"""

# 1. Update Report MD
with open(report_path, "r", encoding="utf-8") as f:
    report_text = f.read()

target_report = "Pushes Version 2.0 schedule to all `IsCompanyLinked == true` location templates and resets `HasPendingLocSync = false`.\n\n---"
replacement_report = f"Pushes Version 2.0 schedule to all `IsCompanyLinked == true` location templates and resets `HasPendingLocSync = false`.\n{evidence_53_section_report}\n---"

if target_report in report_text and "Evidence 53" not in report_text:
    report_text = report_text.replace(target_report, replacement_report)
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(report_text)
    print("Updated Report MD with Evidence 53 verification.")
else:
    print("Report MD already updated or target pattern not found.")

# 2. Update Master Defect Log MD
with open(master_path, "r", encoding="utf-8") as f:
    master_text = f.read()

target_master = "Execute `POST /api/companies/3a249871-7a8d-dec5-2d72-47795dd2662d/worktemplates/apply-sync` via Swagger to immediately push Version 2.0 down to Location 1 and clear the pending sync flag.\n\n---"
replacement_master = f"Execute `POST /api/companies/3a249871-7a8d-dec5-2d72-47795dd2662d/worktemplates/apply-sync` via Swagger to immediately push Version 2.0 down to Location 1 and clear the pending sync flag.\n{evidence_53_section_master}\n---"

if target_master in master_text and "Evidence 53" not in master_text:
    master_text = master_text.replace(target_master, replacement_master)
    with open(master_path, "w", encoding="utf-8") as f:
        f.write(master_text)
    print("Updated Master Defect Log MD with Evidence 53 verification.")
else:
    print("Master Defect Log MD already updated or target pattern not found.")
