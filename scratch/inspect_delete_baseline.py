import sys, json, uuid
from pymongo import MongoClient
from bson import Binary

sys.stdout.reconfigure(encoding='utf-8')

client = MongoClient('mongodb://10.1.0.4:27018/')
db = client['Sahab']

company_uuid = Binary.from_uuid(uuid.UUID("3a249871-7a8d-dec5-2d72-47795dd2662d"))

print("=== 1. Work Templates for Company Attendance 8 ===")
templates = list(db['ERP.Attendance.WorkTemplates'].find({"CompanyId": company_uuid}))
print(f"Total Work Templates found: {len(templates)}")

cdwt = [t for t in templates if t.get('IsDefault') and not t.get('LocationId')]
print(f"CDWT templates: {len(cdwt)}")
for t in cdwt:
    print(f"  _id: {t['_id'].as_uuid()} | Version: {t.get('Version')} | IsSuperseded: {t.get('IsSuperseded')} | IsDeleted: {t.get('IsDeleted')} | Type: {t.get('TemplateType')} | Code: {t.get('ShortCode')}")

loc_templates = [t for t in templates if t.get('LocationId')]
print(f"Location templates: {len(loc_templates)}")
loc_groups = {}
for t in loc_templates:
    loc_id = str(t['LocationId'].as_uuid())
    loc_groups.setdefault(loc_id, []).append(t)

for loc_id, t_list in loc_groups.items():
    print(f"  Location {loc_id}: {len(t_list)} templates")
    for t in t_list[:8]:
        print(f"    _id: {t['_id'].as_uuid()} | Code: {t.get('ShortCode')} | Type: {t.get('TemplateType')} | IsDefault: {t.get('IsDefault')} | IsDeleted: {t.get('IsDeleted')}")

print("\n=== 2. Work Plans for Company Attendance 8 ===")
work_plans = list(db['ERP.Attendance.WorkPlans'].find({"CompanyId": company_uuid}))
print(f"Total Work Plans: {len(work_plans)}")
for wp in work_plans:
    wt_ref = wp.get('WorkTemplateId') or (wp.get('WorkTemplate', {}).get('Id') if isinstance(wp.get('WorkTemplate'), dict) else None)
    loc_id = wp.get('LocationId').as_uuid() if wp.get('LocationId') else None
    print(f"  WP _id: {wp['_id'].as_uuid()} | Loc: {loc_id} | IsDefault: {wp.get('IsDefault')} | IsDeleted: {wp.get('IsDeleted')} | WTRef: {wt_ref}")

print("\n=== 3. Work Assignments for Company Attendance 8 ===")
work_assignments = list(db['ERP.Attendance.WorkAssignments'].find({"CompanyId": company_uuid}))
print(f"Total Work Assignments: {len(work_assignments)}")
for wa in work_assignments:
    pid = wa.get('WorkPlanId').as_uuid() if hasattr(wa.get('WorkPlanId'), 'as_uuid') else wa.get('WorkPlanId')
    print(f"  WA _id: {wa['_id'].as_uuid()} | PlanId: {pid} | IsDeleted: {wa.get('IsDeleted')}")

print("\n=== 4. Work Assignment Maps for Company Attendance 8 ===")
maps = list(db['ERP.Attendance.WorkAssignmentMaps'].find({"CompanyId": company_uuid}))
print(f"Total Work Assignment Maps: {len(maps)}")
for m in maps:
    emp_id = m.get('EmployeeId').as_uuid() if hasattr(m.get('EmployeeId'), 'as_uuid') else m.get('EmployeeId')
    wa_id = m.get('WorkAssignmentId').as_uuid() if hasattr(m.get('WorkAssignmentId'), 'as_uuid') else m.get('WorkAssignmentId')
    print(f"  Map _id: {m['_id'].as_uuid()} | EmpId: {emp_id} | WAId: {wa_id}")
