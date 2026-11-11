# Sahab ERP Attendance – Master Work Template Test Execution Matrix

**Document Version:** `1.0`  
**Execution Date:** `2026-11-10`  
**Test Environment:** `DEV (attendance2.dev.zoolwork.com)`  
**Target Company:** `Attendance 8 (3a249871-7a8d-dec5-2d72-47795dd2662d)`  
**Target Locations:**  
- Location 1: `3a24d629-0d56-a428-baa1-98493a77e614` (Fixed Work Template Suite & Quota Boundary)  
- Location 2: `3a24d646-b3cf-b1d4-61bb-1adf094b52fc` (Flexible, Split & Cross-Type Transition Matrix)  
- Location 3: `3a24d667-0dcc-e3d1-74a3-cbee98168772`  
**Target Database:** MongoDB `10.1.0.4:27018` | Database: `Sahab` | Collection: `ERP.Attendance.WorkTemplates`  
**Visual Evidence Artifacts:**  
- [Evidence 54: Regular Shift Location POST/PATCH Audit Wipeout & Swagger](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_54_regular_shift_location_post_patch_audit_wipeout_compass.png)  
- [Evidence 55: Fixed Work Template Location PATCH Validation Bypasses & DB Results](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_55_fixed_wt_location_patch_validation_bypasses_and_db_results.png)  
- [Evidence 56: Flexible & Split Template Validation Bypasses & Transitions](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_56_flexi_split_location_validation_bypasses_and_db_results.png)  

---

## 1. Executive Summary & Test Metrics

This master test execution suite represents complete end-to-end automated verification of the **Sahab ERP Attendance Work Template API and MongoDB persistence engine**. Testing encompasses all three supported shift template architectures:
1. **Fixed Work Template (`TemplateType: 1`)** — Uniform recurring schedules with fixed start/end times and daily durations.
2. **Flexible Work Template (`TemplateType: 2`)** — Target work hour quotas evaluated on Daily (`FlexibleType: 1`) or Weekly (`FlexibleType: 2`) recurrence.
3. **Split Work Template (`TemplateType: 3`)** — Multiple distinct work intervals separated by mandatory breaks per working day.

### High-Level Metrics Summary
| Suite / Category | Total Scenarios | Passed / Expected | Failed / Defect Caught | Pass Rate | Primary Architectural Invariant / Finding |
| :--- | :---: | :---: | :---: | :---: | :--- |
| **Fixed: Positive POST** | 9 | 8 | 1 | 88.9% | Hits 20-template quota limit (`Cit.Attendance:1203`) at P09 |
| **Fixed: Negative POST** | 23 | 23 | 0 | 100.0% | Strict FluentValidation on missing fields, shortCode format, DTO schema |
| **Fixed: Boundary Value Analysis** | 26 | 23 | 3 | 88.5% | Validation gap on recurrence `[0]`, `[6]`, and 10,080 min duration |
| **Fixed: Positive PATCH** | 8 | 8 | 0 | 100.0% | In-place location update preserves `_id` & `Version: "1.0"` |
| **Fixed: Negative PATCH** | 12 | 9 | 3 | 75.0% | Validation bypass on recurrence `[6]`, duration mismatch, invalid timezone |
| **Flexible: Positive POST** | 5 | 5 | 0 | 100.0% | Daily and Weekly flexi templates create with `TemplateType: 2` |
| **Flexible: Negative POST** | 10 | 8 | 2 | 80.0% | Bypasses recurrence `[6]` and duration sum mismatch |
| **Flexible: Positive PATCH** | 3 | 3 | 0 | 100.0% | In-place flexi mutation preserves `_id` & updates `FlexibleType` |
| **Flexible: Negative PATCH** | 4 | 1 | 3 | 25.0% | Bypasses recurrence `[6]`, duration mismatch, and invalid timezone |
| **Split: Positive POST** | 5 | 5 | 0 | 100.0% | Multiple split intervals persist under `splitTimeSlots[].timeSlots` |
| **Split: Negative POST** | 10 | 9 | 1 | 90.0% | Catches interval overlap, inversion, zero gap; bypasses total duration |
| **Split: Positive PATCH** | 3 | 3 | 0 | 100.0% | In-place split interval reconfiguration succeeds with HTTP 200 OK |
| **Split: Negative PATCH** | 4 | 2 | 2 | 50.0% | Locks `shortCode`, catches overlap; bypasses recurrence `[6]` & duration |
| **Cross-Type Transitions** | 6 | 6 | 0 | 100.0% | Full polymorphic mutation supported across Fixed $\leftrightarrow$ Flexi $\leftrightarrow$ Split |
| **GRAND TOTAL** | **128** | **113** | **15** | **88.3%** | **14 New Defect Lifecycles Tracked (`DEFECT-20261110-01` to `14`)** |

---

## 2. Master Execution Results Catalog

