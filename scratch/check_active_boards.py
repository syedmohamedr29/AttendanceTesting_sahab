import pymongo, uuid

client = pymongo.MongoClient('mongodb://10.1.0.4:27018/', serverSelectionTimeoutMS=5000, uuidRepresentation='standard')
sahab = client['Sahab']
comp_id = uuid.UUID('3a24e5e5-302e-91bd-feaa-b07979766dfe')
boards = list(sahab['ERP.Attendance.ShiftRotationBoard'].find({'CompanyId': comp_id, 'IsDeleted': False}))
print(f"Active boards count for Attendance 11: {len(boards)}")
for b in boards:
    print(f"  ID: {b.get('_id')}, Name: {b.get('RotationName')}, Location: {b.get('LocationId')}, Members: {len(b.get('Members', []))}, Teams: {len(b.get('Teams', []))}")
