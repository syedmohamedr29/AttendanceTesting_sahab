import json
import requests
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open("scratch/current_token.json") as f:
    token = json.load(f)["access_token"]

cid = "3a249872-2d69-f931-41f6-d8db086b09b8"

headers = {
    "Authorization": f"Bearer {token}",
    "__tenant": "Attendance",
    "Accept": "application/json"
}

r = requests.get(f"https://company8.dev.zoolwork.com/api/company/workLocations/getAllWorkLocations?companyId={cid}", headers=headers)
print("Locations status:", r.status_code)
try:
    data = r.json()
    print("Locations count:", len(data) if isinstance(data, list) else data)
    print(json.dumps(data, indent=2, ensure_ascii=False))
except Exception as e:
    print("Locations text:", r.text)

