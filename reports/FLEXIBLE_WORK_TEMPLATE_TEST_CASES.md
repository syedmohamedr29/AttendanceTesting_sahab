# Sahab ERP Attendance – Flexible Work Template Test Suite Specification & Execution Log

**Document Version:** `1.0`  
**Execution Date:** `2026-11-10`  
**Module:** Flexible Work Template (`TemplateType: 2`)  
**Target Location:** Location 2 (`3a24d646-b3cf-b1d4-61bb-1adf094b52fc`)  
**Total Scenarios:** `22` | **Passed:** `17` | **Failed:** `5`  
**Target Collection:** `Sahab.ERP.Attendance.WorkTemplates`  
**Visual Evidence:** [Evidence 56 (Flexible & Split Template Validation Bypasses & Transitions)](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_56_flexi_split_location_validation_bypasses_and_db_results.png)  

---

## 1. Module Overview & Technical Architecture

A **Flexible (Flexi) Work Template** (`TemplateType: 2`) eliminates fixed check-in/check-out timestamps and evaluates attendance based on completed duration quotas. Flexible templates operate in two distinct modes:
1. **Daily Flexible (`FlexibleType: 1`)** — Enforces a specific daily required work duration (e.g., 480 minutes per working day).
2. **Weekly Flexible (`FlexibleType: 2`)** — Enforces a cumulative weekly quota (e.g., 2,400 minutes across the working week) where employees can vary daily hours.

### Key Domain Properties:
- `templateType`: Integer `2` (Flexi).
- `flexibleType`: Integer `1` (Daily) or `2` (Weekly).
- `flexiTimeSlots`: Array of 7 weekday slots containing `dayEnum`, `isWorkingDay`, `workDurationInMinutes`, and `recurrenceOfMonth`.
- Does **not** include `startTime` or `endTime` properties in slots.

---

## 2. Test Execution Breakdown by Category

### 2.1 Positive POST (Creation of Daily & Weekly Flexi Shifts) (5 Scenarios)
| Test ID | Description | HTTP Method & Endpoint | Status | Result | Notes / Defect Caught |
| :--- | :--- | :--- | :---: | :---: | :--- |
| `FLX-POS-01` | Flexible Daily standard 5-day (480m/day, 2400m total) | `POST /worktemplates/flexi` | `200` | ✅ PASS | Flexible Daily standard 5-day (480m/day, 2400m total) |
| `FLX-POS-02` | Flexible Weekly required duration (2400m) | `POST /worktemplates/flexi` | `200` | ✅ PASS | Flexible Weekly required duration (2400m) |
| `FLX-POS-03` | Flexible 6-day schedule (2880m total) | `POST /worktemplates/flexi` | `200` | ✅ PASS | Flexible 6-day schedule (2880m total) |
| `FLX-POS-04` | Flexible 4-day schedule (1920m total) | `POST /worktemplates/flexi` | `200` | ✅ PASS | Flexible 4-day schedule (1920m total) |
| `FLX-POS-05` | Flexible India Timezone (Asia/Kolkata) | `POST /worktemplates/flexi` | `200` | ✅ PASS | Flexible India Timezone (Asia/Kolkata) |

### 2.2 Negative POST (Schema Guardrails & Bypasses) (10 Scenarios)
| Test ID | Description | HTTP Method & Endpoint | Status | Result | Notes / Defect Caught |
| :--- | :--- | :--- | :---: | :---: | :--- |
| `FLX-NEG-01` | Empty template name | `POST /worktemplates/flexi` | `400` | ✅ PASS | Empty template name |
| `FLX-NEG-02` | ShortCode length < 7 ('FLX01') | `POST /worktemplates/flexi` | `400` | ✅ PASS | ShortCode length < 7 ('FLX01') |
| `FLX-NEG-03` | Duplicate shortCode (FXD0001) | `POST /worktemplates/flexi` | `400` | ✅ PASS | Duplicate shortCode (FXD0001) |
| `FLX-NEG-04` | Invalid FlexibleType (999) | `POST /worktemplates/flexi` | `400` | ✅ PASS | Invalid FlexibleType (999) |
| `FLX-NEG-05` | Negative daily duration (-480m) | `POST /worktemplates/flexi` | `400` | ✅ PASS | Negative daily duration (-480m) |
| `FLX-NEG-06` | Working day with 0 minutes on Daily Flexi | `POST /worktemplates/flexi` | `400` | ✅ PASS | Working day with 0 minutes on Daily Flexi |
| `FLX-NEG-07` | Off-day with active duration (480m) | `POST /worktemplates/flexi` | `400` | ✅ PASS | Off-day with active duration (480m) |
| `FLX-NEG-08` | Invalid dayEnum (8) | `POST /worktemplates/flexi` | `400` | ✅ PASS | Invalid dayEnum (8) |
| `FLX-NEG-09` | Invalid recurrence index ([6]) | `POST /worktemplates/flexi` | `200` | ❌ FAIL | Invalid recurrence index ([6]) **[DEFECT-20261110-10]** |
| `FLX-NEG-10` | Duration sum mismatch (3000 vs 2400) | `POST /worktemplates/flexi` | `200` | ❌ FAIL | Duration sum mismatch (3000 vs 2400) **[DEFECT-20261110-11]** |

### 2.3 Positive PATCH (In-Place Location Mutation) (3 Scenarios)
| Test ID | Description | HTTP Method & Endpoint | Status | Result | Notes / Defect Caught |
| :--- | :--- | :--- | :---: | :---: | :--- |
| `FLX-PAT-01` | Update Flexible template name | `PATCH /worktemplates/flexi` | `200` | ✅ PASS | Update Flexible template name |
| `FLX-PAT-02` | Update daily duration to 540m (2700m total) | `PATCH /worktemplates/flexi` | `200` | ✅ PASS | Update daily duration to 540m (2700m total) |
| `FLX-PAT-03` | Update timezone to Asia/Dubai | `PATCH /worktemplates/flexi` | `200` | ✅ PASS | Update timezone to Asia/Dubai |

### 2.4 Negative PATCH (Immutability & Validation Gaps) (4 Scenarios)
| Test ID | Description | HTTP Method & Endpoint | Status | Result | Notes / Defect Caught |
| :--- | :--- | :--- | :---: | :---: | :--- |
| `FLX-PAT-04` | Attempt to alter shortCode in PATCH (Cit.Attendance:1107) | `PATCH /worktemplates/flexi` | `400` | ✅ PASS | Attempt to alter shortCode in PATCH (Cit.Attendance:1107) |
| `FLX-PAT-05` | Recurrence [6] in Flexible PATCH | `PATCH /worktemplates/flexi` | `200` | ❌ FAIL | Recurrence [6] in Flexible PATCH **[DEFECT-20261110-10]** |
| `FLX-PAT-06` | Duration mismatch in Flexible PATCH (3500 vs 2700) | `PATCH /worktemplates/flexi` | `200` | ❌ FAIL | Duration mismatch in Flexible PATCH (3500 vs 2700) **[DEFECT-20261110-11]** |
| `FLX-PAT-07` | Invalid timezone in Flexible PATCH | `PATCH /worktemplates/flexi` | `200` | ❌ FAIL | Invalid timezone in Flexible PATCH **[DEFECT-20261110-12]** |

---

## 3. Detailed Payload & Database Verification Log

#### Scenario `FLX-POS-01`: Flexible Daily standard 5-day (480m/day, 2400m total)
- **Endpoint:** `POST https://attendance2.dev.zoolwork.com/api/companies/3a249871-7a8d-dec5-2d72-47795dd2662d/worktemplates/flexi?locationId=3a24d646-b3cf-b1d4-61bb-1adf094b52fc`
- **Execution Result:** HTTP `200` -> **PASS**
- **MongoDB `_id`:** `7ecfbe95-8d3c-4612-a0cc-1454e9093a53`

