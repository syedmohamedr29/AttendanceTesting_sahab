# -*- coding: utf-8 -*-
from pymongo import MongoClient
import uuid

client = MongoClient('mongodb://10.1.0.4:27018/', serverSelectionTimeoutMS=5000, uuidRepresentation='csharpLegacy')
db_comp = client['CompanySvcNET8test']

for cname, cid_str in [("Attendance 10", "3a249872-e23c-a401-7d8b-4a8049ac8c9b"), ("Attendance 11", "3a24e5e5-302e-91bd-feaa-b07979766dfe")]:
    doc = db_comp['CompaniesMaster'].find_one({"_id": uuid.UUID(cid_str)})
    if doc:
        print(f"=== {cname} ({cid_str}) ===")
        for l in doc.get("CompanyWorkLocations", []):
            loc_id = l.get('_id')
            lname = l.get('LocationName', {}).get('en', {}).get('Name') or l.get('LocationName', {}).get('ar', {}).get('Name')
            print(f"  Location ID: {loc_id} | Name: {lname}")
