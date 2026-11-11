import sys
import json
import urllib.request

sys.stdout.reconfigure(encoding='utf-8')

with urllib.request.urlopen('https://attendance2.dev.zoolwork.com/swagger/v1/swagger.json') as resp:
    swagger = json.loads(resp.read().decode('utf-8'))

for path, methods in swagger.get('paths', {}).items():
    if 'short-code' in path.lower():
        print(f"Path: {path}")
        for m, spec in methods.items():
            print(f"  Method: {m.upper()}")
            for p in spec.get('parameters', []):
                print(f"    Param: {p.get('name')} in {p.get('in')} (type: {p.get('schema', {}).get('type')})")

