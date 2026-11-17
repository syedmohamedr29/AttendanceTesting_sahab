from pymongo import MongoClient
import bson
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

client = MongoClient('mongodb://10.1.0.4:27018/', serverSelectionTimeoutMS=5000)
print("Databases:", client.list_database_names())

db = client['Sahab']
print("Collections in Sahab:", db.list_collection_names()[:20])

# Check for companies collection
for col_name in db.list_collection_names():
    if 'company' in col_name.lower() or 'tenant' in col_name.lower() or 'organization' in col_name.lower():
        print("Found company-related col:", col_name)
        c = db[col_name]
        for doc in c.find():
            # look for name containing Attendance 12
            s = str(doc)
            if 'Attendance 12' in s or 'attendance 12' in s.lower():
                print(f"Match in {col_name}:", doc)

# Also check ERP.Attendance.WorkTemplates for distinct CompanyId
wt_col = db['ERP.Attendance.WorkTemplates']
print("Checking ERP.Attendance.WorkTemplates distinct CompanyId...")
sample_wts = list(wt_col.find({}, {"CompanyId": 1, "WorkTemplateName": 1, "ShortCode": 1}).limit(50))
print(f"Sample WTs count: {len(sample_wts)}")
