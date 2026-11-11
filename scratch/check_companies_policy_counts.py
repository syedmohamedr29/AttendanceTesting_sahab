import pymongo, sys
from bson.binary import UuidRepresentation
from bson.codec_options import CodecOptions

sys.stdout.reconfigure(encoding='utf-8')
client = pymongo.MongoClient('mongodb://10.1.0.4:27018/?directConnection=true', serverSelectionTimeoutMS=5000)
db = client['Sahab']
col = db.get_collection('ERP.Attendance.Policies', codec_options=CodecOptions(uuid_representation=UuidRepresentation.STANDARD))

counts = {}
for doc in col.find({}, {'CompanyId': 1, 'CompanyName': 1, 'Type': 1}):
    cid = str(doc.get('CompanyId'))
    cname = str(doc.get('CompanyName', {}).get('en') if isinstance(doc.get('CompanyName'), dict) else doc.get('CompanyName'))
    ptype = doc.get('Type')
    key = (cid, cname)
    if key not in counts:
        counts[key] = {1: 0, 2: 0, 3: 0, 'total': 0}
    counts[key][ptype] = counts[key].get(ptype, 0) + 1
    counts[key]['total'] += 1

print(f"{'Company ID':<38} | {'Company Name':<20} | Total | Break(1) | OT(2) | Grace(3)")
print("-" * 90)
for (cid, cname), v in counts.items():
    print(f"{cid:<38} | {cname:<20} | {v['total']:<5} | {v.get(1,0):<8} | {v.get(2,0):<5} | {v.get(3,0):<8}")
