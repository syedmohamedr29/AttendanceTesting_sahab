# Rotation Work Assignment Master Test Specification (RTM, DTO Validations, Operational Lifecycle & Security Invariants)

**Microservices:** `SP.AttendanceSvc` (.NET 9 / ASP.NET Core) & `SP.EmployeeSvc` (.NET 8)  
**Gateway Routes:** `https://gw8.dev.zoolwork.com/api/companies/{companyId}/shift-rotations/{rotationId}`  
**Database Collections:** `Sahab.ERP.Attendance.ShiftRotationBoard`, `ERP.Attendance.WorkAssignmentMaps`, `ERP.Attendance.WorkAssignments`, `EmployeeSvcNET8test.Employee`  
**Test Methodology:** Requirements Traceability Matrix (RTM), Equivalence Partitioning (EP), Boundary Value Analysis (BVA), Negative/Positive Standalone, Cross-Location Guards, and MongoDB Operational Document State Transitions  
**Total Test Scenarios:** 190 Scenarios across 10 Structured Operational Suites  
**Author:** Antigravity Senior QA Automation & Architecture Specialist  

---

## 1. Executive Test Strategy & Operational Assignment Lifecycle

A **Rotation Work Assignment** is the runtime bridge linking individual employees to recurring cyclic shift rotation boards. While a Rotation Work Plan defines the structural rules (teams, plans, patterns, and durations), the **Work Assignment** layer handles:

1. **Preflight Conflict Detection:** Evaluating overlapping regular plans and team assignments before committing.

2. **Team Enrollment:** Atomic single and bulk enrollment with open-ended (`9999-12-31`) or bounded tenure.

3. **Cross-Location Isolation:** Ensuring employees can only be assigned to rotations matching their physical facility in `SP.EmployeeSvc`.

4. **Schedule Materialization:** Rolling projection of operational shift instances into `Sahab.ERP.Attendance.WorkAssignmentMaps` with exact cyclical step alternations.

5. **Member Lifecycle Transitions:** Period resizing, intra-rotation team transfers, cross-board transfers, and soft-deletion with future schedule map pruning.

---

## 2. Requirements Traceability Matrix (RTM)

| Req ID | Business Requirement Description | Microservice Scope | Enforcement Endpoint |
| :---: | :--- | :--- | :--- |
| **REQ-RWA-001** | Preflight Conflict Detection Engine | `Preflight endpoint must evaluate date overlaps, existing active plans, and team memberships without mutating DB.` | `check-conflicts Endpoint` |
| **REQ-RWA-002** | Atomic Team Assignment Enrollment | `POST /employees must enroll employees atomically into rotation teams with valid start and end dates.` | `POST /teams/{teamId}/employees` |
| **REQ-RWA-003** | Mandatory Location Scoping | `Enrollment, move, and edit endpoints must enforce valid locationId query parameter matching the rotation board.` | `Location Scoping Guard` |
| **REQ-RWA-004** | Cross-Location Isolation Guard | `Employees can ONLY be assigned to rotations matching their assigned workLocation in SP.EmployeeSvc.` | `Location Isolation Guard` |
| **REQ-RWA-005** | Employee Active Status Requirement | `Only active employees (IsActive: true, Status: 2) can be enrolled. Inactive or offboarded employees must be rejected.` | `Employee Status Guard` |
| **REQ-RWA-006** | Open-Ended Assignment Support | `Rotation assignments support open-ended tenure (endDate: null), persisted as 9999-12-31.` | `AddRotationEmployeesDto.EndDate` |
| **REQ-RWA-007** | Fixed Assignment Period Boundary | `Fixed date assignments require endDate >= startDate. endDate < startDate must be rejected with 400.` | `AddRotationEmployeesDto Validation` |
| **REQ-RWA-008** | Automatic Conflict Resolution (adjustConflicts) | `When adjustConflicts: true, system auto-truncates or splits existing overlapping assignments. If false, rejects with 400.` | `Conflict Resolution Engine` |
| **REQ-RWA-009** | Duplicate Active Membership Rejection | `An employee already actively assigned to a team cannot be re-enrolled into the same or another team in the same rotation.` | `Membership Uniqueness Guard` |
| **REQ-RWA-010** | Bulk Assignment Scalability | `System must support enrolling multiple active employees in a single atomic request (up to company workforce capacity).` | `Bulk Enrollment Handler` |
| **REQ-RWA-011** | Schedule Materialization Engine | `POST /generate-schedule must materialize operational shift instances into ERP.Attendance.WorkAssignmentMaps.` | `Schedule Generator` |
| **REQ-RWA-012** | Operational Map Data Integrity | `Generated maps must hold Source: 'Rotation', RotationId, TeamId, WorkPlanId, StartDate, EndDate, and IsActive.` | `WorkAssignmentMaps Schema` |
| **REQ-RWA-013** | Schedule Generation Idempotency | `Repeated execution of generate-schedule must update existing maps without creating duplicate entries.` | `Idempotency Controller` |
| **REQ-RWA-014** | Staggered Team Sequence Realignment | `Schedule materialization must project step sequences based on team startSequenceOrder and pattern durations.` | `Cyclic Math Engine` |
| **REQ-RWA-015** | Member Period Modification (Resizing) | `PATCH /members/{id} must allow extending or shortening assignment periods with automatic map adjustment.` | `EditRotationMemberPeriodDto` |
| **REQ-RWA-016** | Intra-Rotation Team Transfer | `POST /move-team transfers member between teams in the same rotation board from effectiveFrom.` | `MoveRotationMemberTeamDto` |
| **REQ-RWA-017** | Inter-Board & Regular Work Plan Transfer | `PATCH /move transfers member across rotation boards or into regular work plans with preflight conflict validation.` | `MoveEmployeeDto` |
| **REQ-RWA-018** | Member Soft-Deletion & Map Pruning | `DELETE /members/{id} sets IsActive: false in ShiftRotationBoard.Members and purges future operational schedule maps.` | `DELETE /members/{id}` |
| **REQ-RWA-019** | Scheduled Future Member Termination | `DELETE /members/{id}?endDate={futureDate} keeps member active until futureDate and prunes maps thereafter.` | `Future Pruning Engine` |
| **REQ-RWA-020** | Active Member Rotation Deletion Guard | `Rotation boards with active members cannot be deleted. Deletion attempts must be blocked with 400 Bad Request.` | `Active Member Deletion Guard` |
| **REQ-RWA-021** | Member Roster Listing & Segmentation | `GET /employees must list assigned members with filtering by teamId, segment (Active/Inactive), and snapshot asOf date.` | `GET /employees Filter` |
| **REQ-RWA-022** | Individual Projected Schedule Query | `GET /employees/{id}/schedule returns daily shift timeline for an employee within a specified date window.` | `GET /schedule Query` |
| **REQ-RWA-023** | Employee Self-Service Rotation Lookup | `GET /me/rotation returns the authenticated employee's active rotation board and current team.` | `GET /me/rotation` |
| **REQ-RWA-024** | Multi-Tenant Cross-Company Isolation | `Attempting to assign or query members across tenant boundaries via companyId tampering must return 403 Forbidden.` | `Tenant Security Guard` |

---

## 3. Comprehensive Test Suites (190 Test Scenarios)

### Suite 1: Preflight Conflict Check Engine (POST .../check-conflicts)

