import requests
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open("scratch/target_company.json") as f:
    target = json.load(f)

with open("scratch/current_token.json") as f:
    token_data = json.load(f)

company_id = target["company_id"]
token = token_data["access_token"]
tenant = target["tenant"]

headers = {
    "Authorization": f"Bearer {token}",
    "__tenant": tenant,
    "Accept": "application/json"
}

url = f"https://attendance2.dev.zoolwork.com/api/companies/{company_id}/worktemplates"
r = requests.get(url, headers=headers)
print("GET /worktemplates Status:", r.status_code)
if r.status_code == 200:
    data = r.json()
    items = data.get("items", data) if isinstance(data, dict) else data
    print(f"Total templates found: {len(items)}")
    for t in items:
        print(f"ID: {t.get('id')} | Name: {t.get('templateName')} | Code: {t.get('shortCode')} | Type: {t.get('templateType')} | isDefault: {t.get('isDefault')} | State: {t.get('state')}")
        with open("scratch/existing_templates.json", "w", encoding='utf-8') as f:
            json.dump(items, f, indent=2, ensure_ascii=False)
else:
    print("Response:", r.text)

# Also check versions endpoint
r_ver = requests.get(f"https://attendance2.dev.zoolwork.com/api/companies/{company_id}/worktemplates/company-default/versions", headers=headers)
print("\nGET /company-default/versions Status:", r_ver.status_code)
if r_ver.status_code == 200:
    print("Versions:", json.dumps(r_ver.json(), indent=2)[:500])

# Also check sync-status endpoint
r_sync = requests.get(f"https://attendance2.dev.zoolwork.com/api/companies/{company_id}/worktemplates/company-default/sync-status", headers=headers)
print("\nGET /company-default/sync-status Status:", r_sync.status_code)
if r_sync.status_code == 200:
    print("Sync Status:", json.dumps(r_sync.json(), indent=2))

