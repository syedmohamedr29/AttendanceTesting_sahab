import sys
import json
import requests

sys.stdout.reconfigure(encoding='utf-8')

url = "https://attendance2.dev.zoolwork.com/swagger/v1/swagger.json"
resp = requests.get(url, timeout=10)
print(f"Swagger JSON Status: {resp.status_code}")
if resp.status_code == 200:
    swagger = resp.json()
    paths = swagger.get("paths", {})
    policy_paths = [p for p in paths.keys() if "policy" in p.lower() or "policies" in p.lower() or "break" in p.lower() or "grace" in p.lower() or "overtime" in p.lower()]
    print(f"Found {len(policy_paths)} policy-related paths:")
    for p in sorted(policy_paths):
        methods = list(paths[p].keys())
        print(f"  {p} -> {methods}")
        
    with open("scratch/attendance_swagger.json", "w", encoding="utf-8") as f:
        json.dump(swagger, f, indent=2)

