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

res = requests.get("https://company8.dev.zoolwork.com/api/company/companies/CompanyShortList", headers=headers)
companies = res.json()
print("Total companies:", len(companies))
print("First item keys:", companies[0].keys() if companies else "Empty")
for c in companies:
    print(json.dumps(c, ensure_ascii=False))

