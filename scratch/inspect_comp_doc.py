# -*- coding: utf-8 -*-
from pymongo import MongoClient

client = MongoClient('mongodb://10.1.0.4:27018/', serverSelectionTimeoutMS=5000)
db_comp = client['CompanySvcNET8test']

doc = db_comp['CompaniesMaster'].find_one()
if doc:
    print("Keys:", list(doc.keys()))
    print("BasicDetails:", doc.get("BasicDetails"))
