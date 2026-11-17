import requests
import json
import os

CONFIG_FILE = 'scratch/confluence_config.json'

with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
    cfg = json.load(f)

auth = (cfg['email'], cfg['api_token'])
base_url = cfg['confluence_url']
page_id = cfg['page_id']

attachments = [
    'defect_evidence/evidence_40_swagger_policy_tenantname_id_in_request_body.png',
    'defect_evidence/evidence_41_overtime_policy_negative_rateformula_accepted_compass.png',
    'defect_evidence/evidence_42_policy_tenantname_empty_object_compass.png',
    'defect_evidence/evidence_43_policy_duplicate_id_mongo_500_crash.png',
    'defect_evidence/evidence_44_attendance7_reverification_defects_compass.png',
    'defect_evidence/evidence_45_api_request_body_invalid_structure_id_tenantname_comparison.png',
    'defect_evidence/evidence_46_break_policy_500_crash_null_break_and_duplicate_breaks_compass.png',
    'defect_evidence/evidence_47_grace_period_patch_invalid_enums_and_threshold_accepted_compass.png',
    'defect_evidence/evidence_49_policy_type_string_vs_db_enum_int_compass.png',
    'defect_evidence/evidence_50_misleading_duplicate_policy_error_1505_compass.png'
]

att_url = f"{base_url}/rest/api/content/{page_id}/child/attachment"
headers = {"X-Atlassian-Token": "nocheck"}

for img_path in attachments:
    filename = os.path.basename(img_path)
    mime = 'image/jpeg' if filename.endswith('.jpg') else 'image/png'
    print(f"Uploading {filename} to page {page_id}...")
    with open(img_path, 'rb') as f:
        files = {'file': (filename, f, mime)}
        r_att = requests.post(att_url, auth=auth, headers=headers, files=files)
        print(f"  {filename} upload status: {r_att.status_code}")
        if r_att.status_code not in [200, 201]:
            print(f"  Response: {r_att.text[:200]}")
