import pymongo
from bson import json_util, binary
import datetime
import uuid
import json

opts = json_util.JSONOptions(uuid_representation=binary.UuidRepresentation.STANDARD)

client = pymongo.MongoClient('mongodb://10.1.0.4:27018/', serverSelectionTimeoutMS=5000, uuidRepresentation='standard')
db = client['Sahab']

wa_col = db['ERP.Attendance.WorkAssignments']
wam_col = db['ERP.Attendance.WorkAssignmentMaps']

att11_uuid = uuid.UUID('3a24e5e5-302e-91bd-feaa-b07979766dfe')
print('=== Attendance 11 in ERP.Attendance.WorkAssignments ===')
for doc in wa_col.find({'CompanyId': att11_uuid}):
    print(json_util.dumps(doc, indent=2, json_options=opts))

print('\n=== Attendance 11 in ERP.Attendance.WorkAssignmentMaps ===')
for doc in wam_col.find({'CompanyId': att11_uuid}):
    print(json_util.dumps(doc, indent=2, json_options=opts))

# Also check Attendance 10
att10_uuid = uuid.UUID('3a249872-e23c-a401-7d8b-4a8049ac8c9b')
print('\n=== Attendance 10 in ERP.Attendance.WorkAssignments ===')
print('Count:', wa_col.count_documents({'CompanyId': att10_uuid}))
print('=== Attendance 10 in ERP.Attendance.WorkAssignmentMaps ===')
print('Count:', wam_col.count_documents({'CompanyId': att10_uuid}))

# AssignmentType breakdown across collection
print('\n=== AssignmentType Breakdown in WorkAssignmentMaps ===')
for at in [1, 2, 3]:
    cnt = wam_col.count_documents({'AssignmentType': at})
    name = {1: 'Regular', 2: 'Roster', 3: 'Rotation'}.get(at, 'Unknown')
    print(f'  Type {at} ({name}): {cnt}')
