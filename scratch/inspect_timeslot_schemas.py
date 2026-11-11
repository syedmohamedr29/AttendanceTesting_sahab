import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('scratch/attendance2_swagger_live.json', 'r', encoding='utf-8') as f:
    sw = json.load(f)

schemas = sw.get('components', {}).get('schemas', {})

print("=== TimeSlotFlexi ===")
print(json.dumps(schemas.get('TimeSlotFlexi', {}), indent=2))

print("=== TimeSlotSplit ===")
print(json.dumps(schemas.get('TimeSlotSplit', {}), indent=2))

print("=== FlexibleType ===")
print(json.dumps(schemas.get('FlexibleType', {}), indent=2))

