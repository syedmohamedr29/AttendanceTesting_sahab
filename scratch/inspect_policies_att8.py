import sys, json, uuid
from pymongo import MongoClient
from bson import Binary

sys.stdout.reconfigure(encoding='utf-8')

client = MongoClient('mongodb://10.1.0.4:27018/')
db = client['Sahab']
comp_id = Binary.from_uuid(uuid.UUID("3a249871-7a8d-dec5-2d72-47795dd2662d"))

policies = list(db['ERP.Attendance.AttendancePolicies'].find({"CompanyId": comp_id}))
print(f"Total policies for Attendance 8: {len(policies)}")
for p in policies[:5]:
    pid = p['_id'].as_uuid() if hasattr(p['_id'], 'as_uuid') else p['_id']
    ptype = p.get('PolicyType')
    print(f"  Policy: {pid} | Type: {ptype} | Name: {p.get('PolicyName')}")
