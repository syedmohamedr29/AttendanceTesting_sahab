# Shift Rotation & Rotation Work Plan Test Specification (RTM, DTO Validations, Functional, Positive & Negative Invariants)

**Microservices:** `SP.AttendanceSvc` (.NET 9 / ASP.NET Core) & `SP.EmployeeSvc` (.NET 8)  
**Gateway Routes:** `https://gw8.dev.zoolwork.com/api/companies/{companyId}/shift-rotations` & `worktemplates/rotation`  
**Database Collections:** `Sahab.ERP.Attendance.ShiftRotationBoard`, `ERP.Attendance.WorkAssignmentMaps`, `ERP.Attendance.WorkTemplates`  
**Test Methodology:** Requirements Traceability Matrix (RTM), Equivalence Partitioning (EP), Boundary Value Analysis (BVA), Negative/Positive standalone, DTO Field Invariants, and MongoDB Document State Transitions  
**Total Test Scenarios:** 194 Scenarios across 8 Structured Suites  
**Author:** Antigravity Senior QA Automation & Microservice Specialist  

---

## 1. Executive Test Strategy & Architectural Blueprint

A **Shift Rotation Work Plan** is the cyclical scheduling engine of the Zoolwork attendance platform. It manages structured, recurring work schedules across one or more teams, alternating between day/night/swing shifts or working/rest periods according to mathematically defined cycles.

### 🔑 Architectural Foundations:
1. **The Three-Tier Hierarchy:**
   - **Rotation Header (`ERP.Attendance.ShiftRotationBoard`):** Top-level definition holding `RotationName`, `PatternType`, `WeeksPerStep`, `LocationId`, embedded `Plans[]`, `Teams[]`, and `Members[]`.
   - **Embedded Rotation Plans (`Plans[]`):** Each step in the rotation references a specific Work Plan with embedded Work Template and Policies (e.g. Plan 1 = 'Morning Shift', Plan 2 = 'Night Shift').
   - **Teams & Step Sequence (`Teams[]` & `Steps[]`):** Teams rotate through the `Steps` based on their `StartSequenceOrder`.
2. **Dual Representation in MongoDB:**
   - **Master Document:** Stored in `Sahab.ERP.Attendance.ShiftRotationBoard`.
   - **Materialized Operational Maps:** When members are assigned, schedule rows are materialized into `Sahab.ERP.Attendance.WorkAssignmentMaps` with `Source: "Rotation"`, `RotationId`, and `TeamId`.
3. **Pattern Types:**
   - **`Alternating` (Type 1):** Equal duration per step defined globally by `WeeksPerStep`.
   - **`Uneven` (Type 2):** Each step can define an independent `DurationWeeks`.

---

## 2. Requirements Traceability Matrix (RTM)

| Req ID | Business Requirement Description | Microservice Components | Scope & Enforcement |
| :---: | :--- | :--- | :--- |
| **REQ-ROT-001** | Shift Rotation Multilingual Naming | `ShiftRotationDto.RotationName` | Rotation must have localized names (en, ar) with min 1 and max 200 characters. |
| **REQ-ROT-002** | Mandatory Work Location Scoping | `ShiftRotationBoard.CompanyId/LocationId` | All rotation endpoints must enforce valid locationId query parameter belonging to company. |
| **REQ-ROT-003** | Pattern Type Invariants | `RotationPatternType Enum` | PatternType must be 'Alternating' or 'Uneven'. 'NotApplicable' or invalid strings rejected. |
| **REQ-ROT-004** | Alternating Weeks Per Step Boundary | `ShiftRotationDto.WeeksPerStep` | For Alternating pattern, weeksPerStep must be integer between 1 and 52 inclusive. |
| **REQ-ROT-005** | Uneven Duration Weeks Boundary | `RotationStepDto.DurationWeeks` | For Uneven pattern, each step durationWeeks must be positive integer >= 1. |
| **REQ-ROT-006** | Embedded Rotation Plans Integrity | `RotationPlanDto` | Rotation must declare >= 1 Plan. Each plan must have unique planIndex >= 1 and valid workTemplateId. |
| **REQ-ROT-007** | Rotation Template Compatibility | `WorkTemplateType Enforcement` | WorkTemplate assigned to a rotation plan must be of type Fixed or Rotation. Flexi rejected. |
| **REQ-ROT-008** | Rotation Step Sequence Integrity | `RotationStepDto.PlanIndex` | Steps array must reference valid planIndex. Step order defines cyclical execution. |
| **REQ-ROT-009** | Rotation Teams Uniqueness & Sequences | `RotationTeamDto` | Teams must have unique names and distinct startSequenceOrder values mapped to valid steps. |
| **REQ-ROT-010** | Preflight Conflict Detection Engine | `check-conflicts Endpoint` | Preflight endpoint must detect date overlaps, cross-plan, and cross-team conflicts without mutating DB. |
| **REQ-ROT-011** | Employee Lifecycle & Location Isolation | `Employee Location Guard` | Only active employees belonging to the specified Work Location can be assigned to rotation teams. |
| **REQ-ROT-012** | Cross-Location Assignment Guard | `Location Cross-Tenant Guard` | Employees from another work location (e.g. Dammam) must be rejected when assigned to Jeddah rotation. |
| **REQ-ROT-013** | Inactive / Offboarded Employee Rejection | `Employee Status Guard` | Inactive, offboarded, or exited employees must be rejected during assignment. |
| **REQ-ROT-014** | Date Range & Open-Ended Assignment | `AddRotationEmployeesDto` | Rotation assignment supports open-ended (null endDate) or fixed period. EndDate >= StartDate. |
| **REQ-ROT-015** | Schedule Materialization Engine | `WorkAssignmentMaps Sync` | generate-schedule must materialize cyclic shift instances into ERP.Attendance.WorkAssignmentMaps. |
| **REQ-ROT-016** | Rotation Member Period Modification | `EditRotationMemberPeriodDto` | Member startDate/endDate can be adjusted with conflict check and map truncation. |
| **REQ-ROT-017** | Team Transfer Within Rotation | `MoveRotationMemberTeamDto` | Member can move between teams in same rotation; schedule maps regenerate from effectiveFrom. |
| **REQ-ROT-018** | Cross-Rotation & Cross-Plan Transfer | `MoveEmployeeDto` | Member can move to another rotation or regular work plan with preflight validation. |
| **REQ-ROT-019** | Rotation Member Soft-Deletion | `DELETE /members/{id}` | Removing a member sets IsActive=false and truncates WorkAssignmentMaps from endDate. |
| **REQ-ROT-020** | Rotation Board Deletion Guard | `DELETE /shift-rotations/{id}` | Rotation board cannot be deleted if active members exist. Empty board is soft-deleted. |
| **REQ-ROT-021** | Rotation Work Template CRUD & Slots | `RotationWorkTemplateDto` | Rotation work templates support day-of-week slots, overnight cross-midnight shifts, and duration sums. |
| **REQ-ROT-022** | Multi-Tenant Company Isolation | `Tenant Security Guard` | Cross-tenant access via companyId or locationId tampering must return 403 Forbidden. |

---

## 3. Comprehensive Test Suites (194 Test Scenarios)

### Suite 1: Shift Rotation Creation (POST /shift-rotations, POST /preview)

