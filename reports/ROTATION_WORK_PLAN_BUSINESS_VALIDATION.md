# Shift Rotation & Rotation Work Plan Business Domain & DTO Validation Reference

**Microservices:** `SP.AttendanceSvc` (.NET 9) & `SP.EmployeeSvc` (.NET 8)  
**Database:** MongoDB `Sahab` (`ERP.Attendance.ShiftRotationBoard`, `ERP.Attendance.WorkAssignmentMaps`, `ERP.Attendance.WorkTemplates`)  
**Author:** Antigravity Senior QA Automation & Architecture Specialist  

---

## 1. Domain Validation Rules & Invariants

### Rule 1: Pattern Type & Duration Math
- **Alternating (`patternType = 1`):** Every step in the rotation executes for exactly `weeksPerStep` weeks. Total cycle length = `len(steps) * weeksPerStep` weeks.
- **Uneven (`patternType = 2`):** Each step executes for its specific `durationWeeks`. Total cycle length = `sum(step.durationWeeks for step in steps)` weeks.
- **Boundary Constraints:** `weeksPerStep` in `[1, 52]`. Step `durationWeeks` in `[1, 52]`. Values `<= 0` or `> 52` must be rejected with `400 Bad Request`.

### Rule 2: Three-Tier Referential Integrity
- **Plan Index Mapping:** Every step in `steps[]` must reference a valid `planIndex` defined in `plans[]`. Referencing an undeclared index is an unrecoverable validation error (`400 Bad Request`).
- **Team Sequence Mapping:** Each team in `teams[]` must have a unique `startSequenceOrder` in range `[1, len(steps)]`. Duplicate sequence orders cause concurrent shift collisions.

### Rule 3: Work Template Compatibility
- Only Work Templates of type `Fixed` or `Rotation` can be bound to a rotation plan. Flexible work templates (`templateType = Flexi`) cannot be scheduled in a cyclic rotation and must be rejected.

### Rule 4: Employee Lifecycle & Cross-Location Isolation
- **Active Status Requirement:** Only employees with `IsActive == true` and `Status == 2` in `SP.EmployeeSvc` can be assigned to rotation teams. Inactive or offboarded employees must be rejected.
- **Strict Location Isolation:** Employees can ONLY be assigned to rotation boards matching their assigned `workLocation` (`CompanyLocationId`). Cross-location assignment (e.g. Dammam employee assigned to Jeddah rotation) violates multi-facility physical attendance rules and must be strictly rejected.

### Rule 5: Conflict Resolution & Map Synchronization
- When assigning an employee with an existing active assignment:
  - If `adjustConflicts == false`: Assignment rejected with `400 Bad Request` and detailed conflict array.
  - If `adjustConflicts == true`: System auto-truncates existing assignment `EndDate` to `newStartDate - 1 day` and materializes rotation schedule maps.
- Removing a member from rotation truncates `Sahab.ERP.Attendance.WorkAssignmentMaps` documents starting from `endDate`.

---

## 2. Complete DTO Field Matrix & Constraints

| DTO Name | Property | Type | Nullable | Required | Valid Range / Constraints |
| :--- | :--- | :---: | :---: | :---: | :--- |
| `ShiftRotationDto` | `tenantName` | LocalizedString | No | No | Localized tenant identifier (`en`, `ar`) |
| `ShiftRotationDto` | `rotationName` | LocalizedString | No | Yes | English & Arabic names (1 - 200 chars) |
| `ShiftRotationDto` | `patternType` | Enum | No | Yes | `Alternating` (1) or `Uneven` (2) |
| `ShiftRotationDto` | `weeksPerStep` | Integer | Yes | Cond. | Required if `patternType == Alternating`. Range: `1 - 52` |
| `ShiftRotationDto` | `plans` | Array | No | Yes | Min 1 element. Unique `planIndex` >= 1 |
| `ShiftRotationDto` | `steps` | Array | No | Yes | Min 1 element. Valid `planIndex` references |
| `ShiftRotationDto` | `teams` | Array | No | Yes | Min 1 element. Unique `startSequenceOrder` |
| `RotationStepDto` | `planIndex` | Integer | No | Yes | References declared `planIndex` in `plans` |
| `RotationStepDto` | `durationWeeks`| Integer | Yes | Cond. | Required if `patternType == Uneven`. Range: `1 - 52` |
| `AddRotationEmployeesDto` | `employeeIds` | Array<UUID> | No | Yes | Non-empty array of active employee UUIDs |
| `AddRotationEmployeesDto` | `startDate` | DateString | No | Yes | ISO Date `YYYY-MM-DD`. Valid calendar date |
| `AddRotationEmployeesDto` | `endDate` | DateString | Yes | No | ISO Date `YYYY-MM-DD`. Must be >= `startDate` |
| `AddRotationEmployeesDto` | `adjustConflicts` | Boolean | No | Yes | `true` to auto-resolve, `false` to enforce block |
| `MoveEmployeeDto` | `targetType` | Enum | No | Yes | `Board`, `WorkPlan`, or `Rotation` |
| `MoveEmployeeDto` | `effectiveFrom` | DateString | No | Yes | ISO Date `YYYY-MM-DD` |
| `RotationWorkTemplateDto` | `shortCode` | String | No | Yes | Unique alphanumeric code within company |
| `RotationWorkTemplateDto` | `rotationTimeSlots` | Array | No | Yes | Min 1 slot. Sum of work/rest days must be 7 |