# -*- coding: utf-8 -*-

emp_section = """
### 5.15 Employee Employment Lifecycle, DOJ Invariants & Location/Template Prerequisites Suite
- **Scope:** Validates employee master state guards (`Active`, `Inactive`, `Offboarding`, `Offboarded/Terminated`), Date of Joining (`DOJ`) invariants, exit boundaries, cross-location constraints, and Work Template compatibility.
- **Microservice Integration:** Validates integration between `SP.AttendanceSvc` and `SP.EmployeeSvc` (`EmployeeSvcNET8test.Employee`).

| Test Case ID | Test Title & Scope | Employee Master State (DB) | Request Payload & Query | Expected HTTP & Invariant Assertion |
| :--- | :--- | :--- | :--- | :--- |
| `WA-EMP-001` | **Positive: Active Employee Assigned On or After DOJ** | `IsActive: true`, `EmployeeStatus: 1/2` (Active), `DOJ: 2026-11-01`. | `startDate: "2026-11-13"`, `endDate: null`, valid location & plan. | **HTTP 200 OK.** Header and detail map created successfully in `WorkAssignmentMaps`. |
| `WA-EMP-002` | **Negative: Assignment Start Date Precedes DOJ (`startDate < DOJ`)** | `IsActive: true`, `DOJ: 2026-12-01` (Future hire). | `startDate: "2026-11-13"`, `endDate: null`. | **HTTP 400 Bad Request.** `Cit.Attendance:Validation` / "Work assignment start date cannot precede employee date of joining (2026-12-01)". |
| `WA-EMP-003` | **Negative: Inactive Employee Rejected** | `IsActive: false`, `EmployeeStatus: 1`. | `startDate: "2026-11-13"`, `employeeIds: [EMP_INACTIVE]`. | **HTTP 400 Bad Request.** `Cit.Attendance:Validation` / "Inactive employee cannot be assigned to a work plan". Zero DB writes. |
| `WA-EMP-004` | **Negative: Offboarded / Terminated Employee Rejected** | `IsActive: false`, `EmployeeStatus: 6` (Terminated/Separated). | `startDate: "2026-11-13"`, `employeeIds: [EMP_OFFBOARDED]`. | **HTTP 400 Bad Request.** `Cit.Attendance:Validation` / "Terminated or offboarded employee cannot be assigned". |
| `WA-EMP-005` | **Negative: Offboarding Employee Open-Ended Assignment Blocked** | `IsActive: true`, `EmployeeStatus: 5` (Notice Period), `Separation.LWD: 2026-11-30`. | `startDate: "2026-11-13"`, `endDate: null` (Open-ended). | **HTTP 400 Bad Request.** `Cit.Attendance:Validation` / "Cannot create open-ended work assignment for employee in offboarding". |
| `WA-EMP-006` | **Positive: Offboarding Employee Closed Assignment Before Exit** | `IsActive: true`, `EmployeeStatus: 5` (Notice Period), `Separation.LWD: 2026-11-30`. | `startDate: "2026-11-13"`, `endDate: "2026-11-25"` (Before LWD). | **HTTP 200 OK.** Permitted because assignment period completes prior to employee exit date. |
| `WA-EMP-007` | **Negative: Offboarding Employee Assignment Spanning Past Exit Date** | `IsActive: true`, `EmployeeStatus: 5` (Notice Period), `Separation.LWD: 2026-11-30`. | `startDate: "2026-11-13"`, `endDate: "2026-12-15"` (After LWD). | **HTTP 400 Bad Request.** `Cit.Attendance:Validation` / "Assignment endDate cannot exceed employee last working day (2026-11-30)". |
| `WA-EMP-008` | **Negative: Cross-Location Employee Assignment Blocked** | `IsActive: true`, registered at `WorkLocation: Loc_Chennai`. | Route `?locationId=Loc_Dammam`, `employeeIds: [EMP_CHENNAI]`. | **HTTP 400 Bad Request.** `Cit.Attendance:Validation` / "Employee does not belong to the specified work location". |
| `WA-EMP-009` | **Negative: Cross-Company Employee Assignment Blocked** | `IsActive: true`, registered under `Company: Attendance 10`. | Route `.../companies/{Attendance11_Id}/workassignments`. | **HTTP 400 Bad Request.** Multi-tenant company boundary enforced. |
| `WA-EMP-010` | **Boundary: Start Date Exactly on DOJ (`startDate == DOJ`)** | `IsActive: true`, `DOJ: 2026-11-13`. | `startDate: "2026-11-13"`, `endDate: null`. | **HTTP 200 OK.** Edge boundary permitted: employee assigned on their exact first working day. |
| `WA-EMP-011` | **Boundary: Start Date 1 Day Before DOJ (`startDate == DOJ - 1d`)** | `IsActive: true`, `DOJ: 2026-11-14`. | `startDate: "2026-11-13"`, `endDate: null`. | **HTTP 400 Bad Request.** Off-by-one boundary strictly caught and rejected. |
| `WA-EMP-012` | **Positive: Today Start Date Boundary (`startDate == today`)** | `IsActive: true`, `DOJ: 2025-01-01`. | `startDate: "2026-11-13"`, `endDate: null`. | **HTTP 200 OK.** Active immediately (`Status: 1`, `IsActive: true` in `WorkAssignmentMaps`). |
| `WA-EMP-013` | **Negative: Non-Existent Location ID in Query Parameter** | N/A | Query `?locationId=00000000-0000-0000-0000-000000000000`. | **HTTP 400 / 404.** Location not found. |
| `WA-EMP-014` | **Negative: Location Belongs to Different Company** | Valid employee. | Route has `Company_A`, query has `locationId` of `Company_B`. | **HTTP 400 Bad Request.** `Cit.Attendance:9002` / Location does not belong to company. |
| `WA-EMP-015` | **Negative: Work Plan Has Incompatible Rotation Template** | Valid employee. | `workPlanId` embeds `RotationWorkTemplate` (`TemplateType=5`). | **HTTP 400 Bad Request.** `Cit.Attendance:1104` (Incompatible template type for regular assignment). |
| `WA-EMP-016` | **Negative: Work Plan Has Incompatible Roster Template** | Valid employee. | `workPlanId` embeds `RosterWorkTemplate` (`TemplateType=4`). | **HTTP 400 Bad Request.** `Cit.Attendance:1104` (Incompatible template type for regular assignment). |
| `WA-EMP-017` | **Prerequisite Verification: Active Employee Setup in Employee8 DB** | Check `EmployeeSvcNET8test.Employee`. | Query employee by `_id` before test execution. | Verify `IsActive == true`, `WorkInformation.WorkLocation._id == locationId`, `DOJ <= startDate`. |
| `WA-EMP-018` | **Prerequisite Teardown & Isolation** | Test cleanup. | Delete test `WorkAssignments` and `WorkAssignmentMaps` after test run. | Restores employee schedule to baseline without orphaned records. |
"""

