import sys
import json

sys.stdout.reconfigure(encoding='utf-8')

with open("scratch/attendance_swagger.json", "r", encoding="utf-8") as f:
    swagger = json.load(f)

paths = swagger["paths"]
for endpoint in [
    "/api/companies/{companyId}/attpolicies/break/{policyId}",
    "/api/companies/{companyId}/attpolicies/graceperiod/{policyId}",
    "/api/companies/{companyId}/attpolicies/overtime/{policyId}",
    "/api/companies/{companyId}/attpolicies/{policyId}/delete"
]:
    print(f"\n==================== {endpoint} ====================")
    op = paths[endpoint]["patch"]
    print("Summary:", op.get("summary"))
    print("Parameters:", json.dumps(op.get("parameters", []), indent=2))
    rb = op.get("requestBody", {})
    content = rb.get("content", {})
    schema_ref = content.get("application/json", {}).get("schema", {})
    print("Request Schema:", json.dumps(schema_ref, indent=2))

