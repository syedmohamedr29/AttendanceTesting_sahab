import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('scratch/all_swagger_endpoints_audit.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

wt_endpoints = [d for d in data if 'worktemplate' in d['path'].lower()]
print(f"Total worktemplate POST/PATCH/PUT endpoints: {len(wt_endpoints)}")
for d in wt_endpoints:
    print(f"{d['method']} {d['path']}: has_tenantName={d['has_tenantName']}, schema={d['schema']}")