| TC ID | Test Scenario | Category | Priority | Input / Preconditions | Expected HTTP | Expected Response / DB State | RTM Req |
| :--- | :--- | :---: | :---: | :--- | :---: | :--- | :---: |
| `RWA-CHK-001` | Positive: Preflight check for clean active employee with no existing assignments | POS | P0 | Valid companyId, locationId, clean employeeId, startDate: 2026-12-01, endDate: null | `200 OK` | Returns hasConflicts: false, cleanEmployeeIds: [empId], blockedEmployeeIds: [], canProceed: true. | REQ-RWA-001 |
| `RWA-CHK-002` | Positive: Preflight check detects active regular work plan conflict | POS | P0 | Employee has active regular work plan, adjustConflicts: false | `200 OK` | Returns hasConflicts: true, conflicts itemize overlapping RegularPlan with resolution: Removed/Adjusted. | REQ-RWA-001, REQ-RWA-008 |
| `RWA-CHK-003` | Positive: Preflight check detects employee already active in same rotation team | POS | P0 | Employee already assigned to Team Alpha, querying Team Alpha | `200 OK` | Returns alreadyMembers: [empId], alreadyMemberCount: 1, canProceed: false. | REQ-RWA-001, REQ-RWA-009 |
| `RWA-CHK-004` | Positive: Preflight check detects employee active in another team of same rotation | POS | P0 | Employee assigned to Team Alpha, preflight checking Team Bravo | `200 OK` | Returns conflict: employee active in another team. Advises move-team endpoint. | REQ-RWA-001, REQ-RWA-016 |
| `RWA-CHK-005` | Positive: Preflight check for bulk batch (mix of 2 clean, 2 conflicting employees) | POS | P1 | 4 employeeIds submitted in single preflight check | `200 OK` | Itemizes cleanEmployeeIds (2) and adjustableEmployeeIds (2) accurately. | REQ-RWA-001, REQ-RWA-010 |
| `RWA-CHK-006` | Positive: Preflight check with excludeMembershipId ignores current membership | POS | P1 | excludeMembershipId set to employee's existing membership GUID | `200 OK` | Ignores self-conflict during period edit simulation. | REQ-RWA-001, REQ-RWA-015 |
| `RWA-CHK-007` | Negative DTO: Missing employeeIds array in preflight check | DTO | P0 | employeeIds omitted or null | `400 Bad Request` | Validation error: employeeIds array is required. | REQ-RWA-001 |
| `RWA-CHK-008` | Negative DTO: Empty employeeIds array in preflight check | DTO | P1 | employeeIds: [] | `400 Bad Request` | Validation error: At least one employeeId required. | REQ-RWA-001 |
| `RWA-CHK-009` | Negative DTO: Missing startDate in preflight check | DTO | P0 | startDate omitted or null | `400 Bad Request` | Validation error: startDate is required. | REQ-RWA-007 |
| `RWA-CHK-010` | Negative DTO: Invalid date format in startDate | DTO | P2 | startDate: '2026/13/45' | `400 Bad Request` | Schema date parsing error. | REQ-RWA-007 |
| `RWA-CHK-011` | Negative BVA: endDate earlier than startDate in preflight check | BVA | P0 | startDate: 2026-12-01, endDate: 2026-11-01 | `400 Bad Request` | Validation error: endDate cannot be before startDate. | REQ-RWA-007 |
| `RWA-CHK-012` | Positive BVA: Single day period boundary (endDate == startDate) | BVA | P2 | startDate: 2026-12-01, endDate: 2026-12-01 | `200 OK` | Preflight allows single day assignment check. | REQ-RWA-007 |
| `RWA-CHK-013` | Negative: Preflight check on non-existent rotationId | NEG | P1 | rotationId: 00000000-0000-0000-0000-000000000000 | `404 Not Found` | Rotation board not found error. | REQ-RWA-001 |
| `RWA-CHK-014` | Negative: Preflight check on non-existent teamId | NEG | P1 | teamId: 00000000-0000-0000-0000-000000000000 | `404 Not Found` | Team not found in rotation board. | REQ-RWA-001 |
| `RWA-CHK-015` | Scoping Negative: Preflight check without mandatory locationId | SEC | P0 | Omit locationId query parameter | `400 Bad Request` | Enforces mandatory location scoping. | REQ-RWA-003 |
| `RWA-CHK-016` | Scoping Negative: locationId query mismatch with rotation board location | SEC | P1 | locationId=Dammam while rotation board is Jeddah | `400/404` | Location mismatch rejection. | REQ-RWA-003 |
| `RWA-CHK-017` | Security: Cross-location preflight check (Dammam employee on Jeddah board) | SEC | P0 | Preflight Dammam employee SA-EMP-0001 on Jeddah rotation | `400 / Conflict Block` | Preflight must flag location mismatch: employee does not belong to rotation location. | REQ-RWA-004 |
| `RWA-CHK-018` | Security: Inactive employee in preflight check (SA-EMP-0006) | BUS | P0 | employeeIds: [SA-EMP-0006] (IsActive: false) | `400 / Blocked` | Preflight must mark employee as blocked: Inactive employee cannot be enrolled. | REQ-RWA-005 |
| `RWA-CHK-019` | Security: Offboarded employee in preflight check | BUS | P0 | Employee in offboarded status in EmployeeSvc | `400 / Blocked` | Preflight marks employee as blocked. | REQ-RWA-005 |
| `RWA-CHK-020` | Idempotency: Preflight check does NOT mutate MongoDB state | POS | P0 | Verify ShiftRotationBoard and WorkAssignmentMaps before and after check | `200 OK` | 0 documents created or modified in MongoDB. | REQ-RWA-001 |

---

### Suite 2: Member Team Enrollment & Bulk Assignment (POST .../employees)

