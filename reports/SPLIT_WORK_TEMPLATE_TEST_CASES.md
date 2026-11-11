# Sahab ERP Attendance – Split Work Template Test Suite Specification & Execution Log

**Document Version:** `1.0`  
**Execution Date:** `2026-11-10`  
**Module:** Split Work Template (`TemplateType: 3`)  
**Target Location:** Location 2 (`3a24d646-b3cf-b1d4-61bb-1adf094b52fc`)  
**Total Scenarios:** `22` | **Passed:** `19` | **Failed:** `3`  
**Target Collection:** `Sahab.ERP.Attendance.WorkTemplates`  
**Visual Evidence:** [Evidence 56 (Flexible & Split Template Validation Bypasses & Transitions)](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_56_flexi_split_location_validation_bypasses_and_db_results.png)  

---

## 1. Module Overview & Technical Architecture

A **Split Work Template** (`TemplateType: 3`) accommodates shifts structured into multiple active work sessions separated by mandatory non-working break windows (e.g., Morning Shift: 08:00–12:00, Break: 12:00–14:00, Afternoon Shift: 14:00–18:00).

### Key Domain Properties:
- `templateType`: Integer `3` (Split).
- `splitTimeSlots`: Array of 7 weekday rows.
- `timeSlots`: Array of interval objects embedded within each working day slot. Each interval contains `startTime`, `endTime`, and `workDurationInMinutes`.
- **Mathematical Invariant:** `slot.workDurationInMinutes` must equal the sum of durations of all child intervals inside `timeSlots`.
- **Interval Invariant:** Intervals on the same day cannot overlap and must be strictly chronological.

---

## 2. Test Execution Breakdown by Category

### 2.1 Positive POST (Creation of Multi-Interval Split Shifts) (5 Scenarios)
| Test ID | Description | HTTP Method & Endpoint | Status | Result | Notes / Defect Caught |
| :--- | :--- | :--- | :---: | :---: | :--- |
| `SPL-POS-01` | Split standard 2-interval shift (240+240=480m/day, total 2400m) | `POST /worktemplates/split` | `200` | ✅ PASS | Split standard 2-interval shift (240+240=480m/day, total 2400m) |
| `SPL-POS-02` | Split 3-interval shift (180+180+120=480m/day) | `POST /worktemplates/split` | `200` | ✅ PASS | Split 3-interval shift (180+180+120=480m/day) |
| `SPL-POS-03` | Split 6-day working schedule (2880m total) | `POST /worktemplates/split` | `200` | ✅ PASS | Split 6-day working schedule (2880m total) |
| `SPL-POS-04` | Split 4-day working schedule (1920m total) | `POST /worktemplates/split` | `200` | ✅ PASS | Split 4-day working schedule (1920m total) |
| `SPL-POS-05` | Split India Timezone (Asia/Kolkata) | `POST /worktemplates/split` | `200` | ✅ PASS | Split India Timezone (Asia/Kolkata) |

### 2.2 Negative POST (Interval Overlap, Inversion & Sum Guardrails) (10 Scenarios)
| Test ID | Description | HTTP Method & Endpoint | Status | Result | Notes / Defect Caught |
| :--- | :--- | :--- | :---: | :---: | :--- |
| `SPL-NEG-01` | Empty template name | `POST /worktemplates/split` | `400` | ✅ PASS | Empty template name |
| `SPL-NEG-02` | ShortCode length < 7 ('SPL01') | `POST /worktemplates/split` | `400` | ✅ PASS | ShortCode length < 7 ('SPL01') |
| `SPL-NEG-03` | Duplicate shortCode (SPD0001) | `POST /worktemplates/split` | `400` | ✅ PASS | Duplicate shortCode (SPD0001) |
| `SPL-NEG-04` | Overlapping split intervals (1 hr overlap) | `POST /worktemplates/split` | `400` | ✅ PASS | Overlapping split intervals (1 hr overlap) |
| `SPL-NEG-05` | Zero break gap between intervals (12:00 to 12:00) | `POST /worktemplates/split` | `400` | ✅ PASS | Zero break gap between intervals (12:00 to 12:00) |
| `SPL-NEG-06` | Inverted split interval (startTime 12:00 > endTime 08:00) | `POST /worktemplates/split` | `400` | ✅ PASS | Inverted split interval (startTime 12:00 > endTime 08:00) |
| `SPL-NEG-07` | Empty timeSlots array on working day | `POST /worktemplates/split` | `400` | ✅ PASS | Empty timeSlots array on working day |
| `SPL-NEG-08` | Interval duration does not equal (endTime - startTime) | `POST /worktemplates/split` | `400` | ✅ PASS | Interval duration does not equal (endTime - startTime) |
| `SPL-NEG-09` | Daily duration does not equal interval sum (600 vs 480) | `POST /worktemplates/split` | `400` | ✅ PASS | Daily duration does not equal interval sum (600 vs 480) |
| `SPL-NEG-10` | Total duration mismatch in Split (3000 vs 2400) | `POST /worktemplates/split` | `200` | ❌ FAIL | Total duration mismatch in Split (3000 vs 2400) **[DEFECT-20261110-13]** |

### 2.3 Positive PATCH (In-Place Location Mutation) (3 Scenarios)
| Test ID | Description | HTTP Method & Endpoint | Status | Result | Notes / Defect Caught |
| :--- | :--- | :--- | :---: | :---: | :--- |
| `SPL-PAT-01` | Update Split template name | `PATCH /worktemplates/split` | `200` | ✅ PASS | Update Split template name |
| `SPL-PAT-02` | Update Split interval timings (09-13 & 15-19) | `PATCH /worktemplates/split` | `200` | ✅ PASS | Update Split interval timings (09-13 & 15-19) |
| `SPL-PAT-03` | Update timezone to Asia/Dubai | `PATCH /worktemplates/split` | `200` | ✅ PASS | Update timezone to Asia/Dubai |

### 2.4 Negative PATCH (Immutability & Validation Gaps) (4 Scenarios)
| Test ID | Description | HTTP Method & Endpoint | Status | Result | Notes / Defect Caught |
| :--- | :--- | :--- | :---: | :---: | :--- |
| `SPL-PAT-04` | Attempt to alter shortCode in Split PATCH (Cit.Attendance:1107) | `PATCH /worktemplates/split` | `400` | ✅ PASS | Attempt to alter shortCode in Split PATCH (Cit.Attendance:1107) |
| `SPL-PAT-05` | Overlapping intervals in Split PATCH | `PATCH /worktemplates/split` | `400` | ✅ PASS | Overlapping intervals in Split PATCH |
| `SPL-PAT-06` | Recurrence [6] in Split PATCH | `PATCH /worktemplates/split` | `200` | ❌ FAIL | Recurrence [6] in Split PATCH **[DEFECT-20261110-14]** |
| `SPL-PAT-07` | Duration mismatch in Split PATCH (3200 vs 2400) | `PATCH /worktemplates/split` | `200` | ❌ FAIL | Duration mismatch in Split PATCH (3200 vs 2400) **[DEFECT-20261110-13]** |

---

## 3. Detailed Payload & Database Verification Log

#### Scenario `SPL-POS-01`: Split standard 2-interval shift (240+240=480m/day, total 2400m)
- **Endpoint:** `POST https://attendance2.dev.zoolwork.com/api/companies/3a249871-7a8d-dec5-2d72-47795dd2662d/worktemplates/split?locationId=3a24d646-b3cf-b1d4-61bb-1adf094b52fc`
- **Execution Result:** HTTP `200` -> **PASS**
- **MongoDB `_id`:** `ab6bb972-24e9-4b3c-9c23-55ef8770f6e5`

**Request Payload:**
```json
{
  "templateName": {
    "en": "Split Location Shift SPD0001",
    "ar": "\u0648\u0631\u062f\u064a\u0629 \u0645\u062c\u0632\u0623\u0629 SPD0001"
  },
  "shortCode": "SPD0001",
  "templateType": 3,
  "totalWorkDurationInMinutes": 2400,
  "totalWorkingDays": 5,
  "totalDaysOff": 2,
  "timeZoneId": "Asia/Riyadh",
  "splitTimeSlots": [
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
      "workDurationInMinutes": 480,
      "timeSlots": [
        {
          "startTime": "08:00:00",
          "endTime": "12:00:00",
          "workDurationInMinutes": 240
        },
        {
          "startTime": "14:00:00",
          "endTime": "18:00:00",
          "workDurationInMinutes": 240
        }
      ]
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
      "workDurationInMinutes": 480,
      "timeSlots": [
        {
          "startTime": "08:00:00",
          "endTime": "12:00:00",
          "workDurationInMinutes": 240
        },
        {
          "startTime": "14:00:00",
          "endTime": "18:00:00",
          "workDurationInMinutes": 240
        }
      ]
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
      "workDurationInMinutes": 480,
      "timeSlots": [
        {
          "startTime": "08:00:00",
          "endTime": "12:00:00",
          "workDurationInMinutes": 240
        },
        {
          "startTime": "14:00:00",
          "endTime": "18:00:00",
          "workDurationInMinutes": 240
        }
      ]
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
      "workDurationInMinutes": 480,
      "timeSlots": [
        {
          "startTime": "08:00:00",
          "endTime": "12:00:00",
          "workDurationInMinutes": 240
        },
        {
          "startTime": "14:00:00",
          "endTime": "18:00:00",
          "workDurationInMinutes": 240
        }
      ]
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
      "workDurationInMinutes": 480,
      "timeSlots": [
        {
          "startTime": "08:00:00",
          "endTime": "12:00:00",
          "workDurationInMinutes": 240
        },
        {
          "startTime": "14:00:00",
          "endTime": "18:00:00",
          "workDurationInMinutes": 240
        }
      ]
    },
    {
      "dayEnum": 6,
      "isWorkingDay": false,
      "recurrenceOfMonth": [],
      "workDurationInMinutes": 0,
      "timeSlots": []
    },
    {
      "dayEnum": 7,
      "isWorkingDay": false,
      "recurrenceOfMonth": [],
      "workDurationInMinutes": 0,
      "timeSlots": []
    }
  ]
}
```
---

