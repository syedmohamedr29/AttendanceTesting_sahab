import json
import requests
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open("scratch/current_token.json") as f:
    token = json.load(f)["access_token"]

cid = "3a249872-2d69-f931-41f6-d8db086b09b8"
headers = {"Authorization": f"Bearer {token}"}

r = requests.get(f"https://attendance2.dev.zoolwork.com/api/companies/{cid}/worktemplates", headers=headers)
print("Status:", r.status_code)
print("Response:", r.text)