| TC ID | Test Scenario | Category | Priority | Input / Preconditions | Expected HTTP | Expected Response / DB State | RTM Req |
| :--- | :--- | :---: | :---: | :--- | :---: | :--- | :---: |
| `RWA-ENR-001` | Positive: Enroll single active employee with open-ended period (endDate: null) | POS | P0 | Valid rotationId, teamId, employeeId, startDate: 2026-11-20, endDate: null | `200 OK` | Enrolls member into team; MongoDB stores EndDate: 9999-12-31, IsActive: true. | REQ-RWA-002, REQ-RWA-006 |
| `RWA-ENR-002` | Positive: Enroll employee with fixed date range (startDate to endDate) | POS | P0 | startDate: 2026-12-01, endDate: 2027-05-31 | `200 OK` | Enrolls member with explicit bounded period. | REQ-RWA-002, REQ-RWA-007 |
| `RWA-ENR-003` | Positive: Bulk enroll 5 active employees simultaneously into Team Alpha | POS | P0 | employeeIds: [emp1, emp2, emp3, emp4, emp5] | `200 OK` | All 5 employees enrolled atomically in single database transaction. | REQ-RWA-002, REQ-RWA-010 |
| `RWA-ENR-004` | Positive: Enroll employee with overlapping regular plan when adjustConflicts: true | BUS | P0 | adjustConflicts: true with conflicting active regular work plan | `200 OK` | Auto-adjusts existing regular plan endDate to startDate-1 and enrolls member. | REQ-RWA-002, REQ-RWA-008 |
| `RWA-ENR-005` | Business Negative: Enroll employee with overlapping plan when adjustConflicts: false | BUS | P0 | adjustConflicts: false with conflicting active regular work plan | `400 Bad Request` | Rejection: Cit.Attendance:1409 / Review adjustments and confirm with adjustConflicts: true. | REQ-RWA-002, REQ-RWA-008 |
| `RWA-ENR-006` | Business Negative: Re-enrolling employee already actively assigned to same team | BUS | P0 | Enrolling active member into same team again | `400 Bad Request` | Duplicate enrollment rejected: Employee is already an active member of this team. | REQ-RWA-002, REQ-RWA-009 |
| `RWA-ENR-007` | Business Negative: Enrolling employee already active in another team of same rotation | BUS | P0 | Enrolling Team Alpha member directly into Team Bravo | `400 Bad Request` | Collision rejected: Employee already active in rotation. Use move-team workflow. | REQ-RWA-002, REQ-RWA-009 |
| `RWA-ENR-008` | Negative DTO: Missing employeeIds array | DTO | P0 | employeeIds: null or omitted | `400 Bad Request` | Validation error: employeeIds array is required. | REQ-RWA-002 |
| `RWA-ENR-009` | Negative DTO: Empty employeeIds array | DTO | P1 | employeeIds: [] | `400 Bad Request` | Validation error: At least one employeeId required. | REQ-RWA-002 |
| `RWA-ENR-010` | Negative DTO: Missing startDate in enrollment payload | DTO | P0 | startDate: null or omitted | `400 Bad Request` | Validation error: startDate is required. | REQ-RWA-007 |
| `RWA-ENR-011` | Negative DTO: Malformed GUID string in employeeIds array | DTO | P2 | employeeIds: ['not-a-valid-guid'] | `400 Bad Request` | GUID format parsing failure. | REQ-RWA-002 |
| `RWA-ENR-012` | Negative BVA: endDate < startDate (end date before start date) | BVA | P0 | startDate: 2026-12-01, endDate: 2026-11-01 | `400 Bad Request` | Validation error: endDate cannot be earlier than startDate. | REQ-RWA-007 |
| `RWA-ENR-013` | Boundary: endDate == startDate (single-day enrollment) | BVA | P2 | startDate: 2026-12-01, endDate: 2026-12-01 | `200 OK` | Single day assignment boundary accepted. | REQ-RWA-007 |
| `RWA-ENR-014` | Effective Date: Retroactive assignment (startDate 30 days in past) | POS | P1 | startDate: 30 days prior to today | `200 OK` | Creates historical member record for past attendance reconciliation. | REQ-RWA-002 |
| `RWA-ENR-015` | Effective Date: Future assignment (startDate 60 days in future) | POS | P1 | startDate: 60 days in future | `200 OK` | Creates pending member record active from future effective date. | REQ-RWA-002 |
| `RWA-ENR-016` | Deduplication: Duplicate employee GUIDs in same request array | DTO | P2 | employeeIds: [empA, empA] | `200 OK` | Deduplicates array and enrolls employee once cleanly. | REQ-RWA-002 |
| `RWA-ENR-017` | Negative: Enroll into non-existent teamId | NEG | P1 | POST /teams/{fakeTeamId}/employees | `404 Not Found` | Team not found error. | REQ-RWA-002 |
| `RWA-ENR-018` | Negative: Enroll into non-existent rotationId | NEG | P1 | POST /shift-rotations/{fakeId}/teams/{teamId}/employees | `404 Not Found` | Rotation board not found error. | REQ-RWA-002 |
| `RWA-ENR-019` | Scoping Negative: Enroll employees without mandatory locationId | SEC | P0 | POST /employees without locationId query | `400 Bad Request` | Enforces mandatory location scoping. | REQ-RWA-003 |
| `RWA-ENR-020` | Scoping Negative: locationId does not match rotation board location | SEC | P1 | locationId=Dammam while rotation board is Jeddah | `400/404` | Mismatched location scoping rejected. | REQ-RWA-003 |
| `RWA-ENR-021` | Atomic Rollback: Batch contains 1 valid and 1 non-existent employee GUID | BUS | P1 | employeeIds: [ValidEmp, 00000000-0000-0000-0000-000000000000] | `400/404` | Transaction rolls back or reports partial notFoundEmployeeIds cleanly. | REQ-RWA-010 |
| `RWA-ENR-022` | High-Volume Capacity: Bulk enrollment of 48 company employees simultaneously | POS | P1 | All 48 active employees enrolled into Team Alpha | `200 OK` | Bulk enrollment completes within performance budget (< 3s). | REQ-RWA-010 |
| `RWA-ENR-023` | MongoDB Document Assert: Verify Members array in ShiftRotationBoard | POS | P0 | Query ShiftRotationBoard in Sahab DB | `200 OK` | Member document appended with MembershipId, EmployeeId, TeamId, StartDate. | REQ-RWA-002 |
| `RWA-ENR-024` | MongoDB Field Assert: Verify member document fields and timestamps | POS | P0 | Inspect embedded member fields | `200 OK` | PeriodStartDate, PeriodEndDate, GeneratedThrough, IsActive: true populated. | REQ-RWA-002 |
| `RWA-ENR-025` | Re-activation Guard: Enroll employee on a soft-deleted rotation board | BUS | P1 | POST /employees targeting rotation board with IsDeleted: true | `400 Bad Request` | Validation error: Cannot enroll employees on a deleted rotation board. | REQ-RWA-020 |
| `RWA-ENR-026` | Security: Cross-tenant enrollment attempt (Company B employee into Company A) | SEC | P0 | Employee from another tenant in employeeIds array | `403/400` | Tenant isolation guard blocks foreign employee enrollment. | REQ-RWA-024 |

---

### Suite 3: Critical Cross-Location Isolation Guards

| TC ID | Test Scenario | Category | Priority | Input / Preconditions | Expected HTTP | Expected Response / DB State | RTM Req |
| :--- | :--- | :---: | :---: | :--- | :---: | :--- | :---: |
| `RWA-LOC-001` | CRITICAL GUARD: Enroll Dammam employee (SA-EMP-0001) into Jeddah Rotation Board | SEC | P0 | SA-EMP-0001 (WorkLocation: Dammam) submitted to Jeddah Rotation | `400 Bad Request` | Security Guard: System must verify employee workLocation and reject cross-location enrollment. | REQ-RWA-004 |
| `RWA-LOC-002` | CRITICAL GUARD: Preflight conflict check detects cross-location mismatch | SEC | P0 | POST /check-conflicts for Dammam employee on Jeddah board | `Conflict / Block` | Preflight reports blockedEmployeeIds: [empId], canProceed: false due to location mismatch. | REQ-RWA-004 |
| `RWA-LOC-003` | CRITICAL GUARD: Enroll Dammam employee (SA-EMP-0004) into Riyadh Rotation Board | SEC | P0 | SA-EMP-0004 (WorkLocation: Dammam) submitted to Riyadh Rotation | `400 Bad Request` | Cross-location enrollment into Riyadh facility rejected. | REQ-RWA-004 |
| `RWA-LOC-004` | CRITICAL GUARD: Bulk batch containing employees from mixed locations | SEC | P0 | employeeIds: [DammamEmp, JeddahEmp] submitted to Jeddah rotation | `400 Bad Request` | Identifies and rejects employees whose workLocation does not match target board. | REQ-RWA-004 |
| `RWA-LOC-005` | Multi-Location Schedule Collision: Employee active in Dammam regular plan enrolled in Jeddah | SEC | P0 | Employee active in Dammam plan submitted to Jeddah rotation with adjustConflicts: true | `400 Bad Request` | Cross-location conflict adjustment blocked without formal location transfer. | REQ-RWA-004 |
| `RWA-LOC-006` | MongoDB Multi-Location Map Assert: Verify 0 concurrent cross-location maps created | SEC | P0 | Query WorkAssignmentMaps where EmployeeId == SA-EMP-0001 and IsActive: true | `0 Concurrent Maps` | Employee must NOT hold active maps across disparate LocationIds simultaneously. | REQ-RWA-004 |
| `RWA-LOC-007` | Cross-Location Move Attempt: Move member from Dammam rotation to Jeddah rotation | SEC | P0 | PATCH /move targeting rotation board in another location | `400 Bad Request` | Inter-location transfer blocked without formal EmployeeSvc location transfer. | REQ-RWA-004 |
| `RWA-LOC-008` | Cross-Location Move Preflight: Check conflicts for move across locations | SEC | P0 | POST /move/check-conflicts targeting different location | `Conflict / Block` | Flags location transfer violation. | REQ-RWA-004 |
| `RWA-LOC-009` | Formal Transfer Acceptance: Employee formally transferred to Jeddah in EmployeeSvc | POS | P1 | Employee WorkLocation updated to Jeddah, then enrolled in Jeddah rotation | `200 OK` | Enrollment succeeds once employee location matches rotation location. | REQ-RWA-004 |
| `RWA-LOC-010` | Location Scoping Tampering: Pass locationId=Jeddah in query for Dammam rotationId in path | SEC | P0 | Query locationId != Path board's LocationId | `400 Bad Request` | URL path to query mismatch rejected. | REQ-RWA-003 |
| `RWA-LOC-011` | Company Location Validation: Pass non-existent locationId GUID | SEC | P1 | locationId: 00000000-0000-0000-0000-000000000000 | `404 Not Found` | Location not found in company. | REQ-RWA-003 |
| `RWA-LOC-012` | Cross-Tenant Location Tampering: Pass locationId belonging to Company B | SEC | P0 | locationId from another company | `403 Forbidden` | Tenant isolation guard blocks foreign location access. | REQ-RWA-024 |
| `RWA-LOC-013` | Schedule Materialization Location Assert: Generated maps hold board's LocationId | POS | P0 | Inspect LocationId in materialized WorkAssignmentMaps | `200 OK` | Map LocationId strictly equals rotation board's LocationId. | REQ-RWA-012 |
| `RWA-LOC-014` | Roster Query Location Scoping: Query members across locations | POS | P1 | GET /employees respects rotation board location boundary | `200 OK` | Only returns members of specified rotation board. | REQ-RWA-021 |
| `RWA-LOC-015` | Employee Projected Schedule Location Assert: Schedule bound to assigned location | POS | P1 | GET /employees/{id}/schedule reflects correct location metadata | `200 OK` | Location details match rotation board. | REQ-RWA-022 |
| `RWA-LOC-016` | Tenant Name Location Header Verification: Multilingual location preserved | POS | P2 | Verify locationName object in response payload | `200 OK` | Returns accurate localized location name (en, ar). | REQ-RWA-003 |

