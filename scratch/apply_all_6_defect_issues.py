import sys

sys.stdout.reconfigure(encoding='utf-8')

report_path = "Attendance2_Defects_Gaps_and_Architecture_Inconsistencies_Report.md"
master_path = "Defects/Attendance2_Master_Defect_Log.md"

# Define 6 defect issues for Report MD
defect_entries_report = """
#### Defect `DEFECT-20261110-04`: `PATCH /worktemplates/fixed/{id}` Validation Bypass — In-Place Location Update Accepts Out-of-Range Monthly Recurrence Index 6 (`recurrenceOfMonth: [6]`) with HTTP 200 OK

- **Severity:** 🟠 **P1 Critical** (Validation Bypass, In-Place Data Integrity Corruption & DTO Contract Asymmetry)
- **Module / Feature:** Module 2: Work Template & Location Cascade / Regular Shift In-Place PATCH Validation Lifecycle
- **Affected Endpoints:** `PATCH /api/companies/{companyId}/worktemplates/fixed/{id}?locationId={locationId}`
- **Target Collection:** `Sahab.ERP.Attendance.WorkTemplates`
- **Target Company:** Attendance 8 (`3a249871-7a8d-dec5-2d72-47795dd2662d`)
- **Target Location:** Location 1 (`3a24d629-0d56-a428-baa1-98493a77e614`)
- **Target Document Tested:** `c9e00652-eae5-429a-bef0-4d4ddf9e0a0f` (`FXL0101`)
- **Visual Evidence:** [Evidence 55 (Fixed Work Template Location PATCH Validation Bypasses & MongoDB Verification)](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_55_fixed_wt_location_patch_validation_bypasses_and_db_results.png)

##### 1. Problem Description & Direct Evidence Analysis
- Recurrence enum defines values `1` through `5` (First=1 to Fifth=5). There are only 5 possible recurrences of any weekday in a month.
- While POST rejects invalid recurrence entries, calling `PATCH /worktemplates/fixed/c9e00652-eae5-429a-bef0-4d4ddf9e0a0f?locationId=3a24d629-0d56-a428-baa1-98493a77e614` with `"recurrenceOfMonth": [6]` returned **HTTP 200 OK** and persisted `RecurrenceOfMonth: [6]` directly into MongoDB.

##### 2. Tested Payload & Response
```json
{
  "shortCode": "FXL0101",
  "templateType": 1,
  "fixedTimeSlots": [
    {
      "workDurationInMinutes": 540,
      "dayEnum": 1,
      "isWorkingDay": true,
      "recurrenceOfMonth": [6],
      "startTime": "08:00:00",
      "endTime": "17:00:00"
    }
  ]
}
```
* **Live Response:** `HTTP 200 OK` (Expected: `HTTP 400 Bad Request` with `Cit.Attendance:Validation`).
* **MongoDB Proof:** Document `c9e00652-eae5-429a-bef0-4d4ddf9e0a0f` persisted `RecurrenceOfMonth: [6]`.

##### 3. Developer Remediation (.NET 9 C#)
- In `UpdateFixedWorkTemplateValidator.cs`, add `.Must(r => r >= 1 && r <= 5)` for each recurrence index in `RecurrenceOfMonth`.

---

#### Defect `DEFECT-20261110-05`: `PATCH /worktemplates/fixed/{id}` Validation Bypass — In-Place Location Update Accepts Mismatched Total Work Duration (`totalWorkDurationInMinutes: 3000` vs `2700m` Slot Sum) with HTTP 200 OK

- **Severity:** 🟠 **P1 Critical** (Mathematical Invariant Failure, Validation Bypass & Data Integrity Corruption)
- **Module / Feature:** Module 2: Work Template & Location Cascade / Regular Shift In-Place PATCH Validation Lifecycle
- **Affected Endpoints:** `PATCH /api/companies/{companyId}/worktemplates/fixed/{id}?locationId={locationId}`
- **Target Collection:** `Sahab.ERP.Attendance.WorkTemplates`
- **Target Company:** Attendance 8 (`3a249871-7a8d-dec5-2d72-47795dd2662d`)
- **Target Location:** Location 1 (`3a24d629-0d56-a428-baa1-98493a77e614`)
- **Target Document Tested:** `c9e00652-eae5-429a-bef0-4d4ddf9e0a0f` (`FXL0101`)
- **Visual Evidence:** [Evidence 55 (Fixed Work Template Location PATCH Validation Bypasses & MongoDB Verification)](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_55_fixed_wt_location_patch_validation_bypasses_and_db_results.png)

##### 1. Problem Description & Direct Evidence Analysis
- The PATCH payload declared `"totalWorkDurationInMinutes": 3000`, while the schedule consisted of 5 working days $\times$ 540 min = 2,700 min.
- While POST strictly requires that declared total duration equals the sum of slot durations, PATCH returned **HTTP 200 OK** and silently overwrote MongoDB with corrupt totals (`TotalWorkDurationInMinutes: 3000.0`).

##### 2. Tested Payload & Response
```json
{
  "shortCode": "FXL0101",
  "templateType": 1,
  "totalWorkDurationInMinutes": 3000,
  "totalWorkingDays": 5,
  "totalDaysOff": 2,
  "fixedTimeSlots": [
    { "workDurationInMinutes": 540, "dayEnum": 1, "isWorkingDay": true, "recurrenceOfMonth": [1,2,3,4,5], "startTime": "08:00:00", "endTime": "17:00:00" },
    { "workDurationInMinutes": 540, "dayEnum": 2, "isWorkingDay": true, "recurrenceOfMonth": [1,2,3,4,5], "startTime": "08:00:00", "endTime": "17:00:00" },
    { "workDurationInMinutes": 540, "dayEnum": 3, "isWorkingDay": true, "recurrenceOfMonth": [1,2,3,4,5], "startTime": "08:00:00", "endTime": "17:00:00" },
    { "workDurationInMinutes": 540, "dayEnum": 4, "isWorkingDay": true, "recurrenceOfMonth": [1,2,3,4,5], "startTime": "08:00:00", "endTime": "17:00:00" },
    { "workDurationInMinutes": 540, "dayEnum": 5, "isWorkingDay": true, "recurrenceOfMonth": [1,2,3,4,5], "startTime": "08:00:00", "endTime": "17:00:00" },
    { "workDurationInMinutes": 0, "dayEnum": 6, "isWorkingDay": false, "recurrenceOfMonth": [], "startTime": "00:00:00", "endTime": "00:00:00" },
    { "workDurationInMinutes": 0, "dayEnum": 7, "isWorkingDay": false, "recurrenceOfMonth": [], "startTime": "00:00:00", "endTime": "00:00:00" }
  ]
}
```
* **Live Response:** `HTTP 200 OK` (Expected: `HTTP 400 Bad Request` with `Cit.Attendance:Validation`).
* **MongoDB Proof:** Document `c9e00652-eae5-429a-bef0-4d4ddf9e0a0f` persisted `TotalWorkDurationInMinutes: 3000.0` (mathematical sum is 2,700).

##### 3. Developer Remediation (.NET 9 C#)
- In `UpdateFixedWorkTemplateValidator.cs`, enforce:
  `RuleFor(x => x.TotalWorkDurationInMinutes).Equal(x => x.FixedTimeSlots.Where(s => s.IsWorkingDay).Sum(s => s.WorkDurationInMinutes)).WithMessage("Total work duration must match the sum of slot durations.");`

---

#### Defect `DEFECT-20261110-06`: `PATCH /worktemplates/fixed/{id}` Validation Bypass — In-Place Location Update Accepts Arbitrary / Invalid Timezone String (`"Invalid/Timezone"`) with HTTP 200 OK

- **Severity:** 🟠 **P1 Critical** (Validation Bypass, Shift Engine Evaluation Crash Risk & Unvalidated String Input)
- **Module / Feature:** Module 2: Work Template & Location Cascade / Regular Shift In-Place PATCH Validation Lifecycle
- **Affected Endpoints:** `PATCH /api/companies/{companyId}/worktemplates/fixed/{id}?locationId={locationId}`
- **Target Collection:** `Sahab.ERP.Attendance.WorkTemplates`
- **Target Company:** Attendance 8 (`3a249871-7a8d-dec5-2d72-47795dd2662d`)
- **Target Location:** Location 1 (`3a24d629-0d56-a428-baa1-98493a77e614`)
- **Target Document Tested:** `c9e00652-eae5-429a-bef0-4d4ddf9e0a0f` (`FXL0101`)
- **Visual Evidence:** [Evidence 55 (Fixed Work Template Location PATCH Validation Bypasses & MongoDB Verification)](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_55_fixed_wt_location_patch_validation_bypasses_and_db_results.png)

##### 1. Problem Description & Direct Evidence Analysis
- The PATCH payload passed `"timeZoneId": "Invalid/Timezone"`.
- The endpoint returned **HTTP 200 OK** without validating the string against the standard IANA / Windows timezone database, persisting an unresolvable timezone into MongoDB. When the punch evaluation engine attempts `TimeZoneInfo.FindSystemTimeZoneById("Invalid/Timezone")`, an unhandled `TimeZoneNotFoundException` will crash the calculation worker.

##### 2. Tested Payload & Response
```json
{
  "shortCode": "FXL0101",
  "templateType": 1,
  "timeZoneId": "Invalid/Timezone"
}
```
* **Live Response:** `HTTP 200 OK` (Expected: `HTTP 400 Bad Request` with `Cit.Attendance:Validation`).
* **MongoDB Proof:** Document `c9e00652-eae5-429a-bef0-4d4ddf9e0a0f` persisted `TimeZoneId: "Invalid/Timezone"`.

##### 3. Developer Remediation (.NET 9 C#)
- In `UpdateFixedWorkTemplateValidator.cs`, add:
  `RuleFor(x => x.TimeZoneId).Must(BeAValidTimeZone).WithMessage("Invalid timezone identifier.");`

---

#### Defect `DEFECT-20261110-07`: `POST /worktemplates/fixed` Boundary Validation Gap — Creation Endpoint Accepts Out-of-Range Recurrence Values `[0]` and `[6]` on Working Days with HTTP 200 OK

- **Severity:** 🟠 **P1 Critical** (Boundary Value Validation Failure, Calendar Invariant Breach & Corrupt Recurrence Persistence)
- **Module / Feature:** Module 2: Work Template Creation / Boundary Value Analysis Lifecycle
- **Affected Endpoints:** `POST /api/companies/{companyId}/worktemplates/fixed?locationId={locationId}`
- **Target Collection:** `Sahab.ERP.Attendance.WorkTemplates`
- **Target Company:** Attendance 8 (`3a249871-7a8d-dec5-2d72-47795dd2662d`)
- **Target Location:** Location 1 (`3a24d629-0d56-a428-baa1-98493a77e614`)
- **Documents Created in Mongo:** `9605711d-dc54-405c-a73b-e45a79cc22c9` (`BVBVA16`) and `6382798d-ed99-461d-a7df-c5add6896170` (`BVBVA17`)
- **Visual Evidence:** [Evidence 55 (Fixed Work Template Location PATCH Validation Bypasses & MongoDB Verification)](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_55_fixed_wt_location_patch_validation_bypasses_and_db_results.png)

##### 1. Problem Description & Direct Evidence Analysis
- In test case `BVA16`, `"recurrenceOfMonth": [0]` was submitted (0 is below the minimum recurrence of 1).
- In test case `BVA17`, `"recurrenceOfMonth": [6]` was submitted (6 is above the maximum recurrence of 5).
- Both requests succeeded with **HTTP 200 OK** and created full documents in MongoDB with corrupt recurrence arrays.

##### 2. Developer Remediation (.NET 9 C#)
- In `CreateFixedWorkTemplateValidator.cs`, add:
  `RuleForEach(x => x.FixedTimeSlots).ChildRules(slot => slot.RuleForEach(s => s.RecurrenceOfMonth).InclusiveBetween(1, 5));`

---

#### Defect `DEFECT-20261110-08`: `POST /worktemplates/fixed` Boundary Validation Gap — Creation Endpoint Accepts Impossible Continuous Work Duration of 10,080 Minutes (Full Week Continuous Working) with HTTP 200 OK

- **Severity:** 🟡 **P2 Major** (Domain Sanity Limit Failure, Extreme Boundary Acceptance & Labour Law Invariant Breach)
- **Module / Feature:** Module 2: Work Template Creation / Boundary Value Analysis Lifecycle
- **Affected Endpoints:** `POST /api/companies/{companyId}/worktemplates/fixed?locationId={locationId}`
- **Target Collection:** `Sahab.ERP.Attendance.WorkTemplates`
- **Target Document Created:** `40ac02d3-85f8-4f3e-afb9-813d421c186e` (`BVBVA26`)
- **Visual Evidence:** [Evidence 55 (Fixed Work Template Location PATCH Validation Bypasses & MongoDB Verification)](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_55_fixed_wt_location_patch_validation_bypasses_and_db_results.png)

##### 1. Problem Description & Direct Evidence Analysis
- In test case `BVA26`, `"totalWorkDurationInMinutes": 10080` (168 hours = 24 hours $\times$ 7 days nonstop) was passed.
- The POST endpoint returned **HTTP 200 OK** and persisted a template with 10,080 minutes into MongoDB without warning, violating statutory maximum weekly working hour regulations (Saudi Labour Law Art. 98 caps weekly hours at 48 hours / 2,880 minutes).

##### 2. Developer Remediation (.NET 9 C#)
- Enforce a configurable upper ceiling:
  `RuleFor(x => x.TotalWorkDurationInMinutes).LessThanOrEqualTo(3600).WithMessage("Total weekly work duration cannot exceed 60 hours (3,600 minutes).");`

---

#### Defect `DEFECT-20261110-09`: Location Work Template Hard Quota Enforced at 20 Templates with `Cit.Attendance:1203 Location maximum limit reached.` — Lack of Capacity Warning or Location Quota Management in API & UI

- **Severity:** 🟡 **P2 Major** (Architectural Quota Constraint, Lack of Quota Visibility & Silent Provisioning Failure)
- **Module / Feature:** Module 2: Work Template Creation / Location Template Quota Lifecycle
- **Affected Endpoints:** `POST /api/companies/{companyId}/worktemplates/fixed?locationId={locationId}`
- **Target Location:** Location 1 (`3a24d629-0d56-a428-baa1-98493a77e614`)
- **Visual Evidence:** [Evidence 55 (Fixed Work Template Location PATCH Validation Bypasses & MongoDB Verification)](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_55_fixed_wt_location_patch_validation_bypasses_and_db_results.png)

##### 1. Problem Description & Direct Evidence Analysis
- When Location 1 reached 20 work templates, attempting to create an additional valid template (`POST-P09`) was rejected with:
  `HTTP 400 Bad Request` | `{"error": {"code": "Cit.Attendance:1203", "message": "Location maximum limit reached."}}`
- Neither Swagger nor the Web UI indicates that a 20-template quota exists per location, nor is there a quota usage API endpoint to check capacity.

##### 2. Developer Remediation (.NET 9 C#)
- Expose location quota metadata in `GET /api/companies/{companyId}/worktemplates?locationId={locationId}` (e.g. `"quota": { "used": 20, "max": 20 }`).
- Surface a clear warning banner in Web UI when location approaches 20 templates.
"""

