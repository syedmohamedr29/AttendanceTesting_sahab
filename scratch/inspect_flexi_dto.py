import sys
import json
import urllib.request

sys.stdout.reconfigure(encoding='utf-8')

with urllib.request.urlopen('https://attendance2.dev.zoolwork.com/swagger/v1/swagger.json') as resp:
    swagger = json.loads(resp.read().decode('utf-8'))

schemas = swagger.get('components', {}).get('schemas', {})
flexi_dto = schemas.get('FlexiWorkTemplateDto', {})
print("FlexiWorkTemplateDto:", json.dumps(flexi_dto, indent=2))