---

### Suite 4: Employee Lifecycle & Status Constraints

| TC ID | Test Scenario | Category | Priority | Input / Preconditions | Expected HTTP | Expected Response / DB State | RTM Req |
| :--- | :--- | :---: | :---: | :--- | :---: | :--- | :---: |
| `RWA-EMP-001` | CRITICAL GUARD: Enrolling inactive employee (SA-EMP-0006, IsActive: false) | BUS | P0 | employeeIds: [SA-EMP-0006] (IsActive: false, Status: 1) | `400 Bad Request` | Validation error: Inactive employee cannot be enrolled in shift rotation. | REQ-RWA-005 |
| `RWA-EMP-002` | CRITICAL GUARD: Status Code Assert on Inactive Enrollment | BUS | P0 | Assert HTTP response code is 400 Bad Request (NOT 200 OK with 'No employees enrolled') | `400 Bad Request` | Defect 69 verification: System must return 400 for invalid inactive inputs. | REQ-RWA-005 |
| `RWA-EMP-003` | Business Negative: Enrolling offboarded employee (Status: 3) | BUS | P0 | Employee initiated into offboarding in EmployeeSvc | `400 Bad Request` | Validation error: Offboarded employee cannot be assigned to rotation. | REQ-RWA-005 |
| `RWA-EMP-004` | Business Negative: Enrolling exited/terminated employee | BUS | P0 | Employee finalized exit in EmployeeSvc | `400 Bad Request` | Validation error: Terminated employee cannot be assigned. | REQ-RWA-005 |
| `RWA-EMP-005` | Business Positive: Enrolling re-activated employee (SA-EMP-0004) | POS | P0 | Employee transitioned IsActive: false -> true via activateemployees endpoint | `200 OK` | Enrollment succeeds once employee is activated. | REQ-RWA-005 |
| `RWA-EMP-006` | Lifecycle Sync: Offboarding active rotation member auto-truncates membership | BUS | P0 | Initiate offboarding on active rotation member in EmployeeSvc | `200 OK` | Attendance sync event truncates rotation membership to offboarding date. | REQ-RWA-005 |
| `RWA-EMP-007` | Lifecycle Sync: Exited member has schedule maps deleted after exit date | BUS | P0 | Finalize exit on rotation member | `200 OK` | Future schedule maps in WorkAssignmentMaps purged. | REQ-RWA-005, REQ-RWA-018 |
| `RWA-EMP-008` | Probationary Employee: Enrolling active employee in probationary period | POS | P1 | Employee with active probation status | `200 OK` | Enrolls cleanly based on active employment flag. | REQ-RWA-005 |
| `RWA-EMP-009` | Contract End Date Alignment: Enrollment endDate exceeding employment contract | BUS | P1 | Employee contract ends 2027-01-01, assignment open-ended | `200 / Warning` | System bounds assignment or warns about employment contract expiration. | REQ-RWA-005 |
| `RWA-EMP-010` | Re-hire Lifecycle: Enrolling re-hired employee with new employment record | POS | P1 | Re-hired employee with active status | `200 OK` | Enrolls under new active employment tenure. | REQ-RWA-005 |
| `RWA-EMP-011` | Bulk Inactive Mixture: 3 active employees + 1 inactive employee in same batch | BUS | P1 | employeeIds: [Active1, Active2, Active3, Inactive] | `400 / Partial Report` | Reports inactive employee clearly; enrolls active members or rolls back atomically. | REQ-RWA-005, REQ-RWA-010 |
| `RWA-EMP-012` | Orphaned Member Prevention: Verify inactive employee NOT appended to Members array | POS | P0 | Query ShiftRotationBoard.Members after failed inactive enrollment | `200 OK` | 0 inactive members added to MongoDB document. | REQ-RWA-005 |
| `RWA-EMP-013` | Non-existent Employee: Submit random GUID not in Employee collection | NEG | P1 | employeeIds: [randomGuid] | `404/400` | Employee not found error. | REQ-RWA-005 |
| `RWA-EMP-014` | Cross-Tenant Employee: Submit valid employeeId from Company B | SEC | P0 | employeeIds: [CompB_EmpId] | `403/400` | Multi-tenancy isolation guard blocks foreign employee. | REQ-RWA-024 |
| `RWA-EMP-015` | Employee Code Consistency: Verify employeeCode in response matches EmployeeSvc | POS | P1 | Compare employeeCode in API response with Employee collection | `200 OK` | Exact match (e.g. SA-EMP-0004). | REQ-RWA-005 |
| `RWA-EMP-016` | Employee Department & Designation Localization: en and ar objects populated | POS | P2 | Inspect department and designation in addedMembers response | `200 OK` | Multilingual strings correctly resolved. | REQ-RWA-002 |
| `RWA-EMP-017` | Attendance Exemption Flag: Enrolling employee marked attendance-exempt | POS | P2 | Employee marked exempt in Attendance Config | `200 OK` | Enrolls in rotation roster; exemption honored during punch processing. | REQ-RWA-005 |
| `RWA-EMP-018` | Audit Trail Assert: Verify CreatedBy identity recorded in member record | POS | P2 | Inspect CreatedBy user email in MongoDB member record | `200 OK` | Authenticated user identity accurately logged. | REQ-RWA-002 |

---

### Suite 5: Schedule Materialization & Operational Maps Engine