# Table rows for Report MD
table_rows_report = """| **`DEFECT-20261110-09`** | **🟡 P2 (Architectural Quota)** | **Work Template Module**<br>(Location Quota Management) | `ERP.Attendance.WorkTemplates`<br>(`POST /worktemplates/fixed`) | **Location Work Template Hard Quota Enforced at 20 Templates:** Creating 21st template is blocked with `Cit.Attendance:1203 Location maximum limit reached.` without UI warning or quota visibility. | ❌ **FAIL ([Evidence 55](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_55_fixed_wt_location_patch_validation_bypasses_and_db_results.png))** |
| **`DEFECT-20261110-08`** | **🟡 P2 (Sanity Guardrail)** | **Work Template Module**<br>(POST Boundary Validation) | `ERP.Attendance.WorkTemplates`<br>(`POST /worktemplates/fixed`) | **Continuous 10,080 Min Weekly Work Duration Accepted:** API accepts 168-hour nonstop continuous weekly duration without upper ceiling validation, violating labour law limits. | ❌ **FAIL ([Evidence 55](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_55_fixed_wt_location_patch_validation_bypasses_and_db_results.png))** |
| **`DEFECT-20261110-07`** | **🟠 P1 (Boundary Validation)** | **Work Template Module**<br>(POST Boundary Validation) | `ERP.Attendance.WorkTemplates`<br>(`POST /worktemplates/fixed`) | **POST Accepts Out-of-Range Recurrence Values `[0]` and `[6]`:** Working day slots accept recurrence index 0 and 6 with HTTP 200 OK, persisting invalid recurrence arrays into MongoDB. | ❌ **FAIL ([Evidence 55](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_55_fixed_wt_location_patch_validation_bypasses_and_db_results.png))** |
| **`DEFECT-20261110-06`** | **🟠 P1 (Validation Bypass)** | **Work Template Module**<br>(Fixed Work Template PATCH) | `ERP.Attendance.WorkTemplates`<br>(`PATCH /worktemplates/fixed/{id}`) | **PATCH Accepts Arbitrary Invalid Timezone String:** In-place location PATCH accepts `"timeZoneId": "Invalid/Timezone"` with HTTP 200 OK, risking server crash during punch reconciliation. | ❌ **FAIL ([Evidence 55](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_55_fixed_wt_location_patch_validation_bypasses_and_db_results.png))** |
| **`DEFECT-20261110-05`** | **🟠 P1 (Math Invariant)** | **Work Template Module**<br>(Fixed Work Template PATCH) | `ERP.Attendance.WorkTemplates`<br>(`PATCH /worktemplates/fixed/{id}`) | **PATCH Accepts Total Work Duration Mismatch (3000m vs 2700m):** In-place location PATCH does not validate declared total duration against slot sum, corrupting MongoDB totals. | ❌ **FAIL ([Evidence 55](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_55_fixed_wt_location_patch_validation_bypasses_and_db_results.png))** |
| **`DEFECT-20261110-04`** | **🟠 P1 (Validation Bypass)** | **Work Template Module**<br>(Fixed Work Template PATCH) | `ERP.Attendance.WorkTemplates`<br>(`PATCH /worktemplates/fixed/{id}`) | **PATCH Accepts Out-of-Range Recurrence Index 6 (`[6]`):** In-place location PATCH accepts recurrence index 6 with HTTP 200 OK, persisting invalid monthly recurrence into MongoDB. | ❌ **FAIL ([Evidence 55](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_55_fixed_wt_location_patch_validation_bypasses_and_db_results.png))** |
"""

