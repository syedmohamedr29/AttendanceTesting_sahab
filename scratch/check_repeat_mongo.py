import sys, json, uuid
from pymongo import MongoClient
from bson import Binary

sys.stdout.reconfigure(encoding='utf-8')

client = MongoClient('mongodb://10.1.0.4:27018/')
db = client['Sahab']

doc_id = Binary.from_uuid(uuid.UUID("cf3ef115-b548-436b-afd1-568be4f5ebfa"))
doc = db['ERP.Attendance.WorkTemplates'].find_one({"_id": doc_id})
print(f"MongoDB after repeat delete:")
print(f"  IsDeleted: {doc.get('IsDeleted')}")
print(f"  ModifiedAt: {doc.get('ModifiedAt')}")
print(f"  ModifiedBy: {doc.get('ModifiedBy')}")
print(f"  ChangeLog: {doc.get('ChangeLog')}")
