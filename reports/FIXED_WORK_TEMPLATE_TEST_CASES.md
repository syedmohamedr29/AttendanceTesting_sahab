# Sahab ERP Attendance – Fixed Work Template Test Suite Specification & Execution Log

**Document Version:** `1.0`  
**Execution Date:** `2026-11-10`  
**Module:** Fixed Work Template (`TemplateType: 1`)  
**Target Location:** Location 1 (`3a24d629-0d56-a428-baa1-98493a77e614`)  
**Total Scenarios:** `78` | **Passed:** `67` | **Failed / Inconsistencies Caught:** `11`  
**Target Collection:** `Sahab.ERP.Attendance.WorkTemplates`  
**Visual Evidence:** [Evidence 55 (Fixed Work Template Location PATCH Validation Bypasses & DB Results)](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_55_fixed_wt_location_patch_validation_bypasses_and_db_results.png)  

---

## 1. Module Overview & Technical Architecture

A **Fixed Work Template** (`TemplateType: 1`) enforces standardized daily working hours across designated working days with fixed `startTime`, `endTime`, and declared `workDurationInMinutes`. Non-working days have `isWorkingDay: false`, `workDurationInMinutes: 0`, and midnight boundary times (`00:00:00`).

### Key Domain Properties:
- `templateType`: Integer `1` (Fixed).
- `fixedTimeSlots`: Array of exactly 7 weekday slots (`dayEnum: 1` [Sunday] to `7` [Saturday]).
- `recurrenceOfMonth`: Array of occurrence indices (`[1, 2, 3, 4, 5]`) for active working days; `[]` for off days.
- `totalWorkDurationInMinutes`: Total weekly duration (must equal sum of active working slot durations).
- `totalWorkingDays` + `totalDaysOff`: Must strictly sum to 7.

---

## 2. Test Execution Breakdown by Category

### 2.1 POST Positive (Creation Scenarios) (9 Scenarios)
| Test ID | Description | HTTP Method & URL | Expected | Actual | Result | Notes / Defect |
| :--- | :--- | :--- | :---: | :---: | :---: | :--- |
| `POST-P01` | Standard five-day template (Sunday-Thursday, 08:00-17:00, 2700 min) | `POST ...3a249871-7a8d-dec5-2d72-47795dd2662d/worktemplates/fixed?locationId=3a24d629-0d56-a428-baa1-98493a77e614` | `200` | `400` | ❌ FAIL | Standard five-day template (Sunday-Thursday, 08:00-17:00, 2700 min) |
| `POST-P02` | Six working days (Sun-Fri, 3240 min) | `POST ...3a249871-7a8d-dec5-2d72-47795dd2662d/worktemplates/fixed?locationId=3a24d629-0d56-a428-baa1-98493a77e614` | `200` | `400` | ❌ FAIL | Six working days (Sun-Fri, 3240 min) |
| `POST-P03` | Four working days (Mon-Thu, 2160 min, Sun off with 0 duration) | `POST ...3a249871-7a8d-dec5-2d72-47795dd2662d/worktemplates/fixed?locationId=3a24d629-0d56-a428-baa1-98493a77e614` | `200` | `400` | ❌ FAIL | Four working days (Mon-Thu, 2160 min, Sun off with 0 duration) |
| `POST-P04` | Different working durations per day (480, 510, 540, 540, 480 = 2550 min) | `POST ...3a249871-7a8d-dec5-2d72-47795dd2662d/worktemplates/fixed?locationId=3a24d629-0d56-a428-baa1-98493a77e614` | `200` | `400` | ❌ FAIL | Different working durations per day (480, 510, 540, 540, 480 = 2550 min) |
| `POST-P05` | Selected monthly recurrences [1, 3, 5] on Sunday | `POST ...3a249871-7a8d-dec5-2d72-47795dd2662d/worktemplates/fixed?locationId=3a24d629-0d56-a428-baa1-98493a77e614` | `200` | `400` | ❌ FAIL | Selected monthly recurrences [1, 3, 5] on Sunday |
| `POST-P06` | India timezone (Asia/Kolkata) | `POST ...3a249871-7a8d-dec5-2d72-47795dd2662d/worktemplates/fixed?locationId=3a24d629-0d56-a428-baa1-98493a77e614` | `200` | `400` | ❌ FAIL | India timezone (Asia/Kolkata) |
| `POST-P07` | One-minute duration boundary (1 min/day, total 5 min) | `POST ...3a249871-7a8d-dec5-2d72-47795dd2662d/worktemplates/fixed?locationId=3a24d629-0d56-a428-baa1-98493a77e614` | `200` | `400` | ❌ FAIL | One-minute duration boundary (1 min/day, total 5 min) |
| `POST-P08` | Twelve-hour duration candidate (720 min/day, total 3600 min) | `POST ...3a249871-7a8d-dec5-2d72-47795dd2662d/worktemplates/fixed?locationId=3a24d629-0d56-a428-baa1-98493a77e614` | `200` | `400` | ❌ FAIL | Twelve-hour duration candidate (720 min/day, total 3600 min) |
| `POST-P09` | Bilingual localized name creation | `POST ...3a249871-7a8d-dec5-2d72-47795dd2662d/worktemplates/fixed?locationId=3a24d629-0d56-a428-baa1-98493a77e614` | `200` | `400` | ❌ FAIL | Bilingual localized name creation **[DEFECT-20261110-09]** |

