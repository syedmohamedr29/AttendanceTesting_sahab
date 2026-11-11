import sys, json, uuid
from pymongo import MongoClient

sys.stdout.reconfigure(encoding='utf-8')

client = MongoClient('mongodb://10.1.0.4:27018/')
db = client['Sahab']

print("=== Companies in WorkAssignments ===")
comp_ids = db['ERP.Attendance.WorkAssignments'].distinct("CompanyId")
for cid in comp_ids:
    c_uuid = cid.as_uuid() if hasattr(cid, 'as_uuid') else cid
    cnt = db['ERP.Attendance.WorkAssignments'].count_documents({"CompanyId": cid})
    print(f"  Company: {c_uuid} -> {cnt} assignments")

print("=== Companies in WorkAssignmentMaps ===")
map_cids = db['ERP.Attendance.WorkAssignmentMaps'].distinct("CompanyId")
for cid in map_cids:
    c_uuid = cid.as_uuid() if hasattr(cid, 'as_uuid') else cid
    cnt = db['ERP.Attendance.WorkAssignmentMaps'].count_documents({"CompanyId": cid})
    print(f"  Company: {c_uuid} -> {cnt} maps")
