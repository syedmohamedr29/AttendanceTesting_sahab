import os

evidence_files = [
    "evidence_59_workplan_post_swagger_tenantname_circled.png",
    "evidence_60_workplan_swagger_isdeleted_and_id_circled.png",
    "evidence_61_workplan_post_swagger_200_full_context.jpg",
    "evidence_62_workplan_get_state_filter_inverted.png",
    "evidence_63_workplan_default_invariants_and_delete_defects.png",
    "evidence_64_workplan_patch_stale_policies_desync.png",
    "evidence_65_workplan_policy_validation_bypasses_post_patch.png",
    "evidence_66_workplan_patch_soft_delete_and_inuse_bypass.png",
    "evidence_67_workplan_wa_propagation_broken_name_policies.png",
    "evidence_68_workplan_name_wt_validation_and_patch_quirks.png",
    "evidence_69_workplan_500_http_and_deleted_quota_exhaustion.png",
    "evidence_70_workplan_retest_policy_with_without_and_rtm.png",
    "evidence_71_workplan_get_employees_and_edge_defects.png",
    "evidence_72_workplan_overtime_disabled_with_overtime_policy_embedded.jpg",
    "evidence_73_attendance10_extreme_qa_validation_findings.png"
]

for fn in evidence_files:
    p = os.path.join("defect_evidence", fn)
    exists = os.path.exists(p)
    sz = os.path.getsize(p) if exists else 0
    print(f"{fn}: Exists={exists}, Size={sz} bytes")
