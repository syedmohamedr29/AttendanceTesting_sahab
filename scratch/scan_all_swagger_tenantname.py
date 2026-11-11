import requests
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

res = requests.get('https://attendance2.dev.zoolwork.com/swagger/v1/swagger.json')
if res.status_code != 200:
    print(f"Failed to fetch swagger: {res.status_code}")
    sys.exit(1)

sw = res.json()
paths = sw.get('paths', {})
schemas = sw.get('components', {}).get('schemas', {})

print(f"Total paths in Attendance 2 Swagger: {len(paths)}")
print(f"Total schemas in Attendance 2 Swagger: {len(schemas)}")

def find_props_in_schema(schema_obj, visited=None):
    if visited is None:
        visited = set()
    props = set()
    if not isinstance(schema_obj, dict):
        return props
    
    # Direct properties
    for p in schema_obj.get('properties', {}).keys():
        props.add(p)
        
    # AllOf
    for sub in schema_obj.get('allOf', []):
        ref = sub.get('$ref')
        if ref:
            s_name = ref.split('/')[-1]
            if s_name not in visited:
                visited.add(s_name)
                props.update(find_props_in_schema(schemas.get(s_name, {}), visited))
        else:
            props.update(find_props_in_schema(sub, visited))
            
    return props

endpoints_with_tenantname = []
all_post_patch_put_audit = []

for path, path_item in paths.items():
    for method in ['post', 'patch', 'put']:
        if method in path_item:
            op = path_item[method]
            op_id = op.get('operationId', f"{method.upper()} {path}")
            req_body = op.get('requestBody', {})
            content = req_body.get('content', {}).get('application/json', {})
            schema_info = content.get('schema', {})
            ref = schema_info.get('$ref')
            
            schema_name = ref.split('/')[-1] if ref else "None"
            props = set()
            if ref:
                props = find_props_in_schema(schemas.get(schema_name, {}))
            elif 'properties' in schema_info:
                props = set(schema_info['properties'].keys())
                
            has_tenant_name = 'tenantName' in props
            has_tenant_id = 'tenantId' in props
            has_company_id = 'companyId' in props
            has_location_id = 'locationId' in props
            has_short_code = 'shortCode' in props
            
            item = {
                "method": method.upper(),
                "path": path,
                "schema": schema_name,
                "has_tenantName": has_tenant_name,
                "has_tenantId": has_tenant_id,
                "has_companyId": has_company_id,
                "has_locationId": has_location_id,
                "has_shortCode": has_short_code,
                "all_props": sorted(list(props))
            }
            all_post_patch_put_audit.append(item)
            if has_tenant_name:
                endpoints_with_tenantname.append(item)

print(f"\n================================================================================")
print(f"AUDIT SUMMARY: {len(endpoints_with_tenantname)} ENDPOINTS STILL HAVE 'tenantName' IN BODY DTO!")
print(f"================================================================================")
for ep in endpoints_with_tenantname:
    print(f"\n* {ep['method']} {ep['path']}")
    print(f"  Schema: {ep['schema']}")
    print(f"  Properties: {ep['all_props']}")

# Also save full report to json
with open("scratch/all_swagger_endpoints_audit.json", "w", encoding='utf-8') as f:
    json.dump(all_post_patch_put_audit, f, indent=2, ensure_ascii=False)