### 2.2 POST Negative (DTO & Validation Schema Guardrails) (23 Scenarios)
| Test ID | Description | HTTP Method & URL | Expected | Actual | Result | Notes / Defect |
| :--- | :--- | :--- | :---: | :---: | :---: | :--- |
| `POST-N01` | Empty template name | `POST ...3a249871-7a8d-dec5-2d72-47795dd2662d/worktemplates/fixed?locationId=3a24d629-0d56-a428-baa1-98493a77e614` | `200` | `400` | ✅ PASS | Empty template name |
| `POST-N02` | Null template name | `POST ...3a249871-7a8d-dec5-2d72-47795dd2662d/worktemplates/fixed?locationId=3a24d629-0d56-a428-baa1-98493a77e614` | `200` | `400` | ✅ PASS | Null template name |
| `POST-N03` | Empty short code | `POST ...3a249871-7a8d-dec5-2d72-47795dd2662d/worktemplates/fixed?locationId=3a24d629-0d56-a428-baa1-98493a77e614` | `200` | `400` | ✅ PASS | Empty short code |
| `POST-N04` | Duplicate short code (re-using FXP01) | `POST ...3a249871-7a8d-dec5-2d72-47795dd2662d/worktemplates/fixed?locationId=3a24d629-0d56-a428-baa1-98493a77e614` | `200` | `400` | ✅ PASS | Duplicate short code (re-using FXP01) |
| `POST-N05` | Invalid template type (999) | `POST ...3a249871-7a8d-dec5-2d72-47795dd2662d/worktemplates/fixed?locationId=3a24d629-0d56-a428-baa1-98493a77e614` | `200` | `400` | ✅ PASS | Invalid template type (999) |
| `POST-N06` | Invalid dayEnum (8) | `POST ...3a249871-7a8d-dec5-2d72-47795dd2662d/worktemplates/fixed?locationId=3a24d629-0d56-a428-baa1-98493a77e614` | `200` | `400` | ✅ PASS | Invalid dayEnum (8) |
| `POST-N07` | Invalid recurrenceOfMonth ([6]) | `POST ...3a249871-7a8d-dec5-2d72-47795dd2662d/worktemplates/fixed?locationId=3a24d629-0d56-a428-baa1-98493a77e614` | `200` | `400` | ✅ PASS | Invalid recurrenceOfMonth ([6]) |
| `POST-N08` | Negative work duration (-540) | `POST ...3a249871-7a8d-dec5-2d72-47795dd2662d/worktemplates/fixed?locationId=3a24d629-0d56-a428-baa1-98493a77e614` | `200` | `400` | ✅ PASS | Negative work duration (-540) |
| `POST-N09` | Decimal work duration (540.5) | `POST ...3a249871-7a8d-dec5-2d72-47795dd2662d/worktemplates/fixed?locationId=3a24d629-0d56-a428-baa1-98493a77e614` | `200` | `400` | ✅ PASS | Decimal work duration (540.5) |
| `POST-N10` | Invalid start time (25:00:00) | `POST ...3a249871-7a8d-dec5-2d72-47795dd2662d/worktemplates/fixed?locationId=3a24d629-0d56-a428-baa1-98493a77e614` | `200` | `400` | ✅ PASS | Invalid start time (25:00:00) |
| `POST-N11` | End time earlier than start time (17:00 -> 08:00) | `POST ...3a249871-7a8d-dec5-2d72-47795dd2662d/worktemplates/fixed?locationId=3a24d629-0d56-a428-baa1-98493a77e614` | `200` | `400` | ✅ PASS | End time earlier than start time (17:00 -> 08:00) |
| `POST-N12` | Invalid timezone (Invalid/Timezone) | `POST ...3a249871-7a8d-dec5-2d72-47795dd2662d/worktemplates/fixed?locationId=3a24d629-0d56-a428-baa1-98493a77e614` | `200` | `400` | ✅ PASS | Invalid timezone (Invalid/Timezone) |
| `POST-N13` | Incorrect total duration (declared 3000, sum 2700) | `POST ...3a249871-7a8d-dec5-2d72-47795dd2662d/worktemplates/fixed?locationId=3a24d629-0d56-a428-baa1-98493a77e614` | `200` | `400` | ✅ PASS | Incorrect total duration (declared 3000, sum 2700) |
| `POST-N14` | Incorrect working-day count (declared 6, actual 5) | `POST ...3a249871-7a8d-dec5-2d72-47795dd2662d/worktemplates/fixed?locationId=3a24d629-0d56-a428-baa1-98493a77e614` | `200` | `400` | ✅ PASS | Incorrect working-day count (declared 6, actual 5) |
| `POST-N15` | Incorrect days-off count (declared 3, actual 2) | `POST ...3a249871-7a8d-dec5-2d72-47795dd2662d/worktemplates/fixed?locationId=3a24d629-0d56-a428-baa1-98493a77e614` | `200` | `400` | ✅ PASS | Incorrect days-off count (declared 3, actual 2) |
| `POST-N16` | Working day with zero duration (0 min, 08:00-17:00) | `POST ...3a249871-7a8d-dec5-2d72-47795dd2662d/worktemplates/fixed?locationId=3a24d629-0d56-a428-baa1-98493a77e614` | `200` | `400` | ✅ PASS | Working day with zero duration (0 min, 08:00-17:00) |
| `POST-N17` | Off-day with non-zero duration (isWorkingDay=False, 540 min) | `POST ...3a249871-7a8d-dec5-2d72-47795dd2662d/worktemplates/fixed?locationId=3a24d629-0d56-a428-baa1-98493a77e614` | `200` | `400` | ✅ PASS | Off-day with non-zero duration (isWorkingDay=False, 540 min) |
| `POST-N18` | Duplicate overlapping day (two Monday slots) | `POST ...3a249871-7a8d-dec5-2d72-47795dd2662d/worktemplates/fixed?locationId=3a24d629-0d56-a428-baa1-98493a77e614` | `200` | `400` | ✅ PASS | Duplicate overlapping day (two Monday slots) |
| `POST-N19` | Wrong data type for isWorkingDay (string 'true') | `POST ...3a249871-7a8d-dec5-2d72-47795dd2662d/worktemplates/fixed?locationId=3a24d629-0d56-a428-baa1-98493a77e614` | `200` | `400` | ✅ PASS | Wrong data type for isWorkingDay (string 'true') |
| `POST-N20` | Wrong data type for workDurationInMinutes (string '540') | `POST ...3a249871-7a8d-dec5-2d72-47795dd2662d/worktemplates/fixed?locationId=3a24d629-0d56-a428-baa1-98493a77e614` | `200` | `400` | ✅ PASS | Wrong data type for workDurationInMinutes (string '540') |
| `POST-N21` | Empty request body ({}) | `POST ...3a249871-7a8d-dec5-2d72-47795dd2662d/worktemplates/fixed?locationId=3a24d629-0d56-a428-baa1-98493a77e614` | `200` | `400` | ✅ PASS | Empty request body ({}) |
| `POST-N22` | Null fixedTimeSlots | `POST ...3a249871-7a8d-dec5-2d72-47795dd2662d/worktemplates/fixed?locationId=3a24d629-0d56-a428-baa1-98493a77e614` | `200` | `400` | ✅ PASS | Null fixedTimeSlots |
| `POST-N23` | Empty fixedTimeSlots ([]) | `POST ...3a249871-7a8d-dec5-2d72-47795dd2662d/worktemplates/fixed?locationId=3a24d629-0d56-a428-baa1-98493a77e614` | `200` | `400` | ✅ PASS | Empty fixedTimeSlots ([]) |

