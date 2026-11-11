import requests
import json

r = requests.get('https://attendance2.dev.zoolwork.com/swagger/v1/swagger.json')
sw = r.json()
schemas = sw.get('components', {}).get('schemas', {})

print("Total schemas:", len(schemas))
wt_schemas = [k for k in schemas.keys() if 'template' in k.lower() or 'slot' in k.lower() or 'time' in k.lower() or 'fixed' in k.lower() or 'flexi' in k.lower() or 'split' in k.lower()]
print("Matching schemas:", wt_schemas)

for s in wt_schemas:
    print(f"\n--- {s} ---")
    props = schemas[s].get('properties', {})
    for p, v in props.items():
        print(f"  {p}: {v.get('type')}, ref={v.get('$ref')}")

