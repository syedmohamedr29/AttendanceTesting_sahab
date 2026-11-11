import json
import requests

with open("scratch/current_token.json") as f:
    token = json.load(f)["access_token"]

cid = "3a249872-2d69-f931-41f6-d8db086b09b8"
headers = {
    "Authorization": f"Bearer {token}",
    "__tenant": "Attendance",
    "Accept": "application/json"
}

r = requests.get(f"https://company8.dev.zoolwork.com/api/company/companies/{cid}/getChecklist", headers=headers)
print("Checklist status:", r.status_code)
print(json.dumps(r.json(), indent=2))