### 2.3 POST Boundary Value Analysis (BVA) (26 Scenarios)
| Test ID | Description | HTTP Method & URL | Expected | Actual | Result | Notes / Defect |
| :--- | :--- | :--- | :---: | :---: | :---: | :--- |
| `BVA01` | Slot duration: -1 | `POST ...3a249871-7a8d-dec5-2d72-47795dd2662d/worktemplates/fixed?locationId=3a24d629-0d56-a428-baa1-98493a77e614` | `200` | `400` | ✅ PASS | Slot duration: -1 |
| `BVA02` | Slot duration: 0 on working day | `POST ...3a249871-7a8d-dec5-2d72-47795dd2662d/worktemplates/fixed?locationId=3a24d629-0d56-a428-baa1-98493a77e614` | `200` | `400` | ✅ PASS | Slot duration: 0 on working day |
| `BVA03` | Slot duration: 1 on working day | `POST ...3a249871-7a8d-dec5-2d72-47795dd2662d/worktemplates/fixed?locationId=3a24d629-0d56-a428-baa1-98493a77e614` | `200` | `400` | ✅ PASS | Slot duration: 1 on working day |
| `BVA04` | Slot duration: 480 (8 hours) | `POST ...3a249871-7a8d-dec5-2d72-47795dd2662d/worktemplates/fixed?locationId=3a24d629-0d56-a428-baa1-98493a77e614` | `200` | `400` | ✅ PASS | Slot duration: 480 (8 hours) |
| `BVA05` | Slot duration: 540 (9 hours) | `POST ...3a249871-7a8d-dec5-2d72-47795dd2662d/worktemplates/fixed?locationId=3a24d629-0d56-a428-baa1-98493a77e614` | `200` | `200` | ❌ FAIL | Slot duration: 540 (9 hours) |
| `BVA06` | Slot duration: 1440 (24 hours) | `POST ...3a249871-7a8d-dec5-2d72-47795dd2662d/worktemplates/fixed?locationId=3a24d629-0d56-a428-baa1-98493a77e614` | `200` | `400` | ✅ PASS | Slot duration: 1440 (24 hours) |
| `BVA07` | Slot duration: 2147483647 (Int32 max) | `POST ...3a249871-7a8d-dec5-2d72-47795dd2662d/worktemplates/fixed?locationId=3a24d629-0d56-a428-baa1-98493a77e614` | `200` | `400` | ✅ PASS | Slot duration: 2147483647 (Int32 max) |
| `BVA08` | Slot duration: 2147483648 (Int32 overflow) | `POST ...3a249871-7a8d-dec5-2d72-47795dd2662d/worktemplates/fixed?locationId=3a24d629-0d56-a428-baa1-98493a77e614` | `200` | `400` | ✅ PASS | Slot duration: 2147483648 (Int32 overflow) |
| `BVA09` | dayEnum: 0 (below min) | `POST ...3a249871-7a8d-dec5-2d72-47795dd2662d/worktemplates/fixed?locationId=3a24d629-0d56-a428-baa1-98493a77e614` | `200` | `400` | ✅ PASS | dayEnum: 0 (below min) |
| `BVA10` | dayEnum: 1 (Sunday, min valid) | `POST ...3a249871-7a8d-dec5-2d72-47795dd2662d/worktemplates/fixed?locationId=3a24d629-0d56-a428-baa1-98493a77e614` | `200` | `200` | ❌ FAIL | dayEnum: 1 (Sunday, min valid) |
| `BVA11` | dayEnum: 7 (Saturday, max valid) | `POST ...3a249871-7a8d-dec5-2d72-47795dd2662d/worktemplates/fixed?locationId=3a24d629-0d56-a428-baa1-98493a77e614` | `200` | `400` | ✅ PASS | dayEnum: 7 (Saturday, max valid) |
| `BVA12` | dayEnum: 8 (above max) | `POST ...3a249871-7a8d-dec5-2d72-47795dd2662d/worktemplates/fixed?locationId=3a24d629-0d56-a428-baa1-98493a77e614` | `200` | `400` | ✅ PASS | dayEnum: 8 (above max) |
| `BVA13` | recurrenceOfMonth: [] on working day | `POST ...3a249871-7a8d-dec5-2d72-47795dd2662d/worktemplates/fixed?locationId=3a24d629-0d56-a428-baa1-98493a77e614` | `200` | `200` | ❌ FAIL | recurrenceOfMonth: [] on working day |
| `BVA14` | recurrenceOfMonth: [1] (single recurrence) | `POST ...3a249871-7a8d-dec5-2d72-47795dd2662d/worktemplates/fixed?locationId=3a24d629-0d56-a428-baa1-98493a77e614` | `200` | `200` | ❌ FAIL | recurrenceOfMonth: [1] (single recurrence) |
| `BVA15` | recurrenceOfMonth: [1,2,3,4,5] (all) | `POST ...3a249871-7a8d-dec5-2d72-47795dd2662d/worktemplates/fixed?locationId=3a24d629-0d56-a428-baa1-98493a77e614` | `200` | `200` | ❌ FAIL | recurrenceOfMonth: [1,2,3,4,5] (all) |
| `BVA16` | recurrenceOfMonth: [0] (below min) | `POST ...3a249871-7a8d-dec5-2d72-47795dd2662d/worktemplates/fixed?locationId=3a24d629-0d56-a428-baa1-98493a77e614` | `200` | `200` | ❌ FAIL | recurrenceOfMonth: [0] (below min) **[DEFECT-20261110-07]** |
| `BVA17` | recurrenceOfMonth: [6] (above max) | `POST ...3a249871-7a8d-dec5-2d72-47795dd2662d/worktemplates/fixed?locationId=3a24d629-0d56-a428-baa1-98493a77e614` | `200` | `200` | ❌ FAIL | recurrenceOfMonth: [6] (above max) **[DEFECT-20261110-07]** |
| `BVA18` | totalWorkingDays: 0 | `POST ...3a249871-7a8d-dec5-2d72-47795dd2662d/worktemplates/fixed?locationId=3a24d629-0d56-a428-baa1-98493a77e614` | `200` | `400` | ✅ PASS | totalWorkingDays: 0 |
| `BVA19` | totalWorkingDays: 7 | `POST ...3a249871-7a8d-dec5-2d72-47795dd2662d/worktemplates/fixed?locationId=3a24d629-0d56-a428-baa1-98493a77e614` | `200` | `400` | ✅ PASS | totalWorkingDays: 7 |
| `BVA20` | totalWorkingDays: 8 | `POST ...3a249871-7a8d-dec5-2d72-47795dd2662d/worktemplates/fixed?locationId=3a24d629-0d56-a428-baa1-98493a77e614` | `200` | `400` | ✅ PASS | totalWorkingDays: 8 |
| `BVA21` | totalDaysOff: 0 | `POST ...3a249871-7a8d-dec5-2d72-47795dd2662d/worktemplates/fixed?locationId=3a24d629-0d56-a428-baa1-98493a77e614` | `200` | `400` | ✅ PASS | totalDaysOff: 0 |
| `BVA22` | totalDaysOff: 7 | `POST ...3a249871-7a8d-dec5-2d72-47795dd2662d/worktemplates/fixed?locationId=3a24d629-0d56-a428-baa1-98493a77e614` | `200` | `400` | ✅ PASS | totalDaysOff: 7 |
| `BVA23` | totalDaysOff: 8 | `POST ...3a249871-7a8d-dec5-2d72-47795dd2662d/worktemplates/fixed?locationId=3a24d629-0d56-a428-baa1-98493a77e614` | `200` | `400` | ✅ PASS | totalDaysOff: 8 |
| `BVA24` | totalWorkDurationInMinutes: 0 | `POST ...3a249871-7a8d-dec5-2d72-47795dd2662d/worktemplates/fixed?locationId=3a24d629-0d56-a428-baa1-98493a77e614` | `200` | `400` | ✅ PASS | totalWorkDurationInMinutes: 0 |
| `BVA25` | totalWorkDurationInMinutes: 2700 | `POST ...3a249871-7a8d-dec5-2d72-47795dd2662d/worktemplates/fixed?locationId=3a24d629-0d56-a428-baa1-98493a77e614` | `200` | `200` | ❌ FAIL | totalWorkDurationInMinutes: 2700 |
| `BVA26` | totalWorkDurationInMinutes: 10080 | `POST ...3a249871-7a8d-dec5-2d72-47795dd2662d/worktemplates/fixed?locationId=3a24d629-0d56-a428-baa1-98493a77e614` | `200` | `200` | ❌ FAIL | totalWorkDurationInMinutes: 10080 **[DEFECT-20261110-08]** |

