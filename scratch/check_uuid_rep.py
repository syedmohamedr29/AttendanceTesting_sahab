# -*- coding: utf-8 -*-
from pymongo import MongoClient

client = MongoClient('mongodb://10.1.0.4:27018/', serverSelectionTimeoutMS=5000)
db_comp = client['CompanySvcNET8test']

doc = db_comp['CompaniesMaster'].find_one({"Name.en": "Attendance 8"})
if not doc:
    # search any attendance
    for d in db_comp['CompaniesMaster'].find().limit(10):
        if 'attendance' in str(d).lower():
            print("Found attendance doc in CompaniesMaster:", d['_id'], type(d['_id']), d.get('Name'))
            break
else:
    print("Found Attendance 8:", doc['_id'], type(doc['_id']))
