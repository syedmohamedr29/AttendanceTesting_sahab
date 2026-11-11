import sys
import json
import requests

sys.stdout.reconfigure(encoding='utf-8')

with open("scratch/current_token.json") as f:
    token_info = json.load(f)

token = token_info["access_token"]
headers = {
    "Authorization": f"Bearer {token}",
    "__tenant": "Attendance",
    "Accept": "application/json"
}

url = "https://company8.dev.zoolwork.com/api/company/companies/CompanyShortList"
r = requests.get(url, headers=headers, timeout=10)
print(f"Status: {r.status_code}")
if r.status_code == 200:
    companies = r.json()
    print(f"Total companies found: {len(companies)}")
    for c in companies:
        name = c.get('name') or c.get('companyName') or c
        cid = c.get('id') or c.get('companyId')
        print(f"Company: {name} | ID: {cid}")
else:
    print(r.text)

