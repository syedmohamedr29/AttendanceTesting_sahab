import json, requests, sys, concurrent.futures
from pymongo import MongoClient
from bson import Binary
import uuid

sys.stdout.reconfigure(encoding='utf-8')

token_data = json.load(open('scratch/current_token.json', encoding='utf-8'))
token = token_data.get('access_token')

headers = {
    "Authorization": f"Bearer {token}",
    "Content-Type": "application/json"
}

company_id = "3a249871-7a8d-dec5-2d72-47795dd2662d"
loc_id = "3a24d646-b3cf-b1d4-61bb-1adf094b52fc"

# Create a test template for concurrent delete
payload = {
    "templateName": { "en": "Concurrent Delete Test", "ar": "اختبار الحذف المتزامن" },
    "shortCode": "DLCON01",
    "templateType": 1,
    "totalWorkDurationInMinutes": 2700,
    "totalWorkingDays": 5,
    "totalDaysOff": 2,
    "timeZoneId": "Asia/Riyadh",
    "fixedTimeSlots": [
        { "dayEnum": 1, "isWorkingDay": True, "recurrenceOfMonth": [1, 2, 3, 4, 5], "startTime": "08:00:00", "endTime": "17:00:00", "workDurationInMinutes": 540 },
        { "dayEnum": 2, "isWorkingDay": True, "recurrenceOfMonth": [1, 2, 3, 4, 5], "startTime": "08:00:00", "endTime": "17:00:00", "workDurationInMinutes": 540 },
        { "dayEnum": 3, "isWorkingDay": True, "recurrenceOfMonth": [1, 2, 3, 4, 5], "startTime": "08:00:00", "endTime": "17:00:00", "workDurationInMinutes": 540 },
        { "dayEnum": 4, "isWorkingDay": True, "recurrenceOfMonth": [1, 2, 3, 4, 5], "startTime": "08:00:00", "endTime": "17:00:00", "workDurationInMinutes": 540 },
        { "dayEnum": 5, "isWorkingDay": True, "recurrenceOfMonth": [1, 2, 3, 4, 5], "startTime": "08:00:00", "endTime": "17:00:00", "workDurationInMinutes": 540 },
        { "dayEnum": 6, "isWorkingDay": False, "recurrenceOfMonth": [], "startTime": "00:00:00", "endTime": "00:00:00", "workDurationInMinutes": 0 },
        { "dayEnum": 7, "isWorkingDay": False, "recurrenceOfMonth": [], "startTime": "00:00:00", "endTime": "00:00:00", "workDurationInMinutes": 0 }
    ]
}

url_post = f"https://attendance2.dev.zoolwork.com/api/companies/{company_id}/worktemplates/fixed?locationId={loc_id}"
res_post = requests.post(url_post, headers=headers, json=payload)
client = MongoClient('mongodb://10.1.0.4:27018/')
db = client['Sahab']
comp_bin = Binary.from_uuid(uuid.UUID(company_id))
doc = db['ERP.Attendance.WorkTemplates'].find_one({"ShortCode": "DLCON01", "CompanyId": comp_bin})
target_id = str(doc['_id'].as_uuid())
print(f"Created DLCON01: {target_id}")

url_del = f"https://attendance2.dev.zoolwork.com/api/companies/{company_id}/worktemplates/{target_id}/delete?locationId={loc_id}"

def send_del(req_num):
    r = requests.patch(url_del, headers=headers)
    return req_num, r.status_code, r.text

with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
    futures = [executor.submit(send_del, 1), executor.submit(send_del, 2)]
    for f in concurrent.futures.as_completed(futures):
        req_num, code, text = f.result()
        print(f"Req {req_num}: Status {code} | Response: {text}")

after = db['ERP.Attendance.WorkTemplates'].find_one({"_id": doc['_id']})
print(f"Mongo after concurrent delete: IsDeleted={after.get('IsDeleted')}")