| TC ID | Test Scenario | Category | Priority | Input / Preconditions | Expected HTTP | Expected Response / DB State | RTM Req |
| :--- | :--- | :---: | :---: | :--- | :---: | :--- | :---: |
| `RWA-SCH-001` | Positive: Trigger schedule generation for rotation board with active members | POS | P0 | POST /shift-rotations/{id}/generate-schedule?locationId=ValidLoc | `200 OK` | Triggers cyclical schedule calculation across active teams. | REQ-RWA-011 |
| `RWA-SCH-002` | MongoDB Collection Assert: Verify documents created in ERP.Attendance.WorkAssignmentMaps | POS | P0 | Query WorkAssignmentMaps where RotationId == rotationId | `200 OK` | Documents materialized with operational shift data. | REQ-RWA-011, REQ-RWA-012 |
| `RWA-SCH-003` | Schema Field Assert: Verify Source: 'Rotation' on materialized maps | POS | P0 | Inspect Source field on generated map documents | `200 OK` | Source field strictly equals 'Rotation'. | REQ-RWA-012 |
| `RWA-SCH-004` | Foreign Key Assert: Verify RotationId, TeamId, and WorkPlanId linkage | POS | P0 | Validate GUID references in map documents | `200 OK` | RotationId and TeamId correctly reference ShiftRotationBoard. | REQ-RWA-012 |
| `RWA-SCH-005` | Cyclic Rotation Pattern Assert: Team Alpha alternates Plan 1 (wk1) -> Plan 2 (wk2) | POS | P0 | Inspect sequential weekly maps for Team Alpha | `200 OK` | Shifts alternate between Morning and Night plans across weeks. | REQ-RWA-014 |
| `RWA-SCH-006` | Staggered Start Sequence Assert: Team Bravo starts on Plan 2 based on sequenceOrder: 2 | POS | P0 | Inspect sequential weekly maps for Team Bravo | `200 OK` | Team Bravo executes Plan 2 (wk1) -> Plan 1 (wk2). | REQ-RWA-014 |
| `RWA-SCH-007` | Uneven Rotation Duration Assert: Step durations reflect independent durationWeeks | POS | P1 | Schedule generated on Uneven board (Step 1=2 wks, Step 2=1 wk) | `200 OK` | Team executes Step 1 for 14 days, Step 2 for 7 days. | REQ-RWA-014 |
| `RWA-SCH-008` | Idempotency: Re-executing generate-schedule produces 0 duplicate map documents | POS | P0 | POST /generate-schedule executed twice consecutively | `200 OK` | Map count in MongoDB remains exactly identical. | REQ-RWA-013 |
| `RWA-SCH-009` | Edge Case: Generate schedule on rotation board with 0 assigned members | POS | P1 | POST /generate-schedule on empty board | `200 OK` | Completes cleanly; 0 maps written to WorkAssignmentMaps. | REQ-RWA-011 |
| `RWA-SCH-010` | Negative: Generate schedule on non-existent rotationId | NEG | P1 | POST /shift-rotations/{fakeId}/generate-schedule | `404 Not Found` | Rotation board not found error. | REQ-RWA-011 |
| `RWA-SCH-011` | Scoping Negative: Generate schedule without mandatory locationId | SEC | P0 | POST /generate-schedule without locationId query | `400 Bad Request` | Enforces mandatory location scoping. | REQ-RWA-003 |
| `RWA-SCH-012` | Overnight Shift Slots: 20:00 to 04:00 cross-midnight materialization | POS | P0 | Inspect daily shift slot records for night rotation | `200 OK` | Overnight slot correctly materializes across calendar midnight without date truncation. | REQ-RWA-012 |
| `RWA-SCH-013` | Rest Days Materialization: Days off have isWorkingDay: false and 0 work duration | POS | P1 | Inspect scheduled days off (Friday, Saturday) | `200 OK` | isWorkingDay marked false, totalWorkDurationInMinutes: 0. | REQ-RWA-012 |
| `RWA-SCH-014` | Policy Binding Assert: Embedded policies (Break, Overtime) attached to maps | POS | P1 | Inspect PolicyIds on daily materialized maps | `200 OK` | Policies defined on rotation plan attached to schedule instances. | REQ-RWA-012 |
| `RWA-SCH-015` | Generation Horizon: Verify GeneratedThrough timestamp covers 2 years (104 weeks) | POS | P1 | Inspect member GeneratedThrough date in ShiftRotationBoard | `200 OK` | GeneratedThrough matches standard 2-year rolling horizon. | REQ-RWA-011 |
| `RWA-SCH-016` | Future Start Date Horizon: Employee with future startDate shows empty prior maps | POS | P1 | startDate: +30 days | `200 OK` | 0 maps generated for dates prior to effective startDate. | REQ-RWA-011 |
| `RWA-SCH-017` | Bounded End Date Horizon: Employee with fixed endDate has 0 maps after endDate | POS | P1 | endDate: 2027-01-31 | `200 OK` | Maps materialize strictly up to 2027-01-31; 0 maps thereafter. | REQ-RWA-011 |
| `RWA-SCH-018` | Regeneration on Plan Update: Modifying rotation plan realigns future schedule maps | BUS | P1 | PATCH plan workTemplateId and regenerate schedule | `200 OK` | Future maps updated to reflect new shift timings. | REQ-RWA-011 |
| `RWA-SCH-019` | Regeneration on Team Move: Member moving to new team realigns schedule maps | BUS | P1 | Member moved from Team Alpha to Team Bravo | `200 OK` | Maps re-projected under Team Bravo cycle from effectiveFrom. | REQ-RWA-016 |
| `RWA-SCH-020` | Query Individual Schedule: GET /employees/{id}/schedule returns accurate timeline | POS | P0 | GET /schedule with 30-day date window | `200 OK` | Returns matching daily shift entries. | REQ-RWA-022 |
| `RWA-SCH-021` | Query Schedule Date Inversion: GET /schedule with from > to | BVA | P2 | GET /schedule?from=2026-12-31&to=2026-11-01 | `400 Bad Request` | Validation error: from date cannot be after to date. | REQ-RWA-022 |
| `RWA-SCH-022` | Performance & Throughput: Schedule generation for 48 members runs < 5s | POS | P2 | 48 employees x 104 weeks schedule generation | `200 OK` | Executes within latency budget. | REQ-RWA-011 |

---

### Suite 6: Member Period Modification & Date Resizing (PATCH .../members/{id})

