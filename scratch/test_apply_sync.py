import requests
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

company_id = "3a249871-7a8d-dec5-2d72-47795dd2662d" # Attendance 8

with open("scratch/current_token.json") as f:
    token_data = json.load(f)

token = token_data["access_token"]
tenant = "Attendance"
base_url = "https://attendance2.dev.zoolwork.com"
auth_headers = {
    "Authorization": f"Bearer {token}",
    "__tenant": tenant,
    "Content-Type": "application/json",
    "Accept": "application/json"
}

r_apply = requests.post(f"{base_url}/api/companies/{company_id}/worktemplates/apply-sync", headers=auth_headers)
print(f"Apply-sync: HTTP {r_apply.status_code}")
print(r_apply.text)

r_sync = requests.get(f"{base_url}/api/companies/{company_id}/worktemplates/company-default/sync-status", headers=auth_headers)
print(f"Sync-status after apply-sync: HTTP {r_sync.status_code}")
print(r_sync.text)

