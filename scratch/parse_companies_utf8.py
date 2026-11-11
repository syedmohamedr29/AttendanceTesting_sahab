import requests
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open("scratch/current_token.json") as f:
    token_info = json.load(f)

token = token_info["access_token"]

headers = {
    "Authorization": f"Bearer {token}",
    "__tenant": "Attendance",
    "Accept": "application/json"
}

r = requests.get("https://company8.dev.zoolwork.com/api/company/companies/CompanyShortList", headers=headers)
print("Status:", r.status_code)
companies = r.json()
print(f"Total companies found: {len(companies)}")

for idx, c in enumerate(companies, 1):
    c_id = c.get("id")
    c_name = c.get("companyName")
    print(f"{idx}. ID: {c_id} | Name: {c_name} | Email: {c.get('emailId')}")

# Save the full company list to json
with open("scratch/companies_list.json", "w", encoding='utf-8') as f:
    json.dump(companies, f, indent=2, ensure_ascii=False)

