# -*- coding: utf-8 -*-
from pymongo import MongoClient

client = MongoClient('mongodb://10.1.0.4:27018/', serverSelectionTimeoutMS=5000, uuidRepresentation='csharpLegacy')
db_comp = client['CompanySvcNET8test']

# Find companies in CompanySvcNET8test
print("=== Companies in CompanySvcNET8test.CompaniesMaster ===")
for doc in db_comp['CompaniesMaster'].find({}, {"Name": 1, "Locations": 1}).limit(15):
    c_name = doc.get("Name", {})
    locs = doc.get("Locations", [])
    loc_names = [l.get("Name", {}).get("en") or l.get("Name", {}).get("ar") for l in locs]
    print(f"Company ID: {doc['_id']} | Name: {c_name} | Locations: {loc_names}")

db_att = client['Sahab']
print("\n=== Recent Holiday Calendars in Sahab ===")
for doc in db_att['ERP.Attendance.HolidayCalendars'].find().sort("_id", -1).limit(5):
    print(f"ID: {doc['_id']} | CompanyId: {doc.get('CompanyId')} | LocId: {doc.get('LocationId')} | Year: {doc.get('Year')} | Type: {doc.get('CalendarType')} | IsInherited: {doc.get('IsInherited')}")