| TC ID | Test Scenario | Category | Priority | Input / Preconditions | Expected HTTP | Expected Response / DB State | RTM Req |
| :--- | :--- | :---: | :---: | :--- | :---: | :--- | :---: |
| `RWA-PRD-001` | Positive: Extend member endDate to future date (2027-06-30) | POS | P0 | PATCH /members/{id} with extended endDate, adjustConflicts: true | `200 OK` | Member endDate updated; schedule maps generated through new endDate. | REQ-RWA-015 |
| `RWA-PRD-002` | Positive: Shorten member endDate (early termination of assignment) | POS | P1 | PATCH /members/{id} with earlier endDate | `200 OK` | Member endDate shortened; obsolete future maps pruned from MongoDB. | REQ-RWA-015 |
| `RWA-PRD-003` | Positive: Convert open-ended assignment (endDate: null) to fixed endDate | POS | P1 | Setting endDate: '2027-03-31' | `200 OK` | Assignment successfully bounded to fixed date. | REQ-RWA-015 |
| `RWA-PRD-004` | Positive: Convert fixed endDate to open-ended (endDate: null) | POS | P1 | Setting endDate: null | `200 OK` | Assignment converted back to open-ended tenure. | REQ-RWA-015 |
| `RWA-PRD-005` | Negative BVA: Update period with endDate < startDate | BVA | P0 | startDate: 2026-11-20, endDate: 2026-10-01 | `400 Bad Request` | Validation error: endDate cannot be before startDate. | REQ-RWA-015 |
| `RWA-PRD-006` | Conflict: Extending period overlaps with another assignment (adjustConflicts: false) | BUS | P0 | Extended range collides with regular plan, adjustConflicts: false | `400 Bad Request` | Conflict reported: Overlapping assignment detected. Requires adjustConflicts: true. | REQ-RWA-008, REQ-RWA-015 |
| `RWA-PRD-007` | Conflict: Extending period with adjustConflicts: true auto-resolves overlap | BUS | P0 | Extended range collides with regular plan, adjustConflicts: true | `200 OK` | Auto-adjusts colliding assignment and updates member period. | REQ-RWA-008, REQ-RWA-015 |
| `RWA-PRD-008` | Negative: Update non-existent membershipId | NEG | P1 | PATCH /members/{fakeGuid} | `404 Not Found` | Membership not found error. | REQ-RWA-015 |
| `RWA-PRD-009` | Negative DTO: Malformed membership GUID string | DTO | P2 | PATCH /members/invalid-guid | `400 Bad Request` | GUID format parsing error. | REQ-RWA-015 |
| `RWA-PRD-010` | Scoping Negative: Update member period without locationId | SEC | P0 | PATCH /members/{id} without locationId query | `400 Bad Request` | Enforces mandatory location scoping. | REQ-RWA-003 |
| `RWA-PRD-011` | Scoping Negative: locationId query mismatch with board location | SEC | P1 | locationId=Dammam while member is on Jeddah board | `400/404` | Mismatched location scoping rejected. | REQ-RWA-003 |
| `RWA-PRD-012` | Update startDate: Shift effective startDate forward (+14 days) | POS | P1 | startDate shifted from 2026-11-20 to 2026-12-04 | `200 OK` | startDate updated; obsolete maps before new startDate removed. | REQ-RWA-015 |
| `RWA-PRD-013` | Update startDate: Shift effective startDate backward (retroactive expansion) | POS | P1 | startDate shifted into past | `200 OK` | startDate updated; retroactive schedule maps generated. | REQ-RWA-015 |
| `RWA-PRD-014` | Inactive Member Edit: Attempt to update period of soft-deleted member | BUS | P1 | PATCH on member with IsActive: false | `400 Bad Request` | Validation error: Cannot modify period of an inactive member. | REQ-RWA-015 |
| `RWA-PRD-015` | Deleted Board Member Edit: Attempt to update member on deleted board | BUS | P1 | PATCH on member where board IsDeleted: true | `400 Bad Request` | Validation error: Cannot modify member on a deleted rotation board. | REQ-RWA-020 |
| `RWA-PRD-016` | MongoDB Document Assert: Verify ShiftRotationBoard.Members updated | POS | P0 | Query ShiftRotationBoard in MongoDB | `200 OK` | StartDate and EndDate properties updated in embedded member document. | REQ-RWA-015 |
| `RWA-PRD-017` | MongoDB Map Assert: Verify WorkAssignmentMaps pruned after shortened endDate | POS | P0 | Query maps where date > newEndDate | `200 OK` | Future maps deleted or marked inactive. | REQ-RWA-015 |
| `RWA-PRD-018` | Security: Update member period belonging to Company B | SEC | P0 | MembershipId from another company | `403 Forbidden` | Tenant isolation guard blocks foreign membership modification. | REQ-RWA-024 |
| `RWA-PRD-019` | Audit Field Assert: Verify ModifiedAt timestamp refreshed on board | POS | P2 | Inspect LastModificationTime on board | `200 OK` | Audit timestamp updated. | REQ-RWA-015 |
| `RWA-PRD-020` | Audit User Assert: Verify ModifiedBy identity logged | POS | P2 | Inspect LastModifierId on board | `200 OK` | Modifier identity accurately logged. | REQ-RWA-015 |

---

### Suite 7: Intra-Rotation Team Transfer (POST .../move-team)

| TC ID | Test Scenario | Category | Priority | Input / Preconditions | Expected HTTP | Expected Response / DB State | RTM Req |
| :--- | :--- | :---: | :---: | :--- | :---: | :--- | :---: |
| `RWA-MVT-001` | Positive: Move member from Team Alpha to Team Bravo with valid effectiveFrom | POS | P0 | POST /move-team with target teamId: Team Bravo, effectiveFrom: 2026-12-01 | `200 OK` | Member transferred to Team Bravo; schedule maps re-aligned from effectiveFrom. | REQ-RWA-016 |
| `RWA-MVT-002` | Positive: Immediate team transfer (effectiveFrom = today) | POS | P0 | effectiveFrom set to today's date | `200 OK` | Member transitions to new team immediately. | REQ-RWA-016 |
| `RWA-MVT-003` | Positive: Future team transfer (effectiveFrom = +30 days) | POS | P1 | effectiveFrom set to future date | `200 OK` | Member remains in current team until effective date, then transitions. | REQ-RWA-016 |
| `RWA-MVT-004` | Business Negative: Move member to the SAME team they are currently assigned to | BUS | P0 | teamId set to current assigned teamId | `400 Bad Request` | Validation error: Employee is already an active member of target team. | REQ-RWA-016 |
| `RWA-MVT-005` | Negative: Move to non-existent target teamId | NEG | P1 | teamId: 00000000-0000-0000-0000-000000000000 | `404 Not Found` | Target team not found in rotation board. | REQ-RWA-016 |
| `RWA-MVT-006` | Negative: Move member on non-existent rotationId | NEG | P1 | rotationId: fakeGuid | `404 Not Found` | Rotation board not found. | REQ-RWA-016 |
| `RWA-MVT-007` | Negative: Move non-existent membershipId | NEG | P1 | membershipId: fakeGuid | `404 Not Found` | Membership not found. | REQ-RWA-016 |
| `RWA-MVT-008` | Negative DTO: Missing teamId in move-team payload | DTO | P0 | teamId omitted or null | `400 Bad Request` | Validation error: teamId is required. | REQ-RWA-016 |
| `RWA-MVT-009` | Negative DTO: Missing effectiveFrom in move-team payload | DTO | P0 | effectiveFrom omitted or null | `400 Bad Request` | Validation error: effectiveFrom is required. | REQ-RWA-016 |
| `RWA-MVT-010` | Negative DTO: Invalid date format in effectiveFrom | DTO | P2 | effectiveFrom: 'invalid-date' | `400 Bad Request` | Date parsing error. | REQ-RWA-016 |
| `RWA-MVT-011` | Scoping Negative: Move team without mandatory locationId | SEC | P0 | POST /move-team without locationId query | `400 Bad Request` | Enforces mandatory location scoping. | REQ-RWA-003 |
| `RWA-MVT-012` | Inactive Member Move: Attempt to move an inactive/soft-deleted member | BUS | P1 | POST /move-team on member with IsActive: false | `400 Bad Request` | Validation error: Cannot transfer an inactive member. | REQ-RWA-016 |
| `RWA-MVT-013` | MongoDB Document Assert: Verify member TeamId updated in ShiftRotationBoard | POS | P0 | Query member record in MongoDB | `200 OK` | TeamId updated to target team GUID. | REQ-RWA-016 |
| `RWA-MVT-014` | MongoDB Map Assert: Verify operational maps switch to Team Bravo cycle | POS | P0 | Inspect maps after effectiveFrom | `200 OK` | Shift sequences reflect Team Bravo pattern from effectiveFrom. | REQ-RWA-016 |
| `RWA-MVT-015` | Historical Retention Assert: Prior maps before effectiveFrom retain Team Alpha pattern | POS | P1 | Inspect maps before effectiveFrom | `200 OK` | Historical Team Alpha shifts preserved without tampering. | REQ-RWA-016 |
| `RWA-MVT-016` | Security: Move member belonging to Company B | SEC | P0 | Cross-company membershipId move attempt | `403 Forbidden` | Tenant isolation guard blocks foreign member transfer. | REQ-RWA-024 |

---

### Suite 8: Inter-Board & Regular Work Plan Transfer (PATCH .../move)

