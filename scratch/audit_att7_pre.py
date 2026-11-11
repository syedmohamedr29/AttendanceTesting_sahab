import json
import requests
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open("scratch/current_token.json") as f:
    token = json.load(f)["access_token"]

cid = "3a249870-c8ae-b3dc-1b8d-c44efad14f89" # Attendance 7

headers = {
    "Authorization": f"Bearer {token}",
    "__tenant": "Attendance",
    "Accept": "application/json"
}

print("=== 1. PRE-CREATION AUDIT: WORK TEMPLATES ===")
r = requests.get(f"https://attendance2.dev.zoolwork.com/api/companies/{cid}/worktemplates", headers=headers)
print("Work templates status:", r.status_code, r.text)

print("\n=== 2. PRE-CREATION AUDIT: SYNC STATUS ===")
r = requests.get(f"https://attendance2.dev.zoolwork.com/api/companies/{cid}/worktemplates/company-default/sync-status", headers=headers)
print("Sync status:", r.status_code, r.text)

print("\n=== 3. PRE-CREATION AUDIT: SHORTCODE AVAILABILITY (ATT7FIX) ===")
r = requests.get(f"https://attendance2.dev.zoolwork.com/api/companies/{cid}/worktemplates/short-code/availability?code=ATT7FIX", headers=headers)
print("ShortCode ATT7FIX availability:", r.status_code, r.text)

print("\n=== 4. PRE-CREATION AUDIT: COMPANY CHECKLIST (SP.CompanySvc) ===")
r = requests.get(f"https://company8.dev.zoolwork.com/api/company/companies/{cid}/getChecklist", headers=headers)
print("Company checklist status:", r.status_code, r.text)

