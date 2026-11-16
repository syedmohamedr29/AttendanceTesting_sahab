import pymongo, uuid
from bson import binary

client = pymongo.MongoClient('mongodb://10.1.0.4:27018/', serverSelectionTimeoutMS=5000, uuidRepresentation='standard')
db = client['EmployeeSvcNET8test']

emps = list(db['Employee'].find({'EmployeeCode': {'$in': ['SA-EMP-0001', 'SA-EMP-0002', 'SA-EMP-0003', 'SA-EMP-0004', 'SA-EMP-0005', 'SA-EMP-0006']}}).sort('EmployeeCode', 1))
for e in emps:
    raw_id = e['_id']
    if hasattr(raw_id, 'as_uuid'):
        emp_id = raw_id.as_uuid(binary.UuidRepresentation.CSHARP_LEGACY)
    elif isinstance(raw_id, (bytes, bytearray)):
        emp_id = uuid.UUID(bytes_le=raw_id)
    else:
        emp_id = str(raw_id)
    
    doj = e.get('WorkInformation', {}).get('DateOfJoining')
    loc = e.get('WorkInformation', {}).get('WorkLocation', {})
    loc_name = loc.get('Name', {}).get('en') if isinstance(loc.get('Name'), dict) else str(loc.get('Name'))
    
    print(f"Code: {e.get('EmployeeCode'):<12} | ID: {str(emp_id)} | IsActive: {e.get('IsActive')!s:<5} | Status: {e.get('EmployeeStatus')} | Onboard: {e.get('OnBoardingStatus')} | Loc: {loc_name} | DOJ: {doj}")
