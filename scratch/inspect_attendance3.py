import requests
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('scratch/current_token.json') as f:
    token_data = json.load(f)

token = token_data['access_token']
company_id = "3a247435-e31d-ef15-8cc9-62c587f4eb3f"
tenant = "Attendance"

headers = {
    'Authorization': f'Bearer {token}',
    '__tenant': tenant,
    'Accept': 'application/json'
}

# 1. Inspect Company 3 in Company Service
print("=== 1. Company 3 in Company Service ===")
res_comp = requests.get(f"https://company8.dev.zoolwork.com/api/company/companies/{company_id}", headers=headers)
print(f"Status: {res_comp.status_code}")
if res_comp.status_code == 200:
    comp_json = res_comp.json()
    checklist = comp_json.get("companyChecklist", {})
    print("Company Checklist:")
    print(json.dumps(checklist, indent=2))
else:
    print(res_comp.text)

# 2. Inspect Locations for Company 3
print("\n=== 2. Locations for Company 3 ===")
res_loc = requests.get(f"https://company8.dev.zoolwork.com/api/company/locations/by-company/{company_id}", headers=headers)
print(f"Status: {res_loc.status_code}")
if res_loc.status_code == 200:
    print(json.dumps(res_loc.json(), indent=2))
else:
    print(res_loc.text)

# 3. Inspect Work Templates for Company 3 in Attendance Service
print("\n=== 3. Work Templates for Company 3 ===")
res_wt = requests.get(f"https://attendance2.dev.zoolwork.com/api/companies/{company_id}/worktemplates", headers=headers)
print(f"Status: {res_wt.status_code}")
if res_wt.status_code == 200:
    print(json.dumps(res_wt.json(), indent=2))
else:
    print(res_wt.text)