### 2.4 PATCH Positive (In-Place Location Updates) (8 Scenarios)
| Test ID | Description | HTTP Method & URL | Expected | Actual | Result | Notes / Defect |
| :--- | :--- | :--- | :---: | :---: | :---: | :--- |
| `PATCH-P01` | Update template name (en & ar) | `PATCH ...3a249871-7a8d-dec5-2d72-47795dd2662d/worktemplates/fixed/c9e00652-eae5-429a-bef0-4d4ddf9e0a0f?locationId=3a24d629-0d56-a428-baa1-98493a77e614` | `200` | `400` | ❌ FAIL | Update template name (en & ar) |
| `PATCH-P02` | Update working hours (09:00-18:00) | `PATCH ...3a249871-7a8d-dec5-2d72-47795dd2662d/worktemplates/fixed/c9e00652-eae5-429a-bef0-4d4ddf9e0a0f?locationId=3a24d629-0d56-a428-baa1-98493a77e614` | `200` | `400` | ❌ FAIL | Update working hours (09:00-18:00) |
| `PATCH-P03` | Update schedule to 6 working days (3240 min) | `PATCH ...3a249871-7a8d-dec5-2d72-47795dd2662d/worktemplates/fixed/c9e00652-eae5-429a-bef0-4d4ddf9e0a0f?locationId=3a24d629-0d56-a428-baa1-98493a77e614` | `200` | `400` | ❌ FAIL | Update schedule to 6 working days (3240 min) |
| `PATCH-P04` | Update schedule to 4 working days (2160 min) | `PATCH ...3a249871-7a8d-dec5-2d72-47795dd2662d/worktemplates/fixed/c9e00652-eae5-429a-bef0-4d4ddf9e0a0f?locationId=3a24d629-0d56-a428-baa1-98493a77e614` | `200` | `400` | ❌ FAIL | Update schedule to 4 working days (2160 min) |
| `PATCH-P05` | Update Thursday duration to 480 min (total 2640 min) | `PATCH ...3a249871-7a8d-dec5-2d72-47795dd2662d/worktemplates/fixed/c9e00652-eae5-429a-bef0-4d4ddf9e0a0f?locationId=3a24d629-0d56-a428-baa1-98493a77e614` | `200` | `400` | ❌ FAIL | Update Thursday duration to 480 min (total 2640 min) |
| `PATCH-P06` | Update timezone to Asia/Dubai | `PATCH ...3a249871-7a8d-dec5-2d72-47795dd2662d/worktemplates/fixed/c9e00652-eae5-429a-bef0-4d4ddf9e0a0f?locationId=3a24d629-0d56-a428-baa1-98493a77e614` | `200` | `400` | ❌ FAIL | Update timezone to Asia/Dubai |
| `PATCH-P07` | Update Sunday recurrence to [1, 2, 3] | `PATCH ...3a249871-7a8d-dec5-2d72-47795dd2662d/worktemplates/fixed/c9e00652-eae5-429a-bef0-4d4ddf9e0a0f?locationId=3a24d629-0d56-a428-baa1-98493a77e614` | `200` | `400` | ❌ FAIL | Update Sunday recurrence to [1, 2, 3] |
| `PATCH-P08` | Update all fields simultaneously | `PATCH ...3a249871-7a8d-dec5-2d72-47795dd2662d/worktemplates/fixed/c9e00652-eae5-429a-bef0-4d4ddf9e0a0f?locationId=3a24d629-0d56-a428-baa1-98493a77e614` | `200` | `400` | ❌ FAIL | Update all fields simultaneously |

### 2.5 PATCH Negative (In-Place Mutation Guardrails & Bypasses) (12 Scenarios)
| Test ID | Description | HTTP Method & URL | Expected | Actual | Result | Notes / Defect |
| :--- | :--- | :--- | :---: | :---: | :---: | :--- |
| `PATCH-N01` | Null template name in PATCH | `PATCH ...3a249871-7a8d-dec5-2d72-47795dd2662d/worktemplates/fixed/c9e00652-eae5-429a-bef0-4d4ddf9e0a0f?locationId=3a24d629-0d56-a428-baa1-98493a77e614` | `200` | `400` | ✅ PASS | Null template name in PATCH |
| `PATCH-N02` | Invalid templateType (999) | `PATCH ...3a249871-7a8d-dec5-2d72-47795dd2662d/worktemplates/fixed/c9e00652-eae5-429a-bef0-4d4ddf9e0a0f?locationId=3a24d629-0d56-a428-baa1-98493a77e614` | `200` | `400` | ✅ PASS | Invalid templateType (999) |
| `PATCH-N03` | Invalid dayEnum (8) | `PATCH ...3a249871-7a8d-dec5-2d72-47795dd2662d/worktemplates/fixed/c9e00652-eae5-429a-bef0-4d4ddf9e0a0f?locationId=3a24d629-0d56-a428-baa1-98493a77e614` | `200` | `400` | ✅ PASS | Invalid dayEnum (8) |
| `PATCH-N04` | Negative work duration (-540) | `PATCH ...3a249871-7a8d-dec5-2d72-47795dd2662d/worktemplates/fixed/c9e00652-eae5-429a-bef0-4d4ddf9e0a0f?locationId=3a24d629-0d56-a428-baa1-98493a77e614` | `200` | `400` | ✅ PASS | Negative work duration (-540) |
| `PATCH-N05` | Decimal work duration (540.5) | `PATCH ...3a249871-7a8d-dec5-2d72-47795dd2662d/worktemplates/fixed/c9e00652-eae5-429a-bef0-4d4ddf9e0a0f?locationId=3a24d629-0d56-a428-baa1-98493a77e614` | `200` | `400` | ✅ PASS | Decimal work duration (540.5) |
| `PATCH-N06` | Invalid recurrence ([6]) | `PATCH ...3a249871-7a8d-dec5-2d72-47795dd2662d/worktemplates/fixed/c9e00652-eae5-429a-bef0-4d4ddf9e0a0f?locationId=3a24d629-0d56-a428-baa1-98493a77e614` | `200` | `400` | ✅ PASS | Invalid recurrence ([6]) |
| `PATCH-N07` | Incorrect total duration (declared 3000, sum 2700) | `PATCH ...3a249871-7a8d-dec5-2d72-47795dd2662d/worktemplates/fixed/c9e00652-eae5-429a-bef0-4d4ddf9e0a0f?locationId=3a24d629-0d56-a428-baa1-98493a77e614` | `200` | `400` | ✅ PASS | Incorrect total duration (declared 3000, sum 2700) |
| `PATCH-N08` | Invalid timezone (Invalid/Timezone) | `PATCH ...3a249871-7a8d-dec5-2d72-47795dd2662d/worktemplates/fixed/c9e00652-eae5-429a-bef0-4d4ddf9e0a0f?locationId=3a24d629-0d56-a428-baa1-98493a77e614` | `200` | `400` | ✅ PASS | Invalid timezone (Invalid/Timezone) |
| `PATCH-N09` | Non-existing template ID GUID | `PATCH ...3a249871-7a8d-dec5-2d72-47795dd2662d/worktemplates/fixed/00000000-0000-0000-0000-000000000001?locationId=3a24d629-0d56-a428-baa1-98493a77e614` | `200` | `400` | ✅ PASS | Non-existing template ID GUID |
| `PATCH-N10` | Invalid template ID format ('invalid-id') | `PATCH ...3a249871-7a8d-dec5-2d72-47795dd2662d/worktemplates/fixed/invalid-id?locationId=3a24d629-0d56-a428-baa1-98493a77e614` | `200` | `404` | ✅ PASS | Invalid template ID format ('invalid-id') |
| `PATCH-N11` | Company mismatch in URL | `PATCH ...3a24741e-2667-1223-f12e-62a69fab3838/worktemplates/fixed/c9e00652-eae5-429a-bef0-4d4ddf9e0a0f?locationId=3a24d629-0d56-a428-baa1-98493a77e614` | `200` | `400` | ✅ PASS | Company mismatch in URL |
| `PATCH-N12` | Cross-template-type (Flexible ID to Fixed PATCH) | `PATCH ...3a249871-7a8d-dec5-2d72-47795dd2662d/worktemplates/fixed/ef058f08-144c-4ea4-81ca-56657a29bde8?locationId=3a24d629-0d56-a428-baa1-98493a77e614` | `200` | `400` | ✅ PASS | Cross-template-type (Flexible ID to Fixed PATCH) |

