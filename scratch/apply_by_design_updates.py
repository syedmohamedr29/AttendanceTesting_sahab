import sys, re

sys.stdout.reconfigure(encoding='utf-8')

report_path = "Attendance2_Defects_Gaps_and_Architecture_Inconsistencies_Report.md"
master_path = "Defects/Attendance2_Master_Defect_Log.md"

# 1. Update Report MD Table row 47
with open(report_path, "r", encoding="utf-8") as f:
    report_text = f.read()

old_row_report = '| **`DEFECT-20261110-02`** | **🟠 P1 (Lifecycle & Cascade Gap)** | **Work Template Module**<br>(Location Synchronization) | `ERP.Attendance.WorkTemplates`<br>(`PATCH /worktemplates/*`) | **CDWT Edit Fails to Auto-Update Seeded Location Default Templates:** Editing CDWT creates Version 2.0 and sets `HasPendingLocSync = true`, but fails to auto-cascade changes to linked location templates, leaving them on stale Version 1.0 schedule. | ❌ **FAIL ([Evidence 52](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_52_cdwt_edit_cascade_failure_haspendinglocsync_true_compass.png))** |'
new_row_report = '| **`DEFECT-20261110-02`** | 🟢 **Closed (By Design)** | **Work Template Module**<br>(Location Immutability & Sync) | `ERP.Attendance.WorkTemplates`<br>(`PATCH /worktemplates/*`) | **Company Default Assigned to Location Immutable at Location Level (Not a Bug):** CDWT assigned to a location cannot be edited directly at location level. Locations needing custom schedules create new location templates (e.g. Flexi). CDWT edit sets `HasPendingLocSync: true` to drive sync banner, not auto-overwrite. | ✅ **CLOSED (NOT A BUG / BY DESIGN)** |'

if old_row_report in report_text:
    report_text = report_text.replace(old_row_report, new_row_report)
    print("Report MD: Replaced defect table row.")
else:
    print("Report MD: Table row pattern not matched!")

# Update Report MD Section 4134
old_sec_report = """#### Defect `DEFECT-20261110-02`: Editing Company Default Work Template (CDWT Version 2.0) Fails to Auto-Update Seeded Location Default Templates; `HasPendingLocSync: true` Stalled in MongoDB

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
- Pushes Version 2.0 schedule to all `IsCompanyLinked == true` location templates and resets `HasPendingLocSync = false`."""

new_sec_report = """#### Defect `DEFECT-20261110-02`: [CLOSED - CONFIRMED BY DESIGN] Company Default Work Template Assigned to Location is Immutable at Location Level; Location Edits Require Creating New Location Template

- **Severity:** 🟢 **Closed — Working as Designed (Not a Bug)** (Work Template Governance & Location Immutability Architecture)
- **Module / Feature:** Module 2: Work Template & Location Cascade / Shift & Rotation Template Lifecycle
- **Target Collection:** `Sahab.ERP.Attendance.WorkTemplates`
- **Target Company:** Attendance 8 (`3a249871-7a8d-dec5-2d72-47795dd2662d`)
- **Visual Evidence:** [Evidence 52 (CDWT Edit Sets HasPendingLocSync: true; Location Immutability)](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_52_cdwt_edit_cascade_failure_haspendinglocsync_true_compass.png)<br>*(User Verification Screenshot: [evidence_52_user_cdwt_edit_haspendinglocsync_true.jpg](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_52_user_cdwt_edit_haspendinglocsync_true.jpg))*

##### 1. Problem Description & User Clarification
1. **Initial Observation:** Editing CDWT creates Version 2.0 (4 days / 2160 min) and sets `HasPendingLocSync: true` on the CDWT document, but the seeded location template at Location 1 was not automatically edited/overwritten.
2. **User Architectural Clarification (10-Nov-2026):**
   > *"Note: does not bug. Company default work template is assigned to the location cannot able to edit particular location. If you want change location edit you create new location and edit (location sync also same concept)."*

##### 2. Business Architecture Invariant Resolution (Working as Designed)
- **Location Immutability:** When CDWT is assigned/seeded to a location, that template is strictly locked to corporate policy and cannot be altered at the location level (`cannot able to edit particular location`).
- **Location Customization Workflow:** If a specific location requires unique shift durations, flexible timings, or custom working days, the user/administrator **creates a new work template for that location** (`you want change location edit you create new location and edit`), exactly as demonstrated with the 3 Flexible templates (`LOC0002` etc.) created on Attendance 8.
- **Sync Model:** Editing CDWT sets `HasPendingLocSync: true` on the company default to alert administrators via the sync banner, but does NOT forcibly overwrite independent location templates."""

