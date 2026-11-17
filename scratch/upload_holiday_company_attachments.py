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
    'defect_evidence/evidence_29_holiday_calendar_end_date_before_start_date_accepted.png',
    'defect_evidence/evidence_32_holiday_patch_1706_current_year_today_blocked_swagger.png',
    'defect_evidence/evidence_24_holiday_calendar_empty_holidaylists_array_accepted.jpg',
    'defect_evidence/evidence_30_holiday_calendar_holiday_outside_calendar_year.jpg',
    'defect_evidence/evidence_25_holiday_calendar_duplicate_shortcode_allowed.jpg'
]

att_url = f"{base_url}/rest/api/content/{page_id}/child/attachment"
headers = {"X-Atlassian-Token": "nocheck"}

for img_path in attachments:
    filename = os.path.basename(img_path)
    mime = 'image/jpeg' if filename.endswith('.jpg') else 'image/png'
    print(f"Uploading {filename} to page {page_id}...")
    with open(img_path, 'rb') as f:
        files = {'file': (filename, f, mime)}
        r = requests.post(att_url, auth=auth, headers=headers, files=files)
        print(f"Status for {filename}: {r.status_code}")