**Request Payload:**
```json
{
  "templateName": {
    "en": "Flexible Location Shift FXD0001",
    "ar": "\u0648\u0631\u062f\u064a\u0629 \u0645\u0631\u0646\u0629 FXD0001"
  },
  "shortCode": "FXD0001",
  "templateType": 2,
  "flexibleType": 1,
  "totalWorkDurationInMinutes": 2400,
  "totalWorkingDays": 5,
  "totalDaysOff": 2,
  "timeZoneId": "Asia/Riyadh",
  "flexiTimeSlots": [
    {
      "dayEnum": 1,
      "isWorkingDay": true,
      "recurrenceOfMonth": [
        1,
        2,
        3,
        4,
        5
      ],
      "workDurationInMinutes": 480
    },
    {
      "dayEnum": 2,
      "isWorkingDay": true,
      "recurrenceOfMonth": [
        1,
        2,
        3,
        4,
        5
      ],
      "workDurationInMinutes": 480
    },
    {
      "dayEnum": 3,
      "isWorkingDay": true,
      "recurrenceOfMonth": [
        1,
        2,
        3,
        4,
        5
      ],
      "workDurationInMinutes": 480
    },
    {
      "dayEnum": 4,
      "isWorkingDay": true,
      "recurrenceOfMonth": [
        1,
        2,
        3,
        4,
        5
      ],
      "workDurationInMinutes": 480
    },
    {
      "dayEnum": 5,
      "isWorkingDay": true,
      "recurrenceOfMonth": [
        1,
        2,
        3,
        4,
        5
      ],
      "workDurationInMinutes": 480
    },
    {
      "dayEnum": 6,
      "isWorkingDay": false,
      "recurrenceOfMonth": [],
      "workDurationInMinutes": 0
    },
    {
      "dayEnum": 7,
      "isWorkingDay": false,
      "recurrenceOfMonth": [],
      "workDurationInMinutes": 0
    }
  ]
}
```
---

#### Scenario `FLX-POS-02`: Flexible Weekly required duration (2400m)
- **Endpoint:** `POST https://attendance2.dev.zoolwork.com/api/companies/3a249871-7a8d-dec5-2d72-47795dd2662d/worktemplates/flexi?locationId=3a24d646-b3cf-b1d4-61bb-1adf094b52fc`
- **Execution Result:** HTTP `200` -> **PASS**
- **MongoDB `_id`:** `99a81ce8-5f57-4fea-9652-07156040f051`

**Request Payload:**
```json
{
  "templateName": {
    "en": "Flexible Location Shift FXW0001",
    "ar": "\u0648\u0631\u062f\u064a\u0629 \u0645\u0631\u0646\u0629 FXW0001"
  },
  "shortCode": "FXW0001",
  "templateType": 2,
  "flexibleType": 2,
  "totalWorkDurationInMinutes": 2400,
  "totalWorkingDays": 5,
  "totalDaysOff": 2,
  "timeZoneId": "Asia/Riyadh",
  "flexiTimeSlots": [
    {
      "dayEnum": 1,
      "isWorkingDay": true,
      "recurrenceOfMonth": [
        1,
        2,
        3,
        4,
        5
      ],
      "workDurationInMinutes": 480
    },
    {
      "dayEnum": 2,
      "isWorkingDay": true,
      "recurrenceOfMonth": [
        1,
        2,
        3,
        4,
        5
      ],
      "workDurationInMinutes": 480
    },
    {
      "dayEnum": 3,
      "isWorkingDay": true,
      "recurrenceOfMonth": [
        1,
        2,
        3,
        4,
        5
      ],
      "workDurationInMinutes": 480
    },
    {
      "dayEnum": 4,
      "isWorkingDay": true,
      "recurrenceOfMonth": [
        1,
        2,
        3,
        4,
        5
      ],
      "workDurationInMinutes": 480
    },
    {
      "dayEnum": 5,
      "isWorkingDay": true,
      "recurrenceOfMonth": [
        1,
        2,
        3,
        4,
        5
      ],
      "workDurationInMinutes": 480
    },
    {
      "dayEnum": 6,
      "isWorkingDay": false,
      "recurrenceOfMonth": [],
      "workDurationInMinutes": 0
    },
    {
      "dayEnum": 7,
      "isWorkingDay": false,
      "recurrenceOfMonth": [],
      "workDurationInMinutes": 0
    }
  ]
}
```
---

#### Scenario `FLX-POS-03`: Flexible 6-day schedule (2880m total)
- **Endpoint:** `POST https://attendance2.dev.zoolwork.com/api/companies/3a249871-7a8d-dec5-2d72-47795dd2662d/worktemplates/flexi?locationId=3a24d646-b3cf-b1d4-61bb-1adf094b52fc`
- **Execution Result:** HTTP `200` -> **PASS**
- **MongoDB `_id`:** `68dab14c-9355-4f19-b553-118b5a70212b`

**Request Payload:**
```json
{
  "templateName": {
    "en": "Flexible Location Shift FXD0002",
    "ar": "\u0648\u0631\u062f\u064a\u0629 \u0645\u0631\u0646\u0629 FXD0002"
  },
  "shortCode": "FXD0002",
  "templateType": 2,
  "flexibleType": 1,
  "totalWorkDurationInMinutes": 2880,
  "totalWorkingDays": 6,
  "totalDaysOff": 1,
  "timeZoneId": "Asia/Riyadh",
  "flexiTimeSlots": [
    {
      "dayEnum": 1,
      "isWorkingDay": true,
      "recurrenceOfMonth": [
        1,
        2,
        3,
        4,
        5
      ],
      "workDurationInMinutes": 480
    },
    {
      "dayEnum": 2,
      "isWorkingDay": true,
      "recurrenceOfMonth": [
        1,
        2,
        3,
        4,
        5
      ],
      "workDurationInMinutes": 480
    },
    {
      "dayEnum": 3,
      "isWorkingDay": true,
      "recurrenceOfMonth": [
        1,
        2,
        3,
        4,
        5
      ],
      "workDurationInMinutes": 480
    },
    {
      "dayEnum": 4,
      "isWorkingDay": true,
      "recurrenceOfMonth": [
        1,
        2,
        3,
        4,
        5
      ],
      "workDurationInMinutes": 480
    },
    {
      "dayEnum": 5,
      "isWorkingDay": true,
      "recurrenceOfMonth": [
        1,
        2,
        3,
        4,
        5
      ],
      "workDurationInMinutes": 480
    },
    {
      "dayEnum": 6,
      "isWorkingDay": true,
      "recurrenceOfMonth": [
        1,
        2,
        3,
        4,
        5
      ],
      "workDurationInMinutes": 480
    },
    {
      "dayEnum": 7,
      "isWorkingDay": false,
      "recurrenceOfMonth": [],
      "workDurationInMinutes": 0
    }
  ]
}
```
---

#### Scenario `FLX-POS-04`: Flexible 4-day schedule (1920m total)
- **Endpoint:** `POST https://attendance2.dev.zoolwork.com/api/companies/3a249871-7a8d-dec5-2d72-47795dd2662d/worktemplates/flexi?locationId=3a24d646-b3cf-b1d4-61bb-1adf094b52fc`
- **Execution Result:** HTTP `200` -> **PASS**
- **MongoDB `_id`:** `7562cf81-8eae-4c28-b59c-8ba893739848`

