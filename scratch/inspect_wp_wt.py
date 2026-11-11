import sys, json, uuid
from pymongo import MongoClient

sys.stdout.reconfigure(encoding='utf-8')

client = MongoClient('mongodb://10.1.0.4:27018/')
db = client['Sahab']

sample = db['ERP.Attendance.WorkAssignments'].find_one()
wpid = sample.get('WorkPlanId')
wp = db['ERP.Attendance.WorkPlans'].find_one({"_id": wpid})
if wp:
    wt = wp.get('WorkTemplate')
    print("WorkPlan found:")
    print(f"  Plan Name: {wp.get('PlanName')}")
    if isinstance(wt, dict):
        wt_id = wt.get('_id')
        print(f"  WorkTemplate ID: {wt_id.as_uuid() if hasattr(wt_id, 'as_uuid') else wt_id}")
        print(f"  WorkTemplate Name: {wt.get('WorkTemplateName')}")
        print(f"  WorkTemplate Type: {wt.get('TemplateType')}")
        print(f"  WorkTemplate ShortCode: {wt.get('ShortCode')}")
    else:
        print(f"  WT: {wt}")
