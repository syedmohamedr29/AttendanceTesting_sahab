import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open("scratch/all_swagger_endpoints_audit.json", encoding="utf-8") as f:
    endpoints = json.load(f)

print("=== ALL POLICY ENDPOINTS IN SWAGGER ===")
policy_endpoints = [ep for ep in endpoints if "policy" in ep.get("path", "").lower() or "policies" in ep.get("path", "").lower()]
print(f"Total Policy Endpoints: {len(policy_endpoints)}")
for ep in policy_endpoints:
    print(f"{ep.get('method'):<6} {ep.get('path')} (Schema: {ep.get('schema')})")

