import requests
import json
import os

with open('scratch/confluence_config.json', 'r') as f:
    cfg = json.load(f)

auth = (cfg['email'], cfg['api_token'])
base_url = cfg['confluence_url']
page_id = cfg['page_id']

image_path = 'defect_evidence/evidence_02_companiesmaster_checklist_false.png'
if not os.path.exists(image_path):
    raise FileNotFoundError(f"{image_path} does not exist!")

filename = os.path.basename(image_path)
print(f"Uploading {filename} to page {page_id}...")

url = f"{base_url}/rest/api/content/{page_id}/child/attachment"
headers = {
    "X-Atlassian-Token": "nocheck"
}

with open(image_path, 'rb') as f:
    files = {
        'file': (filename, f, 'image/png')
    }
    r = requests.post(url, auth=auth, headers=headers, files=files)

print("Attachment upload status:", r.status_code)
if r.status_code in (200, 201):
    res = r.json()
    att_results = res.get('results', [])
    att_name = att_results[0].get('title') if att_results else filename
    print(f"Successfully attached {att_name} to page {page_id}!")
else:
    print("Error uploading attachment:", r.text)
