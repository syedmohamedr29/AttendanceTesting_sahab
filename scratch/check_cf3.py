import sys
sys.stdout.reconfigure(encoding='utf-8')
import pymongo, uuid
from bson.binary import Binary

client = pymongo.MongoClient("mongodb://10.1.0.4:27018/")
db = client["Sahab"]
col = db["ERP.Attendance.WorkTemplates"]

tid = Binary.from_uuid(uuid.UUID("cf3ef115-b548-436b-afd1-568be4f5ebfa"))
doc = col.find_one({"_id": tid})
if doc:
    print(f"cf3ef115: IsDeleted={doc.get('IsDeleted')} | ShortCode={doc.get('ShortCode')} | Loc={doc.get('LocationId')}")
else:
    print("cf3ef115 not found")

