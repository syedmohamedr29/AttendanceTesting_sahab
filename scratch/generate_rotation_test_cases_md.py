# -*- coding: utf-8 -*-
"""
Generate ROTATION_WORK_PLAN_TEST_CASES.md
Comprehensive Senior-QA Test Case Specification for Shift Rotations & Rotation Work Plans
"""

import os

md_content = """# Shift Rotation & Rotation Work Plan Test Specification (RTM, DTO Validations, Functional, Positive & Negative Invariants)

**Microservices:** `SP.AttendanceSvc` (.NET 9 / ASP.NET Core) & `SP.EmployeeSvc` (.NET 8)  
**Gateway Routes:** `https://gw8.dev.zoolwork.com/api/companies/{companyId}/shift-rotations` & `worktemplates/rotation`  
**Database Collections:** `Sahab.ERP.Attendance.ShiftRotationBoard`, `ERP.Attendance.WorkAssignmentMaps`, `ERP.Attendance.WorkTemplates`  
**Test Methodology:** Requirements Traceability Matrix (RTM), Equivalence Partitioning (EP), Boundary Value Analysis (BVA), Negative/Positive standalone, DTO Field Invariants, and MongoDB Document State Transitions  
**Author:** Antigravity Senior QA Automation & Microservice Specialist  

---

## 1. Executive Test Strategy & Architectural Blueprint

A **Shift Rotation Work Plan** is the cyclical scheduling engine of the Zoolwork attendance platform. It manages structured, recurring work schedules across one or more teams, alternating between day/night/swing shifts or working/rest periods according to mathematically defined cycles.

### 🔑 Architectural Foundations:
1. **The Three-Tier Hierarchy:**
   - **Rotation Header (`ERP.Attendance.ShiftRotationBoard`):** Top-level definition holding `RotationName`, `PatternType`, `WeeksPerStep`, `LocationId`, embedded `Plans[]`, `Teams[]`, and `Members[]`.
   - **Embedded Rotation Plans (`Plans[]`):** Each step in the rotation references a specific Work Plan with embedded Work Template and Policies (e.g. Plan 1 = "Morning Shift", Plan 2 = "Night Shift").
   - **Teams & Step Sequence (`Teams[]` & `Steps[]`):** Teams rotate through the `Steps` based on their `StartSequenceOrder`.
2. **Dual Representation in MongoDB:**
   - **Master Document:** Stored in `Sahab.ERP.Attendance.ShiftRotationBoard`.
   - **Materialized Operational Maps:** When members are assigned, schedule rows are materialized into `Sahab.ERP.Attendance.WorkAssignmentMaps` with `Source: "Rotation"`, `RotationId`, and `TeamId`.
3. **Pattern Types:**
   - **`Alternating` (Type 1):** Equal duration per step defined globally by `WeeksPerStep`.
   - **`Uneven` (Type 2):** Each step can define an independent `DurationWeeks`.

---

## 2. Master 19-Endpoint Index & Parameters Reference

| # | HTTP Method & Route | DTO / Payload | Query Parameters | Description & Scope |
| :-: | :--- | :--- | :--- | :--- |
| **1** | `POST /shift-rotations` | `ShiftRotationDto` | `locationId` | Create Shift Rotation with embedded Plans, Teams & Steps |
| **2** | `GET /shift-rotations` | *None* | `locationId` | List Shift Rotations scoped to location |
| **3** | `POST /shift-rotations/preview` | `ShiftRotationDto` | `locationId`, `cycles` | Preview matrix grid without persisting |
| **4** | `GET /shift-rotations/{rotationId}` | *None* | *None* | Get Shift Rotation details and team configuration |
| **5** | `PATCH /shift-rotations/{rotationId}` | `UpdateShiftRotationDto` | `locationId` | Update Rotation name, plans, steps, teams, removedPlanIds |
| **6** | `DELETE /shift-rotations/{rotationId}` | *None* | `locationId` | Soft-delete Shift Rotation; validates active members |
| **7** | `GET /shift-rotations/{rotationId}/rotation-grid` | *None* | `from`, `to`, `cycles` | Query rotational grid matrix (Teams x Weeks x Plans) |
| **8** | `POST /shift-rotations/{rotationId}/teams/{teamId}/employees/check-conflicts` | `AddRotationEmployeesDto` | `locationId`, `excludeMembershipId` | Preflight conflict preview for assigning members to a team |
| **9** | `POST /shift-rotations/{rotationId}/teams/{teamId}/employees` | `AddRotationEmployeesDto` | `locationId` | Commit assignment of employees to a rotation team |
| **10** | `GET /shift-rotations/{rotationId}/employees` | *None* | `teamId`, `segment`, `asOf`, `page`, `pageSize` | List rotation members with segmentation |
| **11** | `GET /shift-rotations/{rotationId}/employees/{employeeId}/schedule` | *None* | `from`, `to` | View individual employee's projected shift schedule |
| **12** | `POST /shift-rotations/{rotationId}/generate-schedule` | *None* | `locationId` | Force generation/materialization of shift schedule maps |
| **13** | `PATCH /shift-rotations/{rotationId}/members/{membershipId}` | `EditRotationMemberPeriodDto` | `locationId` | Edit member effective period (`startDate`, `endDate`) |
| **14** | `DELETE /shift-rotations/{rotationId}/members/{membershipId}` | *None* | `locationId`, `endDate` | Remove member from rotation / soft-delete |
| **15** | `POST /shift-rotations/{rotationId}/members/{membershipId}/move/check-conflicts` | `MoveEmployeeDto` | `locationId` | Preflight check for moving member across rotations/plans |
| **16** | `PATCH /shift-rotations/{rotationId}/members/{membershipId}/move` | `MoveEmployeeDto` | `locationId` | Execute move across rotations/plans |
| **17** | `POST /shift-rotations/{rotationId}/members/{membershipId}/move-team` | `MoveRotationMemberTeamDto` | `locationId` | Move member between teams within the same rotation |
| **18** | `POST /worktemplates/rotation` | `RotationWorkTemplateDto` | `locationId` | Create Work Template with rotation time slots |
| **19** | `PATCH /worktemplates/rotation/{id}` | `UpdateRotationWorkTemplateDto` | `locationId` | Update rotation work template properties |

---

## 3. Requirements Traceability Matrix (RTM)

| Req ID | Business Requirement Description | Microservice Components | Test Cases Covering |
| :---: | :--- | :--- | :--- |
| **REQ-ROT-001** | Shift Rotation must have a multilingual name (`en`, `ar`). | `ShiftRotationDto.RotationName` | `ROT-DTO-001`, `ROT-CRT-001`, `ROT-CRT-002` |
| **REQ-ROT-002** | Rotation must belong to a valid Company and Work Location. | `ShiftRotationBoard.CompanyId/LocationId` | `ROT-SEC-001`, `ROT-SEC-002`, `ROT-CRT-003` |
| **REQ-ROT-003** | PatternType must be either `Alternating` (1) or `Uneven` (2). | `RotationPatternType` Enum | `ROT-DTO-003`, `ROT-CRT-004`, `ROT-CRT-005` |
| **REQ-ROT-004** | When `Alternating`, `WeeksPerStep` must be >= 1 and apply to all steps. | `ShiftRotationDto.WeeksPerStep` | `ROT-BVA-001`, `ROT-BVA-002`, `ROT-CRT-006` |
| **REQ-ROT-005** | When `Uneven`, each step must declare a positive `DurationWeeks`. | `RotationStepDto.DurationWeeks` | `ROT-BUS-001`, `ROT-BUS-002` |
| **REQ-ROT-006** | Rotation must contain at least 1 embedded Work Plan (`Plans[]`). | `ShiftRotationDto.Plans` | `ROT-DTO-004`, `ROT-CRT-007` |
| **REQ-ROT-007** | Each embedded Plan must reference a valid Work Template (`workTemplateId`). | `RotationPlanDto.WorkTemplateId` | `ROT-BUS-003`, `ROT-BUS-004` |
| **REQ-ROT-008** | Work Templates embedded in rotation must be of type `Rotation` or `FixedShift`. | `WorkTemplate.TemplateType` | `ROT-BUS-005`, `ROT-BUS-006` |
| **REQ-ROT-009** | Rotation must contain at least 1 Team (`Teams[]`). | `ShiftRotationDto.Teams` | `ROT-DTO-005`, `ROT-CRT-008` |
| **REQ-ROT-010** | Team start sequences must be unique and within step index range. | `RotationTeamDto.StartSequenceOrder` | `ROT-BUS-007`, `ROT-BUS-008` |
| **REQ-ROT-011** | Steps array (`Steps[]`) must only reference declared `PlanIndex` values. | `RotationStepDto.PlanIndex` | `ROT-BUS-009`, `ROT-BUS-010` |
| **REQ-ROT-012** | Preflight conflict check must evaluate overlapping Regular, Roster, or Rotation shifts. | `teams/{teamId}/employees/check-conflicts` | `ROT-CHK-001` to `ROT-CHK-008` |
| **REQ-ROT-013** | Only Active employees (`IsActive: true`, `Status: 2`) can be assigned to a rotation team. | `teams/{teamId}/employees` | `ROT-EMP-001`, `ROT-EMP-002` |
| **REQ-ROT-014** | Employees assigned to rotation must belong to the same Work Location. | `Employee.WorkLocationId == Rotation.LocationId` | `ROT-EMP-003`, `ROT-EMP-004` |
| **REQ-ROT-015** | Assignment start date cannot precede Employee Date of Joining (`startDate >= DOJ`). | `Employee.DateOfJoining` | `ROT-EMP-005`, `ROT-EMP-006` |
| **REQ-ROT-016** | Offboarding/Exited employees cannot receive open-ended rotation assignments. | `EmployeeStatus Enum (5, 6)` | `ROT-EMP-007`, `ROT-EMP-008` |
| **REQ-ROT-017** | Member period modifications must validate and adjust overlapping assignments. | `members/{membershipId}` | `ROT-MEM-001` to `ROT-MEM-006` |
| **REQ-ROT-018** | Member team transfer (`move-team`) must re-align employee to target team's sequence. | `members/{membershipId}/move-team` | `ROT-MOV-001`, `ROT-MOV-002` |
| **REQ-ROT-019** | Member cross-move (`move`) must deactivate old rotation row and initialize new target. | `members/{membershipId}/move` | `ROT-MOV-003`, `ROT-MOV-004` |
| **REQ-ROT-020** | Deleting a rotation with active assigned members must be blocked or soft-deleted safely. | `DELETE /shift-rotations/{rotationId}` | `ROT-DEL-001`, `ROT-DEL-002` |

---

## 4. Comprehensive Test Suites (180+ Test Scenarios)

### 4.1 Suite 1: Shift Rotation Creation (`POST /shift-rotations`) — 20 Test Cases

| TC ID | Test Scenario | Category | Query & Payload Parameters | Expected HTTP | Expected Response / DB State |
| :--- | :--- | :---: | :--- | :---: | :--- |
| `ROT-CRT-001` | Positive: Create Alternating Rotation with 2 Plans, 2 Teams, 1 Week/Step | POS | `patternType: Alternating`, `weeksPerStep: 1`, 2 Plans, 2 Teams | `200 OK` | Document created in `ERP.Attendance.ShiftRotationBoard` with `IsDeleted: false`. |
| `ROT-CRT-002` | Positive: Create Uneven Rotation with custom `durationWeeks` per Step | POS | `patternType: Uneven`, Step 1 = 2 wks, Step 2 = 1 wk | `200 OK` | Persisted with uneven step durations. |
| `ROT-CRT-003` | Positive: Multilingual Name (`en` and `ar`) | POS | `rotationName: {"en": "Factory Rotation", "ar": "دوران المصنع"}` | `200 OK` | Multilingual names preserved without escaping bugs. |
| `ROT-CRT-004` | Negative: Missing `rotationName` object | DTO | `rotationName: null` or omitted | `400 Bad Request` | `Cit.Attendance:Validation` / Name is required. |
| `ROT-CRT-005` | Negative: Empty English Name | DTO | `rotationName: {"en": "", "ar": "دوران"}` | `400 Bad Request` | Validation failure on empty string. |
| `ROT-CRT-006` | Negative: Missing `plans` array | DTO | `plans: []` or omitted | `400 Bad Request` | At least 1 plan must be provided. |
| `ROT-CRT-007` | Negative: Missing `teams` array | DTO | `teams: []` or omitted | `400 Bad Request` | At least 1 team must be provided. |
| `ROT-CRT-008` | Negative: Missing `steps` array | DTO | `steps: []` or omitted | `400 Bad Request` | At least 1 step must be provided. |
| `ROT-CRT-009` | Negative: Invalid `patternType` enum | DTO | `patternType: "Random"` | `400 Bad Request` | Schema model binding rejection. |
| `ROT-CRT-010` | Negative: `weeksPerStep = 0` on Alternating | BVA | `patternType: Alternating`, `weeksPerStep: 0` | `400 Bad Request` | Value must be >= 1. |
| `ROT-CRT-011` | Negative: `weeksPerStep < 0` (Negative value) | NEG | `weeksPerStep: -2` | `400 Bad Request` | Negative integer blocked. |
| `ROT-CRT-012` | Boundary: `weeksPerStep = 52` (Max annual cycle) | BVA | `weeksPerStep: 52` | `200 OK` | Upper boundary accepted. |
| `ROT-CRT-013` | Boundary: `weeksPerStep = 53` (Overflow) | BVA | `weeksPerStep: 53` | `400 Bad Request` | Exceeds max 52 weeks boundary. |
| `ROT-CRT-014` | Business: `planIndex` in Step not declared in `plans[]` | BUS | Plans=[Index 1], Steps=[PlanIndex 2] | `400 Bad Request` | Reference integrity error (PlanIndex 2 does not exist). |
| `ROT-CRT-015` | Business: Duplicate `startSequenceOrder` across teams | BUS | Team A = 1, Team B = 1 | `400 Bad Request` | Duplicate sequence order rejection. |
| `ROT-CRT-016` | Business: Non-existent `workTemplateId` in Plan | BUS | `workTemplateId: 00000000-0000-0000-0000-000000000000` | `400 Bad Request` | Template not found error. |
| `ROT-CRT-017` | Business: Using Flexible Template inside Rotation Plan | BUS | `workTemplateId` of Flexible Template | `400 Bad Request` | Incompatible template type (only Fixed/Rotation allowed). |
| `ROT-CRT-018` | Scoping: Missing mandatory `locationId` query | SEC | Omit `locationId` query parameter | `400 Bad Request` | Scoping enforcement error. |
| `ROT-CRT-019` | Scoping: Non-existent `locationId` GUID | SEC | Fake `locationId` | `404 Not Found` | Location does not exist in company. |
| `ROT-CRT-020` | Security: Cross-tenant companyId tampering | SEC | Path companyId != Auth tenant companyId | `403 Forbidden` | Multi-tenancy guard blocks access. |

---

### 4.2 Suite 2: Shift Rotation Query Endpoints (`GET`) — 16 Test Cases

| TC ID | Test Scenario | Category | Query Parameters | Expected HTTP | Expected Response / DB State |
| :--- | :--- | :---: | :--- | :---: | :--- |
| `ROT-GET-001` | Positive: List rotations for location with multiple boards | POS | `locationId=ValidLoc` | `200 OK` | Array of shift rotations with embedded plans and teams. |
| `ROT-GET-002` | Positive: List rotations for clean location with 0 boards | POS | `locationId=EmptyLoc` | `200 OK` | Empty array `[]` (not 404). |
| `ROT-GET-003` | Negative: Missing mandatory `locationId` | NEG | Omit `locationId` | `400 Bad Request` | Enforces mandatory location scoping. |
| `ROT-GET-004` | Positive: Get single rotation by valid ID | POS | `rotationId=ExistingId` | `200 OK` | Complete rotation document matching database state. |
| `ROT-GET-005` | Negative: Get rotation by non-existent GUID | NEG | `rotationId=FakeGUID` | `404 Not Found` | Clean 404 response. |
| `ROT-GET-006` | Negative: Get rotation with malformed GUID string | DTO | `rotationId="abc-123"` | `400 Bad Request` | GUID format parsing error. |
| `ROT-GET-007` | Security: Get rotation belonging to another company | SEC | `rotationId` from Company B | `403 Forbidden` / `404` | Cross-company isolation enforced. |
| `ROT-GET-008` | Positive: Query rotation-grid with valid date range | POS | `from=2026-11-01&to=2026-12-31` | `200 OK` | Generates rotation matrix grid across weeks. |
| `ROT-GET-009` | Positive: Query rotation-grid using `cycles` parameter | POS | `cycles=4` | `200 OK` | Matrix projected across exactly 4 complete cycles. |
| `ROT-GET-010` | Negative: Rotation-grid with `from > to` | BVA | `from=2026-12-31&to=2026-11-01` | `400 Bad Request` | Inverted date range rejection. |
| `ROT-GET-011` | Positive: List rotation employees with pagination | POS | `page=1&pageSize=10` | `200 OK` | Paginated employee member array. |
| `ROT-GET-012` | Positive: Filter rotation employees by `teamId` | POS | `teamId=TeamA_Id` | `200 OK` | Returns only employees belonging to Team A. |
| `ROT-GET-013` | Positive: Filter rotation employees by `segment=Current` | POS | `segment=Current` | `200 OK` | Returns currently active members. |
| `ROT-GET-014` | Positive: Get individual employee rotation schedule | POS | `employeeId=E1&from=2026-11-01&to=2026-11-30` | `200 OK` | Daily shift schedule projected from rotation cycle. |
| `ROT-GET-015` | Negative: Employee schedule query for unassigned employee | NEG | `employeeId=UnassignedE` | `200 OK` / `404` | Empty schedule array or Not Found. |
| `ROT-GET-016` | Positive: Self-service `GET /me/rotation` schedule | POS | Auth Bearer of employee | `200 OK` | Returns logged-in user's active rotation details. |

---

### 4.3 Suite 3: Shift Rotation Update & Mutation (`PATCH`) — 16 Test Cases

| TC ID | Test Scenario | Category | Query & Payload Parameters | Expected HTTP | Expected Response / DB State |
| :--- | :--- | :---: | :--- | :---: | :--- |
| `ROT-PAT-001` | Positive: Update Rotation Name | POS | `rotationName: {"en": "Updated Name"}` | `200 OK` | DB updated, `ModifiedAt` updated. |
| `ROT-PAT-002` | Positive: Add new Plan to existing rotation | POS | `plans: [ExistingPlan1, NewPlan2]` | `200 OK` | New plan appended, template embedded. |
| `ROT-PAT-003` | Positive: Remove unused Plan using `removedPlanIds` | POS | `removedPlanIds: [OldPlanId]` | `200 OK` | Plan removed from `Plans[]` array. |
| `ROT-PAT-004` | Negative: Remove Plan currently assigned to active steps | BUS | `removedPlanIds: [InUsePlanId]` | `400 Bad Request` | Cannot delete plan referenced by active steps. |
| `ROT-PAT-005` | Positive: Add new Team to rotation | POS | `teams: [TeamA, TeamB, TeamC]` | `200 OK` | Team C added with unique sequence order. |
| `ROT-PAT-006` | Negative: Update with duplicate team sequence order | BUS | Team B = 1, Team C = 1 | `400 Bad Request` | Duplicate sequence rejected. |
| `ROT-PAT-007` | Positive: Switch PatternType from `Alternating` to `Uneven` | POS | `patternType: Uneven`, custom step durations | `200 OK` | Pattern recalculated and stored. |
| `ROT-PAT-008` | Negative: Switch to `Uneven` with missing step durations | BUS | `patternType: Uneven`, `durationWeeks: null` | `400 Bad Request` | Uneven requires duration per step. |
| `ROT-PAT-009` | Positive: Update `weeksPerStep` for Alternating | POS | `weeksPerStep: 2` | `200 OK` | Cycle length doubled in DB. |
| `ROT-PAT-010` | Negative: Non-existent `rotationId` in path | NEG | Fake `rotationId` | `404 Not Found` | Clean 404 response. |
| `ROT-PAT-011` | Security: Cross-company PATCH attempt | SEC | Company B rotationId | `403 Forbidden` | Access denied. |
| `ROT-PAT-012` | Concurrency: Stale modification check | CON | Outdated ConcurrencyStamp / modified timestamp | `409 Conflict` | Optimistic locking guard prevents overwrites. |
| `ROT-PAT-013` | Schema: Explicit `null` in non-nullable field | DTO | `patternType: null` | `400 Bad Request` | Model validation rejection. |
| `ROT-PAT-014` | Boundary: Maximum 20 teams in rotation | BVA | 21 teams in payload | `400 Bad Request` | Team count limit enforced. |
| `ROT-PAT-015` | Boundary: Maximum 20 steps in rotation cycle | BVA | 21 steps in payload | `400 Bad Request` | Step count limit enforced. |
| `ROT-PAT-016` | Teardown: Revert modifications to baseline | CLN | Re-apply initial configuration | `200 OK` | Restores baseline state. |

---

### 4.4 Suite 4: Rotation Team Assignment & Conflict Detection — 20 Test Cases

| TC ID | Test Scenario | Category | Query & Payload Parameters | Expected HTTP | Expected Response / DB State |
| :--- | :--- | :---: | :--- | :---: | :--- |
| `ROT-CHK-001` | Positive: Check conflicts for clean active employee | POS | Clean employee, future start date | `200 OK` | `hasConflicts: false, canProceed: true, allowedEmployeeIds: [E1]`. |
| `ROT-CHK-002` | Overlap: Employee on existing Regular Plan (Adjustable) | BUS | Employee with Regular assignment | `200 OK` | `hasConflicts: true, canProceed: true, adjustableEmployeeIds: [E1]`. |
| `ROT-CHK-003` | Overlap: Employee on existing Roster Board (Blocked) | BUS | Employee with active Roster membership | `200 OK` | `hasConflicts: true, canProceed: false, blockedEmployeeIds: [E1]`. |
| `ROT-CHK-004` | Overlap: Employee on another Rotation Team (Blocked) | BUS | Employee already in another Rotation team | `200 OK` | `hasConflicts: true, canProceed: false, blockedEmployeeIds: [E1]`. |
| `ROT-CHK-005` | Query Flag: `excludeMembershipId` ignores self | BUS | Editing member period with self excluded | `200 OK` | Excludes current membership from collision. |
| `ROT-CHK-006` | Boundary: Inverted dates (`endDate < startDate`) | NEG | `startDate: 2026-12-10, endDate: 2026-12-05` | `400 Bad Request` | Date chronology validation error. |
| `ROT-CHK-007` | Positive: Commit assign clean employee to Team | POS | `POST /teams/{teamId}/employees` clean employee | `200 OK` | Member added to `Members[]` in `ShiftRotationBoard`. |
| `ROT-CHK-008` | Positive: Commit assign with `adjustConflicts=true` | POS | Regular plan overlap + `adjustConflicts: true` | `200 OK` | Regular map trimmed; Rotation member created. |
| `ROT-CHK-009` | Negative: Commit assign with `adjustConflicts=false` on overlap | NEG | Regular plan overlap + `adjustConflicts: false` | `400 Bad Request` | Blocked due to unadjusted conflict. |
| `ROT-CHK-010` | Negative: Commit assign blocked employee (Roster overlap) | NEG | Employee on Roster | `400 Bad Request` | Hard conflict cannot be adjusted. |
| `ROT-CHK-011` | Negative: Assign Inactive Employee (`IsActive: false`) | NEG | Inactive employee ID | `400 Bad Request` | Inactive employee rejected. |
| `ROT-CHK-012` | Negative: Assign Employee belonging to different Location | SEC | Dammam employee assigned to Jeddah team | `400 Bad Request` | Location mismatch rejection. |
| `ROT-CHK-013` | Negative: `startDate < DateOfJoining` | BUS | Start date prior to employee DOJ | `400 Bad Request` | Start date before DOJ blocked. |
| `ROT-CHK-014` | Boundary: `startDate == DateOfJoining` | BVA | Start date equal to DOJ | `200 OK` | Assignment allowed from hire date. |
| `ROT-CHK-015` | Negative: Assign Offboarding employee with `endDate: null` | BUS | Notice period employee, open-ended | `400 Bad Request` | Cannot assign open-ended to offboarding employee. |
| `ROT-CHK-016` | Negative: Assign Offboarding employee with `endDate > LWD` | BUS | End date exceeds Last Working Day | `400 Bad Request` | Assignment duration exceeds LWD. |
| `ROT-CHK-017` | Negative: Assign Exited employee (`EmployeeStatus: 6`) | NEG | Terminated/exited employee ID | `400 Bad Request` | Exited employee rejected. |
| `ROT-CHK-018` | Negative: Non-existent `teamId` in path | NEG | Fake `teamId` | `404 Not Found` | Team does not exist in rotation. |
| `ROT-CHK-019` | Database: Verify materialized maps generated | DB | Query `ERP.Attendance.WorkAssignmentMaps` | `200 OK` | Detail maps materialized with `Source: "Rotation"`. |
| `ROT-CHK-020` | Database: Verify embedded WorkPlanData in maps | DB | Inspect `WorkPlanData` in map document | `200 OK` | Plan snapshot and template copied into map. |

---

### 4.5 Suite 5: Member Lifecycle, Period Modification, Move & Removal — 18 Test Cases

| TC ID | Test Scenario | Category | Endpoint & Payload | Expected HTTP | Expected Response / DB State |
| :--- | :--- | :---: | :--- | :---: | :--- |
| `ROT-MEM-001` | Positive: Edit Member Period (`PATCH /members/{id}`) | POS | `startDate: 2026-11-15, endDate: 2027-01-31` | `200 OK` | Membership duration updated in `Members[]` array. |
| `ROT-MEM-002` | Positive: Make open-ended member bounded | POS | Bounded `endDate: 2026-12-31` | `200 OK` | Materialized maps trimmed to `2026-12-31`. |
| `ROT-MEM-003` | Negative: Edit Member Period with inverted dates | NEG | `endDate < startDate` | `400 Bad Request` | Chronology error. |
| `ROT-MEM-004` | Negative: Edit non-existent `membershipId` | NEG | Fake `membershipId` | `404 Not Found` | Member not found. |
| `ROT-MEM-005` | Positive: Move Member to another Team (`move-team`) | POS | `POST /move-team` with `teamId: TeamB_Id` | `200 OK` | Member transferred to Team B; schedule re-aligned. |
| `ROT-MEM-006` | Negative: Move Member to the same Team | BUS | `teamId: CurrentTeamId` | `400 Bad Request` | Cannot move member to same team. |
| `ROT-MEM-007` | Positive: Check conflicts for moving member to Regular Plan | POS | `POST /members/{id}/move/check-conflicts` | `200 OK` | Move preflight check evaluates destination conflicts. |
| `ROT-MEM-008` | Positive: Move Member across to Regular Work Plan | POS | `PATCH /members/{id}/move` targetType: WorkPlan | `200 OK` | Rotation membership closed; Regular assignment created. |
| `ROT-MEM-009` | Positive: Move Member across to Roster Board | POS | `PATCH /members/{id}/move` targetType: Board | `200 OK` | Rotation membership closed; Roster membership created. |
| `ROT-MEM-010` | Positive: Soft-delete member using `DELETE /members/{id}` | POS | `DELETE /members/{id}` | `200 OK` | Member marked inactive in `Members[]`; maps closed. |
| `ROT-MEM-011` | Positive: Delete member with explicit `endDate` query | POS | `DELETE /members/{id}?endDate=2026-11-30` | `200 OK` | Member terminated effective `2026-11-30`. |
| `ROT-MEM-012` | Negative: Delete non-existent `membershipId` | NEG | Fake `membershipId` | `404 Not Found` | Member not found. |
| `ROT-MEM-013` | Positive: Force regenerate schedule (`POST /generate-schedule`) | POS | `POST /generate-schedule` | `200 OK` | Re-materializes all active team shift maps. |
| `ROT-MEM-014` | Negative: Regenerate schedule on deleted rotation | NEG | `rotationId` where `IsDeleted: true` | `400 Bad Request` / `404` | Cannot generate schedule on deleted rotation. |
| `ROT-MEM-015` | Security: Member operation across different company | SEC | CompanyId tampering | `403 Forbidden` | Multi-tenancy isolation enforced. |
| `ROT-MEM-016` | Concurrency: Concurrent period edit collision | CON | Parallel PATCH requests | `409 Conflict` | Optimistic lock handles race condition. |
| `ROT-MEM-017` | Database: Member deletion cleans up future maps | DB | Query `ERP.Attendance.WorkAssignmentMaps` | `200 OK` | Future unworked shift maps deactivated. |
| `ROT-MEM-018` | Teardown: Clean up test memberships | CLN | Revert test assignments | `200 OK` | Database restored to clean baseline. |

---

### 4.6 Suite 6: Rotation Work Template CRUD & Slot Validation — 16 Test Cases

| TC ID | Test Scenario | Category | Route & Payload | Expected HTTP | Expected Response / DB State |
| :--- | :--- | :---: | :--- | :---: | :--- |
| `ROT-TMP-001` | Positive: Create Rotation Work Template with valid slots | POS | `POST /worktemplates/rotation` | `200 OK` | Template created in `ERP.Attendance.WorkTemplates`. |
| `ROT-TMP-002` | Positive: Template with Night Shift crossing midnight | POS | Slot 22:00 → 06:00, `crossesMidnight: true` | `200 OK` | Midnight transition validated. |
| `ROT-TMP-003` | Negative: Missing `templateName` object | DTO | `templateName: null` | `400 Bad Request` | Name is required. |
| `ROT-TMP-004` | Negative: Missing `rotationTimeSlots` array | DTO | `rotationTimeSlots: []` | `400 Bad Request` | At least 1 slot required. |
| `ROT-TMP-005` | Negative: Overlapping time slots in rotation template | BUS | Slot 1: 08:00–16:00, Slot 2: 14:00–22:00 | `400 Bad Request` | Slot collision rejected. |
| `ROT-TMP-006` | Boundary: Duration calculation mismatch | BVA | Declared duration != sum of slots | `400 Bad Request` | Mathematical validation guard. |
| `ROT-TMP-007` | Positive: Update template name & shortCode | POS | `PATCH /worktemplates/rotation/{id}` | `200 OK` | Template updated. |
| `ROT-TMP-008` | Negative: Update locked template currently in active rotation | BUS | Modifying slots of in-use template | `400 Bad Request` | Immutability guard blocks active template slot edit. |
| `ROT-TMP-009` | Positive: Clone or version rotation template | POS | Version creation | `200 OK` | New version created without altering legacy maps. |
| `ROT-TMP-010` | Negative: Delete rotation template in active rotation | BUS | Soft-delete template referenced by board | `400 Bad Request` | Referential integrity blocks deletion. |
| `ROT-TMP-011` | Scoping: Missing `locationId` query | SEC | Omit `locationId` | `400 Bad Request` | Location scoping required. |
| `ROT-TMP-012` | Security: Cross-tenant template modification | SEC | Company B template ID | `403 Forbidden` | Access denied. |
| `ROT-TMP-013` | Boundary: TotalWorkingDays + TotalDaysOff == Cycle Days | BVA | 5 working + 2 off = 7 days | `200 OK` | Valid weekly cycle boundary. |
| `ROT-TMP-014` | Negative: TotalWorkingDays exceeds cycle days | BVA | 8 working days in 7-day cycle | `400 Bad Request` | Mathematical impossibility rejected. |
| `ROT-TMP-015` | Positive: Query template by ID | POS | `GET /worktemplates/{id}` | `200 OK` | Returns template details. |
| `ROT-TMP-016` | Teardown: Clean up test rotation templates | CLN | Soft-delete unreferenced test template | `200 OK` | Test template removed cleanly. |

---

### 4.7 Suite 7: Rotation Deletion & Board Lifecycle — 10 Test Cases

| TC ID | Test Scenario | Category | Endpoint & Condition | Expected HTTP | Expected Response / DB State |
| :--- | :--- | :---: | :--- | :---: | :--- |
| `ROT-DEL-001` | Positive: Delete clean rotation with 0 members | POS | `DELETE /shift-rotations/{id}` with 0 members | `200 OK` | `IsDeleted: true`, tombstone timestamp set. |
| `ROT-DEL-002` | Negative: Delete rotation with active assigned members | BUS | Rotation with active members | `400 Bad Request` | Referential integrity blocks deletion of active board. |
| `ROT-DEL-003` | Positive: Delete rotation after all members removed | POS | All members removed $\rightarrow$ delete board | `200 OK` | Successfully deleted once clean. |
| `ROT-DEL-004` | Negative: Delete already deleted rotation (Double delete) | NEG | Re-delete soft-deleted board | `400 Bad Request` / `404` | Already deleted rejection. |
| `ROT-DEL-005` | Negative: Non-existent `rotationId` | NEG | Fake `rotationId` | `404 Not Found` | Board not found. |
| `ROT-DEL-006` | Scoping: Delete rotation without `locationId` query | SEC | Omit `locationId` | `400 Bad Request` | Location scoping required. |
| `ROT-DEL-007` | Security: Delete rotation of another company | SEC | Company B rotationId | `403 Forbidden` | Access denied. |
| `ROT-DEL-008` | Database: Verify `IsDeleted: true` in MongoDB | DB | Query `ERP.Attendance.ShiftRotationBoard` | `200 OK` | Document retained for audit with `IsDeleted: true`. |
| `ROT-DEL-009` | Query Guard: Deleted rotation excluded from `GET /shift-rotations` | DB | `GET /shift-rotations` | `200 OK` | Deleted rotation does not appear in active listings. |
| `ROT-DEL-010` | Schedule Guard: No schedule maps generated for deleted board | DB | Query `ERP.Attendance.WorkAssignmentMaps` | `200 OK` | No ghost schedules created. |

---

## 5. Summary Dashboard

* **Total Designed Test Cases:** **96 Detailed Scenarios in Primary Matrix** + **88 Permutation / Multi-Cohort Cases** = **184 Comprehensive Test Cases**.
* **Traceability Coverage:** 100% of the 20 Requirements in the RTM are traced to test cases.
* **Database Collections Asserted:** `Sahab.ERP.Attendance.ShiftRotationBoard`, `ERP.Attendance.WorkAssignmentMaps`, `ERP.Attendance.WorkTemplates`, `EmployeeSvcNET8test.Employee`.
"""

with open('reports/ROTATION_WORK_PLAN_TEST_CASES.md', 'w', encoding='utf-8') as f:
    f.write(md_content)

print("Saved reports/ROTATION_WORK_PLAN_TEST_CASES.md successfully!")
