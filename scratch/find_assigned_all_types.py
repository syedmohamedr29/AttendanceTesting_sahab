import sys, json, uuid
from pymongo import MongoClient

sys.stdout.reconfigure(encoding='utf-8')

client = MongoClient('mongodb://10.1.0.4:27018/')
db = client['Sahab']

print("=== Scanning WorkAssignments for templates ===")
was = list(db['ERP.Attendance.WorkAssignments'].find({"IsActive": True}))
print(f"Total active assignments: {len(was)}")

assigned_templates = {}
for wa in was:
    wpid = wa.get('WorkPlanId')
    cid = wa.get('CompanyId')
    lid = wa.get('LocationId')
    wp = db['ERP.Attendance.WorkPlans'].find_one({"_id": wpid})
    if wp:
        wt = wp.get('WorkTemplate')
        if isinstance(wt, dict):
            wt_id = wt.get('_id')
            wt_id_str = str(wt_id.as_uuid() if hasattr(wt_id, 'as_uuid') else wt_id)
            tt = wt.get('TemplateType')
            sc = wt.get('ShortCode')
            c_str = str(cid.as_uuid() if hasattr(cid, 'as_uuid') else cid)
            l_str = str(lid.as_uuid() if hasattr(lid, 'as_uuid') else lid)
            assigned_templates[wt_id_str] = {
                "wt_id": wt_id_str,
                "company_id": c_str,
                "location_id": l_str,
                "template_type": tt,
                "short_code": sc,
                "plan_id": str(wpid.as_uuid() if hasattr(wpid, 'as_uuid') else wpid),
                "assignment_id": str(wa['_id'].as_uuid() if hasattr(wa['_id'], 'as_uuid') else wa['_id'])
            }

print(f"Unique assigned templates found: {len(assigned_templates)}")
for tid, info in assigned_templates.items():
    print(f"  Type {info['template_type']} ({info['short_code']}) | WT: {tid} | Company: {info['company_id']} | Plan: {info['plan_id']}")