| TC ID | Test Scenario | Category | Priority | Input / Preconditions | Expected HTTP | Expected Response / DB State | RTM Req |
| :--- | :--- | :---: | :---: | :--- | :---: | :--- | :---: |
| `RWA-MVB-001` | Positive: Preflight check for transferring member across rotation boards | POS | P0 | POST /move/check-conflicts with targetType: Rotation, targetRotationId, targetTeamId | `200 OK` | Returns conflict assessment for proposed cross-board transfer. | REQ-RWA-017 |
| `RWA-MVB-002` | Positive: Execute transfer across rotation boards (PATCH /move) | POS | P0 | PATCH /move with targetType: Rotation, targetRotationId, targetTeamId, effectiveFrom | `200 OK` | Transfers member to target rotation; original membership closed, new membership created. | REQ-RWA-017 |
| `RWA-MVB-003` | Positive: Preflight check for transferring member to Regular Work Plan | POS | P0 | POST /move/check-conflicts with targetType: WorkPlan, targetWorkPlanId | `200 OK` | Assesses conflicts with regular work plan. | REQ-RWA-017 |
| `RWA-MVB-004` | Positive: Execute transfer to Regular Work Plan (PATCH /move) | POS | P0 | PATCH /move with targetType: WorkPlan, targetWorkPlanId, effectiveFrom | `200 OK` | Transfers member from rotation to regular work assignment. | REQ-RWA-017 |
| `RWA-MVB-005` | Conflict Resolution: Transfer with overlapping assignment and adjustConflicts: true | BUS | P0 | Target plan has overlap, adjustConflicts: true | `200 OK` | Auto-resolves overlap and completes transfer. | REQ-RWA-008, REQ-RWA-017 |
| `RWA-MVB-006` | Conflict Rejection: Transfer with overlapping assignment and adjustConflicts: false | BUS | P0 | Target plan has overlap, adjustConflicts: false | `400 Bad Request` | Rejection: Conflict detected. Requires adjustConflicts: true. | REQ-RWA-008, REQ-RWA-017 |
| `RWA-MVB-007` | Negative DTO: Invalid targetType enum string | DTO | P1 | targetType: 'InvalidType' | `400 Bad Request` | Schema model binding rejection: Invalid MoveTargetType value. | REQ-RWA-017 |
| `RWA-MVB-008` | Negative DTO: targetType is Rotation but targetRotationId is missing | DTO | P0 | targetType: Rotation, targetRotationId: null | `400 Bad Request` | Validation error: targetRotationId is required when targetType is Rotation. | REQ-RWA-017 |
| `RWA-MVB-009` | Negative DTO: targetType is WorkPlan but targetWorkPlanId is missing | DTO | P0 | targetType: WorkPlan, targetWorkPlanId: null | `400 Bad Request` | Validation error: targetWorkPlanId is required when targetType is WorkPlan. | REQ-RWA-017 |
| `RWA-MVB-010` | Negative: Move referencing non-existent targetRotationId | NEG | P1 | targetRotationId: fakeGuid | `404 Not Found` | Target rotation board not found. | REQ-RWA-017 |
| `RWA-MVB-011` | Negative: Move referencing non-existent targetWorkPlanId | NEG | P1 | targetWorkPlanId: fakeGuid | `404 Not Found` | Target work plan not found. | REQ-RWA-017 |
| `RWA-MVB-012` | Cross-Location Guard: Attempt to move member to rotation board in ANOTHER location | SEC | P0 | targetRotationId is in Jeddah while member is in Dammam | `400 Bad Request` | Cross-location transfer blocked without formal employee location transfer. | REQ-RWA-004 |
| `RWA-MVB-013` | Cross-Location Guard: Attempt to move member to regular work plan in ANOTHER location | SEC | P0 | targetWorkPlanId is in Jeddah while member is in Dammam | `400 Bad Request` | Cross-location work plan transfer blocked. | REQ-RWA-004 |
| `RWA-MVB-014` | Scoping Negative: Move member without mandatory locationId | SEC | P0 | PATCH /move without locationId query | `400 Bad Request` | Enforces mandatory location scoping. | REQ-RWA-003 |
| `RWA-MVB-015` | MongoDB Source Assert: Verify source board membership marked closed | POS | P0 | Query source ShiftRotationBoard in MongoDB | `200 OK` | Source member EndDate set to effectiveFrom-1; IsActive: false if immediate. | REQ-RWA-017 |
| `RWA-MVB-016` | MongoDB Target Assert: Verify target board membership or regular map created | POS | P0 | Query target collection in MongoDB | `200 OK` | New active membership created in target board. | REQ-RWA-017 |
| `RWA-MVB-017` | Security: Move member belonging to Company B | SEC | P0 | Cross-company membershipId transfer attempt | `403 Forbidden` | Tenant isolation guard blocks access. | REQ-RWA-024 |
| `RWA-MVB-018` | Idempotency: Re-executing PATCH /move on already transferred member | BUS | P2 | Repeating move request | `400/404` | Validation error: Member has already been moved. | REQ-RWA-017 |

---

### Suite 9: Member Soft-Deletion & Assignment Removal (DELETE .../members/{id})

| TC ID | Test Scenario | Category | Priority | Input / Preconditions | Expected HTTP | Expected Response / DB State | RTM Req |
| :--- | :--- | :---: | :---: | :--- | :---: | :--- | :---: |
| `RWA-DEL-001` | Positive: Remove member from rotation with immediate endDate (endDate = today) | POS | P0 | DELETE /members/{id}?locationId=ValidLoc&endDate=Today | `200 OK` | Member immediately inactivated; future schedule maps purged. | REQ-RWA-018 |
| `RWA-DEL-002` | Positive: Remove member with scheduled future endDate (endDate = +14 days) | POS | P0 | DELETE /members/{id}?locationId=ValidLoc&endDate=+14days | `200 OK` | Member remains active until future endDate; maps after future endDate purged. | REQ-RWA-019 |
| `RWA-DEL-003` | Positive: Remove member with retroactive past endDate | POS | P1 | DELETE /members/{id}?endDate=-7days | `200 OK` | Member inactivated retroactively; obsolete maps pruned. | REQ-RWA-018 |
| `RWA-DEL-004` | Negative: Delete member with non-existent membershipId | NEG | P1 | DELETE /members/{fakeGuid} | `404 Not Found` | Membership not found error. | REQ-RWA-018 |
| `RWA-DEL-005` | Negative: Delete member on non-existent rotationId | NEG | P1 | DELETE /shift-rotations/{fakeId}/members/{id} | `404 Not Found` | Rotation board not found. | REQ-RWA-018 |
| `RWA-DEL-006` | Negative DTO: Malformed membership GUID string | DTO | P2 | DELETE /members/not-a-guid | `400 Bad Request` | GUID format parsing failure. | REQ-RWA-018 |
| `RWA-DEL-007` | Negative DTO: Invalid date format in endDate query parameter | DTO | P2 | endDate=2026-99-99 | `400 Bad Request` | Date parsing error. | REQ-RWA-018 |
| `RWA-DEL-008` | Scoping Negative: Delete member without mandatory locationId | SEC | P0 | DELETE /members/{id} without locationId query | `400 Bad Request` | Enforces mandatory location scoping. | REQ-RWA-003 |
| `RWA-DEL-009` | Scoping Negative: locationId does not match board location | SEC | P1 | locationId=Dammam while member is in Jeddah board | `400/404` | Mismatched location scoping rejected. | REQ-RWA-003 |
| `RWA-DEL-010` | Business Negative: Deleting member that is ALREADY inactive/deleted | BUS | P1 | DELETE /members/{id} on member where IsActive: false | `400/404` | Validation error: Member is already deleted. | REQ-RWA-018 |
| `RWA-DEL-011` | MongoDB Document Assert: Verify member has IsActive: false in ShiftRotationBoard | POS | P0 | Query ShiftRotationBoard in Sahab DB | `200 OK` | Member record updated: IsActive: false, EndDate populated. | REQ-RWA-018 |
| `RWA-DEL-012` | MongoDB Map Assert: Verify WorkAssignmentMaps after endDate are purged | POS | P0 | Query WorkAssignmentMaps where date > endDate | `200 OK` | Obsolete maps pruned from MongoDB. | REQ-RWA-018 |
| `RWA-DEL-013` | Historical Map Assert: Prior maps before endDate remain preserved for payroll | POS | P0 | Query WorkAssignmentMaps where date <= endDate | `200 OK` | Historical attendance shifts intact. | REQ-RWA-018 |
| `RWA-DEL-014` | Board Deletion Enablement: Board with all members removed can now be deleted | POS | P0 | DELETE /shift-rotations/{id} after all members deleted | `200 OK` | Board deletion succeeds once active member count reaches 0. | REQ-RWA-020 |
| `RWA-DEL-015` | Security: Delete member belonging to Company B | SEC | P0 | Cross-company membership deletion attempt | `403 Forbidden` | Tenant isolation guard blocks deletion. | REQ-RWA-024 |
| `RWA-DEL-016` | Audit Trail Assert: Verify DeletedAt and DeletedBy recorded on member removal | POS | P2 | Inspect audit fields in MongoDB member document | `200 OK` | Removal timestamp and user identity accurately logged. | REQ-RWA-018 |