#### Scenario `SPL-POS-02`: Split 3-interval shift (180+180+120=480m/day)
- **Endpoint:** `POST https://attendance2.dev.zoolwork.com/api/companies/3a249871-7a8d-dec5-2d72-47795dd2662d/worktemplates/split?locationId=3a24d646-b3cf-b1d4-61bb-1adf094b52fc`
- **Execution Result:** HTTP `200` -> **PASS**
- **MongoDB `_id`:** `5766c9f3-8632-4359-b9a6-3796b14d355c`

**Request Payload:**
```json
{
  "templateName": {
    "en": "Split Location Shift SPD0002",
    "ar": "\u0648\u0631\u062f\u064a\u0629 \u0645\u062c\u0632\u0623\u0629 SPD0002"
  },
  "shortCode": "SPD0002",
  "templateType": 3,
  "totalWorkDurationInMinutes": 2400,
  "totalWorkingDays": 5,
  "totalDaysOff": 2,
  "timeZoneId": "Asia/Riyadh",
  "splitTimeSlots": [
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
      "workDurationInMinutes": 480,
      "timeSlots": [
        {
          "startTime": "08:00:00",
          "endTime": "11:00:00",
          "workDurationInMinutes": 180
        },
        {
          "startTime": "12:00:00",
          "endTime": "15:00:00",
          "workDurationInMinutes": 180
        },
        {
          "startTime": "16:00:00",
          "endTime": "18:00:00",
          "workDurationInMinutes": 120
        }
      ]
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
      "workDurationInMinutes": 480,
      "timeSlots": [
        {
          "startTime": "08:00:00",
          "endTime": "11:00:00",
          "workDurationInMinutes": 180
        },
        {
          "startTime": "12:00:00",
          "endTime": "15:00:00",
          "workDurationInMinutes": 180
        },
        {
          "startTime": "16:00:00",
          "endTime": "18:00:00",
          "workDurationInMinutes": 120
        }
      ]
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
      "workDurationInMinutes": 480,
      "timeSlots": [
        {
          "startTime": "08:00:00",
          "endTime": "11:00:00",
          "workDurationInMinutes": 180
        },
        {
          "startTime": "12:00:00",
          "endTime": "15:00:00",
          "workDurationInMinutes": 180
        },
        {
          "startTime": "16:00:00",
          "endTime": "18:00:00",
          "workDurationInMinutes": 120
        }
      ]
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
      "workDurationInMinutes": 480,
      "timeSlots": [
        {
          "startTime": "08:00:00",
          "endTime": "11:00:00",
          "workDurationInMinutes": 180
        },
        {
          "startTime": "12:00:00",
          "endTime": "15:00:00",
          "workDurationInMinutes": 180
        },
        {
          "startTime": "16:00:00",
          "endTime": "18:00:00",
          "workDurationInMinutes": 120
        }
      ]
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
      "workDurationInMinutes": 480,
      "timeSlots": [
        {
          "startTime": "08:00:00",
          "endTime": "11:00:00",
          "workDurationInMinutes": 180
        },
        {
          "startTime": "12:00:00",
          "endTime": "15:00:00",
          "workDurationInMinutes": 180
        },
        {
          "startTime": "16:00:00",
          "endTime": "18:00:00",
          "workDurationInMinutes": 120
        }
      ]
    },
    {
      "dayEnum": 6,
      "isWorkingDay": false,
      "recurrenceOfMonth": [],
      "workDurationInMinutes": 0,
      "timeSlots": []
    },
    {
      "dayEnum": 7,
      "isWorkingDay": false,
      "recurrenceOfMonth": [],
      "workDurationInMinutes": 0,
      "timeSlots": []
    }
  ]
}
```
---

#### Scenario `SPL-POS-03`: Split 6-day working schedule (2880m total)
- **Endpoint:** `POST https://attendance2.dev.zoolwork.com/api/companies/3a249871-7a8d-dec5-2d72-47795dd2662d/worktemplates/split?locationId=3a24d646-b3cf-b1d4-61bb-1adf094b52fc`
- **Execution Result:** HTTP `200` -> **PASS**
- **MongoDB `_id`:** `0dc290bd-f874-41b7-89a2-4ab0de190b9d`

**Request Payload:**
```json
{
  "templateName": {
    "en": "Split Location Shift SPD0003",
    "ar": "\u0648\u0631\u062f\u064a\u0629 \u0645\u062c\u0632\u0623\u0629 SPD0003"
  },
  "shortCode": "SPD0003",
  "templateType": 3,
  "totalWorkDurationInMinutes": 2880,
  "totalWorkingDays": 6,
  "totalDaysOff": 1,
  "timeZoneId": "Asia/Riyadh",
  "splitTimeSlots": [
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
      "workDurationInMinutes": 480,
      "timeSlots": [
        {
          "startTime": "08:00:00",
          "endTime": "12:00:00",
          "workDurationInMinutes": 240
        },
        {
          "startTime": "14:00:00",
          "endTime": "18:00:00",
          "workDurationInMinutes": 240
        }
      ]
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
      "workDurationInMinutes": 480,
      "timeSlots": [
        {
          "startTime": "08:00:00",
          "endTime": "12:00:00",
          "workDurationInMinutes": 240
        },
        {
          "startTime": "14:00:00",
          "endTime": "18:00:00",
          "workDurationInMinutes": 240
        }
      ]
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
      "workDurationInMinutes": 480,
      "timeSlots": [
        {
          "startTime": "08:00:00",
          "endTime": "12:00:00",
          "workDurationInMinutes": 240
        },
        {
          "startTime": "14:00:00",
          "endTime": "18:00:00",
          "workDurationInMinutes": 240
        }
      ]
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
      "workDurationInMinutes": 480,
      "timeSlots": [
        {
          "startTime": "08:00:00",
          "endTime": "12:00:00",
          "workDurationInMinutes": 240
        },
        {
          "startTime": "14:00:00",
          "endTime": "18:00:00",
          "workDurationInMinutes": 240
        }
      ]
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
      "workDurationInMinutes": 480,
      "timeSlots": [
        {
          "startTime": "08:00:00",
          "endTime": "12:00:00",
          "workDurationInMinutes": 240
        },
        {
          "startTime": "14:00:00",
          "endTime": "18:00:00",
          "workDurationInMinutes": 240
        }
      ]
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
      "workDurationInMinutes": 480,
      "timeSlots": [
        {
          "startTime": "08:00:00",
          "endTime": "12:00:00",
          "workDurationInMinutes": 240
        },
        {
          "startTime": "14:00:00",
          "endTime": "18:00:00",
          "workDurationInMinutes": 240
        }
      ]
    },
    {
      "dayEnum": 7,
      "isWorkingDay": false,
      "recurrenceOfMonth": [],
      "workDurationInMinutes": 0,
      "timeSlots": []
    }
  ]
}
```
---

#### Scenario `SPL-POS-04`: Split 4-day working schedule (1920m total)
- **Endpoint:** `POST https://attendance2.dev.zoolwork.com/api/companies/3a249871-7a8d-dec5-2d72-47795dd2662d/worktemplates/split?locationId=3a24d646-b3cf-b1d4-61bb-1adf094b52fc`
- **Execution Result:** HTTP `200` -> **PASS**
- **MongoDB `_id`:** `4565d924-fd11-42ae-a1ef-3fedaaafd722`

**Request Payload:**
```json
{
  "templateName": {
    "en": "Split Location Shift SPD0004",
    "ar": "\u0648\u0631\u062f\u064a\u0629 \u0645\u062c\u0632\u0623\u0629 SPD0004"
  },
  "shortCode": "SPD0004",
  "templateType": 3,
  "totalWorkDurationInMinutes": 1920,
  "totalWorkingDays": 4,
  "totalDaysOff": 3,
  "timeZoneId": "Asia/Riyadh",
  "splitTimeSlots": [
    {
      "dayEnum": 1,
      "isWorkingDay": false,
      "recurrenceOfMonth": [],
      "workDurationInMinutes": 0,
      "timeSlots": []
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
      "workDurationInMinutes": 480,
      "timeSlots": [
        {
          "startTime": "08:00:00",
          "endTime": "12:00:00",
          "workDurationInMinutes": 240
        },
        {
          "startTime": "14:00:00",
          "endTime": "18:00:00",
          "workDurationInMinutes": 240
        }
      ]
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
      "workDurationInMinutes": 480,
      "timeSlots": [
        {
          "startTime": "08:00:00",
          "endTime": "12:00:00",
          "workDurationInMinutes": 240
        },
        {
          "startTime": "14:00:00",
          "endTime": "18:00:00",
          "workDurationInMinutes": 240
        }
      ]
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
      "workDurationInMinutes": 480,
      "timeSlots": [
        {
          "startTime": "08:00:00",
          "endTime": "12:00:00",
          "workDurationInMinutes": 240
        },
        {
          "startTime": "14:00:00",
          "endTime": "18:00:00",
          "workDurationInMinutes": 240
        }
      ]
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
      "workDurationInMinutes": 480,
      "timeSlots": [
        {
          "startTime": "08:00:00",
          "endTime": "12:00:00",
          "workDurationInMinutes": 240
        },
        {
          "startTime": "14:00:00",
          "endTime": "18:00:00",
          "workDurationInMinutes": 240
        }
      ]
    },
    {
      "dayEnum": 6,
      "isWorkingDay": false,
      "recurrenceOfMonth": [],
      "workDurationInMinutes": 0,
      "timeSlots": []
    },
    {
      "dayEnum": 7,
      "isWorkingDay": false,
      "recurrenceOfMonth": [],
      "workDurationInMinutes": 0,
      "timeSlots": []
    }
  ]
}
```
---

