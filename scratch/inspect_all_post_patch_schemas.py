import requests
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

res = requests.get('https://attendance2.dev.zoolwork.com/swagger/v1/swagger.json')
if res.status_code == 200:
    sw = res.json()
    paths = sw.get('paths', {})
    schemas = sw.get('components', {}).get('schemas', {})
    
    target_endpoints = [
        ('POST', '/api/companies/{companyId}/worktemplates/fixed'),
        ('POST', '/api/companies/{companyId}/worktemplates/flexi'),
        ('POST', '/api/companies/{companyId}/worktemplates/split'),
        ('PATCH', '/api/companies/{companyId}/worktemplates/fixed/{id}'),
        ('PATCH', '/api/companies/{companyId}/worktemplates/flexi/{id}'),
        ('PATCH', '/api/companies/{companyId}/worktemplates/split/{id}')
    ]
    
    print("=== SWAGGER SCHEMA INSPECTION FOR POST & PATCH ===")
    for method, path in target_endpoints:
        path_obj = paths.get(path, {})
        op_obj = path_obj.get(method.lower(), {})
        print(f"\n--- {method} {path} ---")
        if not op_obj:
            print("  [NOT FOUND IN SWAGGER!]")
            continue
            
        req_body = op_obj.get('requestBody', {})
        content = req_body.get('content', {}).get('application/json', {})
        schema_info = content.get('schema', {})
        ref = schema_info.get('$ref')
        
        schema_name = ref.split('/')[-1] if ref else "Inline/None"
        print(f"  Schema: {schema_name}")
        
        if ref:
            s_obj = schemas.get(schema_name, {})
            props = list(s_obj.get('properties', {}).keys())
            print(f"  Properties ({len(props)}): {props}")
            
            scoping_fields = [p for p in props if p.lower() in ['tenantid', 'tenantname', 'companyid', 'companyname', 'locationid', 'locationname', 'id']]
            print(f"  Scoping/Audit fields in body: {scoping_fields}")
else:
    print('Failed to get Swagger:', res.status_code)

