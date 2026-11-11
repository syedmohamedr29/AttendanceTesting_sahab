import requests
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('scratch/current_token.json') as f:
    token_data = json.load(f)

token = token_data['access_token']
headers = {
    'Authorization': f'Bearer {token}',
    '__tenant': 'Attendance',
    'Accept': 'application/json'
}

base_url = "https://attendance2.dev.zoolwork.com"
c8 = "3a249871-7a8d-dec5-2d72-47795dd2662d"
r = requests.get(f"{base_url}/api/companies/{c8}/worktemplates", headers=headers)
data = r.json()
print("Templates count:", len(data.get("templates", [])))
for t in data.get("templates", []):
    print("Template keys:", list(t.keys()))
    print("ID:", t.get("id"))
    print("Name:", t.get("name") or t.get("workTemplateName"))
    print("Type:", t.get("type"))
    print("TenantName in GET response?:", "tenantName" in t or "TenantName" in t)
    if "tenantName" in t:
        print("tenantName:", t["tenantName"])
    if "TenantName" in t:
        print("TenantName:", t["TenantName"])
