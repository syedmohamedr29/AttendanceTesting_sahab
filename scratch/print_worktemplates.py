import requests
import json

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
print("Response type:", type(r.json()))
print("Response content:", json.dumps(r.json(), indent=2))

