import requests
import json

r = requests.get('https://attendance2.dev.zoolwork.com/swagger/v1/swagger.json')
sw = r.json()
schemas = sw.get('components', {}).get('schemas', {})

sub_schemas = ['FixedTimeSlotDto', 'FlexiTimeSlotDto', 'SplitTimeSlotDto', 'SplitIntervalDto', 'WorkTemplateNameDto']

for s in sub_schemas:
    if s in schemas:
        print(f"\n--- {s} ---")
        for p, v in schemas[s].get('properties', {}).items():
            print(f"  {p}: {v}")
    else:
        # Search for similar names
        matches = [k for k in schemas.keys() if s.lower() in k.lower()]
        print(f"Schema {s} not found directly, matches: {matches}")
        for m in matches:
            print(f"  --- {m} ---")
            for p, v in schemas[m].get('properties', {}).items():
                print(f"    {p}: {v.get('type')}, ref={v.get('$ref')}")

