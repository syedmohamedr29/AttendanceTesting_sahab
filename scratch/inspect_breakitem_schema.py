import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('scratch/attendance2_swagger_live.json', 'r', encoding='utf-8') as f:
    sw = json.load(f)

schemas = sw.get('components', {}).get('schemas', {})

print("=== BreakItem ===")
print(json.dumps(schemas.get('BreakItem', {}), indent=2))

