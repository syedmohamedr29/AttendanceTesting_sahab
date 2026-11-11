import json
import requests
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open("scratch/current_token.json") as f:
    token = json.load(f)["access_token"]

r = requests.get("https://attendance2.dev.zoolwork.com/swagger/v1/swagger.json", headers={"Authorization": f"Bearer {token}"})
swagger = r.json()
schemas = swagger.get("components", {}).get("schemas", {})

for name in ["OvertimeDayRate", "PolicyType", "PolicyState"]:
    if name in schemas:
        print(f"\n--- {name} ---")
        print(json.dumps(schemas[name], indent=2, ensure_ascii=False))

