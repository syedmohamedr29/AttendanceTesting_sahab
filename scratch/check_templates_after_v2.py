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
loc_id = '3a24d629-0d56-a428-baa1-98493a77e614'

r = requests.get(f'https://attendance2.dev.zoolwork.com/api/companies/{company_id}/worktemplates?locationId={loc_id}', headers=headers, verify=False)
print(f"Status: {r.status_code}")
if r.status_code == 200:
    templates = r.json().get('templates', [])
    print(f"Total templates in Location 1 now: {len(templates)}")
    with open('scratch/loc1_templates_after_v2.json', 'w', encoding='utf-8') as f:
        json.dump(templates, f, indent=2, ensure_ascii=False)
    
    for t in templates:
        name = t.get('workTemplateName', {})
        print(f"ID: {t.get('id')} | ShortCode: {t.get('shortCode')} | Type: {t.get('templateType')} | Version: {t.get('version')} | CreatedAt: {t.get('createdAt')} | ModifiedAt: {t.get('modifiedAt')} | Name: {name.get('en')}")
