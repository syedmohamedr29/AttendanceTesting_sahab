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
    'defect_evidence/evidence_19_holiday_calendar_tenantname_empty_red_circle.jpg'
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
