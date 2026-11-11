import json
import requests
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open("scratch/current_token.json") as f:
    token = json.load(f)["access_token"]

cid = "3a249872-2d69-f931-41f6-d8db086b09b8"
headers = {"Authorization": f"Bearer {token}"}

for q in ["", "?includeArchived=true", "?includeDeleted=true", "?status=All", "?status=Archived"]:
    r = requests.get(f"https://attendance2.dev.zoolwork.com/api/companies/{cid}/worktemplates{q}", headers=headers)
    print(f"GET /worktemplates{q}: {r.status_code}")
    if r.status_code == 200:
        data = r.json()
        items = data.get("templates", []) if isinstance(data, dict) else data
        print(f"Count: {len(items)}")
        for it in items:
            print(f"  ID: {it.get('id')}, Type: {it.get('templateType') or it.get('type')}, ShortCode: {it.get('shortCode')}, isDefault: {it.get('isDefault')}, status: {it.get('status')}")

