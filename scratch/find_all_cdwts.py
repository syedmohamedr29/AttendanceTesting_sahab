import sys, json, uuid
from pymongo import MongoClient

sys.stdout.reconfigure(encoding='utf-8')

client = MongoClient('mongodb://10.1.0.4:27018/')
db = client['Sahab']

print("=== Scanning active CDWT across all companies ===")
cdwts = list(db['ERP.Attendance.WorkTemplates'].find({"IsDefault": True, "IsSuperseded": False, "IsDeleted": False}))
print(f"Total active default templates: {len(cdwts)}")
for t in cdwts:
    cid = t.get('CompanyId')
    lid = t.get('LocationId')
    cid_str = str(cid.as_uuid() if hasattr(cid, 'as_uuid') else cid)
    lid_str = str(lid.as_uuid() if hasattr(lid, 'as_uuid') else lid)
    tt = t.get('TemplateType')
    sc = t.get('ShortCode')
    name = t.get('WorkTemplateName')
    tid = str(t['_id'].as_uuid() if hasattr(t['_id'], 'as_uuid') else t['_id'])
    print(f"  Type {tt} ({sc}) | _id: {tid} | Company: {cid_str} | Loc: {lid_str} | Name: {name}")
