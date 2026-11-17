# -*- coding: utf-8 -*-
from pymongo import MongoClient
import uuid

client = MongoClient('mongodb://10.1.0.4:27018/', serverSelectionTimeoutMS=5000, uuidRepresentation='csharpLegacy')
db_comp = client['CompanySvcNET8test']

doc = db_comp['CompaniesMaster'].find_one({"_id": uuid.UUID("3a249871-7a8d-dec5-2d72-47795dd2662d")})
if doc:
    print("Locations in Attendance 8:")
    for l in doc.get("CompanyWorkLocations", []):
        print("  ", l)
