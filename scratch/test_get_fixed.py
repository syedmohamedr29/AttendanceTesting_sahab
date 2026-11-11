import json
import requests
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open("scratch/current_token.json") as f:
    token = json.load(f)["access_token"]

cid = "3a249872-2d69-f931-41f6-d8db086b09b8"
v1_id = "9892844a-d055-420b-b6cf-877cd1a9c703"

headers = {
    "Authorization": f"Bearer {token}",
    "Content-Type": "application/json"
}

r = requests.get(f"https://attendance2.dev.zoolwork.com/api/companies/{cid}/worktemplates/{v1_id}", headers=headers)
print("GET by ID Status:", r.status_code)
print("GET by ID Response:", r.text[:300])

