import sys
import json
import requests

sys.stdout.reconfigure(encoding='utf-8')

with open("scratch/current_token.json") as f:
    token_info = json.load(f)

token = token_info["access_token"]
c9_id = "3a249872-2d69-f931-41f6-d8db086b09b8" # Attendance 9

headers = {
    "Authorization": f"Bearer {token}",
    "__tenant": "Attendance",
    "Content-Type": "application/json",
    "Accept": "application/json"
}

base_att = "https://attendance2.dev.zoolwork.com"
base_cmp = "https://company8.dev.zoolwork.com"

print(f"=== INITIAL STATE CHECK FOR ATTENDANCE 9 ({c9_id}) ===")

# 1. Existing Work Templates
r_wt = requests.get(f"{base_att}/api/companies/{c9_id}/worktemplates", headers=headers)
print(f"GET /worktemplates: HTTP {r_wt.status_code}")
print(r_wt.text[:500])

# 2. Company Default Sync Status
r_sync = requests.get(f"{base_att}/api/companies/{c9_id}/worktemplates/company-default/sync-status", headers=headers)
print(f"\nGET /company-default/sync-status: HTTP {r_sync.status_code}")
print(r_sync.text[:500])

# 3. Company Default Versions
r_ver = requests.get(f"{base_att}/api/companies/{c9_id}/worktemplates/company-default/versions", headers=headers)
print(f"\nGET /company-default/versions: HTTP {r_ver.status_code}")
print(r_ver.text[:500])

# 4. Company Service Checklist
r_chk = requests.get(f"{base_cmp}/api/company/companies/{c9_id}/getChecklist", headers=headers)
print(f"\nGET Company Checklist: HTTP {r_chk.status_code}")
print(r_chk.text[:500])

