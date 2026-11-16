import pymongo

client = pymongo.MongoClient('mongodb://10.1.0.4:27018/', serverSelectionTimeoutMS=5000)
db_emp = client['EmployeeSvcNET8test']
col_emp = db_emp['Employee']

doc = col_emp.find_one({"EmployeeCode": "SA-EMP-0001"})
if doc:
    print("Found SA-EMP-0001:")
    print("  _id:", doc.get("_id"))
    print("  EmployeeCode:", doc.get("EmployeeCode"))
    print("  IsActive:", doc.get("IsActive"))
    print("  CompanyId field:", doc.get("CompanyId"))
    print("  Employment:", doc.get("Employment"))
    print("  Keys:", list(doc.keys()))
else:
    print("SA-EMP-0001 not found.")