**Request Payload:**
```json
{
  "templateName": {
    "en": "Flexible Location Shift FXD0003",
    "ar": "\u0648\u0631\u062f\u064a\u0629 \u0645\u0631\u0646\u0629 FXD0003"
  },
  "shortCode": "FXD0003",
  "templateType": 2,
  "flexibleType": 1,
  "totalWorkDurationInMinutes": 1920,
  "totalWorkingDays": 4,
  "totalDaysOff": 3,
  "timeZoneId": "Asia/Riyadh",
  "flexiTimeSlots": [
    {
      "dayEnum": 1,
      "isWorkingDay": false,
      "recurrenceOfMonth": [],
      "workDurationInMinutes": 0
    },
    {
      "dayEnum": 2,
      "isWorkingDay": true,
      "recurrenceOfMonth": [
        1,
        2,
        3,
        4,
        5
      ],
      "workDurationInMinutes": 480
    },
    {
      "dayEnum": 3,
      "isWorkingDay": true,
      "recurrenceOfMonth": [
        1,
        2,
        3,
        4,
        5
      ],
      "workDurationInMinutes": 480
    },
    {
      "dayEnum": 4,
      "isWorkingDay": true,
      "recurrenceOfMonth": [
        1,
        2,
        3,
        4,
        5
      ],
      "workDurationInMinutes": 480
    },
    {
      "dayEnum": 5,
      "isWorkingDay": true,
      "recurrenceOfMonth": [
        1,
        2,
        3,
        4,
        5
      ],
      "workDurationInMinutes": 480
    },
    {
      "dayEnum": 6,
      "isWorkingDay": false,
      "recurrenceOfMonth": [],
      "workDurationInMinutes": 0
    },
    {
      "dayEnum": 7,
      "isWorkingDay": false,
      "recurrenceOfMonth": [],
      "workDurationInMinutes": 0
    }
  ]
}
```
---

#### Scenario `FLX-POS-05`: Flexible India Timezone (Asia/Kolkata)
- **Endpoint:** `POST https://attendance2.dev.zoolwork.com/api/companies/3a249871-7a8d-dec5-2d72-47795dd2662d/worktemplates/flexi?locationId=3a24d646-b3cf-b1d4-61bb-1adf094b52fc`
- **Execution Result:** HTTP `200` -> **PASS**
- **MongoDB `_id`:** `0ae8a4ce-d405-4615-8ff1-9a2b9c2729bf`

**Request Payload:**
```json
{
  "templateName": {
    "en": "Flexible Location Shift FXD0004",
    "ar": "\u0648\u0631\u062f\u064a\u0629 \u0645\u0631\u0646\u0629 FXD0004"
  },
  "shortCode": "FXD0004",
  "templateType": 2,
  "flexibleType": 1,
  "totalWorkDurationInMinutes": 2400,
  "totalWorkingDays": 5,
  "totalDaysOff": 2,
  "timeZoneId": "Asia/Kolkata",
  "flexiTimeSlots": [
    {
      "dayEnum": 1,
      "isWorkingDay": true,
      "recurrenceOfMonth": [
        1,
        2,
        3,
        4,
        5
      ],
      "workDurationInMinutes": 480
    },
    {
      "dayEnum": 2,
      "isWorkingDay": true,
      "recurrenceOfMonth": [
        1,
        2,
        3,
        4,
        5
      ],
      "workDurationInMinutes": 480
    },
    {
      "dayEnum": 3,
      "isWorkingDay": true,
      "recurrenceOfMonth": [
        1,
        2,
        3,
        4,
        5
      ],
      "workDurationInMinutes": 480
    },
    {
      "dayEnum": 4,
      "isWorkingDay": true,
      "recurrenceOfMonth": [
        1,
        2,
        3,
        4,
        5
      ],
      "workDurationInMinutes": 480
    },
    {
      "dayEnum": 5,
      "isWorkingDay": true,
      "recurrenceOfMonth": [
        1,
        2,
        3,
        4,
        5
      ],
      "workDurationInMinutes": 480
    },
    {
      "dayEnum": 6,
      "isWorkingDay": false,
      "recurrenceOfMonth": [],
      "workDurationInMinutes": 0
    },
    {
      "dayEnum": 7,
      "isWorkingDay": false,
      "recurrenceOfMonth": [],
      "workDurationInMinutes": 0
    }
  ]
}
```
---

#### Scenario `FLX-NEG-01`: Empty template name
- **Endpoint:** `POST https://attendance2.dev.zoolwork.com/api/companies/3a249871-7a8d-dec5-2d72-47795dd2662d/worktemplates/flexi?locationId=3a24d646-b3cf-b1d4-61bb-1adf094b52fc`
- **Execution Result:** HTTP `400` -> **PASS**
- **API Error:** `Cit.Attendance:Validation` | `An English template name is required.`

**Request Payload:**
```json
{
  "templateName": {
    "en": "",
    "ar": ""
  },
  "shortCode": "FXDNEG1",
  "templateType": 2,
  "flexibleType": 1,
  "totalWorkDurationInMinutes": 2400,
  "totalWorkingDays": 5,
  "totalDaysOff": 2,
  "timeZoneId": "Asia/Riyadh",
  "flexiTimeSlots": [
    {
      "dayEnum": 1,
      "isWorkingDay": true,
      "recurrenceOfMonth": [
        1,
        2,
        3,
        4,
        5
      ],
      "workDurationInMinutes": 480
    },
    {
      "dayEnum": 2,
      "isWorkingDay": true,
      "recurrenceOfMonth": [
        1,
        2,
        3,
        4,
        5
      ],
      "workDurationInMinutes": 480
    },
    {
      "dayEnum": 3,
      "isWorkingDay": true,
      "recurrenceOfMonth": [
        1,
        2,
        3,
        4,
        5
      ],
      "workDurationInMinutes": 480
    },
    {
      "dayEnum": 4,
      "isWorkingDay": true,
      "recurrenceOfMonth": [
        1,
        2,
        3,
        4,
        5
      ],
      "workDurationInMinutes": 480
    },
    {
      "dayEnum": 5,
      "isWorkingDay": true,
      "recurrenceOfMonth": [
        1,
        2,
        3,
        4,
        5
      ],
      "workDurationInMinutes": 480
    },
    {
      "dayEnum": 6,
      "isWorkingDay": false,
      "recurrenceOfMonth": [],
      "workDurationInMinutes": 0
    },
    {
      "dayEnum": 7,
      "isWorkingDay": false,
      "recurrenceOfMonth": [],
      "workDurationInMinutes": 0
    }
  ]
}
```
---

#### Scenario `FLX-NEG-02`: ShortCode length < 7 ('FLX01')
- **Endpoint:** `POST https://attendance2.dev.zoolwork.com/api/companies/3a249871-7a8d-dec5-2d72-47795dd2662d/worktemplates/flexi?locationId=3a24d646-b3cf-b1d4-61bb-1adf094b52fc`
- **Execution Result:** HTTP `400` -> **PASS**
- **API Error:** `Cit.Attendance:Validation` | `ShortCode must be exactly 7 letters or digits.`

