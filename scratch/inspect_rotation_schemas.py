import json

with open('scratch/attendance2_swagger_live.json', 'r', encoding='utf-8') as f:
    sw = json.load(f)

schemas = sw.get('components', {}).get('schemas', {})

target_routes = [
    ('/api/companies/{companyId}/shift-rotations', 'post'),
    ('/api/companies/{companyId}/shift-rotations', 'get'),
    ('/api/companies/{companyId}/shift-rotations/preview', 'post'),
    ('/api/companies/{companyId}/shift-rotations/{rotationId}', 'get'),
    ('/api/companies/{companyId}/shift-rotations/{rotationId}', 'patch'),
    ('/api/companies/{companyId}/shift-rotations/{rotationId}', 'delete'),
    ('/api/companies/{companyId}/shift-rotations/{rotationId}/rotation-grid', 'get'),
    ('/api/companies/{companyId}/shift-rotations/{rotationId}/teams/{teamId}/employees/check-conflicts', 'post'),
    ('/api/companies/{companyId}/shift-rotations/{rotationId}/teams/{teamId}/employees', 'post'),
    ('/api/companies/{companyId}/shift-rotations/{rotationId}/employees', 'get'),
    ('/api/companies/{companyId}/shift-rotations/{rotationId}/employees/{employeeId}/schedule', 'get'),
    ('/api/companies/{companyId}/shift-rotations/{rotationId}/generate-schedule', 'post'),
    ('/api/companies/{companyId}/shift-rotations/{rotationId}/members/{membershipId}', 'patch'),
    ('/api/companies/{companyId}/shift-rotations/{rotationId}/members/{membershipId}', 'delete'),
    ('/api/companies/{companyId}/shift-rotations/{rotationId}/members/{membershipId}/move/check-conflicts', 'post'),
    ('/api/companies/{companyId}/shift-rotations/{rotationId}/members/{membershipId}/move', 'patch'),
    ('/api/companies/{companyId}/shift-rotations/{rotationId}/members/{membershipId}/move-team', 'post'),
    ('/api/companies/{companyId}/worktemplates/rotation', 'post'),
    ('/api/companies/{companyId}/worktemplates/rotation/{id}', 'patch'),
]

for route, method in target_routes:
    op = sw['paths'].get(route, {}).get(method)
    if not op:
        print(f"NOT FOUND: {method.upper()} {route}")
        continue
    print(f"=== {method.upper()} {route} ===")
    print("  Summary:", op.get('summary', ''))
    params = op.get('parameters', [])
    for p in params:
        print(f"  Param: {p.get('name')} in {p.get('in')} (req: {p.get('required')}) type: {p.get('schema', {}).get('type')}")
    rb = op.get('requestBody', {})
    if rb:
        content = rb.get('content', {})
        for ctype, val in content.items():
            schema_ref = val.get('schema', {}).get('$ref') or val.get('schema', {}).get('type')
            print(f"  RequestBody [{ctype}]: {schema_ref}")
            if schema_ref and '#/components/schemas/' in str(schema_ref):
                sname = schema_ref.split('/')[-1]
                sdef = schemas.get(sname, {})
                props = list(sdef.get('properties', {}).keys())
                reqs = sdef.get('required', [])
                print(f"    Schema {sname} (req: {reqs}): {props}")
                for prop in props:
                    pdetails = sdef['properties'][prop]
                    ptype = pdetails.get('type') or pdetails.get('$ref') or pdetails.get('format')
                    print(f"      - {prop}: {ptype}")