#### Scenario `SPL-POS-05`: Split India Timezone (Asia/Kolkata)
- **Endpoint:** `POST https://attendance2.dev.zoolwork.com/api/companies/3a249871-7a8d-dec5-2d72-47795dd2662d/worktemplates/split?locationId=3a24d646-b3cf-b1d4-61bb-1adf094b52fc`
- **Execution Result:** HTTP `200` -> **PASS**
- **MongoDB `_id`:** `e180b571-b783-4f00-a37f-c0a7b1c23d4c`

**Request Payload:**
```json
{
  "templateName": {
    "en": "Split Location Shift SPD0005",
    "ar": "\u0648\u0631\u062f\u064a\u0629 \u0645\u062c\u0632\u0623\u0629 SPD0005"
  },
  "shortCode": "SPD0005",
  "templateType": 3,
  "totalWorkDurationInMinutes": 2400,
  "totalWorkingDays": 5,
  "totalDaysOff": 2,
  "timeZoneId": "Asia/Kolkata",
  "splitTimeSlots": [
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
      "workDurationInMinutes": 480,
      "timeSlots": [
        {
          "startTime": "08:00:00",
          "endTime": "12:00:00",
          "workDurationInMinutes": 240
        },
        {
          "startTime": "14:00:00",
          "endTime": "18:00:00",
          "workDurationInMinutes": 240
        }
      ]
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
      "workDurationInMinutes": 480,
      "timeSlots": [
        {
          "startTime": "08:00:00",
          "endTime": "12:00:00",
          "workDurationInMinutes": 240
        },
        {
          "startTime": "14:00:00",
          "endTime": "18:00:00",
          "workDurationInMinutes": 240
        }
      ]
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
      "workDurationInMinutes": 480,
      "timeSlots": [
        {
          "startTime": "08:00:00",
          "endTime": "12:00:00",
          "workDurationInMinutes": 240
        },
        {
          "startTime": "14:00:00",
          "endTime": "18:00:00",
          "workDurationInMinutes": 240
        }
      ]
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
      "workDurationInMinutes": 480,
      "timeSlots": [
        {
          "startTime": "08:00:00",
          "endTime": "12:00:00",
          "workDurationInMinutes": 240
        },
        {
          "startTime": "14:00:00",
          "endTime": "18:00:00",
          "workDurationInMinutes": 240
        }
      ]
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
      "workDurationInMinutes": 480,
      "timeSlots": [
        {
          "startTime": "08:00:00",
          "endTime": "12:00:00",
          "workDurationInMinutes": 240
        },
        {
          "startTime": "14:00:00",
          "endTime": "18:00:00",
          "workDurationInMinutes": 240
        }
      ]
    },
    {
      "dayEnum": 6,
      "isWorkingDay": false,
      "recurrenceOfMonth": [],
      "workDurationInMinutes": 0,
      "timeSlots": []
    },
    {
      "dayEnum": 7,
      "isWorkingDay": false,
      "recurrenceOfMonth": [],
      "workDurationInMinutes": 0,
      "timeSlots": []
    }
  ]
}
```
---

#### Scenario `SPL-NEG-01`: Empty template name
- **Endpoint:** `POST https://attendance2.dev.zoolwork.com/api/companies/3a249871-7a8d-dec5-2d72-47795dd2662d/worktemplates/split?locationId=3a24d646-b3cf-b1d4-61bb-1adf094b52fc`
- **Execution Result:** HTTP `400` -> **PASS**
- **API Error:** `Cit.Attendance:Validation` | `An English template name is required.`

**Request Payload:**
```json
{
  "templateName": {
    "en": "",
    "ar": ""
  },
  "shortCode": "SPDNEG1",
  "templateType": 3,
  "totalWorkDurationInMinutes": 2400,
  "totalWorkingDays": 5,
  "totalDaysOff": 2,
  "timeZoneId": "Asia/Riyadh",
  "splitTimeSlots": [
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
      "workDurationInMinutes": 480,
      "timeSlots": [
        {
          "startTime": "08:00:00",
          "endTime": "12:00:00",
          "workDurationInMinutes": 240
        },
        {
          "startTime": "14:00:00",
          "endTime": "18:00:00",
          "workDurationInMinutes": 240
        }
      ]
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
      "workDurationInMinutes": 480,
      "timeSlots": [
        {
          "startTime": "08:00:00",
          "endTime": "12:00:00",
          "workDurationInMinutes": 240
        },
        {
          "startTime": "14:00:00",
          "endTime": "18:00:00",
          "workDurationInMinutes": 240
        }
      ]
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
      "workDurationInMinutes": 480,
      "timeSlots": [
        {
          "startTime": "08:00:00",
          "endTime": "12:00:00",
          "workDurationInMinutes": 240
        },
        {
          "startTime": "14:00:00",
          "endTime": "18:00:00",
          "workDurationInMinutes": 240
        }
      ]
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
      "workDurationInMinutes": 480,
      "timeSlots": [
        {
          "startTime": "08:00:00",
          "endTime": "12:00:00",
          "workDurationInMinutes": 240
        },
        {
          "startTime": "14:00:00",
          "endTime": "18:00:00",
          "workDurationInMinutes": 240
        }
      ]
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
      "workDurationInMinutes": 480,
      "timeSlots": [
        {
          "startTime": "08:00:00",
          "endTime": "12:00:00",
          "workDurationInMinutes": 240
        },
        {
          "startTime": "14:00:00",
          "endTime": "18:00:00",
          "workDurationInMinutes": 240
        }
      ]
    },
    {
      "dayEnum": 6,
      "isWorkingDay": false,
      "recurrenceOfMonth": [],
      "workDurationInMinutes": 0,
      "timeSlots": []
    },
    {
      "dayEnum": 7,
      "isWorkingDay": false,
      "recurrenceOfMonth": [],
      "workDurationInMinutes": 0,
      "timeSlots": []
    }
  ]
}
```
---

#### Scenario `SPL-NEG-02`: ShortCode length < 7 ('SPL01')
- **Endpoint:** `POST https://attendance2.dev.zoolwork.com/api/companies/3a249871-7a8d-dec5-2d72-47795dd2662d/worktemplates/split?locationId=3a24d646-b3cf-b1d4-61bb-1adf094b52fc`
- **Execution Result:** HTTP `400` -> **PASS**
- **API Error:** `Cit.Attendance:Validation` | `ShortCode must be exactly 7 letters or digits.`

**Request Payload:**
```json
{
  "templateName": {
    "en": "Split Location Shift SPL01",
    "ar": "\u0648\u0631\u062f\u064a\u0629 \u0645\u062c\u0632\u0623\u0629 SPL01"
  },
  "shortCode": "SPL01",
  "templateType": 3,
  "totalWorkDurationInMinutes": 2400,
  "totalWorkingDays": 5,
  "totalDaysOff": 2,
  "timeZoneId": "Asia/Riyadh",
  "splitTimeSlots": [
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
      "workDurationInMinutes": 480,
      "timeSlots": [
        {
          "startTime": "08:00:00",
          "endTime": "12:00:00",
          "workDurationInMinutes": 240
        },
        {
          "startTime": "14:00:00",
          "endTime": "18:00:00",
          "workDurationInMinutes": 240
        }
      ]
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
      "workDurationInMinutes": 480,
      "timeSlots": [
        {
          "startTime": "08:00:00",
          "endTime": "12:00:00",
          "workDurationInMinutes": 240
        },
        {
          "startTime": "14:00:00",
          "endTime": "18:00:00",
          "workDurationInMinutes": 240
        }
      ]
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
      "workDurationInMinutes": 480,
      "timeSlots": [
        {
          "startTime": "08:00:00",
          "endTime": "12:00:00",
          "workDurationInMinutes": 240
        },
        {
          "startTime": "14:00:00",
          "endTime": "18:00:00",
          "workDurationInMinutes": 240
        }
      ]
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
      "workDurationInMinutes": 480,
      "timeSlots": [
        {
          "startTime": "08:00:00",
          "endTime": "12:00:00",
          "workDurationInMinutes": 240
        },
        {
          "startTime": "14:00:00",
          "endTime": "18:00:00",
          "workDurationInMinutes": 240
        }
      ]
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
      "workDurationInMinutes": 480,
      "timeSlots": [
        {
          "startTime": "08:00:00",
          "endTime": "12:00:00",
          "workDurationInMinutes": 240
        },
        {
          "startTime": "14:00:00",
          "endTime": "18:00:00",
          "workDurationInMinutes": 240
        }
      ]
    },
    {
      "dayEnum": 6,
      "isWorkingDay": false,
      "recurrenceOfMonth": [],
      "workDurationInMinutes": 0,
      "timeSlots": []
    },
    {
      "dayEnum": 7,
      "isWorkingDay": false,
      "recurrenceOfMonth": [],
      "workDurationInMinutes": 0,
      "timeSlots": []
    }
  ]
}
```
---

