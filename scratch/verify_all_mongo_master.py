from pymongo import MongoClient
import bson
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

client = MongoClient('mongodb://10.1.0.4:27018/', serverSelectionTimeoutMS=5000)
db = client['Sahab']
col = db['ERP.Attendance.WorkTemplates']

company_uuid = bson.Binary.from_uuid(bson.uuid.UUID('3a249871-7a8d-dec5-2d72-47795dd2662d'))
loc2_uuid = bson.Binary.from_uuid(bson.uuid.UUID('3a24d646-b3cf-b1d4-61bb-1adf094b52fc'))

# Query all templates in Location 2
cursor = col.find({"CompanyId": company_uuid, "LocationId": loc2_uuid})
docs = list(cursor)

print(f"Total documents found in MongoDB for Location 2: {len(docs)}")
summary = []
for d in docs:
    s = {
        "_id": str(d.get('_id').as_uuid()) if hasattr(d.get('_id'), 'as_uuid') else str(d.get('_id')),
        "ShortCode": d.get('ShortCode'),
        "TemplateType": d.get('TemplateType'),
        "_t": d.get('_t'),
        "WorkTemplateName": d.get('WorkTemplateName'),
        "Version": d.get('Version'),
        "IsDefault": d.get('IsDefault'),
        "IsCompanyLinked": d.get('IsCompanyLinked'),
        "TotalWorkDurationInMinutes": d.get('TotalWorkDurationInMinutes'),
        "CreatedAt": str(d.get('CreatedAt')),
        "ModifiedAt": str(d.get('ModifiedAt'))
    }
    summary.append(s)
    print(f"ID: {s['_id']} | Code: {s['ShortCode']} | Type: {s['TemplateType']} | _t: {s['_t']} | Version: {s['Version']} | Dur: {s['TotalWorkDurationInMinutes']} | Name: {s['WorkTemplateName'].get('en')}")

with open('scratch/loc2_mongo_verified_docs.json', 'w', encoding='utf-8') as f:
    json.dump(summary, f, indent=2, ensure_ascii=False)
print("Saved loc2_mongo_verified_docs.json")
