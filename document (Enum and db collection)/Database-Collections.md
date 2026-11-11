# Attendance 2: Database Collections

The MongoDB collections that the Attendance 2 service (`SP.AttendanceSvc`) reads and writes. The
list is built from the collection map in `appsettings.json` and from the entity classes on `main`,
as deployed in `dev300-1.0.2` (23 Oct 2026).

## Where the data lives

| | DEV |
|---|---|
| Server | `10.1.0.4:27018` |
| Database | `Sahab` (the shared DEV ERP database) |
| Collection prefix | `ERP.Attendance.*`, with the attendance-log pipeline under `ERP.Attendance.Log.*` |

Attendance 1 (`ZW.AttendanceSvc`, the payroll-facing service) has its own collections. Nothing in
this document applies to it.

## Conventions you will see in every document

| Convention | What it means when you query |
|---|---|
| `_id` and every id field are GUIDs stored as **UUID subtype 4** | In Compass or mongosh, query with `UUID("3f2c…")`. A GUID copied from another service's data (subtype 3, different byte order) matches nothing, and no error is raised |
| `TenantId` on every document | Every read and write is filtered by the tenant in the caller's token. Data from another tenant is never returned |
| `CompanyId`, and `LocationId` on location-scoped data | Every API route carries `companyId`; most location data also needs `locationId` |
| Names are dictionaries | `{ "en": "Morning Shift", "ar": "…" }` |
| Enums are stored as **numbers** | See [Enum-List.md](Enum-List.md) for the values |
| `DateOnly` fields are stored as dates at midnight UTC; `TimeOnly` as `"HH:mm:ss"` strings; durations (`TimeSpan`) as tick counts | |
| Audit fields | `CreatedAt`, `CreatedBy`, `ModifiedAt`, `ModifiedBy` are set by the server from the caller's token. No request accepts them |
| Soft delete | Most master data is never physically removed. Look for `IsDeleted = true`, `IsActive = false` or `Status = Archived` |
| Polymorphic collections | `_t` holds the sub-type (for example `RosterWorkPlan`). The `Type` column below tells you which values to expect |

---

## Summary

| # | Collection | Module | One document is… |
|---|---|---|---|
| 1 | `ERP.Attendance.WorkTemplates` | Work Templates | One work template (or one saved version of the company default) |
| 2 | `ERP.Attendance.WorkPlans` | Work Plans | One work plan: regular, roster shift or rotation plan |
| 3 | `ERP.Attendance.WorkAssignments` | Work Assignments | One assignment header: a plan, a period and a location |
| 4 | `ERP.Attendance.WorkAssignmentMaps` | Work Assignments / Roster / Rotation | One employee's assignment row (regular period, one roster day, or one rotation step window) |
| 5 | `ERP.Attendance.Policies` | Policies | One break, grace period or overtime policy |
| 6 | `ERP.Attendance.HolidayCalendars` | Holiday Calendars | One company or location holiday calendar |
| 7 | `ERP.Attendance.Configs` | Employee Exceptions | One employee exempted from attendance for a period |
| 8 | `ERP.Attendance.RosterBoards` | Roster Boards | One roster board with its members, shifts and areas |
| 9 | `ERP.Attendance.EmployeeRosterAssignments` | Roster Boards | One employee × board × shift association |
| 10 | `ERP.Attendance.RosterSchedulePeriods` | Roster Planner | The publish state of one board for one period |
| 11 | `ERP.Attendance.ShiftRotationBoard` | Shift Rotations | One shift rotation with its teams, pattern and members |
| 12 | `ERP.Attendance.Log.AttGlobalSessionMaster` | Attendance Log | One import session (pay period × location × pay group) and its files |
| 13 | `ERP.Attendance.Log.DailyProcessedL3` | Attendance Log | One employee's daily records for one pay period |
| 14 | `ERP.Attendance.Log.MonthlyLogL4` | Attendance Log | One employee's monthly summary for one pay period |
| 15 | `ERP.Attendance.Log.MonthlySummaryForPayrollL5` | Attendance Log (legacy) | One employee's payroll summary for one pay period |
| 16 | `ERP.Attendance.Log.EmpAttProcessState` | Attendance Log | One employee's processing state in one session |
| 17 | `ERP.Attendance.Log.Errors` | Attendance Log | One upload, import or processing error |
| 18 | `ERP.Attendance.Log.AttGlobalConfig` | Attendance Log | The attendance-log configuration of one company |
| 19 | `ERP.Attendance.Log.RawBiometricL1` | Attendance Log (not in use) | Raw biometric punches |
| 20 | `ERP.Attendance.Log.FirstEntryLastExitL2` | Attendance Log (not in use) | First entry and last exit per day |
| 21 | `fs.files` / `fs.chunks` | Attendance Log | GridFS storage of the uploaded CSV files |
| 22 | `EmployeeEnrollments` | Owned by the HR / Employee service | One employee's enrolment. **Read-only for Attendance 2** |
| 23 | `ERP.Attendance._ReleaseMigration` | Release migration | One run of the release migration script |