#### Scenario `SPL-NEG-03`: Duplicate shortCode (SPD0001)
- **Endpoint:** `POST https://attendance2.dev.zoolwork.com/api/companies/3a249871-7a8d-dec5-2d72-47795dd2662d/worktemplates/split?locationId=3a24d646-b3cf-b1d4-61bb-1adf094b52fc`
- **Execution Result:** HTTP `400` -> **PASS**
- **API Error:** `Cit.Attendance:1106` | `This short code is already used by another work template in this company. Choose a different code.`

**Request Payload:**
```json
{
  "templateName": {
    "en": "Split Location Shift SPD0001",
    "ar": "\u0648\u0631\u062f\u064a\u0629 \u0645\u062c\u0632\u0623\u0629 SPD0001"
  },
  "shortCode": "SPD0001",
  "templateType": 3,
  "totalWorkDurationInMinutes": 2400,
  "totalWorkingDays": 5,
  "totalDaysOff": 2,
  "timeZoneId": "Asia/Riyadh",
  "splitTimeSlots": [
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
      "workDurationInMinutes": 480,
      "timeSlots": [
        {
          "startTime": "08:00:00",
          "endTime": "12:00:00",
          "workDurationInMinutes": 240
        },
        {
          "startTime": "14:00:00",
          "endTime": "18:00:00",
          "workDurationInMinutes": 240
        }
      ]
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
      "workDurationInMinutes": 480,
      "timeSlots": [
        {
          "startTime": "08:00:00",
          "endTime": "12:00:00",
          "workDurationInMinutes": 240
        },
        {
          "startTime": "14:00:00",
          "endTime": "18:00:00",
          "workDurationInMinutes": 240
        }
      ]
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
      "workDurationInMinutes": 480,
      "timeSlots": [
        {
          "startTime": "08:00:00",
          "endTime": "12:00:00",
          "workDurationInMinutes": 240
        },
        {
          "startTime": "14:00:00",
          "endTime": "18:00:00",
          "workDurationInMinutes": 240
        }
      ]
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
      "workDurationInMinutes": 480,
      "timeSlots": [
        {
          "startTime": "08:00:00",
          "endTime": "12:00:00",
          "workDurationInMinutes": 240
        },
        {
          "startTime": "14:00:00",
          "endTime": "18:00:00",
          "workDurationInMinutes": 240
        }
      ]
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
      "workDurationInMinutes": 480,
      "timeSlots": [
        {
          "startTime": "08:00:00",
          "endTime": "12:00:00",
          "workDurationInMinutes": 240
        },
        {
          "startTime": "14:00:00",
          "endTime": "18:00:00",
          "workDurationInMinutes": 240
        }
      ]
    },
    {
      "dayEnum": 6,
      "isWorkingDay": false,
      "recurrenceOfMonth": [],
      "workDurationInMinutes": 0,
      "timeSlots": []
    },
    {
      "dayEnum": 7,
      "isWorkingDay": false,
      "recurrenceOfMonth": [],
      "workDurationInMinutes": 0,
      "timeSlots": []
    }
  ]
}
```
---

#### Scenario `SPL-NEG-04`: Overlapping split intervals (1 hr overlap)
- **Endpoint:** `POST https://attendance2.dev.zoolwork.com/api/companies/3a249871-7a8d-dec5-2d72-47795dd2662d/worktemplates/split?locationId=3a24d646-b3cf-b1d4-61bb-1adf094b52fc`
- **Execution Result:** HTTP `400` -> **PASS**
- **API Error:** `Cit.Attendance:Validation` | `Split intervals must be in shift order, must not overlap, need a break between them and must fit within 23 hours 59 minutes. An interval may cross midnight.`

**Request Payload:**
```json
{
  "templateName": {
    "en": "Split Location Shift SPDNEG4",
    "ar": "\u0648\u0631\u062f\u064a\u0629 \u0645\u062c\u0632\u0623\u0629 SPDNEG4"
  },
  "shortCode": "SPDNEG4",
  "templateType": 3,
  "totalWorkDurationInMinutes": 2460,
  "totalWorkingDays": 5,
  "totalDaysOff": 2,
  "timeZoneId": "Asia/Riyadh",
  "splitTimeSlots": [
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
      "workDurationInMinutes": 540,
      "timeSlots": [
        {
          "startTime": "08:00:00",
          "endTime": "13:00:00",
          "workDurationInMinutes": 300
        },
        {
          "startTime": "12:00:00",
          "endTime": "16:00:00",
          "workDurationInMinutes": 240
        }
      ]
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
      "workDurationInMinutes": 480,
      "timeSlots": [
        {
          "startTime": "08:00:00",
          "endTime": "12:00:00",
          "workDurationInMinutes": 240
        },
        {
          "startTime": "14:00:00",
          "endTime": "18:00:00",
          "workDurationInMinutes": 240
        }
      ]
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
      "workDurationInMinutes": 480,
      "timeSlots": [
        {
          "startTime": "08:00:00",
          "endTime": "12:00:00",
          "workDurationInMinutes": 240
        },
        {
          "startTime": "14:00:00",
          "endTime": "18:00:00",
          "workDurationInMinutes": 240
        }
      ]
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
      "workDurationInMinutes": 480,
      "timeSlots": [
        {
          "startTime": "08:00:00",
          "endTime": "12:00:00",
          "workDurationInMinutes": 240
        },
        {
          "startTime": "14:00:00",
          "endTime": "18:00:00",
          "workDurationInMinutes": 240
        }
      ]
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
      "workDurationInMinutes": 480,
      "timeSlots": [
        {
          "startTime": "08:00:00",
          "endTime": "12:00:00",
          "workDurationInMinutes": 240
        },
        {
          "startTime": "14:00:00",
          "endTime": "18:00:00",
          "workDurationInMinutes": 240
        }
      ]
    },
    {
      "dayEnum": 6,
      "isWorkingDay": false,
      "recurrenceOfMonth": [],
      "workDurationInMinutes": 0,
      "timeSlots": []
    },
    {
      "dayEnum": 7,
      "isWorkingDay": false,
      "recurrenceOfMonth": [],
      "workDurationInMinutes": 0,
      "timeSlots": []
    }
  ]
}
```
---

#### Scenario `SPL-NEG-05`: Zero break gap between intervals (12:00 to 12:00)
- **Endpoint:** `POST https://attendance2.dev.zoolwork.com/api/companies/3a249871-7a8d-dec5-2d72-47795dd2662d/worktemplates/split?locationId=3a24d646-b3cf-b1d4-61bb-1adf094b52fc`
- **Execution Result:** HTTP `400` -> **PASS**
- **API Error:** `Cit.Attendance:Validation` | `Split intervals must be in shift order, must not overlap, need a break between them and must fit within 23 hours 59 minutes. An interval may cross midnight.`

**Request Payload:**
```json
{
  "templateName": {
    "en": "Split Location Shift SPDNEG5",
    "ar": "\u0648\u0631\u062f\u064a\u0629 \u0645\u062c\u0632\u0623\u0629 SPDNEG5"
  },
  "shortCode": "SPDNEG5",
  "templateType": 3,
  "totalWorkDurationInMinutes": 2400,
  "totalWorkingDays": 5,
  "totalDaysOff": 2,
  "timeZoneId": "Asia/Riyadh",
  "splitTimeSlots": [
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
      "workDurationInMinutes": 480,
      "timeSlots": [
        {
          "startTime": "08:00:00",
          "endTime": "12:00:00",
          "workDurationInMinutes": 240
        },
        {
          "startTime": "12:00:00",
          "endTime": "16:00:00",
          "workDurationInMinutes": 240
        }
      ]
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
      "workDurationInMinutes": 480,
      "timeSlots": [
        {
          "startTime": "08:00:00",
          "endTime": "12:00:00",
          "workDurationInMinutes": 240
        },
        {
          "startTime": "14:00:00",
          "endTime": "18:00:00",
          "workDurationInMinutes": 240
        }
      ]
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
      "workDurationInMinutes": 480,
      "timeSlots": [
        {
          "startTime": "08:00:00",
          "endTime": "12:00:00",
          "workDurationInMinutes": 240
        },
        {
          "startTime": "14:00:00",
          "endTime": "18:00:00",
          "workDurationInMinutes": 240
        }
      ]
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
      "workDurationInMinutes": 480,
      "timeSlots": [
        {
          "startTime": "08:00:00",
          "endTime": "12:00:00",
          "workDurationInMinutes": 240
        },
        {
          "startTime": "14:00:00",
          "endTime": "18:00:00",
          "workDurationInMinutes": 240
        }
      ]
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
      "workDurationInMinutes": 480,
      "timeSlots": [
        {
          "startTime": "08:00:00",
          "endTime": "12:00:00",
          "workDurationInMinutes": 240
        },
        {
          "startTime": "14:00:00",
          "endTime": "18:00:00",
          "workDurationInMinutes": 240
        }
      ]
    },
    {
      "dayEnum": 6,
      "isWorkingDay": false,
      "recurrenceOfMonth": [],
      "workDurationInMinutes": 0,
      "timeSlots": []
    },
    {
      "dayEnum": 7,
      "isWorkingDay": false,
      "recurrenceOfMonth": [],
      "workDurationInMinutes": 0,
      "timeSlots": []
    }
  ]
}
```
---