if old_sec_report in report_text:
    report_text = report_text.replace(old_sec_report, new_sec_report)
    print("Report MD: Replaced defect section.")
else:
    print("Report MD: Defect section pattern not matched!")

# Add Scenario 4 to Report MD
scenario_4_report = """### 4. Scenario: Company Default Work Template Location Immutability & Independent Location Template Creation
* **Status:** **NOT A BUG / EXPECTED DOMAIN BEHAVIOR (Working as Designed)**
* **Observed System Behavior:**
  When a Company Default Work Template (CDWT) is assigned/seeded to a company location, that template cannot be edited directly at the individual location level. Furthermore, when CDWT is edited at the company level (creating Version 2.0 with 2160 min / 4 days), the system sets `HasPendingLocSync: true` on the CDWT document but does not auto-mutate or overwrite location templates.
* **Business Justification & Domain Architecture:**
  - **Corporate Governance & Location Immutability:** The Company Default Work Template represents centralized organization policy. It is intentionally immutable at the individual location level (`cannot able to edit particular location`) to prevent unauthorized local branch modifications and maintain enterprise-wide compliance.
  - **Location Customization Protocol:** If a specific location requires a unique duration, flexible timings, or different working days, the intended workflow is to **create a new work template specifically for that location** (`you want change location edit you create new location and edit`). The new location template operates autonomously without tampering with the company baseline.
  - **Location Synchronization Concept (`location sync also same concept`):** The location sync banner and `HasPendingLocSync` flag exist to notify administrators that a new company baseline exists. Independent location templates operate on their own lifecycle with `HasPendingLocSync: false` by default (as verified on the 3 Flexible templates `LOC0002` on Attendance 8 in [Evidence 53](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_53_flexi_templates_location_sync_verification_compass.png)), rather than having background jobs overwrite custom location schedules.
* **Defect Resolution:** `DEFECT-20261110-02` is officially **CLOSED - CONFIRMED BY DESIGN (NOT A BUG)**.

---
"""

if "### 3. Scenario: Past Year Holiday Calendar Creation Blocked" in report_text and "### 4. Scenario: Company Default Work Template Location Immutability" not in report_text:
    target_p = "# 🏢 Part 3G: Defects Identified on 05 November 2026"
    report_text = report_text.replace(target_p, scenario_4_report + "\n" + target_p)
    print("Report MD: Added Scenario 4.")

with open(report_path, "w", encoding="utf-8") as f:
    f.write(report_text)
print("Saved Report MD successfully.")

# 2. Update Master Defect Log MD
with open(master_path, "r", encoding="utf-8") as f:
    master_text = f.read()

old_row_master = '| [`DEFECT-20261110-02`](#defect-20261110-02) | 🟠 P1 | Work Template / Cascade & Lifecycle Sync | Editing Company Default Work Template (CDWT Version 2.0) Fails to Auto-Update Seeded Location Default Templates; `HasPendingLocSync: true` Stalled in MongoDB | ``PATCH /worktemplates/fixed/{id}`` | [Evidence 52](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_52_cdwt_edit_cascade_failure_haspendinglocsync_true_compass.png) |'
new_row_master = '| [`DEFECT-20261110-02`](#defect-20261110-02) | 🟢 Closed | Work Template / Location Immutability & Sync | **[CLOSED - BY DESIGN]** Company Default Work Template Assigned to Location is Immutable at Location Level; Editing Requires Creating New Location Template (Not a Bug) | ``PATCH /worktemplates/*`` | 🟢 Closed (By Design) |'

if old_row_master in master_text:
    master_text = master_text.replace(old_row_master, new_row_master)
    print("Master Defect Log: Replaced defect table row.")
else:
    print("Master Defect Log: Table row pattern not matched!")

old_sec_master_pattern = r'### <a id="defect-20261110-02"></a>🔴 DEFECT-20261110-02: Editing Company Default Work Template[\s\S]*?#### 4\. Developer Remediation \(\.NET 9 C#\)[\s\S]*?clear the pending sync flag\.'

