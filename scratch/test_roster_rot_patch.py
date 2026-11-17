# -*- coding: utf-8 -*-
import json
import requests
import random
import string
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

BASE_URL = "https://attendance2.dev.zoolwork.com"
COMPANY_ID = "3a24e5e5-302e-91bd-feaa-b07979766dfe"  # Attendance 11
LOC_RIYADH = "3a24e666-59d9-a713-f782-12163167ddcd"
LOC_DAMMAM = "3a24e666-df63-3dc7-0ea7-02ec8be341e7"

with open("scratch/current_token.json", "r") as f:
    token_data = json.load(f)
token = token_data.get("token") or token_data.get("access_token")

headers = {
    "Authorization": f"Bearer {token}",
    "Content-Type": "application/json",
    "__tenant": "Attendance"
}

roster_id = "1ccd76ed-22d8-4987-a684-edf2255ab400"
rot_id = "c3b80ad3-4e09-4807-973c-ab5501e901da"

# Test DOC-B-01: Edit name, colour, timings
payload_b01 = {
    "templateName": {"en": "Updated Roster Name", "ar": "اسم محدث"},
    "colour": "#FA5252",
    "rosterTimeSlots": [
        {"dayEnum": "Sun", "isWorkingDay": True, "startTime": "08:00", "endTime": "16:00", "workDurationInMinutes": 480, "crossesMidnight": False},
        {"dayEnum": "Mon", "isWorkingDay": True, "startTime": "08:00", "endTime": "16:00", "workDurationInMinutes": 480, "crossesMidnight": False},
        {"dayEnum": "Tue", "isWorkingDay": True, "startTime": "08:00", "endTime": "16:00", "workDurationInMinutes": 480, "crossesMidnight": False},
        {"dayEnum": "Wed", "isWorkingDay": True, "startTime": "08:00", "endTime": "16:00", "workDurationInMinutes": 480, "crossesMidnight": False},
        {"dayEnum": "Thu", "isWorkingDay": True, "startTime": "08:00", "endTime": "16:00", "workDurationInMinutes": 480, "crossesMidnight": False},
        {"dayEnum": "Fri", "isWorkingDay": False, "startTime": "00:00", "endTime": "00:00", "workDurationInMinutes": 0, "crossesMidnight": False},
        {"dayEnum": "Sat", "isWorkingDay": False, "startTime": "00:00", "endTime": "00:00", "workDurationInMinutes": 0, "crossesMidnight": False}
    ]
}
r_b01 = requests.patch(f"{BASE_URL}/api/companies/{COMPANY_ID}/worktemplates/roster/{roster_id}?locationId={LOC_RIYADH}", headers=headers, json=payload_b01, verify=False)
print("DOC-B-01 status:", r_b01.status_code)
print("DOC-B-01 text:", r_b01.text)

# Test DOC-D-01: Edit rotation name and timings
payload_d01 = {
    "templateName": {"en": "Updated Rotation D01", "ar": "اسم مناوبة محدث"},
    "rotationTimeSlots": [
        {"dayEnum": "Sun", "isWorkingDay": True, "startTime": "09:00", "endTime": "17:00", "workDurationInMinutes": 480},
        {"dayEnum": "Mon", "isWorkingDay": True, "startTime": "09:00", "endTime": "17:00", "workDurationInMinutes": 480},
        {"dayEnum": "Tue", "isWorkingDay": True, "startTime": "09:00", "endTime": "17:00", "workDurationInMinutes": 480},
        {"dayEnum": "Wed", "isWorkingDay": True, "startTime": "09:00", "endTime": "17:00", "workDurationInMinutes": 480},
        {"dayEnum": "Thu", "isWorkingDay": True, "startTime": "09:00", "endTime": "17:00", "workDurationInMinutes": 480},
        {"dayEnum": "Fri", "isWorkingDay": False, "startTime": "00:00", "endTime": "00:00", "workDurationInMinutes": 0},
        {"dayEnum": "Sat", "isWorkingDay": False, "startTime": "00:00", "endTime": "00:00", "workDurationInMinutes": 0}
    ]
}
r_d01 = requests.patch(f"{BASE_URL}/api/companies/{COMPANY_ID}/worktemplates/rotation/{rot_id}?locationId={LOC_DAMMAM}", headers=headers, json=payload_d01, verify=False)
print("DOC-D-01 status:", r_d01.status_code)
print("DOC-D-01 text:", r_d01.text)

# Find an existing roster board or create one to test DOC-E-03
r_boards = requests.get(f"{BASE_URL}/api/companies/{COMPANY_ID}/roster-boards?locationId={LOC_RIYADH}", headers=headers, verify=False)
board_id = None
if r_boards.status_code == 200:
    boards = r_boards.json().get("rosterBoards", []) or r_boards.json().get("data", [])
    if boards:
        board_id = boards[0].get("id")
        print("Found existing board ID:", board_id)

if not board_id:
    # Create board
    b_payload = {
        "boardName": {"en": "Test Roster Board", "ar": "لوحة جدول"},
        "supervisor": {"name": "Supervisor Test", "email": "supervisor@test.com"},
        "publishingFrequency": "Weekly",
        "hasAreas": False
    }
    r_cb = requests.post(f"{BASE_URL}/api/companies/{COMPANY_ID}/roster-boards?locationId={LOC_RIYADH}", headers=headers, json=b_payload, verify=False)
    print("Create board status:", r_cb.status_code)
    if r_cb.status_code in [200, 201]:
        board_id = r_cb.json().get("id") or r_cb.json().get("data", {}).get("id")
        print("Created board ID:", board_id)

if board_id:
    shift_code = "SHF" + "".join(random.choices(string.digits, k=4))
    shift_payload = {
        "boardId": board_id,
        "shiftName": {"en": "Morning Shift E03", "ar": "وردية صباحية"},
        "code": shift_code,
        "colour": "#20C997",
        "totalWorkingDays": 5,
        "totalDaysOff": 2,
        "totalWorkDurationInMinutes": 2400,
        "rosterTimeSlots": [
            {"dayEnum": "Sun", "isWorkingDay": True, "startTime": "08:00", "endTime": "16:00", "workDurationInMinutes": 480, "crossesMidnight": False},
            {"dayEnum": "Mon", "isWorkingDay": True, "startTime": "08:00", "endTime": "16:00", "workDurationInMinutes": 480, "crossesMidnight": False},
            {"dayEnum": "Tue", "isWorkingDay": True, "startTime": "08:00", "endTime": "16:00", "workDurationInMinutes": 480, "crossesMidnight": False},
            {"dayEnum": "Wed", "isWorkingDay": True, "startTime": "08:00", "endTime": "16:00", "workDurationInMinutes": 480, "crossesMidnight": False},
            {"dayEnum": "Thu", "isWorkingDay": True, "startTime": "08:00", "endTime": "16:00", "workDurationInMinutes": 480, "crossesMidnight": False},
            {"dayEnum": "Fri", "isWorkingDay": False, "startTime": "00:00", "endTime": "00:00", "workDurationInMinutes": 0, "crossesMidnight": False},
            {"dayEnum": "Sat", "isWorkingDay": False, "startTime": "00:00", "endTime": "00:00", "workDurationInMinutes": 0, "crossesMidnight": False}
        ]
    }
    r_e03 = requests.post(f"{BASE_URL}/api/companies/{COMPANY_ID}/workplans/roster?locationId={LOC_RIYADH}", headers=headers, json=shift_payload, verify=False)
    print("DOC-E-03 status:", r_e03.status_code)
    print("DOC-E-03 text:", r_e03.text)
