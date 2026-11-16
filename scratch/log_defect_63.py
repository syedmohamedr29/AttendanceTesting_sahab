# -*- coding: utf-8 -*-
"""
Append Defect 63 / DEFECT-20261114-05: Cross-Location Assignment Allowed & Multi-Location Concurrent Schedules
"""

# 1. Update Defects/Attendance2_Master_Defect_Log.md
defect_63_log = """
---

## Defect 63: CRITICAL — Cross-Location Assignment Allowed & Multi-Location Concurrent Active Schedules Permitted (Location Integrity Breach)

- **Defect ID:** `DEFECT-WA-05` / `DEFECT-20261114-05`
- **Severity:** 🔴 **P0 Critical** (Business Invariant & Data Integrity Breach)
- **Component:** Work Assignments (`POST /api/companies/{companyId}/workassignments` & `POST /check-conflicts`)
- **Microservices Involved:** `SP.AttendanceSvc` (.NET 9), `SP.EmployeeSvc` (.NET 8)
- **Environment:** DEV | Company: `Attendance 11` (`3a24e5e5-302e-91bd-feaa-b07979766dfe`)
- **Database Collections:** `Sahab.ERP.Attendance.WorkAssignmentMaps`, `EmployeeSvcNET8test.Employee`

### 1. Description & Defect Overview
The system does not validate employee employment location during the work assignment process. 
1. An employee whose assigned work location in `SP.EmployeeSvc` is **Dammam** can be freely assigned to a work plan belonging to **Jeddah** (`POST /workassignments?locationId={Jeddah}`).
2. Worse, `POST /check-conflicts?locationId={Jeddah}` queries existing maps strictly filtered by `locationId == Jeddah`. It is completely blind to assignments in other locations, returning `hasConflicts: false, canProceed: true`.
3. Consequently, an employee can hold **two simultaneous, open-ended active work assignments across two different cities**, creating conflicting attendance evaluation schedules and corruption in timesheet processing.

### 2. Live Reproduction Steps & Proof on Attendance 11
1. **Employee Verification in EmployeeSvc:**
   - Employee `SA-EMP-0001` (`f9e1a6d5-6bd5-7d46-ae85-38b81dc80887`):
     `WorkInformation.WorkLocation._id`: `3a24e666-df63-3dc7-0ea7-02ec8be341e7` (**Dammam**).
2. **Existing Assignment in AttendanceSvc:**
   - Active open-ended assignment in **Dammam**: `StartDate: 2026-11-13`, `EndDate: null` / `9999-12-31`.
3. **Preflight Conflict Check on Jeddah:**
   - `POST /api/companies/3a24e5e5-302e-91bd-feaa-b07979766dfe/workassignments/check-conflicts?locationId=3a24e667-5941-8331-9a1f-d77aa73945b3` (Jeddah):
     ```json
     {
       "locationId": "3a24e667-5941-8331-9a1f-d77aa73945b3",
       "startDate": "2026-11-20",
       "endDate": null,
       "employeeIds": ["f9e1a6d5-6bd5-7d46-ae85-38b81dc80887"]
     }
     ```
   - **Observed Result:** Returns `HTTP 200 OK: {"message":"No conflicts detected","hasConflicts":false,"allowedEmployeeIds":["f9e1a6d5..."],"canProceed":true}`. (FAILS TO CHECK EMPLOYEE'S ACTUAL LOCATION).
4. **Commit Assignment to Jeddah:**
   - `POST /api/companies/3a24e5e5-302e-91bd-feaa-b07979766dfe/workassignments?locationId=3a24e667-5941-8331-9a1f-d77aa73945b3` (Jeddah) with plan `a7e0804a-d313-4410-9428-1781d480dd45`.
   - **Observed Result:** Returns `HTTP 200 OK: {"message":"Work assignment created","workAssignment":{"id":"959cbf80-1cc2-48ae-8eb3-ce0dbf440b4d"}}`.
5. **MongoDB Proof in `Sahab.ERP.Attendance.WorkAssignmentMaps`:**
   ```javascript
   db['ERP.Attendance.WorkAssignmentMaps'].find({ EmployeeCode: "SA-EMP-0001", IsActive: true })
   ```
   **Output:** Exactly **2 concurrent active open-ended maps**:
   * Map 1: `Location: Dammam`, `StartDate: 2026-11-13`, `EndDate: 9999-12-31`, `IsActive: true`.
   * Map 2: `Location: Jeddah`, `StartDate: 2026-11-20`, `EndDate: 9999-12-31`, `IsActive: true`.

### 3. Expected Behavior & Fix
1. In `POST /workassignments/check-conflicts` and `POST /workassignments`, the backend must fetch the employee's `WorkLocationId` from `SP.EmployeeSvc`. If `Employee.WorkLocationId != request.locationId`, reject with `HTTP 400 Bad Request` (`Cit.Attendance:Validation` / "Employee does not belong to the selected location").
2. Furthermore, conflict detection must search `ERP.Attendance.WorkAssignmentMaps` by `EmployeeId` across the **entire company (tenant)**, not strictly scoped to the single `locationId` query parameter, to prevent multi-location overlapping schedules.
"""