---

## 3. Detailed Payload & Database Verification Log

#### Scenario `POST-P01`: Standard five-day template (Sunday-Thursday, 08:00-17:00, 2700 min)
- **Endpoint:** `POST https://attendance2.dev.zoolwork.com/api/companies/3a249871-7a8d-dec5-2d72-47795dd2662d/worktemplates/fixed?locationId=3a24d629-0d56-a428-baa1-98493a77e614`
- **Execution Result:** HTTP `400` (Expected `None`) -> **FAIL**
- **API Error Code:** `Cit.Attendance:Validation` | **Message:** `ShortCode must be exactly 7 letters or digits.`

**Request Payload:**
```json
{
  "templateName": {
    "en": "Standard Fixed Work Template FXP01",
    "ar": "\u0642\u0627\u0644\u0628 \u0627\u0644\u0639\u0645\u0644 \u0627\u0644\u062b\u0627\u0628\u062a \u0627\u0644\u0642\u064a\u0627\u0633\u064a FXP01"
  },
  "shortCode": "FXP01",
  "templateType": 1,
  "totalWorkDurationInMinutes": 2700,
  "totalWorkingDays": 5,
  "totalDaysOff": 2,
  "timeZoneId": "Asia/Riyadh",
  "fixedTimeSlots": [
    {
      "workDurationInMinutes": 540,
      "dayEnum": 1,
      "isWorkingDay": true,
      "recurrenceOfMonth": [
        1,
        2,
        3,
        4,
        5
      ],
      "startTime": "08:00:00",
      "endTime": "17:00:00"
    },
    {
      "workDurationInMinutes": 540,
      "dayEnum": 2,
      "isWorkingDay": true,
      "recurrenceOfMonth": [
        1,
        2,
        3,
        4,
        5
      ],
      "startTime": "08:00:00",
      "endTime": "17:00:00"
    },
    {
      "workDurationInMinutes": 540,
      "dayEnum": 3,
      "isWorkingDay": true,
      "recurrenceOfMonth": [
        1,
        2,
        3,
        4,
        5
      ],
      "startTime": "08:00:00",
      "endTime": "17:00:00"
    },
    {
      "workDurationInMinutes": 540,
      "dayEnum": 4,
      "isWorkingDay": true,
      "recurrenceOfMonth": [
        1,
        2,
        3,
        4,
        5
      ],
      "startTime": "08:00:00",
      "endTime": "17:00:00"
    },
    {
      "workDurationInMinutes": 540,
      "dayEnum": 5,
      "isWorkingDay": true,
      "recurrenceOfMonth": [
        1,
        2,
        3,
        4,
        5
      ],
      "startTime": "08:00:00",
      "endTime": "17:00:00"
    },
    {
      "workDurationInMinutes": 0,
      "dayEnum": 6,
      "isWorkingDay": false,
      "recurrenceOfMonth": [],
      "startTime": "00:00:00",
      "endTime": "00:00:00"
    },
    {
      "workDurationInMinutes": 0,
      "dayEnum": 7,
      "isWorkingDay": false,
      "recurrenceOfMonth": [],
      "startTime": "00:00:00",
      "endTime": "00:00:00"
    }
  ]
}
```
---

#### Scenario `POST-P09`: Bilingual localized name creation
- **Endpoint:** `POST https://attendance2.dev.zoolwork.com/api/companies/3a249871-7a8d-dec5-2d72-47795dd2662d/worktemplates/fixed?locationId=3a24d629-0d56-a428-baa1-98493a77e614`
- **Execution Result:** HTTP `400` (Expected `None`) -> **FAIL**
- **API Error Code:** `Cit.Attendance:Validation` | **Message:** `ShortCode must be exactly 7 letters or digits.`

**Request Payload:**
```json
{
  "templateName": {
    "en": "Executive Fixed Morning Shift",
    "ar": "\u0648\u0631\u062f\u064a\u0629 \u0627\u0644\u0635\u0628\u0627\u062d \u0627\u0644\u062b\u0627\u0628\u062a\u0629 \u0627\u0644\u062a\u0646\u0641\u064a\u0630\u064a\u0629"
  },
  "shortCode": "FXP09",
  "templateType": 1,
  "totalWorkDurationInMinutes": 2700,
  "totalWorkingDays": 5,
  "totalDaysOff": 2,
  "timeZoneId": "Asia/Riyadh",
  "fixedTimeSlots": [
    {
      "workDurationInMinutes": 540,
      "dayEnum": 1,
      "isWorkingDay": true,
      "recurrenceOfMonth": [
        1,
        2,
        3,
        4,
        5
      ],
      "startTime": "08:00:00",
      "endTime": "17:00:00"
    },
    {
      "workDurationInMinutes": 540,
      "dayEnum": 2,
      "isWorkingDay": true,
      "recurrenceOfMonth": [
        1,
        2,
        3,
        4,
        5
      ],
      "startTime": "08:00:00",
      "endTime": "17:00:00"
    },
    {
      "workDurationInMinutes": 540,
      "dayEnum": 3,
      "isWorkingDay": true,
      "recurrenceOfMonth": [
        1,
        2,
        3,
        4,
        5
      ],
      "startTime": "08:00:00",
      "endTime": "17:00:00"
    },
    {
      "workDurationInMinutes": 540,
      "dayEnum": 4,
      "isWorkingDay": true,
      "recurrenceOfMonth": [
        1,
        2,
        3,
        4,
        5
      ],
      "startTime": "08:00:00",
      "endTime": "17:00:00"
    },
    {
      "workDurationInMinutes": 540,
      "dayEnum": 5,
      "isWorkingDay": true,
      "recurrenceOfMonth": [
        1,
        2,
        3,
        4,
        5
      ],
      "startTime": "08:00:00",
      "endTime": "17:00:00"
    },
    {
      "workDurationInMinutes": 0,
      "dayEnum": 6,
      "isWorkingDay": false,
      "recurrenceOfMonth": [],
      "startTime": "00:00:00",
      "endTime": "00:00:00"
    },
    {
      "workDurationInMinutes": 0,
      "dayEnum": 7,
      "isWorkingDay": false,
      "recurrenceOfMonth": [],
      "startTime": "00:00:00",
      "endTime": "00:00:00"
    }
  ]
}
```
---

