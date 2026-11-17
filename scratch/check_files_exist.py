import os

evidences = [
    'defect_evidence/evidence_40_swagger_policy_tenantname_id_in_request_body.png',
    'defect_evidence/evidence_41_overtime_policy_negative_rateformula_accepted_compass.png',
    'defect_evidence/evidence_42_policy_tenantname_empty_object_compass.png',
    'defect_evidence/evidence_43_policy_duplicate_id_mongo_500_crash.png',
    'defect_evidence/evidence_44_attendance7_reverification_defects_compass.png',
    'defect_evidence/evidence_45_api_request_body_invalid_structure_id_tenantname_comparison.png',
    'defect_evidence/evidence_46_break_policy_500_crash_null_break_and_duplicate_breaks_compass.png',
    'defect_evidence/evidence_47_grace_period_patch_invalid_enums_and_threshold_accepted_compass.png',
    'defect_evidence/evidence_48_policy_omitted_tenantname_persists_as_empty_object_compass.png',
    'defect_evidence/evidence_49_policy_type_string_vs_db_enum_int_compass.png',
    'defect_evidence/evidence_50_misleading_duplicate_policy_error_1505_compass.png',
]

for ev in evidences:
    print(f"{ev}: {os.path.exists(ev)}")
