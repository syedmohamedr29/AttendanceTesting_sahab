# -*- coding: utf-8 -*-
from pymongo import MongoClient

client = MongoClient('mongodb://10.1.0.4:27018/', serverSelectionTimeoutMS=5000, uuidRepresentation='csharpLegacy')
db_comp = client['CompanySvcNET8test']

print("=== Attendance Companies in CompaniesMaster ===")
for doc in db_comp['CompaniesMaster'].find():
    bd = doc.get('BasicDetails', {})
    cn = bd.get('CompanyName', {})
    en_name = cn.get('en', {}).get('Name') if isinstance(cn.get('en'), dict) else None
    if en_name and 'attendance' in en_name.lower():
        locs = doc.get('CompanyWorkLocations', [])
        loc_info = [(str(l.get('Id')), l.get('Name', {}).get('en') if isinstance(l.get('Name'), dict) else l.get('Name')) for l in locs]
        print(f"{en_name:<20} | ID: {doc['_id']} | TenantId: {doc.get('TenantId')} | Locations ({len(loc_info)}): {loc_info}")
