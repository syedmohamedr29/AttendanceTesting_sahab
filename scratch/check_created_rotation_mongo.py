import pymongo, uuid, json
from bson.binary import Binary

client = pymongo.MongoClient("mongodb://10.1.0.4:27018/")
db = client["Sahab"]
col = db["ERP.Attendance.WorkTemplates"]

tid = Binary.from_uuid(uuid.UUID("5aa227f7-3b96-444c-9c2d-51ecbf52b7ee"))
doc = col.find_one({"_id": tid})

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
