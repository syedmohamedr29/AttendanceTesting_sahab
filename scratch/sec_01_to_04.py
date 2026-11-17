# coding: utf-8

def get_content():
    return """
## 1. Module Functional Analysis & Entity Relationship Blueprint

### 1.1 Module Purpose & Scope
The **Scheduler (Roster)** module in Attendance 2 is an enterprise workforce planning engine designed for dynamic, non-standard shift operations where employee working hours, rest days, and work areas vary on a day-by-day basis (e.g., hospital emergency departments, 24/7 security teams, call centers, manufacturing plants).

The application is hosted at `/attendance/Scheduler` and is organized into five functional tabs:
1. **Overview (`?tab=overview`):** Executive operational dashboard showing board counts, employees currently on boards, periods pending publication, real-time 24-hour Gantt chart of active shifts, and weekly cross-board shift status.
2. **Schedules (`?tab=schedules`):** Read-only audit view displaying a 7-day employee × day grid per board and dedicated member schedule cards with shift details, grace periods, overtime policies, and break rules.
3. **Planner (`?tab=planner`):** The operational core. Provides the Schedule Plans list (board × period status matrix), area setup wizard, interactive day-by-day shift allocation grid, shift cloning (Copy Previous), schedule reset (Clear), and period publishing / unpublishing.
4. **Boards (`?tab=boards`):** Administrative board lifecycle management: location assignment, supervisor binding, publishing frequency configuration (Weekly, Bi-Weekly, Monthly), area creation/renaming/deletion, employee enrollment, effective period management, and cross-plan employee transfers.
5. **Templates (`?tab=templates`):** Definition and maintenance of board-specific Roster Work Plans (`PlanType = 2`) and their underlying Roster Work Templates (`TemplateType = 4`), including code uniqueness validation, color swatches, 7-day timing profiles, and policy attachments (Break, Overtime, Grace Period).

---

### 1.2 Entity Relationship & Data Model Architecture
```mermaid
erDiagram
    LOCATION ||--o{ ROSTER_BOARD : "belongs to (immutable)"
    EMPLOYEE ||--o{ ROSTER_BOARD : "supervises"
    ROSTER_BOARD ||--o{ ROSTER_AREA : "defines areas (optional)"
    ROSTER_BOARD ||--o{ ROSTER_WORK_PLAN : "owns shifts"
    ROSTER_WORK_PLAN ||--|| WORK_TEMPLATE : "underlying template (Type 4 Roster)"
    ROSTER_WORK_PLAN }o--o{ ATTENDANCE_POLICY : "links (Break, OT, Grace)"
    ROSTER_BOARD ||--o{ BOARD_MEMBERSHIP : "enrolls employees"
    ROSTER_AREA ||--o{ BOARD_MEMBERSHIP : "places member"
    EMPLOYEE ||--o{ BOARD_MEMBERSHIP : "participates in"
    ROSTER_BOARD ||--o{ ROSTER_SCHEDULE_PERIOD : "tracks publish state"
    BOARD_MEMBERSHIP ||--o{ WORK_ASSIGNMENT_MAP : "generates daily slots"
```

#### Primary Database Collections in MongoDB (`Sahab.ERP.Attendance.*`):
1. **`Sahab.ERP.Attendance.RosterBoards`:** Root board entity. Stores `boardName` (multilingual), `locationId`, `supervisor` (`BoardSupervisorDto`), `publishingFrequency` (`1=Weekly`, `2=BiWeekly`, `3=Monthly`), `hasAreas` (bool), `areas[]` (embedded list of areas), and `employees[]` (embedded board memberships).
2. **`Sahab.ERP.Attendance.WorkPlans`:** Work plans with `PlanType = 2` (Roster). References the parent `boardId` and links to the underlying template.
3. **`Sahab.ERP.Attendance.WorkTemplates`:** Templates with `TemplateType = 4` (Roster). Stores the 7-day slot timings (`rosterTimeSlots[]`), duration, color, code, and policy mappings.
4. **`Sahab.ERP.Attendance.WorkAssignmentMaps`:** The atomic unified schedule store. Roster slots are stored with `AssignmentType = 2` (Roster). Each record stores `employeeId`, `date`, `workPlanId` (or null if `isDayOff = true`), `areaId`, and `status`.
5. **`Sahab.ERP.Attendance.RosterSchedulePeriods`:** Created on first publication of a period. Stores `boardId`, `anchor` (period start date), `status` (`Published`), `version` (integer), `changesNotPublished` (boolean), `publishedBy`, and `publishedAt`.

---

### 1.3 DTO Validation & Input Architecture (POST, PATCH, GET)
- **ID Validation (Route & Body):**
  - All identifiers (`companyId`, `boardId`, `locationId`, `areaId`, `membershipId`, `workPlanId`, `employeeId`, `policyIds`) must conform strictly to RFC 4122 UUID v4 format.
  - Cross-Company Security Boundary: Supplying an entity ID belonging to another company returns `HTTP 404 Not Found` or `HTTP 403 Forbidden` (`Cit.Attendance:9001`).
  - Cross-Location Isolation Boundary: A board belongs strictly to one location. Attempting to assign employees, shifts, or targets from a different location returns `HTTP 400 Bad Request` (`Cit.Attendance:9002`).
- **Query Parameter Constraints:**
  - `locationId` (UUID): Mandatory query parameter across all mutation routes. Omission must return `HTTP 400 Bad Request`.
  - `anchor` (ISO Date `YYYY-MM-DD`): Period start date anchor. Must align with board frequency (Sunday for weekly, Fortnight origin, 1st of month).
  - `from` and `to` (ISO Dates): Query date window. Validation rules: `from` and `to` are mutually required; `from <= to`; total date range cannot exceed 31 days (`Cit.Attendance:2204`).
  - `page` & `pageSize`: Standard pagination integers (`page >= 1`, `pageSize: 1..100`, default 10).
  - `search`: String parameter up to 100 characters. Searches employee name or employee code.

---

## 2. Complete API Inventory

| # | Method | Complete Route Path | Query Parameters | Request Body DTO | Response Model | Success Code | Error Codes | Submodule |
|---|---|---|---|---|---|---|---|---|
| **1** | `GET` | `/api/companies/{companyId}/workplans` | `type=roster`, `locationId={guid}` | None | `WorkPlanDto[]` | `200 OK` | `400`, `401`, `9001` | Templates |
| **2** | `GET` | `/api/companies/{companyId}/workplans/{id}` | None | None | `WorkPlanDetailDto` | `200 OK` | `404 (1301)`, `9001` | Templates |
| **3** | `POST` | `/api/companies/{companyId}/workplans/roster` | `locationId={guid}` | `CreateRosterWorkPlanDto` | `CreatedWorkPlanResponseDto` | `200 OK` | `400`, `1106`, `1203`, `1301`, `1501-1508`, `9001`, `9002` | Templates |
| **4** | `PATCH` | `/api/companies/{companyId}/workplans/roster/{id}` | `locationId={guid}` | `UpdateRosterWorkPlanDto` | `UpdateWorkPlanResponseDto` | `200 OK` | `400`, `1107`, `1905`, `9001`, `9002` | Templates |
| **5** | `DELETE` | `/api/companies/{companyId}/workplans/{id}` | `locationId={guid}` | None | `DeleteWorkPlanResponseDto` | `200 OK` | `400 (1304)`, `404 (1301)`, `9001` | Templates |
| **6** | `GET` | `/api/companies/{companyId}/worktemplates/short-code/availability` | `code={string}` | None | `CodeAvailabilityResponseDto` | `200 OK` | `400`, `401` | Templates |
| **7** | `GET` | `/api/companies/{companyId}/roster-boards` | `locationId={guid}` | None | `RosterBoardSummaryDto[]` | `200 OK` | `400`, `401`, `9001` | Boards |
| **8** | `GET` | `/api/companies/{companyId}/roster-boards/{boardId}` | None | None | `RosterBoardDetailDto` | `200 OK` | `404 (404)`, `9001` | Boards |
| **9** | `POST` | `/api/companies/{companyId}/roster-boards` | `locationId={guid}` | `CreateRosterBoardDto` | `RosterBoardDetailDto` | `200 OK` | `400`, `9001`, `9002` | Boards |
| **10** | `PATCH` | `/api/companies/{companyId}/roster-boards/{boardId}` | `locationId={guid}` | `UpdateRosterBoardDto` | `UpdatedFieldsResponseDto` | `200 OK` | `400 (1903, 1904)`, `404`, `9001` | Boards |
| **11** | `DELETE` | `/api/companies/{companyId}/roster-boards/{boardId}` | `locationId={guid}` | None | `DeleteBoardResponseDto` | `200 OK` | `400 (1901, 1902)`, `404`, `9001` | Boards |
| **12** | `PATCH` | `/api/companies/{companyId}/roster-boards/{boardId}/areas/{areaId}/rename` | `locationId={guid}` | `RenameAreaDto` | `SuccessResponseDto` | `200 OK` | `400`, `404`, `9001` | Boards |
| **13** | `DELETE` | `/api/companies/{companyId}/roster-boards/{boardId}/areas/{areaId}` | `locationId={guid}` | None | `SuccessResponseDto` | `200 OK` | `400 (1903)`, `404`, `9001` | Boards |
| **14** | `POST` | `/api/companies/{companyId}/roster-boards/{boardId}/employees/check-conflicts` | `locationId={guid}` | `CheckConflictsDto` | `CheckConflictsResponseDto` | `200 OK` | `400`, `9001`, `9002` | Board Employees |
| **15** | `PATCH` | `/api/companies/{companyId}/roster-boards/{boardId}/employees` | `locationId={guid}` | `AddBoardEmployeesDto` | `AddEmployeesResponseDto` | `200 OK` | `400 (1914, 1409)`, `9001` | Board Employees |
| **16** | `PATCH` | `/api/companies/{companyId}/roster-boards/{boardId}/employees/{membershipId}/period` | `locationId={guid}` | `UpdatePeriodDto` | `UpdatePeriodResponseDto` | `200 OK` | `400 (1914, 1409)`, `404` | Board Employees |
| **17** | `DELETE` | `/api/companies/{companyId}/roster-boards/{boardId}/employees/{membershipId}` | `locationId={guid}` | None | `RemoveMemberResponseDto` | `200 OK` | `400 (InvalidState)`, `404` | Board Employees |
| **18** | `POST` | `/api/companies/{companyId}/roster-boards/{boardId}/employees/{membershipId}/move/check-conflicts` | `locationId={guid}` | `MoveCheckConflictsDto` | `MoveCheckResponseDto` | `200 OK` | `400`, `404`, `9002` | Board Employees |
| **19** | `PATCH` | `/api/companies/{companyId}/roster-boards/{boardId}/employees/{membershipId}/move` | `locationId={guid}` | `ExecuteMoveDto` | `ExecuteMoveResponseDto` | `200 OK` | `400 (1408, 1409)`, `404`, `9002` | Board Employees |
| **20** | `GET` | `/api/companies/{companyId}/roster-boards/{boardId}/areas/employees` | `asOf={date}` | None | `AreaEmployeesDto` | `200 OK` | `400`, `404` | Planner Setup |
| **21** | `PATCH` | `/api/companies/{companyId}/roster-boards/{boardId}/areas/{areaId}/employees` | `locationId={guid}` | `AssignAreaEmployeesDto` | `AssignAreaResponseDto` | `200 OK` | `400`, `404` | Planner Setup |
| **22** | `GET` | `/api/companies/{companyId}/schedule-plans` | `frequency={enum}`, `anchor={date}` | None | `SchedulePlansListDto` | `200 OK` | `400`, `401` | Planner Grid |
| **23** | `GET` | `/api/companies/{companyId}/roster-boards/{boardId}/schedule` | `anchor={date}` | None | `ScheduleGridDto` | `200 OK` | `400`, `404` | Planner Grid |
| **24** | `POST` | `/api/companies/{companyId}/roster-boards/{boardId}/schedule/assign` | `locationId={guid}` | `AssignRosterShiftDto` | `AssignResponseDto` | `200 OK` | `400 (1906, 1301)`, `404` | Planner Grid |
| **25** | `POST` | `/api/companies/{companyId}/roster-boards/{boardId}/schedule/clear` | `locationId={guid}` | `ClearRosterScheduleDto` | `ClearResponseDto` | `200 OK` | `400 (1913)`, `404` | Planner Grid |
| **26** | `POST` | `/api/companies/{companyId}/roster-boards/{boardId}/schedule/copy-previous` | `locationId={guid}` | `CopyPreviousDto` | `CopyPreviousResponseDto` | `200 OK` | `400 (1906)`, `404` | Planner Grid |
| **27** | `GET` | `/api/companies/{companyId}/roster-boards/{boardId}/schedule/export/excel` | `anchor`, `areaIds`, `timeZone` | None | Binary Excel File | `200 OK` | `400`, `404` | Planner Grid |
| **28** | `POST` | `/api/companies/{companyId}/roster-boards/{boardId}/schedule/publish` | `locationId={guid}` | `PublishScheduleDto` | `PublishResponseDto` | `200 OK` | `400 (1907-1910)`, `404` | Publishing |
| **29** | `POST` | `/api/companies/{companyId}/roster-boards/{boardId}/schedule/unpublish` | `locationId={guid}` | `UnpublishScheduleDto` | `UnpublishResponseDto` | `200 OK` | `400 (1909, 1911, 1912)` | Publishing |
| **30** | `GET` | `/api/companies/{companyId}/roster-boards/overview/summary` | `locationId`, `boardId`, `from`, `to` | None | `OverviewSummaryDto` | `200 OK` | `400 (2204)` | Overview |
| **31** | `GET` | `/api/companies/{companyId}/roster-boards/overview/publishing` | `locationId`, `boardId`, `from`, `to` | None | `OverviewPublishingDto` | `200 OK` | `400 (2204)` | Overview |
| **32** | `GET` | `/api/companies/{companyId}/roster-boards/overview/today` | `locationId`, `boardId`, `areaId` | None | `OverviewTodayDto` | `200 OK` | `400` | Overview |
| **33** | `GET` | `/api/companies/{companyId}/roster-boards/overview/week` | `locationId`, `boardId`, `from`, `to` | None | `OverviewWeekDto` | `200 OK` | `400 (2204)` | Overview |
| **34** | `GET` | `/api/companies/{companyId}/roster-boards/schedules` | `from`, `to`, `search`, `page`, `pageSize` | None | `SchedulesGridDto` | `200 OK` | `400 (2204)` | Schedules |
| **35** | `GET` | `/api/companies/{companyId}/roster-boards/schedules/employees/{employeeId}` | `from`, `to` | None | `MemberScheduleCardDto` | `200 OK` | `404 (2207)`, `400 (2204)` | Schedules |

---

## 3. Field-Level Validation Matrix

| Field Name | Target API | Mandatory? | Data Type | Min / Format | Max / Limit | Valid Test Values | Invalid Test Values | Business Rule & System Validation |
|---|---|---|---|---|---|---|---|---|
| `boardName.en` | `POST /roster-boards` | Yes | String | 1 char | 100 chars | `"Emergency Room Roster"` | `""`, Whitespace, >100 chars | Primary English label. Mandatory on create/edit. Duplicate names permitted across boards. |
| `boardName.ar` | `POST /roster-boards` | No | String | 0 chars | 100 chars | `"جدول الطوارئ"` | >100 chars | Optional Arabic localized name. |
| `publishingFrequency` | `POST /roster-boards` | Yes | Integer | 1 | 3 | `1` (Weekly), `2` (BiWeekly), `3` (Monthly) | `0`, `4`, `-1`, `"Weekly"` | Determines scheduling period window. Custom frequency is strictly refused. |
| `supervisor.employeeId` | `POST /roster-boards` | Yes | UUID | UUID v4 | 36 chars | Active Employee UUID | Null, Invalid UUID, Inactive EMP | Supervisor must be active in `SP.EmployeeSvc` at the same location. |
| `supervisor.name.en` | `POST /roster-boards` | Yes | String | 1 char | 100 chars | `"Dr. Ahmed Supervisor"` | `""`, Null | Supervisor snapshot display name. |
| `supervisor.employeeCode` | `POST /roster-boards` | Yes | String | 1 char | 50 chars | `"EMP-001"` | `""`, Null | Employee code of supervisor. |
| `hasAreas` | `POST /roster-boards` | Yes | Boolean | - | - | `true`, `false` | Null, `"true"`, `1` | Enables area management. Cannot be toggled false while members have assigned areas (1904). |
| `areas[].name.en` | `POST /roster-boards` | Conditional | String | 1 char | 100 chars | `"Triage & Trauma"` | `""`, Duplicate in board | Mandatory for each area if `hasAreas = true`. Must be unique within the board. |
| `shiftName.en` | `POST /workplans/roster` | Yes | String | 1 char | 100 chars | `"Morning Shift"` | `""`, Duplicate on board | Shift name must be unique within the board. |
| `code` | `POST /workplans/roster` | Yes | String | 1 char | 20 chars | `"MORN01"`, Alphanumeric | Duplicate code, Space, >20 | Globally unique code across regular work plans and roster shifts. Immutable on edit (1107). |
| `colour` | `POST /workplans/roster` | Yes | Hex String | 7 chars | 7 chars | `"#14B8A6"`, 8 UI palette hexes | `"red"`, `"#ZZZZZZ"`, `""` | Shift badge color on schedule grid. |
| `rosterTimeSlots` | `POST /workplans/roster` | Yes | Array | 7 items | 7 items | 7 daily slot definitions (Sun to Sat) | <7 or >7 items, Null | Defines 7-day timing template. DayEnum: 0 (Sun) to 6 (Sat). |
| `startTime` / `endTime` | `POST /workplans/roster` | Yes | Time String | `"00:00"` | `"23:59"` | `"06:00"`, `"14:00"` | `"25:00"`, `"6 AM"`, `""` | Military time format `HH:mm`. If `endTime < startTime`, indicates overnight shift crossing midnight. |
| `policyIds` | `POST /workplans/roster` | No | Array[UUID] | 0 items | 3 items | Active policy UUIDs | Inactive policy, duplicate type | Max 1 policy per type (`Break`, `Overtime`, `GracePeriod`). Inactive policy returns 1506. |
| `employeeIds` | `PATCH .../employees` | Yes | Array[UUID] | 1 item | 500 items | Active EMP UUIDs at location | `[]`, Inactive EMP, Cross-loc | All employees must belong to board location. Inactive employees must be rejected. |
| `startDate` | `PATCH .../employees` | Yes | ISO Date | Today | Future | `"2026-11-22"` | Past date (for new membership) | Effective enrollment start date. Cannot be in the past for new memberships. |
| `endDate` | `PATCH .../employees` | No | ISO Date | `>= startDate` | Open-ended | `"2027-11-22"`, `null` | `< startDate` | Optional expiration date of membership. `null` indicates indefinite assignment. |
| `adjustConflicts` | `PATCH .../employees` | No | Boolean | - | - | `true`, `false` | Null | If `true`, confirms automatic ending/splitting/removal of conflicting regular work plans. |
| `slots[].employeeId` | `POST .../schedule/assign` | Yes | UUID | UUID v4 | 36 chars | Active board member UUID | Non-member, Inactive | Target employee for shift assignment. Must be an active member for specified dates. |
| `slots[].dates` | `POST .../schedule/assign` | Yes | Array[Date] | 1 date | 31 dates | `["2026-11-22", "2026-11-23"]` | `[]`, Invalid dates | Dates to assign shift or day-off. |
| `dayOff` | `POST .../schedule/assign` | Yes | Boolean | - | - | `true`, `false` | Null | If `true`, marks specified dates as Rest Days (`workPlanId` must be null). |
| `anchor` | `POST .../schedule/publish` | Yes | ISO Date | Valid Date | - | `"2026-11-22"` | Invalid date format | Period start date anchor (Sunday for weekly, Fortnight origin, 1st of month). |
| `version` | `POST .../schedule/publish` | No | Integer | 0 | Max Int | `0`, `1`, `2` | Negative int, Mismatched int | Optimistic concurrency token. If sent and differs from current DB version, returns 1910. |
| `allowEmpty` | `POST .../schedule/publish` | Yes | Boolean | - | - | `true`, `false` | Null | Must be `true` if publishing a period with 0 assigned shifts and no open holidays (1908). |
| `force` | `POST .../schedule/unpublish` | Yes | Boolean | - | - | `true`, `false` | Null | If period has already started, `force: true` is mandatory to override and unpublish (1911). |

---

## 4. Mandatory vs. Optional Field Matrix

| API Group / Request Entity | Mandatory Fields (Must Provide) | Optional Fields (Can Omit) | System Default / Fallback Behavior if Omitted |
|---|---|---|---|
| **Create Roster Board** | `boardName.en`, `supervisor.employeeId`, `supervisor.name`, `supervisor.employeeCode`, `publishingFrequency`, `hasAreas` | `boardName.ar`, `areas[]` | `boardName.ar = ""` (empty), `areas = []` (no areas created). |
| **Update Roster Board** | At least one field changed (`boardName`, `supervisor`, `publishingFrequency`, `hasAreas`, `addedAreas`, `removedAreaIds`) | Any un-updated property | Partial update: unprovided fields remain strictly unchanged in MongoDB. |
| **Create Roster Shift** | `boardId`, `shiftName.en`, `code`, `colour`, `rosterTimeSlots[]` (7 items), `totalWorkDurationInMinutes`, `totalWorkingDays`, `totalDaysOff` | `shiftName.ar`, `description`, `isBreakPolicyEnabled`, `isOvertimePolicyEnabled`, `isGracePeriodPolicyEnabled`, `policyIds` | `description = ""`, policy flags default to `false`, `policyIds = []`. |
| **Update Roster Shift** | None (All body fields optional) | All fields optional | Partial update: fields omitted retain existing values. Note: `code`, `boardId`, `locationId` locked. |
| **Add Employees to Board** | `employeeIds[]`, `startDate` | `endDate`, `areaId`, `adjustConflicts` | `endDate = null` (open-ended), `areaId = null` (unassigned area), `adjustConflicts = false`. |
| **Assign Shifts / Day Off** | `slots[]` (`employeeId`, `dates[]`), `dayOff` | `workPlanId` (Mandatory if `dayOff = false`) | If `dayOff = true`, `workPlanId` ignored/null. |
| **Publish Period** | `anchor`, `allowEmpty` | `version` | If `version` omitted, skips optimistic concurrency lock check. |
| **Unpublish Period** | `anchor`, `force` | None | Must specify `force: true` if period has already commenced. |
| **Overview / Schedules Queries** | None (All parameters optional) | `from`, `to`, `locationId`, `boardId`, `areaId`, `department`, `page`, `pageSize` | Defaults to current week (Sunday to Saturday), current location, page 1, pageSize 10. |
"""