| TC ID | Test Scenario | Category | Priority | Input / Preconditions | Expected HTTP | Expected Response / DB State | RTM Req |
| :--- | :--- | :---: | :---: | :--- | :---: | :--- | :---: |
| `ROT-CRT-001` | Positive: Create Alternating Rotation with 2 Plans, 2 Teams, 1 Week/Step | POS | P0 | Valid companyId, locationId, patternType: Alternating, weeksPerStep: 1, 2 Plans, 2 Teams | `200 OK` | Document created in ERP.Attendance.ShiftRotationBoard with IsDeleted: false. | REQ-ROT-001, REQ-ROT-004 |
| `ROT-CRT-002` | Positive: Create Uneven Rotation with custom durationWeeks per Step | POS | P0 | Valid companyId, locationId, patternType: Uneven, Step 1=2 wks, Step 2=1 wk, Step 3=3 wks | `200 OK` | Persisted with uneven step durations in ShiftRotationBoard. | REQ-ROT-003, REQ-ROT-005 |
| `ROT-CRT-003` | Positive: Multilingual Name (en and ar) | POS | P1 | rotationName: {'en': 'Factory Rotation', 'ar': 'دوران المصنع'} | `200 OK` | Multilingual names preserved in database without escaping/encoding issues. | REQ-ROT-001 |
| `ROT-CRT-004` | Positive: Rotation with embedded policies (Break, Overtime, Grace) | POS | P1 | Plans define isBreakPolicyEnabled: true, isOvertimePolicyEnabled: true, policyIds populated | `200 OK` | Plan policies stored correctly in embedded Plans array. | REQ-ROT-006 |
| `ROT-CRT-005` | Positive: Preview endpoint generates rotational grid projection without persisting | POS | P0 | POST /shift-rotations/preview with valid ShiftRotationDto payload | `200 OK` | Returns projected matrix grid; no document written to ShiftRotationBoard. | REQ-ROT-003 |
| `ROT-CRT-006` | Positive: Preview endpoint with cycles=4 query parameter | POS | P1 | POST /shift-rotations/preview?cycles=4 | `200 OK` | Matrix grid projects exactly 4 complete cycles. | REQ-ROT-003 |
| `ROT-CRT-007` | Positive BVA: Minimum cycle duration weeksPerStep = 1 | BVA | P1 | patternType: Alternating, weeksPerStep: 1 | `200 OK` | Lower boundary accepted cleanly. | REQ-ROT-004 |
| `ROT-CRT-008` | Positive BVA: Maximum annual cycle duration weeksPerStep = 52 | BVA | P1 | patternType: Alternating, weeksPerStep: 52 | `200 OK` | Upper boundary accepted cleanly. | REQ-ROT-004 |
| `ROT-CRT-009` | Negative DTO: Missing rotationName object entirely | DTO | P0 | rotationName: null or omitted from payload | `400 Bad Request` | Validation error: Cit.Attendance:Validation / Rotation name is required. | REQ-ROT-001 |
| `ROT-CRT-010` | Negative DTO: Empty string for English rotation name | DTO | P1 | rotationName: {'en': '', 'ar': 'دوران'} | `400 Bad Request` | Validation error: Rotation English name cannot be empty. | REQ-ROT-001 |
| `ROT-CRT-011` | Negative BVA: English rotation name exceeding 200 characters | BVA | P2 | rotationName: {'en': 'A'*201, 'ar': 'دوران'} | `400 Bad Request` | Validation error: Rotation name exceeds maximum length 200. | REQ-ROT-001 |
| `ROT-CRT-012` | Negative DTO: Invalid patternType enum string | DTO | P1 | patternType: 'Random' | `400 Bad Request` | Schema model binding rejection: Invalid RotationPatternType value. | REQ-ROT-003 |
| `ROT-CRT-013` | Negative DTO: patternType set to enum value NotApplicable | DTO | P1 | patternType: 'NotApplicable' | `400 Bad Request` | Validation error: Pattern type must be Alternating or Uneven. | REQ-ROT-003 |
| `ROT-CRT-014` | Negative BVA: weeksPerStep = 0 on Alternating pattern | BVA | P1 | patternType: Alternating, weeksPerStep: 0 | `400 Bad Request` | Validation error: weeksPerStep must be greater than or equal to 1. | REQ-ROT-004 |
| `ROT-CRT-015` | Negative BVA: weeksPerStep = -1 (negative integer) | BVA | P1 | patternType: Alternating, weeksPerStep: -1 | `400 Bad Request` | Validation error: Negative cycle weeks rejected. | REQ-ROT-004 |
| `ROT-CRT-016` | Negative BVA: weeksPerStep = 53 (overflow annual cycle) | BVA | P2 | patternType: Alternating, weeksPerStep: 53 | `400 Bad Request` | Validation error: weeksPerStep cannot exceed 52 weeks. | REQ-ROT-004 |
| `ROT-CRT-017` | Negative DTO: Floating point number for weeksPerStep = 1.5 | DTO | P2 | patternType: Alternating, weeksPerStep: 1.5 | `400 Bad Request` | JSON deserialization failure: Expected integer for weeksPerStep. | REQ-ROT-004 |
| `ROT-CRT-018` | Negative DTO: Empty plans array | DTO | P0 | plans: [] or omitted | `400 Bad Request` | Validation error: At least one rotation plan must be defined. | REQ-ROT-006 |
| `ROT-CRT-019` | Negative DTO: Null plans property | DTO | P1 | plans: null | `400 Bad Request` | Validation error: Plans list cannot be null. | REQ-ROT-006 |
| `ROT-CRT-020` | Negative DTO: Empty teams array | DTO | P0 | teams: [] or omitted | `400 Bad Request` | Validation error: At least one team must be defined. | REQ-ROT-009 |
| `ROT-CRT-021` | Negative DTO: Empty steps array | DTO | P0 | steps: [] or omitted | `400 Bad Request` | Validation error: At least one step must be defined. | REQ-ROT-008 |
| `ROT-CRT-022` | Business Negative: planIndex referenced in steps does not exist in plans | BUS | P0 | plans: [planIndex: 1], steps: [planIndex: 2] | `400 Bad Request` | Integrity error: Step references undeclared planIndex 2. | REQ-ROT-008 |
| `ROT-CRT-023` | Business Negative: Duplicate planIndex declared in plans array | BUS | P1 | plans: [planIndex: 1, planIndex: 1] | `400 Bad Request` | Integrity error: Duplicate planIndex 1 in plans array. | REQ-ROT-006 |
| `ROT-CRT-024` | Business Negative: Duplicate startSequenceOrder across teams | BUS | P1 | teams: [Team A order: 1, Team B order: 1] | `400 Bad Request` | Integrity error: Duplicate startSequenceOrder across teams. | REQ-ROT-009 |
| `ROT-CRT-025` | Business Negative: Team startSequenceOrder exceeds total steps count | BUS | P1 | steps count = 2, team startSequenceOrder = 3 | `400 Bad Request` | Validation error: startSequenceOrder exceeds total steps in rotation. | REQ-ROT-009 |
| `ROT-CRT-026` | Business Negative: Team startSequenceOrder = 0 or negative integer | BVA | P1 | teams: [Team A order: 0] | `400 Bad Request` | Validation error: startSequenceOrder must be >= 1. | REQ-ROT-009 |
| `ROT-CRT-027` | Business Negative: Non-existent workTemplateId GUID | BUS | P1 | workTemplateId: 00000000-0000-0000-0000-000000000000 | `400 Bad Request` | Validation error: Referenced work template does not exist. | REQ-ROT-006 |
| `ROT-CRT-028` | Business Negative: Using Flexible template in rotation plan | BUS | P1 | workTemplateId referencing template with templateType: Flexi | `400 Bad Request` | Validation error: Only Fixed or Rotation templates permitted in rotation plans. | REQ-ROT-007 |
| `ROT-CRT-029` | Scoping Negative: Missing mandatory locationId query parameter | SEC | P0 | POST /shift-rotations without locationId query | `400 Bad Request` | Scoping error: locationId is required. | REQ-ROT-002 |
| `ROT-CRT-030` | Security Negative: Cross-tenant companyId tampering in path vs auth token | SEC | P0 | Path companyId != token companyId | `403 Forbidden` | Multi-tenancy isolation guard blocks access. | REQ-ROT-022 |

