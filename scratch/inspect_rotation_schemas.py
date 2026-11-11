import json

with open('scratch/attendance2_swagger_live.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

schemas = data.get('components', {}).get('schemas', {})

for name in ['RotationWorkTemplateDto', 'UpdateRotationWorkTemplateDto', 'TimeSlotRotation', 'Day', 'RecurrenceOfMonth', 'WorkTemplateType']:
    if name in schemas:
        print(f"\n=== SCHEMA: {name} ===")
        print(json.dumps(schemas[name], indent=2))
    else:
        print(f"Schema {name} not found")
