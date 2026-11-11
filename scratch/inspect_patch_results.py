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

tests = [
    ("Payslip 2", "3a247eed-01f0-8dc3-c935-1338bd373d88", "PATCH Fixed"),
    ("Payslip 3", "3a247eed-b8da-b2fd-08b1-e2d8673d9da8", "PATCH Flexi"),
    ("Payslip 4", "3a247eee-6ca6-1b8c-4e34-6ea5c08e0837", "PATCH Split")
]

for name, cid, op in tests:
    r = requests.get(f"{base_url}/api/companies/{cid}/worktemplates", headers=headers)
    print(f"\n=== {name} ({op}) ===")
    if r.status_code == 200:
        data = r.json().get('templates', [])
        for t in data:
            print(f"ID: {t.get('id')} | Version: {t.get('version')} | Status: {t.get('status')} | TenantName: {t.get('tenantName')}")

