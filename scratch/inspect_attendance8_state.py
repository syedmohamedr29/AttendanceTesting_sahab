import requests
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open("scratch/current_token.json") as f:
    token_data = json.load(f)

token = token_data["access_token"]
company_id = "3a249871-7a8d-dec5-2d72-47795dd2662d" # Attendance 8

headers = {
    "Authorization": f"Bearer {token}",
    "__tenant": "Attendance",
    "Accept": "application/json"
}

base_url = "https://attendance2.dev.zoolwork.com"

print(f"Checking state for Company: Attendance 8 ({company_id})")

# 1. Check existing work templates
url_wt = f"{base_url}/api/companies/{company_id}/worktemplates"
r_wt = requests.get(url_wt, headers=headers, timeout=10)
print(f"1. Work Templates Status: {r_wt.status_code}")
if r_wt.status_code == 200:
    data = r_wt.json()
    items = data.get("data", {}).get("items", []) or data.get("items", []) or data.get("templates", []) or (data if isinstance(data, list) else [])
    print(f"Total Work Templates found: {len(items)}")
    for it in items:
        print(f"  ID: {it.get('id')} | ShortCode: {it.get('shortCode')} | IsDefault: {it.get('isDefault')} | Name: {it.get('templateName')} | LocId: {it.get('locationId')}")
else:
    print("WT error response:", r_wt.text)

# 2. Check sync status
url_sync = f"{base_url}/api/companies/{company_id}/worktemplates/company-default/sync-status"
r_sync = requests.get(url_sync, headers=headers, timeout=10)
print(f"2. Sync Status: {r_sync.status_code}")
print(f"Sync Body: {r_sync.text}")

# 3. Check locations for Attendance 8
comp_url = f"https://company8.dev.zoolwork.com/api/company/worklocations/company/{company_id}"
r_loc = requests.get(comp_url, headers=headers, timeout=10)
print(f"3. Work Locations Status: {r_loc.status_code}")
if r_loc.status_code == 200:
    locs = r_loc.json()
    print(f"Total Locations found: {len(locs)}")
    for l in locs:
        print(f"  Loc ID: {l.get('id')} | Code: {l.get('shortCode')} | Name: {l.get('name')}")
else:
    print("Locations error response:", r_loc.text)

