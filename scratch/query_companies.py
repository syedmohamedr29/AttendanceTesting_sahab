import requests
import json

with open("scratch/current_token.json") as f:
    token_info = json.load(f)

token = token_info["access_token"]
tenant_id = token_info["tenant_id"]

headers = {
    "Authorization": f"Bearer {token}",
    "__tenant": "Attendance",
    "Accept": "application/json"
}

endpoints = [
    "https://company8.dev.zoolwork.com/api/company/companies/companyList",
    "https://company8.dev.zoolwork.com/api/company/companies/CompanyShortList",
    "https://company8.dev.zoolwork.com/api/company/companies/companyAndUnitBasics",
    "https://company8.dev.zoolwork.com/api/company/remote/companyCache"
]

for ep in endpoints:
    try:
        r = requests.get(ep, headers=headers, timeout=10)
        print(f"\nEndpoint: {ep} -> Status: {r.status_code}")
        if r.status_code == 200:
            data = r.json()
            print("Response:", json.dumps(data, indent=2)[:500])
            items = data.get("items", data) if isinstance(data, dict) else data
            if isinstance(items, list):
                for item in items:
                    print("  Company Item:", item)
    except Exception as e:
        print("Error:", e)

