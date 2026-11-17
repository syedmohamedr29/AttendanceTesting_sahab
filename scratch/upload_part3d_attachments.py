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
    'defect_evidence/evidence_09_split_overlap_500_validation_exception.png',
    'defect_evidence/evidence_01_worktemplates_created_with_placeholder.png',
    'defect_evidence/evidence_14_att4_patch_shortcode_locked_1107.png',
    'defect_evidence/evidence_08_negative_grace_accepted_200.png',
    'defect_evidence/evidence_15_att4_patch_empty_payload_500.png',
    'defect_evidence/evidence_10_negative_break_accepted_200.png',
    'defect_evidence/evidence_12_calendar_sum_not_7_500_validation_exception.png'
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