---

### Suite 2: Shift Rotation Query Endpoints (GET)

| TC ID | Test Scenario | Category | Priority | Input / Preconditions | Expected HTTP | Expected Response / DB State | RTM Req |
| :--- | :--- | :---: | :---: | :--- | :---: | :--- | :---: |
| `ROT-GET-001` | Positive: List shift rotations for location with multiple boards | POS | P0 | GET /shift-rotations?locationId=ValidLoc | `200 OK` | Array of shift rotations with embedded plans, teams, steps returned. | REQ-ROT-002 |
| `ROT-GET-002` | Positive: List shift rotations for clean location with 0 boards | POS | P1 | GET /shift-rotations?locationId=EmptyLoc | `200 OK` | Returns empty array [] (not 404). | REQ-ROT-002 |
| `ROT-GET-003` | Negative: Missing mandatory locationId query parameter on GET list | NEG | P1 | GET /shift-rotations without locationId | `400 Bad Request` | Enforces mandatory location scoping. | REQ-ROT-002 |
| `ROT-GET-004` | Positive: Get single shift rotation by valid rotationId | POS | P0 | GET /shift-rotations/{rotationId} | `200 OK` | Returns full board document matching MongoDB state. | REQ-ROT-002 |
| `ROT-GET-005` | Negative: Get rotation by non-existent rotationId | NEG | P1 | GET /shift-rotations/{randomGuid} | `404 Not Found` | Clean 404 response. | REQ-ROT-002 |
| `ROT-GET-006` | Negative DTO: Get rotation with malformed GUID string | DTO | P2 | GET /shift-rotations/not-a-guid | `400 Bad Request` | GUID format parsing error. | REQ-ROT-002 |
| `ROT-GET-007` | Security: Get rotation belonging to another company | SEC | P0 | rotationId from Company B queried under Company A | `403/404` | Cross-company tenant isolation enforced. | REQ-ROT-022 |
| `ROT-GET-008` | Positive: Query rotation-grid with valid date range (from and to) | POS | P0 | GET /shift-rotations/{id}/rotation-grid?from=2026-11-01&to=2026-12-31 | `200 OK` | Returns weekly matrix of teams vs assigned plans. | REQ-ROT-002 |
| `ROT-GET-009` | Positive: Query rotation-grid with cycles=3 parameter | POS | P1 | GET /shift-rotations/{id}/rotation-grid?cycles=3 | `200 OK` | Matrix projected across exactly 3 complete cycles. | REQ-ROT-003 |
| `ROT-GET-010` | Negative BVA: Query rotation-grid with from > to | BVA | P1 | GET /rotation-grid?from=2026-12-31&to=2026-11-01 | `400 Bad Request` | Validation error: 'from' date cannot be after 'to' date. | REQ-ROT-002 |
| `ROT-GET-011` | Negative DTO: Query rotation-grid with invalid date format | DTO | P2 | GET /rotation-grid?from=invalid-date | `400 Bad Request` | Date parsing error. | REQ-ROT-002 |
| `ROT-GET-012` | Negative BVA: Query rotation-grid with negative cycles=-1 | BVA | P2 | GET /rotation-grid?cycles=-1 | `400 Bad Request` | Validation error: cycles must be >= 1. | REQ-ROT-003 |
| `ROT-GET-013` | Negative BVA: Query rotation-grid with cycles=0 | BVA | P2 | GET /rotation-grid?cycles=0 | `400 Bad Request` | Validation error: cycles must be >= 1. | REQ-ROT-003 |
| `ROT-GET-014` | Positive: List rotation members with valid pagination (page=1, pageSize=20) | POS | P0 | GET /shift-rotations/{id}/employees?page=1&pageSize=20 | `200 OK` | Paginated list of assigned members with metadata. | REQ-ROT-011 |
| `ROT-GET-015` | Positive: List rotation members filtered by teamId | POS | P1 | GET /shift-rotations/{id}/employees?teamId=ValidTeamId | `200 OK` | Returns only members belonging to specified team. | REQ-ROT-009 |
| `ROT-GET-016` | Positive: List rotation members filtered by segment=Active | POS | P1 | GET /shift-rotations/{id}/employees?segment=Active | `200 OK` | Returns currently active members only. | REQ-ROT-011 |
| `ROT-GET-017` | Positive: List rotation members filtered by asOf date snapshot | POS | P1 | GET /shift-rotations/{id}/employees?asOf=2026-11-15 | `200 OK` | Returns members active on specified snapshot date. | REQ-ROT-011 |
| `ROT-GET-018` | Negative BVA: List rotation members with page=0 or negative page | BVA | P2 | GET /shift-rotations/{id}/employees?page=0 | `400 Bad Request` | Validation error: page must be >= 1. | REQ-ROT-011 |
| `ROT-GET-019` | Positive: Get individual employee projected schedule | POS | P0 | GET /shift-rotations/{id}/employees/{employeeId}/schedule?from=2026-11-01&to=2026-12-31 | `200 OK` | Projected shift timeline for specific employee. | REQ-ROT-015 |
| `ROT-GET-020` | Negative: Get schedule for employee not assigned to rotation | NEG | P1 | GET /shift-rotations/{id}/employees/{unassignedEmpId}/schedule | `404 Not Found` | Employee not assigned to rotation board. | REQ-ROT-015 |
| `ROT-GET-021` | Positive: Get personal rotation (GET /me/rotation) for authenticated employee | POS | P1 | GET /me/rotation as authenticated user | `200 OK` | Returns current employee's assigned rotation board. | REQ-ROT-011 |
| `ROT-GET-022` | Positive: Get personal rotation when user has no active rotation | POS | P2 | GET /me/rotation for unassigned user | `200 OK` | Returns null / empty object. | REQ-ROT-011 |

---

### Suite 3: Shift Rotation Update & Mutation (PATCH)

