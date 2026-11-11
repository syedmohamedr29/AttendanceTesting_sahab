import pymongo, uuid
from bson.binary import Binary

client = pymongo.MongoClient("mongodb://10.1.0.4:27018/")
db = client["Sahab"]
col = db["ERP.Attendance.WorkTemplates"]

cid = Binary.from_uuid(uuid.UUID("3a249871-7a8d-dec5-2d72-47795dd2662d"))
locs = {
    "Location 1": "3a24d629-0d56-a428-baa1-98493a77e614",
    "Location 2": "3a24d646-b3cf-b1d4-61bb-1adf094b52fc",
    "Location 3": "3a24d667-0dcc-e3d1-74a3-cbee98168772"
}

for name, lid in locs.items():
    lid_b = Binary.from_uuid(uuid.UUID(lid))
    tot = col.count_documents({"CompanyId": cid, "LocationId": lid_b})
    active = col.count_documents({"CompanyId": cid, "LocationId": lid_b, "IsDeleted": False})
    deleted = col.count_documents({"CompanyId": cid, "LocationId": lid_b, "IsDeleted": True})
    print(f"{name} ({lid}): Total={tot}, Active={active}, Deleted={deleted}")
