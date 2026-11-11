import sys, json, uuid
from pymongo import MongoClient
from bson import Binary

sys.stdout.reconfigure(encoding='utf-8')

client = MongoClient('mongodb://10.1.0.4:27018/')
db = client['Sahab']
company_uuid = Binary.from_uuid(uuid.UUID("3a249871-7a8d-dec5-2d72-47795dd2662d"))

templates = list(db['ERP.Attendance.WorkTemplates'].find({"CompanyId": company_uuid}))
for t in templates:
    lid = t.get('LocationId')
    lid_uuid = lid.as_uuid() if hasattr(lid, 'as_uuid') else lid
    if str(lid_uuid) == "00000000-0000-0000-0000-000000000000":
        print(f"ID: {t['_id'].as_uuid()} | Version: {t.get('Version')} | IsDefault: {t.get('IsDefault')} | IsSuperseded: {t.get('IsSuperseded')} | IsDeleted: {t.get('IsDeleted')} | Name: {t.get('WorkTemplateName')}")
