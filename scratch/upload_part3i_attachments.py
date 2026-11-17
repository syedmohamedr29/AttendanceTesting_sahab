import json
import requests
import os

CONFIG_FILE = 'scratch/confluence_config.json'

with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
    cfg = json.load(f)

auth = (cfg['email'], cfg['api_token'])
base_url = cfg['confluence_url']
page_id = cfg['page_id']

files_to_upload = [
    "evidence_52_cdwt_edit_cascade_failure_haspendinglocsync_true_compass.png",
    "evidence_53_cdwt_patch_sets_haspendinglocsync_true_not_auto_overwrite_compass.png",
    "evidence_54_regular_shift_location_post_patch_audit_wipeout_compass.png",
    "evidence_55_fixed_wt_location_patch_validation_bypasses_and_db_results.png",
    "evidence_56_flexi_split_location_validation_bypasses_and_db_results.png",
    "evidence_57_worktemplate_delete_lifecycle_and_bypasses.png",
    "evidence_58_rotation_worktemplate_lifecycle_and_defects.png"
]

upload_url = f"{base_url}/rest/api/content/{page_id}/child/attachment"
headers = {"X-Atlassian-Token": "nocheck"}

for fname in files_to_upload:
    fpath = os.path.join("defect_evidence", fname)
    if not os.path.exists(fpath):
        print(f"File not found: {fpath}")
        continue
    
    print(f"Uploading {fname} ({os.path.getsize(fpath)} bytes)...")
    with open(fpath, "rb") as f:
        files = {"file": (fname, f, "image/png")}
        r = requests.post(upload_url, auth=auth, headers=headers, files=files)
        print(f"Response: {r.status_code}")
        if r.status_code not in (200, 201):
            print(f"Error: {r.text[:300]}")
