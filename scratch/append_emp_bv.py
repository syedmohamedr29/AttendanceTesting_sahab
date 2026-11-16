# -*- coding: utf-8 -*-

emp_bv_section = """
---

## 10. Employee Master Prerequisites & Employment Lifecycle Rules (Active, Offboarding, DOJ & Location Integrity)

> **Inter-Service Integration:** `SP.AttendanceSvc` (.NET 9) queries `SP.EmployeeSvc` / `EmployeeSvcNET8test.Employee` via gRPC / Internal HTTP.  
> **Key Database:** MongoDB `EmployeeSvcNET8test.Employee` (2,502 employees in DEV).

### 10.1 The Employee Lifecycle State Rules for Work Assignment

```mermaid
flowchart TD
    subgraph Employee Status Matrix
        Active["Active Employee<br>(IsActive: true, Status: 1/2)"] -->|Allowed on/after DOJ| AssignOK["✅ Work Assignment Created<br>(startDate >= DOJ)"]
        
        FutureDOJ["Future Joiner<br>(DOJ > Today)"] -->|startDate < DOJ| RejectDOJ["❌ HTTP 400 Bad Request<br>Cannot precede DOJ"]
        FutureDOJ -->|startDate >= DOJ| AssignFuture["✅ Allowed for Future Period"]
        
        Offboarding["Offboarding / Notice Period<br>(Status: 5, LWD set)"] -->|endDate: null| RejectOpen["❌ HTTP 400 Bad Request<br>No open-ended assignments"]
        Offboarding -->|endDate <= LWD| AssignClosed["✅ Allowed until LWD"]
        Offboarding -->|endDate > LWD| RejectPastExit["❌ HTTP 400 Bad Request<br>Cannot exceed LWD"]
        
        Offboarded["Offboarded / Terminated<br>(Status: 6, IsActive: false)"] --> RejectTerm["❌ HTTP 400 Bad Request<br>Terminated employee rejected"]
        
        Inactive["Inactive / Suspended<br>(IsActive: false)"] --> RejectInact["❌ HTTP 400 Bad Request<br>Inactive employee rejected"]
    end
```

| Employee State | Source Collection Field | Work Assignment Allowed? | Permitted Assignment Period | Target Error if Violated |
| :--- | :--- | :---: | :--- | :--- |
| **Active Employee** | `IsActive: true`, `EmployeeStatus: 1/2` | **YES** | `startDate >= DateOfJoining`<br>`endDate`: Open-ended or closed | `400 Cit.Attendance:1405` (if past start) |
| **Future Hire (DOJ in future)** | `WorkInformation.DateOfJoining > today` | **CONDITIONAL** | Allowed **ONLY IF** `startDate >= DateOfJoining` | `400 Cit.Attendance:Validation` ("Cannot assign before DOJ") |
| **Offboarding / Notice Period** | `EmployeeStatus: 5`, `Separation.LWD` | **RESTRICTED** | Allowed **ONLY IF** `endDate != null` AND `endDate <= Separation.LWD` | `400 Cit.Attendance:Validation` ("Cannot exceed LWD") |
| **Terminated / Offboarded** | `EmployeeStatus: 6`, `IsActive: false` | ❌ **STRICT NO** | None. Completely blocked from new assignments. | `400 Cit.Attendance:Validation` ("Terminated employee") |
| **Inactive / Suspended** | `IsActive: false` | ❌ **STRICT NO** | None. Completely blocked. | `400 Cit.Attendance:Validation` ("Inactive employee") |
| **Cross-Location Employee** | `WorkInformation.WorkLocation._id != locationId` | ❌ **STRICT NO** | Employee cannot be assigned to another location's plan. | `400 Cit.Attendance:Validation` ("Location mismatch") |

---

### 10.2 Prerequisite Setup Protocol in `EmployeeSvcNET8test.Employee`

Before executing manual or automated Work Assignment tests:
1. **Query Target Employee:** Ensure employee document exists in `EmployeeSvcNET8test.Employee`:
   ```javascript
   db.getSiblingDB("EmployeeSvcNET8test").getCollection("Employee").findOne({
     "_id": UUID("f9e1a6d5-6bd5-7d46-ae85-38b81dc80887")
   }, {
     "EmployeeCode": 1,
     "IsActive": 1,
     "EmployeeStatus": 1,
     "BasicInformation.Company.CompanyId": 1,
     "WorkInformation.WorkLocation._id": 1,
     "WorkInformation.DateOfJoining": 1,
     "Separation": 1
   });
   ```
2. **Verify Mandatory Preconditions:**
   - `IsActive` must equal `true`.
   - `EmployeeStatus` must equal `1` or `2`.
   - `BasicInformation.Company.CompanyId` must match route `{companyId}`.
   - `WorkInformation.WorkLocation._id` must match query `{locationId}`.
   - `WorkInformation.DateOfJoining` must be on or before assignment `startDate` (`DOJ <= 2026-11-13`).
3. **Automated Teardown:** Delete test `WorkAssignments` and `WorkAssignmentMaps` after execution to restore the employee's active schedule to baseline.
"""

with open('reports/WORK_ASSIGNMENT_BUSINESS_VALIDATION.md', 'r', encoding='utf-8') as f:
    text = f.read()

# Add to TOC
toc_target = '9. [End-to-End POST & PATCH API Execution Protocol & Flow State Machines](#9-end-to-end-post--patch-api-execution-protocol--flow-state-machines)\n'
toc_addition = '10. [Employee Master Prerequisites & Employment Lifecycle Rules (Active, Offboarding, DOJ & Location Integrity)](#10-employee-master-prerequisites--employment-lifecycle-rules-active-offboarding-doj--location-integrity)\n'
new_text = text.replace(toc_target, toc_target + toc_addition)
new_text += emp_bv_section

with open('reports/WORK_ASSIGNMENT_BUSINESS_VALIDATION.md', 'w', encoding='utf-8') as f:
    f.write(new_text)

print('Updated reports/WORK_ASSIGNMENT_BUSINESS_VALIDATION.md with Section 10')
