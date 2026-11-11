import sys, pymongo, uuid, json
from bson.binary import Binary, UuidRepresentation

sys.stdout.reconfigure(encoding='utf-8')

client = pymongo.MongoClient('mongodb://10.1.0.4:27018/?directConnection=true', serverSelectionTimeoutMS=5000)
db = client['Sahab']
col = db['ERP.Attendance.Policies']

target_id = '5c7e8a2d-3916-4277-b4c6-e3b744af6c1e'
bin_id = Binary.from_uuid(uuid.UUID(target_id), UuidRepresentation.STANDARD)
doc = col.find_one({'_id': bin_id})
if doc:
    print('=== Found duplicatePolicyId document 5c7e8a2d-3916-4277-b4c6-e3b744af6c1e ===')
    print(json.dumps(doc, indent=2, default=str, ensure_ascii=False))
else:
    print('Policy 5c7e8a2d not found directly!')

comp_id = '3a249871-7a8d-dec5-2d72-47795dd2662d'
comp_bin = Binary.from_uuid(uuid.UUID(comp_id), UuidRepresentation.STANDARD)
docs = list(col.find({'CompanyId': comp_bin}))
print(f'\nTotal policies for Attendance 8: {len(docs)}')
for d in docs:
    print(f"Doc {d.get('_id')}: Name={d.get('Name')}, Type={d.get('Type')}, Rule={d.get('OvertimeRule')}, Rates={d.get('Rates')}")
