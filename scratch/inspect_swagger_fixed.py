import sys
import json
import urllib.request

sys.stdout.reconfigure(encoding='utf-8')

with urllib.request.urlopen('https://attendance2.dev.zoolwork.com/swagger/v1/swagger.json') as resp:
    swagger = json.loads(resp.read().decode('utf-8'))

for path, methods in swagger.get('paths', {}).items():
    if path == '/api/companies/{companyId}/worktemplates/fixed':
        spec = methods.get('post', {})
        rb = spec.get('requestBody', {}).get('content', {}).get('application/json', {})
        ref = rb.get('schema', {}).get('$ref', '')
        print("Fixed DTO:", ref)
        def_name = ref.split('/')[-1]
        s_def = swagger.get('components', {}).get('schemas', {}).get(def_name, {})
        print("Properties:", list(s_def.get('properties', {}).keys()))
        slots_ref = s_def.get('properties', {}).get('fixedTimeSlots', {}).get('items', {}).get('$ref')
        if slots_ref:
            slot_def_name = slots_ref.split('/')[-1]
            slot_def = swagger.get('components', {}).get('schemas', {}).get(slot_def_name, {})
            print("Slot def:", slot_def)

