import json, requests, sys
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
loc_id = "3a24d646-b3cf-b1d4-61bb-1adf094b52fc" # Location 2

client = MongoClient('mongodb://10.1.0.4:27018/')
db = client['Sahab']
comp_bin = Binary.from_uuid(uuid.UUID(company_id))

# 1. Flexible Positive Delete (DEL-P02)
flexi_payload = {
    "templateName": { "en": "Delete Test Flexi Shift DLFLX01", "ar": "وردية اختبار الحذف DLFLX01" },
    "shortCode": "DLFLX01",
    "templateType": 2,
    "flexibleType": 1,
    "totalWorkDurationInMinutes": 2400,
    "totalWorkingDays": 5,
    "totalDaysOff": 2,
    "timeZoneId": "Asia/Riyadh",
    "flexiTimeSlots": [
        { "dayEnum": 1, "isWorkingDay": True, "recurrenceOfMonth": [1, 2, 3, 4, 5], "workDurationInMinutes": 480 },
        { "dayEnum": 2, "isWorkingDay": True, "recurrenceOfMonth": [1, 2, 3, 4, 5], "workDurationInMinutes": 480 },
        { "dayEnum": 3, "isWorkingDay": True, "recurrenceOfMonth": [1, 2, 3, 4, 5], "workDurationInMinutes": 480 },
        { "dayEnum": 4, "isWorkingDay": True, "recurrenceOfMonth": [1, 2, 3, 4, 5], "workDurationInMinutes": 480 },
        { "dayEnum": 5, "isWorkingDay": True, "recurrenceOfMonth": [1, 2, 3, 4, 5], "workDurationInMinutes": 480 },
        { "dayEnum": 6, "isWorkingDay": False, "recurrenceOfMonth": [], "workDurationInMinutes": 0 },
        { "dayEnum": 7, "isWorkingDay": False, "recurrenceOfMonth": [], "workDurationInMinutes": 0 }
    ]
}

url_flexi_post = f"https://attendance2.dev.zoolwork.com/api/companies/{company_id}/worktemplates/flexi?locationId={loc_id}"
res_flx = requests.post(url_flexi_post, headers=headers, json=flexi_payload)
print(f"POST DLFLX01 Status: {res_flx.status_code}")
flx_doc = db['ERP.Attendance.WorkTemplates'].find_one({"ShortCode": "DLFLX01", "CompanyId": comp_bin})
if flx_doc:
    flx_id = str(flx_doc['_id'].as_uuid())
    print(f"  DLFLX01 Created ID: {flx_id}")
    url_del_flx = f"https://attendance2.dev.zoolwork.com/api/companies/{company_id}/worktemplates/{flx_id}/delete?locationId={loc_id}"
    res_del_flx = requests.patch(url_del_flx, headers=headers)
    print(f"  PATCH Delete DLFLX01 Status: {res_del_flx.status_code} | {res_del_flx.text}")
    after_flx = db['ERP.Attendance.WorkTemplates'].find_one({"_id": flx_doc['_id']})
    print(f"  MongoDB DLFLX01 After Delete: IsDeleted={after_flx.get('IsDeleted')}")

# 2. Split Positive Delete (DEL-P03)
split_payload = {
    "templateName": { "en": "Delete Test Split Shift DLSPL01", "ar": "وردية اختبار الحذف DLSPL01" },
    "shortCode": "DLSPL01",
    "templateType": 3,
    "totalWorkDurationInMinutes": 2400,
    "totalWorkingDays": 5,
    "totalDaysOff": 2,
    "timeZoneId": "Asia/Riyadh",
    "splitTimeSlots": [
        { "dayEnum": 1, "isWorkingDay": True, "recurrenceOfMonth": [1, 2, 3, 4, 5], "workDurationInMinutes": 480, "timeSlots": [
            { "startTime": "08:00:00", "endTime": "12:00:00", "workDurationInMinutes": 240 },
            { "startTime": "14:00:00", "endTime": "18:00:00", "workDurationInMinutes": 240 }
        ]},
        { "dayEnum": 2, "isWorkingDay": True, "recurrenceOfMonth": [1, 2, 3, 4, 5], "workDurationInMinutes": 480, "timeSlots": [
            { "startTime": "08:00:00", "endTime": "12:00:00", "workDurationInMinutes": 240 },
            { "startTime": "14:00:00", "endTime": "18:00:00", "workDurationInMinutes": 240 }
        ]},
        { "dayEnum": 3, "isWorkingDay": True, "recurrenceOfMonth": [1, 2, 3, 4, 5], "workDurationInMinutes": 480, "timeSlots": [
            { "startTime": "08:00:00", "endTime": "12:00:00", "workDurationInMinutes": 240 },
            { "startTime": "14:00:00", "endTime": "18:00:00", "workDurationInMinutes": 240 }
        ]},
        { "dayEnum": 4, "isWorkingDay": True, "recurrenceOfMonth": [1, 2, 3, 4, 5], "workDurationInMinutes": 480, "timeSlots": [
            { "startTime": "08:00:00", "endTime": "12:00:00", "workDurationInMinutes": 240 },
            { "startTime": "14:00:00", "endTime": "18:00:00", "workDurationInMinutes": 240 }
        ]},
        { "dayEnum": 5, "isWorkingDay": True, "recurrenceOfMonth": [1, 2, 3, 4, 5], "workDurationInMinutes": 480, "timeSlots": [
            { "startTime": "08:00:00", "endTime": "12:00:00", "workDurationInMinutes": 240 },
            { "startTime": "14:00:00", "endTime": "18:00:00", "workDurationInMinutes": 240 }
        ]},
        { "dayEnum": 6, "isWorkingDay": False, "recurrenceOfMonth": [], "workDurationInMinutes": 0, "timeSlots": [] },
        { "dayEnum": 7, "isWorkingDay": False, "recurrenceOfMonth": [], "workDurationInMinutes": 0, "timeSlots": [] }
    ]
}

url_split_post = f"https://attendance2.dev.zoolwork.com/api/companies/{company_id}/worktemplates/split?locationId={loc_id}"
res_spl = requests.post(url_split_post, headers=headers, json=split_payload)
print(f"\nPOST DLSPL01 Status: {res_spl.status_code}")
spl_doc = db['ERP.Attendance.WorkTemplates'].find_one({"ShortCode": "DLSPL01", "CompanyId": comp_bin})
if spl_doc:
    spl_id = str(spl_doc['_id'].as_uuid())
    print(f"  DLSPL01 Created ID: {spl_id}")
    url_del_spl = f"https://attendance2.dev.zoolwork.com/api/companies/{company_id}/worktemplates/{spl_id}/delete?locationId={loc_id}"
    res_del_spl = requests.patch(url_del_spl, headers=headers)
    print(f"  PATCH Delete DLSPL01 Status: {res_del_spl.status_code} | {res_del_spl.text}")
    after_spl = db['ERP.Attendance.WorkTemplates'].find_one({"_id": spl_doc['_id']})
    print(f"  MongoDB DLSPL01 After Delete: IsDeleted={after_spl.get('IsDeleted')}")
