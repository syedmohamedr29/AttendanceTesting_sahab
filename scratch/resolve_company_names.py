# -*- coding: utf-8 -*-
from pymongo import MongoClient
import uuid

client = MongoClient('mongodb://10.1.0.4:27018/', serverSelectionTimeoutMS=5000, uuidRepresentation='csharpLegacy')
db_comp = client['CompanySvcNET8test']

cids = [
    uuid.UUID("0056203a-a311-b96d-897f-bd360d56fc2d"),
    uuid.UUID("7298243a-3ce2-01a4-7d8b-4a8049ac8c9b"),
    uuid.UUID("8bfc1b3a-a6d3-ad8f-a1e3-cc095d479d38"),
    uuid.UUID("5a07243a-e621-e8ba-cc36-5a4e41e90e32"),
]

print("=== Resolving Company Names ===")
for cid in cids:
    doc = db_comp['CompaniesMaster'].find_one({"_id": cid})
    if doc:
        print(f"CID: {cid} | Name: {doc.get('Name')} | Code: {doc.get('Code')} | Locations: {len(doc.get('Locations', []))}")
        for l in doc.get('Locations', []):
            print(f"   Loc ID: {l.get('LocationId') or l.get('Id')} | Name: {l.get('Name')}")
    else:
        print(f"CID {cid} not found in CompaniesMaster")
