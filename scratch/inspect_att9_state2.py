import json
import requests
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open("scratch/current_token.json") as f:
    token = json.load(f)["access_token"]

cid = "3a249872-2d69-f931-41f6-d8db086b09b8"
headers = {"Authorization": f"Bearer {token}"}

print("=== 2. SYNC STATUS ===")
r = requests.get(f"https://attendance2.dev.zoolwork.com/api/companies/{cid}/company-default/sync-status", headers=headers)
print("Sync status code:", r.status_code)
print("Sync status text:", r.text)

print("\n=== 3. VERSIONS ===")
r = requests.get(f"https://attendance2.dev.zoolwork.com/api/companies/{cid}/company-default/versions", headers=headers)
print("Versions status code:", r.status_code)
print("Versions text:", r.text)

print("\n=== 4. GET PREVIOUS FLEXI TEMPLATE ===")
r = requests.get(f"https://attendance2.dev.zoolwork.com/api/companies/{cid}/worktemplates/7328b6a5-4dcd-411f-8c2a-6fd2d2f86615", headers=headers)
print("Flexi template status code:", r.status_code)
print("Flexi template text:", r.text)

print("\n=== 5. GET NEW FIXED TEMPLATE ===")
r = requests.get(f"https://attendance2.dev.zoolwork.com/api/companies/{cid}/worktemplates/d5abe5c4-d51f-4287-9baf-38e2e4f547c8", headers=headers)
print("Fixed template status code:", r.status_code)
print("Fixed template text:", r.text)

