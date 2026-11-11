import json
from bson.binary import Binary
import uuid, pymongo

client = pymongo.MongoClient("mongodb://10.1.0.4:27018/")
db = client["Sahab"]
col = db["ERP.Attendance.WorkTemplates"]

with open("scratch/rotation_test_suite_results.json", "r", encoding="utf-8") as f:
    results = json.load(f)

for tid in ["ROT-N03", "ROT-N07", "ROT-N32"]:
    t = next(x for x in results if x["test_id"] == tid)
    print(f"\n=== {tid} ===")
    print("Payload:", json.dumps(t["payload"], indent=2))
    print("Response summary:", t["response_summary"])
    created_id = t.get("created_id")
    print("Created ID:", created_id)
    if created_id:
        doc = col.find_one({"_id": Binary.from_uuid(uuid.UUID(created_id))})
        if doc:
            print("MongoDB Document:")
            print("  ShortCode:", doc.get("ShortCode"))
            print("  TemplateType:", doc.get("TemplateType"))
            print("  WorkTemplateName:", doc.get("WorkTemplateName"))
            print("  CompanyId:", uuid.UUID(bytes=doc["CompanyId"]))
            print("  LocationId:", uuid.UUID(bytes=doc["LocationId"]) if doc.get("LocationId") else None)
            print("  LocationName:", doc.get("LocationName"))
