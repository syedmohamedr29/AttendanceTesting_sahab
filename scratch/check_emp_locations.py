import pymongo, uuid
from bson import binary

mongo = pymongo.MongoClient('mongodb://10.1.0.4:27018/')
db = mongo['EmployeeSvcNET8test']

emps = list(db['Employee'].find({'EmployeeCode': {'$in': ['SA-EMP-0001', 'SA-EMP-0002', 'SA-EMP-0003', 'SA-EMP-0004']}}))
for e in emps:
    raw_id = e['_id']
    uid = raw_id.as_uuid(binary.UuidRepresentation.CSHARP_LEGACY) if hasattr(raw_id, 'as_uuid') else uuid.UUID(bytes_le=raw_id)
    w_loc = e.get('WorkInformation', {}).get('WorkLocation', {})
    print(f"EmployeeCode: {e.get('EmployeeCode')}")
    print(f"  EmployeeId: {uid}")
    print(f"  WorkLocation keys: {list(w_loc.keys())}")
    print(f"  WorkLocation: {w_loc}")