---

## Master data

### 1. `ERP.Attendance.WorkTemplates`

A work template defines working days, timings and hours.

| | |
|---|---|
| `_t` values | `FixedWorkTemplate`, `FlexiWorkTemplate`, `SplitWorkTemplate`, `RosterWorkTemplate`, `RotationWorkTemplate` |
| Key fields | `WorkTemplateName`, `ShortCode`, `TemplateType`, `Status`, `IsDefault`, `LocationId` (empty GUID = company template), `TotalWorkDurationInMinutes`, `TotalWorkingDays`, `TotalDaysOff`, `Version`, `IsDeleted`, `IsArchivable`, `IsEditable`, `TimeZoneId`, `ChangeLog[]` |
| Company default versioning | Editing the company default creates a **new document** and marks the old one `IsSuperseded = true`. `HasPendingLocSync` and `IsCompanyLinked` drive the "apply to locations" banner |
| Type-specific fields | `FixedTimeSlots`, `FlexiTimeSlots` + `FlexibleType`, `SplitTimeSlots`, `RosterTimeSlots` + `Colour`, `RotationTimeSlots` |
| Written by | `/worktemplates/*`, and `POST/PATCH /workplans/roster` (a roster shift creates its template) |
| Rules worth testing | `ShortCode` is upper-case, unique per company and cannot change after creation. Only the company default can have `IsDefault = true` |

### 2. `ERP.Attendance.WorkPlans`

A work plan combines a work template with policies.

| | |
|---|---|
| `_t` values | `RegularWorkPlan`, `RosterWorkPlan`, `RotationWorkPlan`. Older documents with no `_t` are read as regular |
| Key fields | `WorkPlanName`, `Description`, `PlanType`, `LocationId`, `IsDefault` (the location default plan), `IsDeleted`, `WorkTemplate` (an **embedded copy** of the template), `Policies[]` (embedded copies), `IsBreakPolicyEnabled`, `IsOvertimePolicyEnabled`, `IsGracePeriodPolicyEnabled` |
| Type-specific fields | Roster: `BoardId`. Rotation: `RotationId`, `PlanIndex` |
| Written by | `/workplans/*`, `/shift-rotations/*` (rotation plans) |
| Note | The embedded template and policies are snapshots. Editing a template or policy does not change existing plans until the plan itself is updated |

### 3. `ERP.Attendance.WorkAssignments`

The header of a regular assignment: which plan, at which location, for which period.

| | |
|---|---|
| Key fields | `WorkPlanId`, `WorkPlanName`, `LocationId`, `StartDate`, `EndDate` (null = open-ended), `Status`, `IsActive` |
| Written by | `POST /workassignments`, `POST /workassignments/adjust`, moves between plans |
| Note | The per-employee rows live in `WorkAssignmentMaps` and point back through `WorkAssignmentId` |

### 4. `ERP.Attendance.WorkAssignmentMaps`

One employee's assignment. This is the collection the rest of the platform reads to find out which
plan an employee is on. **It is the only source of an employee's location for attendance.**

| | |
|---|---|
| `_t` values | `RegularWorkAssignmentMap`, `RosterWorkAssignmentMap`, `RotationWorkAssignmentMap`. No `_t` = regular |
| Key fields | `AssignmentType`, `EmployeeId`, `EmployeeCode`, `EmployeeName`, `Department`, `Designation`, `Nationality`, `ReportingTo`, `HRPartner`, `LocationId`, `StartDate`, `EndDate`, `Status`, `IsActive`, `WorkAssignmentId`, `HolidayCalendarId`, `WorkPlanData` (embedded copy of the plan) |
| Regular row | One document per employee per assignment period |
| Roster row | **One document per employee per scheduled day** (`StartDate` = `EndDate` = the day). `RosterAssignment` holds `RosterBoardId`, `BoardName`, `MembershipId`, `Area`. A Day Off is a roster row with no work plan |
| Rotation row | One document per employee per rotation step window. `RotationAssignment` holds `RotationId`, `TeamId`, `MembershipId`, `PlanIndex`, `SequenceOrder`, `CycleNumber`, `IsPartial` |
| Written by | Work assignment create, edit, remove, move; roster assign, clear, copy, area changes; rotation enrol, generate, move, remove |
| Rules worth testing | One employee cannot hold two overlapping commitments. A regular assignment can be adjusted around a new one after confirmation; roster and rotation overlaps are refused |

