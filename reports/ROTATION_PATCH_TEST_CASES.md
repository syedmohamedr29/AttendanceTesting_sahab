# Sahab ERP Attendance – Rotation Work Template PATCH API Test Catalog

**Execution Date:** `2026-11-10` | **Endpoint:** `PATCH /api/companies/{companyId}/worktemplates/rotation/{id}?locationId={locationId}`

## 1. Positive PATCH Test Scenarios

| Test ID | Method | Endpoint & Query | Expected | Actual | Verdict | Error Code | Scenario Description |
| :--- | :---: | :--- | :---: | :---: | :---: | :--- | :--- |
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

## 2. Negative PATCH Test Scenarios

| Test ID | Method | Endpoint & Query | Expected | Actual | Verdict | Error Code | Scenario Description |
| :--- | :---: | :--- | :---: | :---: | :---: | :--- | :--- |
| `ROT-N34` | `PATCH` | `/companies/3a23498e-e546-b040-2dda-43eb267a42a7/worktemplates/rotation/e2b22c5f-8d8b-461c-93c7-6556ca86f5fc?locationId=3a24d667-0dcc-e3d1-74a3-cbee98168772` | `[400, 404]` | `400` | ✅ PASS | `Cit.Attendance:9001` | Wrong company on PATCH |
| `ROT-N35` | `PATCH` | `/companies/3a249871-7a8d-dec5-2d72-47795dd2662d/worktemplates/rotation/08ead061-cefc-474e-be2d-0f3871731e5b?locationId=3a24d667-0dcc-e3d1-74a3-cbee98168772` | `404` | `400` | ❌ FAIL | `Cit.Attendance:1101` | Nonexistent template ID on PATCH |
| `ROT-N36` | `PATCH` | `/companies/3a249871-7a8d-dec5-2d72-47795dd2662d/worktemplates/rotation/invalid-id-string?locationId=3a24d667-0dcc-e3d1-74a3-cbee98168772` | `404` | `404` | ✅ PASS | `-` | Invalid PATCH ID string |
| `ROT-N37` | `PATCH` | `/companies/3a249871-7a8d-dec5-2d72-47795dd2662d/worktemplates/rotation/e2b22c5f-8d8b-461c-93c7-6556ca86f5fc?locationId=3a24d667-0dcc-e3d1-74a3-cbee98168772` | `[200, 400]` | `400` | ✅ PASS | `Cit.Attendance:1107` | Attempt to modify immutable short code on PATCH |
| `ROT-N38` | `PATCH` | `/companies/3a249871-7a8d-dec5-2d72-47795dd2662d/worktemplates/rotation/e2b22c5f-8d8b-461c-93c7-6556ca86f5fc?locationId=3a24d667-0dcc-e3d1-74a3-cbee98168772` | `[200, 400]` | `200` | ✅ PASS | `-` | Change Rotation to Fixed on PATCH |
| `ROT-N39` | `PATCH` | `/companies/3a249871-7a8d-dec5-2d72-47795dd2662d/worktemplates/rotation/0ba519c8-c2e2-4bce-8a70-23b1616ed5f7?locationId=3a24d667-0dcc-e3d1-74a3-cbee98168772` | `[400, 404]` | `400` | ✅ PASS | `Cit.Attendance:9002` | Update Fixed template through Rotation endpoint |
| `ROT-N40` | `PATCH` | `/companies/3a249871-7a8d-dec5-2d72-47795dd2662d/worktemplates/rotation/7ecfbe95-8d3c-4612-a0cc-1454e9093a53?locationId=3a24d667-0dcc-e3d1-74a3-cbee98168772` | `[400, 404]` | `400` | ✅ PASS | `Cit.Attendance:9002` | Update Flexi template through Rotation endpoint |
| `ROT-N42` | `PATCH` | `/companies/3a23498e-e546-b040-2dda-43eb267a42a7/worktemplates/rotation/59dd499a-0f08-4ae0-8a20-05682614d27f?locationId=3a234994-37b8-214a-d8a1-ff5d184f0e1e` | `[400, 403, 404]` | `400` | ✅ PASS | `Cit.Attendance:1101` | Update non-editable template |