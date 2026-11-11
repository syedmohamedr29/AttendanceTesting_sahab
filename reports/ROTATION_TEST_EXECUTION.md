# Sahab ERP Attendance – Rotation Work Template Master Test Execution Matrix

**Document Version:** `1.0` | **Execution Date:** `2026-11-10`

**Target Company:** `Attendance 8 (3a249871-7a8d-dec5-2d72-47795dd2662d)`

**Visual Evidence:** [Evidence 58 (Rotation Lifecycle & Defects)](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_58_rotation_worktemplate_lifecycle_and_defects.png)

## 1. High-Level Metrics Summary Table

| Category | Total | Passed | Failed | Blocked | Pass Rate | Key Architectural Finding |
| :--- | :---: | :---: | :---: | :---: | :---: | :--- |
| **Positive POST (`ROT-P01` - `ROT-P13`)** | 13 | 13 | 0 | 0 | 100.0% | LocationId required; 24h day duration capped at 23h59m |
| **Positive PATCH (`ROT-U01` - `ROT-U10`)** | 10 | 10 | 0 | 0 | 100.0% | In-place update succeeds; CreatedAt audit trail preserved |
| **Negative Tests (`ROT-N01` - `ROT-N45`)** | 44 | 40 | 4 | 0 | 90.9% | Caught cross-company location leak & empty name bypass |
| **BVA / Boundary (`ROT-B01` - `ROT-B11`)** | 11 | 11 | 0 | 0 | 100.0% | 0 working days blocked; dayEnum boundaries enforced |
| **GRAND TOTAL** | **78** | **74** | **4** | **0** | **94.9%** | **5 New Rotation Defects Identified & Tracked** |

## 2. Complete Execution Breakdown (All 78 Tests)