| TC ID | Test Scenario | Category | Priority | Input / Preconditions | Expected HTTP | Expected Response / DB State | RTM Req |
| :--- | :--- | :---: | :---: | :--- | :---: | :--- | :---: |
| `ROT-PAT-001` | Positive: Partial update - Rename rotation board | POS | P0 | PATCH /shift-rotations/{id} with updated rotationName | `200 OK` | Rotation board name updated in MongoDB. | REQ-ROT-001 |
| `ROT-PAT-002` | Positive: Add new plan to existing rotation | POS | P0 | PATCH /shift-rotations/{id} with new plan in plans array | `200 OK` | New plan appended with unique planIndex. | REQ-ROT-006 |
| `ROT-PAT-003` | Positive: Update workTemplateId in existing plan | POS | P1 | PATCH /shift-rotations/{id} with modified workTemplateId | `200 OK` | Plan template reference updated. | REQ-ROT-006 |
| `ROT-PAT-004` | Positive: Remove unassigned plan via removedPlanIds | POS | P1 | PATCH /shift-rotations/{id} with removedPlanIds: [planId] | `200 OK` | Plan removed from board. | REQ-ROT-006 |
| `ROT-PAT-005` | Business Negative: Attempt to remove plan currently active with members | BUS | P0 | PATCH /shift-rotations/{id} removing active planId | `400 Bad Request` | Business block: Cannot remove plan with active member assignments. | REQ-ROT-006 |
| `ROT-PAT-006` | Positive: Add new team to existing rotation | POS | P1 | PATCH /shift-rotations/{id} with new team in teams array | `200 OK` | New team added with valid startSequenceOrder. | REQ-ROT-009 |
| `ROT-PAT-007` | Positive: Update team name (en and ar) | POS | P1 | PATCH /shift-rotations/{id} with modified teamName | `200 OK` | Team name updated. | REQ-ROT-009 |
| `ROT-PAT-008` | Positive: Update team startSequenceOrder | POS | P1 | PATCH /shift-rotations/{id} realigning team startSequenceOrder | `200 OK` | Team rotational starting point updated. | REQ-ROT-009 |
| `ROT-PAT-009` | Positive: Update steps sequence order and step counts | POS | P1 | PATCH /shift-rotations/{id} with reordered steps array | `200 OK` | Rotational steps updated. | REQ-ROT-008 |
| `ROT-PAT-010` | Positive: Convert pattern from Alternating to Uneven | POS | P1 | patternType: Uneven with durationWeeks on steps | `200 OK` | Pattern converted to uneven durations. | REQ-ROT-003 |
| `ROT-PAT-011` | Positive: Convert pattern from Uneven to Alternating | POS | P1 | patternType: Alternating with global weeksPerStep | `200 OK` | Pattern converted to alternating duration. | REQ-ROT-003 |
| `ROT-PAT-012` | Positive BVA: Update weeksPerStep to upper boundary 52 | BVA | P2 | weeksPerStep: 52 | `200 OK` | Updated to 52 weeks successfully. | REQ-ROT-004 |
| `ROT-PAT-013` | Negative BVA: Update weeksPerStep to 0 or negative integer | BVA | P1 | weeksPerStep: 0 | `400 Bad Request` | Validation error: weeksPerStep must be >= 1. | REQ-ROT-004 |
| `ROT-PAT-014` | Negative BVA: Update weeksPerStep to 53 (overflow) | BVA | P2 | weeksPerStep: 53 | `400 Bad Request` | Validation error: weeksPerStep cannot exceed 52. | REQ-ROT-004 |
| `ROT-PAT-015` | Negative DTO: Update with empty steps array | DTO | P1 | steps: [] | `400 Bad Request` | Validation error: steps cannot be empty. | REQ-ROT-008 |
| `ROT-PAT-016` | Negative DTO: Update with empty teams array | DTO | P1 | teams: [] | `400 Bad Request` | Validation error: teams cannot be empty. | REQ-ROT-009 |
| `ROT-PAT-017` | Business Negative: Update steps referencing non-existent planIndex | BUS | P0 | steps reference planIndex 99 not in plans | `400 Bad Request` | Integrity error: Referenced planIndex not found. | REQ-ROT-008 |
| `ROT-PAT-018` | Business Negative: Duplicate startSequenceOrder across teams in update | BUS | P1 | teams have duplicate sequence orders | `400 Bad Request` | Validation error: Team sequence orders must be unique. | REQ-ROT-009 |
| `ROT-PAT-019` | Negative: Update rotation using non-existent rotationId | NEG | P1 | PATCH /shift-rotations/{randomGuid} | `404 Not Found` | Clean 404 response. | REQ-ROT-002 |
| `ROT-PAT-020` | Negative DTO: Update rotation with malformed GUID | DTO | P2 | PATCH /shift-rotations/bad-id | `400 Bad Request` | GUID format parsing failure. | REQ-ROT-002 |
| `ROT-PAT-021` | Scoping Negative: Update rotation without mandatory locationId | SEC | P0 | PATCH /shift-rotations/{id} without locationId | `400 Bad Request` | Mandatory location scoping enforced. | REQ-ROT-002 |
| `ROT-PAT-022` | Security Negative: Update rotation belonging to another tenant/company | SEC | P0 | Cross-company rotationId mutation attempt | `403 Forbidden` | Multi-tenancy isolation guard blocks access. | REQ-ROT-022 |
| `ROT-PAT-023` | Business: Update rotation with active schedules triggers map sync | BUS | P2 | PATCH rotation that has generated schedules | `200 OK` | Updates board and flags schedules for regeneration. | REQ-ROT-002 |
| `ROT-PAT-024` | MongoDB Assert: Verify ShiftRotationBoard document and UpdatedAt timestamp | POS | P0 | Query MongoDB document after PATCH | `200 OK` | Document properties updated and UpdatedAt refreshed. | REQ-ROT-002 |

---

### Suite 4: Team Assignment & Preflight Conflict Detection

