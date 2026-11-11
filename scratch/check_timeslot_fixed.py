import requests
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

res = requests.get('https://attendance2.dev.zoolwork.com/swagger/v1/swagger.json')
if res.status_code == 200:
    sw = res.json()
    schemas = sw.get('components', {}).get('schemas', {})
    print("TimeSlotFixed schema:")
    print(json.dumps(schemas.get('TimeSlotFixed', {}), indent=2))

