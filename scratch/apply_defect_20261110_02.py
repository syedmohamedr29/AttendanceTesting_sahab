import sys

sys.stdout.reconfigure(encoding='utf-8')

file1 = "Defects/Attendance2_Master_Defect_Log.md"
file2 = "Attendance2_Defects_Gaps_and_Architecture_Inconsistencies_Report.md"

# -------------------------------------------------------------------------
# 1. Update Defects/Attendance2_Master_Defect_Log.md
# -------------------------------------------------------------------------
with open(file1, "r", encoding="utf-8") as f:
    text1 = f.read()

text1 = text1.replace("(All 69 Defects)", "(All 70 Defects)")

# Quick Reference Table: Add DEFECT-20261110-02 above DEFECT-20261110-01
target_tbl = "| [`DEFECT-20261110-01`](#defect-20261110-01) |"
new_tbl_row = """| [`DEFECT-20261110-02`](#defect-20261110-02) | 🟠 P1 | Work Template / Cascade & Lifecycle Sync | Editing Company Default Work Template (CDWT Version 2.0) Fails to Auto-Update Seeded Location Default Templates; `HasPendingLocSync: true` Stalled in MongoDB | ``PATCH /worktemplates/fixed/{id}`` | [Evidence 52](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_52_cdwt_edit_cascade_failure_haspendinglocsync_true_compass.png) |
| [`DEFECT-20261110-01`](#defect-20261110-01) |"""

if target_tbl in text1:
    text1 = text1.replace(target_tbl, new_tbl_row)
    print("Added DEFECT-20261110-02 to Quick Reference Table in Master Defect Log.")
else:
    print("Warning: target_tbl not found in Master Defect Log.")

# Detailed section: Add DEFECT-20261110-02 before DEFECT-20261110-01
target_detail = '### <a id="defect-20261110-01"></a>🔴 DEFECT-20261110-01:'

detail_1002 = """### <a id="defect-20261110-02"></a>🔴 DEFECT-20261110-02: Editing Company Default Work Template (CDWT Version 2.0) Fails to Auto-Update Seeded Location Default Templates; `HasPendingLocSync: true` Stalled in MongoDB

| Field | Detail |
| :--- | :--- |
| **Defect ID** | `DEFECT-20261110-02` |
| **Severity** | 🟠 **P1 Critical** (Work Template Lifecycle Invariant, Location Synchronization Gap & Stale Shift Schedule Cascade) |
| **Module / Sub-Feature** | Module 2: Work Template & Location Cascade / Shift & Rotation Template Lifecycle |
| **API Endpoints** | `PATCH /api/companies/{companyId}/worktemplates/fixed/{id}`<br>`GET /api/companies/{companyId}/worktemplates/company-default/sync-status`<br>`POST /api/companies/{companyId}/worktemplates/apply-sync` |
| **Target Collection** | `Sahab.ERP.Attendance.WorkTemplates` |
| **Target Companies Verified** | Attendance 8 (`3a249871-7a8d-dec5-2d72-47795dd2662d`) |
| **Visual Evidence** | [Evidence 52 (CDWT Edit Fails to Auto-Update Seeded Location Templates; HasPendingLocSync: true)](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_52_cdwt_edit_cascade_failure_haspendinglocsync_true_compass.png)<br>*(User Verification Screenshot: [evidence_52_user_cdwt_edit_haspendinglocsync_true.jpg](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_52_user_cdwt_edit_haspendinglocsync_true.jpg))* |
| **Status** | **OPEN / CONFIRMED ON DEV ENVIRONMENT** |

#### 1. Issue Description & Live Evidence
During live MongoDB Compass testing on Company **Attendance 8** (`3a249871-7a8d-dec5-2d72-47795dd2662d`):
1. **CDWT Edited to Version 2.0:**
   The user edited the Company Default Work Template (CDWT), changing working days from 5 to 4 and total work duration from 2700 to 2160 minutes. This successfully persisted Version 2.0 (`Version: "2.0"`, `IsDefault: true`).
2. **Failure to Cascade to Seeded Location Templates:**
   - On creation, the system automatically seeded the location-level default template for Location 1 (`IsCompanyLinked = true`).
   - However, upon editing CDWT to Version 2.0, the seeded location template at Location 1 was **NOT updated**.
   - Inspection of the CDWT Version 2.0 document shows:
     ```json
     {
       "Version": "2.0",
       "TotalWorkDurationInMinutes": 2160,
       "TotalWorkingDays": 4,
       "TotalDaysOff": 3,
       "IsDefault": true,
       "HasPendingLocSync": true   <--- STUCK AT TRUE!
     }
     ```
   - The seeded location template remains stranded with obsolete Version 1.0 schedule (5 days, 2700 minutes), causing direct schedule divergence between the company default and its linked locations.

#### 2. Root Cause Analysis
- `UpdateFixedWorkTemplateCommandHandler.cs` sets `HasPendingLocSync = true` upon creating the new version, but does **not** trigger an automatic cascade to `IsCompanyLinked = true` location templates.
- Instead, the backend relies on an external/manual call to `POST /api/companies/{companyId}/worktemplates/apply-sync`.
- This creates an asymmetric lifecycle: creation auto-seeds location templates, but editing abandons them in an un-synchronized state unless explicitly triggered.

#### 3. Photographic Proof & Evidence
| Evidence Image Preview | Live Verification Reference |
| :---: | :--- |
| ![DEFECT-20261110-02](../defect_evidence/evidence_52_cdwt_edit_cascade_failure_haspendinglocsync_true_compass.png) | **File:** `evidence_52_cdwt_edit_cascade_failure_haspendinglocsync_true_compass.png`<br><br>[🔍 Click to Open Full-Resolution Image](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_52_cdwt_edit_cascade_failure_haspendinglocsync_true_compass.png)<br><br>*Evidence 52: MongoDB Compass inspection of Sahab.ERP.Attendance.WorkTemplates on Attendance 8 showing CDWT Version 2.0 with HasPendingLocSync: true while seeded location template is left un-updated.* |

#### 4. Developer Remediation (.NET 9 C#)
1. **Auto-Cascade on Edit (Recommended):**
   In `UpdateFixedWorkTemplateCommandHandler.cs`, automatically invoke `ApplySyncToLocationsAsync` for all `IsCompanyLinked == true` location templates upon saving CDWT edits, and reset `HasPendingLocSync = false`.
2. **Immediate Manual Sync for Attendance 8:**
   Execute `POST /api/companies/3a249871-7a8d-dec5-2d72-47795dd2662d/worktemplates/apply-sync` via Swagger to immediately push Version 2.0 down to Location 1 and clear the pending sync flag.

---

"""

