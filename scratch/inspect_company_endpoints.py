import requests
import json

r = requests.get('https://company8.dev.zoolwork.com/swagger/v1/swagger.json')
sw = r.json()

print("Company8 Swagger paths count:", len(sw.get("paths", {})))
company_paths = [p for p in sw.get("paths", {}).keys() if 'comp' in p.lower()]
print("Paths with 'comp':", company_paths[:20])

for p in company_paths:
    print(f"Path: {p} -> Methods: {list(sw['paths'][p].keys())}")

