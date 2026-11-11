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

# 1. GET worktemplates
r_wt = requests.get(f"{base_url}/api/companies/{company_id}/worktemplates", headers=auth_headers)
print(f"=== 1. Work Templates (HTTP {r_wt.status_code}) ===")
print(r_wt.text)

# 2. GET sync-status
r_sync = requests.get(f"{base_url}/api/companies/{company_id}/worktemplates/company-default/sync-status", headers=auth_headers)
print(f"\n=== 2. Sync Status (HTTP {r_sync.status_code}) ===")
print(r_sync.text)

# 3. GET versions
r_ver = requests.get(f"{base_url}/api/companies/{company_id}/worktemplates/company-default/versions", headers=auth_headers)
print(f"\n=== 3. Versions (HTTP {r_ver.status_code}) ===")
print(r_ver.text)

# 4. Check company locations
r_loc = requests.get(f"https://company8.dev.zoolwork.com/api/companies/{company_id}/locations", headers=auth_headers)
print(f"\n=== 4. Company Locations (HTTP {r_loc.status_code}) ===")
print(r_loc.text[:500] if r_loc.status_code == 200 else r_loc.text)