with open('Defects/Attendance2_Master_Defect_Log.md', 'a', encoding='utf-8') as f:
    f.write(defect_63_log)
print("Appended Defect 63 to Defects/Attendance2_Master_Defect_Log.md")

# 2. Update Attendance2_Defects_Gaps_and_Architecture_Inconsistencies_Report.md
with open('Attendance2_Defects_Gaps_and_Architecture_Inconsistencies_Report.md', 'r', encoding='utf-8') as f:
    rep = f.read()

defect_report_entry = """

---

#### Defect `DEFECT-20261114-05`: Cross-Location Assignment Allowed & Multi-Location Concurrent Active Work Assignment Maps Created (Location Isolation Failure)

<a id="defect-20261114-05"></a>

- **Severity:** 🔴 **P0 Critical** (Location Scoping Breach & Multi-Location Overlap Corruption)
- **Component:** Work Assignments (`POST /api/companies/{companyId}/workassignments` & `POST /check-conflicts`)
- **Microservices Involved:** `SP.AttendanceSvc` (.NET 9), `SP.EmployeeSvc` (.NET 8)
- **Database Collections:** `Sahab.ERP.Attendance.WorkAssignmentMaps`, `EmployeeSvcNET8test.Employee`
- **Environment:** DEV | Company: `Attendance 11` (`3a24e5e5-302e-91bd-feaa-b07979766dfe`)

##### 1. Defect Summary & Live Proof
When an admin creates a work assignment for **Jeddah** (`3a24e667-5941-8331-9a1f-d77aa73945b3`), the system fails to verify whether the submitted employees actually belong to Jeddah. 
We tested employee `SA-EMP-0001` (whose official work location in `SP.EmployeeSvc` is **Dammam** and who already has an active, open-ended assignment in Dammam).

* **Check Conflicts Result:** Returns `HTTP 200 OK` with `hasConflicts: false, canProceed: true`, completely failing to detect both the location mismatch and the existing Dammam assignment.
* **Commit Result:** Returns `HTTP 200 OK`, creating Header `959cbf80-1cc2-48ae-8eb3-ce0dbf440b4d` and a second detail map in `ERP.Attendance.WorkAssignmentMaps` under Jeddah (`3a24e667...`).
* **MongoDB Live Proof:** In `Sahab.ERP.Attendance.WorkAssignmentMaps`, `SA-EMP-0001` now simultaneously holds **2 active open-ended maps** across Dammam and Jeddah (`IsActive: true` on both)!

##### 2. Expected Architecture & Fix
1. Validate `Employee.WorkLocationId == request.locationId`. If mismatched, reject with `HTTP 400 Bad Request` (`Cit.Attendance:Validation` / "Employee work location does not match assignment location").
2. Preflight conflict detection must search `WorkAssignmentMaps` across all locations of the company to prevent cross-location schedule collisions.
"""

marker = "# ✅ Part 5: Actionable Developer Checklist (Date-Wise)"
if marker in rep:
    rep = rep.replace(marker, defect_report_entry + "\n\n" + marker, 1)
    with open('Attendance2_Defects_Gaps_and_Architecture_Inconsistencies_Report.md', 'w', encoding='utf-8') as f:
        f.write(rep)
    print("Appended DEFECT-20261114-05 to Attendance2_Defects_Gaps_and_Architecture_Inconsistencies_Report.md")
else:
    print("Marker not found in report!")

# 3. Update Excel workbooks for WA-SEC-002
import openpyxl
for ef in ['AttendanceTestCases_Master_Consolidated.xlsx', 'AttendanceTestCases.xlsx', 'Attendance_Policies_Manual_API_TestCases_MongoDB.xlsx']:
    wb = openpyxl.load_workbook(ef)
    for sname in ['Work Assignments (Master 203)', 'Work Assignments']:
        if sname in wb.sheetnames:
            ws = wb[sname]
            for row in ws.iter_rows(min_row=2):
                tc_id = str(row[0].value).strip() if row[0].value else ''
                if tc_id == 'WA-SEC-002':
                    row[8].value = 'Fail'
                    row[9].value = 'DEFECT-20261114-05: Cross-location assignment allowed. Dammam employee assigned to Jeddah without validation.'
    wb.save(ef)
    print(f"Updated WA-SEC-002 in {ef}")
