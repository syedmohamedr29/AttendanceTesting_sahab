# -*- coding: utf-8 -*-
from pymongo import MongoClient
import uuid

client = MongoClient('mongodb://10.1.0.4:27018/', serverSelectionTimeoutMS=5000, uuidRepresentation='csharpLegacy')
db = client['Sahab']
col = db['ERP.Attendance.HolidayCalendars']

print("=== Companies with Holiday Calendars in Mongo ===")
pipeline = [
    {"$group": {
        "_id": "$CompanyId",
        "count": {"$sum": 1},
        "types": {"$addToSet": "$CalendarType"},
        "locations": {"$addToSet": "$LocationId"}
    }}
]

for doc in col.aggregate(pipeline):
    cid = doc["_id"]
    # Convert binary UUID to standard string if binary
    cid_str = str(uuid.UUID(bytes_le=cid)) if isinstance(cid, bytes) and len(cid) == 16 else str(cid)
    types = doc["types"]
    loc_count = len(doc["locations"])
    print(f"Company UUID: {cid_str} | Calendars: {doc['count']} | Types: {types} | Locations: {loc_count}")
