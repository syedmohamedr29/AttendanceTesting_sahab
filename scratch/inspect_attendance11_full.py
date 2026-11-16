import pymongo
from bson import binary, json_util
import uuid

opts = json_util.JSONOptions(uuid_representation=binary.UuidRepresentation.STANDARD)

client = pymongo.MongoClient('mongodb://10.1.0.4:27018/', serverSelectionTimeoutMS=5000, uuidRepresentation='standard')

att11_id = uuid.UUID('3a24e5e5-302e-91bd-feaa-b07979766dfe')
print('=== Target Company: Attendance 11 ===')
print('CompanyId:', att11_id)

# 1. Inspect Employee collection
emp_db = client['EmployeeSvcNET8test']
emp_col = emp_db['Employee']

# Query by CompanyId
# Let's check count by CompanyId
emp_count = emp_col.count_documents({'BasicInformation.Company.CompanyId': att11_id})
print(f'\n1. EmployeeSvcNET8test.Employee count for Attendance 11: {emp_count}')

active_emps = []
inactive_emps = []
for emp in emp_col.find({'BasicInformation.Company.CompanyId': att11_id}):
    is_act = emp.get('IsActive', False)
    st = emp.get('EmployeeStatus')
    code = emp.get('EmployeeCode')
    name = emp.get('BasicInformation', {}).get('EmployeeNames', {}).get('en', {}).get('FullName')
    loc = emp.get('WorkInformation', {}).get('WorkLocation', {})
    doj = emp.get('WorkInformation', {}).get('DateOfJoining')
    item = {
        'id': str(emp['_id']),
        'code': code,
        'name': name,
        'isActive': is_act,
        'status': st,
        'location': loc.get('Names', {}).get('en', {}).get('Name') or str(loc.get('_id')),
        'locationId': str(loc.get('_id')),
        'doj': str(doj)
    }
    if is_act:
        active_emps.append(item)
    else:
        inactive_emps.append(item)

print(f'  Active Employees: {len(active_emps)}')
print(f'  Inactive / Other Employees: {len(inactive_emps)}')
print('\nActive Employees list:')
for e in active_emps:
    print(' ', e['code'], '|', e['name'], '| Loc:', e['location'], '| DOJ:', e['doj'], '| ID:', e['id'])

if inactive_emps:
    print('\nInactive Employees list:')
    for e in inactive_emps:
        print(' ', e['code'], '|', e['name'], '| Loc:', e['location'], '| Status:', e['status'], '| ID:', e['id'])

# 2. Inspect Sahab Database
sahab_db = client['Sahab']

# WorkTemplates
wt_col = sahab_db['ERP.Attendance.WorkTemplates']
wt_list = list(wt_col.find({'CompanyId': att11_id}))
print(f'\n2. ERP.Attendance.WorkTemplates count: {len(wt_list)}')
for wt in wt_list:
    w_id = wt.get('_id')
    w_name = wt.get('WorkTemplateName')
    w_type = wt.get('TemplateType')
    w_loc = wt.get('LocationId')
    w_code = wt.get('ShortCode')
    print(f'  WT: {w_id} | Name: {w_name} | Type: {w_type} | Loc: {w_loc} | Code: {w_code}')

# WorkPlans
wp_col = sahab_db['ERP.Attendance.WorkPlans']
wp_list = list(wp_col.find({'CompanyId': att11_id}))
print(f'\n3. ERP.Attendance.WorkPlans count: {len(wp_list)}')
for wp in wp_list:
    p_id = wp.get('_id')
    p_name = wp.get('WorkPlanName')
    p_type = wp.get('PlanType')
    p_loc = wp.get('LocationId')
    p_def = wp.get('IsDefault')
    p_del = wp.get('IsDeleted')
    p_inuse = wp.get('HasWorkAssignments')
    print(f'  WP: {p_id} | Name: {p_name} | Type: {p_type} | Loc: {p_loc} | Default: {p_def} | Deleted: {p_del} | InUse: {p_inuse}')

# Policies
pol_col = sahab_db['ERP.Attendance.Policies']
pol_list = list(pol_col.find({'CompanyId': att11_id}))
print(f'\n4. ERP.Attendance.Policies count: {len(pol_list)}')
for pol in pol_list:
    pol_id = pol.get('_id')
    pol_name = pol.get('Name')
    pol_type = pol.get('Type')
    pol_act = pol.get('IsActive')
    print(f'  Policy: {pol_id} | Name: {pol_name} | Type: {pol_type} | Active: {pol_act}')

# WorkAssignments
wa_col = sahab_db['ERP.Attendance.WorkAssignments']
wa_list = list(wa_col.find({'CompanyId': att11_id}))
print(f'\n5. ERP.Attendance.WorkAssignments count: {len(wa_list)}')
for wa in wa_list:
    hid = wa.get('_id')
    wp_n = wa.get('WorkPlanName')
    lid = wa.get('LocationId')
    s_dt = wa.get('StartDate')
    e_dt = wa.get('EndDate')
    print(f'  WA Header: {hid} | Plan: {wp_n} | Loc: {lid} | Dates: {s_dt} -> {e_dt}')

# WorkAssignmentMaps
wam_col = sahab_db['ERP.Attendance.WorkAssignmentMaps']
wam_list = list(wam_col.find({'CompanyId': att11_id}))
print(f'\n6. ERP.Attendance.WorkAssignmentMaps count: {len(wam_list)}')
for wam in wam_list:
    mid = wam.get('_id')
    ecode = wam.get('EmployeeCode')
    empid = wam.get('EmployeeId')
    wp_n = wam.get('WorkPlanData', {}).get('WorkPlanName')
    s_dt = wam.get('StartDate')
    e_dt = wam.get('EndDate')
    print(f'  WAM Map: {mid} | Emp: {ecode} ({empid}) | Plan: {wp_n} | Dates: {s_dt} -> {e_dt}')

# 7. Check Locations in CompanySvc
co_db = client['CompanySvcNET8test']
cm_col = co_db['CompaniesMaster']
comp_doc = cm_col.find_one({'_id': att11_id})
if not comp_doc:
    comp_doc = cm_col.find_one({'CompanyId': att11_id})

print('\n7. Company & Locations from CompanySvc:')
if comp_doc:
    print('Company Found:', comp_doc.get('_id'), comp_doc.get('CompanyName'))
    locs = comp_doc.get('Locations', [])
    print(f'Locations ({len(locs)}):')
    for l in locs:
        lid = l.get('LocationId') or l.get('_id')
        lname = l.get('LocationName')
        print(f'  Loc ID: {lid} | Name: {lname}')
else:
    distinct_locs = wp_col.distinct('LocationId', {'CompanyId': att11_id})
    print('Distinct LocationIds in WorkPlans:', distinct_locs)