new_sec_master = """### <a id="defect-20261110-02"></a>🟢 DEFECT-20261110-02: [CLOSED - CONFIRMED BY DESIGN] Company Default Work Template Assigned to Location is Immutable at Location Level; Location Edits Require Creating New Location Template

| Field | Detail |
| :--- | :--- |
| **Defect ID** | `DEFECT-20261110-02` |
| **Severity** | 🟢 **Closed — Working as Designed (Not a Bug)** (Work Template Governance & Location Immutability Architecture) |
| **Module / Sub-Feature** | Module 2: Work Template & Location Cascade / Shift & Rotation Template Lifecycle |
| **API Endpoints** | `PATCH /api/companies/{companyId}/worktemplates/fixed/{id}`<br>`GET /api/companies/{companyId}/worktemplates/company-default/sync-status` |
| **Target Collection** | `Sahab.ERP.Attendance.WorkTemplates` |
| **Target Companies Verified** | Attendance 8 (`3a249871-7a8d-dec5-2d72-47795dd2662d`) |
| **Live Status** | 🟢 **CLOSED (WORKING AS DESIGNED / NOT A BUG per User Architecture Note 10-Nov-2026)** |

#### 1. Problem Description & Direct Evidence Analysis
1. **Initial Observation:** Editing CDWT creates Version 2.0 (4 days / 2160 min) and sets `HasPendingLocSync: true` on the CDWT document, but the seeded location template at Location 1 was not automatically edited/overwritten.
2. **User Architectural Clarification (10-Nov-2026):**
   > *"Note: does not bug. Company default work template is assigned to the location cannot able to edit particular location. If you want change location edit you create new location and edit (location sync also same concept)."*

#### 2. Business Architecture Invariant Resolution (Working as Designed)
- **Location Immutability:** When CDWT is assigned/seeded to a location, that template is strictly locked to corporate policy and cannot be altered at the location level (`cannot able to edit particular location`).
- **Location Customization Workflow:** If a specific location requires unique shift durations, flexible timings, or custom working days, the user/administrator **creates a new work template for that location** (`you want change location edit you create new location and edit`), exactly as demonstrated with the 3 Flexible templates (`LOC0002` etc.) created on Attendance 8.
- **Sync Model:** Editing CDWT sets `HasPendingLocSync: true` on the company default to alert administrators via the sync banner, but does NOT forcibly overwrite independent location templates."""

if re.search(old_sec_master_pattern, master_text):
    master_text = re.sub(old_sec_master_pattern, new_sec_master, master_text)
    print("Master Defect Log: Replaced defect section via regex.")
else:
    print("Master Defect Log: Defect section pattern not matched!")

scenario_4_master = """### Scenario 4: Company Default Work Template Location Immutability & Independent Location Template Creation
- **Status:** ✅ **WORKING AS DESIGNED (NOT A BUG)**
- **Observed Behavior:**
  When a Company Default Work Template (CDWT) is assigned / auto-seeded to a company location, that template cannot be edited directly at the individual location level. Editing the Company Default Work Template at the company level (e.g. creating Version 2.0 with 2160 min / 4 days) sets `HasPendingLocSync: true` on the CDWT document, but does not auto-mutate or overwrite location templates.
- **Domain Justification & Business Architecture:**
  1. **Location Immutability of Company Default:** The Company Default Work Template is a centralized corporate policy. It is intentionally immutable at the individual location level (`cannot able to edit particular location`) to prevent unauthorized local branch modifications and preserve organizational policy integrity.
  2. **Location Customization Workflow:** If a specific location requires a unique duration, flexible timings, or different working days, the user/administrator **creates a new work template specifically for that location** (`you want change location edit you create new location and edit`). The new location template operates autonomously.
  3. **Location Synchronization Model (`location sync also same concept`):** The location sync banner and `HasPendingLocSync` flag exist to notify administrators that a new company baseline exists. Independent location templates operate on their own lifecycle with `HasPendingLocSync: false` by default (as verified on the 3 Flexible templates `LOC0002` on Attendance 8 in Evidence 53), rather than having background jobs overwrite custom location schedules.
- **Defect Resolution:** `DEFECT-20261110-02` is officially **CLOSED - CONFIRMED BY DESIGN (NOT A BUG)**.
"""

if "### Scenario 3: Past Year Holiday Calendar Creation Blocked" in master_text and "### Scenario 4: Company Default Work Template Location Immutability" not in master_text:
    target_m = "## 8. Master Visual Evidence Index"
    if target_m not in master_text:
        target_m = "# 8. Master Visual Evidence Index"
    if target_m in master_text:
        master_text = master_text.replace(target_m, scenario_4_master + "\n---\n\n" + target_m)
        print("Master Defect Log: Added Scenario 4 before Master Visual Evidence Index.")
    else:
        # Append before EOF or at end of Section 7
        master_text += "\n\n" + scenario_4_master
        print("Master Defect Log: Appended Scenario 4.")

with open(master_path, "w", encoding="utf-8") as f:
    f.write(master_text)
print("Saved Master Defect Log MD successfully.")
