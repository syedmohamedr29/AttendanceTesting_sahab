import requests
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('scratch/current_token.json') as f:
    token_data = json.load(f)

token = token_data['access_token']
headers = {
    'Authorization': f'Bearer {token}',
    '__tenant': 'Attendance',
    'Content-Type': 'application/json',
    'Accept': 'application/json'
}

base_url = "https://attendance2.dev.zoolwork.com"
c8 = "3a249871-7a8d-dec5-2d72-47795dd2662d" # Attendance 8
# Attendance 8 holiday types: let's query them or check
# First let's check holiday types for Attendance 8
r_ht = requests.get(f"{base_url}/api/companies/{c8}/holidaytypes", headers=headers)
print("Holiday types for Attendance 8 status:", r_ht.status_code)
ht_id = "3a249870-18c5-eb35-b782-7b26f5f35ccd"
if r_ht.status_code == 200 and r_ht.json():
    ht_id = r_ht.json()[0]['id']
    print(f"Using holiday type ID: {ht_id}")

# 1. Test empty holidayLists: [] (DEFECT-20261103-06 / HC-DTO-80)
p_empty_list = {
    "shortCode": "HOLEMP1",
    "name": {"en": "Empty List Test", "ar": "تجربة"},
    "year": 2026,
    "yearlyCalendar": {
        "year": 2026,
        "holidayLists": []
    }
}
r_emp = requests.post(f"{base_url}/api/companies/{c8}/holidaylist", json=p_empty_list, headers=headers)
print("\n[DEFECT-20261103-06] Empty holidayLists: [] POST status:", r_emp.status_code)
print("Response:", r_emp.text)

# 2. Test chronological inversion: endDate < startDate (DEFECT-20261103-11 / HC-DTO-66)
p_inversion = {
    "shortCode": "HOLINV1",
    "name": {"en": "Inversion Test", "ar": "تجربة"},
    "year": 2026,
    "yearlyCalendar": {
        "year": 2026,
        "holidayLists": [
            {
                "holidayName": {"en": "Inverted Holiday", "ar": "عطلة معكوسة"},
                "holidayTypeId": ht_id,
                "startDate": "2026-05-10T00:00:00Z",
                "endDate": "2026-05-08T00:00:00Z" # 2 days BEFORE start!
            }
        ]
    }
}
r_inv = requests.post(f"{base_url}/api/companies/{c8}/holidaylist", json=p_inversion, headers=headers)
print("\n[DEFECT-20261103-11] Chronological Inversion POST status:", r_inv.status_code)
print("Response:", r_inv.text)

# 3. Test child holiday empty English name: holidayName.en == "" (DEFECT-20261103-10 / HC-DTO-21)
p_empty_child_name = {
    "shortCode": "HOLCHN1",
    "name": {"en": "Child Empty Name Test", "ar": "تجربة"},
    "year": 2026,
    "yearlyCalendar": {
        "year": 2026,
        "holidayLists": [
            {
                "holidayName": {"en": "", "ar": "عطلة بدون إنجليزي"},
                "holidayTypeId": ht_id,
                "startDate": "2026-05-10T00:00:00Z",
                "endDate": "2026-05-10T00:00:00Z"
            }
        ]
    }
}
r_chn = requests.post(f"{base_url}/api/companies/{c8}/holidaylist", json=p_empty_child_name, headers=headers)
print("\n[DEFECT-20261103-10] Child Holiday Empty Name POST status:", r_chn.status_code)
print("Response:", r_chn.text)

# 4. Test missing holidayTypeId: (DEFECT-20261103-13 / HC-DTO-23)
p_missing_ht = {
    "shortCode": "HOLMHT1",
    "name": {"en": "Missing Holiday Type Test", "ar": "تجربة"},
    "year": 2026,
    "yearlyCalendar": {
        "year": 2026,
        "holidayLists": [
            {
                "holidayName": {"en": "Valid Holiday", "ar": "عطلة"},
                "startDate": "2026-05-10T00:00:00Z",
                "endDate": "2026-05-10T00:00:00Z"
            }
        ]
    }
}
r_mht = requests.post(f"{base_url}/api/companies/{c8}/holidaylist", json=p_missing_ht, headers=headers)
print("\n[DEFECT-20261103-13] Missing holidayTypeId POST status:", r_mht.status_code)
print("Response:", r_mht.text)

