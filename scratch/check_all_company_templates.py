import requests
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('scratch/current_token.json') as f:
    token_data = json.load(f)

token = token_data['access_token']
headers = {
    'Authorization': f'Bearer {token}',
    '__tenant': 'Attendance',
    'Accept': 'application/json'
}

base_url = "https://attendance2.dev.zoolwork.com"

companies = {
    "Attendance 3": "3a247435-e31d-ef15-8cc9-62c587f4eb3f",
    "Attendance 4": "3a247436-8669-844a-7d2f-1a209af02d8e",
    "Attendance 5": "3a247437-34e2-a501-5d36-c3f764adc19d",
    "Attendance 8": "3a249871-7a8d-dec5-2d72-47795dd2662d"
}

for name, cid in companies.items():
    r = requests.get(f"{base_url}/api/companies/{cid}/worktemplates", headers=headers)
    print(f"\n=== {name} ({cid}) ===")
    if r.status_code == 200:
        data = r.json().get('templates', [])
        print(f"Total templates: {len(data)}")
        for t in data:
            print(f"  ID: {t.get('id')} | Type: {t.get('type')} | Status: {t.get('status')} | Version: {t.get('version')} | IsDefault: {t.get('isDefault')} | TenantName: {t.get('tenantName')}")
    else:
        print(f"  Error: {r.status_code} - {r.text}")

