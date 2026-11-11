import requests
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

res = requests.get('https://attendance2.dev.zoolwork.com/swagger/v1/swagger.json').json()
schemas = res.get('components', {}).get('schemas', {})
print("BreakPolicyDto:")
print(json.dumps(schemas.get("BreakPolicyDto", {}), indent=2))
print("\nBreakItem:")
print(json.dumps(schemas.get("BreakItem", {}), indent=2))