---

### Suite 10: Roster, Member Querying & Projection Schedules (GET)

| TC ID | Test Scenario | Category | Priority | Input / Preconditions | Expected HTTP | Expected Response / DB State | RTM Req |
| :--- | :--- | :---: | :---: | :--- | :---: | :--- | :---: |
| `RWA-GET-001` | Positive: List rotation members with valid pagination (page=1, pageSize=20) | POS | P0 | GET /shift-rotations/{id}/employees?page=1&pageSize=20 | `200 OK` | Returns paginated array of assigned members with metadata. | REQ-RWA-021 |
| `RWA-GET-002` | Positive: Filter rotation members by teamId | POS | P1 | GET /shift-rotations/{id}/employees?teamId=ValidTeamId | `200 OK` | Returns only members belonging to specified team. | REQ-RWA-021 |
| `RWA-GET-003` | Positive: Filter rotation members by segment=Active | POS | P1 | GET /shift-rotations/{id}/employees?segment=Active | `200 OK` | Returns currently active members only. | REQ-RWA-021 |
| `RWA-GET-004` | Positive: Filter rotation members by segment=Inactive | POS | P1 | GET /shift-rotations/{id}/employees?segment=Inactive | `200 OK` | Returns terminated/soft-deleted members only. | REQ-RWA-021 |
| `RWA-GET-005` | Positive: Filter rotation members by asOf snapshot date | POS | P1 | GET /shift-rotations/{id}/employees?asOf=2026-11-20 | `200 OK` | Returns members active on specified snapshot date. | REQ-RWA-021 |
| `RWA-GET-006` | Negative BVA: Query members with page=0 or negative page number | BVA | P2 | GET /shift-rotations/{id}/employees?page=0 | `400 Bad Request` | Validation error: page must be >= 1. | REQ-RWA-021 |
| `RWA-GET-007` | Negative BVA: Query members with pageSize=0 or negative pageSize | BVA | P2 | GET /shift-rotations/{id}/employees?pageSize=0 | `400 Bad Request` | Validation error: pageSize must be >= 1. | REQ-RWA-021 |
| `RWA-GET-008` | Boundary BVA: Query members with max pageSize=100 | BVA | P2 | GET /shift-rotations/{id}/employees?pageSize=100 | `200 OK` | Upper boundary page size accepted. | REQ-RWA-021 |
| `RWA-GET-009` | Positive: Query individual projected schedule (GET /schedule) with date range | POS | P0 | GET /employees/{employeeId}/schedule?from=2026-11-20&to=2026-12-20 | `200 OK` | Returns daily shift instances for employee. | REQ-RWA-022 |
| `RWA-GET-010` | Negative: Query schedule for employee not assigned to rotation | NEG | P1 | GET /employees/{unassignedId}/schedule | `404 Not Found` | Employee not assigned to rotation board error. | REQ-RWA-022 |
| `RWA-GET-011` | Negative BVA: Query schedule with from > to (date inversion) | BVA | P1 | GET /employees/{id}/schedule?from=2026-12-31&to=2026-11-01 | `400 Bad Request` | Validation error: from date cannot be after to date. | REQ-RWA-022 |
| `RWA-GET-012` | Negative DTO: Query schedule with invalid date format | DTO | P2 | GET /schedule?from=invalid-date | `400 Bad Request` | Date parsing error. | REQ-RWA-022 |
| `RWA-GET-013` | Positive: Employee self-service rotation query (GET /me/rotation) | POS | P0 | GET /me/rotation as authenticated employee | `200 OK` | Returns current user's active rotation board and assigned team. | REQ-RWA-023 |
| `RWA-GET-014` | Positive: GET /me/rotation when user has NO active rotation | POS | P1 | GET /me/rotation for unassigned user | `200 OK` | Returns null / empty object cleanly. | REQ-RWA-023 |
| `RWA-GET-015` | Positive: Team roster attendance summary (GET /team/attendance/summary) | POS | P1 | GET /team/attendance/summary for supervisor | `200 OK` | Returns aggregated attendance summary for team rotation members. | REQ-RWA-021 |
| `RWA-GET-016` | Positive: Team roster work plans (GET /team/work-plans) | POS | P1 | GET /team/work-plans for supervisor | `200 OK` | Returns active work plans and rotation schedules for team. | REQ-RWA-021 |
| `RWA-GET-017` | Security: Query rotation members on board belonging to Company B | SEC | P0 | Cross-company rotationId in path | `403 Forbidden / 404` | Multi-tenancy isolation guard blocks foreign board query. | REQ-RWA-024 |
| `RWA-GET-018` | Security: Query individual schedule for employee in Company B | SEC | P0 | Cross-company employeeId in schedule query | `403 Forbidden / 404` | Tenant isolation guard blocks foreign schedule query. | REQ-RWA-024 |

---

## 4. Test Suite Execution & Coverage Dashboard

| Suite # | Suite Scope | Total TCs | P0 Critical | P1 Major | P2 Medium | Primary Endpoints Covered |
| :---: | :--- | :---: | :---: | :---: | :---: | :--- |
| **1** | Preflight Conflict Check Engine | 20 | 8 | 8 | 4 | `POST .../employees/check-conflicts` |
| **2** | Member Team Enrollment & Bulk Assignment | 26 | 12 | 10 | 4 | `POST .../teams/{teamId}/employees` |
| **3** | Critical Cross-Location Isolation Guards | 16 | 10 | 4 | 2 | Location Cross-Service Validation |
| **4** | Employee Lifecycle & Status Constraints | 18 | 8 | 7 | 3 | Inactive, Offboarded & Exited Guards |
| **5** | Schedule Materialization & Operational Maps | 22 | 8 | 11 | 3 | `POST .../generate-schedule`, `GET /schedule` |
| **6** | Member Period Modification & Date Resizing | 20 | 8 | 9 | 3 | `PATCH .../members/{membershipId}` |
| **7** | Intra-Rotation Team Transfer | 16 | 6 | 7 | 3 | `POST .../members/{id}/move-team` |
| **8** | Inter-Board & Regular Work Plan Transfer | 18 | 8 | 8 | 2 | `PATCH .../members/{id}/move` |
| **9** | Member Soft-Deletion & Assignment Removal | 16 | 7 | 6 | 3 | `DELETE .../members/{membershipId}` |
| **10** | Roster, Member Querying & Projection Schedules | 18 | 5 | 9 | 4 | `GET .../employees`, `GET /me/rotation` |
| **TOTAL** | **Master Rotation Work Assignment Suite** | **190** | **80** | **79** | **31** | **All 11 Assignment & Lifecycle Endpoints** |