with open('reports/WORK_ASSIGNMENT_TEST_CASES.md', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('## 6. Cross-Cutting BVA, DTO Schema Invariants')
if idx != -1:
    new_text = text[:idx] + emp_section + '\n---\n\n' + text[idx:]
    # Update TOC
    toc_target = '   - [5.14 End-to-End Multi-Step Workflow & Sequence Test Cases (POST & PATCH Flows)](#514-end-to-end-multi-step-workflow--sequence-test-cases-post--patch-flows)\n'
    toc_addition = '   - [5.15 Employee Employment Lifecycle, DOJ Invariants & Location/Template Prerequisites Suite](#515-employee-employment-lifecycle-doj-invariants--locationtemplate-prerequisites-suite)\n'
    new_text = new_text.replace(toc_target, toc_target + toc_addition)
    
    # Update title count from 173 to 191
    new_text = new_text.replace('173 Comprehensive Scenarios', '191 Comprehensive Scenarios')
    new_text = new_text.replace('173 Test Cases', '191 Test Cases')
    new_text = new_text.replace('173 comprehensive test scenarios', '191 comprehensive test scenarios')
    
    with open('reports/WORK_ASSIGNMENT_TEST_CASES.md', 'w', encoding='utf-8') as f:
        f.write(new_text)
    print('Updated reports/WORK_ASSIGNMENT_TEST_CASES.md with Section 5.15 (18 new TCs, total 191 TCs)')
else:
    print('ERROR: Section 6 not found in reports/WORK_ASSIGNMENT_TEST_CASES.md')
