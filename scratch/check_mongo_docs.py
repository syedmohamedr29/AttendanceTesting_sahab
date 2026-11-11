from pymongo import MongoClient
import bson
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

client = MongoClient('mongodb://10.1.0.4:27018/', serverSelectionTimeoutMS=5000)
db = client['Sahab']
col = db['ERP.Attendance.WorkTemplates']

company_uuid = bson.Binary.from_uuid(bson.uuid.UUID('3a249871-7a8d-dec5-2d72-47795dd2662d'))
loc1_uuid = bson.Binary.from_uuid(bson.uuid.UUID('3a24d629-0d56-a428-baa1-98493a77e614'))

doc_c9 = col.find_one({'_id': bson.Binary.from_uuid(bson.uuid.UUID('c9e00652-eae5-429a-bef0-4d4ddf9e0a0f'))})
doc_0b = col.find_one({'_id': bson.Binary.from_uuid(bson.uuid.UUID('0ba519c8-c2e2-4bce-8a70-23b1616ed5f7'))})

def format_doc(doc):
    if not doc:
        return "None"
    return {
        "_id": str(doc.get('_id').as_uuid()) if hasattr(doc.get('_id'), 'as_uuid') else str(doc.get('_id')),
        "ShortCode": doc.get('ShortCode'),
        "WorkTemplateName": doc.get('WorkTemplateName'),
        "TemplateType": doc.get('TemplateType'),
        "Version": doc.get('Version'),
        "IsDefault": doc.get('IsDefault'),
        "IsCompanyLinked": doc.get('IsCompanyLinked'),
        "CreatedAt": str(doc.get('CreatedAt')),
        "CreatedBy": str(doc.get('CreatedBy')),
        "ModifiedAt": str(doc.get('ModifiedAt')),
        "ModifiedBy": str(doc.get('ModifiedBy')),
        "TimeZoneId": doc.get('TimeZoneId'),
        "TotalWorkDurationInMinutes": doc.get('TotalWorkDurationInMinutes'),
        "TotalWorkingDays": doc.get('TotalWorkingDays'),
        "TotalDaysOff": doc.get('TotalDaysOff'),
        "FixedTimeSlots_count": len(doc.get('FixedTimeSlots', [])) if doc.get('FixedTimeSlots') else 0
    }

print("=== Doc c9e00652 (FXL0101) in Mongo ===")
print(json.dumps(format_doc(doc_c9), indent=2, ensure_ascii=False))

print("\n=== Doc 0ba519c8 (LOC0001) in Mongo ===")
print(json.dumps(format_doc(doc_0b), indent=2, ensure_ascii=False))
