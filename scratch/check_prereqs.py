from pymongo import MongoClient
from bson import Binary

client = MongoClient('mongodb://10.1.0.4:27018/')
sahab = client['Sahab']
emp_db = client['EmployeeSvcNET8test']

company_id = '3a24e5e5-302e-91bd-feaa-b07979766dfe'

# Check ShiftRotationBoard
boards = list(sahab['ERP.Attendance.ShiftRotationBoard'].find())
matching_boards = [b for b in boards if company_id in str(b.get('CompanyId', ''))]
print(f"ShiftRotationBoards found for Attendance 11: {len(matching_boards)}")
for b in matching_boards:
    print(f"  Board ID: {b.get('_id')}, Name: {b.get('RotationName')}, Location: {b.get('LocationId')}, Plans: {len(b.get('Plans', []))}, Teams: {len(b.get('Teams', []))}, Members: {len(b.get('Members', []))}")

# Check WorkTemplates
templates = list(sahab['ERP.Attendance.WorkTemplates'].find({'IsDeleted': False}))
comp_templates = [t for t in templates if company_id in str(t.get('CompanyId', ''))]
print(f"WorkTemplates found for Attendance 11: {len(comp_templates)}")
for t in comp_templates:
    print(f"  Template ID: {t.get('_id')}, Code: {t.get('ShortCode')}, Type: {t.get('TemplateType')}, Name: {t.get('TemplateName', {}).get('en')}")

# Check Employees
emps = list(emp_db['Employees'].find())
comp_emps = [e for e in emps if company_id in str(e.get('CompanyId', ''))]
active_emps = [e for e in comp_emps if e.get('IsActive') is True]
print(f"Total employees for Attendance 11: {len(comp_emps)}, Active: {len(active_emps)}")
