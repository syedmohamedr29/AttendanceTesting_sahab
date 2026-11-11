import requests
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

# 1. Fetch live swagger schema
sw_res = requests.get('https://attendance2.dev.zoolwork.com/swagger/v1/swagger.json')
if sw_res.status_code != 200:
    print(f"Error fetching Swagger: {sw_res.status_code}")
    sys.exit(1)

sw = sw_res.json()
schemas = sw.get('components', {}).get('schemas', {})

target_schemas = [
    ("POST Fixed", "FixedWorkTemplateDto"),
    ("POST Flexi", "FlexiWorkTemplateDto"),
    ("POST Split", "SplitWorkTemplateDto"),
    ("PATCH Fixed", "UpdateFixedWorkTemplateDto"),
    ("PATCH Flexi", "UpdateFlexiWorkTemplateDto"),
    ("PATCH Split", "UpdateSplitWorkTemplateDto")
]

print("=== SWAGGER DTO SCHEMAS AUDIT ===")
for label, s_name in target_schemas:
    s = schemas.get(s_name, {})
    props = list(s.get('properties', {}).keys())
    has_tenant_name = 'tenantName' in props
    has_tenant_id = 'tenantId' in props
    has_company_id = 'companyId' in props
    has_location_id = 'locationId' in props
    print(f"[{label}] Schema '{s_name}':")
    print(f"  tenantName present: {has_tenant_name}")
    print(f"  tenantId present: {has_tenant_id}")
    print(f"  companyId present: {has_company_id}")
    print(f"  locationId present: {has_location_id}")
    print(f"  All properties: {props}")
    print()

