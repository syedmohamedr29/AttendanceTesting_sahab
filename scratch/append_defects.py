# -*- coding: utf-8 -*-
with open('Defects/Attendance2_Master_Defect_Log.md', 'r', encoding='utf-8') as f:
    text = f.read()

defect_entry = """

---

# PART IX: WORK ASSIGNMENT & EMPLOYEE LIFECYCLE DEFECTS (LIVE ATTENDANCE 11 RUN)

## Defect 59: CRITICAL — Inactive Employee Assignment Commit returns HTTP 200 OK and Generates Orphaned Header in MongoDB with 0 Detail Maps

- **Defect ID:** `DEFECT-WA-01` / `BUG-WA-03`
- **Severity:** High / Data Integrity
- **Component:** Work Assignments (`POST /api/companies/{companyId}/workassignments`)
- **Microservices Involved:** `AttendanceSvcNET8test` (Gateway: `gw8.dev.zoolwork.com`), `EmployeeSvcNET8test`
- **Environment:** DEV | Company: `Attendance 11` (`3a24e5e5-302e-91bd-feaa-b07979766dfe`)
- **Database Collections:** `Sahab.ERP.Attendance.WorkAssignments`, `Sahab.ERP.Attendance.WorkAssignmentMaps`

### 1. Description & Defect Overview
When a client submits an inactive employee (`IsActive: false`, `EmployeeStatus: 1`, e.g., `SA-EMP-0006`) to `POST /api/companies/{companyId}/workassignments?locationId={locationId}`, the microservice responds with `HTTP 200 OK: {"message":"Work assignment created"}`. It physically inserts a Header document in `ERP.Attendance.WorkAssignments` (`9dd98d95-9aef-47e6-b216-7d72a5674827`), but silently fails to create any corresponding employee mapping document in `ERP.Attendance.WorkAssignmentMaps`.

### 2. Live Reproduction Steps
1. Identify inactive employee in MongoDB (`SA-EMP-0006` `39879386-4c24-ee4c-84ec-6eb7daa765ac`, `IsActive: false`).
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
3. Observe HTTP Response: Returns `HTTP 200 OK: {"message":"Work assignment created","workAssignment":{"id":"9dd98d95-9aef-47e6-b216-7d72a5674827"}}`.
4. Inspect MongoDB:
   - `ERP.Attendance.WorkAssignments`: Header `9dd98d95...` exists.
   - `ERP.Attendance.WorkAssignmentMaps`: Exactly `0` documents exist for Header `9dd98d95...` or `SA-EMP-0006`.

### 3. Business Impact & Root Cause
- **Impact:** Frontend displays a success message, but the employee is never actually assigned. Orphaned headers pollute the database.
- **Root Cause:** Backend creation pipeline validates the work plan and inserts the Header *before* validating the active status of employees in `EmployeeSvc`. The detail map generator then skips inactive employees, leaving the header orphaned.
- **Expected Behavior:** The endpoint must validate employee active status *first*, rejecting the entire request with `HTTP 400 Bad Request` (`Cit.Attendance:Validation` / Inactive employee cannot be assigned).

---

## Defect 60: Swagger Route Gap — `PATCH /workassignments/details/{id}/remove` Returns HTTP 404 Not Found

- **Defect ID:** `DEFECT-WA-02` / `BUG-WA-04`
- **Severity:** Medium
- **Component:** Work Assignments (`PATCH /api/companies/{companyId}/workassignments/details/{id}/remove`)
- **Route:** `PATCH /api/companies/{companyId}/workassignments/details/{id}/remove?locationId={locationId}`
- **Observed:** Returns `HTTP 404 Not Found` with empty response body.
- **Expected:** Endpoint documented in Swagger specification to deactivate assignment row. Must execute and return `HTTP 200 OK`.

---

## Defect 61: Missing Location Query Enforcement on `GET /workassignments/upcoming` and `GET /workassignments/details`

- **Defect ID:** `DEFECT-WA-03` / `BUG-WA-01` & `BUG-WA-02`
- **Severity:** Low / Scoping Bypasses
- **Endpoints:** `GET /workassignments/upcoming` and `GET /workassignments/details`
- **Observed:** Omitting mandatory query parameter `locationId` does not return `HTTP 400 Bad Request`. On `/upcoming`, it returns `200 OK` with an empty array; on `/details`, it returns records across all locations.
- **Expected:** Return `HTTP 400 Bad Request` with validation error indicating `locationId` is required.
"""

with open('Defects/Attendance2_Master_Defect_Log.md', 'a', encoding='utf-8') as f:
    f.write(defect_entry)

print("Appended Defects 59-61 to Defects/Attendance2_Master_Defect_Log.md")
