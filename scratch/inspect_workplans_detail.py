import sys, json, uuid
from pymongo import MongoClient
from bson import Binary

sys.stdout.reconfigure(encoding='utf-8')

client = MongoClient('mongodb://10.1.0.4:27018/')
db = client['Sahab']
company_uuid = Binary.from_uuid(uuid.UUID("3a249871-7a8d-dec5-2d72-47795dd2662d"))

work_plans = list(db['ERP.Attendance.WorkPlans'].find({"CompanyId": company_uuid}))
for i, wp in enumerate(work_plans):
    print(f"=== Work Plan {i+1} ({wp['_id'].as_uuid()}) ===")
    print(f"  PlanName: {wp.get('PlanName')}")
    print(f"  IsDefault: {wp.get('IsDefault')}")
    print(f"  LocationId: {wp.get('LocationId').as_uuid() if wp.get('LocationId') else None}")
    wt = wp.get('WorkTemplate')
    if isinstance(wt, dict):
        wt_id = wt.get('_id') or wt.get('Id')
        wt_id_str = wt_id.as_uuid() if hasattr(wt_id, 'as_uuid') else wt_id
        print(f"  Embedded WorkTemplate Id: {wt_id_str}")
        print(f"  Embedded WorkTemplate Name: {wt.get('WorkTemplateName')}")
        print(f"  Embedded WorkTemplate ShortCode: {wt.get('ShortCode')}")
    else:
        print(f"  WorkTemplate field: {wt}")