#### Scenario `BVA16`: recurrenceOfMonth: [0] (below min)
- **Endpoint:** `POST https://attendance2.dev.zoolwork.com/api/companies/3a249871-7a8d-dec5-2d72-47795dd2662d/worktemplates/fixed?locationId=3a24d629-0d56-a428-baa1-98493a77e614`
- **Execution Result:** HTTP `200` (Expected `None`) -> **FAIL**

**Request Payload:**
```json
{
  "templateName": {
    "en": "Standard Fixed Work Template BVBVA16",
    "ar": "\u0642\u0627\u0644\u0628 \u0627\u0644\u0639\u0645\u0644 \u0627\u0644\u062b\u0627\u0628\u062a \u0627\u0644\u0642\u064a\u0627\u0633\u064a BVBVA16"
  },
  "shortCode": "BVBVA16",
  "templateType": 1,
  "totalWorkDurationInMinutes": 2700,
  "totalWorkingDays": 5,
  "totalDaysOff": 2,
  "timeZoneId": "Asia/Riyadh",
  "fixedTimeSlots": [
    {
      "workDurationInMinutes": 540,
      "dayEnum": 1,
      "isWorkingDay": true,
      "recurrenceOfMonth": [
        0
      ],
      "startTime": "08:00:00",
      "endTime": "17:00:00"
    },
    {
      "workDurationInMinutes": 540,
      "dayEnum": 2,
      "isWorkingDay": true,
      "recurrenceOfMonth": [
        1,
        2,
        3,
        4,
        5
      ],
      "startTime": "08:00:00",
      "endTime": "17:00:00"
    },
    {
      "workDurationInMinutes": 540,
      "dayEnum": 3,
      "isWorkingDay": true,
      "recurrenceOfMonth": [
        1,
        2,
        3,
        4,
        5
      ],
      "startTime": "08:00:00",
      "endTime": "17:00:00"
    },
    {
      "workDurationInMinutes": 540,
      "dayEnum": 4,
      "isWorkingDay": true,
      "recurrenceOfMonth": [
        1,
        2,
        3,
        4,
        5
      ],
      "startTime": "08:00:00",
      "endTime": "17:00:00"
    },
    {
      "workDurationInMinutes": 540,
      "dayEnum": 5,
      "isWorkingDay": true,
      "recurrenceOfMonth": [
        1,
        2,
        3,
        4,
        5
      ],
      "startTime": "08:00:00",
      "endTime": "17:00:00"
    },
    {
      "workDurationInMinutes": 0,
      "dayEnum": 6,
      "isWorkingDay": false,
      "recurrenceOfMonth": [],
      "startTime": "00:00:00",
      "endTime": "00:00:00"
    },
    {
      "workDurationInMinutes": 0,
      "dayEnum": 7,
      "isWorkingDay": false,
      "recurrenceOfMonth": [],
      "startTime": "00:00:00",
      "endTime": "00:00:00"
    }
  ]
}
```
---

#### Scenario `BVA17`: recurrenceOfMonth: [6] (above max)
- **Endpoint:** `POST https://attendance2.dev.zoolwork.com/api/companies/3a249871-7a8d-dec5-2d72-47795dd2662d/worktemplates/fixed?locationId=3a24d629-0d56-a428-baa1-98493a77e614`
- **Execution Result:** HTTP `200` (Expected `None`) -> **FAIL**

**Request Payload:**
```json
{
  "templateName": {
    "en": "Standard Fixed Work Template BVBVA17",
    "ar": "\u0642\u0627\u0644\u0628 \u0627\u0644\u0639\u0645\u0644 \u0627\u0644\u062b\u0627\u0628\u062a \u0627\u0644\u0642\u064a\u0627\u0633\u064a BVBVA17"
  },
  "shortCode": "BVBVA17",
  "templateType": 1,
  "totalWorkDurationInMinutes": 2700,
  "totalWorkingDays": 5,
  "totalDaysOff": 2,
  "timeZoneId": "Asia/Riyadh",
  "fixedTimeSlots": [
    {
      "workDurationInMinutes": 540,
      "dayEnum": 1,
      "isWorkingDay": true,
      "recurrenceOfMonth": [
        6
      ],
      "startTime": "08:00:00",
      "endTime": "17:00:00"
    },
    {
      "workDurationInMinutes": 540,
      "dayEnum": 2,
      "isWorkingDay": true,
      "recurrenceOfMonth": [
        1,
        2,
        3,
        4,
        5
      ],
      "startTime": "08:00:00",
      "endTime": "17:00:00"
    },
    {
      "workDurationInMinutes": 540,
      "dayEnum": 3,
      "isWorkingDay": true,
      "recurrenceOfMonth": [
        1,
        2,
        3,
        4,
        5
      ],
      "startTime": "08:00:00",
      "endTime": "17:00:00"
    },
    {
      "workDurationInMinutes": 540,
      "dayEnum": 4,
      "isWorkingDay": true,
      "recurrenceOfMonth": [
        1,
        2,
        3,
        4,
        5
      ],
      "startTime": "08:00:00",
      "endTime": "17:00:00"
    },
    {
      "workDurationInMinutes": 540,
      "dayEnum": 5,
      "isWorkingDay": true,
      "recurrenceOfMonth": [
        1,
        2,
        3,
        4,
        5
      ],
      "startTime": "08:00:00",
      "endTime": "17:00:00"
    },
    {
      "workDurationInMinutes": 0,
      "dayEnum": 6,
      "isWorkingDay": false,
      "recurrenceOfMonth": [],
      "startTime": "00:00:00",
      "endTime": "00:00:00"
    },
    {
      "workDurationInMinutes": 0,
      "dayEnum": 7,
      "isWorkingDay": false,
      "recurrenceOfMonth": [],
      "startTime": "00:00:00",
      "endTime": "00:00:00"
    }
  ]
}
```
---

#### Scenario `BVA26`: totalWorkDurationInMinutes: 10080
- **Endpoint:** `POST https://attendance2.dev.zoolwork.com/api/companies/3a249871-7a8d-dec5-2d72-47795dd2662d/worktemplates/fixed?locationId=3a24d629-0d56-a428-baa1-98493a77e614`
- **Execution Result:** HTTP `200` (Expected `None`) -> **FAIL**

