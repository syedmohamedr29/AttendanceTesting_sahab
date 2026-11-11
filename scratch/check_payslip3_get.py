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
c3 = "3a247eed-b8da-b2fd-08b1-e2d8673d9da8" # Payslip 3
r = requests.get(f"{base_url}/api/companies/{c3}/worktemplates", headers=headers)
if r.status_code == 200:
    for t in r.json().get('templates', []):
        print(f"Payslip 3 ID: {t.get('id')} | TenantName: {t.get('tenantName')}")