#### Scenario `SPL-NEG-06`: Inverted split interval (startTime 12:00 > endTime 08:00)
- **Endpoint:** `POST https://attendance2.dev.zoolwork.com/api/companies/3a249871-7a8d-dec5-2d72-47795dd2662d/worktemplates/split?locationId=3a24d646-b3cf-b1d4-61bb-1adf094b52fc`
- **Execution Result:** HTTP `400` -> **PASS**
- **API Error:** `Cit.Attendance:Validation` | `Split intervals must be in shift order, must not overlap, need a break between them and must fit within 23 hours 59 minutes. An interval may cross midnight. Each split interval's duration must equal its time range, and the day's duration must equal the sum of its intervals.`

**Request Payload:**
```json
{
  "templateName": {
    "en": "Split Location Shift SPDNEG6",
    "ar": "\u0648\u0631\u062f\u064a\u0629 \u0645\u062c\u0632\u0623\u0629 SPDNEG6"
  },
  "shortCode": "SPDNEG6",
  "templateType": 3,
  "totalWorkDurationInMinutes": 2400,
  "totalWorkingDays": 5,
  "totalDaysOff": 2,
  "timeZoneId": "Asia/Riyadh",
  "splitTimeSlots": [
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
      "workDurationInMinutes": 480,
      "timeSlots": [
        {
          "startTime": "12:00:00",
          "endTime": "08:00:00",
          "workDurationInMinutes": 240
        },
        {
          "startTime": "14:00:00",
          "endTime": "18:00:00",
          "workDurationInMinutes": 240
        }
      ]
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
      "workDurationInMinutes": 480,
      "timeSlots": [
        {
          "startTime": "08:00:00",
          "endTime": "12:00:00",
          "workDurationInMinutes": 240
        },
        {
          "startTime": "14:00:00",
          "endTime": "18:00:00",
          "workDurationInMinutes": 240
        }
      ]
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
      "workDurationInMinutes": 480,
      "timeSlots": [
        {
          "startTime": "08:00:00",
          "endTime": "12:00:00",
          "workDurationInMinutes": 240
        },
        {
          "startTime": "14:00:00",
          "endTime": "18:00:00",
          "workDurationInMinutes": 240
        }
      ]
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
      "workDurationInMinutes": 480,
      "timeSlots": [
        {
          "startTime": "08:00:00",
          "endTime": "12:00:00",
          "workDurationInMinutes": 240
        },
        {
          "startTime": "14:00:00",
          "endTime": "18:00:00",
          "workDurationInMinutes": 240
        }
      ]
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
      "workDurationInMinutes": 480,
      "timeSlots": [
        {
          "startTime": "08:00:00",
          "endTime": "12:00:00",
          "workDurationInMinutes": 240
        },
        {
          "startTime": "14:00:00",
          "endTime": "18:00:00",
          "workDurationInMinutes": 240
        }
      ]
    },
    {
      "dayEnum": 6,
      "isWorkingDay": false,
      "recurrenceOfMonth": [],
      "workDurationInMinutes": 0,
      "timeSlots": []
    },
    {
      "dayEnum": 7,
      "isWorkingDay": false,
      "recurrenceOfMonth": [],
      "workDurationInMinutes": 0,
      "timeSlots": []
    }
  ]
}
```
---

#### Scenario `SPL-NEG-07`: Empty timeSlots array on working day
- **Endpoint:** `POST https://attendance2.dev.zoolwork.com/api/companies/3a249871-7a8d-dec5-2d72-47795dd2662d/worktemplates/split?locationId=3a24d646-b3cf-b1d4-61bb-1adf094b52fc`
- **Execution Result:** HTTP `400` -> **PASS**
- **API Error:** `Cit.Attendance:Validation` | `A split working day needs at least one interval.`

**Request Payload:**
```json
{
  "templateName": {
    "en": "Split Location Shift SPDNEG7",
    "ar": "\u0648\u0631\u062f\u064a\u0629 \u0645\u062c\u0632\u0623\u0629 SPDNEG7"
  },
  "shortCode": "SPDNEG7",
  "templateType": 3,
  "totalWorkDurationInMinutes": 2400,
  "totalWorkingDays": 5,
  "totalDaysOff": 2,
  "timeZoneId": "Asia/Riyadh",
  "splitTimeSlots": [
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
      "workDurationInMinutes": 480,
      "timeSlots": []
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
      "workDurationInMinutes": 480,
      "timeSlots": [
        {
          "startTime": "08:00:00",
          "endTime": "12:00:00",
          "workDurationInMinutes": 240
        },
        {
          "startTime": "14:00:00",
          "endTime": "18:00:00",
          "workDurationInMinutes": 240
        }
      ]
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
      "workDurationInMinutes": 480,
      "timeSlots": [
        {
          "startTime": "08:00:00",
          "endTime": "12:00:00",
          "workDurationInMinutes": 240
        },
        {
          "startTime": "14:00:00",
          "endTime": "18:00:00",
          "workDurationInMinutes": 240
        }
      ]
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
      "workDurationInMinutes": 480,
      "timeSlots": [
        {
          "startTime": "08:00:00",
          "endTime": "12:00:00",
          "workDurationInMinutes": 240
        },
        {
          "startTime": "14:00:00",
          "endTime": "18:00:00",
          "workDurationInMinutes": 240
        }
      ]
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
      "workDurationInMinutes": 480,
      "timeSlots": [
        {
          "startTime": "08:00:00",
          "endTime": "12:00:00",
          "workDurationInMinutes": 240
        },
        {
          "startTime": "14:00:00",
          "endTime": "18:00:00",
          "workDurationInMinutes": 240
        }
      ]
    },
    {
      "dayEnum": 6,
      "isWorkingDay": false,
      "recurrenceOfMonth": [],
      "workDurationInMinutes": 0,
      "timeSlots": []
    },
    {
      "dayEnum": 7,
      "isWorkingDay": false,
      "recurrenceOfMonth": [],
      "workDurationInMinutes": 0,
      "timeSlots": []
    }
  ]
}
```
---

#### Scenario `SPL-NEG-08`: Interval duration does not equal (endTime - startTime)
- **Endpoint:** `POST https://attendance2.dev.zoolwork.com/api/companies/3a249871-7a8d-dec5-2d72-47795dd2662d/worktemplates/split?locationId=3a24d646-b3cf-b1d4-61bb-1adf094b52fc`
- **Execution Result:** HTTP `400` -> **PASS**
- **API Error:** `Cit.Attendance:Validation` | `Each split interval's duration must equal its time range, and the day's duration must equal the sum of its intervals.`

**Request Payload:**
```json
{
  "templateName": {
    "en": "Split Location Shift SPDNEG8",
    "ar": "\u0648\u0631\u062f\u064a\u0629 \u0645\u062c\u0632\u0623\u0629 SPDNEG8"
  },
  "shortCode": "SPDNEG8",
  "templateType": 3,
  "totalWorkDurationInMinutes": 2400,
  "totalWorkingDays": 5,
  "totalDaysOff": 2,
  "timeZoneId": "Asia/Riyadh",
  "splitTimeSlots": [
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
      "workDurationInMinutes": 480,
      "timeSlots": [
        {
          "startTime": "08:00:00",
          "endTime": "12:00:00",
          "workDurationInMinutes": 180
        },
        {
          "startTime": "14:00:00",
          "endTime": "18:00:00",
          "workDurationInMinutes": 240
        }
      ]
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
      "workDurationInMinutes": 480,
      "timeSlots": [
        {
          "startTime": "08:00:00",
          "endTime": "12:00:00",
          "workDurationInMinutes": 240
        },
        {
          "startTime": "14:00:00",
          "endTime": "18:00:00",
          "workDurationInMinutes": 240
        }
      ]
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
      "workDurationInMinutes": 480,
      "timeSlots": [
        {
          "startTime": "08:00:00",
          "endTime": "12:00:00",
          "workDurationInMinutes": 240
        },
        {
          "startTime": "14:00:00",
          "endTime": "18:00:00",
          "workDurationInMinutes": 240
        }
      ]
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
      "workDurationInMinutes": 480,
      "timeSlots": [
        {
          "startTime": "08:00:00",
          "endTime": "12:00:00",
          "workDurationInMinutes": 240
        },
        {
          "startTime": "14:00:00",
          "endTime": "18:00:00",
          "workDurationInMinutes": 240
        }
      ]
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
      "workDurationInMinutes": 480,
      "timeSlots": [
        {
          "startTime": "08:00:00",
          "endTime": "12:00:00",
          "workDurationInMinutes": 240
        },
        {
          "startTime": "14:00:00",
          "endTime": "18:00:00",
          "workDurationInMinutes": 240
        }
      ]
    },
    {
      "dayEnum": 6,
      "isWorkingDay": false,
      "recurrenceOfMonth": [],
      "workDurationInMinutes": 0,
      "timeSlots": []
    },
    {
      "dayEnum": 7,
      "isWorkingDay": false,
      "recurrenceOfMonth": [],
      "workDurationInMinutes": 0,
      "timeSlots": []
    }
  ]
}
```
---

