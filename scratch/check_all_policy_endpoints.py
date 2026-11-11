import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open("scratch/all_swagger_endpoints_audit.json", encoding="utf-8") as f:
    endpoints = json.load(f)

print("=== SEARCHING ALL ENDPOINTS WITH 'att' OR 'polic' ===")
matches = [ep for ep in endpoints if "attpolic" in ep.get("path", "").lower() or "policy" in ep.get("path", "").lower()]
for ep in matches:
    print(f"{ep.get('method'):<6} {ep.get('path')}")

# Also check live Swagger JSON from attendance2
with open("scratch/current_token.json") as f:
    token = json.load(f)["access_token"]

# Let's inspect live swagger doc
import requests
try:
    r = requests.get("https://attendance2.dev.zoolwork.com/swagger/v1/swagger.json", headers={"Authorization": f"Bearer {token}"})
    if r.status_code == 200:
        swagger = r.json()
        print("\n=== LIVE SWAGGER ATTENDANCE POLICY PATHS ===")
        for path, methods in swagger.get("paths", {}).items():
            if "policy" in path.lower() or "policies" in path.lower():
                for m in methods:
                    print(f"{m.upper():<6} {path}")
except Exception as e:
    print("Error fetching live swagger:", e)

