# Rotation Work Assignment Business Domain & DTO Validation Reference

**Microservices:** `SP.AttendanceSvc` (.NET 9) & `SP.EmployeeSvc` (.NET 8)  
**Collections:** `Sahab.ERP.Attendance.ShiftRotationBoard`, `ERP.Attendance.WorkAssignmentMaps`, `EmployeeSvcNET8test.Employee`  
**Author:** Antigravity Senior QA Automation & Architecture Specialist  

---

## 1. Domain Rules & Invariants for Rotation Work Assignments

### Rule 1: Cross-Location Physical Isolation Guard
- An employee whose assigned `workLocation` (`CompanyLocationId`) in `SP.EmployeeSvc` is Dammam can **never** be enrolled in a Jeddah or Riyadh rotation board.
- The preflight check `POST /check-conflicts` and commit `POST /employees` must cross-reference `Employee.CompanyLocationId` against `ShiftRotationBoard.LocationId`.
- Violations must be rejected with `400 Bad Request` (`Cit.Attendance:Validation` / 'Employee does not belong to rotation work location').

### Rule 2: Employee Active Status Requirement
- Only employees with `IsActive == true` and `Status == 2` in `EmployeeSvcNET8test.Employee` can be enrolled.
- Inactive (`IsActive: false`) or offboarded (`Status: 3`) employees must be rejected with `HTTP 400 Bad Request`.
- The system must **never** return `HTTP 200 OK` with an empty enrollment payload when inactive employees are submitted.

### Rule 3: Conflict Auto-Resolution (adjustConflicts)
- If an employee has an existing active regular work plan or rotation assignment:
  - `adjustConflicts == false`: Enrollment blocked with `400 Bad Request` (`Cit.Attendance:1409`).
  - `adjustConflicts == true`: System auto-truncates existing plan's `EndDate` to `newStartDate - 1 day` and creates rotation membership.

### Rule 4: Schedule Map Materialization & Idempotency
- Invoking `POST /generate-schedule` generates sequential daily shift instances in `Sahab.ERP.Attendance.WorkAssignmentMaps`.
- Maps are tagged with `Source: "Rotation"`, `RotationId`, `TeamId`, `WorkPlanId`, `StartDate`, `EndDate`, and `IsActive: true`.
- Re-executing generation must be **100% idempotent** (0 duplicate maps created).

### Rule 5: Active Member Deletion Guard
- A rotation board **cannot** be deleted while active members exist in its `Members[]` array.
- Deletion attempts must be rejected with `400 Bad Request` (`Cit.Attendance:2005`). All members must be removed or transferred first.

---

## 2. Complete DTO Field Matrix & Constraints

| DTO Name | Property | Type | Nullable | Required | Valid Range / Constraints |
| :--- | :--- | :---: | :---: | :---: | :--- |
| `AddRotationEmployeesDto` | `employeeIds` | Array<UUID> | No | Yes | Non-empty array of active employee UUIDs |
| `AddRotationEmployeesDto` | `startDate` | DateString | No | Yes | ISO Date `YYYY-MM-DD`. Valid calendar date |
| `AddRotationEmployeesDto` | `endDate` | DateString | Yes | No | ISO Date `YYYY-MM-DD`. Must be >= `startDate` |
| `AddRotationEmployeesDto` | `adjustConflicts` | Boolean | No | Yes | `true` to auto-resolve, `false` to enforce block |
| `EditRotationMemberPeriodDto` | `startDate` | DateString | No | Yes | ISO Date `YYYY-MM-DD` |
| `EditRotationMemberPeriodDto` | `endDate` | DateString | Yes | No | ISO Date `YYYY-MM-DD`. Must be >= `startDate` |
| `EditRotationMemberPeriodDto` | `adjustConflicts` | Boolean | No | Yes | Conflict resolution flag |
| `MoveRotationMemberTeamDto` | `teamId` | UUID | No | Yes | Target team in SAME rotation board |
| `MoveRotationMemberTeamDto` | `effectiveFrom` | DateString | No | Yes | Effective transition date `YYYY-MM-DD` |
| `MoveEmployeeDto` | `targetType` | Enum | No | Yes | `Board`, `WorkPlan`, or `Rotation` |
| `MoveEmployeeDto` | `targetBoardId` | UUID | Yes | Cond. | Target board GUID if moving to board |
| `MoveEmployeeDto` | `targetWorkPlanId` | UUID | Yes | Cond. | Target work plan GUID if moving to regular plan |
| `MoveEmployeeDto` | `targetRotationId` | UUID | Yes | Cond. | Target rotation GUID if moving to rotation |
| `MoveEmployeeDto` | `targetTeamId` | UUID | Yes | Cond. | Target team GUID in target rotation |
| `MoveEmployeeDto` | `effectiveFrom` | DateString | No | Yes | Effective transition date |
| `MoveEmployeeDto` | `endDate` | DateString | Yes | No | Optional termination date |
| `MoveEmployeeDto` | `adjustConflicts` | Boolean | No | Yes | Conflict resolution flag |