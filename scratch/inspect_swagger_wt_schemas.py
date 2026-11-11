import requests
import json

r = requests.get('https://attendance2.dev.zoolwork.com/swagger/v1/swagger.json')
sw = r.json()

endpoints = [
    '/api/companies/{companyId}/worktemplates/fixed',
    '/api/companies/{companyId}/worktemplates/flexi',
    '/api/companies/{companyId}/worktemplates/split'
]

for ep in endpoints:
    print(f"\n==================== {ep} ====================")
    ep_data = sw.get('paths', {}).get(ep, {}).get('post', {})
    print("Summary:", ep_data.get('summary'))
    print("Parameters:")
    for p in ep_data.get('parameters', []):
        print(f"  {p.get('name')} in {p.get('in')} (required: {p.get('required')})")
    
    # Request body
    req_body = ep_data.get('requestBody', {})
    content = req_body.get('content', {}).get('application/json', {})
    schema_ref = content.get('schema', {}).get('$ref')
    print("Request schema ref:", schema_ref)
    
    if schema_ref:
        schema_name = schema_ref.split('/')[-1]
        schema_def = sw.get('components', {}).get('schemas', {}).get(schema_name, {})
        print(f"Schema {schema_name} properties:")
        for prop, val in schema_def.get('properties', {}).items():
            print(f"  - {prop}: type={val.get('type')}, format={val.get('format')}, ref={val.get('$ref')}")

