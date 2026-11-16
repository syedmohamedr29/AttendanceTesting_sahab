# Regular Work Plan — Business & Template Compatibility Validation Suite

> **Environments:** `https://gw8.dev.zoolwork.com` & `https://attendance2.dev.zoolwork.com` | **Database:** MongoDB `Sahab` (`10.1.0.4:27018`)  
> **Companies Validated:** `Attendance 8` (`3a249871-7a8d-dec5-2d72-47795dd2662d`) & `Attendance 10` (`3a249872-e23c-a401-7d8b-4a8049ac8c9b`)

---

## 1. Attendance 8 (`gw8.dev.zoolwork.com`) Template Compatibility Matrix (8 Cases: 5 Pass, 3 Fail)

| TC ID | Method | Endpoint / Scope | Expected | Actual HTTP | Result | MongoDB Verification Notes |
| :--- | :---: | :--- | :---: | :---: | :---: | :--- |
| `ATT8-BUS-FIXED` | `PATCH` | Regular WorkPlan + Fixed Template (`Type=1`) | `200` | `HTTP 200` | ✅ Pass | Fixed workTemplate compatibility; DB wt_type=1 |
| `ATT8-BUS-FLEXI` | `PATCH` | Regular WorkPlan + Flexible Template (`Type=2`) | `200` | `HTTP 200` | ✅ Pass | Flexible workTemplate compatibility; DB wt_type=2 |
| `ATT8-BUS-SPLIT` | `PATCH` | Regular WorkPlan + Split Template (`Type=3`) | `200` | `HTTP 200` | ✅ Pass | Split workTemplate compatibility; DB wt_type=3 |
| `ATT8-BUS-ROT` | `PATCH` | Regular WorkPlan + **Rotation Template (`Type=5`)** | `400` | `HTTP 200` | ❌ Fail | Incompatible Rotation template embedded! (DEFECT-20261112-09) |
| `ATT8-BUS-ROST` | `PATCH` | Regular WorkPlan + **Roster Template (`Type=4`)** | `400` | `HTTP 200` | ❌ Fail | Incompatible Roster template embedded! (DEFECT-20261112-09) |
| `ATT8-BUS-CROSSLOC` | `PATCH` | Regular WorkPlan + Cross-Location Template | `200` | `HTTP 200` | ✅ Pass | Cross-location template allowed within same company |
| `ATT8-BUS-CROSSCOMP` | `PATCH` | Regular WorkPlan + **Cross-Company Template (`ATT7`)** | `400` | `HTTP 200` | ❌ Fail | Cross-company template embedded! (DEFECT-20261112-09) |
| `ATT8-BUS-DELETED` | `PATCH` | Regular WorkPlan + Soft-Deleted Template | `400` | `HTTP 400` | ✅ Pass | Soft-deleted template rejected with Cit.Attendance:1101 |

---

## 2. Attendance 10 (`attendance2.dev.zoolwork.com`) Extreme QA Validation Suite (30 Cases: 7 Pass, 23 Fail)

> **Company:** `Attendance 10` (`3a249872-e23c-a401-7d8b-4a8049ac8c9b`) | **Location 3:** `3a24e595-8a71-425d-c232-c5204fe1c740`  
> **Target Host Plan:** `7a29bd21-5c3c-4f5c-ba2a-1928f703f035` | **Visual Proof:** [Evidence 72](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_72_workplan_overtime_disabled_with_overtime_policy_embedded.jpg) & [Evidence 73](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_73_attendance10_extreme_qa_validation_findings.png)