| TC ID | Test Scenario | Category | Priority | Input / Preconditions | Expected HTTP | Expected Response / DB State | RTM Req |
| :--- | :--- | :---: | :---: | :--- | :---: | :--- | :---: |
| `ROT-CHK-001` | Positive: Preflight check for clean active employee returns no conflicts | POS | P0 | POST /check-conflicts with clean employeeId | `200 OK` | Returns hasConflicts: false, conflicts: []. | REQ-ROT-010 |
| `ROT-CHK-002` | Positive: Assign single active employee to Team A with open-ended period | POS | P0 | POST /employees with employeeId, startDate: 2026-11-15, endDate: null | `200 OK` | Member added to Team A in ShiftRotationBoard. | REQ-ROT-011, REQ-ROT-014 |
| `ROT-CHK-003` | Positive: Assign multiple active employees in bulk (5 employees) | POS | P0 | POST /employees with 5 valid employeeIds | `200 OK` | All 5 members assigned in single atomic transaction. | REQ-ROT-011 |
| `ROT-CHK-004` | Positive: Assign employee with fixed date range (startDate to endDate) | POS | P1 | startDate: 2026-12-01, endDate: 2027-03-31 | `200 OK` | Member record persisted with bounded period. | REQ-ROT-014 |
| `ROT-CHK-005` | Negative DTO: Missing employeeIds array | DTO | P0 | employeeIds: null or omitted | `400 Bad Request` | Validation error: employeeIds array is required. | REQ-ROT-011 |
| `ROT-CHK-006` | Negative DTO: Empty employeeIds array | DTO | P1 | employeeIds: [] | `400 Bad Request` | Validation error: At least one employeeId required. | REQ-ROT-011 |
| `ROT-CHK-007` | Negative DTO: Missing startDate in payload | DTO | P0 | startDate omitted or null | `400 Bad Request` | Validation error: startDate is required. | REQ-ROT-014 |
| `ROT-CHK-008` | Negative DTO: Invalid date format in startDate | DTO | P2 | startDate: 'not-a-date' | `400 Bad Request` | Date parsing error. | REQ-ROT-014 |
| `ROT-CHK-009` | Negative BVA: endDate < startDate (end date before start date) | BVA | P0 | startDate: 2026-12-01, endDate: 2026-11-01 | `400 Bad Request` | Validation error: endDate cannot be earlier than startDate. | REQ-ROT-014 |
| `ROT-CHK-010` | Boundary: endDate == startDate (single-day assignment) | BVA | P2 | startDate: 2026-12-01, endDate: 2026-12-01 | `200 OK` | Single day assignment boundary accepted. | REQ-ROT-014 |
| `ROT-CHK-011` | Business Negative: Assign employee already actively assigned to SAME team | BUS | P0 | Assigning active member to same team again | `400 Bad Request` | Conflict detected: Employee already active in this team. | REQ-ROT-010 |
| `ROT-CHK-012` | Business Negative: Assign employee already in ANOTHER team in SAME rotation | BUS | P0 | Assigning Team A member to Team B directly | `400 Bad Request` | Conflict detected: Employee already assigned to another team in rotation. | REQ-ROT-010 |
| `ROT-CHK-013` | Business Negative: Assign employee with active REGULAR work plan (adjustConflicts: false) | BUS | P0 | adjustConflicts: false with overlapping regular plan | `400 Bad Request` | Conflict reported: Overlapping active work assignment exists. | REQ-ROT-010 |
| `ROT-CHK-014` | Positive Business: Assign employee with overlapping plan (adjustConflicts: true) | BUS | P0 | adjustConflicts: true with overlapping regular plan | `200 OK` | Auto-resolves conflict by adjusting existing assignment end date. | REQ-ROT-010 |
| `ROT-CHK-015` | CRITICAL GUARD: Cross-Location Block (Dammam Employee -> Jeddah Rotation) | SEC | P0 | Assign SA-EMP-0001 (Dammam) to Jeddah rotation board | `400 Bad Request` | Security/Location Guard: Employee does not belong to rotation work location. | REQ-ROT-012 |
| `ROT-CHK-016` | CRITICAL GUARD: Preflight conflict check detects cross-location mismatch | SEC | P0 | POST /check-conflicts for Dammam employee on Jeddah board | `200 OK (Conflicts)` | Returns hasConflicts: true with location mismatch conflict details. | REQ-ROT-012 |
| `ROT-CHK-017` | CRITICAL GUARD: Inactive employee (IsActive: false) MUST be rejected | BUS | P0 | Assign inactive employee SA-EMP-0006 | `400 Bad Request` | Validation error: Inactive employee cannot be assigned to rotation. | REQ-ROT-013 |
| `ROT-CHK-018` | Business Negative: Assign offboarded/exited employee (Status: 3) | BUS | P0 | Assign employee in offboarded state | `400 Bad Request` | Validation error: Offboarded employee cannot be assigned. | REQ-ROT-013 |
| `ROT-CHK-019` | Business Negative: Assign non-existent employee GUID | NEG | P1 | employeeIds: [00000000-0000-0000-0000-000000000000] | `404/400` | Employee not found error. | REQ-ROT-011 |
| `ROT-CHK-020` | Business Negative: Duplicate employee GUIDs in employeeIds array | DTO | P2 | employeeIds: [EmpA, EmpA] | `200 OK` | Deduplicates array and assigns employee once. | REQ-ROT-011 |
| `ROT-CHK-021` | Negative: Assign to non-existent teamId | NEG | P1 | POST /teams/{fakeTeamId}/employees | `404 Not Found` | Team not found in rotation board. | REQ-ROT-009 |
| `ROT-CHK-022` | Negative: Assign to non-existent rotationId | NEG | P1 | POST /shift-rotations/{fakeId}/teams/{teamId}/employees | `404 Not Found` | Rotation board not found. | REQ-ROT-002 |
| `ROT-CHK-023` | Scoping Negative: Assign employees without mandatory locationId query parameter | SEC | P0 | POST /teams/{teamId}/employees without locationId | `400 Bad Request` | Mandatory location scoping enforced. | REQ-ROT-002 |
| `ROT-CHK-024` | Scoping Negative: locationId does not match rotation board location | SEC | P1 | locationId=Dammam while rotation board is Jeddah | `400/404` | Mismatched location scoping rejected. | REQ-ROT-002 |
| `ROT-CHK-025` | Preflight Check: excludeMembershipId query ignores current membership | POS | P1 | POST /check-conflicts?excludeMembershipId=CurrentId | `200 OK` | Returns hasConflicts: false ignoring self-conflict. | REQ-ROT-010 |
| `ROT-CHK-026` | Preflight Check: Mixed batch (1 clean employee, 1 conflicting employee) | BUS | P1 | POST /check-conflicts with [CleanEmp, ConflictingEmp] | `200 OK` | Returns hasConflicts: true with itemized conflict per employee. | REQ-ROT-010 |
| `ROT-CHK-027` | High-Volume Load: Bulk assignment of 48 active employees simultaneously | POS | P1 | Assigning all 48 company employees to Team A | `200 OK` | Bulk assignment completes within performance threshold. | REQ-ROT-011 |
| `ROT-CHK-028` | Effective Date: Retroactive assignment (startDate in past) | POS | P1 | startDate: 30 days prior to today | `200 OK` | Creates member with past effective date for historical tracking. | REQ-ROT-014 |
| `ROT-CHK-029` | Effective Date: Future assignment (startDate in future) | POS | P1 | startDate: 60 days in future | `200 OK` | Creates member in pending state until effective date arrives. | REQ-ROT-014 |
| `ROT-CHK-030` | MongoDB Assert: Verify member appended to Members array in ShiftRotationBoard | POS | P0 | Query ShiftRotationBoard in Sahab database | `200 OK` | Members array contains new member document. | REQ-ROT-011 |
| `ROT-CHK-031` | MongoDB Assert: Verify member fields (MembershipId, EmployeeId, TeamId, StartDate) | POS | P0 | Inspect embedded member document fields | `200 OK` | All fields correctly mapped with IsActive: true. | REQ-ROT-011 |
| `ROT-CHK-032` | Security: Assign employee belonging to Company B into Company A rotation | SEC | P0 | Cross-company employeeId in payload | `403/400` | Tenant isolation guard blocks foreign employee assignment. | REQ-ROT-022 |

---

### Suite 5: Schedule Materialization & Generation

