import json

with open('scratch/attendance2_swagger_live.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

paths = data.get('paths', {})
rot_post = paths.get('/api/companies/{companyId}/worktemplates/rotation')
rot_patch = paths.get('/api/companies/{companyId}/worktemplates/rotation/{id}')

print("=== ROTATION POST ===")
print(json.dumps(rot_post, indent=2))

print("\n=== ROTATION PATCH ===")
print(json.dumps(rot_patch, indent=2))

# Find referenced schemas
schemas = data.get('components', {}).get('schemas', {})
for k in schemas:
    if 'rotation' in k.lower():
        print(f"\n=== SCHEMA: {k} ===")
        print(json.dumps(schemas[k], indent=2))
