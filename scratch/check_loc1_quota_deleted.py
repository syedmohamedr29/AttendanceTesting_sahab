import sys, json, uuid
from pymongo import MongoClient
from bson import Binary

sys.stdout.reconfigure(encoding='utf-8')

client = MongoClient('mongodb://10.1.0.4:27018/')
db = client['Sahab']
comp_id = Binary.from_uuid(uuid.UUID("3a249871-7a8d-dec5-2d72-47795dd2662d"))
loc1_id = Binary.from_uuid(uuid.UUID("3a24d629-0d56-a428-baa1-98493a77e614"))

total_loc1 = db['ERP.Attendance.WorkTemplates'].count_documents({"CompanyId": comp_id, "LocationId": loc1_id})
active_loc1 = db['ERP.Attendance.WorkTemplates'].count_documents({"CompanyId": comp_id, "LocationId": loc1_id, "IsDeleted": False})
deleted_loc1 = db['ERP.Attendance.WorkTemplates'].count_documents({"CompanyId": comp_id, "LocationId": loc1_id, "IsDeleted": True})

print(f"Location 1 Documents:")
print(f"  Total: {total_loc1}")
print(f"  Active (IsDeleted: false): {active_loc1}")
print(f"  Deleted (IsDeleted: true): {deleted_loc1}")
