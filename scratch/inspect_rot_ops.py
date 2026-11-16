import json

with open('scratch/attendance2_swagger_live.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

paths = data['paths']
rot_endpoints = [p for p in sorted(paths.keys()) if 'shift-rotations' in p or 'worktemplates/rotation' in p]

for p in rot_endpoints:
    for m in paths[p]:
        op = paths[p][m]
        params = [p.get('name') + ('*' if p.get('required') else '') + f"({p.get('in')})" for p in op.get('parameters', [])]
        body = op.get('requestBody', {}).get('content', {}).get('application/json', {}).get('schema', {})
        ref = body.get('$ref', '')
        body_type = ref.split('/')[-1] if ref else body.get('type', 'None')
        print(f"{m.upper():<6} {p}")
        print(f"       Params: {', '.join(params) if params else 'None'}")
        print(f"       Body: {body_type}")
