import json
import requests
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open("scratch/current_token.json") as f:
    token = json.load(f)["access_token"]

headers = {
    "Authorization": f"Bearer {token}",
    "__tenant": "Attendance",
    "Accept": "application/json"
}

print("=== LOOKING UP ATTENDANCE 7 IN COMPANY SHORT LIST ===")
res = requests.get("https://company8.dev.zoolwork.com/api/company/companies/CompanyShortList", headers=headers)
print("Status:", res.status_code)
companies = res.json()
target = None
for c in companies:
    name_en = c.get("name", {}).get("en", "")
    name_ar = c.get("name", {}).get("ar", "")
    print(f"Company: {name_en} | {name_ar} | ID: {c.get('id')}")
    if "7" in name_en or "Attendance 7" in name_en:
        target = c

if target:
    print("\nTARGET FOUND:", json.dumps(target, indent=2, ensure_ascii=False))
else:
    print("\nTarget Attendance 7 NOT FOUND directly by exact match. Check full list above.")