#### Scenario `SPL-NEG-09`: Daily duration does not equal interval sum (600 vs 480)
- **Endpoint:** `POST https://attendance2.dev.zoolwork.com/api/companies/3a249871-7a8d-dec5-2d72-47795dd2662d/worktemplates/split?locationId=3a24d646-b3cf-b1d4-61bb-1adf094b52fc`
- **Execution Result:** HTTP `400` -> **PASS**
- **API Error:** `Cit.Attendance:Validation` | `Each split interval's duration must equal its time range, and the day's duration must equal the sum of its intervals.`

**Request Payload:**
```json
{
  "templateName": {
    "en": "Split Location Shift SPDNEG9",
    "ar": "\u0648\u0631\u062f\u064a\u0629 \u0645\u062c\u0632\u0623\u0629 SPDNEG9"
  },
  "shortCode": "SPDNEG9",
  "templateType": 3,
  "totalWorkDurationInMinutes": 2520,
  "totalWorkingDays": 5,
  "totalDaysOff": 2,
  "timeZoneId": "Asia/Riyadh",
  "splitTimeSlots": [
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
      "workDurationInMinutes": 600,
      "timeSlots": [
        {
          "startTime": "08:00:00",
          "endTime": "12:00:00",
          "workDurationInMinutes": 240
        },
        {
          "startTime": "14:00:00",
          "endTime": "18:00:00",
          "workDurationInMinutes": 240
        }
      ]
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
      "workDurationInMinutes": 480,
      "timeSlots": [
        {
          "startTime": "08:00:00",
          "endTime": "12:00:00",
          "workDurationInMinutes": 240
        },
        {
          "startTime": "14:00:00",
          "endTime": "18:00:00",
          "workDurationInMinutes": 240
        }
      ]
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
      "workDurationInMinutes": 480,
      "timeSlots": [
        {
          "startTime": "08:00:00",
          "endTime": "12:00:00",
          "workDurationInMinutes": 240
        },
        {
          "startTime": "14:00:00",
          "endTime": "18:00:00",
          "workDurationInMinutes": 240
        }
      ]
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
      "workDurationInMinutes": 480,
      "timeSlots": [
        {
          "startTime": "08:00:00",
          "endTime": "12:00:00",
          "workDurationInMinutes": 240
        },
        {
          "startTime": "14:00:00",
          "endTime": "18:00:00",
          "workDurationInMinutes": 240
        }
      ]
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
      "workDurationInMinutes": 480,
      "timeSlots": [
        {
          "startTime": "08:00:00",
          "endTime": "12:00:00",
          "workDurationInMinutes": 240
        },
        {
          "startTime": "14:00:00",
          "endTime": "18:00:00",
          "workDurationInMinutes": 240
        }
      ]
    },
    {
      "dayEnum": 6,
      "isWorkingDay": false,
      "recurrenceOfMonth": [],
      "workDurationInMinutes": 0,
      "timeSlots": []
    },
    {
      "dayEnum": 7,
      "isWorkingDay": false,
      "recurrenceOfMonth": [],
      "workDurationInMinutes": 0,
      "timeSlots": []
    }
  ]
}
```
---

#### Scenario `SPL-NEG-10`: Total duration mismatch in Split (3000 vs 2400)
- **Endpoint:** `POST https://attendance2.dev.zoolwork.com/api/companies/3a249871-7a8d-dec5-2d72-47795dd2662d/worktemplates/split?locationId=3a24d646-b3cf-b1d4-61bb-1adf094b52fc`
- **Execution Result:** HTTP `200` -> **FAIL**
- **MongoDB `_id`:** `bdedeb03-6630-444b-8102-a04c6c59559e`

**Request Payload:**
```json
{
  "templateName": {
    "en": "Split Location Shift SPDNE10",
    "ar": "\u0648\u0631\u062f\u064a\u0629 \u0645\u062c\u0632\u0623\u0629 SPDNE10"
  },
  "shortCode": "SPDNE10",
  "templateType": 3,
  "totalWorkDurationInMinutes": 3000,
  "totalWorkingDays": 5,
  "totalDaysOff": 2,
  "timeZoneId": "Asia/Riyadh",
  "splitTimeSlots": [
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
      "workDurationInMinutes": 480,
      "timeSlots": [
        {
          "startTime": "08:00:00",
          "endTime": "12:00:00",
          "workDurationInMinutes": 240
        },
        {
          "startTime": "14:00:00",
          "endTime": "18:00:00",
          "workDurationInMinutes": 240
        }
      ]
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
      "workDurationInMinutes": 480,
      "timeSlots": [
        {
          "startTime": "08:00:00",
          "endTime": "12:00:00",
          "workDurationInMinutes": 240
        },
        {
          "startTime": "14:00:00",
          "endTime": "18:00:00",
          "workDurationInMinutes": 240
        }
      ]
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
      "workDurationInMinutes": 480,
      "timeSlots": [
        {
          "startTime": "08:00:00",
          "endTime": "12:00:00",
          "workDurationInMinutes": 240
        },
        {
          "startTime": "14:00:00",
          "endTime": "18:00:00",
          "workDurationInMinutes": 240
        }
      ]
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
      "workDurationInMinutes": 480,
      "timeSlots": [
        {
          "startTime": "08:00:00",
          "endTime": "12:00:00",
          "workDurationInMinutes": 240
        },
        {
          "startTime": "14:00:00",
          "endTime": "18:00:00",
          "workDurationInMinutes": 240
        }
      ]
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
      "workDurationInMinutes": 480,
      "timeSlots": [
        {
          "startTime": "08:00:00",
          "endTime": "12:00:00",
          "workDurationInMinutes": 240
        },
        {
          "startTime": "14:00:00",
          "endTime": "18:00:00",
          "workDurationInMinutes": 240
        }
      ]
    },
    {
      "dayEnum": 6,
      "isWorkingDay": false,
      "recurrenceOfMonth": [],
      "workDurationInMinutes": 0,
      "timeSlots": []
    },
    {
      "dayEnum": 7,
      "isWorkingDay": false,
      "recurrenceOfMonth": [],
      "workDurationInMinutes": 0,
      "timeSlots": []
    }
  ]
}
```
---

#### Scenario `SPL-PAT-01`: Update Split template name
- **Endpoint:** `PATCH https://attendance2.dev.zoolwork.com/api/companies/3a249871-7a8d-dec5-2d72-47795dd2662d/worktemplates/split/ab6bb972-24e9-4b3c-9c23-55ef8770f6e5?locationId=3a24d646-b3cf-b1d4-61bb-1adf094b52fc`
- **Execution Result:** HTTP `200` -> **PASS**
- **MongoDB `_id`:** `ab6bb972-24e9-4b3c-9c23-55ef8770f6e5`

**Request Payload:**
```json
{
  "templateName": {
    "en": "Split Location Shift Updated",
    "ar": "\u0648\u0631\u062f\u064a\u0629 \u0645\u062c\u0632\u0623\u0629 \u0645\u062d\u062f\u062b\u0629"
  },
  "shortCode": "SPD0001",
  "templateType": 3,
  "totalWorkDurationInMinutes": 2400,
  "totalWorkingDays": 5,
  "totalDaysOff": 2,
  "timeZoneId": "Asia/Riyadh",
  "splitTimeSlots": [
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
      "workDurationInMinutes": 480,
      "timeSlots": [
        {
          "startTime": "08:00:00",
          "endTime": "12:00:00",
          "workDurationInMinutes": 240
        },
        {
          "startTime": "14:00:00",
          "endTime": "18:00:00",
          "workDurationInMinutes": 240
        }
      ]
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
      "workDurationInMinutes": 480,
      "timeSlots": [
        {
          "startTime": "08:00:00",
          "endTime": "12:00:00",
          "workDurationInMinutes": 240
        },
        {
          "startTime": "14:00:00",
          "endTime": "18:00:00",
          "workDurationInMinutes": 240
        }
      ]
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
      "workDurationInMinutes": 480,
      "timeSlots": [
        {
          "startTime": "08:00:00",
          "endTime": "12:00:00",
          "workDurationInMinutes": 240
        },
        {
          "startTime": "14:00:00",
          "endTime": "18:00:00",
          "workDurationInMinutes": 240
        }
      ]
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
      "workDurationInMinutes": 480,
      "timeSlots": [
        {
          "startTime": "08:00:00",
          "endTime": "12:00:00",
          "workDurationInMinutes": 240
        },
        {
          "startTime": "14:00:00",
          "endTime": "18:00:00",
          "workDurationInMinutes": 240
        }
      ]
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
      "workDurationInMinutes": 480,
      "timeSlots": [
        {
          "startTime": "08:00:00",
          "endTime": "12:00:00",
          "workDurationInMinutes": 240
        },
        {
          "startTime": "14:00:00",
          "endTime": "18:00:00",
          "workDurationInMinutes": 240
        }
      ]
    },
    {
      "dayEnum": 6,
      "isWorkingDay": false,
      "recurrenceOfMonth": [],
      "workDurationInMinutes": 0,
      "timeSlots": []
    },
    {
      "dayEnum": 7,
      "isWorkingDay": false,
      "recurrenceOfMonth": [],
      "workDurationInMinutes": 0,
      "timeSlots": []
    }
  ]
}
```
---