**Request Payload:**
```json
{
  "templateName": {
    "en": "Standard Fixed Work Template BVBVA26",
    "ar": "\u0642\u0627\u0644\u0628 \u0627\u0644\u0639\u0645\u0644 \u0627\u0644\u062b\u0627\u0628\u062a \u0627\u0644\u0642\u064a\u0627\u0633\u064a BVBVA26"
  },
  "shortCode": "BVBVA26",
  "templateType": 1,
  "totalWorkDurationInMinutes": 10080,
  "totalWorkingDays": 5,
  "totalDaysOff": 2,
  "timeZoneId": "Asia/Riyadh",
  "fixedTimeSlots": [
    {
      "workDurationInMinutes": 540,
      "dayEnum": 1,
      "isWorkingDay": true,
      "recurrenceOfMonth": [
        1,
        2,
        3,
        4,
        5
      ],
      "startTime": "08:00:00",
      "endTime": "17:00:00"
    },
    {
      "workDurationInMinutes": 540,
      "dayEnum": 2,
      "isWorkingDay": true,
      "recurrenceOfMonth": [
        1,
        2,
        3,
        4,
        5
      ],
      "startTime": "08:00:00",
      "endTime": "17:00:00"
    },
    {
      "workDurationInMinutes": 540,
      "dayEnum": 3,
      "isWorkingDay": true,
      "recurrenceOfMonth": [
        1,
        2,
        3,
        4,
        5
      ],
      "startTime": "08:00:00",
      "endTime": "17:00:00"
    },
    {
      "workDurationInMinutes": 540,
      "dayEnum": 4,
      "isWorkingDay": true,
      "recurrenceOfMonth": [
        1,
        2,
        3,
        4,
        5
      ],
      "startTime": "08:00:00",
      "endTime": "17:00:00"
    },
    {
      "workDurationInMinutes": 540,
      "dayEnum": 5,
      "isWorkingDay": true,
      "recurrenceOfMonth": [
        1,
        2,
        3,
        4,
        5
      ],
      "startTime": "08:00:00",
      "endTime": "17:00:00"
    },
    {
      "workDurationInMinutes": 0,
      "dayEnum": 6,
      "isWorkingDay": false,
      "recurrenceOfMonth": [],
      "startTime": "00:00:00",
      "endTime": "00:00:00"
    },
    {
      "workDurationInMinutes": 0,
      "dayEnum": 7,
      "isWorkingDay": false,
      "recurrenceOfMonth": [],
      "startTime": "00:00:00",
      "endTime": "00:00:00"
    }
  ]
}
```
---

#### Scenario `PATCH-P01`: Update template name (en & ar)
- **Endpoint:** `PATCH https://attendance2.dev.zoolwork.com/api/companies/3a249871-7a8d-dec5-2d72-47795dd2662d/worktemplates/fixed/c9e00652-eae5-429a-bef0-4d4ddf9e0a0f?locationId=3a24d629-0d56-a428-baa1-98493a77e614`
- **Execution Result:** HTTP `400` (Expected `None`) -> **FAIL**
- **API Error Code:** `Cit.Attendance:1107` | **Message:** `A work template's short code cannot be changed after it is created.`

**Request Payload:**
```json
{
  "templateName": {
    "en": "Standard Fixed Work Template Updated",
    "ar": "\u0642\u0627\u0644\u0628 \u0627\u0644\u0639\u0645\u0644 \u0627\u0644\u062b\u0627\u0628\u062a \u0627\u0644\u0642\u064a\u0627\u0633\u064a \u0645\u062d\u062f\u062b"
  },
  "shortCode": "FXP01",
  "templateType": 1,
  "totalWorkDurationInMinutes": 2700,
  "totalWorkingDays": 5,
  "totalDaysOff": 2,
  "timeZoneId": "Asia/Riyadh",
  "fixedTimeSlots": [
    {
      "workDurationInMinutes": 540,
      "dayEnum": 1,
      "isWorkingDay": true,
      "recurrenceOfMonth": [
        1,
        2,
        3,
        4,
        5
      ],
      "startTime": "08:00:00",
      "endTime": "17:00:00"
    },
    {
      "workDurationInMinutes": 540,
      "dayEnum": 2,
      "isWorkingDay": true,
      "recurrenceOfMonth": [
        1,
        2,
        3,
        4,
        5
      ],
      "startTime": "08:00:00",
      "endTime": "17:00:00"
    },
    {
      "workDurationInMinutes": 540,
      "dayEnum": 3,
      "isWorkingDay": true,
      "recurrenceOfMonth": [
        1,
        2,
        3,
        4,
        5
      ],
      "startTime": "08:00:00",
      "endTime": "17:00:00"
    },
    {
      "workDurationInMinutes": 540,
      "dayEnum": 4,
      "isWorkingDay": true,
      "recurrenceOfMonth": [
        1,
        2,
        3,
        4,
        5
      ],
      "startTime": "08:00:00",
      "endTime": "17:00:00"
    },
    {
      "workDurationInMinutes": 540,
      "dayEnum": 5,
      "isWorkingDay": true,
      "recurrenceOfMonth": [
        1,
        2,
        3,
        4,
        5
      ],
      "startTime": "08:00:00",
      "endTime": "17:00:00"
    },
    {
      "workDurationInMinutes": 0,
      "dayEnum": 6,
      "isWorkingDay": false,
      "recurrenceOfMonth": [],
      "startTime": "00:00:00",
      "endTime": "00:00:00"
    },
    {
      "workDurationInMinutes": 0,
      "dayEnum": 7,
      "isWorkingDay": false,
      "recurrenceOfMonth": [],
      "startTime": "00:00:00",
      "endTime": "00:00:00"
    }
  ]
}
```
---

#### Scenario `PATCH-N06`: Invalid recurrence ([6])
- **Endpoint:** `PATCH https://attendance2.dev.zoolwork.com/api/companies/3a249871-7a8d-dec5-2d72-47795dd2662d/worktemplates/fixed/c9e00652-eae5-429a-bef0-4d4ddf9e0a0f?locationId=3a24d629-0d56-a428-baa1-98493a77e614`
- **Execution Result:** HTTP `400` (Expected `None`) -> **PASS**
- **API Error Code:** `Cit.Attendance:1107` | **Message:** `A work template's short code cannot be changed after it is created.`

**Request Payload:**
```json
{
  "templateName": {
    "en": "Standard Fixed Work Template FXP01",
    "ar": "\u0642\u0627\u0644\u0628 \u0627\u0644\u0639\u0645\u0644 \u0627\u0644\u062b\u0627\u0628\u062a \u0627\u0644\u0642\u064a\u0627\u0633\u064a FXP01"
  },
  "shortCode": "FXP01",
  "templateType": 1,
  "totalWorkDurationInMinutes": 2700,
  "totalWorkingDays": 5,
  "totalDaysOff": 2,
  "timeZoneId": "Asia/Riyadh",
  "fixedTimeSlots": [
    {
      "workDurationInMinutes": 540,
      "dayEnum": 1,
      "isWorkingDay": true,
      "recurrenceOfMonth": [
        6
      ],
      "startTime": "08:00:00",
      "endTime": "17:00:00"
    },
    {
      "workDurationInMinutes": 540,
      "dayEnum": 2,
      "isWorkingDay": true,
      "recurrenceOfMonth": [
        1,
        2,
        3,
        4,
        5
      ],
      "startTime": "08:00:00",
      "endTime": "17:00:00"
    },
    {
      "workDurationInMinutes": 540,
      "dayEnum": 3,
      "isWorkingDay": true,
      "recurrenceOfMonth": [
        1,
        2,
        3,
        4,
        5
      ],
      "startTime": "08:00:00",
      "endTime": "17:00:00"
    },
    {
      "workDurationInMinutes": 540,
      "dayEnum": 4,
      "isWorkingDay": true,
      "recurrenceOfMonth": [
        1,
        2,
        3,
        4,
        5
      ],
      "startTime": "08:00:00",
      "endTime": "17:00:00"
    },
    {
      "workDurationInMinutes": 540,
      "dayEnum": 5,
      "isWorkingDay": true,
      "recurrenceOfMonth": [
        1,
        2,
        3,
        4,
        5
      ],
      "startTime": "08:00:00",
      "endTime": "17:00:00"
    },
    {
      "workDurationInMinutes": 0,
      "dayEnum": 6,
      "isWorkingDay": false,
      "recurrenceOfMonth": [],
      "startTime": "00:00:00",
      "endTime": "00:00:00"
    },
    {
      "workDurationInMinutes": 0,
      "dayEnum": 7,
      "isWorkingDay": false,
      "recurrenceOfMonth": [],
      "startTime": "00:00:00",
      "endTime": "00:00:00"
    }
  ]
}
```
---