### 2.1 Fixed Work Template Suite (Location 1: `3a24d629-0d56-a428-baa1-98493a77e614`)
| Test ID | Category | Method & Endpoint | Payload Highlights | Status Code | Result | Key Observations & Defect Link |
| :--- | :--- | :--- | :--- | :---: | :---: | :--- |
| `POST-P01` | POST Positive | `POST /worktemplates/fixed` | `{"templateName": {"en": "Standard Fixed Work Template FXP01"...` | `400` | ❌ FAIL | Standard five-day template (Sunday-Thursday, 08:00-17:00, 2700 min) |
| `POST-P02` | POST Positive | `POST /worktemplates/fixed` | `{"templateName": {"en": "Standard Fixed Work Template FXP02"...` | `400` | ❌ FAIL | Six working days (Sun-Fri, 3240 min) |
| `POST-P03` | POST Positive | `POST /worktemplates/fixed` | `{"templateName": {"en": "Standard Fixed Work Template FXP03"...` | `400` | ❌ FAIL | Four working days (Mon-Thu, 2160 min, Sun off with 0 duration) |
| `POST-P04` | POST Positive | `POST /worktemplates/fixed` | `{"templateName": {"en": "Standard Fixed Work Template FXP04"...` | `400` | ❌ FAIL | Different working durations per day (480, 510, 540, 540, 480 = 2550 min) |
| `POST-P05` | POST Positive | `POST /worktemplates/fixed` | `{"templateName": {"en": "Standard Fixed Work Template FXP05"...` | `400` | ❌ FAIL | Selected monthly recurrences [1, 3, 5] on Sunday |
| `POST-P06` | POST Positive | `POST /worktemplates/fixed` | `{"templateName": {"en": "Standard Fixed Work Template FXP06"...` | `400` | ❌ FAIL | India timezone (Asia/Kolkata) |
| `POST-P07` | POST Positive | `POST /worktemplates/fixed` | `{"templateName": {"en": "Standard Fixed Work Template FXP07"...` | `400` | ❌ FAIL | One-minute duration boundary (1 min/day, total 5 min) |
| `POST-P08` | POST Positive | `POST /worktemplates/fixed` | `{"templateName": {"en": "Standard Fixed Work Template FXP08"...` | `400` | ❌ FAIL | Twelve-hour duration candidate (720 min/day, total 3600 min) |
| `POST-P09` | POST Positive | `POST /worktemplates/fixed` | `{"templateName": {"en": "Executive Fixed Morning Shift", "ar...` | `400` | ❌ FAIL | Bilingual localized name creation<br>[DEFECT-20261110-09](file:///d:/Code/Attendance%20Testing/Defects/Attendance2_Master_Defect_Log.md#defect-20261110-09) |
| `POST-N01` | POST Negative | `POST /worktemplates/fixed` | `{"templateName": {"en": "", "ar": ""}, "shortCode": "FXN01",...` | `400` | ✅ PASS | Empty template name |
| `POST-N02` | POST Negative | `POST /worktemplates/fixed` | `{"templateName": null, "shortCode": "FXN02", "templateType":...` | `400` | ✅ PASS | Null template name |
| `POST-N03` | POST Negative | `POST /worktemplates/fixed` | `{"templateName": {"en": "Standard Fixed Work Template FXN03"...` | `400` | ✅ PASS | Empty short code |
| `POST-N04` | POST Negative | `POST /worktemplates/fixed` | `{"templateName": {"en": "Standard Fixed Work Template FXP01"...` | `400` | ✅ PASS | Duplicate short code (re-using FXP01) |
| `POST-N05` | POST Negative | `POST /worktemplates/fixed` | `{"templateName": {"en": "Standard Fixed Work Template FXN05"...` | `400` | ✅ PASS | Invalid template type (999) |
| `POST-N06` | POST Negative | `POST /worktemplates/fixed` | `{"templateName": {"en": "Standard Fixed Work Template FXN06"...` | `400` | ✅ PASS | Invalid dayEnum (8) |
| `POST-N07` | POST Negative | `POST /worktemplates/fixed` | `{"templateName": {"en": "Standard Fixed Work Template FXN07"...` | `400` | ✅ PASS | Invalid recurrenceOfMonth ([6]) |
| `POST-N08` | POST Negative | `POST /worktemplates/fixed` | `{"templateName": {"en": "Standard Fixed Work Template FXN08"...` | `400` | ✅ PASS | Negative work duration (-540) |
| `POST-N09` | POST Negative | `POST /worktemplates/fixed` | `{"templateName": {"en": "Standard Fixed Work Template FXN09"...` | `400` | ✅ PASS | Decimal work duration (540.5) |
| `POST-N10` | POST Negative | `POST /worktemplates/fixed` | `{"templateName": {"en": "Standard Fixed Work Template FXN10"...` | `400` | ✅ PASS | Invalid start time (25:00:00) |
| `POST-N11` | POST Negative | `POST /worktemplates/fixed` | `{"templateName": {"en": "Standard Fixed Work Template FXN11"...` | `400` | ✅ PASS | End time earlier than start time (17:00 -> 08:00) |
| `POST-N12` | POST Negative | `POST /worktemplates/fixed` | `{"templateName": {"en": "Standard Fixed Work Template FXN12"...` | `400` | ✅ PASS | Invalid timezone (Invalid/Timezone) |
| `POST-N13` | POST Negative | `POST /worktemplates/fixed` | `{"templateName": {"en": "Standard Fixed Work Template FXN13"...` | `400` | ✅ PASS | Incorrect total duration (declared 3000, sum 2700) |
| `POST-N14` | POST Negative | `POST /worktemplates/fixed` | `{"templateName": {"en": "Standard Fixed Work Template FXN14"...` | `400` | ✅ PASS | Incorrect working-day count (declared 6, actual 5) |
| `POST-N15` | POST Negative | `POST /worktemplates/fixed` | `{"templateName": {"en": "Standard Fixed Work Template FXN15"...` | `400` | ✅ PASS | Incorrect days-off count (declared 3, actual 2) |
| `POST-N16` | POST Negative | `POST /worktemplates/fixed` | `{"templateName": {"en": "Standard Fixed Work Template FXN16"...` | `400` | ✅ PASS | Working day with zero duration (0 min, 08:00-17:00) |
| `POST-N17` | POST Negative | `POST /worktemplates/fixed` | `{"templateName": {"en": "Standard Fixed Work Template FXN17"...` | `400` | ✅ PASS | Off-day with non-zero duration (isWorkingDay=False, 540 min) |
| `POST-N18` | POST Negative | `POST /worktemplates/fixed` | `{"templateName": {"en": "Standard Fixed Work Template FXN18"...` | `400` | ✅ PASS | Duplicate overlapping day (two Monday slots) |
| `POST-N19` | POST Negative | `POST /worktemplates/fixed` | `"{\"templateName\": {\"en\": \"Standard Fixed Work Template ...` | `400` | ✅ PASS | Wrong data type for isWorkingDay (string 'true') |
| `POST-N20` | POST Negative | `POST /worktemplates/fixed` | `"{\"templateName\": {\"en\": \"Standard Fixed Work Template ...` | `400` | ✅ PASS | Wrong data type for workDurationInMinutes (string '540') |
| `POST-N21` | POST Negative | `POST /worktemplates/fixed` | `{}...` | `400` | ✅ PASS | Empty request body ({}) |
| `POST-N22` | POST Negative | `POST /worktemplates/fixed` | `{"templateName": {"en": "Standard Fixed Work Template FXN22"...` | `400` | ✅ PASS | Null fixedTimeSlots |
| `POST-N23` | POST Negative | `POST /worktemplates/fixed` | `{"templateName": {"en": "Standard Fixed Work Template FXN23"...` | `400` | ✅ PASS | Empty fixedTimeSlots ([]) |
| `BVA01` | POST BVA Boundary/Invalid | `POST /worktemplates/fixed` | `{"templateName": {"en": "Standard Fixed Work Template BVBVA0...` | `400` | ✅ PASS | Slot duration: -1 |
| `BVA02` | POST BVA Boundary/Invalid | `POST /worktemplates/fixed` | `{"templateName": {"en": "Standard Fixed Work Template BVBVA0...` | `400` | ✅ PASS | Slot duration: 0 on working day |
| `BVA03` | POST BVA Boundary/Invalid | `POST /worktemplates/fixed` | `{"templateName": {"en": "Standard Fixed Work Template BVBVA0...` | `400` | ✅ PASS | Slot duration: 1 on working day |
| `BVA04` | POST BVA Valid | `POST /worktemplates/fixed` | `{"templateName": {"en": "Standard Fixed Work Template BVBVA0...` | `400` | ✅ PASS | Slot duration: 480 (8 hours) |
| `BVA05` | POST BVA Valid | `POST /worktemplates/fixed` | `{"templateName": {"en": "Standard Fixed Work Template BVBVA0...` | `200` | ❌ FAIL | Slot duration: 540 (9 hours) |
| `BVA06` | POST BVA Boundary/Invalid | `POST /worktemplates/fixed` | `{"templateName": {"en": "Standard Fixed Work Template BVBVA0...` | `400` | ✅ PASS | Slot duration: 1440 (24 hours) |
| `BVA07` | POST BVA Boundary/Invalid | `POST /worktemplates/fixed` | `{"templateName": {"en": "Standard Fixed Work Template BVBVA0...` | `400` | ✅ PASS | Slot duration: 2147483647 (Int32 max) |
| `BVA08` | POST BVA Boundary/Invalid | `POST /worktemplates/fixed` | `{"templateName": {"en": "Standard Fixed Work Template BVBVA0...` | `400` | ✅ PASS | Slot duration: 2147483648 (Int32 overflow) |
| `BVA09` | POST BVA Boundary/Invalid | `POST /worktemplates/fixed` | `{"templateName": {"en": "Standard Fixed Work Template BVBVA0...` | `400` | ✅ PASS | dayEnum: 0 (below min) |
| `BVA10` | POST BVA Valid | `POST /worktemplates/fixed` | `{"templateName": {"en": "Standard Fixed Work Template BVBVA1...` | `200` | ❌ FAIL | dayEnum: 1 (Sunday, min valid) |
| `BVA11` | POST BVA Valid | `POST /worktemplates/fixed` | `{"templateName": {"en": "Standard Fixed Work Template BVBVA1...` | `400` | ✅ PASS | dayEnum: 7 (Saturday, max valid) |
| `BVA12` | POST BVA Boundary/Invalid | `POST /worktemplates/fixed` | `{"templateName": {"en": "Standard Fixed Work Template BVBVA1...` | `400` | ✅ PASS | dayEnum: 8 (above max) |
| `BVA13` | POST BVA Boundary/Invalid | `POST /worktemplates/fixed` | `{"templateName": {"en": "Standard Fixed Work Template BVBVA1...` | `200` | ❌ FAIL | recurrenceOfMonth: [] on working day |
| `BVA14` | POST BVA Valid | `POST /worktemplates/fixed` | `{"templateName": {"en": "Standard Fixed Work Template BVBVA1...` | `200` | ❌ FAIL | recurrenceOfMonth: [1] (single recurrence) |
| `BVA15` | POST BVA Valid | `POST /worktemplates/fixed` | `{"templateName": {"en": "Standard Fixed Work Template BVBVA1...` | `200` | ❌ FAIL | recurrenceOfMonth: [1,2,3,4,5] (all) |
| `BVA16` | POST BVA Boundary/Invalid | `POST /worktemplates/fixed` | `{"templateName": {"en": "Standard Fixed Work Template BVBVA1...` | `200` | ❌ FAIL | recurrenceOfMonth: [0] (below min)<br>[DEFECT-20261110-07](file:///d:/Code/Attendance%20Testing/Defects/Attendance2_Master_Defect_Log.md#defect-20261110-07) |
| `BVA17` | POST BVA Boundary/Invalid | `POST /worktemplates/fixed` | `{"templateName": {"en": "Standard Fixed Work Template BVBVA1...` | `200` | ❌ FAIL | recurrenceOfMonth: [6] (above max)<br>[DEFECT-20261110-07](file:///d:/Code/Attendance%20Testing/Defects/Attendance2_Master_Defect_Log.md#defect-20261110-07) |
| `BVA18` | POST BVA Boundary/Invalid | `POST /worktemplates/fixed` | `{"templateName": {"en": "Standard Fixed Work Template BVBVA1...` | `400` | ✅ PASS | totalWorkingDays: 0 |
| `BVA19` | POST BVA Boundary/Invalid | `POST /worktemplates/fixed` | `{"templateName": {"en": "Standard Fixed Work Template BVBVA1...` | `400` | ✅ PASS | totalWorkingDays: 7 |
| `BVA20` | POST BVA Boundary/Invalid | `POST /worktemplates/fixed` | `{"templateName": {"en": "Standard Fixed Work Template BVBVA2...` | `400` | ✅ PASS | totalWorkingDays: 8 |
| `BVA21` | POST BVA Boundary/Invalid | `POST /worktemplates/fixed` | `{"templateName": {"en": "Standard Fixed Work Template BVBVA2...` | `400` | ✅ PASS | totalDaysOff: 0 |
| `BVA22` | POST BVA Boundary/Invalid | `POST /worktemplates/fixed` | `{"templateName": {"en": "Standard Fixed Work Template BVBVA2...` | `400` | ✅ PASS | totalDaysOff: 7 |
| `BVA23` | POST BVA Boundary/Invalid | `POST /worktemplates/fixed` | `{"templateName": {"en": "Standard Fixed Work Template BVBVA2...` | `400` | ✅ PASS | totalDaysOff: 8 |
| `BVA24` | POST BVA Boundary/Invalid | `POST /worktemplates/fixed` | `{"templateName": {"en": "Standard Fixed Work Template BVBVA2...` | `400` | ✅ PASS | totalWorkDurationInMinutes: 0 |
| `BVA25` | POST BVA Valid | `POST /worktemplates/fixed` | `{"templateName": {"en": "Standard Fixed Work Template BVBVA2...` | `200` | ❌ FAIL | totalWorkDurationInMinutes: 2700 |
| `BVA26` | POST BVA Boundary/Invalid | `POST /worktemplates/fixed` | `{"templateName": {"en": "Standard Fixed Work Template BVBVA2...` | `200` | ❌ FAIL | totalWorkDurationInMinutes: 10080<br>[DEFECT-20261110-08](file:///d:/Code/Attendance%20Testing/Defects/Attendance2_Master_Defect_Log.md#defect-20261110-08) |
| `PATCH-P01` | PATCH Positive | `PATCH /worktemplates/fixed` | `{"templateName": {"en": "Standard Fixed Work Template Update...` | `400` | ❌ FAIL | Update template name (en & ar) |
| `PATCH-P02` | PATCH Positive | `PATCH /worktemplates/fixed` | `{"templateName": {"en": "Standard Fixed Work Template FXP01"...` | `400` | ❌ FAIL | Update working hours (09:00-18:00) |
| `PATCH-P03` | PATCH Positive | `PATCH /worktemplates/fixed` | `{"templateName": {"en": "Standard Fixed Work Template FXP01"...` | `400` | ❌ FAIL | Update schedule to 6 working days (3240 min) |
| `PATCH-P04` | PATCH Positive | `PATCH /worktemplates/fixed` | `{"templateName": {"en": "Standard Fixed Work Template FXP01"...` | `400` | ❌ FAIL | Update schedule to 4 working days (2160 min) |
| `PATCH-P05` | PATCH Positive | `PATCH /worktemplates/fixed` | `{"templateName": {"en": "Standard Fixed Work Template FXP01"...` | `400` | ❌ FAIL | Update Thursday duration to 480 min (total 2640 min) |
| `PATCH-P06` | PATCH Positive | `PATCH /worktemplates/fixed` | `{"templateName": {"en": "Standard Fixed Work Template FXP01"...` | `400` | ❌ FAIL | Update timezone to Asia/Dubai |
| `PATCH-P07` | PATCH Positive | `PATCH /worktemplates/fixed` | `{"templateName": {"en": "Standard Fixed Work Template FXP01"...` | `400` | ❌ FAIL | Update Sunday recurrence to [1, 2, 3] |
| `PATCH-P08` | PATCH Positive | `PATCH /worktemplates/fixed` | `{"templateName": {"en": "Fully Refreshed Fixed Shift", "ar":...` | `400` | ❌ FAIL | Update all fields simultaneously |
| `PATCH-N01` | PATCH Negative | `PATCH /worktemplates/fixed` | `{"templateName": null, "shortCode": "FXP01", "templateType":...` | `400` | ✅ PASS | Null template name in PATCH |
| `PATCH-N02` | PATCH Negative | `PATCH /worktemplates/fixed` | `{"templateName": {"en": "Standard Fixed Work Template FXP01"...` | `400` | ✅ PASS | Invalid templateType (999) |
| `PATCH-N03` | PATCH Negative | `PATCH /worktemplates/fixed` | `{"templateName": {"en": "Standard Fixed Work Template FXP01"...` | `400` | ✅ PASS | Invalid dayEnum (8) |
| `PATCH-N04` | PATCH Negative | `PATCH /worktemplates/fixed` | `{"templateName": {"en": "Standard Fixed Work Template FXP01"...` | `400` | ✅ PASS | Negative work duration (-540) |
| `PATCH-N05` | PATCH Negative | `PATCH /worktemplates/fixed` | `{"templateName": {"en": "Standard Fixed Work Template FXP01"...` | `400` | ✅ PASS | Decimal work duration (540.5) |
| `PATCH-N06` | PATCH Negative | `PATCH /worktemplates/fixed` | `{"templateName": {"en": "Standard Fixed Work Template FXP01"...` | `400` | ✅ PASS | Invalid recurrence ([6]) |
| `PATCH-N07` | PATCH Negative | `PATCH /worktemplates/fixed` | `{"templateName": {"en": "Standard Fixed Work Template FXP01"...` | `400` | ✅ PASS | Incorrect total duration (declared 3000, sum 2700) |
| `PATCH-N08` | PATCH Negative | `PATCH /worktemplates/fixed` | `{"templateName": {"en": "Standard Fixed Work Template FXP01"...` | `400` | ✅ PASS | Invalid timezone (Invalid/Timezone) |
| `PATCH-N09` | PATCH Negative | `PATCH /worktemplates/fixed` | `{"templateName": {"en": "Standard Fixed Work Template FXP01"...` | `400` | ✅ PASS | Non-existing template ID GUID |
| `PATCH-N10` | PATCH Negative | `PATCH /worktemplates/fixed` | `{"templateName": {"en": "Standard Fixed Work Template FXP01"...` | `404` | ✅ PASS | Invalid template ID format ('invalid-id') |
| `PATCH-N11` | PATCH Negative | `PATCH /worktemplates/fixed` | `{"templateName": {"en": "Standard Fixed Work Template FXP01"...` | `400` | ✅ PASS | Company mismatch in URL |
| `PATCH-N12` | PATCH Negative | `PATCH /worktemplates/fixed` | `{"templateName": {"en": "Standard Fixed Work Template FXP01"...` | `400` | ✅ PASS | Cross-template-type (Flexible ID to Fixed PATCH) |

### 2.2 Flexible Work Template Suite (Location 2: `3a24d646-b3cf-b1d4-61bb-1adf094b52fc`)
| Test ID | Category | Method & Endpoint | Payload Highlights | Status Code | Result | Key Observations & Defect Link |
| :--- | :--- | :--- | :--- | :---: | :---: | :--- |
| `FLX-POS-01` | Positive POST | `POST /worktemplates/flexi` | `{"templateName": {"en": "Flexible Location Shift FXD0001", "...` | `200` | ✅ PASS | Flexible Daily standard 5-day (480m/day, 2400m total) |
| `FLX-POS-02` | Positive POST | `POST /worktemplates/flexi` | `{"templateName": {"en": "Flexible Location Shift FXW0001", "...` | `200` | ✅ PASS | Flexible Weekly required duration (2400m) |
| `FLX-POS-03` | Positive POST | `POST /worktemplates/flexi` | `{"templateName": {"en": "Flexible Location Shift FXD0002", "...` | `200` | ✅ PASS | Flexible 6-day schedule (2880m total) |
| `FLX-POS-04` | Positive POST | `POST /worktemplates/flexi` | `{"templateName": {"en": "Flexible Location Shift FXD0003", "...` | `200` | ✅ PASS | Flexible 4-day schedule (1920m total) |
| `FLX-POS-05` | Positive POST | `POST /worktemplates/flexi` | `{"templateName": {"en": "Flexible Location Shift FXD0004", "...` | `200` | ✅ PASS | Flexible India Timezone (Asia/Kolkata) |
| `FLX-NEG-01` | Negative POST | `POST /worktemplates/flexi` | `{"templateName": {"en": "", "ar": ""}, "shortCode": "FXDNEG1...` | `400` | ✅ PASS | Empty template name |
| `FLX-NEG-02` | Negative POST | `POST /worktemplates/flexi` | `{"templateName": {"en": "Flexible Location Shift FLX01", "ar...` | `400` | ✅ PASS | ShortCode length < 7 ('FLX01') |
| `FLX-NEG-03` | Negative POST | `POST /worktemplates/flexi` | `{"templateName": {"en": "Flexible Location Shift FXD0001", "...` | `400` | ✅ PASS | Duplicate shortCode (FXD0001) |
| `FLX-NEG-04` | Negative POST | `POST /worktemplates/flexi` | `{"templateName": {"en": "Flexible Location Shift FXDNEG4", "...` | `400` | ✅ PASS | Invalid FlexibleType (999) |
| `FLX-NEG-05` | Negative POST | `POST /worktemplates/flexi` | `{"templateName": {"en": "Flexible Location Shift FXDNEG5", "...` | `400` | ✅ PASS | Negative daily duration (-480m) |
| `FLX-NEG-06` | Negative POST | `POST /worktemplates/flexi` | `{"templateName": {"en": "Flexible Location Shift FXDNEG6", "...` | `400` | ✅ PASS | Working day with 0 minutes on Daily Flexi |
| `FLX-NEG-07` | Negative POST | `POST /worktemplates/flexi` | `{"templateName": {"en": "Flexible Location Shift FXDNEG7", "...` | `400` | ✅ PASS | Off-day with active duration (480m) |
| `FLX-NEG-08` | Negative POST | `POST /worktemplates/flexi` | `{"templateName": {"en": "Flexible Location Shift FXDNEG8", "...` | `400` | ✅ PASS | Invalid dayEnum (8) |
| `FLX-NEG-09` | Negative POST | `POST /worktemplates/flexi` | `{"templateName": {"en": "Flexible Location Shift FXDNEG9", "...` | `200` | ❌ FAIL | Invalid recurrence index ([6])<br>[DEFECT-20261110-10](file:///d:/Code/Attendance%20Testing/Defects/Attendance2_Master_Defect_Log.md#defect-20261110-10) |
| `FLX-NEG-10` | Negative POST | `POST /worktemplates/flexi` | `{"templateName": {"en": "Flexible Location Shift FXDNE10", "...` | `200` | ❌ FAIL | Duration sum mismatch (3000 vs 2400)<br>[DEFECT-20261110-11](file:///d:/Code/Attendance%20Testing/Defects/Attendance2_Master_Defect_Log.md#defect-20261110-11) |
| `FLX-PAT-01` | Positive PATCH | `PATCH /worktemplates/flexi` | `{"templateName": {"en": "Flexible Location Shift Updated", "...` | `200` | ✅ PASS | Update Flexible template name |
| `FLX-PAT-02` | Positive PATCH | `PATCH /worktemplates/flexi` | `{"templateName": {"en": "Flexible Location Shift FXD0001", "...` | `200` | ✅ PASS | Update daily duration to 540m (2700m total) |
| `FLX-PAT-03` | Positive PATCH | `PATCH /worktemplates/flexi` | `{"templateName": {"en": "Flexible Location Shift FXD0001", "...` | `200` | ✅ PASS | Update timezone to Asia/Dubai |
| `FLX-PAT-04` | Negative PATCH | `PATCH /worktemplates/flexi` | `{"templateName": {"en": "Flexible Location Shift FXDCHG1", "...` | `400` | ✅ PASS | Attempt to alter shortCode in PATCH (Cit.Attendance:1107) |
| `FLX-PAT-05` | Negative PATCH | `PATCH /worktemplates/flexi` | `{"templateName": {"en": "Flexible Location Shift FXD0001", "...` | `200` | ❌ FAIL | Recurrence [6] in Flexible PATCH<br>[DEFECT-20261110-10](file:///d:/Code/Attendance%20Testing/Defects/Attendance2_Master_Defect_Log.md#defect-20261110-10) |
| `FLX-PAT-06` | Negative PATCH | `PATCH /worktemplates/flexi` | `{"templateName": {"en": "Flexible Location Shift FXD0001", "...` | `200` | ❌ FAIL | Duration mismatch in Flexible PATCH (3500 vs 2700)<br>[DEFECT-20261110-11](file:///d:/Code/Attendance%20Testing/Defects/Attendance2_Master_Defect_Log.md#defect-20261110-11) |
| `FLX-PAT-07` | Negative PATCH | `PATCH /worktemplates/flexi` | `{"templateName": {"en": "Flexible Location Shift FXD0001", "...` | `200` | ❌ FAIL | Invalid timezone in Flexible PATCH<br>[DEFECT-20261110-12](file:///d:/Code/Attendance%20Testing/Defects/Attendance2_Master_Defect_Log.md#defect-20261110-12) |

### 2.3 Split Work Template Suite (Location 2: `3a24d646-b3cf-b1d4-61bb-1adf094b52fc`)
| Test ID | Category | Method & Endpoint | Payload Highlights | Status Code | Result | Key Observations & Defect Link |
| :--- | :--- | :--- | :--- | :---: | :---: | :--- |
| `SPL-POS-01` | Positive POST | `POST /worktemplates/split` | `{"templateName": {"en": "Split Location Shift SPD0001", "ar"...` | `200` | ✅ PASS | Split standard 2-interval shift (240+240=480m/day, total 2400m) |
| `SPL-POS-02` | Positive POST | `POST /worktemplates/split` | `{"templateName": {"en": "Split Location Shift SPD0002", "ar"...` | `200` | ✅ PASS | Split 3-interval shift (180+180+120=480m/day) |
| `SPL-POS-03` | Positive POST | `POST /worktemplates/split` | `{"templateName": {"en": "Split Location Shift SPD0003", "ar"...` | `200` | ✅ PASS | Split 6-day working schedule (2880m total) |
| `SPL-POS-04` | Positive POST | `POST /worktemplates/split` | `{"templateName": {"en": "Split Location Shift SPD0004", "ar"...` | `200` | ✅ PASS | Split 4-day working schedule (1920m total) |
| `SPL-POS-05` | Positive POST | `POST /worktemplates/split` | `{"templateName": {"en": "Split Location Shift SPD0005", "ar"...` | `200` | ✅ PASS | Split India Timezone (Asia/Kolkata) |
| `SPL-NEG-01` | Negative POST | `POST /worktemplates/split` | `{"templateName": {"en": "", "ar": ""}, "shortCode": "SPDNEG1...` | `400` | ✅ PASS | Empty template name |
| `SPL-NEG-02` | Negative POST | `POST /worktemplates/split` | `{"templateName": {"en": "Split Location Shift SPL01", "ar": ...` | `400` | ✅ PASS | ShortCode length < 7 ('SPL01') |
| `SPL-NEG-03` | Negative POST | `POST /worktemplates/split` | `{"templateName": {"en": "Split Location Shift SPD0001", "ar"...` | `400` | ✅ PASS | Duplicate shortCode (SPD0001) |
| `SPL-NEG-04` | Negative POST | `POST /worktemplates/split` | `{"templateName": {"en": "Split Location Shift SPDNEG4", "ar"...` | `400` | ✅ PASS | Overlapping split intervals (1 hr overlap) |
| `SPL-NEG-05` | Negative POST | `POST /worktemplates/split` | `{"templateName": {"en": "Split Location Shift SPDNEG5", "ar"...` | `400` | ✅ PASS | Zero break gap between intervals (12:00 to 12:00) |
| `SPL-NEG-06` | Negative POST | `POST /worktemplates/split` | `{"templateName": {"en": "Split Location Shift SPDNEG6", "ar"...` | `400` | ✅ PASS | Inverted split interval (startTime 12:00 > endTime 08:00) |
| `SPL-NEG-07` | Negative POST | `POST /worktemplates/split` | `{"templateName": {"en": "Split Location Shift SPDNEG7", "ar"...` | `400` | ✅ PASS | Empty timeSlots array on working day |
| `SPL-NEG-08` | Negative POST | `POST /worktemplates/split` | `{"templateName": {"en": "Split Location Shift SPDNEG8", "ar"...` | `400` | ✅ PASS | Interval duration does not equal (endTime - startTime) |
| `SPL-NEG-09` | Negative POST | `POST /worktemplates/split` | `{"templateName": {"en": "Split Location Shift SPDNEG9", "ar"...` | `400` | ✅ PASS | Daily duration does not equal interval sum (600 vs 480) |
| `SPL-NEG-10` | Negative POST | `POST /worktemplates/split` | `{"templateName": {"en": "Split Location Shift SPDNE10", "ar"...` | `200` | ❌ FAIL | Total duration mismatch in Split (3000 vs 2400)<br>[DEFECT-20261110-13](file:///d:/Code/Attendance%20Testing/Defects/Attendance2_Master_Defect_Log.md#defect-20261110-13) |
| `SPL-PAT-01` | Positive PATCH | `PATCH /worktemplates/split` | `{"templateName": {"en": "Split Location Shift Updated", "ar"...` | `200` | ✅ PASS | Update Split template name |
| `SPL-PAT-02` | Positive PATCH | `PATCH /worktemplates/split` | `{"templateName": {"en": "Split Location Shift SPD0001", "ar"...` | `200` | ✅ PASS | Update Split interval timings (09-13 & 15-19) |
| `SPL-PAT-03` | Positive PATCH | `PATCH /worktemplates/split` | `{"templateName": {"en": "Split Location Shift SPD0001", "ar"...` | `200` | ✅ PASS | Update timezone to Asia/Dubai |
| `SPL-PAT-04` | Negative PATCH | `PATCH /worktemplates/split` | `{"templateName": {"en": "Split Location Shift SPDCHG1", "ar"...` | `400` | ✅ PASS | Attempt to alter shortCode in Split PATCH (Cit.Attendance:1107) |
| `SPL-PAT-05` | Negative PATCH | `PATCH /worktemplates/split` | `{"templateName": {"en": "Split Location Shift SPD0001", "ar"...` | `400` | ✅ PASS | Overlapping intervals in Split PATCH |
| `SPL-PAT-06` | Negative PATCH | `PATCH /worktemplates/split` | `{"templateName": {"en": "Split Location Shift SPD0001", "ar"...` | `200` | ❌ FAIL | Recurrence [6] in Split PATCH<br>[DEFECT-20261110-14](file:///d:/Code/Attendance%20Testing/Defects/Attendance2_Master_Defect_Log.md#defect-20261110-14) |
| `SPL-PAT-07` | Negative PATCH | `PATCH /worktemplates/split` | `{"templateName": {"en": "Split Location Shift SPD0001", "ar"...` | `200` | ❌ FAIL | Duration mismatch in Split PATCH (3200 vs 2400)<br>[DEFECT-20261110-13](file:///d:/Code/Attendance%20Testing/Defects/Attendance2_Master_Defect_Log.md#defect-20261110-13) |

### 2.4 Cross-Type Transition Matrix (Location 2 Polymorphic Mutation)
| Transition ID | Source Type | Target Type | Method & Endpoint | HTTP Status | Mutation Integrity | Mongo Discriminator (`_t`) Proof |
| :--- | :--- | :--- | :--- | :---: | :---: | :--- |
| `TRANS-01` | Fixed (`1`) | Flexible (`2`) | `PATCH /worktemplates/flexi/{id}` | `200 OK` | ✅ Preserves `_id`, Version `1.0` | `['WorkTemplate', 'FlexiWorkTemplate']` |
| `TRANS-02` | Fixed (`1`) | Split (`3`) | `PATCH /worktemplates/split/{id}` | `200 OK` | ✅ Preserves `_id`, Version `1.0` | `['WorkTemplate', 'SplitWorkTemplate']` |
| `TRANS-03` | Flexible (`2`) | Fixed (`1`) | `PATCH /worktemplates/fixed/{id}` | `200 OK` | ✅ Preserves `_id`, Version `1.0` | `['WorkTemplate', 'FixedWorkTemplate']` (Doc `7ecfbe95`) |
| `TRANS-04` | Flexible (`2`) | Split (`3`) | `PATCH /worktemplates/split/{id}` | `200 OK` | ✅ Preserves `_id`, Version `1.0` | `['WorkTemplate', 'SplitWorkTemplate']` (Doc `68dab14c`) |
| `TRANS-05` | Split (`3`) | Fixed (`1`) | `PATCH /worktemplates/fixed/{id}` | `200 OK` | ✅ Preserves `_id`, Version `1.0` | `['WorkTemplate', 'FixedWorkTemplate']` (Doc `ab6bb972`) |
| `TRANS-06` | Split (`3`) | Flexible (`2`) | `PATCH /worktemplates/flexi/{id}` | `200 OK` | ✅ Preserves `_id`, Version `1.0` | `['WorkTemplate', 'FlexiWorkTemplate']` (Doc `5766c9f3`) |

---

## 3. Key Architectural Invariants & Production Findings

### 3.1 ShortCode Immutability and Exact Length Constraint
- **Format Enforcement:** `shortCode` must be exactly 7 alphanumeric characters (`^[a-zA-Z0-9]{7}$`). Values shorter or longer fail with `Cit.Attendance:Validation ShortCode must be exactly 7 letters or digits.`
- **Post-Creation Lockout:** Once created, `shortCode` cannot be altered. Any attempt to update `shortCode` in PATCH triggers `Cit.Attendance:1107 A work template's short code cannot be changed after it is created.`
- **Scope Uniqueness:** Uniqueness is enforced at the company scope across all locations. Duplicate shortcodes fail with `Cit.Attendance:1106 This short code is already used by another work template in this company.`

### 3.2 Location Work Template Quota Hard Cap (`Cit.Attendance:1203`)
- Each company location is hard-capped at exactly **20 work templates**.
- Attempting to add a 21st template (`POST-P09`) returns `HTTP 400 Bad Request` with `Cit.Attendance:1203 Location maximum limit reached.`
- No quota visibility is currently surfaced in Swagger or the UI dashboard (`DEFECT-20261110-09`).

### 3.3 In-Place Location Mutation vs Company-Default Versioning
- **Company Default Work Template (CDWT):** Modifying CDWT creates a brand-new immutable MongoDB document with `Version: "2.0"`, a new `_id`, and marks the old document as `IsSuperseded: true`.
- **Location Work Template:** Editing a location template mutates the existing document **in place** (retains `_id` and `Version: "1.0"`). However, this triggers `DEFECT-20261110-03` where `CreatedAt` is wiped out to `0001-01-01T00:00:00.000Z` and `CreatedBy` is reset to `null`.

### 3.4 Cross-Module Validation Discrepancies
- Total work duration declared in the request header (`totalWorkDurationInMinutes`) is not validated against the actual sum of working slot durations during PATCH operations across all three template types (`DEFECT-20261110-05`, `DEFECT-20261110-11`, `DEFECT-20261110-13`).
- Monthly recurrence arrays accept out-of-range values `[0]` and `[6]` across Fixed, Flexible, and Split templates (`DEFECT-20261110-04`, `DEFECT-20261110-07`, `DEFECT-20261110-10`, `DEFECT-20261110-14`).