#### Scenario `SPL-PAT-02`: Update Split interval timings (09-13 & 15-19)
- **Endpoint:** `PATCH https://attendance2.dev.zoolwork.com/api/companies/3a249871-7a8d-dec5-2d72-47795dd2662d/worktemplates/split/ab6bb972-24e9-4b3c-9c23-55ef8770f6e5?locationId=3a24d646-b3cf-b1d4-61bb-1adf094b52fc`
- **Execution Result:** HTTP `200` -> **PASS**
- **MongoDB `_id`:** `ab6bb972-24e9-4b3c-9c23-55ef8770f6e5`

**Request Payload:**
```json
{
  "templateName": {
    "en": "Split Location Shift SPD0001",
    "ar": "\u0648\u0631\u062f\u064a\u0629 \u0645\u062c\u0632\u0623\u0629 SPD0001"
  },
  "shortCode": "SPD0001",
  "templateType": 3,
  "totalWorkDurationInMinutes": 2400,
  "totalWorkingDays": 5,
  "totalDaysOff": 2,
  "timeZoneId": "Asia/Riyadh",
  "splitTimeSlots": [
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
      "workDurationInMinutes": 480,
      "timeSlots": [
        {
          "startTime": "09:00:00",
          "endTime": "13:00:00",
          "workDurationInMinutes": 240
        },
        {
          "startTime": "15:00:00",
          "endTime": "19:00:00",
          "workDurationInMinutes": 240
        }
      ]
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
      "workDurationInMinutes": 480,
      "timeSlots": [
        {
          "startTime": "09:00:00",
          "endTime": "13:00:00",
          "workDurationInMinutes": 240
        },
        {
          "startTime": "15:00:00",
          "endTime": "19:00:00",
          "workDurationInMinutes": 240
        }
      ]
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
      "workDurationInMinutes": 480,
      "timeSlots": [
        {
          "startTime": "09:00:00",
          "endTime": "13:00:00",
          "workDurationInMinutes": 240
        },
        {
          "startTime": "15:00:00",
          "endTime": "19:00:00",
          "workDurationInMinutes": 240
        }
      ]
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
      "workDurationInMinutes": 480,
      "timeSlots": [
        {
          "startTime": "09:00:00",
          "endTime": "13:00:00",
          "workDurationInMinutes": 240
        },
        {
          "startTime": "15:00:00",
          "endTime": "19:00:00",
          "workDurationInMinutes": 240
        }
      ]
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
      "workDurationInMinutes": 480,
      "timeSlots": [
        {
          "startTime": "09:00:00",
          "endTime": "13:00:00",
          "workDurationInMinutes": 240
        },
        {
          "startTime": "15:00:00",
          "endTime": "19:00:00",
          "workDurationInMinutes": 240
        }
      ]
    },
    {
      "dayEnum": 6,
      "isWorkingDay": false,
      "recurrenceOfMonth": [],
      "workDurationInMinutes": 0,
      "timeSlots": []
    },
    {
      "dayEnum": 7,
      "isWorkingDay": false,
      "recurrenceOfMonth": [],
      "workDurationInMinutes": 0,
      "timeSlots": []
    }
  ]
}
```
---

#### Scenario `SPL-PAT-03`: Update timezone to Asia/Dubai
- **Endpoint:** `PATCH https://attendance2.dev.zoolwork.com/api/companies/3a249871-7a8d-dec5-2d72-47795dd2662d/worktemplates/split/ab6bb972-24e9-4b3c-9c23-55ef8770f6e5?locationId=3a24d646-b3cf-b1d4-61bb-1adf094b52fc`
- **Execution Result:** HTTP `200` -> **PASS**
- **MongoDB `_id`:** `ab6bb972-24e9-4b3c-9c23-55ef8770f6e5`

**Request Payload:**
```json
{
  "templateName": {
    "en": "Split Location Shift SPD0001",
    "ar": "\u0648\u0631\u062f\u064a\u0629 \u0645\u062c\u0632\u0623\u0629 SPD0001"
  },
  "shortCode": "SPD0001",
  "templateType": 3,
  "totalWorkDurationInMinutes": 2400,
  "totalWorkingDays": 5,
  "totalDaysOff": 2,
  "timeZoneId": "Asia/Dubai",
  "splitTimeSlots": [
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
      "workDurationInMinutes": 480,
      "timeSlots": [
        {
          "startTime": "08:00:00",
          "endTime": "12:00:00",
          "workDurationInMinutes": 240
        },
        {
          "startTime": "14:00:00",
          "endTime": "18:00:00",
          "workDurationInMinutes": 240
        }
      ]
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
      "workDurationInMinutes": 480,
      "timeSlots": [
        {
          "startTime": "08:00:00",
          "endTime": "12:00:00",
          "workDurationInMinutes": 240
        },
        {
          "startTime": "14:00:00",
          "endTime": "18:00:00",
          "workDurationInMinutes": 240
        }
      ]
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
      "workDurationInMinutes": 480,
      "timeSlots": [
        {
          "startTime": "08:00:00",
          "endTime": "12:00:00",
          "workDurationInMinutes": 240
        },
        {
          "startTime": "14:00:00",
          "endTime": "18:00:00",
          "workDurationInMinutes": 240
        }
      ]
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
      "workDurationInMinutes": 480,
      "timeSlots": [
        {
          "startTime": "08:00:00",
          "endTime": "12:00:00",
          "workDurationInMinutes": 240
        },
        {
          "startTime": "14:00:00",
          "endTime": "18:00:00",
          "workDurationInMinutes": 240
        }
      ]
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
      "workDurationInMinutes": 480,
      "timeSlots": [
        {
          "startTime": "08:00:00",
          "endTime": "12:00:00",
          "workDurationInMinutes": 240
        },
        {
          "startTime": "14:00:00",
          "endTime": "18:00:00",
          "workDurationInMinutes": 240
        }
      ]
    },
    {
      "dayEnum": 6,
      "isWorkingDay": false,
      "recurrenceOfMonth": [],
      "workDurationInMinutes": 0,
      "timeSlots": []
    },
    {
      "dayEnum": 7,
      "isWorkingDay": false,
      "recurrenceOfMonth": [],
      "workDurationInMinutes": 0,
      "timeSlots": []
    }
  ]
}
```
---

#### Scenario `SPL-PAT-04`: Attempt to alter shortCode in Split PATCH (Cit.Attendance:1107)
- **Endpoint:** `PATCH https://attendance2.dev.zoolwork.com/api/companies/3a249871-7a8d-dec5-2d72-47795dd2662d/worktemplates/split/ab6bb972-24e9-4b3c-9c23-55ef8770f6e5?locationId=3a24d646-b3cf-b1d4-61bb-1adf094b52fc`
- **Execution Result:** HTTP `400` -> **PASS**
- **API Error:** `Cit.Attendance:1107` | `A work template's short code cannot be changed after it is created.`

**Request Payload:**
```json
{
  "templateName": {
    "en": "Split Location Shift SPDCHG1",
    "ar": "\u0648\u0631\u062f\u064a\u0629 \u0645\u062c\u0632\u0623\u0629 SPDCHG1"
  },
  "shortCode": "SPDCHG1",
  "templateType": 3,
  "totalWorkDurationInMinutes": 2400,
  "totalWorkingDays": 5,
  "totalDaysOff": 2,
  "timeZoneId": "Asia/Riyadh",
  "splitTimeSlots": [
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
      "workDurationInMinutes": 480,
      "timeSlots": [
        {
          "startTime": "08:00:00",
          "endTime": "12:00:00",
          "workDurationInMinutes": 240
        },
        {
          "startTime": "14:00:00",
          "endTime": "18:00:00",
          "workDurationInMinutes": 240
        }
      ]
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
      "workDurationInMinutes": 480,
      "timeSlots": [
        {
          "startTime": "08:00:00",
          "endTime": "12:00:00",
          "workDurationInMinutes": 240
        },
        {
          "startTime": "14:00:00",
          "endTime": "18:00:00",
          "workDurationInMinutes": 240
        }
      ]
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
      "workDurationInMinutes": 480,
      "timeSlots": [
        {
          "startTime": "08:00:00",
          "endTime": "12:00:00",
          "workDurationInMinutes": 240
        },
        {
          "startTime": "14:00:00",
          "endTime": "18:00:00",
          "workDurationInMinutes": 240
        }
      ]
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
      "workDurationInMinutes": 480,
      "timeSlots": [
        {
          "startTime": "08:00:00",
          "endTime": "12:00:00",
          "workDurationInMinutes": 240
        },
        {
          "startTime": "14:00:00",
          "endTime": "18:00:00",
          "workDurationInMinutes": 240
        }
      ]
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
      "workDurationInMinutes": 480,
      "timeSlots": [
        {
          "startTime": "08:00:00",
          "endTime": "12:00:00",
          "workDurationInMinutes": 240
        },
        {
          "startTime": "14:00:00",
          "endTime": "18:00:00",
          "workDurationInMinutes": 240
        }
      ]
    },
    {
      "dayEnum": 6,
      "isWorkingDay": false,
      "recurrenceOfMonth": [],
      "workDurationInMinutes": 0,
      "timeSlots": []
    },
    {
      "dayEnum": 7,
      "isWorkingDay": false,
      "recurrenceOfMonth": [],
      "workDurationInMinutes": 0,
      "timeSlots": []
    }
  ]
}
```
---