**Request Payload:**
```json
{
  "templateName": {
    "en": "Flexible Location Shift FLX01",
    "ar": "\u0648\u0631\u062f\u064a\u0629 \u0645\u0631\u0646\u0629 FLX01"
  },
  "shortCode": "FLX01",
  "templateType": 2,
  "flexibleType": 1,
  "totalWorkDurationInMinutes": 2400,
  "totalWorkingDays": 5,
  "totalDaysOff": 2,
  "timeZoneId": "Asia/Riyadh",
  "flexiTimeSlots": [
    {
      "dayEnum": 1,
      "isWorkingDay": true,
      "recurrenceOfMonth": [
        1,
        2,
        3,
        4,
        5
      ],
      "workDurationInMinutes": 480
    },
    {
      "dayEnum": 2,
      "isWorkingDay": true,
      "recurrenceOfMonth": [
        1,
        2,
        3,
        4,
        5
      ],
      "workDurationInMinutes": 480
    },
    {
      "dayEnum": 3,
      "isWorkingDay": true,
      "recurrenceOfMonth": [
        1,
        2,
        3,
        4,
        5
      ],
      "workDurationInMinutes": 480
    },
    {
      "dayEnum": 4,
      "isWorkingDay": true,
      "recurrenceOfMonth": [
        1,
        2,
        3,
        4,
        5
      ],
      "workDurationInMinutes": 480
    },
    {
      "dayEnum": 5,
      "isWorkingDay": true,
      "recurrenceOfMonth": [
        1,
        2,
        3,
        4,
        5
      ],
      "workDurationInMinutes": 480
    },
    {
      "dayEnum": 6,
      "isWorkingDay": false,
      "recurrenceOfMonth": [],
      "workDurationInMinutes": 0
    },
    {
      "dayEnum": 7,
      "isWorkingDay": false,
      "recurrenceOfMonth": [],
      "workDurationInMinutes": 0
    }
  ]
}
```
---

#### Scenario `FLX-NEG-03`: Duplicate shortCode (FXD0001)
- **Endpoint:** `POST https://attendance2.dev.zoolwork.com/api/companies/3a249871-7a8d-dec5-2d72-47795dd2662d/worktemplates/flexi?locationId=3a24d646-b3cf-b1d4-61bb-1adf094b52fc`
- **Execution Result:** HTTP `400` -> **PASS**
- **API Error:** `Cit.Attendance:1106` | `This short code is already used by another work template in this company. Choose a different code.`

**Request Payload:**
```json
{
  "templateName": {
    "en": "Flexible Location Shift FXD0001",
    "ar": "\u0648\u0631\u062f\u064a\u0629 \u0645\u0631\u0646\u0629 FXD0001"
  },
  "shortCode": "FXD0001",
  "templateType": 2,
  "flexibleType": 1,
  "totalWorkDurationInMinutes": 2400,
  "totalWorkingDays": 5,
  "totalDaysOff": 2,
  "timeZoneId": "Asia/Riyadh",
  "flexiTimeSlots": [
    {
      "dayEnum": 1,
      "isWorkingDay": true,
      "recurrenceOfMonth": [
        1,
        2,
        3,
        4,
        5
      ],
      "workDurationInMinutes": 480
    },
    {
      "dayEnum": 2,
      "isWorkingDay": true,
      "recurrenceOfMonth": [
        1,
        2,
        3,
        4,
        5
      ],
      "workDurationInMinutes": 480
    },
    {
      "dayEnum": 3,
      "isWorkingDay": true,
      "recurrenceOfMonth": [
        1,
        2,
        3,
        4,
        5
      ],
      "workDurationInMinutes": 480
    },
    {
      "dayEnum": 4,
      "isWorkingDay": true,
      "recurrenceOfMonth": [
        1,
        2,
        3,
        4,
        5
      ],
      "workDurationInMinutes": 480
    },
    {
      "dayEnum": 5,
      "isWorkingDay": true,
      "recurrenceOfMonth": [
        1,
        2,
        3,
        4,
        5
      ],
      "workDurationInMinutes": 480
    },
    {
      "dayEnum": 6,
      "isWorkingDay": false,
      "recurrenceOfMonth": [],
      "workDurationInMinutes": 0
    },
    {
      "dayEnum": 7,
      "isWorkingDay": false,
      "recurrenceOfMonth": [],
      "workDurationInMinutes": 0
    }
  ]
}
```
---

#### Scenario `FLX-NEG-04`: Invalid FlexibleType (999)
- **Endpoint:** `POST https://attendance2.dev.zoolwork.com/api/companies/3a249871-7a8d-dec5-2d72-47795dd2662d/worktemplates/flexi?locationId=3a24d646-b3cf-b1d4-61bb-1adf094b52fc`
- **Execution Result:** HTTP `400` -> **PASS**
- **API Error:** `Cit.Attendance:Validation` | `Flexible type must be Daily or Weekly.`

**Request Payload:**
```json
{
  "templateName": {
    "en": "Flexible Location Shift FXDNEG4",
    "ar": "\u0648\u0631\u062f\u064a\u0629 \u0645\u0631\u0646\u0629 FXDNEG4"
  },
  "shortCode": "FXDNEG4",
  "templateType": 2,
  "flexibleType": 999,
  "totalWorkDurationInMinutes": 2400,
  "totalWorkingDays": 5,
  "totalDaysOff": 2,
  "timeZoneId": "Asia/Riyadh",
  "flexiTimeSlots": [
    {
      "dayEnum": 1,
      "isWorkingDay": true,
      "recurrenceOfMonth": [
        1,
        2,
        3,
        4,
        5
      ],
      "workDurationInMinutes": 480
    },
    {
      "dayEnum": 2,
      "isWorkingDay": true,
      "recurrenceOfMonth": [
        1,
        2,
        3,
        4,
        5
      ],
      "workDurationInMinutes": 480
    },
    {
      "dayEnum": 3,
      "isWorkingDay": true,
      "recurrenceOfMonth": [
        1,
        2,
        3,
        4,
        5
      ],
      "workDurationInMinutes": 480
    },
    {
      "dayEnum": 4,
      "isWorkingDay": true,
      "recurrenceOfMonth": [
        1,
        2,
        3,
        4,
        5
      ],
      "workDurationInMinutes": 480
    },
    {
      "dayEnum": 5,
      "isWorkingDay": true,
      "recurrenceOfMonth": [
        1,
        2,
        3,
        4,
        5
      ],
      "workDurationInMinutes": 480
    },
    {
      "dayEnum": 6,
      "isWorkingDay": false,
      "recurrenceOfMonth": [],
      "workDurationInMinutes": 0
    },
    {
      "dayEnum": 7,
      "isWorkingDay": false,
      "recurrenceOfMonth": [],
      "workDurationInMinutes": 0
    }
  ]
}
```
---

#### Scenario `FLX-NEG-05`: Negative daily duration (-480m)
- **Endpoint:** `POST https://attendance2.dev.zoolwork.com/api/companies/3a249871-7a8d-dec5-2d72-47795dd2662d/worktemplates/flexi?locationId=3a24d646-b3cf-b1d4-61bb-1adf094b52fc`
- **Execution Result:** HTTP `400` -> **PASS**
- **API Error:** `Cit.Attendance:Validation` | `A day's work duration cannot be negative. A working day's work duration must be greater than 0 minutes.`

**Request Payload:**
```json
{
  "templateName": {
    "en": "Flexible Location Shift FXDNEG5",
    "ar": "\u0648\u0631\u062f\u064a\u0629 \u0645\u0631\u0646\u0629 FXDNEG5"
  },
  "shortCode": "FXDNEG5",
  "templateType": 2,
  "flexibleType": 1,
  "totalWorkDurationInMinutes": 2400,
  "totalWorkingDays": 5,
  "totalDaysOff": 2,
  "timeZoneId": "Asia/Riyadh",
  "flexiTimeSlots": [
    {
      "dayEnum": 1,
      "isWorkingDay": true,
      "recurrenceOfMonth": [
        1,
        2,
        3,
        4,
        5
      ],
      "workDurationInMinutes": -480
    },
    {
      "dayEnum": 2,
      "isWorkingDay": true,
      "recurrenceOfMonth": [
        1,
        2,
        3,
        4,
        5
      ],
      "workDurationInMinutes": 480
    },
    {
      "dayEnum": 3,
      "isWorkingDay": true,
      "recurrenceOfMonth": [
        1,
        2,
        3,
        4,
        5
      ],
      "workDurationInMinutes": 480
    },
    {
      "dayEnum": 4,
      "isWorkingDay": true,
      "recurrenceOfMonth": [
        1,
        2,
        3,
        4,
        5
      ],
      "workDurationInMinutes": 480
    },
    {
      "dayEnum": 5,
      "isWorkingDay": true,
      "recurrenceOfMonth": [
        1,
        2,
        3,
        4,
        5
      ],
      "workDurationInMinutes": 480
    },
    {
      "dayEnum": 6,
      "isWorkingDay": false,
      "recurrenceOfMonth": [],
      "workDurationInMinutes": 0
    },
    {
      "dayEnum": 7,
      "isWorkingDay": false,
      "recurrenceOfMonth": [],
      "workDurationInMinutes": 0
    }
  ]
}
```
---

