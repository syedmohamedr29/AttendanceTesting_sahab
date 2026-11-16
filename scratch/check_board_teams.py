import pymongo, uuid

client = pymongo.MongoClient('mongodb://10.1.0.4:27018/', serverSelectionTimeoutMS=5000, uuidRepresentation='standard')
sahab = client['Sahab']
doc = sahab['ERP.Attendance.ShiftRotationBoard'].find_one({"_id": uuid.UUID("28636e78-43be-4859-b904-2644f8eea88b")})
if doc:
    print("Found board 28636e78-43be-4859-b904-2644f8eea88b:")
    for t in doc.get("Teams", []):
        print("  Team:", t.get("TeamId"), t.get("TeamName"))
