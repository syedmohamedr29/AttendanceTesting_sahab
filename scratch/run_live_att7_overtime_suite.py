import urllib.request
import urllib.error
import json
import ssl
import sys
import uuid
import pymongo

sys.stdout.reconfigure(encoding='utf-8')

company_id = "3a249870-c8ae-b3dc-1b8d-c44efad14f89"
base_url = f"https://attendance2.dev.zoolwork.com/api/companies/{company_id}/attpolicies"

with open("scratch/current_token.json", "r") as f:
    token = json.load(f)["access_token"]

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

mongo_client = pymongo.MongoClient('mongodb://10.1.0.4:27018/', uuidRepresentation='standard', serverSelectionTimeoutMS=5000)
mongo_col = mongo_client['Sahab']['ERP.Attendance.Policies']

def call_api(method, endpoint, payload=None):
    url = f"{base_url}{endpoint}" if endpoint.startswith("/") else f"{base_url}/{endpoint}"
    data = json.dumps(payload).encode('utf-8') if payload is not None else None
    headers = {
        'Authorization': f'Bearer {token}',
        '__tenant': 'Attendance',
        'Accept': 'application/json',
        'Content-Type': 'application/json'
    }
    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, context=ctx, timeout=15) as resp:
            body = resp.read().decode('utf-8')
            try:
                parsed = json.loads(body)
            except:
                parsed = body
            return resp.status, parsed
    except urllib.error.HTTPError as e:
        err_body = e.read().decode('utf-8')
        try:
            parsed = json.loads(err_body)
        except:
            parsed = err_body
        return e.code, parsed
    except Exception as e:
        return 999, str(e)

print("=== STARTING ATTENDANCE 7 LIVE OVERTIME POLICY TEST SUITE ===")

# Test 1: POST-P01 Standard policy
p01_payload = {
    "type": "Overtime",
    "name": {"en": "Standard Overtime Policy", "ar": "سياسة العمل الإضافي القياسية"},
    "isActive": True,
    "tenantName": {"en": "Attendance", "ar": "Attendance"},
    "overtimeRule": 1,
    "hasBufferBeforeOvertime": True,
    "bufferMinutes": 5,
    "rates": [
        {"dayRate": 1, "rateFormula": 1.5},
        {"dayRate": 2, "rateFormula": 1.5},
        {"dayRate": 3, "rateFormula": 1.5}
    ]
}
status, resp = call_api("POST", "/overtime", p01_payload)
print(f"POST-P01 (Standard): HTTP {status} | Resp: {resp}")

created_id = None
if isinstance(resp, dict) and "id" in resp:
    created_id = resp["id"]
elif isinstance(resp, dict) and "policy" in resp and "id" in resp["policy"]:
    created_id = resp["policy"]["id"]

print(f"Created Policy ID: {created_id}")

# Check MongoDB for created policy
if created_id:
    doc = mongo_col.find_one({"_id": uuid.UUID(created_id)})
    if doc:
        print(f"MongoDB doc found: Type={doc.get('Type')}, OvertimeRule={doc.get('OvertimeRule')}, Rates count={len(doc.get('Rates', []))}")
        print(f"MongoDB TenantName: {doc.get('TenantName')}")
        print(f"MongoDB CompanyName: {doc.get('CompanyName')}")
    else:
        print("MongoDB doc NOT found!")

# Let's clean up any test policies before running the full batch
