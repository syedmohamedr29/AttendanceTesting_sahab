import requests
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open("scratch/current_token.json") as f:
    token_info = json.load(f)

token = token_info["access_token"]
company_id = "3a247435-3cea-83ae-6a9f-6dda99f386a3"

headers = {
    "Authorization": f"Bearer {token}",
    "__tenant": "Attendance",
    "Accept": "application/json"
}

r = requests.get(f"https://company8.dev.zoolwork.com/api/company/worklocations/companyWorkLocationList?companyId={company_id}", headers=headers)
print("Locations Status:", r.status_code)
if r.status_code == 200:
    locs = r.json()
    print("Locations:", json.dumps(locs, indent=2, ensure_ascii=False))
    with open("scratch/attendance2_locations.json", "w", encoding='utf-8') as f:
        json.dump(locs, f, indent=2, ensure_ascii=False)
else:
    print("Response:", r.text)

# Also check company checklist status
r_chk = requests.get(f"https://company8.dev.zoolwork.com/api/company/companies/{company_id}/getChecklist", headers=headers)
print("\nChecklist Status:", r_chk.status_code)
if r_chk.status_code == 200:
    chk = r_chk.json()
    print("Checklist:", json.dumps(chk, indent=2, ensure_ascii=False))
    with open("scratch/attendance2_checklist.json", "w", encoding='utf-8') as f:
        json.dump(chk, f, indent=2, ensure_ascii=False)

