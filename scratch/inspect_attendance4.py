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
    "Accept": "application/json",
    "Content-Type": "application/json"
}

# 1. Query Company Service for Attendance 4
print("Querying Company Service...")
resp_c = requests.get("https://company8.dev.zoolwork.com/api/company/companies", headers=headers, timeout=10)
print(f"Company Service HTTP: {resp_c.status_code}")
if resp_c.status_code == 200:
    companies = resp_c.json()
    att4 = next((c for c in companies if "attendance 4" in c.get("companyName", {}).get("en", "").lower() or "attendance 4" in str(c.get("companyName", {})).lower() or "attendance4" in str(c.get("companyName", {})).lower()), None)
    if att4:
        print(f"Found Attendance 4:")
        print(f"  ID: {att4.get('id')}")
        print(f"  Name: {att4.get('companyName')}")
        print(f"  Code: {att4.get('companyCode')}")
    else:
        print("Attendance 4 not found by name. List of all companies:")
        for c in companies:
            print(f"  - {c.get('id')}: {c.get('companyName')}")

# 2. Query Attendance Service for Attendance 4 work templates
att4_id = "3a247436-8669-844a-7d2f-1a209af02d8e"
print(f"\nQuerying Attendance Service for company {att4_id}...")
resp_att = requests.get(f"https://attendance2.dev.zoolwork.com/api/companies/{att4_id}/worktemplates", headers=headers, timeout=10)
print(f"Attendance Service HTTP: {resp_att.status_code}")
if resp_att.status_code == 200:
    templates = resp_att.json()
    print(f"Work Templates count: {len(templates)}")
    for t in templates:
        print(f"  ID: {t.get('id')} | Name: {t.get('templateName')} | Type: {t.get('templateType')} | Status: {t.get('status')} | Version: {t.get('version')} | IsDefault: {t.get('isDefault')} | ShortCode: {t.get('shortCode')}")

# 3. Query Company Checklist for Attendance 4
print(f"\nQuerying Checklist for company {att4_id}...")
resp_chk = requests.get(f"https://company8.dev.zoolwork.com/api/company/companies/{att4_id}/getChecklist", headers=headers, timeout=10)
print(f"Checklist HTTP: {resp_chk.status_code}")
if resp_chk.status_code == 200:
    print("Checklist:", json.dumps(resp_chk.json(), indent=2))

