import requests
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('scratch/target_company.json') as f:
    target = json.load(f)
with open('scratch/current_token.json') as f:
    token_data = json.load(f)

company_id = target["company_id"]
tenant = target["tenant"]
token = token_data["access_token"]

headers = {
    "Authorization": f"Bearer {token}",
    "__tenant": tenant,
    "Accept": "application/json"
}

# 1. GET worktemplates list
url_list = f"https://attendance2.dev.zoolwork.com/api/companies/{company_id}/worktemplates"
r_list = requests.get(url_list, headers=headers)
print(f"=== 1. GET {url_list} ===")
print(f"Status Code: {r_list.status_code}")
data = r_list.json() if r_list.status_code == 200 else r_list.text
print(json.dumps(data, indent=2, ensure_ascii=False)[:600])

# 2. GET sync-status
url_sync = f"https://attendance2.dev.zoolwork.com/api/companies/{company_id}/worktemplates/company-default/sync-status"
r_sync = requests.get(url_sync, headers=headers)
print(f"\n=== 2. GET {url_sync} ===")
print(f"Status Code: {r_sync.status_code}")
print(r_sync.text)

# 3. GET versions
url_ver = f"https://attendance2.dev.zoolwork.com/api/companies/{company_id}/worktemplates/company-default/versions"
r_ver = requests.get(url_ver, headers=headers)
print(f"\n=== 3. GET {url_ver} ===")
print(f"Status Code: {r_ver.status_code}")
print(r_ver.text[:400])

