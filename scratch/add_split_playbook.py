# -*- coding: utf-8 -*-
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('CDWT_Manual_Testing_Playbook.md', 'r', encoding='utf-8') as f:
    text = f.read()

target = """### EXCEL LOGGING (`CompanyDefault_DTO_Validation_TestCases.xlsx`):
- **Col L (Manual Status):** `Failed`
- **Col M (Actual HTTP Code):** `500`
- **Col N (Actual Notes):** DEFECT-20261028-02: Active intervals on day off throw HTTP 500 crash.


================================================================================
# CATEGORY: 6. PATCH & IMMUTABILITY"""

new_test_cases = """### EXCEL LOGGING (`CompanyDefault_DTO_Validation_TestCases.xlsx`):
- **Col L (Manual Status):** `Failed`
- **Col M (Actual HTTP Code):** `500`
- **Col N (Actual Notes):** DEFECT-20261028-02: Active intervals on day off throw HTTP 500 crash.

---

## CDWT-DTO-54: Split Shift Active Day with Empty Intervals Array ([]) (POST & PATCH)

- **Category:** 5. Split WT
- **Priority:** P1 (High Functional / Crash)
- **Method & Route:** `POST /api/companies/3a247435-3cea-83ae-6a9f-6dda99f386a3/worktemplates/split`

### OPTION 1 (Swagger UI Steps):
1. Expand POST /api/companies/{companyId}/worktemplates/split
2. In companyId: 3a247435-3cea-83ae-6a9f-6dda99f386a3
3. In Request body, paste the JSON payload below (Day 1 has isWorkingDay: true with timeSlots: [])
4. Click Execute

### OPTION 2 (Postman / Direct Request Steps):
- **Method:** `POST`
- **Full URL:** `https://attendance2.dev.zoolwork.com/api/companies/3a247435-3cea-83ae-6a9f-6dda99f386a3/worktemplates/split`
- **Authorization:** `Bearer <valid-token>`
- **Headers:**
  - `Content-Type: application/json`
  - `__tenant: Attendance`
- **Request Body (JSON Payload):**
```json
{
  "templateName": {
    "en": "Split Shift Empty Interval Crash Test"
  },
  "shortCode": "SPL054",
  "totalWorkDurationInMinutes": 1920,
  "totalWorkingDays": 5,
  "totalDaysOff": 2,
  "splitTimeSlots": [
    {
      "dayEnum": 1,
      "isWorkingDay": true,
      "recurrenceOfMonth": [1, 2, 3, 4, 5],
      "workDurationInMinutes": 480,
      "timeSlots": []
    },
    {
      "dayEnum": 2,
      "isWorkingDay": true,
      "recurrenceOfMonth": [1, 2, 3, 4, 5],
      "workDurationInMinutes": 480,
      "timeSlots": [
        {"startTime": "08:00", "endTime": "12:00", "workDurationInMinutes": 240},
        {"startTime": "16:00", "endTime": "20:00", "workDurationInMinutes": 240}
      ]
    },
    {
      "dayEnum": 3,
      "isWorkingDay": true,
      "recurrenceOfMonth": [1, 2, 3, 4, 5],
      "workDurationInMinutes": 480,
      "timeSlots": [
        {"startTime": "08:00", "endTime": "12:00", "workDurationInMinutes": 240},
        {"startTime": "16:00", "endTime": "20:00", "workDurationInMinutes": 240}
      ]
    },
    {
      "dayEnum": 4,
      "isWorkingDay": true,
      "recurrenceOfMonth": [1, 2, 3, 4, 5],
      "workDurationInMinutes": 480,
      "timeSlots": [
        {"startTime": "08:00", "endTime": "12:00", "workDurationInMinutes": 240},
        {"startTime": "16:00", "endTime": "20:00", "workDurationInMinutes": 240}
      ]
    },
    {
      "dayEnum": 5,
      "isWorkingDay": true,
      "recurrenceOfMonth": [1, 2, 3, 4, 5],
      "workDurationInMinutes": 480,
      "timeSlots": [
        {"startTime": "08:00", "endTime": "12:00", "workDurationInMinutes": 240},
        {"startTime": "16:00", "endTime": "20:00", "workDurationInMinutes": 240}
      ]
    },
    {
      "dayEnum": 6,
      "isWorkingDay": false,
      "recurrenceOfMonth": [1, 2, 3, 4, 5],
      "workDurationInMinutes": 0,
      "timeSlots": []
    },
    {
      "dayEnum": 7,
      "isWorkingDay": false,
      "recurrenceOfMonth": [1, 2, 3, 4, 5],
      "workDurationInMinutes": 0,
      "timeSlots": []
    }
  ]
}
```

### EXPECTED RESULT:
- Expected: HTTP 400 Bad Request ("Active working day must contain time intervals.") | Actual DEV Bug: Throws unhandled HTTP 500 crash (DEFECT-20261102-18)

### EXCEL LOGGING (`CompanyDefault_DTO_Validation_TestCases.xlsx`):
- **Col L (Manual Status):** `Failed`
- **Col M (Actual HTTP Code):** `500`
- **Col N (Actual Notes):** DEFECT-20261102-18: Active day with empty intervals array crashes with HTTP 500 instead of HTTP 400.

---

## CDWT-DTO-55: Split Shift Half-Day Single Interval Configuration (POST & PATCH)

- **Category:** 5. Split WT
- **Priority:** P1 (High Business / Functional Gap)
- **Method & Route:** `POST /api/companies/3a247435-3cea-83ae-6a9f-6dda99f386a3/worktemplates/split`

### OPTION 1 (Swagger UI Steps):
1. Expand POST /api/companies/{companyId}/worktemplates/split
2. In companyId: 3a247435-3cea-83ae-6a9f-6dda99f386a3
3. In Request body, paste the JSON payload below (Day 6 Saturday is a half-day with 1 continuous interval 08:00-12:00)
4. Click Execute

### OPTION 2 (Postman / Direct Request Steps):
- **Method:** `POST`
- **Full URL:** `https://attendance2.dev.zoolwork.com/api/companies/3a247435-3cea-83ae-6a9f-6dda99f386a3/worktemplates/split`
- **Authorization:** `Bearer <valid-token>`
- **Headers:**
  - `Content-Type: application/json`
  - `__tenant: Attendance`
- **Request Body (JSON Payload):**
```json
{
  "templateName": {
    "en": "Split Shift with Saturday Half-Day"
  },
  "shortCode": "SPL055",
  "totalWorkDurationInMinutes": 2160,
  "totalWorkingDays": 6,
  "totalDaysOff": 1,
  "splitTimeSlots": [
    {
      "dayEnum": 1,
      "isWorkingDay": true,
      "recurrenceOfMonth": [1, 2, 3, 4, 5],
      "workDurationInMinutes": 480,
      "timeSlots": [
        {"startTime": "08:00", "endTime": "12:00", "workDurationInMinutes": 240},
        {"startTime": "16:00", "endTime": "20:00", "workDurationInMinutes": 240}
      ]
    },
    {
      "dayEnum": 2,
      "isWorkingDay": true,
      "recurrenceOfMonth": [1, 2, 3, 4, 5],
      "workDurationInMinutes": 480,
      "timeSlots": [
        {"startTime": "08:00", "endTime": "12:00", "workDurationInMinutes": 240},
        {"startTime": "16:00", "endTime": "20:00", "workDurationInMinutes": 240}
      ]
    },
    {
      "dayEnum": 3,
      "isWorkingDay": true,
      "recurrenceOfMonth": [1, 2, 3, 4, 5],
      "workDurationInMinutes": 480,
      "timeSlots": [
        {"startTime": "08:00", "endTime": "12:00", "workDurationInMinutes": 240},
        {"startTime": "16:00", "endTime": "20:00", "workDurationInMinutes": 240}
      ]
    },
    {
      "dayEnum": 4,
      "isWorkingDay": true,
      "recurrenceOfMonth": [1, 2, 3, 4, 5],
      "workDurationInMinutes": 480,
      "timeSlots": [
        {"startTime": "08:00", "endTime": "12:00", "workDurationInMinutes": 240},
        {"startTime": "16:00", "endTime": "20:00", "workDurationInMinutes": 240}
      ]
    },
    {
      "dayEnum": 5,
      "isWorkingDay": false,
      "recurrenceOfMonth": [1, 2, 3, 4, 5],
      "workDurationInMinutes": 0,
      "timeSlots": []
    },
    {
      "dayEnum": 6,
      "isWorkingDay": true,
      "recurrenceOfMonth": [1, 2, 3, 4, 5],
      "workDurationInMinutes": 240,
      "timeSlots": [
        {"startTime": "08:00", "endTime": "12:00", "workDurationInMinutes": 240}
      ]
    },
    {
      "dayEnum": 7,
      "isWorkingDay": true,
      "recurrenceOfMonth": [1, 2, 3, 4, 5],
      "workDurationInMinutes": 480,
      "timeSlots": [
        {"startTime": "08:00", "endTime": "12:00", "workDurationInMinutes": 240},
        {"startTime": "16:00", "endTime": "20:00", "workDurationInMinutes": 240}
      ]
    }
  ]
}
```

### EXPECTED RESULT:
- Expected Business Behavior: HTTP 200 OK (Half-day allowed with 1 interval) | Actual DEV Bug: HTTP 400 / 500 ("Split shift working days must contain at least 2 time intervals") (DEFECT-20261102-18)

### EXCEL LOGGING (`CompanyDefault_DTO_Validation_TestCases.xlsx`):
- **Col L (Manual Status):** `Failed`
- **Col M (Actual HTTP Code):** `400 / 500`
- **Col N (Actual Notes):** DEFECT-20261102-18: System blocks half-day single-interval shift on Saturday in Split Template.


================================================================================
# CATEGORY: 6. PATCH & IMMUTABILITY"""

if target in text and "CDWT-DTO-54" not in text:
    text = text.replace(target, new_test_cases)
    with open('CDWT_Manual_Testing_Playbook.md', 'w', encoding='utf-8') as f:
        f.write(text)
    print("SUCCESS: Added CDWT-DTO-54 and CDWT-DTO-55 to CDWT_Manual_Testing_Playbook.md!")
else:
    print("Target not found or already added!")

