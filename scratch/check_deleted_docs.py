import pymongo, uuid
from bson.binary import Binary

client = pymongo.MongoClient("mongodb://10.1.0.4:27018/")
db = client["Sahab"]
col = db["ERP.Attendance.WorkTemplates"]

cid = Binary.from_uuid(uuid.UUID("3a249871-7a8d-dec5-2d72-47795dd2662d"))
docs = list(col.find({"CompanyId": cid, "IsDeleted": True}))
print(f"Found {len(docs)} soft-deleted documents for Attendance 8:")
for d in docs:
    loc_val = uuid.UUID(bytes=d["LocationId"]) if d.get("LocationId") else "Company"
    print(f"  _id: {uuid.UUID(bytes=d['_id'])} | ShortCode: {d.get('ShortCode')} | Type: {d.get('TemplateType')} | Loc: {loc_val}")
