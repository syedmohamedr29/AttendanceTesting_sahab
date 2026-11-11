import sys
import json
import urllib.request

sys.stdout.reconfigure(encoding='utf-8')

# fetch swagger doc
try:
    with urllib.request.urlopen('https://attendance2.dev.zoolwork.com/swagger/v1/swagger.json') as resp:
        swagger = json.loads(resp.read().decode('utf-8'))
        
    for path, methods in swagger.get('paths', {}).items():
        if 'flexi' in path.lower():
            for m, spec in methods.items():
                print(f"{m.upper()} {path}:")
                rb = spec.get('requestBody', {})
                content = rb.get('content', {}).get('application/json', {})
                schema = content.get('schema', {})
                ref = schema.get('$ref', '')
                print(f"  Schema ref: {ref}")
                if ref:
                    def_name = ref.split('/')[-1]
                    s_def = swagger.get('components', {}).get('schemas', {}).get(def_name, {})
                    print(f"  Properties: {list(s_def.get('properties', {}).keys())}")
                    # check flexiTimeSlots item schema
                    slots_ref = s_def.get('properties', {}).get('flexiTimeSlots', {}).get('items', {}).get('$ref')
                    if slots_ref:
                        slot_def_name = slots_ref.split('/')[-1]
                        slot_def = swagger.get('components', {}).get('schemas', {}).get(slot_def_name, {})
                        print(f"  Slot properties: {list(slot_def.get('properties', {}).keys())}")
                        print(f"  Slot schema: {slot_def}")
except Exception as e:
    print(f"Error: {e}")

