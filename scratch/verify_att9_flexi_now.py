import json
import requests
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open("scratch/current_token.json") as f:
    token = json.load(f)["access_token"]

cid = "3a249872-2d69-f931-41f6-d8db086b09b8"
tid = "d74a3552-d519-4aae-a8d8-94df00de2fe0"

headers = {
    "Authorization": f"Bearer {token}",
    "__tenant": "Attendance",
    "Accept": "application/json"
}

print("=== 1. GET WORK TEMPLATE BY ID ===")
r_get = requests.get(f"https://attendance2.dev.zoolwork.com/api/companies/{cid}/worktemplates/{tid}", headers=headers)
print("Status:", r_get.status_code)
print(json.dumps(r_get.json(), indent=2, ensure_ascii=False))

print("\n=== 2. GET SYNC STATUS ===")
r_sync = requests.get(f"https://attendance2.dev.zoolwork.com/api/companies/{cid}/worktemplates/company-default/sync-status", headers=headers)
print("Status:", r_sync.status_code)
print(json.dumps(r_sync.json(), indent=2, ensure_ascii=False))

print("\n=== 3. GET VERSION HISTORY ===")
r_ver = requests.get(f"https://attendance2.dev.zoolwork.com/api/companies/{cid}/worktemplates/company-default/versions", headers=headers)
print("Status:", r_ver.status_code)
print(json.dumps(r_ver.json(), indent=2, ensure_ascii=False))

print("\n=== 4. GET COMPANY CHECKLIST (SP.CompanySvc) ===")
r_chk = requests.get(f"https://company8.dev.zoolwork.com/api/company/companies/{cid}/getChecklist", headers=headers)
print("Status:", r_chk.status_code)
print(json.dumps(r_chk.json(), indent=2, ensure_ascii=False))

