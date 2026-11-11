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

r = requests.get(f"https://attendance2.dev.zoolwork.com/api/companies/{company_id}/worktemplates", headers=headers)
print("GET /worktemplates Status:", r.status_code)
templates = r.json().get("templates", [])
print(f"Total templates now: {len(templates)}")
for t in templates:
    print(f"ID: {t.get('id')} | State: {t.get('status')} | isDeleted: {t.get('isDeleted')} | isArchivable: {t.get('isArchivable')}")