| TC ID | Test Scenario | Category | Priority | Input / Preconditions | Expected HTTP | Expected Response / DB State | RTM Req |
| :--- | :--- | :---: | :---: | :--- | :---: | :--- | :---: |
| `ROT-SCH-001` | Positive: Trigger schedule generation for rotation board with active members | POS | P0 | POST /shift-rotations/{id}/generate-schedule?locationId=ValidLoc | `200 OK` | Shift schedules generated across rotation cycles. | REQ-ROT-015 |
| `ROT-SCH-002` | Positive: Verify schedule generation creates documents in WorkAssignmentMaps | POS | P0 | Inspect ERP.Attendance.WorkAssignmentMaps collection | `200 OK` | Work assignment map documents created with active shift slots. | REQ-ROT-015 |
| `ROT-SCH-003` | Data Assert: Verify generated maps have Source: 'Rotation' and correct IDs | POS | P0 | Query maps where RotationId == rotationId | `200 OK` | Source is 'Rotation', RotationId and TeamId correctly linked. | REQ-ROT-015 |
| `ROT-SCH-004` | Data Assert: Verify alternating shift cycle for Team A (Plan 1 wk1, Plan 2 wk2) | POS | P0 | Inspect sequential weekly maps for Team A | `200 OK` | Rotates between Plan 1 and Plan 2 across alternating weeks. | REQ-ROT-015 |
| `ROT-SCH-005` | Data Assert: Verify staggered shift cycle for Team B (starts on Plan 2) | POS | P0 | Inspect sequential weekly maps for Team B | `200 OK` | Starts on Plan 2 based on startSequenceOrder: 2. | REQ-ROT-015 |
| `ROT-SCH-006` | Positive: Schedule generation for Uneven rotation respects durationWeeks | POS | P1 | Generate schedule on Uneven rotation board | `200 OK` | Step durations match custom durationWeeks per step. | REQ-ROT-015 |
| `ROT-SCH-007` | Idempotency: Repeated schedule generation does not duplicate maps | POS | P0 | POST /generate-schedule executed twice consecutively | `200 OK` | Existing maps updated/idempotent; 0 duplicate map entries created. | REQ-ROT-015 |
| `ROT-SCH-008` | Edge Case: Generate schedule on rotation board with 0 assigned members | POS | P1 | POST /generate-schedule on empty board | `200 OK` | Completes cleanly with 0 maps generated. | REQ-ROT-015 |
| `ROT-SCH-009` | Negative: Generate schedule on non-existent rotationId | NEG | P1 | POST /shift-rotations/{randomGuid}/generate-schedule | `404 Not Found` | Clean 404 response. | REQ-ROT-002 |
| `ROT-SCH-010` | Scoping Negative: Missing mandatory locationId query parameter | SEC | P0 | POST /generate-schedule without locationId | `400 Bad Request` | Enforces mandatory location scoping. | REQ-ROT-002 |
| `ROT-SCH-011` | Query Schedule: View employee schedule within generated range | POS | P0 | GET /employees/{employeeId}/schedule?from=2026-11-01&to=2026-12-31 | `200 OK` | Returns array of daily shift instances matching rotation. | REQ-ROT-015 |
| `ROT-SCH-012` | Query Schedule: Date filtering returns exact matching slice | POS | P1 | GET /schedule with 7-day date window | `200 OK` | Returns exactly 7 days of schedule data. | REQ-ROT-015 |
| `ROT-SCH-013` | Query Schedule: Employee with future start date shows empty prior schedule | POS | P1 | Query dates prior to member startDate | `200 OK` | Returns empty schedule before effective date. | REQ-ROT-015 |
| `ROT-SCH-014` | Query Schedule: Employee with past end date shows no shifts after end date | POS | P1 | Query dates after member endDate | `200 OK` | Returns empty schedule after termination date. | REQ-ROT-015 |
| `ROT-SCH-015` | Shift Boundaries: Verify overnight shift slots across calendar days | POS | P1 | Inspect schedules for 22:00 - 06:00 shift slot | `200 OK` | Shift spans midnight correctly without date wrapping bugs. | REQ-ROT-015 |
| `ROT-SCH-016` | Rest Days: Verify days off are mapped as non-working days | POS | P1 | Inspect schedule on scheduled days off | `200 OK` | isWorkingDay marked false, work duration 0. | REQ-ROT-015 |
| `ROT-SCH-017` | Policy Linkage: Verify embedded policies bound to daily schedule instances | POS | P1 | Inspect daily schedule policy references | `200 OK` | Break and Overtime policy IDs present on schedule days. | REQ-ROT-006 |
| `ROT-SCH-018` | Business: Plan template update triggers schedule map realignment | BUS | P1 | Updating workTemplateId on plan with existing schedule | `200 OK` | Realigns subsequent maps to new template slots. | REQ-ROT-015 |
| `ROT-SCH-019` | Business: Moving member across teams realigns schedule maps | BUS | P1 | Moving member from Team A to Team B | `200 OK` | Maps regenerated under Team B cycle from effectiveFrom. | REQ-ROT-017 |
| `ROT-SCH-020` | Negative BVA: Query schedule with from > to | BVA | P2 | GET /schedule?from=2026-12-31&to=2026-11-01 | `400 Bad Request` | Validation error: from date must be <= to date. | REQ-ROT-015 |
| `ROT-SCH-021` | Security: Query schedule for employee in Company B | SEC | P0 | Cross-company employeeId schedule query | `403/404` | Multi-tenancy isolation guard blocks access. | REQ-ROT-022 |
| `ROT-SCH-022` | Scale Test: Schedule generation for 48 members across 52 weeks runs < 5s | POS | P2 | 48 employees x 52 weeks generation | `200 OK` | Executes within latency SLA. | REQ-ROT-015 |

---

### Suite 6: Member Lifecycle, Period Modification, Move & Removal

