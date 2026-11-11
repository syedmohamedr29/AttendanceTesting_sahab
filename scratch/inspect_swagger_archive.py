import sys
import json
import urllib.request

sys.stdout.reconfigure(encoding='utf-8')

with urllib.request.urlopen('https://attendance2.dev.zoolwork.com/swagger/v1/swagger.json') as resp:
    swagger = json.loads(resp.read().decode('utf-8'))

for path, methods in swagger.get('paths', {}).items():
    if 'archive' in path.lower() or 'delete' in path.lower():
        print(f"Path: {path}")
        for m in methods:
            print(f"  Method: {m.upper()}")