#### Scenario `SPL-PAT-05`: Overlapping intervals in Split PATCH
- **Endpoint:** `PATCH https://attendance2.dev.zoolwork.com/api/companies/3a249871-7a8d-dec5-2d72-47795dd2662d/worktemplates/split/ab6bb972-24e9-4b3c-9c23-55ef8770f6e5?locationId=3a24d646-b3cf-b1d4-61bb-1adf094b52fc`
- **Execution Result:** HTTP `400` -> **PASS**
- **API Error:** `Cit.Attendance:Validation` | `Split intervals must be in shift order, must not overlap, need a break between them and must fit within 23 hours 59 minutes. An interval may cross midnight. Each split interval's duration must equal its time range, and the day's duration must equal the sum of its intervals.`

**Request Payload:**
```json
{
  "templateName": {
    "en": "Split Location Shift SPD0001",
    "ar": "\u0648\u0631\u062f\u064a\u0629 \u0645\u062c\u0632\u0623\u0629 SPD0001"
  },
  "shortCode": "SPD0001",
  "templateType": 3,
  "totalWorkDurationInMinutes": 2400,
  "totalWorkingDays": 5,
  "totalDaysOff": 2,
  "timeZoneId": "Asia/Riyadh",
  "splitTimeSlots": [
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
      "workDurationInMinutes": 480,
      "timeSlots": [
        {
          "startTime": "08:00:00",
          "endTime": "13:00:00",
          "workDurationInMinutes": 300
        },
        {
          "startTime": "12:00:00",
          "endTime": "16:00:00",
          "workDurationInMinutes": 240
        }
      ]
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
      "workDurationInMinutes": 480,
      "timeSlots": [
        {
          "startTime": "08:00:00",
          "endTime": "12:00:00",
          "workDurationInMinutes": 240
        },
        {
          "startTime": "14:00:00",
          "endTime": "18:00:00",
          "workDurationInMinutes": 240
        }
      ]
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
      "workDurationInMinutes": 480,
      "timeSlots": [
        {
          "startTime": "08:00:00",
          "endTime": "12:00:00",
          "workDurationInMinutes": 240
        },
        {
          "startTime": "14:00:00",
          "endTime": "18:00:00",
          "workDurationInMinutes": 240
        }
      ]
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
      "workDurationInMinutes": 480,
      "timeSlots": [
        {
          "startTime": "08:00:00",
          "endTime": "12:00:00",
          "workDurationInMinutes": 240
        },
        {
          "startTime": "14:00:00",
          "endTime": "18:00:00",
          "workDurationInMinutes": 240
        }
      ]
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
      "workDurationInMinutes": 480,
      "timeSlots": [
        {
          "startTime": "08:00:00",
          "endTime": "12:00:00",
          "workDurationInMinutes": 240
        },
        {
          "startTime": "14:00:00",
          "endTime": "18:00:00",
          "workDurationInMinutes": 240
        }
      ]
    },
    {
      "dayEnum": 6,
      "isWorkingDay": false,
      "recurrenceOfMonth": [],
      "workDurationInMinutes": 0,
      "timeSlots": []
    },
    {
      "dayEnum": 7,
      "isWorkingDay": false,
      "recurrenceOfMonth": [],
      "workDurationInMinutes": 0,
      "timeSlots": []
    }
  ]
}
```
---

#### Scenario `SPL-PAT-06`: Recurrence [6] in Split PATCH
- **Endpoint:** `PATCH https://attendance2.dev.zoolwork.com/api/companies/3a249871-7a8d-dec5-2d72-47795dd2662d/worktemplates/split/ab6bb972-24e9-4b3c-9c23-55ef8770f6e5?locationId=3a24d646-b3cf-b1d4-61bb-1adf094b52fc`
- **Execution Result:** HTTP `200` -> **FAIL**
- **MongoDB `_id`:** `ab6bb972-24e9-4b3c-9c23-55ef8770f6e5`

**Request Payload:**
```json
{
  "templateName": {
    "en": "Split Location Shift SPD0001",
    "ar": "\u0648\u0631\u062f\u064a\u0629 \u0645\u062c\u0632\u0623\u0629 SPD0001"
  },
  "shortCode": "SPD0001",
  "templateType": 3,
  "totalWorkDurationInMinutes": 2400,
  "totalWorkingDays": 5,
  "totalDaysOff": 2,
  "timeZoneId": "Asia/Riyadh",
  "splitTimeSlots": [
    {
      "dayEnum": 1,
      "isWorkingDay": true,
      "recurrenceOfMonth": [
        6
      ],
      "workDurationInMinutes": 480,
      "timeSlots": [
        {
          "startTime": "08:00:00",
          "endTime": "12:00:00",
          "workDurationInMinutes": 240
        },
        {
          "startTime": "14:00:00",
          "endTime": "18:00:00",
          "workDurationInMinutes": 240
        }
      ]
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
      "workDurationInMinutes": 480,
      "timeSlots": [
        {
          "startTime": "08:00:00",
          "endTime": "12:00:00",
          "workDurationInMinutes": 240
        },
        {
          "startTime": "14:00:00",
          "endTime": "18:00:00",
          "workDurationInMinutes": 240
        }
      ]
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
      "workDurationInMinutes": 480,
      "timeSlots": [
        {
          "startTime": "08:00:00",
          "endTime": "12:00:00",
          "workDurationInMinutes": 240
        },
        {
          "startTime": "14:00:00",
          "endTime": "18:00:00",
          "workDurationInMinutes": 240
        }
      ]
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
      "workDurationInMinutes": 480,
      "timeSlots": [
        {
          "startTime": "08:00:00",
          "endTime": "12:00:00",
          "workDurationInMinutes": 240
        },
        {
          "startTime": "14:00:00",
          "endTime": "18:00:00",
          "workDurationInMinutes": 240
        }
      ]
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
      "workDurationInMinutes": 480,
      "timeSlots": [
        {
          "startTime": "08:00:00",
          "endTime": "12:00:00",
          "workDurationInMinutes": 240
        },
        {
          "startTime": "14:00:00",
          "endTime": "18:00:00",
          "workDurationInMinutes": 240
        }
      ]
    },
    {
      "dayEnum": 6,
      "isWorkingDay": false,
      "recurrenceOfMonth": [],
      "workDurationInMinutes": 0,
      "timeSlots": []
    },
    {
      "dayEnum": 7,
      "isWorkingDay": false,
      "recurrenceOfMonth": [],
      "workDurationInMinutes": 0,
      "timeSlots": []
    }
  ]
}
```
---

#### Scenario `SPL-PAT-07`: Duration mismatch in Split PATCH (3200 vs 2400)
- **Endpoint:** `PATCH https://attendance2.dev.zoolwork.com/api/companies/3a249871-7a8d-dec5-2d72-47795dd2662d/worktemplates/split/ab6bb972-24e9-4b3c-9c23-55ef8770f6e5?locationId=3a24d646-b3cf-b1d4-61bb-1adf094b52fc`
- **Execution Result:** HTTP `200` -> **FAIL**
- **MongoDB `_id`:** `ab6bb972-24e9-4b3c-9c23-55ef8770f6e5`

**Request Payload:**
```json
{
  "templateName": {
    "en": "Split Location Shift SPD0001",
    "ar": "\u0648\u0631\u062f\u064a\u0629 \u0645\u062c\u0632\u0623\u0629 SPD0001"
  },
  "shortCode": "SPD0001",
  "templateType": 3,
  "totalWorkDurationInMinutes": 3200,
  "totalWorkingDays": 5,
  "totalDaysOff": 2,
  "timeZoneId": "Asia/Riyadh",
  "splitTimeSlots": [
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
      "workDurationInMinutes": 480,
      "timeSlots": [
        {
          "startTime": "08:00:00",
          "endTime": "12:00:00",
          "workDurationInMinutes": 240
        },
        {
          "startTime": "14:00:00",
          "endTime": "18:00:00",
          "workDurationInMinutes": 240
        }
      ]
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
      "workDurationInMinutes": 480,
      "timeSlots": [
        {
          "startTime": "08:00:00",
          "endTime": "12:00:00",
          "workDurationInMinutes": 240
        },
        {
          "startTime": "14:00:00",
          "endTime": "18:00:00",
          "workDurationInMinutes": 240
        }
      ]
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
      "workDurationInMinutes": 480,
      "timeSlots": [
        {
          "startTime": "08:00:00",
          "endTime": "12:00:00",
          "workDurationInMinutes": 240
        },
        {
          "startTime": "14:00:00",
          "endTime": "18:00:00",
          "workDurationInMinutes": 240
        }
      ]
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
      "workDurationInMinutes": 480,
      "timeSlots": [
        {
          "startTime": "08:00:00",
          "endTime": "12:00:00",
          "workDurationInMinutes": 240
        },
        {
          "startTime": "14:00:00",
          "endTime": "18:00:00",
          "workDurationInMinutes": 240
        }
      ]
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
      "workDurationInMinutes": 480,
      "timeSlots": [
        {
          "startTime": "08:00:00",
          "endTime": "12:00:00",
          "workDurationInMinutes": 240
        },
        {
          "startTime": "14:00:00",
          "endTime": "18:00:00",
          "workDurationInMinutes": 240
        }
      ]
    },
    {
      "dayEnum": 6,
      "isWorkingDay": false,
      "recurrenceOfMonth": [],
      "workDurationInMinutes": 0,
      "timeSlots": []
    },
    {
      "dayEnum": 7,
      "isWorkingDay": false,
      "recurrenceOfMonth": [],
      "workDurationInMinutes": 0,
      "timeSlots": []
    }
  ]
}
```
---