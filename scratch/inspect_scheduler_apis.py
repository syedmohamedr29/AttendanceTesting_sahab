import json

with open('scratch/live_swagger_paths.json') as f:
    data = json.load(f)

paths = data.get('paths', {})
components = data.get('components', {}).get('schemas', {})

target_tags = [
    'Scheduler Overview',
    'Scheduler Schedules',
    'Roster Schedule (Planner)',
    'Roster Boards',
    'Shifts & Rotation Schedules',
    'Shifts & Rotation Overview'
]

for tag in target_tags:
    print(f"\n==================== {tag} ====================")
    for p, methods in sorted(paths.items()):
        for m, info in methods.items():
            if tag in info.get('tags', []):
                summary = info.get('summary', '')
                raw_params = info.get('parameters', [])
                param_strs = []
                for param in raw_params:
                    pname = param.get('name')
                    if pname != 'companyId':
                        req_str = 'required' if param.get('required') else 'optional'
                        param_strs.append(f"{pname} ({param.get('in')}, {req_str})")
                
                req_body = info.get('requestBody', {})
                content = req_body.get('content', {}).get('application/json', {}).get('schema', {})
                ref = content.get('$ref', '')
                schema_name = ref.split('/')[-1] if ref else ''
                
                schema_props = []
                if schema_name and schema_name in components:
                    schema_props = list(components[schema_name].get('properties', {}).keys())
                
                print(f"[{m.upper()}] {p}")
                print(f"  Summary : {summary}")
                if param_strs:
                    print(f"  Params  : {', '.join(param_strs)}")
                if schema_name:
                    print(f"  Payload : {schema_name} ({', '.join(schema_props)})")
