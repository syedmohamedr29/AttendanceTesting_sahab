import json

for fn in ['scratch/attendance2_swagger_live.json', 'scratch/attendance_swagger.json']:
    try:
        with open(fn, 'r', encoding='utf-8') as f:
            data = json.load(f)
        print(f"Loaded {fn}")
        paths = [p for p in data.get('paths', {}).keys() if 'rotation' in p.lower() or 'worktemplate' in p.lower()]
        print("Matching paths:", paths)
    except Exception as e:
        print(fn, e)
