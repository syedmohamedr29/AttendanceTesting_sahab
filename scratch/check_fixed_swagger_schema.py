import requests
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

res = requests.get('https://attendance2.dev.zoolwork.com/swagger/v1/swagger.json')
if res.status_code == 200:
    sw = res.json()
    paths = sw.get('paths', {})
    for p in paths:
        if 'worktemplates/fixed' in p.lower():
            post_op = paths[p].get('post', {})
            print(f"Path: {p}")
            print(f"Parameters: {post_op.get('parameters', [])}")
            print(f"RequestBody: {json.dumps(post_op.get('requestBody', {}), indent=2)}")
            # Let's inspect the schema reference
            content = post_op.get('requestBody', {}).get('content', {}).get('application/json', {})
            schema_ref = content.get('schema', {}).get('$ref')
            print(f"Schema Ref: {schema_ref}")
            if schema_ref:
                schema_name = schema_ref.split('/')[-1]
                schema_obj = sw.get('components', {}).get('schemas', {}).get(schema_name, {})
                print(f"Schema {schema_name}:")
                print(json.dumps(schema_obj, indent=2))

