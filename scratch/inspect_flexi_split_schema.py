import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('scratch/attendance2_swagger_live.json', 'r', encoding='utf-8') as f:
    sw = json.load(f)

schemas = sw.get('components', {}).get('schemas', {})

print("=== FlexiWorkTemplateDto ===")
print(json.dumps(schemas.get('FlexiWorkTemplateDto', {}), indent=2))

print("=== SplitWorkTemplateDto ===")
print(json.dumps(schemas.get('SplitWorkTemplateDto', {}), indent=2))