# Table rows for Master Defect Log MD
table_rows_master = """| [`DEFECT-20261110-09`](#defect-20261110-09) | 🟡 P2 | Work Template / Quota Architecture | Location Work Template Hard Quota Enforced at 20 Templates: Creating 21st template blocked with `Cit.Attendance:1203 Location maximum limit reached.` without UI warning | ``POST /worktemplates/fixed`` | [Evidence 55](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_55_fixed_wt_location_patch_validation_bypasses_and_db_results.png) |
| [`DEFECT-20261110-08`](#defect-20261110-08) | 🟡 P2 | Work Template / Sanity Boundary | Impossible Continuous Work Duration Accepted: API accepts 10,080 minutes (168 hours/week nonstop) with HTTP 200 OK without sanity ceiling | ``POST /worktemplates/fixed`` | [Evidence 55](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_55_fixed_wt_location_patch_validation_bypasses_and_db_results.png) |
| [`DEFECT-20261110-07`](#defect-20261110-07) | 🟠 P1 | Work Template / Recurrence Boundary | POST Accepts Out-of-Range Recurrence Values `[0]` and `[6]`: Working day slots accept recurrence 0 and 6 with HTTP 200 OK, persisting into MongoDB | ``POST /worktemplates/fixed`` | [Evidence 55](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_55_fixed_wt_location_patch_validation_bypasses_and_db_results.png) |
| [`DEFECT-20261110-06`](#defect-20261110-06) | 🟠 P1 | Work Template / Timezone Integrity | PATCH Accepts Arbitrary Timezone String: In-place location PATCH accepts `"timeZoneId": "Invalid/Timezone"` with HTTP 200 OK, risking engine crash | ``PATCH /worktemplates/fixed/{id}`` | [Evidence 55](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_55_fixed_wt_location_patch_validation_bypasses_and_db_results.png) |
| [`DEFECT-20261110-05`](#defect-20261110-05) | 🟠 P1 | Work Template / Math Invariant | PATCH Accepts Total Duration Mismatch: In-place location PATCH accepts declared 3,000 min vs 2,700 min slot sum with HTTP 200 OK | ``PATCH /worktemplates/fixed/{id}`` | [Evidence 55](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_55_fixed_wt_location_patch_validation_bypasses_and_db_results.png) |
| [`DEFECT-20261110-04`](#defect-20261110-04) | 🟠 P1 | Work Template / Recurrence Integrity | PATCH Accepts Out-of-Range Recurrence Index 6: In-place location PATCH accepts recurrence `[6]` with HTTP 200 OK, persisting into MongoDB | ``PATCH /worktemplates/fixed/{id}`` | [Evidence 55](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_55_fixed_wt_location_patch_validation_bypasses_and_db_results.png) |
"""