#### Scenario `FLX-NEG-06`: Working day with 0 minutes on Daily Flexi
- **Endpoint:** `POST https://attendance2.dev.zoolwork.com/api/companies/3a249871-7a8d-dec5-2d72-47795dd2662d/worktemplates/flexi?locationId=3a24d646-b3cf-b1d4-61bb-1adf094b52fc`
- **Execution Result:** HTTP `400` -> **PASS**
- **API Error:** `Cit.Attendance:Validation` | `A working day's work duration must be greater than 0 minutes.`

**Request Payload:**
```json
{
  "templateName": {
    "en": "Flexible Location Shift FXDNEG6",
    "ar": "\u0648\u0631\u062f\u064a\u0629 \u0645\u0631\u0646\u0629 FXDNEG6"
  },
  "shortCode": "FXDNEG6",
  "templateType": 2,
  "flexibleType": 1,
  "totalWorkDurationInMinutes": 2400,
  "totalWorkingDays": 5,
  "totalDaysOff": 2,
  "timeZoneId": "Asia/Riyadh",
  "flexiTimeSlots": [
    {
      "dayEnum": 1,
      "isWorkingDay": true,
      "recurrenceOfMonth": [
        1,
        2,
        3,
        4,
        5
      ],
      "workDurationInMinutes": 0
    },
    {
      "dayEnum": 2,
      "isWorkingDay": true,
      "recurrenceOfMonth": [
        1,
        2,
        3,
        4,
        5
      ],
      "workDurationInMinutes": 480
    },
    {
      "dayEnum": 3,
      "isWorkingDay": true,
      "recurrenceOfMonth": [
        1,
        2,
        3,
        4,
        5
      ],
      "workDurationInMinutes": 480
    },
    {
      "dayEnum": 4,
      "isWorkingDay": true,
      "recurrenceOfMonth": [
        1,
        2,
        3,
        4,
        5
      ],
      "workDurationInMinutes": 480
    },
    {
      "dayEnum": 5,
      "isWorkingDay": true,
      "recurrenceOfMonth": [
        1,
        2,
        3,
        4,
        5
      ],
      "workDurationInMinutes": 480
    },
    {
      "dayEnum": 6,
      "isWorkingDay": false,
      "recurrenceOfMonth": [],
      "workDurationInMinutes": 0
    },
    {
      "dayEnum": 7,
      "isWorkingDay": false,
      "recurrenceOfMonth": [],
      "workDurationInMinutes": 0
    }
  ]
}
```
---

#### Scenario `FLX-NEG-07`: Off-day with active duration (480m)
- **Endpoint:** `POST https://attendance2.dev.zoolwork.com/api/companies/3a249871-7a8d-dec5-2d72-47795dd2662d/worktemplates/flexi?locationId=3a24d646-b3cf-b1d4-61bb-1adf094b52fc`
- **Execution Result:** HTTP `400` -> **PASS**
- **API Error:** `Cit.Attendance:Validation` | `A day off cannot have a work duration, times or intervals.`

**Request Payload:**
```json
{
  "templateName": {
    "en": "Flexible Location Shift FXDNEG7",
    "ar": "\u0648\u0631\u062f\u064a\u0629 \u0645\u0631\u0646\u0629 FXDNEG7"
  },
  "shortCode": "FXDNEG7",
  "templateType": 2,
  "flexibleType": 1,
  "totalWorkDurationInMinutes": 2400,
  "totalWorkingDays": 5,
  "totalDaysOff": 2,
  "timeZoneId": "Asia/Riyadh",
  "flexiTimeSlots": [
    {
      "dayEnum": 1,
      "isWorkingDay": true,
      "recurrenceOfMonth": [
        1,
        2,
        3,
        4,
        5
      ],
      "workDurationInMinutes": 480
    },
    {
      "dayEnum": 2,
      "isWorkingDay": true,
      "recurrenceOfMonth": [
        1,
        2,
        3,
        4,
        5
      ],
      "workDurationInMinutes": 480
    },
    {
      "dayEnum": 3,
      "isWorkingDay": true,
      "recurrenceOfMonth": [
        1,
        2,
        3,
        4,
        5
      ],
      "workDurationInMinutes": 480
    },
    {
      "dayEnum": 4,
      "isWorkingDay": true,
      "recurrenceOfMonth": [
        1,
        2,
        3,
        4,
        5
      ],
      "workDurationInMinutes": 480
    },
    {
      "dayEnum": 5,
      "isWorkingDay": true,
      "recurrenceOfMonth": [
        1,
        2,
        3,
        4,
        5
      ],
      "workDurationInMinutes": 480
    },
    {
      "dayEnum": 6,
      "isWorkingDay": false,
      "recurrenceOfMonth": [],
      "workDurationInMinutes": 0
    },
    {
      "dayEnum": 7,
      "isWorkingDay": false,
      "recurrenceOfMonth": [],
      "workDurationInMinutes": 480
    }
  ]
}
```
---

#### Scenario `FLX-NEG-08`: Invalid dayEnum (8)
- **Endpoint:** `POST https://attendance2.dev.zoolwork.com/api/companies/3a249871-7a8d-dec5-2d72-47795dd2662d/worktemplates/flexi?locationId=3a24d646-b3cf-b1d4-61bb-1adf094b52fc`
- **Execution Result:** HTTP `400` -> **PASS**
- **API Error:** `Cit.Attendance:Validation` | `All 7 days of the week must be defined, each day once.`

**Request Payload:**
```json
{
  "templateName": {
    "en": "Flexible Location Shift FXDNEG8",
    "ar": "\u0648\u0631\u062f\u064a\u0629 \u0645\u0631\u0646\u0629 FXDNEG8"
  },
  "shortCode": "FXDNEG8",
  "templateType": 2,
  "flexibleType": 1,
  "totalWorkDurationInMinutes": 2400,
  "totalWorkingDays": 5,
  "totalDaysOff": 2,
  "timeZoneId": "Asia/Riyadh",
  "flexiTimeSlots": [
    {
      "dayEnum": 8,
      "isWorkingDay": true,
      "recurrenceOfMonth": [
        1,
        2,
        3,
        4,
        5
      ],
      "workDurationInMinutes": 480
    },
    {
      "dayEnum": 2,
      "isWorkingDay": true,
      "recurrenceOfMonth": [
        1,
        2,
        3,
        4,
        5
      ],
      "workDurationInMinutes": 480
    },
    {
      "dayEnum": 3,
      "isWorkingDay": true,
      "recurrenceOfMonth": [
        1,
        2,
        3,
        4,
        5
      ],
      "workDurationInMinutes": 480
    },
    {
      "dayEnum": 4,
      "isWorkingDay": true,
      "recurrenceOfMonth": [
        1,
        2,
        3,
        4,
        5
      ],
      "workDurationInMinutes": 480
    },
    {
      "dayEnum": 5,
      "isWorkingDay": true,
      "recurrenceOfMonth": [
        1,
        2,
        3,
        4,
        5
      ],
      "workDurationInMinutes": 480
    },
    {
      "dayEnum": 6,
      "isWorkingDay": false,
      "recurrenceOfMonth": [],
      "workDurationInMinutes": 0
    },
    {
      "dayEnum": 7,
      "isWorkingDay": false,
      "recurrenceOfMonth": [],
      "workDurationInMinutes": 0
    }
  ]
}
```
---