| Test ID | Method | Endpoint & Query | Expected | Actual | Result | Error Code | Key Observations |
| :--- | :---: | :--- | :---: | :---: | :---: | :--- | :--- |
| `ROT-P01` | `POST` | `/companies/3a249871-7a8d-dec5-2d72-47795dd2662d/worktemplates/rotation?locationId=3a24d667-0dcc-e3d1-74a3-cbee98168772` | `200` | `200` | ✅ PASS | `-` | Valid 5 working days, 2 days off |
| `ROT-P02` | `POST` | `/companies/3a249871-7a8d-dec5-2d72-47795dd2662d/worktemplates/rotation?locationId=3a24d667-0dcc-e3d1-74a3-cbee98168772` | `200` | `200` | ✅ PASS | `-` | Valid 6 working days, 1 off day |
| `ROT-P03` | `POST` | `/companies/3a249871-7a8d-dec5-2d72-47795dd2662d/worktemplates/rotation?locationId=3a24d667-0dcc-e3d1-74a3-cbee98168772` | `200` | `200` | ✅ PASS | `-` | Valid 4 working days, 3 off days |
| `ROT-P04` | `POST` | `/companies/3a249871-7a8d-dec5-2d72-47795dd2662d/worktemplates/rotation?locationId=3a24d667-0dcc-e3d1-74a3-cbee98168772` | `[200, 400]` | `200` | ✅ PASS | `-` | Valid 7 working days if supported |
| `ROT-P05` | `POST` | `/companies/3a249871-7a8d-dec5-2d72-47795dd2662d/worktemplates/rotation?locationId=3a24d667-0dcc-e3d1-74a3-cbee98168772` | `[200, 400]` | `200` | ✅ PASS | `-` | Valid 1 working day if supported |
| `ROT-P06` | `POST` | `/companies/3a249871-7a8d-dec5-2d72-47795dd2662d/worktemplates/rotation?locationId=3a24d667-0dcc-e3d1-74a3-cbee98168772` | `200` | `200` | ✅ PASS | `-` | Different working hours by day |
| `ROT-P07` | `POST` | `/companies/3a249871-7a8d-dec5-2d72-47795dd2662d/worktemplates/rotation?locationId=3a24d667-0dcc-e3d1-74a3-cbee98168772` | `200` | `200` | ✅ PASS | `-` | Arabic and English names |
| `ROT-P08` | `POST` | `/companies/3a249871-7a8d-dec5-2d72-47795dd2662d/worktemplates/rotation` | `[200, 400]` | `400` | ✅ PASS | `Cit.Attendance:Validation` | Company-level Rotation template without locationId |
| `ROT-P09` | `POST` | `/companies/3a249871-7a8d-dec5-2d72-47795dd2662d/worktemplates/rotation?locationId=3a24d667-0dcc-e3d1-74a3-cbee98168772` | `200` | `200` | ✅ PASS | `-` | Unique short code |
| `ROT-P10` | `POST` | `/companies/3a249871-7a8d-dec5-2d72-47795dd2662d/worktemplates/rotation?locationId=3a24d667-0dcc-e3d1-74a3-cbee98168772` | `200` | `200` | ✅ PASS | `-` | Valid recurrence combinations |
| `ROT-P11` | `POST` | `/companies/3a249871-7a8d-dec5-2d72-47795dd2662d/worktemplates/rotation?locationId=3a24d667-0dcc-e3d1-74a3-cbee98168772` | `[200, 400]` | `200` | ✅ PASS | `-` | Valid minimum duration |
| `ROT-P12` | `POST` | `/companies/3a249871-7a8d-dec5-2d72-47795dd2662d/worktemplates/rotation?locationId=3a24d667-0dcc-e3d1-74a3-cbee98168772` | `[200, 400]` | `400` | ✅ PASS | `Cit.Attendance:Validation` | Valid maximum duration boundary |
| `ROT-P13` | `POST` | `/companies/3a249871-7a8d-dec5-2d72-47795dd2662d/worktemplates/rotation?locationId=3a24d667-0dcc-e3d1-74a3-cbee98168772` | `[200, 400]` | `200` | ✅ PASS | `-` | Overnight shift (end earlier than start) |
| `ROT-U01` | `PATCH` | `/companies/3a249871-7a8d-dec5-2d72-47795dd2662d/worktemplates/rotation/e2b22c5f-8d8b-461c-93c7-6556ca86f5fc?locationId=3a24d667-0dcc-e3d1-74a3-cbee98168772` | `200` | `200` | ✅ PASS | `-` | Update template name |
| `ROT-U02` | `PATCH` | `/companies/3a249871-7a8d-dec5-2d72-47795dd2662d/worktemplates/rotation/e2b22c5f-8d8b-461c-93c7-6556ca86f5fc?locationId=3a24d667-0dcc-e3d1-74a3-cbee98168772` | `200` | `200` | ✅ PASS | `-` | Update daily hours |
| `ROT-U03` | `PATCH` | `/companies/3a249871-7a8d-dec5-2d72-47795dd2662d/worktemplates/rotation/e2b22c5f-8d8b-461c-93c7-6556ca86f5fc?locationId=3a24d667-0dcc-e3d1-74a3-cbee98168772` | `200` | `200` | ✅ PASS | `-` | Change working days |
| `ROT-U04` | `PATCH` | `/companies/3a249871-7a8d-dec5-2d72-47795dd2662d/worktemplates/rotation/e2b22c5f-8d8b-461c-93c7-6556ca86f5fc?locationId=3a24d667-0dcc-e3d1-74a3-cbee98168772` | `200` | `200` | ✅ PASS | `-` | Change day-off pattern |
| `ROT-U05` | `PATCH` | `/companies/3a249871-7a8d-dec5-2d72-47795dd2662d/worktemplates/rotation/e2b22c5f-8d8b-461c-93c7-6556ca86f5fc?locationId=3a24d667-0dcc-e3d1-74a3-cbee98168772` | `200` | `200` | ✅ PASS | `-` | Update recurrence |
| `ROT-U06` | `PATCH` | `/companies/3a249871-7a8d-dec5-2d72-47795dd2662d/worktemplates/rotation/e2b22c5f-8d8b-461c-93c7-6556ca86f5fc?locationId=3a24d667-0dcc-e3d1-74a3-cbee98168772` | `200` | `200` | ✅ PASS | `-` | Update slot times |
| `ROT-U07` | `PATCH` | `/companies/3a249871-7a8d-dec5-2d72-47795dd2662d/worktemplates/rotation/e2b22c5f-8d8b-461c-93c7-6556ca86f5fc?locationId=3a24d667-0dcc-e3d1-74a3-cbee98168772` | `200` | `200` | ✅ PASS | `-` | Update localization |
| `ROT-U08` | `PATCH` | `/companies/3a249871-7a8d-dec5-2d72-47795dd2662d/worktemplates/rotation/e2b22c5f-8d8b-461c-93c7-6556ca86f5fc?locationId=3a24d667-0dcc-e3d1-74a3-cbee98168772` | `200` | `200` | ✅ PASS | `-` | Update all editable fields |
| `ROT-U09` | `PATCH` | `/companies/3a249871-7a8d-dec5-2d72-47795dd2662d/worktemplates/rotation/e2b22c5f-8d8b-461c-93c7-6556ca86f5fc?locationId=3a24d667-0dcc-e3d1-74a3-cbee98168772` | `200` | `200` | ✅ PASS | `-` | Update location-level Rotation template |
| `ROT-U10` | `PATCH` | `/companies/3a249871-7a8d-dec5-2d72-47795dd2662d/worktemplates/rotation/e2b22c5f-8d8b-461c-93c7-6556ca86f5fc?locationId=3a24d667-0dcc-e3d1-74a3-cbee98168772` | `200` | `200` | ✅ PASS | `-` | Repeat unchanged payload |
| `ROT-N01` | `POST` | `/companies/3a249871-7a8d-dec5-2d72-47795dd2662d/worktemplates/rotation?locationId=3a24d667-0dcc-e3d1-74a3-cbee98168772` | `400` | `400` | ✅ PASS | `Cit.Attendance:1106` | Duplicate short code |
| `ROT-N02` | `POST` | `/companies/3a249871-7a8d-dec5-2d72-47795dd2662d/worktemplates/rotation?locationId=3a24d667-0dcc-e3d1-74a3-cbee98168772` | `[200, 400]` | `200` | ✅ PASS | `-` | Duplicate template name check |
| `ROT-N03` | `POST` | `/companies/3a249871-7a8d-dec5-2d72-47795dd2662d/worktemplates/rotation?locationId=3a24d667-0dcc-e3d1-74a3-cbee98168772` | `400` | `200` | ❌ FAIL | `-` | Empty template name |
| `ROT-N04` | `POST` | `/companies/3a249871-7a8d-dec5-2d72-47795dd2662d/worktemplates/rotation?locationId=3a24d667-0dcc-e3d1-74a3-cbee98168772` | `400` | `400` | ✅ PASS | `-` | Null template name |
| `ROT-N05` | `POST` | `/companies/3a249871-7a8d-dec5-2d72-47795dd2662d/worktemplates/rotation?locationId=3a24d667-0dcc-e3d1-74a3-cbee98168772` | `400` | `400` | ✅ PASS | `Cit.Attendance:Validation` | Missing short code |
| `ROT-N06` | `POST` | `/companies/3a249871-7a8d-dec5-2d72-47795dd2662d/worktemplates/rotation?locationId=3a24d667-0dcc-e3d1-74a3-cbee98168772` | `400` | `400` | ✅ PASS | `Cit.Attendance:Validation` | Empty short code |
| `ROT-N07` | `POST` | `/companies/3a249871-7a8d-dec5-2d72-47795dd2662d/worktemplates/rotation?locationId=3a24d667-0dcc-e3d1-74a3-cbee98168772` | `400` | `200` | ❌ FAIL | `-` | Invalid template type Fixed |
| `ROT-N08` | `POST` | `/companies/3a249871-7a8d-dec5-2d72-47795dd2662d/worktemplates/rotation?locationId=3a24d667-0dcc-e3d1-74a3-cbee98168772` | `400` | `400` | ✅ PASS | `Cit.Attendance:1203` | NotApplicable template type |
| `ROT-N09` | `POST` | `/companies/3a249871-7a8d-dec5-2d72-47795dd2662d/worktemplates/rotation?locationId=3a24d667-0dcc-e3d1-74a3-cbee98168772` | `400` | `400` | ✅ PASS | `-` | Invalid weekday enum InvalidDay |
| `ROT-N10` | `POST` | `/companies/3a249871-7a8d-dec5-2d72-47795dd2662d/worktemplates/rotation?locationId=3a24d667-0dcc-e3d1-74a3-cbee98168772` | `400` | `400` | ✅ PASS | `Cit.Attendance:Validation` | Duplicate weekday Mon |
| `ROT-N11` | `POST` | `/companies/3a249871-7a8d-dec5-2d72-47795dd2662d/worktemplates/rotation?locationId=3a24d667-0dcc-e3d1-74a3-cbee98168772` | `400` | `400` | ✅ PASS | `Cit.Attendance:2032` | Missing weekday (6 rows) |
| `ROT-N12` | `POST` | `/companies/3a249871-7a8d-dec5-2d72-47795dd2662d/worktemplates/rotation?locationId=3a24d667-0dcc-e3d1-74a3-cbee98168772` | `400` | `400` | ✅ PASS | `Cit.Attendance:Validation` | Extra weekday (8 rows) |
| `ROT-N13` | `POST` | `/companies/3a249871-7a8d-dec5-2d72-47795dd2662d/worktemplates/rotation?locationId=3a24d667-0dcc-e3d1-74a3-cbee98168772` | `400` | `400` | ✅ PASS | `Cit.Attendance:Validation` | Empty rotationTimeSlots |
| `ROT-N14` | `POST` | `/companies/3a249871-7a8d-dec5-2d72-47795dd2662d/worktemplates/rotation?locationId=3a24d667-0dcc-e3d1-74a3-cbee98168772` | `400` | `400` | ✅ PASS | `-` | Null rotationTimeSlots |
| `ROT-N15` | `POST` | `/companies/3a249871-7a8d-dec5-2d72-47795dd2662d/worktemplates/rotation?locationId=3a24d667-0dcc-e3d1-74a3-cbee98168772` | `400` | `400` | ✅ PASS | `Cit.Attendance:Validation` | Negative duration -1 |
| `ROT-N16` | `POST` | `/companies/3a249871-7a8d-dec5-2d72-47795dd2662d/worktemplates/rotation?locationId=3a24d667-0dcc-e3d1-74a3-cbee98168772` | `[200, 400]` | `400` | ✅ PASS | `Cit.Attendance:1203` | Decimal duration 480.5 (double vs int) |
| `ROT-N17` | `POST` | `/companies/3a249871-7a8d-dec5-2d72-47795dd2662d/worktemplates/rotation?locationId=3a24d667-0dcc-e3d1-74a3-cbee98168772` | `400` | `400` | ✅ PASS | `Cit.Attendance:Validation` | Working day with zero duration |
| `ROT-N18` | `POST` | `/companies/3a249871-7a8d-dec5-2d72-47795dd2662d/worktemplates/rotation?locationId=3a24d667-0dcc-e3d1-74a3-cbee98168772` | `400` | `400` | ✅ PASS | `Cit.Attendance:1203` | Day off with non-zero duration |
| `ROT-N19` | `POST` | `/companies/3a249871-7a8d-dec5-2d72-47795dd2662d/worktemplates/rotation?locationId=3a24d667-0dcc-e3d1-74a3-cbee98168772` | `400` | `400` | ✅ PASS | `Cit.Attendance:1203` | Total duration mismatch (1500 vs 2400) |
| `ROT-N20` | `POST` | `/companies/3a249871-7a8d-dec5-2d72-47795dd2662d/worktemplates/rotation?locationId=3a24d667-0dcc-e3d1-74a3-cbee98168772` | `400` | `400` | ✅ PASS | `Cit.Attendance:1203` | Working day count mismatch (4 vs 5) |
| `ROT-N21` | `POST` | `/companies/3a249871-7a8d-dec5-2d72-47795dd2662d/worktemplates/rotation?locationId=3a24d667-0dcc-e3d1-74a3-cbee98168772` | `400` | `400` | ✅ PASS | `Cit.Attendance:1203` | Day off count mismatch (3 vs 2) |
| `ROT-N22` | `POST` | `/companies/3a249871-7a8d-dec5-2d72-47795dd2662d/worktemplates/rotation?locationId=3a24d667-0dcc-e3d1-74a3-cbee98168772` | `400` | `400` | ✅ PASS | `-` | Invalid start time 25:00:00 |
| `ROT-N23` | `POST` | `/companies/3a249871-7a8d-dec5-2d72-47795dd2662d/worktemplates/rotation?locationId=3a24d667-0dcc-e3d1-74a3-cbee98168772` | `400` | `400` | ✅ PASS | `-` | Invalid end time 99:00:00 |
| `ROT-N24` | `POST` | `/companies/3a249871-7a8d-dec5-2d72-47795dd2662d/worktemplates/rotation?locationId=3a24d667-0dcc-e3d1-74a3-cbee98168772` | `400` | `400` | ✅ PASS | `Cit.Attendance:Validation` | Start equals end with 480m duration |
| `ROT-N25` | `POST` | `/companies/3a249871-7a8d-dec5-2d72-47795dd2662d/worktemplates/rotation?locationId=3a24d667-0dcc-e3d1-74a3-cbee98168772` | `[200, 400]` | `400` | ✅ PASS | `Cit.Attendance:1203` | End earlier than start |
| `ROT-N26` | `POST` | `/companies/3a249871-7a8d-dec5-2d72-47795dd2662d/worktemplates/rotation?locationId=3a24d667-0dcc-e3d1-74a3-cbee98168772` | `400` | `400` | ✅ PASS | `Cit.Attendance:1203` | Slot duration exceeds time window |
| `ROT-N27` | `POST` | `/companies/3a249871-7a8d-dec5-2d72-47795dd2662d/worktemplates/rotation?locationId=3a24d667-0dcc-e3d1-74a3-cbee98168772` | `400` | `400` | ✅ PASS | `-` | Invalid recurrence Sixth |
| `ROT-N28` | `POST` | `/companies/3a249871-7a8d-dec5-2d72-47795dd2662d/worktemplates/rotation?locationId=3a24d667-0dcc-e3d1-74a3-cbee98168772` | `[200, 400]` | `400` | ✅ PASS | `Cit.Attendance:1203` | Duplicate recurrence First, First |
| `ROT-N29` | `POST` | `/companies/3a249871-7a8d-dec5-2d72-47795dd2662d/worktemplates/rotation?locationId=3a24d667-0dcc-e3d1-74a3-cbee98168772` | `400` | `400` | ✅ PASS | `-` | Invalid recurrence type string |
| `ROT-N30` | `POST` | `/companies/invalid-uuid/worktemplates/rotation?locationId=3a24d667-0dcc-e3d1-74a3-cbee98168772` | `404` | `404` | ✅ PASS | `-` | Invalid CompanyId route |
| `ROT-N31` | `POST` | `/companies/3a249871-7a8d-dec5-2d72-47795dd2662d/worktemplates/rotation?locationId=malformed-location-uuid` | `400` | `400` | ✅ PASS | `-` | Invalid LocationId query param |
| `ROT-N32` | `POST` | `/companies/3a249871-7a8d-dec5-2d72-47795dd2662d/worktemplates/rotation?locationId=3a234994-37b8-214a-d8a1-ff5d184f0e1e` | `[400, 404]` | `200` | ❌ FAIL | `-` | Company/location mismatch |
| `ROT-N33` | `POST` | `/companies/3a249871-7a8d-dec5-2d72-47795dd2662d/worktemplates/rotation?locationId=3a24d667-0dcc-e3d1-74a3-cbee98168772` | `400` | `400` | ✅ PASS | `Cit.Attendance:1203` | Duplicate request with same shortCode |
| `ROT-N34` | `PATCH` | `/companies/3a23498e-e546-b040-2dda-43eb267a42a7/worktemplates/rotation/e2b22c5f-8d8b-461c-93c7-6556ca86f5fc?locationId=3a24d667-0dcc-e3d1-74a3-cbee98168772` | `[400, 404]` | `400` | ✅ PASS | `Cit.Attendance:9001` | Wrong company on PATCH |
| `ROT-N35` | `PATCH` | `/companies/3a249871-7a8d-dec5-2d72-47795dd2662d/worktemplates/rotation/08ead061-cefc-474e-be2d-0f3871731e5b?locationId=3a24d667-0dcc-e3d1-74a3-cbee98168772` | `404` | `400` | ❌ FAIL | `Cit.Attendance:1101` | Nonexistent template ID on PATCH |
| `ROT-N36` | `PATCH` | `/companies/3a249871-7a8d-dec5-2d72-47795dd2662d/worktemplates/rotation/invalid-id-string?locationId=3a24d667-0dcc-e3d1-74a3-cbee98168772` | `404` | `404` | ✅ PASS | `-` | Invalid PATCH ID string |
| `ROT-N37` | `PATCH` | `/companies/3a249871-7a8d-dec5-2d72-47795dd2662d/worktemplates/rotation/e2b22c5f-8d8b-461c-93c7-6556ca86f5fc?locationId=3a24d667-0dcc-e3d1-74a3-cbee98168772` | `[200, 400]` | `400` | ✅ PASS | `Cit.Attendance:1107` | Attempt to modify immutable short code on PATCH |
| `ROT-N38` | `PATCH` | `/companies/3a249871-7a8d-dec5-2d72-47795dd2662d/worktemplates/rotation/e2b22c5f-8d8b-461c-93c7-6556ca86f5fc?locationId=3a24d667-0dcc-e3d1-74a3-cbee98168772` | `[200, 400]` | `200` | ✅ PASS | `-` | Change Rotation to Fixed on PATCH |
| `ROT-N39` | `PATCH` | `/companies/3a249871-7a8d-dec5-2d72-47795dd2662d/worktemplates/rotation/0ba519c8-c2e2-4bce-8a70-23b1616ed5f7?locationId=3a24d667-0dcc-e3d1-74a3-cbee98168772` | `[400, 404]` | `400` | ✅ PASS | `Cit.Attendance:9002` | Update Fixed template through Rotation endpoint |
| `ROT-N40` | `PATCH` | `/companies/3a249871-7a8d-dec5-2d72-47795dd2662d/worktemplates/rotation/7ecfbe95-8d3c-4612-a0cc-1454e9093a53?locationId=3a24d667-0dcc-e3d1-74a3-cbee98168772` | `[400, 404]` | `400` | ✅ PASS | `Cit.Attendance:9002` | Update Flexi template through Rotation endpoint |
| `ROT-N42` | `PATCH` | `/companies/3a23498e-e546-b040-2dda-43eb267a42a7/worktemplates/rotation/59dd499a-0f08-4ae0-8a20-05682614d27f?locationId=3a234994-37b8-214a-d8a1-ff5d184f0e1e` | `[400, 403, 404]` | `400` | ✅ PASS | `Cit.Attendance:1101` | Update non-editable template |
| `ROT-N43` | `POST` | `/companies/3a249871-7a8d-dec5-2d72-47795dd2662d/worktemplates/rotation?locationId=3a24d667-0dcc-e3d1-74a3-cbee98168772` | `401` | `401` | ✅ PASS | `-` | Missing bearer token |
| `ROT-N44` | `POST` | `/companies/00000000-0000-0000-0000-000000000000/worktemplates/rotation?locationId=3a24d667-0dcc-e3d1-74a3-cbee98168772` | `[400, 404]` | `400` | ✅ PASS | `Cit.Attendance:Validation` | Unauthorized/empty company |
| `ROT-N45` | `POST` | `/companies/3a249871-7a8d-dec5-2d72-47795dd2662d/worktemplates/rotation?locationId=3a24d667-0dcc-e3d1-74a3-cbee98168772` | `[200, 400]` | `400` | ✅ PASS | `Cit.Attendance:1203` | Unexpected extra DTO property |
| `ROT-B01` | `POST` | `/companies/3a249871-7a8d-dec5-2d72-47795dd2662d/worktemplates/rotation?locationId=3a24d667-0dcc-e3d1-74a3-cbee98168772` | `400` | `400` | ✅ PASS | `Cit.Attendance:1203` | RecurrenceOfMonth index [0] |
| `ROT-B02` | `POST` | `/companies/3a249871-7a8d-dec5-2d72-47795dd2662d/worktemplates/rotation?locationId=3a24d667-0dcc-e3d1-74a3-cbee98168772` | `400` | `400` | ✅ PASS | `Cit.Attendance:1203` | RecurrenceOfMonth index [6] |
| `ROT-B03` | `POST` | `/companies/3a249871-7a8d-dec5-2d72-47795dd2662d/worktemplates/rotation?locationId=3a24d667-0dcc-e3d1-74a3-cbee98168772` | `400` | `400` | ✅ PASS | `Cit.Attendance:2033` | DayEnum numeric 0 |
| `ROT-B04` | `POST` | `/companies/3a249871-7a8d-dec5-2d72-47795dd2662d/worktemplates/rotation?locationId=3a24d667-0dcc-e3d1-74a3-cbee98168772` | `400` | `400` | ✅ PASS | `Cit.Attendance:2032` | DayEnum numeric 8 |
| `ROT-B05` | `POST` | `/companies/3a249871-7a8d-dec5-2d72-47795dd2662d/worktemplates/rotation?locationId=3a24d667-0dcc-e3d1-74a3-cbee98168772` | `400` | `400` | ✅ PASS | `Cit.Attendance:Validation` | 0 duration on all working days |
| `ROT-B06` | `POST` | `/companies/3a249871-7a8d-dec5-2d72-47795dd2662d/worktemplates/rotation?locationId=3a24d667-0dcc-e3d1-74a3-cbee98168772` | `400` | `400` | ✅ PASS | `Cit.Attendance:Validation` | 1441m (>24h) daily duration |
| `ROT-B07` | `POST` | `/companies/3a249871-7a8d-dec5-2d72-47795dd2662d/worktemplates/rotation?locationId=3a24d667-0dcc-e3d1-74a3-cbee98168772` | `[200, 400]` | `400` | ✅ PASS | `Cit.Attendance:Validation` | Continuous 10,080m weekly duration |
| `ROT-B08` | `POST` | `/companies/3a249871-7a8d-dec5-2d72-47795dd2662d/worktemplates/rotation?locationId=3a24d667-0dcc-e3d1-74a3-cbee98168772` | `400` | `400` | ✅ PASS | `Cit.Attendance:1203` | TotalWorkingDays = 8 |
| `ROT-B09` | `POST` | `/companies/3a249871-7a8d-dec5-2d72-47795dd2662d/worktemplates/rotation?locationId=3a24d667-0dcc-e3d1-74a3-cbee98168772` | `400` | `400` | ✅ PASS | `Cit.Attendance:1203` | TotalDaysOff = -1 |
| `ROT-B10` | `POST` | `/companies/3a249871-7a8d-dec5-2d72-47795dd2662d/worktemplates/rotation?locationId=3a24d667-0dcc-e3d1-74a3-cbee98168772` | `400` | `400` | ✅ PASS | `Cit.Attendance:2034` | TotalDaysOff = 8 |
| `ROT-B11` | `POST` | `/companies/3a249871-7a8d-dec5-2d72-47795dd2662d/worktemplates/rotation?locationId=3a24d667-0dcc-e3d1-74a3-cbee98168772` | `400` | `400` | ✅ PASS | `Cit.Attendance:1203` | Int32 overflow duration |