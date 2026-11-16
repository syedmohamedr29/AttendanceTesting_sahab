import json

swagger_path = 'scratch/attendance2_swagger_live.json'
with open(swagger_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

paths = data.get('paths', {})
components = data.get('components', {}).get('schemas', {})

def resolve_ref(ref):
    if not ref:
        return {}
    name = ref.split('/')[-1]
    return components.get(name, {})

wa_paths = {p: v for p, v in paths.items() if 'workassignment' in p.lower()}

for p in sorted(wa_paths.keys()):
    for m, op in wa_paths[p].items():
        print(f"=== {m.upper()} {p} ===")
        summary = op.get('summary', '')
        op_id = op.get('operationId', '')
        print(f"Summary: {summary} | OpId: {op_id}")
        
        # params
        params = op.get('parameters', [])
        param_list = []
        for pr in params:
            name = pr.get('name')
            p_in = pr.get('in')
            req = pr.get('required')
            p_type = pr.get('schema', {}).get('type')
            p_format = pr.get('schema', {}).get('format')
            param_list.append(f"{name} (in:{p_in}, req:{req}, type:{p_type}{'/' + p_format if p_format else ''})")
        print("Params:", ", ".join(param_list))
        
        # requestBody
        rb = op.get('requestBody', {})
        content = rb.get('content', {}).get('application/json', {})
        schema_ref = content.get('schema', {}).get('$ref', '')
        if schema_ref:
            s_name = schema_ref.split('/')[-1]
            s_def = resolve_ref(schema_ref)
            props = list(s_def.get('properties', {}).keys())
            reqs = s_def.get('required', [])
            print(f"RequestBody DTO: {s_name} | Props: {props} | Required: {reqs}")
            for prop_name, prop_val in s_def.get('properties', {}).items():
                ref = prop_val.get('$ref', '')
                items_ref = prop_val.get('items', {}).get('$ref', '')
                t = prop_val.get('type')
                fmt = prop_val.get('format')
                print(f"   - {prop_name}: type={t}{'/' + fmt if fmt else ''} ref={ref or items_ref}")
        elif content.get('schema'):
            print("RequestBody Schema:", content.get('schema'))
        
        # responses
        resps = {}
        for r_code, r_val in op.get('responses', {}).items():
            r_schema_ref = r_val.get('content', {}).get('application/json', {}).get('schema', {}).get('$ref', '')
            resps[r_code] = r_schema_ref.split('/')[-1] if r_schema_ref else 'schema'
        print("Responses:", resps)
        print()
