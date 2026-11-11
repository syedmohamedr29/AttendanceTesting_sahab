import pymongo, uuid
from bson.binary import Binary

client = pymongo.MongoClient("mongodb://10.1.0.4:27018/")
db = client["Sahab"]
col = db["ERP.Attendance.WorkTemplates"]

docs = list(col.find({"$or": [{"TemplateType": 5}, {"TemplateType": "Rotation"}, {"_t": "RotationWorkTemplate"}]}))
print(f"Found {len(docs)} existing Rotation Work Templates in MongoDB:")
for d in docs:
    print(f"  _id: {uuid.UUID(bytes=d['_id'])} | ShortCode: {d.get('ShortCode')} | Company: {uuid.UUID(bytes=d['CompanyId'])} | Loc: {uuid.UUID(bytes=d['LocationId']) if d.get('LocationId') else 'None'}")
