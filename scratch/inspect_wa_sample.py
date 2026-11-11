import sys, json, uuid
from pymongo import MongoClient

sys.stdout.reconfigure(encoding='utf-8')

client = MongoClient('mongodb://10.1.0.4:27018/')
db = client['Sahab']

sample = db['ERP.Attendance.WorkAssignments'].find_one()
if sample:
    print(f"Sample WA: keys={list(sample.keys())}")
    for k, v in sample.items():
        if hasattr(v, 'as_uuid'):
            print(f"  {k}: {v.as_uuid()}")
        else:
            print(f"  {k}: {v}")
else:
    print("No sample found!")
