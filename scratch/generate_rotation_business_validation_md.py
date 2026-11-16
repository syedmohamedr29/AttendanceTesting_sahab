# -*- coding: utf-8 -*-
"""
Generate ROTATION_WORK_PLAN_BUSINESS_VALIDATION.md
Comprehensive Business Validation, State Machine, and DTO Specification for Shift Rotations
"""

content = """# Shift Rotation & Rotation Work Plan: Business Validation & Architecture Specification

**Target Microservices:** `SP.AttendanceSvc` (.NET 9 / ASP.NET Core) & `SP.EmployeeSvc` (.NET 8)  
**Database Collections:** `Sahab.ERP.Attendance.ShiftRotationBoard` & `Sahab.ERP.Attendance.WorkAssignmentMaps`  
**Document Purpose:** Defines all architectural rules, state machine transitions, DTO validation criteria, and invariant assertions for Shift Rotation Work Plans.

---

## 1. Architectural Model & Domain Invariants

A Shift Rotation represents a cyclical multi-team work plan. The system architecture enforces the following key invariants:

```mermaid
flowchart TD
    Board["ShiftRotationBoard\n(ERP.Attendance.ShiftRotationBoard)"]
    Board --> Plans["Plans[]\n(Embedded Rotation Work Plans)"]
    Board --> Steps["Steps[]\n(Sequence of Steps)"]
    Board --> Teams["Teams[]\n(Rotation Teams)"]
    Board --> Members["Members[]\n(Assigned Employees)"]
    
    Plans --> WT["WorkTemplate\n(Fixed / Rotation Type)"]
    Plans --> Policies["Policies[]\n(Break, OT, Grace)"]
    
    Teams --> StartSeq["StartSequenceOrder\n(1, 2, ... N)"]
    
    Members --> ScheduleMaps["Materialized Shift Maps\n(ERP.Attendance.WorkAssignmentMaps\nSource: 'Rotation')"]
```

---

## 2. DTO Validation Matrix & Schema Rules

### 2.1 `ShiftRotationDto` (Create Rotation)

| Field Name | Type | Required | Business Constraints & Validation Rules | Failure Code |
| :--- | :---: | :---: | :--- | :--- |
| `rotationName` | `Object` | **Yes** | Multilingual dictionary (`en` mandatory, `ar` optional). Min 2 chars, max 100 chars. Empty strings rejected. | `Cit.Attendance:Validation` |
| `plans` | `Array` | **Yes** | Array of `RotationPlanDto`. Must contain at least **1 plan**, maximum **10 plans**. | `Cit.Attendance:Validation` |
| `patternType` | `Enum` | **Yes** | Must be either `"Alternating"` (1) or `"Uneven"` (2). `"NotApplicable"` or invalid strings rejected. | Schema Binding Error |
| `weeksPerStep` | `Int32` | **Cond.** | When `patternType == "Alternating"`, must be integer between **1 and 52**. Values <= 0 or > 52 rejected. | `Cit.Attendance:Validation` |
| `steps` | `Array` | **Yes** | Array of `RotationStepDto`. Must contain at least **1 step**, maximum **52 steps**. | `Cit.Attendance:Validation` |
| `teams` | `Array` | **Yes** | Array of `RotationTeamDto`. Must contain at least **1 team**, maximum **20 teams**. | `Cit.Attendance:Validation` |

---

### 2.2 `RotationPlanDto` (Embedded Plan)

| Field Name | Type | Required | Business Constraints & Validation Rules | Failure Code |
| :--- | :---: | :---: | :--- | :--- |
| `planIndex` | `Int32` | **Yes** | Positive integer starting at **1**. Must be unique within the `plans[]` array. | `Cit.Attendance:Validation` |
| `workPlanName` | `Object` | **Yes** | Multilingual plan name (`en` required). | `Cit.Attendance:Validation` |
| `workTemplateId` | `UUID` | **Yes** | Must reference an existing, non-deleted `WorkTemplate` in `ERP.Attendance.WorkTemplates`. | `Cit.Attendance:1201` |
| `isBreakPolicyEnabled` | `Boolean` | No | If `true`, optional break policy attached. | N/A |
| `isOvertimePolicyEnabled`| `Boolean` | No | If `true`, optional overtime policy attached. | N/A |
| `isGracePeriodPolicyEnabled`| `Boolean` | No | If `true`, optional grace period policy attached. | N/A |
| `policyIds` | `Array` | No | If policies enabled, must reference valid policy UUIDs matching company and location. | `Cit.Attendance:1501` |

---

### 2.3 `RotationStepDto` (Sequence Step)

| Field Name | Type | Required | Business Constraints & Validation Rules | Failure Code |
| :--- | :---: | :---: | :--- | :--- |
| `planIndex` | `Int32` | **Yes** | Must match an existing `planIndex` declared in `plans[]`. Referencing an undeclared index is blocked. | `Cit.Attendance:1301` |
| `durationWeeks` | `Int32` | **Cond.** | Mandatory when `patternType == "Uneven"` (must be >= 1). Ignored/null when `patternType == "Alternating"`. | `Cit.Attendance:Validation` |

---

### 2.4 `RotationTeamDto` (Team Definition)

| Field Name | Type | Required | Business Constraints & Validation Rules | Failure Code |
| :--- | :---: | :---: | :--- | :--- |
| `teamName` | `Object` | **Yes** | Multilingual team name (`en` required, e.g. "Team Alpha"). Must be unique within rotation. | `Cit.Attendance:Validation` |
| `startSequenceOrder` | `Int32` | **Yes** | 1-based order index. Defines which step the team starts on. Must be unique across teams. | `Cit.Attendance:Validation` |

---

### 2.5 `AddRotationEmployeesDto` (Team Assignment)

| Field Name | Type | Required | Business Constraints & Validation Rules | Failure Code |
| :--- | :---: | :---: | :--- | :--- |
| `employeeIds` | `Array` | **Yes** | Array of valid Employee UUIDs. Cannot be empty. All employees must be **Active** (`IsActive: true`). | `Cit.Attendance:Validation` |
| `startDate` | `Date` | **Yes** | `YYYY-MM-DD`. Must be >= Employee Date of Joining (`DOJ`). Past dates rejected unless permitted. | `Cit.Attendance:1405` |
| `endDate` | `Date` | No | Optional end date. Must be >= `startDate`. For offboarding employees, cannot exceed `LWD`. | `Cit.Attendance:Validation` |
| `adjustConflicts` | `Boolean` | **Yes** | If `true`, automatically trims/splits overlapping Regular assignments. If `false`, rejects on conflict. | `Cit.Attendance:Conflict` |

---

## 3. Core Business Rules & Invariants

### Rule 1: Location & Company Isolation
* All embedded Work Templates, Policies, and assigned Employees must belong to the **exact same CompanyId and LocationId** as the Shift Rotation Board. Cross-location assignments must be rejected with `HTTP 400 Bad Request`.

### Rule 2: Template Type Compatibility
* Embedded Work Templates must have `TemplateType` equal to `FixedShift` or `Rotation`. Incompatible template types (e.g. `Flexible`, `SplitShift`, `Unscheduled`) must be strictly rejected.

### Rule 3: Single Schedule Invariant
* An employee can belong to only **one active Rotation Team or Roster Board** on any given calendar date. If an employee is already on a Roster Board or another Rotation, the assignment is blocked as a Hard Conflict (`isBlocked: true`).

### Rule 4: Regular Plan Trimming (Soft Conflict)
* If an employee has an existing open-ended Regular Work Plan assignment, assigning them to a Rotation with `adjustConflicts: true` automatically truncates the Regular assignment to end on `startDate - 1 day` (`EndsEarly`), prioritizing the Rotation schedule.

### Rule 5: Deletion Safeguards
* Executing `DELETE /shift-rotations/{rotationId}` on a rotation that has active members assigned must be blocked with `400 Bad Request` until all members are unassigned or moved.
"""

with open('reports/ROTATION_WORK_PLAN_BUSINESS_VALIDATION.md', 'w', encoding='utf-8') as f:
    f.write(content)

print("Saved reports/ROTATION_WORK_PLAN_BUSINESS_VALIDATION.md successfully!")
