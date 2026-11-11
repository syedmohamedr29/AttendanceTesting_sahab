import sys, json, uuid
from pymongo import MongoClient
from bson import Binary

sys.stdout.reconfigure(encoding='utf-8')

client = MongoClient('mongodb://10.1.0.4:27018/')
db = client['Sahab']
comp_id = Binary.from_uuid(uuid.UUID("3a23498e-e546-b040-2dda-43eb267a42a7"))

print("=== Assigned Templates in Company 3a23498e... ===")
was = list(db['ERP.Attendance.WorkAssignments'].find({"CompanyId": comp_id, "IsDeleted": False}))
print(f"Total active WorkAssignments: {len(was)}")
plan_ids = [wa.get('WorkPlanId') for wa in was if wa.get('WorkPlanId')]

for pid in plan_ids:
    wp = db['ERP.Attendance.WorkPlans'].find_one({"_id": pid})
    if wp:
        wt = wp.get('WorkTemplate')
        wt_id = wt.get('_id') if isinstance(wt, dict) else None
        wt_id_uuid = wt_id.as_uuid() if hasattr(wt_id, 'as_uuid') else wt_id
        wp_uuid = wp['_id'].as_uuid() if hasattr(wp['_id'], 'as_uuid') else wp['_id']
        print(f"  Plan: {wp_uuid} -> WT _id: {wt_id_uuid} | Code: {wt.get('ShortCode') if isinstance(wt, dict) else 'N/A'}")