### 5. `ERP.Attendance.Policies`

| | |
|---|---|
| `_t` values | `BreakPolicy`, `GracePeriodPolicy`, `OvertimePolicy` |
| Key fields | `Name`, `Type`, `IsActive` (false = deleted) |
| Break | `Breaks[]` (paid or unpaid, with durations), `TotalBreakDurationInMinutes`, `TotalPaidBreakDurationInMinutes`, `TotalUnpaidBreakDurationInMinutes` |
| Grace period | `LateCheckInGraceMinutes`, `EarlyCheckOutGraceMinutes`, `DeviationThreshold`, `DeviationPeriod`, `DeductLeaveFrom`, `DeductionDays` |
| Overtime | `OvertimeRule`, `HasBufferBeforeOvertime`, `BufferMinutes`, `Rates[]` (one per day type) |
| Written by | `/attpolicies/*` |

### 6. `ERP.Attendance.HolidayCalendars`

| | |
|---|---|
| Key fields | `Name`, `ShortCode`, `CalendarType` (CompanyDefault or LocationDefault), `LocationId`, `IsInherited` (location still follows the company), `IsPublished`, `LastPublishedOn`, `IsLocked`, `IsActive`, `IsDeleted`, `YearlyCalendar` (`Year` + `HolidayLists[]`) |
| Written by | `/holidaylist/*` |
| Rules worth testing | Publishing pushes the company holidays to every location with `IsInherited = true`. Customising a location sets `IsInherited = false`, after which it no longer receives published changes. Publishing is allowed for the current or the next year only |

### 7. `ERP.Attendance.Configs` (Employee Exceptions)

| | |
|---|---|
| Key fields | `EmployeeId`, `EmployeeCode`, `EmployeeName`, `Email`, `DepartmentId/Name/Code`, `DesignationId/Name/Code`, `EffectiveFrom`, `EffectiveTo`, `IsActive` |
| Written by | `/config/attendance/employee-exemp/*` |

---

## Roster and rotation

### 8. `ERP.Attendance.RosterBoards`

| | |
|---|---|
| Key fields | `BoardName`, `LocationId`, `Supervisor`, `PublishingFrequency`, `HasAreas`, `IsDeleted` |
| `Employees[]` | Board membership rows: `_id` (the **membershipId** used in URLs), `EmployeeId`, `EmployeeCode`, `EmployeeName`, `Department`, `Designation`, `AreaId`, `PeriodStartDate`, `PeriodEndDate`. One employee can have several rows for different periods |
| `WorkPlans[]` | The board's shift palette: `WorkPlanId`, `WorkPlanName`, embedded template and policies |
| `Areas[]` | `AreaId`, `AreaName`, `Order` |
| Written by | `/roster-boards/*`, roster shift create and edit, roster deletes |
| Note | The membership row owns the area. Each scheduled roster day in `WorkAssignmentMaps` carries a copy, and every area change re-syncs those copies |

### 9. `ERP.Attendance.EmployeeRosterAssignments`

| | |
|---|---|
| One document | One employee × board × shift. It records **that** an employee has been given a shift on a board, not **when** |
| Key fields | `BoardId`, `MembershipId`, `EmployeeId`, `WorkPlanId`, `AreaId`, `EmployeeCode`, `EmployeeName`, `WorkPlanName`, `ShortCode`, `Colour` |
| Written by | Roster assign, clear and copy; board and shift deletes |

### 10. `ERP.Attendance.RosterSchedulePeriods`

| | |
|---|---|
| One document | One board × one period. Created only when a period is first published |
| Key fields | `BoardId`, `Frequency`, `PeriodStart`, `PeriodEnd`, `PeriodLabel`, `Status` (Draft or Published), `Version`, `PublishedAt/By`, `UnpublishedAt/By`, `RepublishRequired`, `LastChangedAt`, `PublishedSlotCount`, `PublishedEmployeeCount`, `IsDeleted` |
| Written by | Publish and unpublish. Assign, clear, copy, membership edits and shift edits set `RepublishRequired = true` on a published period |

