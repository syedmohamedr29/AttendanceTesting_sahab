import urllib.request
import json

req = urllib.request.Request('https://attendance2.dev.zoolwork.com/swagger/v1/swagger.json')
with urllib.request.urlopen(req) as resp:
    data = json.loads(resp.read().decode('utf-8'))

for path in data.get('paths', {}):
    if 'graceperiod' in path.lower() or 'split' in path.lower():
        for method in data['paths'][path]:
            op = data['paths'][path][method]
            print(f"Path: {path} | Method: {method} | tag: {op.get('tags')} | opId: {op.get('operationId')}")