#### Scenario `FLX-NEG-09`: Invalid recurrence index ([6])
- **Endpoint:** `POST https://attendance2.dev.zoolwork.com/api/companies/3a249871-7a8d-dec5-2d72-47795dd2662d/worktemplates/flexi?locationId=3a24d646-b3cf-b1d4-61bb-1adf094b52fc`
- **Execution Result:** HTTP `200` -> **FAIL**
- **MongoDB `_id`:** `0ee23f7d-aa83-493b-af79-93c99c2f7c9d`

**Request Payload:**
```json
{
  "templateName": {
    "en": "Flexible Location Shift FXDNEG9",
    "ar": "\u0648\u0631\u062f\u064a\u0629 \u0645\u0631\u0646\u0629 FXDNEG9"
  },
  "shortCode": "FXDNEG9",
  "templateType": 2,
  "flexibleType": 1,
  "totalWorkDurationInMinutes": 2400,
  "totalWorkingDays": 5,
  "totalDaysOff": 2,
  "timeZoneId": "Asia/Riyadh",
  "flexiTimeSlots": [
    {
      "dayEnum": 1,
      "isWorkingDay": true,
      "recurrenceOfMonth": [
        6
      ],
      "workDurationInMinutes": 480
    },
    {
      "dayEnum": 2,
      "isWorkingDay": true,
      "recurrenceOfMonth": [
        1,
        2,
        3,
        4,
        5
      ],
      "workDurationInMinutes": 480
    },
    {
      "dayEnum": 3,
      "isWorkingDay": true,
      "recurrenceOfMonth": [
        1,
        2,
        3,
        4,
        5
      ],
      "workDurationInMinutes": 480
    },
    {
      "dayEnum": 4,
      "isWorkingDay": true,
      "recurrenceOfMonth": [
        1,
        2,
        3,
        4,
        5
      ],
      "workDurationInMinutes": 480
    },
    {
      "dayEnum": 5,
      "isWorkingDay": true,
      "recurrenceOfMonth": [
        1,
        2,
        3,
        4,
        5
      ],
      "workDurationInMinutes": 480
    },
    {
      "dayEnum": 6,
      "isWorkingDay": false,
      "recurrenceOfMonth": [],
      "workDurationInMinutes": 0
    },
    {
      "dayEnum": 7,
      "isWorkingDay": false,
      "recurrenceOfMonth": [],
      "workDurationInMinutes": 0
    }
  ]
}
```
---

#### Scenario `FLX-NEG-10`: Duration sum mismatch (3000 vs 2400)
- **Endpoint:** `POST https://attendance2.dev.zoolwork.com/api/companies/3a249871-7a8d-dec5-2d72-47795dd2662d/worktemplates/flexi?locationId=3a24d646-b3cf-b1d4-61bb-1adf094b52fc`
- **Execution Result:** HTTP `200` -> **FAIL**
- **MongoDB `_id`:** `96a20f25-47fb-496a-b595-0259aedba8c5`

**Request Payload:**
```json
{
  "templateName": {
    "en": "Flexible Location Shift FXDNE10",
    "ar": "\u0648\u0631\u062f\u064a\u0629 \u0645\u0631\u0646\u0629 FXDNE10"
  },
  "shortCode": "FXDNE10",
  "templateType": 2,
  "flexibleType": 1,
  "totalWorkDurationInMinutes": 3000,
  "totalWorkingDays": 5,
  "totalDaysOff": 2,
  "timeZoneId": "Asia/Riyadh",
  "flexiTimeSlots": [
    {
      "dayEnum": 1,
      "isWorkingDay": true,
      "recurrenceOfMonth": [
        1,
        2,
        3,
        4,
        5
      ],
      "workDurationInMinutes": 480
    },
    {
      "dayEnum": 2,
      "isWorkingDay": true,
      "recurrenceOfMonth": [
        1,
        2,
        3,
        4,
        5
      ],
      "workDurationInMinutes": 480
    },
    {
      "dayEnum": 3,
      "isWorkingDay": true,
      "recurrenceOfMonth": [
        1,
        2,
        3,
        4,
        5
      ],
      "workDurationInMinutes": 480
    },
    {
      "dayEnum": 4,
      "isWorkingDay": true,
      "recurrenceOfMonth": [
        1,
        2,
        3,
        4,
        5
      ],
      "workDurationInMinutes": 480
    },
    {
      "dayEnum": 5,
      "isWorkingDay": true,
      "recurrenceOfMonth": [
        1,
        2,
        3,
        4,
        5
      ],
      "workDurationInMinutes": 480
    },
    {
      "dayEnum": 6,
      "isWorkingDay": false,
      "recurrenceOfMonth": [],
      "workDurationInMinutes": 0
    },
    {
      "dayEnum": 7,
      "isWorkingDay": false,
      "recurrenceOfMonth": [],
      "workDurationInMinutes": 0
    }
  ]
}
```
---

#### Scenario `FLX-PAT-01`: Update Flexible template name
- **Endpoint:** `PATCH https://attendance2.dev.zoolwork.com/api/companies/3a249871-7a8d-dec5-2d72-47795dd2662d/worktemplates/flexi/7ecfbe95-8d3c-4612-a0cc-1454e9093a53?locationId=3a24d646-b3cf-b1d4-61bb-1adf094b52fc`
- **Execution Result:** HTTP `200` -> **PASS**
- **MongoDB `_id`:** `7ecfbe95-8d3c-4612-a0cc-1454e9093a53`

**Request Payload:**
```json
{
  "templateName": {
    "en": "Flexible Location Shift Updated",
    "ar": "\u0648\u0631\u062f\u064a\u0629 \u0645\u0631\u0646\u0629 \u0645\u062d\u062f\u062b\u0629"
  },
  "shortCode": "FXD0001",
  "templateType": 2,
  "flexibleType": 1,
  "totalWorkDurationInMinutes": 2400,
  "totalWorkingDays": 5,
  "totalDaysOff": 2,
  "timeZoneId": "Asia/Riyadh",
  "flexiTimeSlots": [
    {
      "dayEnum": 1,
      "isWorkingDay": true,
      "recurrenceOfMonth": [
        1,
        2,
        3,
        4,
        5
      ],
      "workDurationInMinutes": 480
    },
    {
      "dayEnum": 2,
      "isWorkingDay": true,
      "recurrenceOfMonth": [
        1,
        2,
        3,
        4,
        5
      ],
      "workDurationInMinutes": 480
    },
    {
      "dayEnum": 3,
      "isWorkingDay": true,
      "recurrenceOfMonth": [
        1,
        2,
        3,
        4,
        5
      ],
      "workDurationInMinutes": 480
    },
    {
      "dayEnum": 4,
      "isWorkingDay": true,
      "recurrenceOfMonth": [
        1,
        2,
        3,
        4,
        5
      ],
      "workDurationInMinutes": 480
    },
    {
      "dayEnum": 5,
      "isWorkingDay": true,
      "recurrenceOfMonth": [
        1,
        2,
        3,
        4,
        5
      ],
      "workDurationInMinutes": 480
    },
    {
      "dayEnum": 6,
      "isWorkingDay": false,
      "recurrenceOfMonth": [],
      "workDurationInMinutes": 0
    },
    {
      "dayEnum": 7,
      "isWorkingDay": false,
      "recurrenceOfMonth": [],
      "workDurationInMinutes": 0
    }
  ]
}
```
---

