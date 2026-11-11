from pymongo import MongoClient
import bson
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

client = MongoClient('mongodb://10.1.0.4:27018/', serverSelectionTimeoutMS=5000)
db = client['Sahab']
col = db['ERP.Attendance.WorkTemplates']

doc_fxpos01 = col.find_one({'ShortCode': 'FXPOS01'})
if doc_fxpos01:
    res = {
        "_id": str(doc_fxpos01.get('_id').as_uuid()) if hasattr(doc_fxpos01.get('_id'), 'as_uuid') else str(doc_fxpos01.get('_id')),
        "_t": doc_fxpos01.get('_t'),
        "ShortCode": doc_fxpos01.get('ShortCode'),
        "WorkTemplateName": doc_fxpos01.get('WorkTemplateName'),
        "TemplateType": doc_fxpos01.get('TemplateType'),
        "Version": doc_fxpos01.get('Version'),
        "IsDefault": doc_fxpos01.get('IsDefault'),
        "IsCompanyLinked": doc_fxpos01.get('IsCompanyLinked'),
        "LocationId": str(doc_fxpos01.get('LocationId').as_uuid()) if hasattr(doc_fxpos01.get('LocationId'), 'as_uuid') else str(doc_fxpos01.get('LocationId')),
        "LocationName": doc_fxpos01.get('LocationName'),
        "CreatedAt": str(doc_fxpos01.get('CreatedAt')),
        "CreatedBy": str(doc_fxpos01.get('CreatedBy')),
        "TimeZoneId": doc_fxpos01.get('TimeZoneId'),
        "TotalWorkDurationInMinutes": doc_fxpos01.get('TotalWorkDurationInMinutes'),
        "TotalWorkingDays": doc_fxpos01.get('TotalWorkingDays'),
        "TotalDaysOff": doc_fxpos01.get('TotalDaysOff'),
        "FixedTimeSlots": doc_fxpos01.get('FixedTimeSlots')
    }
    print("=== FXPOS01 Mongo Document ===")
    print(json.dumps(res, indent=2, ensure_ascii=False))
else:
    print("FXPOS01 not found!")
