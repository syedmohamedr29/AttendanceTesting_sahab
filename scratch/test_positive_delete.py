import json, requests, sys
from pymongo import MongoClient
from bson import Binary
import uuid

sys.stdout.reconfigure(encoding='utf-8')

token_data = json.load(open('scratch/current_token.json', encoding='utf-8'))
token = token_data.get('access_token')

headers = {
    "Authorization": f"Bearer {token}",
    "Content-Type": "application/json"
}

company_id = "3a249871-7a8d-dec5-2d72-47795dd2662d"
loc_id = "3a24d646-b3cf-b1d4-61bb-1adf094b52fc" # Location 2

client = MongoClient('mongodb://10.1.0.4:27018/')
db = client['Sahab']
comp_bin = Binary.from_uuid(uuid.UUID(company_id))

doc = db['ERP.Attendance.WorkTemplates'].find_one({"ShortCode": "DLPOS01", "CompanyId": comp_bin})
if doc:
    created_id = str(doc['_id'].as_uuid())
    print(f"Found DLPOS01 in MongoDB! _id: {created_id}")
    print(f"MongoDB Before Delete: IsDeleted={doc.get('IsDeleted')}, Status={doc.get('Status')}")

    # Call Delete API
    url_del = f"https://attendance2.dev.zoolwork.com/api/companies/{company_id}/worktemplates/{created_id}/delete?locationId={loc_id}"
    res_del = requests.patch(url_del, headers=headers)
    print(f"\nPATCH Delete Status: {res_del.status_code}")
    print(f"PATCH Delete Response: {res_del.text}")

    # Check MongoDB after deletion
    after_doc = db['ERP.Attendance.WorkTemplates'].find_one({"_id": doc['_id']})
    print(f"\nMongoDB After Delete:")
    print(f"  IsDeleted: {after_doc.get('IsDeleted')}")
    print(f"  Status: {after_doc.get('Status')}")
    print(f"  ModifiedBy: {after_doc.get('ModifiedBy')}")
    print(f"  ModifiedAt: {after_doc.get('ModifiedAt')}")
    print(f"  CreatedAt: {after_doc.get('CreatedAt')}")
    print(f"  CreatedBy: {after_doc.get('CreatedBy')}")
    print(f"  ChangeLog: {after_doc.get('ChangeLog')}")
else:
    print("DLPOS01 not found in Mongo!")