#### Scenario `FLX-PAT-02`: Update daily duration to 540m (2700m total)
- **Endpoint:** `PATCH https://attendance2.dev.zoolwork.com/api/companies/3a249871-7a8d-dec5-2d72-47795dd2662d/worktemplates/flexi/7ecfbe95-8d3c-4612-a0cc-1454e9093a53?locationId=3a24d646-b3cf-b1d4-61bb-1adf094b52fc`
- **Execution Result:** HTTP `200` -> **PASS**
- **MongoDB `_id`:** `7ecfbe95-8d3c-4612-a0cc-1454e9093a53`

**Request Payload:**
```json
{
  "templateName": {
    "en": "Flexible Location Shift FXD0001",
    "ar": "\u0648\u0631\u062f\u064a\u0629 \u0645\u0631\u0646\u0629 FXD0001"
  },
  "shortCode": "FXD0001",
  "templateType": 2,
  "flexibleType": 1,
  "totalWorkDurationInMinutes": 2700,
  "totalWorkingDays": 5,
  "totalDaysOff": 2,
  "timeZoneId": "Asia/Riyadh",
  "flexiTimeSlots": [
    {
      "dayEnum": 1,
      "isWorkingDay": true,
      "recurrenceOfMonth": [
        1,
        2,
        3,
        4,
        5
      ],
      "workDurationInMinutes": 540
    },
    {
      "dayEnum": 2,
      "isWorkingDay": true,
      "recurrenceOfMonth": [
        1,
        2,
        3,
        4,
        5
      ],
      "workDurationInMinutes": 540
    },
    {
      "dayEnum": 3,
      "isWorkingDay": true,
      "recurrenceOfMonth": [
        1,
        2,
        3,
        4,
        5
      ],
      "workDurationInMinutes": 540
    },
    {
      "dayEnum": 4,
      "isWorkingDay": true,
      "recurrenceOfMonth": [
        1,
        2,
        3,
        4,
        5
      ],
      "workDurationInMinutes": 540
    },
    {
      "dayEnum": 5,
      "isWorkingDay": true,
      "recurrenceOfMonth": [
        1,
        2,
        3,
        4,
        5
      ],
      "workDurationInMinutes": 540
    },
    {
      "dayEnum": 6,
      "isWorkingDay": false,
      "recurrenceOfMonth": [],
      "workDurationInMinutes": 0
    },
    {
      "dayEnum": 7,
      "isWorkingDay": false,
      "recurrenceOfMonth": [],
      "workDurationInMinutes": 0
    }
  ]
}
```
---

#### Scenario `FLX-PAT-03`: Update timezone to Asia/Dubai
- **Endpoint:** `PATCH https://attendance2.dev.zoolwork.com/api/companies/3a249871-7a8d-dec5-2d72-47795dd2662d/worktemplates/flexi/7ecfbe95-8d3c-4612-a0cc-1454e9093a53?locationId=3a24d646-b3cf-b1d4-61bb-1adf094b52fc`
- **Execution Result:** HTTP `200` -> **PASS**
- **MongoDB `_id`:** `7ecfbe95-8d3c-4612-a0cc-1454e9093a53`

**Request Payload:**
```json
{
  "templateName": {
    "en": "Flexible Location Shift FXD0001",
    "ar": "\u0648\u0631\u062f\u064a\u0629 \u0645\u0631\u0646\u0629 FXD0001"
  },
  "shortCode": "FXD0001",
  "templateType": 2,
  "flexibleType": 1,
  "totalWorkDurationInMinutes": 2700,
  "totalWorkingDays": 5,
  "totalDaysOff": 2,
  "timeZoneId": "Asia/Dubai",
  "flexiTimeSlots": [
    {
      "dayEnum": 1,
      "isWorkingDay": true,
      "recurrenceOfMonth": [
        1,
        2,
        3,
        4,
        5
      ],
      "workDurationInMinutes": 480
    },
    {
      "dayEnum": 2,
      "isWorkingDay": true,
      "recurrenceOfMonth": [
        1,
        2,
        3,
        4,
        5
      ],
      "workDurationInMinutes": 480
    },
    {
      "dayEnum": 3,
      "isWorkingDay": true,
      "recurrenceOfMonth": [
        1,
        2,
        3,
        4,
        5
      ],
      "workDurationInMinutes": 480
    },
    {
      "dayEnum": 4,
      "isWorkingDay": true,
      "recurrenceOfMonth": [
        1,
        2,
        3,
        4,
        5
      ],
      "workDurationInMinutes": 480
    },
    {
      "dayEnum": 5,
      "isWorkingDay": true,
      "recurrenceOfMonth": [
        1,
        2,
        3,
        4,
        5
      ],
      "workDurationInMinutes": 480
    },
    {
      "dayEnum": 6,
      "isWorkingDay": false,
      "recurrenceOfMonth": [],
      "workDurationInMinutes": 0
    },
    {
      "dayEnum": 7,
      "isWorkingDay": false,
      "recurrenceOfMonth": [],
      "workDurationInMinutes": 0
    }
  ]
}
```
---

#### Scenario `FLX-PAT-04`: Attempt to alter shortCode in PATCH (Cit.Attendance:1107)
- **Endpoint:** `PATCH https://attendance2.dev.zoolwork.com/api/companies/3a249871-7a8d-dec5-2d72-47795dd2662d/worktemplates/flexi/7ecfbe95-8d3c-4612-a0cc-1454e9093a53?locationId=3a24d646-b3cf-b1d4-61bb-1adf094b52fc`
- **Execution Result:** HTTP `400` -> **PASS**
- **API Error:** `Cit.Attendance:1107` | `A work template's short code cannot be changed after it is created.`

**Request Payload:**
```json
{
  "templateName": {
    "en": "Flexible Location Shift FXDCHG1",
    "ar": "\u0648\u0631\u062f\u064a\u0629 \u0645\u0631\u0646\u0629 FXDCHG1"
  },
  "shortCode": "FXDCHG1",
  "templateType": 2,
  "flexibleType": 1,
  "totalWorkDurationInMinutes": 2700,
  "totalWorkingDays": 5,
  "totalDaysOff": 2,
  "timeZoneId": "Asia/Riyadh",
  "flexiTimeSlots": [
    {
      "dayEnum": 1,
      "isWorkingDay": true,
      "recurrenceOfMonth": [
        1,
        2,
        3,
        4,
        5
      ],
      "workDurationInMinutes": 480
    },
    {
      "dayEnum": 2,
      "isWorkingDay": true,
      "recurrenceOfMonth": [
        1,
        2,
        3,
        4,
        5
      ],
      "workDurationInMinutes": 480
    },
    {
      "dayEnum": 3,
      "isWorkingDay": true,
      "recurrenceOfMonth": [
        1,
        2,
        3,
        4,
        5
      ],
      "workDurationInMinutes": 480
    },
    {
      "dayEnum": 4,
      "isWorkingDay": true,
      "recurrenceOfMonth": [
        1,
        2,
        3,
        4,
        5
      ],
      "workDurationInMinutes": 480
    },
    {
      "dayEnum": 5,
      "isWorkingDay": true,
      "recurrenceOfMonth": [
        1,
        2,
        3,
        4,
        5
      ],
      "workDurationInMinutes": 480
    },
    {
      "dayEnum": 6,
      "isWorkingDay": false,
      "recurrenceOfMonth": [],
      "workDurationInMinutes": 0
    },
    {
      "dayEnum": 7,
      "isWorkingDay": false,
      "recurrenceOfMonth": [],
      "workDurationInMinutes": 0
    }
  ]
}
```
---

