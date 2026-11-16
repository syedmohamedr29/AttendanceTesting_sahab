import pymongo, uuid

client = pymongo.MongoClient('mongodb://10.1.0.4:27018/', serverSelectionTimeoutMS=5000, uuidRepresentation='standard')
sahab = client['Sahab']

# Check Jeddah Rotation Board
j_board = sahab['ERP.Attendance.ShiftRotationBoard'].find_one({'_id': uuid.UUID('03ade8fe-7d7f-4244-8172-94111fffef78')})
print("Jeddah Rotation Board Members count:", len(j_board.get('Members', [])))
for m in j_board.get('Members', []):
    print("  Member:", m.get('EmployeeId'), "Team:", m.get('TeamId'), "IsActive:", m.get('IsActive'), "Start:", m.get('StartDate'), "End:", m.get('EndDate'))

# Check WorkAssignmentMaps for SA-EMP-0001
maps_col = sahab['ERP.Attendance.WorkAssignmentMaps']
emp1_maps = list(maps_col.find({"EmployeeId": uuid.UUID('f9e1a6d5-6bd5-7d46-ae85-38b81dc80887')}))
print(f"\nSA-EMP-0001 WorkAssignmentMaps count: {len(emp1_maps)}")
for m in emp1_maps[:5]:
    print("  Map ID:", m.get('_id'), "Loc:", m.get('LocationId'), "Source:", m.get('Source'), "PlanId:", m.get('WorkPlanId'), "RotId:", m.get('RotationId'), "IsActive:", m.get('IsActive'))
