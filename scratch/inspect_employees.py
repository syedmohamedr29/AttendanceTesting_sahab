import sys, json, uuid
from pymongo import MongoClient
from bson import Binary

sys.stdout.reconfigure(encoding='utf-8')

client = MongoClient('mongodb://10.1.0.4:27018/')
db = client['Sahab']
company_uuid = Binary.from_uuid(uuid.UUID("3a249871-7a8d-dec5-2d72-47795dd2662d"))

print("=== EmployeeEnrollments in Attendance 8 ===")
enrollments = list(db['EmployeeEnrollments'].find({"CompanyId": company_uuid}))
print(f"Total enrollments in Attendance 8: {len(enrollments)}")
for e in enrollments[:5]:
    print(f"  Enrollment: {e.get('_id')} | EmpId: {e.get('EmployeeId')} | Name: {e.get('EmployeeName')}")
