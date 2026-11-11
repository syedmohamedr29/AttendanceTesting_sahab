import sys
import json

sys.stdout.reconfigure(encoding='utf-8')

with open("scratch/attendance_swagger.json", "r", encoding="utf-8") as f:
    swagger = json.load(f)

paths = swagger["paths"]
for endpoint in [
    "/api/companies/{companyId}/attpolicies/break",
    "/api/companies/{companyId}/attpolicies/graceperiod",
    "/api/companies/{companyId}/attpolicies/overtime"
]:
    print(f"\n==================== {endpoint} ====================")
    op = paths[endpoint]["post"]
    print("Summary:", op.get("summary"))
    print("Parameters:", json.dumps(op.get("parameters", []), indent=2))
    rb = op.get("requestBody", {})
    content = rb.get("content", {})
    schema_ref = content.get("application/json", {}).get("schema", {})
    print("Request Schema:", json.dumps(schema_ref, indent=2))
    
    # If $ref, look it up in components
    ref_name = schema_ref.get("$ref")
    if ref_name:
        key = ref_name.split("/")[-1]
        schema_def = swagger.get("components", {}).get("schemas", {}).get(key, {})
        print(f"Schema Definition for {key}:")
        print(json.dumps(schema_def, indent=2))
