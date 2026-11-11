import json
import requests
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open("scratch/current_token.json") as f:
    token = json.load(f)["access_token"]

cid = "3a249872-2d69-f931-41f6-d8db086b09b8"
headers = {"Authorization": f"Bearer {token}"}

print("=== SYNC STATUS ===")
r = requests.get(f"https://attendance2.dev.zoolwork.com/api/companies/{cid}/worktemplates/company-default/sync-status", headers=headers)
print("Status code:", r.status_code)
print(json.dumps(r.json(), indent=2, ensure_ascii=False))

print("\n=== VERSIONS ===")
r = requests.get(f"https://attendance2.dev.zoolwork.com/api/companies/{cid}/worktemplates/company-default/versions", headers=headers)
print("Status code:", r.status_code)
print(json.dumps(r.json(), indent=2, ensure_ascii=False))

