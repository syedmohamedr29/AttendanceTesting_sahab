import pymongo, uuid

client = pymongo.MongoClient('mongodb://10.1.0.4:27018/', serverSelectionTimeoutMS=5000, uuidRepresentation='standard')
sahab = client['Sahab']
doc = sahab['ERP.Attendance.ShiftRotationBoard'].find_one({'_id': uuid.UUID('03ade8fe-7d7f-4244-8172-94111fffef78')})
print("Teams in Jeddah doc:")
for t in doc.get('Teams', []):
    print("  TeamId:", t.get('TeamId'), "Name:", t.get('TeamName'))
