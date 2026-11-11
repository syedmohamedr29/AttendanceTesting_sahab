import pymongo, uuid, json
from bson.binary import Binary

client = pymongo.MongoClient("mongodb://10.1.0.4:27018/")
db = client["Sahab"]
col = db["ERP.Attendance.WorkTemplates"]

doc = col.find_one({"_id": Binary.from_uuid(uuid.UUID("59dd499a-0f08-4ae0-8a20-05682614d27f"))})

def default_serializer(o):
    if isinstance(o, (bytes, bytearray)):
        try:
            return str(uuid.UUID(bytes=o))
        except:
            return str(o)
    if isinstance(o, (Binary)):
        return str(uuid.UUID(bytes=o))
    return str(o)

print(json.dumps(doc, indent=2, default=default_serializer))
