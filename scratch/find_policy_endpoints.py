import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('scratch/all_swagger_endpoints_audit.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

print("=== POLICY ENDPOINTS IN SWAGGER ===")
policy_eps = [d for d in data if 'polic' in d['path'].lower()]
for p in policy_eps:
    print(f"{p['method']} {p['path']} (Schema: {p['schema']})")

if not policy_eps:
    print("No endpoint with 'polic' in path. Checking all paths...")
    # let's check all paths in swagger
    with open('scratch/attendance2_swagger_live.json', 'r', encoding='utf-8') as f2:
        sw = json.load(f2)
    for path in sw.get('paths', {}).keys():
        if any(w in path.lower() for w in ['grace', 'break', 'polic', 'config', 'att']):
            print("Match path:", path)

