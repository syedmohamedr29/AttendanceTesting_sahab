import os

evidence_files = [
    "evidence_51_location_default_worktemplate_ar_name_empty_compass.png",
    "evidence_52_cdwt_edit_cascade_failure_haspendinglocsync_true_compass.png",
    "evidence_53_cdwt_patch_sets_haspendinglocsync_true_not_auto_overwrite_compass.png",
    "evidence_54_regular_shift_location_post_patch_audit_wipeout_compass.png",
    "evidence_55_fixed_wt_location_patch_validation_bypasses_and_db_results.png",
    "evidence_56_flexi_split_location_validation_bypasses_and_db_results.png",
    "evidence_57_worktemplate_delete_lifecycle_and_bypasses.png",
    "evidence_58_rotation_worktemplate_lifecycle_and_defects.png"
]

for ef in evidence_files:
    path = os.path.join("defect_evidence", ef)
    exists = os.path.exists(path)
    size = os.path.getsize(path) if exists else 0
    print(f"{ef}: exists={exists}, size={size}")
