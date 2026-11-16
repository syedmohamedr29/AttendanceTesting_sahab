# -*- coding: utf-8 -*-
"""
Update Attendance2_Defects_Gaps_and_Architecture_Inconsistencies_Report.md with Part 3K
"""

with open('Attendance2_Defects_Gaps_and_Architecture_Inconsistencies_Report.md', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update Header Metadata (top lines)
old_meta = "**Report Last Updated:** **13 November 2026"
new_meta = "**Report Last Updated:** **14 November 2026 (Day 11 Update — Live Work Assignment & Employee Lifecycle Run on Attendance 11)** (Updated with `DEFECT-20261114-01` to `DEFECT-20261114-04` — Work Assignments & Employee Lifecycle Live Audit across `Attendance 11` `3a24e5e5-302e-91bd-feaa-b07979766dfe`, **203 Master Test Cases**, Critical Inactive Employee Orphaned Header Defect, Swagger `PATCH /remove` 404 Route Gap, and Missing LocationId Bypasses; previous 13-Nov update"

if old_meta in content:
    content = content.replace(old_meta, new_meta, 1)
    print("Updated header metadata.")
else:
    print("Warning: old_meta not found!")

# 2. Update Table of Contents
old_toc_marker = "* [**✅ Part 5: Actionable Developer Checklist (Date-Wise: Days 1 to 9)**"
new_toc_entry = """* [**🏢 Part 3K: Defects Identified on 14 November 2026 — Work Assignments & Employee Lifecycle Live Audit on Attendance 11: DEFECT-20261114-01 to 04**](#-part-3k-defects-identified-on-14-november-2026--work-assignments--employee-lifecycle-live-audit-on-attendance-11-defect-20261114-01-to-04) — *Critical Orphaned Header on Inactive Employee (`DEFECT-20261114-01`), Swagger Route Gap 404 on `PATCH /remove` (`DEFECT-20261114-02`), and Missing LocationId Scoping Bypasses on `/upcoming` & `/details` (`DEFECT-20261114-03` & `-04`)*
* [**✅ Part 5: Actionable Developer Checklist (Date-Wise: Days 1 to 9)**"""

if old_toc_marker in content:
    content = content.replace(old_toc_marker, new_toc_entry, 1)
    print("Updated Table of Contents.")
else:
    print("Warning: old_toc_marker not found!")

# 3. Create Part 3K Content
part_3k = """

---

### 🏢 Part 3K: Defects Identified on 14 November 2026 — Work Assignments & Employee Lifecycle Live Audit on Attendance 11 (`DEFECT-20261114-01` to `DEFECT-20261114-04`)

<a id="-part-3k-defects-identified-on-14-november-2026--work-assignments--employee-lifecycle-live-audit-on-attendance-11-defect-20261114-01-to-04"></a>

> **Target Company:** `Attendance 11` (`3a24e5e5-302e-91bd-feaa-b07979766dfe`)  
> **Gateways & Microservices:** `gw8.dev.zoolwork.com` (`SP.AttendanceSvc` .NET 9), `employee8.dev.zoolwork.com` (`SP.EmployeeSvc` .NET 8)  
> **Database Collections Inspected:** MongoDB `10.1.0.4:27018` — `Sahab.ERP.Attendance.WorkAssignments`, `Sahab.ERP.Attendance.WorkAssignmentMaps`, `EmployeeSvcNET8test.Employee`  
> **Test Suite Executed:** Master 203 Comprehensive Test Scenarios (13 Individual Endpoints, E2E Flows, Employee Lifecycles, and Date Boundaries)  
> **Execution Date:** 14 November 2026  

---

#### Defect `DEFECT-20261114-01`: Inactive Employee Assignment Commit Returns HTTP 200 OK & Inserts Orphaned Header in `ERP.Attendance.WorkAssignments` with Zero Detail Maps in `ERP.Attendance.WorkAssignmentMaps`

<a id="defect-20261114-01"></a>

- **Severity:** 🔴 **P0 Critical** (Data Integrity Breach, Orphaned Documents & Silent Failure)
- **Component:** Work Assignments (`POST /api/companies/{companyId}/workassignments`)
- **Microservices Involved:** `SP.AttendanceSvc` (.NET 9) & `SP.EmployeeSvc` (.NET 8)
- **Database Collections:** `Sahab.ERP.Attendance.WorkAssignments`, `Sahab.ERP.Attendance.WorkAssignmentMaps`
- **Environment:** DEV | Company: `Attendance 11` (`3a24e5e5-302e-91bd-feaa-b07979766dfe`) | Location: Dammam (`3a24e666-df63-3dc7-0ea7-02ec8be341e7`)

##### 1. Defect Summary & Root Cause
When an assignment creation request is made with an **inactive employee** (`IsActive: false`, `EmployeeStatus: 1`, `OnBoardingStatus: 2`, e.g., `SA-EMP-0006` `39879386-4c24-ee4c-84ec-6eb7daa765ac`), the API accepts the payload, returns `HTTP 200 OK: {"message":"Work assignment created"}` and inserts an assignment Header document in `ERP.Attendance.WorkAssignments` (`9dd98d95-9aef-47e6-b216-7d72a5674827`). However, the backend mapping service drops the inactive employee during map generation, resulting in **exactly 0 documents created in `ERP.Attendance.WorkAssignmentMaps`**.

This causes a severe database inconsistency:
1. The frontend displays a success message indicating the work assignment was created.
2. The Header exists in `ERP.Attendance.WorkAssignments` with an empty assignment scope.
3. The employee is never scheduled, receives zero attendance tracking records, and detail map queries return empty.

##### 2. Live Reproduction Steps & Proof
1. Inspect `SA-EMP-0006` in `EmployeeSvcNET8test.Employee`:
   * `EmployeeCode`: `"SA-EMP-0006"`
   * `_id`: `39879386-4c24-ee4c-84ec-6eb7daa765ac`
   * `IsActive`: `false`
   * `EmployeeStatus`: `1` (Draft / Pending)
2. Send `POST /api/companies/3a24e5e5-302e-91bd-feaa-b07979766dfe/workassignments?locationId=3a24e666-df63-3dc7-0ea7-02ec8be341e7`:
   ```json
   {
     "tenantName": {"en": "Attendance", "ar": "Attendance"},
     "workPlanId": "a1ae96cd-587b-4145-8859-3b42877ea4a5",
     "workPlanName": {"en": "Default Work Plan"},
     "employeeIds": ["39879386-4c24-ee4c-84ec-6eb7daa765ac"],
     "startDate": "2026-11-14",
     "endDate": null
   }
   ```
3. **Observed HTTP Response:**
   ```json
   HTTP/1.1 200 OK
   {
     "message": "Work assignment created",
     "workAssignment": {
       "id": "9dd98d95-9aef-47e6-b216-7d72a5674827",
       "tenantId": "3a24741e-2667-1223-f12e-62a69fab3838",
       "tenantName": {"en": "Attendance", "ar": "Attendance"},
       "companyId": "3a24e5e5-302e-91bd-feaa-b07979766dfe",
       "companyName": {"en": "Attendance 11", "ar": "الحضور 11"},
       "locationId": "3a24e666-df63-3dc7-0ea7-02ec8be341e7",
       "locationName": {"en": "Dammam", "ar": "الدمام"}
     }
   }
   ```
4. **MongoDB Verification Query:**
   ```javascript
   // Query Header
   db['ERP.Attendance.WorkAssignments'].find({ _id: UUID("9dd98d95-9aef-47e6-b216-7d72a5674827") })
   // Result: 1 document found (CreatedAt: 2026-11-14 05:12:08.486Z)

   // Query Detail Maps
   db['ERP.Attendance.WorkAssignmentMaps'].find({ WorkAssignmentId: UUID("9dd98d95-9aef-47e6-b216-7d72a5674827") })
   // Result: 0 documents found! (ORPHANED HEADER)
   ```
5. **Contrast with Active Employee:**
   * When `SA-EMP-0004` (activated via `PUT /api/Employees/activateemployees`, `IsActive: true`, `Status: 2`) was assigned, Header `49f5d505-5fed-4c67-a95b-9b00a26c56b0` AND Detail Map `9b04f05d-71ec-4e0b-94ba-090a60ee3437` were both successfully created.

##### 3. Expected Architecture & Fix
* `POST /workassignments` and `POST /workassignments/check-conflicts` must validate employee active status through `SP.EmployeeSvc` before committing any document.
* If any submitted employee has `IsActive: false` or `EmployeeStatus != 2`, the endpoint must reject the request with:
  ```json
  HTTP/1.1 400 Bad Request
  {
    "error": {
      "code": "Cit.Attendance:Validation",
      "message": "Inactive employees cannot be assigned to a work plan.",
      "data": { "inactiveEmployeeIds": ["39879386-4c24-ee4c-84ec-6eb7daa765ac"] }
    }
  }
  ```
* Transactions must ensure that a Header is never persisted without its corresponding Detail Maps.

---

#### Defect `DEFECT-20261114-02`: Documented Endpoint `PATCH /workassignments/details/{id}/remove` Returns HTTP 404 Not Found on Both Gateway and Direct Service

<a id="defect-20261114-02"></a>

- **Severity:** 🟠 **P1 Major** (API Contract Gap & Incomplete Microservice Implementation)
- **Component:** Work Assignments (`PATCH /api/companies/{companyId}/workassignments/details/{id}/remove`)
- **Target Microservice:** `SP.AttendanceSvc` (.NET 9)
- **Swagger Documentation Reference:** `https://attendance2.dev.zoolwork.com/swagger/index.html` — Tag `Work Assignments`
- **Summary in Swagger:** *"Remove employee from assignment — Removes one employee's assignment row from the work plan."*

##### 1. Defect Summary & Live Repro
The Swagger schema explicitly defines `PATCH /api/companies/{companyId}/workassignments/details/{id}/remove?locationId={locationId}` as the designated endpoint to soft-delete or remove an individual employee detail map.
However, calling this endpoint on an existing, active detail map returns **`HTTP 404 Not Found`** with an empty response body.

##### 2. Live Reproduction Steps
```bash
curl -X PATCH "https://gw8.dev.zoolwork.com/api/companies/3a24e5e5-302e-91bd-feaa-b07979766dfe/workassignments/details/9b04f05d-71ec-4e0b-94ba-090a60ee3437/remove?locationId=3a24e666-df63-3dc7-0ea7-02ec8be341e7" \\
  -H "Authorization: Bearer $TOKEN" \\
  -H "Accept: application/json"
```
* **Observed Result:** `HTTP/1.1 404 Not Found` (0 bytes returned).
* **Direct Microservice Verification:** Calling `https://attendance2.dev.zoolwork.com` directly also returns `404 Not Found`.

##### 3. Expected Architecture & Fix
Implement the controller action in `WorkAssignmentsController` corresponding to route `details/{id}/remove`:
1. Validate `id` exists in `ERP.Attendance.WorkAssignmentMaps`.
2. Soft-delete the map row by setting `IsActive: false`, recording `ModifiedAt: UtcNow` and deactivation timestamp.
3. Return `HTTP 200 OK: {"message": "Employee removed from work assignment successfully."}`.

---

#### Defect `DEFECT-20261114-03`: Missing Mandatory Query Parameter `locationId` on `GET /workassignments/upcoming` Returns HTTP 200 OK Instead of 400

<a id="defect-20261114-03"></a>

- **Severity:** 🟡 **P2 Medium** (API Contract Inconsistency & Missing Input Validation)
- **Component:** Work Assignments (`GET /api/companies/{companyId}/workassignments/upcoming`)
- **Target Microservice:** `SP.AttendanceSvc` (.NET 9)

##### 1. Defect Summary & Live Repro
In the OpenAPI/Swagger specification, `locationId` is marked as a required query parameter (`required: true`) for `GET /workassignments/upcoming`.
However, executing `GET /api/companies/{companyId}/workassignments/upcoming` without providing `locationId` returns `HTTP 200 OK` with payload:
```json
{"message":"No upcoming work assignments are found","upcomingWorkAssignments":[]}
```

##### 2. Expected Architecture & Fix
The controller action must validate that `locationId` is non-empty and non-default. If omitted, return `HTTP 400 Bad Request` (`Cit.Attendance:Validation` / `"Location ID is required."`).

---

#### Defect `DEFECT-20261114-04`: Missing Mandatory Query Parameter `locationId` on `GET /workassignments/details` Returns Records Across All Locations (`200 OK`) Bypassing Isolation

<a id="defect-20261114-04"></a>

- **Severity:** 🟡 **P2 Medium** (Location Isolation Bypass & Multi-Location Data Leak)
- **Component:** Work Assignments (`GET /api/companies/{companyId}/workassignments/details`)
- **Target Microservice:** `SP.AttendanceSvc` (.NET 9)

##### 1. Defect Summary & Live Repro
Calling `GET /api/companies/{companyId}/workassignments/details?state=Active` without `locationId` returns `HTTP 200 OK` and serializes detail assignment rows across **all locations** belonging to the company, completely bypassing location scoping and multi-branch tenancy boundaries.

##### 2. Expected Architecture & Fix
Enforce mandatory location filtering on the endpoint:
* Check `if (!locationId.HasValue || locationId == Guid.Empty) return BadRequest(...);`
* Reject un-scoped calls with `HTTP 400 Bad Request`.
"""

# Find insertion position: right before "## ✅ Part 5: Actionable Developer Checklist (Date-Wise)"
insert_marker = "## ✅ Part 5: Actionable Developer Checklist (Date-Wise)"
if insert_marker in content:
    content = content.replace(insert_marker, part_3k + "\n\n" + insert_marker, 1)
    print("Inserted Part 3K before Part 5.")
else:
    print("Warning: insert_marker not found!")

# 4. Add Day 11 Action Items to Developer Checklist
day11_checklist = """### 📅 Day 11: 14 November 2026 Checklist (Work Assignments & Employee Lifecycle Live Audit)

- [ ] **P0 (`DEFECT-20261114-01`):** In `POST /workassignments`, validate employee active status (`IsActive == true && EmployeeStatus == Active`) before creating Header. Reject inactive employees with `400 Bad Request` and prevent orphaned headers.
- [ ] **P1 (`DEFECT-20261114-02`):** Implement missing route `PATCH /api/companies/{companyId}/workassignments/details/{id}/remove` in `WorkAssignmentsController` to soft-remove employee detail map rows.
- [ ] **P2 (`DEFECT-20261114-03`):** Validate mandatory `locationId` query parameter on `GET /workassignments/upcoming`; return `400 Bad Request` when missing.
- [ ] **P2 (`DEFECT-20261114-04`):** Validate mandatory `locationId` query parameter on `GET /workassignments/details` to enforce strict location scoping and prevent multi-location data leaks.

"""

day1_marker = "### 📅 Day 1: 26 October 2026 Checklist"
if day1_marker in content:
    content = content.replace(day1_marker, day11_checklist + day1_marker, 1)
    print("Added Day 11 Checklist to Part 5.")
else:
    print("Warning: day1_marker not found!")

# Save file
with open('Attendance2_Defects_Gaps_and_Architecture_Inconsistencies_Report.md', 'w', encoding='utf-8') as f:
    f.write(content)

print("Saved updated Attendance2_Defects_Gaps_and_Architecture_Inconsistencies_Report.md successfully!")