# Detail section for Master Defect Log MD
defect_entries_master = """### <a id="defect-20261110-04"></a>🔴 DEFECT-20261110-04: `PATCH /worktemplates/fixed/{id}` Validation Bypass — In-Place Location Update Accepts Out-of-Range Monthly Recurrence Index 6 (`recurrenceOfMonth: [6]`) with HTTP 200 OK

| Field | Detail |
| :--- | :--- |
| **Defect ID** | `DEFECT-20261110-04` |
| **Severity** | 🟠 **P1 Critical** (Validation Bypass, In-Place Data Integrity Corruption & DTO Contract Asymmetry) |
| **Module / Sub-Feature** | Module 2: Work Template & Location Cascade / Regular Shift In-Place PATCH Validation Lifecycle |
| **API Endpoints** | `PATCH /api/companies/{companyId}/worktemplates/fixed/{id}?locationId={locationId}` |
| **Target Collection** | `Sahab.ERP.Attendance.WorkTemplates` |
| **Target Companies Verified** | Attendance 8 (`3a249871-7a8d-dec5-2d72-47795dd2662d`) |
| **Target Location Tested** | Location 1 (`3a24d629-0d56-a428-baa1-98493a77e614`) |
| **Target Document Verified** | `c9e00652-eae5-429a-bef0-4d4ddf9e0a0f` (`FXL0101`) |
| **Live Status** | ❌ **FAIL / OPEN (Verified via Automated Live API Execution & MongoDB Evidence 55)** |
| **Visual Evidence** | [Evidence 55 (Fixed Work Template Location PATCH Validation Bypasses)](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_55_fixed_wt_location_patch_validation_bypasses_and_db_results.png) |

#### 1. Problem Description & Direct Evidence Analysis
- Recurrence enum is 1 to 5 (First=1 .. Fifth=5).
- Calling `PATCH /worktemplates/fixed/c9e00652-eae5-429a-bef0-4d4ddf9e0a0f?locationId=3a24d629-0d56-a428-baa1-98493a77e614` with `"recurrenceOfMonth": [6]` returned **HTTP 200 OK** and persisted `RecurrenceOfMonth: [6]` into MongoDB.

---

### <a id="defect-20261110-05"></a>🔴 DEFECT-20261110-05: `PATCH /worktemplates/fixed/{id}` Validation Bypass — In-Place Location Update Accepts Mismatched Total Work Duration (`totalWorkDurationInMinutes: 3000` vs `2700m` Slot Sum) with HTTP 200 OK

| Field | Detail |
| :--- | :--- |
| **Defect ID** | `DEFECT-20261110-05` |
| **Severity** | 🟠 **P1 Critical** (Mathematical Invariant Failure, Validation Bypass & Data Integrity Corruption) |
| **Module / Sub-Feature** | Module 2: Work Template & Location Cascade / Regular Shift In-Place PATCH Validation Lifecycle |
| **API Endpoints** | `PATCH /api/companies/{companyId}/worktemplates/fixed/{id}?locationId={locationId}` |
| **Target Collection** | `Sahab.ERP.Attendance.WorkTemplates` |
| **Target Companies Verified** | Attendance 8 (`3a249871-7a8d-dec5-2d72-47795dd2662d`) |
| **Target Location Tested** | Location 1 (`3a24d629-0d56-a428-baa1-98493a77e614`) |
| **Target Document Verified** | `c9e00652-eae5-429a-bef0-4d4ddf9e0a0f` (`FXL0101`) |
| **Live Status** | ❌ **FAIL / OPEN (Verified via Automated Live API Execution & MongoDB Evidence 55)** |
| **Visual Evidence** | [Evidence 55 (Fixed Work Template Location PATCH Validation Bypasses)](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_55_fixed_wt_location_patch_validation_bypasses_and_db_results.png) |

#### 1. Problem Description & Direct Evidence Analysis
- The PATCH payload declared `"totalWorkDurationInMinutes": 3000`, while the schedule consisted of 5 working days $\times$ 540 min = 2,700 min.
- PATCH returned **HTTP 200 OK** without validating the sum, corrupting the document totals in MongoDB.

---

### <a id="defect-20261110-06"></a>🔴 DEFECT-20261110-06: `PATCH /worktemplates/fixed/{id}` Validation Bypass — In-Place Location Update Accepts Arbitrary / Invalid Timezone String (`"Invalid/Timezone"`) with HTTP 200 OK

| Field | Detail |
| :--- | :--- |
| **Defect ID** | `DEFECT-20261110-06` |
| **Severity** | 🟠 **P1 Critical** (Validation Bypass, Shift Engine Evaluation Crash Risk & Unvalidated String Input) |
| **Module / Sub-Feature** | Module 2: Work Template & Location Cascade / Regular Shift In-Place PATCH Validation Lifecycle |
| **API Endpoints** | `PATCH /api/companies/{companyId}/worktemplates/fixed/{id}?locationId={locationId}` |
| **Target Collection** | `Sahab.ERP.Attendance.WorkTemplates` |
| **Target Companies Verified** | Attendance 8 (`3a249871-7a8d-dec5-2d72-47795dd2662d`) |
| **Target Location Tested** | Location 1 (`3a24d629-0d56-a428-baa1-98493a77e614`) |
| **Target Document Verified** | `c9e00652-eae5-429a-bef0-4d4ddf9e0a0f` (`FXL0101`) |
| **Live Status** | ❌ **FAIL / OPEN (Verified via Automated Live API Execution & MongoDB Evidence 55)** |
| **Visual Evidence** | [Evidence 55 (Fixed Work Template Location PATCH Validation Bypasses)](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_55_fixed_wt_location_patch_validation_bypasses_and_db_results.png) |

#### 1. Problem Description & Direct Evidence Analysis
- Payload passed `"timeZoneId": "Invalid/Timezone"`.
- The endpoint returned **HTTP 200 OK** and persisted `"Invalid/Timezone"` directly into MongoDB, creating an unhandled exception risk in punch evaluation.

---

### <a id="defect-20261110-07"></a>🔴 DEFECT-20261110-07: `POST /worktemplates/fixed` Boundary Validation Gap — Creation Endpoint Accepts Out-of-Range Recurrence Values `[0]` and `[6]` on Working Days with HTTP 200 OK

| Field | Detail |
| :--- | :--- |
| **Defect ID** | `DEFECT-20261110-07` |
| **Severity** | 🟠 **P1 Critical** (Boundary Value Validation Failure, Calendar Invariant Breach & Corrupt Recurrence Persistence) |
| **Module / Sub-Feature** | Module 2: Work Template Creation / Boundary Value Analysis Lifecycle |
| **API Endpoints** | `POST /api/companies/{companyId}/worktemplates/fixed?locationId={locationId}` |
| **Target Collection** | `Sahab.ERP.Attendance.WorkTemplates` |
| **Target Companies Verified** | Attendance 8 (`3a249871-7a8d-dec5-2d72-47795dd2662d`) |
| **Target Location Tested** | Location 1 (`3a24d629-0d56-a428-baa1-98493a77e614`) |
| **Documents Created in Mongo** | `9605711d-dc54-405c-a73b-e45a79cc22c9` (`BVBVA16`) and `6382798d-ed99-461d-a7df-c5add6896170` (`BVBVA17`) |
| **Live Status** | ❌ **FAIL / OPEN (Verified via Automated Live API Execution & MongoDB Evidence 55)** |
| **Visual Evidence** | [Evidence 55 (Fixed Work Template Location PATCH Validation Bypasses)](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_55_fixed_wt_location_patch_validation_bypasses_and_db_results.png) |

#### 1. Problem Description & Direct Evidence Analysis
- In test case `BVA16`, `"recurrenceOfMonth": [0]` was submitted (0 is below minimum 1).
- In test case `BVA17`, `"recurrenceOfMonth": [6]` was submitted (6 is above maximum 5).
- Both requests succeeded with **HTTP 200 OK** and created full documents in MongoDB with corrupt recurrence arrays.

---

### <a id="defect-20261110-08"></a>🟡 DEFECT-20261110-08: `POST /worktemplates/fixed` Boundary Validation Gap — Creation Endpoint Accepts Impossible Continuous Work Duration of 10,080 Minutes (Full Week Continuous Working) with HTTP 200 OK

| Field | Detail |
| :--- | :--- |
| **Defect ID** | `DEFECT-20261110-08` |
| **Severity** | 🟡 **P2 Major** (Domain Sanity Limit Failure, Extreme Boundary Acceptance & Labour Law Invariant Breach) |
| **Module / Sub-Feature** | Module 2: Work Template Creation / Boundary Value Analysis Lifecycle |
| **API Endpoints** | `POST /api/companies/{companyId}/worktemplates/fixed?locationId={locationId}` |
| **Target Collection** | `Sahab.ERP.Attendance.WorkTemplates` |
| **Target Companies Verified** | Attendance 8 (`3a249871-7a8d-dec5-2d72-47795dd2662d`) |
| **Target Document Created** | `40ac02d3-85f8-4f3e-afb9-813d421c186e` (`BVBVA26`) |
| **Live Status** | ❌ **FAIL / OPEN (Verified via Automated Live API Execution & MongoDB Evidence 55)** |
| **Visual Evidence** | [Evidence 55 (Fixed Work Template Location PATCH Validation Bypasses)](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_55_fixed_wt_location_patch_validation_bypasses_and_db_results.png) |

#### 1. Problem Description & Direct Evidence Analysis
- In test case `BVA26`, `"totalWorkDurationInMinutes": 10080` (168 hours = 24 hours $\times$ 7 days nonstop) was passed.
- The POST endpoint returned **HTTP 200 OK** and persisted a template with 10,080 minutes into MongoDB without warning, violating statutory maximum weekly working hour regulations.

---

### <a id="defect-20261110-09"></a>🟡 DEFECT-20261110-09: Location Work Template Hard Quota Enforced at 20 Templates with `Cit.Attendance:1203 Location maximum limit reached.` — Lack of Capacity Warning or Location Quota Management in API & UI

| Field | Detail |
| :--- | :--- |
| **Defect ID** | `DEFECT-20261110-09` |
| **Severity** | 🟡 **P2 Major** (Architectural Quota Constraint, Lack of Quota Visibility & Silent Provisioning Failure) |
| **Module / Sub-Feature** | Module 2: Work Template Creation / Location Template Quota Lifecycle |
| **API Endpoints** | `POST /api/companies/{companyId}/worktemplates/fixed?locationId={locationId}` |
| **Target Collection** | `Sahab.ERP.Attendance.WorkTemplates` |
| **Target Location** | Location 1 (`3a24d629-0d56-a428-baa1-98493a77e614`) |
| **Live Status** | ❌ **FAIL / OPEN (Verified via Automated Live API Execution & MongoDB Evidence 55)** |
| **Visual Evidence** | [Evidence 55 (Fixed Work Template Location PATCH Validation Bypasses)](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_55_fixed_wt_location_patch_validation_bypasses_and_db_results.png) |

#### 1. Problem Description & Direct Evidence Analysis
- When Location 1 reached 20 work templates, attempting to create an additional valid template (`POST-P09`) was rejected with:
  `HTTP 400 Bad Request` | `{"error": {"code": "Cit.Attendance:1203", "message": "Location maximum limit reached."}}`
- Neither Swagger nor the Web UI indicates that a 20-template quota exists per location, nor is there a quota usage API endpoint to check capacity.
"""

