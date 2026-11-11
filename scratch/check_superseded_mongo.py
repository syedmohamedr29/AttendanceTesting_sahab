import sys, json, uuid
from pymongo import MongoClient
from bson import Binary

sys.stdout.reconfigure(encoding='utf-8')

client = MongoClient('mongodb://10.1.0.4:27018/')
db = client['Sahab']

doc_id = Binary.from_uuid(uuid.UUID("25d0810f-e579-4670-bdc4-00082570c4fb"))
doc = db['ERP.Attendance.WorkTemplates'].find_one({"_id": doc_id})
print(f"Superseded CDWT after delete:")
print(f"  Version: {doc.get('Version')}")
print(f"  IsSuperseded: {doc.get('IsSuperseded')}")
print(f"  IsDefault: {doc.get('IsDefault')}")
print(f"  IsDeleted: {doc.get('IsDeleted')}")
print(f"  ModifiedAt: {doc.get('ModifiedAt')}")
print(f"  ModifiedBy: {doc.get('ModifiedBy')}")
