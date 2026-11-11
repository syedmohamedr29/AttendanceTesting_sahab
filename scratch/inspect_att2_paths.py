import requests
import json

r = requests.get('https://attendance2.dev.zoolwork.com/swagger/v1/swagger.json')
sw = r.json()

wt_paths = [p for p in sw.get('paths', {}).keys() if 'worktemplate' in p.lower() or 'fixed' in p.lower() or 'flexi' in p.lower()]
print("Matching paths count:", len(wt_paths))
for p in wt_paths:
    print(f"Path: {p} -> Methods: {list(sw['paths'][p].keys())}")