if target_detail in text1:
    text1 = text1.replace(target_detail, detail_1002 + target_detail)
    print("Inserted DEFECT-20261110-02 detail into Master Defect Log.")
else:
    print("Warning: target_detail not found in Master Defect Log.")

with open(file1, "w", encoding="utf-8") as f:
    f.write(text1)
print(f"Saved {file1} successfully.")

# -------------------------------------------------------------------------
# 2. Update Attendance2_Defects_Gaps_and_Architecture_Inconsistencies_Report.md
# -------------------------------------------------------------------------
with open(file2, "r", encoding="utf-8") as f:
    text2 = f.read()

# Dashboard table: Add DEFECT-20261110-02 above DEFECT-20261110-01
target_rep_dash = "| **`DEFECT-20261110-01`** |"
new_rep_dash = """| **`DEFECT-20261110-02`** | **🟠 P1 (Lifecycle & Cascade Gap)** | **Work Template Module**<br>(Location Synchronization) | `ERP.Attendance.WorkTemplates`<br>(`PATCH /worktemplates/*`) | **CDWT Edit Fails to Auto-Update Seeded Location Default Templates:** Editing CDWT creates Version 2.0 and sets `HasPendingLocSync = true`, but fails to auto-cascade changes to linked location templates, leaving them on stale Version 1.0 schedule. | ❌ **FAIL ([Evidence 52](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_52_cdwt_edit_cascade_failure_haspendinglocsync_true_compass.png))** |
| **`DEFECT-20261110-01`** |"""

if target_rep_dash in text2:
    text2 = text2.replace(target_rep_dash, new_rep_dash, 1)
    print("Added DEFECT-20261110-02 to Dashboard in Report.")
else:
    print("Warning: target_rep_dash not found in Report.")

# Detailed section in Report: Add DEFECT-20261110-02 before DEFECT-20261110-01
target_rep_detail = "#### Defect `DEFECT-20261110-01`:"
new_rep_detail = """#### Defect `DEFECT-20261110-02`: Editing Company Default Work Template (CDWT Version 2.0) Fails to Auto-Update Seeded Location Default Templates; `HasPendingLocSync: true` Stalled in MongoDB

- **Severity:** 🟠 **P1 Critical** (Work Template Lifecycle Invariant, Location Synchronization Gap & Stale Shift Schedule Cascade)
- **Module / Feature:** Module 2: Work Template & Location Cascade / Shift & Rotation Template Lifecycle
- **Target Collection:** `Sahab.ERP.Attendance.WorkTemplates`
- **Target Company:** Attendance 8 (`3a249871-7a8d-dec5-2d72-47795dd2662d`)
- **Visual Evidence:** [Evidence 52 (CDWT Edit Fails to Auto-Update Seeded Location Templates; HasPendingLocSync: true)](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_52_cdwt_edit_cascade_failure_haspendinglocsync_true_compass.png)<br>*(User Verification Screenshot: [evidence_52_user_cdwt_edit_haspendinglocsync_true.jpg](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_52_user_cdwt_edit_haspendinglocsync_true.jpg))*

##### 1. Problem Description & Direct Evidence Analysis
1. **Version 2.0 Edit:** Editing CDWT updates duration/days (e.g. 4 days / 2160 min) creating Version 2.0.
2. **Missing Auto-Cascade:** Seeded location template at Location 1 is NOT updated and remains on Version 1.0 (5 days / 2700 min).
3. **Pending Sync Flag:** `HasPendingLocSync: true` sits unresolved in MongoDB unless `POST /worktemplates/apply-sync` is manually invoked.

##### 2. Developer Action & Remediation
- Automatically trigger location cascade in `UpdateFixedWorkTemplateCommandHandler.cs` when editing company default templates (`IsDefault == true`).
- Pushes Version 2.0 schedule to all `IsCompanyLinked == true` location templates and resets `HasPendingLocSync = false`.

---

#### Defect `DEFECT-20261110-01`:`"""

if target_rep_detail in text2:
    text2 = text2.replace(target_rep_detail, new_rep_detail)
    print("Added DEFECT-20261110-02 deep-dive to Report.")
else:
    print("Warning: target_rep_detail not found in Report.")

with open(file2, "w", encoding="utf-8") as f:
    f.write(text2)
print("Saved Report successfully.")
