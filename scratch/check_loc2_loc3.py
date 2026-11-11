import requests
import json
import urllib3
import sys

urllib3.disable_warnings()
sys.stdout.reconfigure(encoding='utf-8')

with open('scratch/current_token.json', 'r') as f:
    token = json.load(f)['access_token']

headers = {
    'Authorization': f'Bearer {token}',
    'Accept': 'application/json'
}

company_id = '3a249871-7a8d-dec5-2d72-47795dd2662d'
loc2_id = '3a24d646-b3cf-b1d4-61bb-1adf094b52fc'
loc3_id = '3a24d667-0dcc-e3d1-74a3-cbee98168772'

for name, lid in [("Location 2", loc2_id), ("Location 3", loc3_id)]:
    r = requests.get(f'https://attendance2.dev.zoolwork.com/api/companies/{company_id}/worktemplates?locationId={lid}', headers=headers, verify=False)
    print(f"=== {name} ({lid}) ===")
    print(f"Status: {r.status_code}")
    if r.status_code == 200:
        templates = r.json().get('templates', [])
        print(f"Total templates: {len(templates)}")
        for t in templates:
            print(f"  ID: {t.get('id')} | Code: {t.get('shortCode')} | Type: {t.get('templateType')} | Name: {t.get('workTemplateName', {}).get('en')}")