# 1. Update Report MD
with open(report_path, "r", encoding="utf-8") as f:
    text_r = f.read()

# Replace DEFECT-20261110-04 table row with the full block of 6 table rows
old_row_r = '| **`DEFECT-20261110-04`** | **🟠 P1 (Validation Bypass)** | **Work Template Module**<br>(Fixed Work Template PATCH) | `ERP.Attendance.WorkTemplates`<br>(`PATCH /worktemplates/fixed/{id}`) | **Fixed Work Template PATCH Bypasses Validation:** In-place location PATCH accepts recurrence `[6]`, mismatched total duration `3000m` (vs 2700m sum), and invalid timezone `"Invalid/Timezone"` with HTTP 200 OK, corrupting schedule calculations. | ❌ **FAIL ([Evidence 55](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_55_fixed_wt_location_patch_validation_bypasses_and_db_results.png))** |\n'
if old_row_r in text_r:
    text_r = text_r.replace(old_row_r, table_rows_report)
    print("Report MD: Replaced DEFECT-20261110-04 row with 6 individual rows.")
elif '| **`DEFECT-20261110-03`**' in text_r and 'DEFECT-20261110-09' not in text_r:
    text_r = text_r.replace('| **`DEFECT-20261110-03`**', table_rows_report + '| **`DEFECT-20261110-03`**')
    print("Report MD: Inserted 6 table rows before DEFECT-20261110-03.")