| TC ID | Test Scenario | Category | Priority | Input / Preconditions | Expected HTTP | Expected Response / DB State | RTM Req |
| :--- | :--- | :---: | :---: | :--- | :---: | :--- | :---: |
| `ROT-MEM-001` | Positive: Edit member period - Extend endDate to future date | POS | P0 | PATCH /members/{id} with extended endDate | `200 OK` | Member endDate updated and schedule maps extended. | REQ-ROT-016 |
| `ROT-MEM-002` | Positive: Edit member period - Shorten endDate truncating assignment | POS | P1 | PATCH /members/{id} with earlier endDate | `200 OK` | Member endDate shortened and obsolete future maps pruned. | REQ-ROT-016 |
| `ROT-MEM-003` | Positive: Convert open-ended assignment to fixed endDate | POS | P1 | PATCH /members/{id} setting endDate from null to specific date | `200 OK` | Assignment bounded to fixed date. | REQ-ROT-016 |
| `ROT-MEM-004` | Positive: Convert fixed endDate to open-ended (endDate: null) | POS | P1 | PATCH /members/{id} setting endDate: null | `200 OK` | Assignment converted back to open-ended. | REQ-ROT-016 |
| `ROT-MEM-005` | Negative BVA: Edit member period with endDate < startDate | BVA | P0 | PATCH /members/{id} with endDate before startDate | `400 Bad Request` | Validation error: endDate cannot be before startDate. | REQ-ROT-016 |
| `ROT-MEM-006` | Conflict: Edit period overlaps existing assignment (adjustConflicts: false) | BUS | P1 | PATCH /members/{id} creating overlap with adjustConflicts: false | `400 Bad Request` | Conflict reported: Overlapping assignment detected. | REQ-ROT-016 |
| `ROT-MEM-007` | Conflict: Edit period with adjustConflicts: true auto-resolves overlap | BUS | P1 | PATCH /members/{id} with adjustConflicts: true | `200 OK` | Auto-resolves overlapping assignment. | REQ-ROT-016 |
| `ROT-MEM-008` | Negative: Edit member with non-existent membershipId | NEG | P1 | PATCH /members/{fakeGuid} | `404 Not Found` | Membership not found error. | REQ-ROT-016 |
| `ROT-MEM-009` | Scoping Negative: Edit member without locationId query parameter | SEC | P0 | PATCH /members/{id} without locationId | `400 Bad Request` | Enforces mandatory location scoping. | REQ-ROT-002 |
| `ROT-MEM-010` | Positive: Move member between teams within same rotation (POST /move-team) | POS | P0 | POST /move-team with target teamId and effectiveFrom | `200 OK` | Member transferred to new team; maps adjusted from effectiveFrom. | REQ-ROT-017 |
| `ROT-MEM-011` | Negative: Move team to non-existent teamId | NEG | P1 | POST /move-team with fake teamId | `404 Not Found` | Target team not found. | REQ-ROT-017 |
| `ROT-MEM-012` | Negative: Move team to SAME team employee is already in | BUS | P1 | POST /move-team specifying current teamId | `400 Bad Request` | Validation error: Employee is already in target team. | REQ-ROT-017 |
| `ROT-MEM-013` | Negative DTO: Move team with invalid date format in effectiveFrom | DTO | P2 | POST /move-team with effectiveFrom: 'invalid-date' | `400 Bad Request` | Date parsing error. | REQ-ROT-017 |
| `ROT-MEM-014` | Positive: Preflight check for moving member across rotations | POS | P0 | POST /move/check-conflicts with targetRotationId | `200 OK` | Returns conflict assessment without mutating data. | REQ-ROT-018 |
| `ROT-MEM-015` | Positive: Execute cross-rotation move (PATCH /move) | POS | P0 | PATCH /move with targetType: Rotation, targetRotationId, targetTeamId | `200 OK` | Transfers member across rotation boards seamlessly. | REQ-ROT-018 |
| `ROT-MEM-016` | Positive: Move from Rotation to Regular Work Plan | POS | P0 | PATCH /move with targetType: WorkPlan, targetWorkPlanId | `200 OK` | Transfers member to regular work plan. | REQ-ROT-018 |
| `ROT-MEM-017` | Business Negative: Move member to rotation/plan in ANOTHER location | SEC | P0 | PATCH /move targeting plan in different location | `400 Bad Request` | Cross-location transfer blocked without formal employee location transfer. | REQ-ROT-012 |
| `ROT-MEM-018` | Negative DTO: Move member with invalid targetType enum | DTO | P1 | PATCH /move with targetType: 'Unknown' | `400 Bad Request` | Schema model binding rejection: Invalid MoveTargetType. | REQ-ROT-018 |
| `ROT-MEM-019` | Negative: Move member referencing non-existent targetWorkPlanId | NEG | P1 | targetWorkPlanId: fakeGuid | `404 Not Found` | Target work plan not found. | REQ-ROT-018 |
| `ROT-MEM-020` | Negative: Move member referencing non-existent targetRotationId | NEG | P1 | targetRotationId: fakeGuid | `404 Not Found` | Target rotation board not found. | REQ-ROT-018 |
| `ROT-MEM-021` | Positive: Remove member from rotation (DELETE /members/{membershipId}) | POS | P0 | DELETE /members/{id}?endDate=2026-11-30 | `200 OK` | Member terminated as of endDate. | REQ-ROT-019 |
| `ROT-MEM-022` | Positive: Immediate removal of member (endDate = today) | POS | P0 | DELETE /members/{id}?endDate=Today | `200 OK` | Member immediately inactivated. | REQ-ROT-019 |
| `ROT-MEM-023` | Positive: Future removal of member (endDate = +14 days) | POS | P1 | DELETE /members/{id}?endDate=+14days | `200 OK` | Member remains active until specified future endDate. | REQ-ROT-019 |
| `ROT-MEM-024` | MongoDB Assert: Verify member has IsActive: false in ShiftRotationBoard | POS | P0 | Query ShiftRotationBoard in Sahab DB | `200 OK` | Member record has IsActive: false and EndDate populated. | REQ-ROT-019 |
| `ROT-MEM-025` | MongoDB Assert: Verify WorkAssignmentMaps after endDate are purged | POS | P0 | Query ERP.Attendance.WorkAssignmentMaps after endDate | `200 OK` | Obsolete maps pruned or inactivated. | REQ-ROT-019 |
| `ROT-MEM-026` | Negative: Delete member with non-existent membershipId | NEG | P1 | DELETE /members/{fakeGuid} | `404 Not Found` | Membership not found error. | REQ-ROT-019 |
| `ROT-MEM-027` | Negative: Delete member that is already deleted | BUS | P2 | DELETE /members/{id} on already deleted member | `400/404` | Validation error: Member is already inactive. | REQ-ROT-019 |
| `ROT-MEM-028` | Security: Delete member belonging to another company | SEC | P0 | Cross-company membershipId deletion attempt | `403 Forbidden` | Tenant isolation guard blocks access. | REQ-ROT-022 |

---

### Suite 7: Rotation Work Template CRUD & Slot Invariants

| TC ID | Test Scenario | Category | Priority | Input / Preconditions | Expected HTTP | Expected Response / DB State | RTM Req |
| :--- | :--- | :---: | :---: | :--- | :---: | :--- | :---: |
| `ROT-TMP-001` | Positive: Create Rotation Work Template with 7-day schedule (5 work, 2 off) | POS | P0 | POST /worktemplates/rotation with 7 rotationTimeSlots | `200 OK` | Template created with templateType: Rotation. | REQ-ROT-021 |
| `ROT-TMP-002` | Positive: Multilingual template naming (en and ar) | POS | P1 | templateName: {'en': 'Day Shift Rot', 'ar': 'دوران الوردية النهارية'} | `200 OK` | Multilingual template names stored cleanly. | REQ-ROT-021 |
| `ROT-TMP-003` | Positive: Overnight shift slot spanning midnight (22:00 to 06:00) | POS | P0 | startTime: '22:00:00', endTime: '06:00:00' | `200 OK` | Night shift slot across midnight handled cleanly. | REQ-ROT-021 |
| `ROT-TMP-004` | Positive: Split/Multiple time slots within single day in rotation template | POS | P1 | Multiple slots for same dayEnum | `200 OK` | Split shift within rotation day supported. | REQ-ROT-021 |
| `ROT-TMP-005` | Positive: Unique shortCode assigned to rotation work template | POS | P1 | shortCode: 'ROT-D1' | `200 OK` | Template code assigned. | REQ-ROT-021 |
| `ROT-TMP-006` | Negative DTO: Missing templateName object | DTO | P0 | templateName: null or omitted | `400 Bad Request` | Validation error: templateName is required. | REQ-ROT-021 |
| `ROT-TMP-007` | Negative DTO: Missing rotationTimeSlots array | DTO | P0 | rotationTimeSlots omitted | `400 Bad Request` | Validation error: rotationTimeSlots is required. | REQ-ROT-021 |
| `ROT-TMP-008` | Negative DTO: Empty rotationTimeSlots array | DTO | P1 | rotationTimeSlots: [] | `400 Bad Request` | Validation error: At least one time slot is required. | REQ-ROT-021 |
| `ROT-TMP-009` | Business Negative: Duplicate shortCode within company | BUS | P1 | shortCode matches existing template in company | `400 Bad Request` | Validation error: shortCode must be unique within company. | REQ-ROT-021 |
| `ROT-TMP-010` | Business Invariant: totalWorkingDays + totalDaysOff != 7 | BVA | P1 | totalWorkingDays: 5, totalDaysOff: 3 (sum=8) | `400 Bad Request` | Validation error: Total working days and days off must equal 7. | REQ-ROT-021 |
| `ROT-TMP-011` | Negative BVA: totalWorkDurationInMinutes <= 0 for working day | BVA | P2 | isWorkingDay: true, totalWorkDurationInMinutes: 0 | `400 Bad Request` | Validation error: Working day must have duration > 0. | REQ-ROT-021 |
| `ROT-TMP-012` | Negative DTO: Invalid time format in startTime or endTime | DTO | P1 | startTime: '25:00:00' | `400 Bad Request` | Time format validation failure. | REQ-ROT-021 |
| `ROT-TMP-013` | Negative DTO: dayEnum value out of bounds | DTO | P1 | dayEnum: 7 (valid 0..6) | `400 Bad Request` | Enum range validation error. | REQ-ROT-021 |
| `ROT-TMP-014` | Positive: Update rotation work template (PATCH /worktemplates/rotation/{id}) | POS | P0 | PATCH templateName and shortCode | `200 OK` | Template properties updated. | REQ-ROT-021 |
| `ROT-TMP-015` | Positive: Update rotation time slots with hasPatternUpdate: true | POS | P1 | PATCH rotationTimeSlots with hasPatternUpdate: true | `200 OK` | Template slots updated and pattern flag recognized. | REQ-ROT-021 |
| `ROT-TMP-016` | Positive: Update rotation time slots with hasPatternUpdate: false | POS | P1 | PATCH rotationTimeSlots with hasPatternUpdate: false | `200 OK` | Metadata updated without altering active patterns. | REQ-ROT-021 |
| `ROT-TMP-017` | Business Negative: Modify slots while active in rotation plan without flag | BUS | P1 | PATCH slots on in-use template with hasPatternUpdate omitted | `400 Bad Request` | Integrity error: Pattern update flag required for template in active rotation. | REQ-ROT-021 |
| `ROT-TMP-018` | Negative: Update rotation template by non-existent ID | NEG | P1 | PATCH /worktemplates/rotation/{fakeGuid} | `404 Not Found` | Template not found. | REQ-ROT-021 |
| `ROT-TMP-019` | Scoping Negative: Create rotation template without locationId | SEC | P0 | POST /worktemplates/rotation without locationId | `400 Bad Request` | Enforces mandatory location scoping. | REQ-ROT-002 |
| `ROT-TMP-020` | Scoping Negative: Update rotation template without locationId | SEC | P0 | PATCH /worktemplates/rotation/{id} without locationId | `400 Bad Request` | Enforces mandatory location scoping. | REQ-ROT-002 |
| `ROT-TMP-021` | Security: Tamper companyId to create/update template across tenant boundary | SEC | P0 | Cross-company template creation attempt | `403 Forbidden` | Tenant isolation guard blocks access. | REQ-ROT-022 |
| `ROT-TMP-022` | MongoDB Assert: Verify template stored in ERP.Attendance.WorkTemplates | POS | P0 | Query WorkTemplates collection in MongoDB | `200 OK` | Document created with TemplateType: 'Rotation'. | REQ-ROT-021 |

