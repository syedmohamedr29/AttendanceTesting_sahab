# -*- coding: utf-8 -*-

with open('Defects/Attendance2_Master_Defect_Log.md', 'r', encoding='utf-8') as f:
    master_content = f.read()

with open('Attendance2_Defects_Gaps_and_Architecture_Inconsistencies_Report.md', 'r', encoding='utf-8') as f:
    report_content = f.read()

# Extract Part 3N from report
part3n_header = "### 🏢 Part 3N: Defects Identified on 16 November 2026 — Work Template Module: Location Shifts Live API & MongoDB Audit (`DEFECT-20261116-01` to `DEFECT-20261116-06`)"
part3n_idx = report_content.rfind(part3n_header)
assert part3n_idx != -1, "Part 3N not found in report"
part3n_rich = report_content[part3n_idx:]

# Replace in Master Defect Log
master_part3n_idx = master_content.rfind(part3n_header)
if master_part3n_idx != -1:
    master_content = master_content[:master_part3n_idx] + part3n_rich
    print("Part 3N replaced in Master Defect Log!")

# Also enrich Module 2 Deep Dive in Master Defect Log
target = "#### 1. Executive Summary of Location Shifts Test Results:"
gallery = """📸 **Visual Photographic Evidence Gallery (Module 2: Location Shifts — 16 November 2026):**

| `evidence_54`: UI Regular Shift Locations | `evidence_54`: Post-PATCH Audit Wipeout in Compass | `evidence_55`: Quota Ceiling & Validation Bypasses |
| :---: | :---: | :---: |
| [![Evidence 54 UI](defect_evidence/evidence_54_user_ui_regular_shift_locations.png)](defect_evidence/evidence_54_user_ui_regular_shift_locations.png) | [![Evidence 54 Compass](defect_evidence/evidence_54_regular_shift_location_post_patch_audit_wipeout_compass.png)](defect_evidence/evidence_54_regular_shift_location_post_patch_audit_wipeout_compass.png) | [![Evidence 55 DB](defect_evidence/evidence_55_fixed_wt_location_patch_validation_bypasses_and_db_results.png)](defect_evidence/evidence_55_fixed_wt_location_patch_validation_bypasses_and_db_results.png) |

| `evidence_56`: Flexi/Split Schema Desync | `evidence_57`: Soft-Delete & Tombstone Mutation | `evidence_58`: Rotation Lifecycle & Defects |
| :---: | :---: | :---: |
| [![Evidence 56 DB](defect_evidence/evidence_56_flexi_split_location_validation_bypasses_and_db_results.png)](defect_evidence/evidence_56_flexi_split_location_validation_bypasses_and_db_results.png) | [![Evidence 57 Lifecycle](defect_evidence/evidence_57_worktemplate_delete_lifecycle_and_bypasses.png)](defect_evidence/evidence_57_worktemplate_delete_lifecycle_and_bypasses.png) | [![Evidence 58 Rotation](defect_evidence/evidence_58_rotation_worktemplate_lifecycle_and_defects.png)](defect_evidence/evidence_58_rotation_worktemplate_lifecycle_and_defects.png) |

---

#### 1. Executive Summary of Location Shifts Test Results:"""

if target in master_content and "Visual Photographic Evidence Gallery (Module 2: Location Shifts" not in master_content:
    master_content = master_content.replace(target, gallery, 1)
    print("Added gallery to Module 2 Deep Dive in Master Defect Log!")

with open('Defects/Attendance2_Master_Defect_Log.md', 'w', encoding='utf-8') as f:
    f.write(master_content)

print("Saved enriched Master Defect Log!")
