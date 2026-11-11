# Sahab ERP Attendance – Rotation Work Template POST API Test Catalog

**Execution Date:** `2026-11-10` | **Endpoint:** `POST /api/companies/{companyId}/worktemplates/rotation?locationId={locationId}`

## 1. Positive POST Test Scenarios

| Test ID | Method | Endpoint & Query | Expected | Actual | Verdict | Error Code | Scenario Description |
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

## 2. Negative POST Test Scenarios

| Test ID | Method | Endpoint & Query | Expected | Actual | Verdict | Error Code | Scenario Description |
| :--- | :---: | :--- | :---: | :---: | :---: | :--- | :--- |
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
| `ROT-N43` | `POST` | `/companies/3a249871-7a8d-dec5-2d72-47795dd2662d/worktemplates/rotation?locationId=3a24d667-0dcc-e3d1-74a3-cbee98168772` | `401` | `401` | ✅ PASS | `-` | Missing bearer token |
| `ROT-N44` | `POST` | `/companies/00000000-0000-0000-0000-000000000000/worktemplates/rotation?locationId=3a24d667-0dcc-e3d1-74a3-cbee98168772` | `[400, 404]` | `400` | ✅ PASS | `Cit.Attendance:Validation` | Unauthorized/empty company |
| `ROT-N45` | `POST` | `/companies/3a249871-7a8d-dec5-2d72-47795dd2662d/worktemplates/rotation?locationId=3a24d667-0dcc-e3d1-74a3-cbee98168772` | `[200, 400]` | `400` | ✅ PASS | `Cit.Attendance:1203` | Unexpected extra DTO property |