#### Scenario `FLX-PAT-05`: Recurrence [6] in Flexible PATCH
- **Endpoint:** `PATCH https://attendance2.dev.zoolwork.com/api/companies/3a249871-7a8d-dec5-2d72-47795dd2662d/worktemplates/flexi/7ecfbe95-8d3c-4612-a0cc-1454e9093a53?locationId=3a24d646-b3cf-b1d4-61bb-1adf094b52fc`
- **Execution Result:** HTTP `200` -> **FAIL**
- **MongoDB `_id`:** `7ecfbe95-8d3c-4612-a0cc-1454e9093a53`

**Request Payload:**
```json
{
  "templateName": {
    "en": "Flexible Location Shift FXD0001",
    "ar": "\u0648\u0631\u062f\u064a\u0629 \u0645\u0631\u0646\u0629 FXD0001"
  },
  "shortCode": "FXD0001",
  "templateType": 2,
  "flexibleType": 1,
  "totalWorkDurationInMinutes": 2700,
  "totalWorkingDays": 5,
  "totalDaysOff": 2,
  "timeZoneId": "Asia/Riyadh",
  "flexiTimeSlots": [
    {
      "dayEnum": 1,
      "isWorkingDay": true,
      "recurrenceOfMonth": [
        6
      ],
      "workDurationInMinutes": 480
    },
    {
      "dayEnum": 2,
      "isWorkingDay": true,
      "recurrenceOfMonth": [
        1,
        2,
        3,
        4,
        5
      ],
      "workDurationInMinutes": 480
    },
    {
      "dayEnum": 3,
      "isWorkingDay": true,
      "recurrenceOfMonth": [
        1,
        2,
        3,
        4,
        5
      ],
      "workDurationInMinutes": 480
    },
    {
      "dayEnum": 4,
      "isWorkingDay": true,
      "recurrenceOfMonth": [
        1,
        2,
        3,
        4,
        5
      ],
      "workDurationInMinutes": 480
    },
    {
      "dayEnum": 5,
      "isWorkingDay": true,
      "recurrenceOfMonth": [
        1,
        2,
        3,
        4,
        5
      ],
      "workDurationInMinutes": 480
    },
    {
      "dayEnum": 6,
      "isWorkingDay": false,
      "recurrenceOfMonth": [],
      "workDurationInMinutes": 0
    },
    {
      "dayEnum": 7,
      "isWorkingDay": false,
      "recurrenceOfMonth": [],
      "workDurationInMinutes": 0
    }
  ]
}
```
---

#### Scenario `FLX-PAT-06`: Duration mismatch in Flexible PATCH (3500 vs 2700)
- **Endpoint:** `PATCH https://attendance2.dev.zoolwork.com/api/companies/3a249871-7a8d-dec5-2d72-47795dd2662d/worktemplates/flexi/7ecfbe95-8d3c-4612-a0cc-1454e9093a53?locationId=3a24d646-b3cf-b1d4-61bb-1adf094b52fc`
- **Execution Result:** HTTP `200` -> **FAIL**
- **MongoDB `_id`:** `7ecfbe95-8d3c-4612-a0cc-1454e9093a53`

**Request Payload:**
```json
{
  "templateName": {
    "en": "Flexible Location Shift FXD0001",
    "ar": "\u0648\u0631\u062f\u064a\u0629 \u0645\u0631\u0646\u0629 FXD0001"
  },
  "shortCode": "FXD0001",
  "templateType": 2,
  "flexibleType": 1,
  "totalWorkDurationInMinutes": 3500,
  "totalWorkingDays": 5,
  "totalDaysOff": 2,
  "timeZoneId": "Asia/Riyadh",
  "flexiTimeSlots": [
    {
      "dayEnum": 1,
      "isWorkingDay": true,
      "recurrenceOfMonth": [
        1,
        2,
        3,
        4,
        5
      ],
      "workDurationInMinutes": 480
    },
    {
      "dayEnum": 2,
      "isWorkingDay": true,
      "recurrenceOfMonth": [
        1,
        2,
        3,
        4,
        5
      ],
      "workDurationInMinutes": 480
    },
    {
      "dayEnum": 3,
      "isWorkingDay": true,
      "recurrenceOfMonth": [
        1,
        2,
        3,
        4,
        5
      ],
      "workDurationInMinutes": 480
    },
    {
      "dayEnum": 4,
      "isWorkingDay": true,
      "recurrenceOfMonth": [
        1,
        2,
        3,
        4,
        5
      ],
      "workDurationInMinutes": 480
    },
    {
      "dayEnum": 5,
      "isWorkingDay": true,
      "recurrenceOfMonth": [
        1,
        2,
        3,
        4,
        5
      ],
      "workDurationInMinutes": 480
    },
    {
      "dayEnum": 6,
      "isWorkingDay": false,
      "recurrenceOfMonth": [],
      "workDurationInMinutes": 0
    },
    {
      "dayEnum": 7,
      "isWorkingDay": false,
      "recurrenceOfMonth": [],
      "workDurationInMinutes": 0
    }
  ]
}
```
---

#### Scenario `FLX-PAT-07`: Invalid timezone in Flexible PATCH
- **Endpoint:** `PATCH https://attendance2.dev.zoolwork.com/api/companies/3a249871-7a8d-dec5-2d72-47795dd2662d/worktemplates/flexi/7ecfbe95-8d3c-4612-a0cc-1454e9093a53?locationId=3a24d646-b3cf-b1d4-61bb-1adf094b52fc`
- **Execution Result:** HTTP `200` -> **FAIL**
- **MongoDB `_id`:** `7ecfbe95-8d3c-4612-a0cc-1454e9093a53`

**Request Payload:**
```json
{
  "templateName": {
    "en": "Flexible Location Shift FXD0001",
    "ar": "\u0648\u0631\u062f\u064a\u0629 \u0645\u0631\u0646\u0629 FXD0001"
  },
  "shortCode": "FXD0001",
  "templateType": 2,
  "flexibleType": 1,
  "totalWorkDurationInMinutes": 2700,
  "totalWorkingDays": 5,
  "totalDaysOff": 2,
  "timeZoneId": "Invalid/Timezone",
  "flexiTimeSlots": [
    {
      "dayEnum": 1,
      "isWorkingDay": true,
      "recurrenceOfMonth": [
        1,
        2,
        3,
        4,
        5
      ],
      "workDurationInMinutes": 480
    },
    {
      "dayEnum": 2,
      "isWorkingDay": true,
      "recurrenceOfMonth": [
        1,
        2,
        3,
        4,
        5
      ],
      "workDurationInMinutes": 480
    },
    {
      "dayEnum": 3,
      "isWorkingDay": true,
      "recurrenceOfMonth": [
        1,
        2,
        3,
        4,
        5
      ],
      "workDurationInMinutes": 480
    },
    {
      "dayEnum": 4,
      "isWorkingDay": true,
      "recurrenceOfMonth": [
        1,
        2,
        3,
        4,
        5
      ],
      "workDurationInMinutes": 480
    },
    {
      "dayEnum": 5,
      "isWorkingDay": true,
      "recurrenceOfMonth": [
        1,
        2,
        3,
        4,
        5
      ],
      "workDurationInMinutes": 480
    },
    {
      "dayEnum": 6,
      "isWorkingDay": false,
      "recurrenceOfMonth": [],
      "workDurationInMinutes": 0
    },
    {
      "dayEnum": 7,
      "isWorkingDay": false,
      "recurrenceOfMonth": [],
      "workDurationInMinutes": 0
    }
  ]
}
```
---