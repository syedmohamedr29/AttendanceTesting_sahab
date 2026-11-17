# -*- coding: utf-8 -*-

with open('Attendance2_Defects_Gaps_and_Architecture_Inconsistencies_Report.md', 'r', encoding='utf-8') as f:
    text = f.read()

target = "#### 1. Executive Summary of Location Shifts Test Results:"
replacement = """📸 **Visual Photographic Evidence Gallery (Module 2: Location Shifts — 16 November 2026):**

| `evidence_54`: UI Regular Shift Locations | `evidence_54`: Post-PATCH Audit Wipeout in Compass | `evidence_55`: Quota Ceiling & Validation Bypasses |
| :---: | :---: | :---: |
| [![Evidence 54 UI](defect_evidence/evidence_54_user_ui_regular_shift_locations.png)](defect_evidence/evidence_54_user_ui_regular_shift_locations.png) | [![Evidence 54 Compass](defect_evidence/evidence_54_regular_shift_location_post_patch_audit_wipeout_compass.png)](defect_evidence/evidence_54_regular_shift_location_post_patch_audit_wipeout_compass.png) | [![Evidence 55 DB](defect_evidence/evidence_55_fixed_wt_location_patch_validation_bypasses_and_db_results.png)](defect_evidence/evidence_55_fixed_wt_location_patch_validation_bypasses_and_db_results.png) |

| `evidence_56`: Flexi/Split Schema Desync | `evidence_57`: Soft-Delete & Tombstone Mutation | `evidence_58`: Rotation Lifecycle & Defects |
| :---: | :---: | :---: |
| [![Evidence 56 DB](defect_evidence/evidence_56_flexi_split_location_validation_bypasses_and_db_results.png)](defect_evidence/evidence_56_flexi_split_location_validation_bypasses_and_db_results.png) | [![Evidence 57 Lifecycle](defect_evidence/evidence_57_worktemplate_delete_lifecycle_and_bypasses.png)](defect_evidence/evidence_57_worktemplate_delete_lifecycle_and_bypasses.png) | [![Evidence 58 Rotation](defect_evidence/evidence_58_rotation_worktemplate_lifecycle_and_defects.png)](defect_evidence/evidence_58_rotation_worktemplate_lifecycle_and_defects.png) |

---

#### 1. Executive Summary of Location Shifts Test Results:"""

assert target in text, "target not found in report"
text = text.replace(target, replacement, 1)

with open('Attendance2_Defects_Gaps_and_Architecture_Inconsistencies_Report.md', 'w', encoding='utf-8') as f:
    f.write(text)

print("Successfully added visual gallery to Module 2 Deep Dive in Report!")
