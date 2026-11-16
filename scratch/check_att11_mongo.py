import pymongo
from bson import binary, json_util
import uuid

client = pymongo.MongoClient('mongodb://10.1.0.4:27018/', serverSelectionTimeoutMS=5000, uuidRepresentation='standard')
att11_id = uuid.UUID('3a24e5e5-302e-91bd-feaa-b07979766dfe')

sahab = client['Sahab']
emp_db = client['EmployeeSvcNET8test']

# 1. Employees count
emp_col = emp_db['Employee']
emp_count = emp_col.count_documents({'BasicInformation.Company.CompanyId': att11_id})
active_count = emp_col.count_documents({'BasicInformation.Company.CompanyId': att11_id, 'IsActive': True})
print(f"Attendance 11 Employees in MongoDB: Total={emp_count}, Active={active_count}")

# 2. ShiftRotationBoards
rot_col = sahab['ERP.Attendance.ShiftRotationBoard']
rot_count = rot_col.count_documents({'CompanyId': att11_id})
print(f"Attendance 11 ShiftRotationBoards in MongoDB: {rot_count}")

# 3. WorkTemplates of type Rotation or Fixed
wt_col = sahab['ERP.Attendance.WorkTemplates']
wt_count = wt_col.count_documents({'CompanyId': att11_id, 'IsDeleted': False})
print(f"Attendance 11 WorkTemplates in MongoDB (IsDeleted: False): {wt_count}")
for t in wt_col.find({'CompanyId': att11_id, 'IsDeleted': False}):
    print(f"  ID: {t.get('_id')}, ShortCode: {t.get('ShortCode')}, Type: {t.get('TemplateType')}, Name: {t.get('TemplateName', {}).get('en')}")

# 4. WorkPlans in Sahab
wp_col = sahab['ERP.Attendance.WorkPlans']
wp_count = wp_col.count_documents({'CompanyId': att11_id, 'IsDeleted': False})
print(f"Attendance 11 WorkPlans in MongoDB (IsDeleted: False): {wp_count}")
for p in wp_col.find({'CompanyId': att11_id, 'IsDeleted': False}):
    print(f"  ID: {p.get('_id')}, Name: {p.get('WorkPlanName', {}).get('en')}, Location: {p.get('LocationId')}, TemplateId: {p.get('WorkTemplateId')}")
