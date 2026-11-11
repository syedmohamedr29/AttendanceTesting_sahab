import pymongo, uuid, sys
from bson.binary import UuidRepresentation
from bson.codec_options import CodecOptions

sys.stdout.reconfigure(encoding='utf-8')
client = pymongo.MongoClient('mongodb://10.1.0.4:27018/?directConnection=true', serverSelectionTimeoutMS=5000)
db = client['Sahab']
col = db.get_collection('ERP.Attendance.Policies', codec_options=CodecOptions(uuid_representation=UuidRepresentation.STANDARD))

att7_str = '3a249870-c8ae-b3dc-1b8d-c44efad14f89'
u = uuid.UUID(att7_str)

docs = list(col.find({'CompanyId': u}))
print(f"Total Policies in Attendance 7: {len(docs)}")
types = {}
for d in docs:
    t = d.get('Type')
    types[t] = types.get(t, 0) + 1
    print(f"ID: {d.get('_id')} | Type: {d.get('Type')} | _t: {d.get('_t')} | Name: {d.get('Name')}")
    if d.get('Type') == 1 or 'Break' in str(d.get('_t', '')):
        print(f"   BREAK POLICY DETAILS: Breaks count: {len(d.get('Breaks', []))} | TotalDuration: {d.get('TotalBreakDurationInMinutes')}")
        for b in d.get('Breaks', []):
            print(f"      Item: {b}")

print("Type breakdown:", types)