# Replace detail section
old_detail_start = '#### Defect `DEFECT-20261110-04`:'
old_detail_end = '#### Defect `DEFECT-20261110-03`:'
if old_detail_start in text_r and old_detail_end in text_r:
    idx1 = text_r.find(old_detail_start)
    idx2 = text_r.find(old_detail_end)
    text_r = text_r[:idx1] + defect_entries_report.strip() + "\n\n---\n\n" + text_r[idx2:]
    print("Report MD: Replaced details with 6 individual defect sections.")

with open(report_path, "w", encoding="utf-8") as f:
    f.write(text_r)
print("Saved Report MD successfully.")

# 2. Update Master Defect Log MD
with open(master_path, "r", encoding="utf-8") as f:
    text_m = f.read()

old_row_m = '| [`DEFECT-20261110-04`](#defect-20261110-04) | 🟠 P1 | Work Template / Schedule Integrity | Fixed Work Template PATCH Validation Bypass: Accepts Recurrence Index 6 (`[6]`), Mismatched Total Duration (`3000m` vs `2700m`), and Invalid Timezone (`"Invalid/Timezone"`) with HTTP 200 OK | ``PATCH /worktemplates/fixed/{id}`` | [Evidence 55](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_55_fixed_wt_location_patch_validation_bypasses_and_db_results.png) |\n'
if old_row_m in text_m:
    text_m = text_m.replace(old_row_m, table_rows_master)
    print("Master Log: Replaced DEFECT-20261110-04 row with 6 individual rows.")
elif '| [`DEFECT-20261110-03`]' in text_m and 'DEFECT-20261110-09' not in text_m:
    text_m = text_m.replace('| [`DEFECT-20261110-03`]', table_rows_master + '| [`DEFECT-20261110-03`]')
    print("Master Log: Inserted 6 table rows before DEFECT-20261110-03.")

old_m_detail_start = '### <a id="defect-20261110-04"></a>'
old_m_detail_end = '### <a id="defect-20261110-03"></a>'
if old_m_detail_start in text_m and old_m_detail_end in text_m:
    idx1 = text_m.find(old_m_detail_start)
    idx2 = text_m.find(old_m_detail_end)
    text_m = text_m[:idx1] + defect_entries_master.strip() + "\n\n---\n\n" + text_m[idx2:]
    print("Master Log: Replaced details with 6 individual defect sections.")

with open(master_path, "w", encoding="utf-8") as f:
    f.write(text_m)
print("Saved Master Defect Log successfully.")
