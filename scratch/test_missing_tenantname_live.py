import urllib.request, json, ssl, pymongo, uuid, sys
from bson.binary import Binary, UuidRepresentation

sys.stdout.reconfigure(encoding='utf-8')

with open('scratch/current_token.json', 'r') as f:
    token = json.load(f)['access_token']

base_url = "https://attendance2.dev.zoolwork.com"
company_id = "3a249870-c8ae-b3dc-1b8d-c44efad14f89"  # Attendance 7

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

# Clean payload omitting tenantName
test_name_en = f"Standard Overtime Policy Missing TenantName {uuid.uuid4().hex[:6]}"
payload = {
    "type": "Overtime",
    "name": {
        "en": test_name_en,
        "ar": "سياسة العمل الإضافي القياسية بدون اسم المستأجر"
    },
    "isActive": True,
    "overtimeRule": 2,  # use rule 2 to avoid duplicate rule 1
    "hasBufferBeforeOvertime": True,
    "bufferMinutes": 5,
    "rates": [
        {"dayRate": 1, "rateFormula": 1.5},
        {"dayRate": 2, "rateFormula": 1.5},
        {"dayRate": 3, "rateFormula": 1.5}
    ]
}

url = f"{base_url}/api/companies/{company_id}/attpolicies/overtime"
data_bytes = json.dumps(payload).encode('utf-8')
headers = {
    'Authorization': f'Bearer {token}',
    '__tenant': 'Attendance',
    'Content-Type': 'application/json',
    'Accept': 'application/json'
}
req = urllib.request.Request(url, data=data_bytes, headers=headers, method='POST')

try:
    with urllib.request.urlopen(req, context=ctx) as resp:
        print('HTTP Status:', resp.status)
        resp_body = resp.read().decode('utf-8')
        resp_json = json.loads(resp_body)
        print('API Response JSON:')
        print(json.dumps(resp_json, indent=2, ensure_ascii=False))
        created_id = resp_json.get('policy', {}).get('id') or resp_json.get('id')
        print('\nCreated Policy ID:', created_id)
except urllib.error.HTTPError as e:
    print('HTTPError:', e.code)
    print('Error Body:', e.read().decode('utf-8'))
    created_id = None

# If created, check MongoDB
if created_id:
    client = pymongo.MongoClient('mongodb://10.1.0.4:27018/?directConnection=true', serverSelectionTimeoutMS=5000)
    db = client['Sahab']
    col = db['ERP.Attendance.Policies']
    target_bin = Binary.from_uuid(uuid.UUID(created_id), UuidRepresentation.STANDARD)
    doc = col.find_one({'_id': target_bin})
    print('\n======================================================')
    print('DIRECT MONGODB DOCUMENT INSPECTION (Sahab.ERP.Attendance.Policies):')
    print('======================================================')
    print('Document _id:', created_id)
    print('TenantId in DB:', doc.get('TenantId'))
    print('TenantName in DB:', doc.get('TenantName'))
    print('TenantName type in DB:', type(doc.get('TenantName')))
    print('Is TenantName None?:', doc.get('TenantName') is None)
    print('Is TenantName Empty Dict?:', doc.get('TenantName') == {})
    print('CompanyName in DB:', doc.get('CompanyName'))
    print('Name in DB:', doc.get('Name'))
    print('\nFull Mongo Document:')
    print(json.dumps(doc, indent=2, default=str, ensure_ascii=False))
