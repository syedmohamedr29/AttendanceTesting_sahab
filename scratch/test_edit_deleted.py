import json, requests, sys

sys.stdout.reconfigure(encoding='utf-8')

token_data = json.load(open('scratch/current_token.json', encoding='utf-8'))
token = token_data.get('access_token')

headers = {
    "Authorization": f"Bearer {token}",
    "Content-Type": "application/json"
}

company_id = "3a249871-7a8d-dec5-2d72-47795dd2662d"
loc_id = "3a24d646-b3cf-b1d4-61bb-1adf094b52fc"
deleted_id = "cf3ef115-b548-436b-afd1-568be4f5ebfa"

payload = {
    "templateName": { "en": "Revived Shift", "ar": "وردية مستعادة" },
    "shortCode": "DLPOS01",
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

url_patch = f"https://attendance2.dev.zoolwork.com/api/companies/{company_id}/worktemplates/fixed/{deleted_id}?locationId={loc_id}"
res = requests.patch(url_patch, headers=headers, json=payload)
print(f"Edit Deleted Template Status: {res.status_code}")
print(f"Edit Deleted Template Response: {res.text}")
