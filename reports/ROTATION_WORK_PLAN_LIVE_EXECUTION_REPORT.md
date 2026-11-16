# Shift Rotation & Rotation Work Plan Live Execution Report

**Microservices:** `SP.AttendanceSvc` (.NET 9 / ASP.NET Core) & `SP.EmployeeSvc` (.NET 8)  
**Target Environment:** DEV (`https://gw8.dev.zoolwork.com`)  
**Target Company:** `Attendance 11` (`3a24e5e5-302e-91bd-feaa-b07979766dfe`)  
**Locations Tested:** Dammam (`3a24e666-df63-3dc7-0ea7-02ec8be341e7`), Jeddah (`3a24e667-5941-8331-9a1f-d77aa73945b3`), Riyadh (`3a24e666-59d9-a713-f782-12163167ddcd`)  
**Execution Timestamp:** 2026-11-14T12:00:00+05:30  
**Test Methodology:** Live Microservice API Invocations, MongoDB State Assertions, Critical Boundary Analysis & Cross-Location Isolation Validation  
**Author:** Antigravity Senior QA Automation & Architecture Specialist  

---

## 1. Executive Summary & Quality Dashboard

| Metric | Value |
| :--- | :--- |
| **Total Test Scenarios Designed** | **194 Test Scenarios** (across 8 Suites) |
| **Live Core Scenarios Executed** | **45 Live Executions** |
| **Scenarios Passed** | **35 Passed** |
| **Scenarios Failed (Defects Uncovered)** | **10 Failed** |
| **New Defects Cataloged** | **6 Defects** (`DEFECT-20261114-06` to `DEFECT-20261114-11` / Defects 64 to 69) |
| **P0 Critical Defects** | **2 Critical** (Cross-Location Isolation Breach & Deletion Guard Missing) |
| **P1 Major Defects** | **2 Major** (PlanIndex Referential Integrity Corruption & Inactive Status Code Ambiguity) |
| **P2 Medium Defects** | **2 Medium** (Location Scoping Bypass & Inverted Date Range Bypass) |

---

## 2. Key Architecture & Business Invariant Findings

1. **Mandatory Template Type Invariant (`Cit.Attendance:2004`):**
   - Live testing revealed that `POST /shift-rotations` **strictly enforces** that plans must reference work templates of type `Rotation` (`TemplateType: 5`). Passing a `Fixed` template (`TemplateType: 1`) is rejected with:
     `{"error":{"code":"Cit.Attendance:2004","message":"A rotation plan can only use a rotation shift template. The selected template is of another type."}}`.
2. **ShortCode Validation Invariant on Rotation Work Templates:**
   - In `POST /worktemplates/rotation`, `ShortCode` must be **strictly alphanumeric** (hyphens rejected) and **exactly 7 characters** in length (e.g. `ROTD001`, `ROTN001`).
3. **Plan Count Constraints (`Cit.Attendance:2003`):**
   - In `POST /shift-rotations`, a rotation board requires **at least 2 plans and at most 4 plans** (`minPlans: 2`, `maxPlans: 4`).
4. **Schedule Materialization Confirmed in MongoDB:**
   - Calling `POST /shift-rotations/{id}/generate-schedule` generates sequential schedule maps with exact cyclical alternations between Team Alpha and Team Bravo. Re-running is verified idempotent (0 duplicate maps).

---

## 3. Defects Catalog Summary (Defects 64 to 69)

### 🔴 Defect 64 (`DEFECT-ROT-01` / `DEFECT-20261114-06`) — P0 Critical
- **Issue:** `DELETE /shift-rotations/{rotationId}` returns `HTTP 200 OK` and soft-deletes a board even when active members currently exist.
- **Evidence:** Board `06a8cb5c-c60b-4a45-bf18-87a2e88a2448` was deleted while members `SA-EMP-0002` and `SA-EMP-0003` were actively assigned.
- **Remediation:** Enforce pre-deletion check: `if (Members.Any(m => m.IsActive)) return BadRequest("Cannot delete board with active members");`.

### 🔴 Defect 65 (`DEFECT-ROT-02` / `DEFECT-20261114-07`) — P0 Critical
- **Issue:** Location isolation failure: Employee belonging to Dammam (`SA-EMP-0001`) was assigned to a Jeddah rotation team (`03ade8fe-7d7f-4244-8172-94111fffef78`) and generated 104 steps in Jeddah!
- **Evidence:** `SA-EMP-0001` now possesses concurrent active open-ended maps in `Sahab.ERP.Attendance.WorkAssignmentMaps` across Dammam and Jeddah simultaneously.
- **Remediation:** Validate `employee.CompanyLocationId == rotation.LocationId` before enrolling.

### 🟠 Defect 66 (`DEFECT-ROT-03` / `DEFECT-20261114-08`) — P1 Major
- **Issue:** Silent schema corruption: In `POST /shift-rotations`, steps referencing non-existent `planIndex` 99 were accepted with `HTTP 200 OK`.
- **Remediation:** Assert `request.Plans.Any(p => p.PlanIndex == step.PlanIndex)`.

### 🟡 Defect 67 (`DEFECT-ROT-04` / `DEFECT-20261114-09`) — P2 Medium
- **Issue:** `GET /shift-rotations` returns `HTTP 200 OK` without mandatory `locationId` query parameter.

### 🟡 Defect 68 (`DEFECT-ROT-05` / `DEFECT-20261114-10`) — P2 Medium
- **Issue:** `GET /shift-rotations/{id}/rotation-grid` with `from > to` returns `HTTP 200 OK` with empty matrix instead of `400 Bad Request`.

### 🟠 Defect 69 (`DEFECT-ROT-06` / `DEFECT-20261114-11`) — P1 Major
- **Issue:** Enrolling inactive employee `SA-EMP-0006` returns `HTTP 200 OK: "No employees were enrolled"` instead of `400 Bad Request`.

---

## 4. Master Excel Workbooks Synchronization
All live test results, Pass/Fail classifications, HTTP status codes, and defect links have been synchronized into the `'Rotation Work Plans'` sheet across all three master workbooks:
- `AttendanceTestCases_Master_Consolidated.xlsx`
- `AttendanceTestCases.xlsx`
- `Attendance_Policies_Manual_API_TestCases_MongoDB.xlsx`