| TC ID | Section | Method | Test Invariant / Scope | Expected | Actual | Result | Live MongoDB State & Defect Ref |
| :--- | :--- | :---: | :--- | :---: | :---: | :---: | :--- |
| `ATT10-POS-01` | Positive Update | `PATCH` | Succeeded with expected HTTP 200 | `200` | `200` | ✅ Pass | Flags=[False, False, False], Pols=0, WT_Type=1 |
| `ATT10-POS-02` | Positive Template Swap | `PATCH` | Succeeded with expected HTTP 200 | `200` | `200` | ✅ Pass | Flags=[False, False, False], Pols=0, WT_Type=2 |
| `ATT10-POS-03` | Positive Policy Attach | `PATCH` | Succeeded with expected HTTP 200 | `200` | `200` | ✅ Pass | Flags=[False, True, False], Pols=1, WT_Type=1 |
| `ATT10-POS-04` | Positive Policy Detach | `PATCH` | Succeeded with expected HTTP 200 | `200` | `200` | ✅ Pass | Flags=[False, False, False], Pols=1, WT_Type=1 |
| `ATT10-POL-01` | Policy Invariant Bug | `PATCH` | API returned 200 OK! Missing backend validation. | `400` | `200` | ❌ Fail | Flags=[False, False, False], Pols=1, WT_Type=1 (`DEFECT-20261112-06`) |
| `ATT10-POL-02` | Policy Invariant Bug | `PATCH` | API returned 200 OK! Missing backend validation. | `400` | `200` | ❌ Fail | Flags=[False, True, False], Pols=1, WT_Type=1 (`DEFECT-20261112-06`) |
| `ATT10-POL-03` | Policy Invariant Bug | `PATCH` | API returned 200 OK! Missing backend validation. | `400` | `200` | ❌ Fail | Flags=[True, False, False], Pols=1, WT_Type=1 (`DEFECT-20261112-06`) |
| `ATT10-POL-04` | Policy Invariant Bug | `PATCH` | API returned 200 OK! Missing backend validation. | `400` | `200` | ❌ Fail | Flags=[False, False, True], Pols=1, WT_Type=1 (`DEFECT-20261112-06`) |
| `ATT10-POL-05` | Policy Invariant Bug | `PATCH` | API returned 200 OK! Missing backend validation. | `400` | `200` | ❌ Fail | Flags=[False, True, False], Pols=2, WT_Type=1 (`DEFECT-20261112-06`) |
| `ATT10-POL-06` | Policy Security Bug | `PATCH` | API returned 200 OK! Missing backend validation. | `400` | `200` | ❌ Fail | Flags=[True, False, False], Pols=1, WT_Type=1 (`DEFECT-20261112-06`) |
| `ATT10-WT-01` | Template Compatibility Bug | `PATCH` | API returned 200 OK! Missing backend validation. | `400` | `200` | ❌ Fail | Flags=[False, False, False], Pols=1, WT_Type=5 (`DEFECT-20261112-09`) |
| `ATT10-WT-02` | Template Compatibility Bug | `PATCH` | API returned 200 OK! Missing backend validation. | `400` | `200` | ❌ Fail | Flags=[False, False, False], Pols=1, WT_Type=4 (`DEFECT-20261112-09`) |
| `ATT10-WT-03` | Template Security Bug | `PATCH` | API returned 200 OK! Missing backend validation. | `400` | `200` | ❌ Fail | Flags=[False, False, False], Pols=1, WT_Type=1 (`DEFECT-20261112-09`) |
| `ATT10-WT-04` | Template Guard | `PATCH` | Properly rejected with HTTP 400. | `400` | `400` | ✅ Pass | Flags=[False, False, False], Pols=1, WT_Type=1 (`DEFECT-20261112-09`) |
| `ATT10-BVA-NAME-01` | Name BVA Negative | `PATCH` | API returned 200 OK! Missing backend validation. | `400` | `200` | ❌ Fail | Flags=[False, False, False], Pols=1, WT_Type=1 (`DEFECT-20261112-09`) |
| `ATT10-BVA-NAME-02` | Name BVA Negative | `PATCH` | API returned 200 OK! Missing backend validation. | `400` | `200` | ❌ Fail | Flags=[False, False, False], Pols=1, WT_Type=1 (`DEFECT-20261112-09`) |
| `ATT10-BVA-NAME-03` | Name BVA Negative | `PATCH` | API returned 200 OK! Missing backend validation. | `400` | `200` | ❌ Fail | Flags=[False, False, False], Pols=1, WT_Type=1 (`DEFECT-20261112-09`) |
| `ATT10-BVA-NAME-04` | Name Boundary Max | `PATCH` | API returned 200 OK! Missing backend validation. | `400` | `200` | ❌ Fail | Flags=[False, False, False], Pols=1, WT_Type=1 (`DEFECT-20261112-09`) |
| `ATT10-BVA-NAME-05` | Name Boundary Extreme | `PATCH` | API returned 200 OK! Missing backend validation. | `400` | `200` | ❌ Fail | Flags=[False, False, False], Pols=1, WT_Type=1 (`DEFECT-20261112-09`) |
| `ATT10-BVA-NAME-06` | Name Special Chars | `PATCH` | API returned 200 OK! Missing backend validation. | `400` | `200` | ❌ Fail | Flags=[False, False, False], Pols=1, WT_Type=1 (`DEFECT-20261112-09`) |
| `ATT10-BVA-DESC-01` | Description Quirk | `PATCH` | API returned 200 OK! Missing backend validation. | `400` | `200` | ❌ Fail | Flags=[False, False, False], Pols=1, WT_Type=1 (`DEFECT-20261112-09/10`) |
| `ATT10-BVA-DESC-02` | Description Stress | `PATCH` | API returned 200 OK! Missing backend validation. | `400` | `200` | ❌ Fail | Flags=[False, False, False], Pols=1, WT_Type=1 (`DEFECT-20261112-09/10`) |
| `ATT10-DTO-01` | DTO Parity Bug | `PATCH` | API returned 200 OK! Missing backend validation. | `400` | `200` | ❌ Fail | Flags=[False, False, False], Pols=1, WT_Type=1 (`DEFECT-20261112-07/09/13`) |
| `ATT10-DTO-02` | Data Type Boundary | `PATCH` | API returned 200 OK! Missing backend validation. | `400` | `200` | ❌ Fail | Flags=[False, False, False], Pols=1, WT_Type=1 (`DEFECT-20261112-07/09/13`) |
| `ATT10-DTO-03` | Security Bypass | `PATCH` | API returned 200 OK! Missing backend validation. | `400` | `200` | ❌ Fail | Flags=[False, False, False], Pols=1, WT_Type=1 (`DEFECT-20261112-07/09/13`) |
| `ATT10-GET-01` | GET By ID | `GET` | Succeeded with expected HTTP 200 | `200` | `200` | ✅ Pass | Flags=[False, False, False], Pols=1, WT_Type=1 |
| `ATT10-GET-02` | GET By Nonexistent ID | `GET` | Properly rejected with HTTP 404. | `404` | `404` | ✅ Pass | Flags=[False, False, False], Pols=1, WT_Type=1 |
| `ATT10-GET-03` | GET Employees Valid | `GET` | Expected 200 but got 404: {'error': {'code': 'Cit.Sbp:NotFou | `200` | `404` | ❌ Fail | Flags=[False, False, False], Pols=1, WT_Type=1 |
| `ATT10-GET-04` | GET Employees Boundary | `GET` | Unexpected HTTP 404 (Expected 400): {'error': {'code': 'Cit. | `400` | `404` | ❌ Fail | Flags=[False, False, False], Pols=1, WT_Type=1 |
| `ATT10-GET-05` | GET Inverted State Filter | `GET` | state=active returned 1 deleted plans! | `200` | `200` | ❌ Fail | Flags=[False, False, False], Pols=1, WT_Type=1 (`DEFECT-20261112-03`) |