import requests
import json
import urllib3
urllib3.disable_warnings()

with open('scratch/current_token.json', 'r') as f:
    token = json.load(f)['access_token']

headers = {
    'Authorization': f'Bearer {token}',
    'Accept': 'application/json'
}

company_id = '3a249871-7a8d-dec5-2d72-47795dd2662d'
loc_ids = [
    '3a24d629-0d56-a428-baa1-98493a77e614', # Loc 1
    '3a24d646-b3cf-b1d4-61bb-1adf094b52fc', # Loc 2
    '3a24d667-0dcc-e3d1-74a3-cbee98168772'  # Loc 3
]

print("=== Company Templates (no location) ===")
r = requests.get(f'https://attendance2.dev.zoolwork.com/api/companies/{company_id}/worktemplates', headers=headers, verify=False)
print(f"Status: {r.status_code}")
if r.status_code == 200:
    items = r.json().get('templates', [])
    for it in items:
        print(f"ID: {it.get('id')} | ShortCode: {it.get('shortCode')} | Type: {it.get('templateType')} | Default: {it.get('isDefault')} | LocLinked: {it.get('isCompanyLinked')}")

for lid in loc_ids:
    print(f"\n=== Location Templates for {lid} ===")
    r = requests.get(f'https://attendance2.dev.zoolwork.com/api/companies/{company_id}/worktemplates?locationId={lid}', headers=headers, verify=False)
    if r.status_code == 200:
        items = r.json().get('templates', [])
        for it in items:
            print(f"ID: {it.get('id')} | ShortCode: {it.get('shortCode')} | Type: {it.get('templateType')} | Default: {it.get('isDefault')} | LocLinked: {it.get('isCompanyLinked')}")
