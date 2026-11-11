import requests
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

res = requests.get('https://company8.dev.zoolwork.com/swagger/v1/swagger.json')
if res.status_code == 200:
    sw = res.json()
    paths = sw.get('paths', {})
    print(f'Total paths in Company8: {len(paths)}')
    for p in paths:
        if 'compan' in p.lower() or 'check' in p.lower() or 'location' in p.lower():
            methods = list(paths[p].keys())
            print(f"{p} -> {methods}")
else:
    print('Failed to get swagger:', res.status_code)