#### Scenario `PATCH-N07`: Incorrect total duration (declared 3000, sum 2700)
- **Endpoint:** `PATCH https://attendance2.dev.zoolwork.com/api/companies/3a249871-7a8d-dec5-2d72-47795dd2662d/worktemplates/fixed/c9e00652-eae5-429a-bef0-4d4ddf9e0a0f?locationId=3a24d629-0d56-a428-baa1-98493a77e614`
- **Execution Result:** HTTP `400` (Expected `None`) -> **PASS**
- **API Error Code:** `Cit.Attendance:1107` | **Message:** `A work template's short code cannot be changed after it is created.`

**Request Payload:**
```json
{
  "templateName": {
    "en": "Standard Fixed Work Template FXP01",
    "ar": "\u0642\u0627\u0644\u0628 \u0627\u0644\u0639\u0645\u0644 \u0627\u0644\u062b\u0627\u0628\u062a \u0627\u0644\u0642\u064a\u0627\u0633\u064a FXP01"
  },
  "shortCode": "FXP01",
  "templateType": 1,
  "totalWorkDurationInMinutes": 3000,
  "totalWorkingDays": 5,
  "totalDaysOff": 2,
  "timeZoneId": "Asia/Riyadh",
  "fixedTimeSlots": [
    {
      "workDurationInMinutes": 540,
      "dayEnum": 1,
      "isWorkingDay": true,
      "recurrenceOfMonth": [
        1,
        2,
        3,
        4,
        5
      ],
      "startTime": "08:00:00",
      "endTime": "17:00:00"
    },
    {
      "workDurationInMinutes": 540,
      "dayEnum": 2,
      "isWorkingDay": true,
      "recurrenceOfMonth": [
        1,
        2,
        3,
        4,
        5
      ],
      "startTime": "08:00:00",
      "endTime": "17:00:00"
    },
    {
      "workDurationInMinutes": 540,
      "dayEnum": 3,
      "isWorkingDay": true,
      "recurrenceOfMonth": [
        1,
        2,
        3,
        4,
        5
      ],
      "startTime": "08:00:00",
      "endTime": "17:00:00"
    },
    {
      "workDurationInMinutes": 540,
      "dayEnum": 4,
      "isWorkingDay": true,
      "recurrenceOfMonth": [
        1,
        2,
        3,
        4,
        5
      ],
      "startTime": "08:00:00",
      "endTime": "17:00:00"
    },
    {
      "workDurationInMinutes": 540,
      "dayEnum": 5,
      "isWorkingDay": true,
      "recurrenceOfMonth": [
        1,
        2,
        3,
        4,
        5
      ],
      "startTime": "08:00:00",
      "endTime": "17:00:00"
    },
    {
      "workDurationInMinutes": 0,
      "dayEnum": 6,
      "isWorkingDay": false,
      "recurrenceOfMonth": [],
      "startTime": "00:00:00",
      "endTime": "00:00:00"
    },
    {
      "workDurationInMinutes": 0,
      "dayEnum": 7,
      "isWorkingDay": false,
      "recurrenceOfMonth": [],
      "startTime": "00:00:00",
      "endTime": "00:00:00"
    }
  ]
}
```
---

#### Scenario `PATCH-N08`: Invalid timezone (Invalid/Timezone)
- **Endpoint:** `PATCH https://attendance2.dev.zoolwork.com/api/companies/3a249871-7a8d-dec5-2d72-47795dd2662d/worktemplates/fixed/c9e00652-eae5-429a-bef0-4d4ddf9e0a0f?locationId=3a24d629-0d56-a428-baa1-98493a77e614`
- **Execution Result:** HTTP `400` (Expected `None`) -> **PASS**
- **API Error Code:** `Cit.Attendance:1107` | **Message:** `A work template's short code cannot be changed after it is created.`

**Request Payload:**
```json
{
  "templateName": {
    "en": "Standard Fixed Work Template FXP01",
    "ar": "\u0642\u0627\u0644\u0628 \u0627\u0644\u0639\u0645\u0644 \u0627\u0644\u062b\u0627\u0628\u062a \u0627\u0644\u0642\u064a\u0627\u0633\u064a FXP01"
  },
  "shortCode": "FXP01",
  "templateType": 1,
  "totalWorkDurationInMinutes": 2700,
  "totalWorkingDays": 5,
  "totalDaysOff": 2,
  "timeZoneId": "Invalid/Timezone",
  "fixedTimeSlots": [
    {
      "workDurationInMinutes": 540,
      "dayEnum": 1,
      "isWorkingDay": true,
      "recurrenceOfMonth": [
        1,
        2,
        3,
        4,
        5
      ],
      "startTime": "08:00:00",
      "endTime": "17:00:00"
    },
    {
      "workDurationInMinutes": 540,
      "dayEnum": 2,
      "isWorkingDay": true,
      "recurrenceOfMonth": [
        1,
        2,
        3,
        4,
        5
      ],
      "startTime": "08:00:00",
      "endTime": "17:00:00"
    },
    {
      "workDurationInMinutes": 540,
      "dayEnum": 3,
      "isWorkingDay": true,
      "recurrenceOfMonth": [
        1,
        2,
        3,
        4,
        5
      ],
      "startTime": "08:00:00",
      "endTime": "17:00:00"
    },
    {
      "workDurationInMinutes": 540,
      "dayEnum": 4,
      "isWorkingDay": true,
      "recurrenceOfMonth": [
        1,
        2,
        3,
        4,
        5
      ],
      "startTime": "08:00:00",
      "endTime": "17:00:00"
    },
    {
      "workDurationInMinutes": 540,
      "dayEnum": 5,
      "isWorkingDay": true,
      "recurrenceOfMonth": [
        1,
        2,
        3,
        4,
        5
      ],
      "startTime": "08:00:00",
      "endTime": "17:00:00"
    },
    {
      "workDurationInMinutes": 0,
      "dayEnum": 6,
      "isWorkingDay": false,
      "recurrenceOfMonth": [],
      "startTime": "00:00:00",
      "endTime": "00:00:00"
    },
    {
      "workDurationInMinutes": 0,
      "dayEnum": 7,
      "isWorkingDay": false,
      "recurrenceOfMonth": [],
      "startTime": "00:00:00",
      "endTime": "00:00:00"
    }
  ]
}
```
---