### 11. `ERP.Attendance.ShiftRotationBoard`

| | |
|---|---|
| Key fields | `RotationName`, `LocationId`, `PatternType`, `WeeksPerStep`, `IsDeleted` |
| `Plans[]` | Snapshots of the rotation's work plans (the plans themselves are `RotationWorkPlan` documents in `WorkPlans`) |
| `Teams[]` | `TeamId`, `TeamName`, `DisplayOrder`, `RotationPattern[]` (the team's sequence of plans; all indexes are 1-based) |
| `Members[]` | `_id` (the **membershipId**), `TeamId`, `EmployeeId`, `EmployeeCode`, `EmployeeName`, `Department`, `Designation`, `PeriodStartDate`, `PeriodEndDate`, `GeneratedThrough` (how far the schedule has been generated) |
| Written by | `/shift-rotations/*` |
| Note | A rotation has no start date of its own. Each member cycles from their own start date |

---

## Attendance log pipeline

The pipeline runs **upload → import → process → publish**, one session per pay period, location and
pay group. A pay period runs from the 16th of one month to the 15th of the next. Its key looks like
`Sep16_2026_to_Oct15_2026` and is the `SessionKey` field below.

### 12. `ERP.Attendance.Log.AttGlobalSessionMaster`

| | |
|---|---|
| Key fields | `SessionId`, `SessionKey`, `Month`, `Year`, `PayGroupId`, `LocationId`, `DeclaredLevel`, `State`, `FinalisedAt`, `PublishedAt`, `UploadedBy`, `UploadedAt` |
| `Files[]` | `FileId` (GridFS id), `FileName`, `SizeBytes`, `Status`, `IssueCount`, `ValidationResult`, `ImportStats` |
| Progress | `ImportProgress` (stage, row counts), `ProcessingProgress` (stage, employee counts) |
| Lock | `ActiveOperation`, `OperationOwnerId`, `OperationExpiresAt`. While a lock is held, a second upload, import, process or delete on the same session is refused |

### 13. `ERP.Attendance.Log.DailyProcessedL3`

| | |
|---|---|
| One document | One employee for one pay period |
| Key fields | `SessionKey`, `DailyKey`, `PeriodStart`, `PeriodEnd`, `EmployeeInfo` (name, code), `EnrollmentRef` (`EmployeeId`, `PayGroupId`, `DateOfJoining`), `Summary` |
| `AttendanceRecords[]` | One row per day: `WorkDate`, `Status` (L3RecordStatus), `DayType`, `AttendanceTags[]`, `LeaveDetails`, `HolidayDetails`, `FileDayType`, `FileAttendanceStatus`, and `Record` (shift start and end, required hours, entry and exit, hours worked, late, early, shortfall, deduction, normal / weekend / holiday / total extra hours, `RuleApplied`, notes) |
| Written by | Import, every L3 edit API (edit, regularize, mark day off or holiday, overrides, clear), settle and unsettle |
| Indexes | Created at service start-up |

### 14. `ERP.Attendance.Log.MonthlyLogL4`

| | |
|---|---|
| One document | One employee's monthly summary for one pay period |
| Key fields | `EmployeeCode`, `EmployeeName`, `StartDate`, `EndDate`, `Status` (AggregateStatus), monthly totals (hours worked, late, early, shortfall, deduction, normal / weekend / holiday / total extra hours, exception), day counts (present, absent, holiday, weekend, late, early departure, paid leave, unpaid leave), `AttendanceTagCounts`, `DayTypeCounts`, `Remarks` |
| Written by | Process and re-process |
| Note | `AttendanceTagCounts` and `DayTypeCounts` use the enum **names** as keys, unlike every other enum field |

### 15. `ERP.Attendance.Log.MonthlySummaryForPayrollL5` (legacy)

| | |
|---|---|
| Key fields | `EmployeeCode`, `EmployeeName`, `StartDate`, `EndDate`, `NormalDaysExtraHours`, `WeekendExtraHours`, `HolidayExtraHours`, `Absent`, `Shortfall`, `IsNewJoinee`, `DateOfJoining`, `WorkingDaysInPeriod` |
| Note | Reporting stops at L4. L5 data may still appear, but it is not part of the current flow |

### 16. `ERP.Attendance.Log.EmpAttProcessState`

| | |
|---|---|
| One document | One employee in one session and pay group |
| Key fields | `SessionKey`, `PayGroupId`, `EmployeeCode`, `EmployeeName`, `Status`, `CompletedLevels[]`, `CurrentLevel`, `FailurePoint`, `SkipDetails`, `AuditLog[]` (every status change) |
| Indexes | Created at service start-up |

### 17. `ERP.Attendance.Log.Errors`

| | |
|---|---|
| One document | One error or warning raised during upload, import or processing |
| Key fields | `SessionKey`, `SessionId`, `PayGroupId`, `Stage`, `Level`, `Scope`, `FileId`, `EmployeeCode`, `EmployeeName`, `RecordDate`, `Severity`, `ErrorCode`, `Message`, `OccurredAt`, `IsResolved`, `ResolvedBy`, `ResolvedAt`, `LevelData.L3` (a snapshot of the row and the flagged field names) |
| Indexes | Created at service start-up |

### 18. `ERP.Attendance.Log.AttGlobalConfig`

| | |
|---|---|
| One document | One company's attendance-log settings |
| Key fields | `AllowedMonths`, `AllowedFiles` (default `.csv`), `AllowedLevels`, `AllowedFileLevel` (default L3), `MaxFileSizeInMB` (default 50), `Headers` (expected CSV headers per level), `MinDaysAllowed`, `DayOffs` (default Saturday, Sunday), `DefaultWorkTemplateId`, `ImportPolicyMode`, `NextProcessingDay`, `HrContact`, `PolicyLink`, `NightShiftStart` |
| Written by | `POST/PATCH /att-log/config` |

### 19–20. `ERP.Attendance.Log.RawBiometricL1`, `ERP.Attendance.Log.FirstEntryLastExitL2`

Defined for raw biometric (L1) and first-entry / last-exit (L2) uploads. Only L3 files are uploaded
today, so these collections are expected to be empty.

### 21. `fs.files` / `fs.chunks` (GridFS)

The original uploaded CSV files. `Files[].FileId` in the session points here, and
`GET /att-log/sessions/{sessionId}/files/{fileId}/download` streams them back.

---

## Shared and support collections

### 22. `EmployeeEnrollments` (owned by the HR / Employee service)

Attendance 2 **reads** this collection and never writes it. It is the source of employee identity,
pay group, department, designation, reporting line and joining date for the attendance log and
self-service APIs.

| | |
|---|---|
| Key fields | `EmployeeId`, `EmployeeCode`, `EmployeePlaceholderId`, `PayGroupId`, `PayGroupName`, `EmployeeName` (`en`, `ar`), `EmployeeEmail`, `Gender`, `Nationality`, `Department`, `Designation`, `HRPartner`, `ReportingTo`, `WorkContract`, `EmployeeStatus`, `EmploymentType`, `DateOfJoining`, `IsActive`, `IsDeleted` |

### 23. `ERP.Attendance._ReleaseMigration`

Written only by `documents/migrations/sahab-release-migration.mongosh.js`. It holds one document per
run (`_id: "run-<stamp>"`, with start and finish times, the backup database name and the results) and
one document per re-coded template short code (`kind: "shortcode"`, keeping the original code). The
service itself does not read it.

---

## How the collections relate

```text
WorkTemplates ──embedded copy──▶ WorkPlans ──embedded copy──▶ WorkAssignmentMaps ◀── WorkAssignments (regular header)
                                    ▲  ▲                          ▲          ▲
Policies ──embedded copy────────────┘  │                          │          │
                                       │                          │          │
RosterBoards ── WorkPlans[] (shifts) ──┘     roster day rows ─────┘          │
     │ Employees[] (membershipId)                                            │
     ├── EmployeeRosterAssignments (employee × board × shift)                │
     └── RosterSchedulePeriods (publish state per period)                    │
                                                                             │
ShiftRotationBoard ── Plans → RotationWorkPlan (WorkPlans)                   │
     └── Members[] (membershipId) ──────── rotation step-window rows ────────┘

HolidayCalendars (company → inherited locations)       Configs (employee exceptions)

AttGlobalConfig
AttGlobalSessionMaster ──Files[]──▶ fs.files
     ├── DailyProcessedL3 ──process──▶ MonthlyLogL4 (──▶ legacy L5)
     ├── EmpAttProcessState
     └── Errors

EmployeeEnrollments (HR-owned, read-only)
```