---

### Suite 8: Shift Rotation Deletion & Board Lifecycle Guards

| TC ID | Test Scenario | Category | Priority | Input / Preconditions | Expected HTTP | Expected Response / DB State | RTM Req |
| :--- | :--- | :---: | :---: | :--- | :---: | :--- | :---: |
| `ROT-DEL-001` | Positive: Soft-delete rotation board with 0 assigned members | POS | P0 | DELETE /shift-rotations/{id}?locationId=ValidLoc on empty board | `200 OK` | Rotation board soft-deleted successfully. | REQ-ROT-020 |
| `ROT-DEL-002` | Positive MongoDB Assert: Verify board has IsDeleted: true | POS | P0 | Query ShiftRotationBoard document in Sahab DB | `200 OK` | Document marked with IsDeleted: true. | REQ-ROT-020 |
| `ROT-DEL-003` | Positive Filter Assert: Deleted board does NOT appear in GET list | POS | P0 | GET /shift-rotations after deletion | `200 OK` | Deleted board excluded from active rotation listing. | REQ-ROT-020 |
| `ROT-DEL-004` | Business Guard Negative: Delete rotation board with ACTIVE members | BUS | P0 | DELETE /shift-rotations/{id} on board with active members | `400 Bad Request` | Business block: Cannot delete rotation board with active member assignments. | REQ-ROT-020 |
| `ROT-DEL-005` | Business Guard Positive: Delete board after all members removed | BUS | P0 | DELETE /shift-rotations/{id} after all members soft-deleted | `200 OK` | Board deletion succeeds after active member clearance. | REQ-ROT-020 |
| `ROT-DEL-006` | Cascading Assert: WorkAssignmentMaps for deleted board invalidated | POS | P1 | Query WorkAssignmentMaps for deleted board | `200 OK` | Associated maps deactivated or pruned. | REQ-ROT-020 |
| `ROT-DEL-007` | Negative: Delete rotation board with non-existent rotationId | NEG | P1 | DELETE /shift-rotations/{fakeGuid} | `404 Not Found` | Board not found error. | REQ-ROT-002 |
| `ROT-DEL-008` | Negative: Delete already deleted rotation board | BUS | P2 | DELETE /shift-rotations/{id} on board with IsDeleted: true | `400/404` | Validation error: Board is already deleted. | REQ-ROT-020 |
| `ROT-DEL-009` | Negative DTO: Malformed GUID string in delete path | DTO | P2 | DELETE /shift-rotations/not-a-guid | `400 Bad Request` | GUID parsing failure. | REQ-ROT-002 |
| `ROT-DEL-010` | Scoping Negative: Delete rotation board without mandatory locationId | SEC | P0 | DELETE /shift-rotations/{id} without locationId | `400 Bad Request` | Enforces mandatory location scoping. | REQ-ROT-002 |
| `ROT-DEL-011` | Scoping Negative: locationId does not match board location | SEC | P1 | DELETE with locationId of Dammam on Jeddah board | `400/404` | Mismatched location scoping rejected. | REQ-ROT-002 |
| `ROT-DEL-012` | Security: Delete rotation board belonging to another company | SEC | P0 | Cross-company board deletion attempt | `403 Forbidden` | Tenant isolation guard blocks deletion. | REQ-ROT-022 |
| `ROT-DEL-013` | Re-activation Guard: System prevents adding members to deleted board | BUS | P1 | POST /employees on deleted rotation board | `400 Bad Request` | Validation error: Cannot assign members to a deleted rotation board. | REQ-ROT-020 |
| `ROT-DEL-014` | Audit Trail Assert: Verify DeletedAt and DeletedBy recorded in DB | POS | P2 | Inspect ShiftRotationBoard audit fields in MongoDB | `200 OK` | DeletedAt timestamp and DeletedBy identity properly populated. | REQ-ROT-020 |

---

## 4. Test Suite Execution & Coverage Dashboard

| Suite # | Suite Scope | Total TCs | P0 Critical | P1 Major | P2 Medium | Primary Endpoint Covered |
| :---: | :--- | :---: | :---: | :---: | :---: | :--- |
| **1** | Shift Rotation Creation & Preview | 30 | 10 | 15 | 5 | `POST /shift-rotations`, `POST /preview` |
| **2** | Shift Rotation Query Endpoints | 22 | 6 | 11 | 5 | `GET /shift-rotations`, `GET /{id}`, `GET /grid` |
| **3** | Shift Rotation Update & Mutation | 24 | 7 | 13 | 4 | `PATCH /shift-rotations/{id}` |
| **4** | Team Assignment & Preflight Conflict Detection | 32 | 14 | 14 | 4 | `POST /teams/{teamId}/employees` & `check-conflicts` |
| **5** | Schedule Materialization & Generation | 22 | 8 | 11 | 3 | `POST /generate-schedule`, `GET /schedule` |
| **6** | Member Lifecycle, Period Modification, Move & Removal | 28 | 10 | 14 | 4 | `PATCH /members/{id}`, `DELETE /members/{id}`, `POST /move` |
| **7** | Rotation Work Template CRUD & Slot Invariants | 22 | 8 | 11 | 3 | `POST /worktemplates/rotation`, `PATCH /rotation/{id}` |
| **8** | Shift Rotation Deletion & Board Lifecycle Guards | 14 | 6 | 6 | 2 | `DELETE /shift-rotations/{id}` |
| **TOTAL** | **Comprehensive Rotation Master Test Suite** | **194** | **69** | **95** | **30** | **All 19 Rotation & Template Endpoints** |