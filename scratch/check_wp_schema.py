import pymongo, json, uuid
from bson import binary

mongo = pymongo.MongoClient('mongodb://10.1.0.4:27018/')
db = mongo['Sahab']
one_wp = db['ERP.Attendance.WorkPlans'].find_one()
if one_wp:
    print('WP top keys:', list(one_wp.keys()))
    print('Company:', one_wp.get('CompanyId') or one_wp.get('Company'))

# Let's find work plan from existing assignment f9e467c6-fd79-4066-87f6-b4262419c5f8
wa = db['ERP.Attendance.WorkAssignments'].find_one()
if wa:
    print('Existing WA keys:', list(wa.keys()))
    print('WA WorkPlanId:', wa.get('WorkPlanId'))
    print('WA CompanyId:', wa.get('CompanyId'))
    print('WA LocationId:', wa.get('LocationId'))
