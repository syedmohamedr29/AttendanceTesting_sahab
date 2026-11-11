import sys

md_path = r'D:\Code\Attendance Testing\Attendance_API_Endpoints_and_Testing_Guide.md'

with open(md_path, 'r', encoding='utf-8') as f:
    existing_content = f.read()

# Update Table of Contents
old_toc_marker = "4. [External Integrated Services Matrix](#external-integrated-services-matrix)"
new_toc = """   - [Module 18: Leave Integration (1 Endpoint)](#module-18-leave-integration-1-endpoint)
   - [External Integrated Services Matrix](#external-integrated-services-matrix)
4. [Part 4: MongoDB Database Collections & Architecture (All 23 Collections)](#part-4-mongodb-database-collections--architecture)
   - [Database Conventions & Querying Rules](#database-conventions--querying-rules)
   - [Master Collections Inventory (All 23 Collections)](#master-collections-inventory-all-23-collections)
   - [Master Data Collections Detail](#master-data-collections-detail)
   - [Roster & Rotation Collections Detail](#roster--rotation-collections-detail)
   - [Attendance Log Pipeline Collections Detail](#attendance-log-pipeline-collections-detail)
   - [Shared & System Collections Detail](#shared--system-collections-detail)
   - [Collection Entity-Relationship Architecture Diagram](#collection-entity-relationship-architecture-diagram)"""

if "Part 4: MongoDB Database Collections" not in existing_content:
    existing_content = existing_content.replace(
        "   - [Module 18: Leave Integration (1 Endpoint)](#module-18-leave-integration-1-endpoint)\n   - [External Integrated Services Matrix](#external-integrated-services-matrix)",
        new_toc
    )

part_4_content = """

---

# Part 4: MongoDB Database Collections & Architecture

> **Server:** `10.1.0.4:27018`  
> **Database:** `Sahab` (Shared DEV ERP Database)  
> **Collection Prefixes:** `ERP.Attendance.*` and `ERP.Attendance.Log.*`  
> **Attendance 1 vs. 2:** Attendance 1 (`ZW.AttendanceSvc`) has separate collections; nothing here applies to it.

---

### Database Conventions & Querying Rules

| Convention | Storage Representation | Querying & Testing Rules |
|---|---|---|
| **Identifiers (`_id`, GUIDs)** | **UUID Subtype 4** | In Compass or `mongosh`, query with `UUID("3f2c…")`. Standard GUIDs from other services (subtype 3) match nothing. |
| **Multi-Tenancy (`TenantId`)** | UUID on every document | Every read and write is strictly scoped by the tenant in caller's token. Data from other tenants is never returned. |
| **Scoping (`CompanyId`, `LocationId`)** | UUID fields | `companyId` is in route; location data carries `LocationId`. Empty GUID (`00000000-...`) denotes Company-level default. |
| **Multilingual Names** | Dictionary object | Format: `{ "en": "Morning Shift", "ar": "وردية صباحية" }`. Both keys stored and returned byte-exact. |
| **Enum Storage** | **Integer Numbers** | Stored as numbers in DB (`TemplateType: 1`), but sent/received as **string names** in REST APIs (`"Fixed"`). *(Exception: `MonthlyLogL4.AttendanceTagCounts` uses string names).* |
| **Dates & Times** | DateOnly, TimeOnly, Duration | `DateOnly` stored as UTC midnight; `TimeOnly` stored as `"HH:mm:ss"` string; durations stored as `TimeSpan` tick counts. |
| **Audit Metadata** | Stamped from JWT | `CreatedAt`, `CreatedBy`, `ModifiedAt`, `ModifiedBy` are automatically populated by the server; payload values are ignored. |
| **Soft Delete** | Status flags | Master records are rarely physically removed. Look for `IsDeleted = true`, `IsActive = false`, or `Status = Archived`. |
| **Polymorphic Entities** | Type discriminator `_t` | Identifies concrete entity classes (e.g., `_t: ["WorkTemplate", "FixedWorkTemplate"]`). |

---

### Master Collections Inventory (All 23 Collections)

| # | Collection Name | Functional Module | Document Unit (One Record Represents...) | Discriminator (`_t` values) | Read / Written By |
|---|---|---|---|---|---|
| 1 | `ERP.Attendance.WorkTemplates` | Work Templates | One work template (or saved version of company default) | `FixedWorkTemplate`, `FlexiWorkTemplate`, `SplitWorkTemplate`, `RosterWorkTemplate`, `RotationWorkTemplate` | Written by `/worktemplates/*`, `POST /workplans/roster` |
| 2 | `ERP.Attendance.WorkPlans` | Work Plans | One work plan (Regular, Roster Shift, or Rotation Plan) | `RegularWorkPlan`, `RosterWorkPlan`, `RotationWorkPlan` | Written by `/workplans/*`, `/shift-rotations/*` |
| 3 | `ERP.Attendance.WorkAssignments` | Work Assignments | One assignment header (Plan × Location × Period) | None | Written by `POST /workassignments`, `/adjust`, moves |
| 4 | `ERP.Attendance.WorkAssignmentMaps` | Assignments / Roster / Rotation | One employee's active assignment row (regular range, 1 roster day, or rotation step) | `RegularWorkAssignmentMap`, `RosterWorkAssignmentMap`, `RotationWorkAssignmentMap` | Written by Assignments, Roster Planner, Rotations |
| 5 | `ERP.Attendance.Policies` | Policies | One Break, Grace Period, or Overtime policy | `BreakPolicy`, `GracePeriodPolicy`, `OvertimePolicy` | Written by `/attpolicies/*` (Max 30 company cap) |
| 6 | `ERP.Attendance.HolidayCalendars` | Holiday Calendars | One company or location holiday calendar per year | None | Written by `/holidaylist/*` |
| 7 | `ERP.Attendance.Configs` | Employee Exceptions | One employee exempted from attendance tracking | None | Written by `/config/attendance/employee-exemp/*` |
| 8 | `ERP.Attendance.RosterBoards` | Roster Boards | One roster board with members, shifts, and physical areas | None | Written by `/roster-boards/*` |
| 9 | `ERP.Attendance.EmployeeRosterAssignments` | Roster Boards | One employee × board × shift association (records *that* an employee works a shift) | None | Written by Roster assign, clear, copy, deletes |
| 10 | `ERP.Attendance.RosterSchedulePeriods` | Roster Planner | Publish state of one board for one pay period | None | Written by Roster period publish & unpublish |
| 11 | `ERP.Attendance.ShiftRotationBoard` | Shift Rotations | One shift rotation with teams, pattern, and members | None | Written by `/shift-rotations/*` |
| 12 | `ERP.Attendance.Log.AttGlobalSessionMaster` | Attendance Log | One import session (pay period × location × pay group) | None | Written by `/att-log/uploadfile`, import, finalize |
| 13 | `ERP.Attendance.Log.DailyProcessedL3` | Attendance Log | One employee's daily biometric punch records for one pay period | None | Written by CSV import, L3 punch edits, regularization |
| 14 | `ERP.Attendance.Log.MonthlyLogL4` | Attendance Log | One employee's monthly aggregated summary for one pay period | None | Written by `POST /att-log/start-process` |
| 15 | `ERP.Attendance.Log.MonthlySummaryForPayrollL5` | Attendance Log (Legacy) | One employee's payroll overtime summary for one pay period | None | Maintained for legacy compatibility (reporting uses L4) |
| 16 | `ERP.Attendance.Log.EmpAttProcessState` | Attendance Log | One employee's step-by-step processing state in a session | None | Written by import and processing workers |
| 17 | `ERP.Attendance.Log.Errors` | Attendance Log | One error, warning, or blocker raised during import/processing | None | Written by validation engine and issue resolver |
| 18 | `ERP.Attendance.Log.AttGlobalConfig` | Attendance Log | Company attendance-log global configuration | None | Written by `POST/PATCH /att-log/config` |
| 19 | `ERP.Attendance.Log.RawBiometricL1` | Attendance Log (Not in use) | Raw biometric clock punches | None | Reserved for future biometric hardware integration |
| 20 | `ERP.Attendance.Log.FirstEntryLastExitL2` | Attendance Log (Not in use) | First entry and last exit per day | None | Reserved for future pre-processed punches |
| 21 | `fs.files` / `fs.chunks` | Attendance Log (GridFS) | Binary storage of uploaded monthly CSV files | None | GridFS storage driver |
| 22 | `EmployeeEnrollments` | HR Service Shared Collection | Employee identity, pay group, designation, joining date | None | **Read-only for Attendance 2** (Owned by HR Service) |
| 23 | `ERP.Attendance._ReleaseMigration` | Deployment System | Release migration tracking and short code re-coding audit | None | Written by database deployment migrations |

---

### Master Data Collections Detail

#### 1. `ERP.Attendance.WorkTemplates`
Defines weekly working days, timings, and standard working hours.
* **Polymorphic Discriminator (`_t`):** `FixedWorkTemplate`, `FlexiWorkTemplate`, `SplitWorkTemplate`, `RosterWorkTemplate`, `RotationWorkTemplate`
* **Core Fields:**
  - `WorkTemplateName`: Multilingual dictionary (`{"en": "...", "ar": "..."}`)
  - `ShortCode`: Exactly 7 alphanumeric characters, uppercase, unique per company
  - `TemplateType`: Enum integer (1=Fixed, 2=Flexi, 3=Split, 4=Roster, 5=Rotation)
  - `LocationId`: GUID (Empty `00000000-...` = Company Default; Non-empty = Location-specific)
  - `IsDefault`: Boolean (Only Company Default can have `IsDefault = true`)
  - `Version`: String (e.g., `"1.0"`, `"2.0"`)
  - `HasPendingLocSync`: Boolean (triggers "Apply Sync to Locations" banner)
  - `TotalWorkDurationInMinutes`, `TotalWorkingDays`, `TotalDaysOff`, `TimeZoneId`
  - `ChangeLog[]`: Array of version change audit chips
* **Type-Specific Fields:**
  - Fixed: `FixedTimeSlots[]` (DayEnum, StartTime, EndTime, IsWorkingDay)
  - Flexi: `FlexiTimeSlots[]`, `FlexibleType` (1=Daily, 2=Weekly)
  - Split: `SplitTimeSlots[]` (First slot & Second slot with interval gap)
  - Roster: `RosterTimeSlots[]`, `Colour` (Hex code e.g. `#3B82F6`)
  - Rotation: `RotationTimeSlots[]` (All 7 days required)

---

#### 2. `ERP.Attendance.WorkPlans`
Combines a Work Template with Policies for a specific location.
* **Polymorphic Discriminator (`_t`):** `RegularWorkPlan`, `RosterWorkPlan`, `RotationWorkPlan`
* **Core Fields:**
  - `WorkPlanName`, `ShortCode`, `Description`, `LocationId`, `LocationName`
  - `PlanType`: Enum integer (1=Regular, 2=Roster, 3=Rotation)
  - `IsDefault`: Boolean (The single Location Default Work Plan)
  - `WorkTemplate`: **Embedded snapshot** copy of the template (`EmbeddedWorkTemplate`)
  - `Policies[]`: Array of **embedded snapshot** copies of policies (`EmbeddedPolicy`)
  - `IsGracePeriodPolicyEnabled`, `IsOvertimePolicyEnabled`, `IsBreakPolicyEnabled`
  - `BoardId`: GUID (Present on `RosterWorkPlan`)
  - `RotationId`, `PlanIndex`: Present on `RotationWorkPlan`
* **Architecture Rule:** Snapshot immutability. Modifying a policy or template in the master library does NOT alter existing Work Plans.

---

#### 3. `ERP.Attendance.WorkAssignments` & `WorkAssignmentMaps`
The foundational linkage associating employees to Work Plans.
* **Header Collection (`ERP.Attendance.WorkAssignments`):**
  - Fields: `WorkPlanId`, `WorkPlanName`, `LocationId`, `StartDate`, `EndDate` (null = open-ended), `Status`, `IsActive`
* **Mapping Collection (`ERP.Attendance.WorkAssignmentMaps`):**
  - **The platform's single source of truth for an employee's location and active shift.**
  - `_t` values: `RegularWorkAssignmentMap`, `RosterWorkAssignmentMap`, `RotationWorkAssignmentMap`
  - Core Fields: `AssignmentType`, `EmployeeId`, `EmployeeCode`, `EmployeeName`, `Department`, `Designation`, `LocationId`, `StartDate`, `EndDate`, `HolidayCalendarId`, `WorkPlanData` (embedded snapshot)
  - **Regular Row:** 1 document per employee per assignment date range
  - **Roster Row:** **1 document per employee per scheduled day** (`StartDate` = `EndDate` = day). Contains `RosterAssignment` (`BoardId`, `BoardName`, `Area`, `MembershipId`). Day Offs have no work plan.
  - **Rotation Row:** 1 document per employee per rotation step window. Contains `RotationAssignment` (`RotationId`, `TeamId`, `PlanIndex`, `SequenceOrder`).

---

#### 4. `ERP.Attendance.Policies`
Company-level attendance rules library.
* **Polymorphic Discriminator (`_t`):** `BreakPolicy`, `GracePeriodPolicy`, `OvertimePolicy`
* **Limit:** Max 30 policies per company across all types combined.
* **Core Fields:**
  - `Name`: Multilingual dictionary (`en`, `ar`)
  - `Type`: Enum integer (1=Break, 2=Overtime, 3=GracePeriod)
  - `IsActive`: Boolean (Soft delete sets `IsActive = false`)
* **Type-Specific Fields:**
  - **Grace Period (Type 3):** `LateCheckInGraceMinutes`, `EarlyCheckOutGraceMinutes`, `DeviationThreshold`, `DeviationPeriod` (1=Weekly, 2=BiWeekly, 3=Monthly), `DeductLeaveFrom` (1=Annual, 2=Casual, 3=Sick), `DeductionDays` (e.g., 0.5)
  - **Overtime (Type 2):** `OvertimeRule` (1=AllExtraTime, 2=BeforeShift, 3=AfterShift), `MinimumOvertimeMinutes`, `BufferMinutes`, `Rates[]` (Weekday=1.5, Weekend=2.0, Holiday=2.5)
  - **Break (Type 1):** `BreakType` (1=Paid, 2=Unpaid), `BreakDurationInMinutes`

---

#### 5. `ERP.Attendance.HolidayCalendars`
Public holiday lists per company/location and per year.
* **Core Fields:**
  - `Name`, `ShortCode` (e.g. `HC-2027`), `LocationId` (Empty GUID = Company Default)
  - `CalendarType`: Enum integer (1=CompanyDefault, 2=LocationDefault)
  - `IsInherited`: Boolean (`true` = follows company default and is overwritten on publish; `false` = detached/customised)
  - `IsPublished`: Boolean (staged edits turn `IsPublished = false` until explicit publish)
  - `LastPublishedOn`: DateTime UTC
  - `YearlyCalendar`: `{ Year: 2027, HolidayLists: [ { HolidayName, HolidayType, StartDate, EndDate } ] }`
* **Rules:** Only current year ($Y$) and next year ($Y+1$) can be modified. Holidays must start after today.

---

#### 6. `ERP.Attendance.Configs` (Employee Exceptions)
* **Fields:** `EmployeeId`, `EmployeeCode`, `EmployeeName`, `Department`, `Designation`, `EffectiveFrom`, `EffectiveTo`, `IsActive`
* **Purpose:** Exempts listed employees from attendance tracking and shortfall deductions for the date window.

---

### Roster & Rotation Collections Detail

#### 7. `ERP.Attendance.RosterBoards` & `EmployeeRosterAssignments`
* **Board Header (`ERP.Attendance.RosterBoards`):**
  - Fields: `BoardName`, `LocationId`, `Supervisor`, `PublishingFrequency`, `HasAreas`
  - `Employees[]`: Array of enrolled members (`MembershipId`, `EmployeeId`, `PeriodStartDate`, `PeriodEndDate`, `AreaId`)
  - `WorkPlans[]`: Embedded shift palette available for scheduling on this board
  - `Areas[]`: Array of physical working areas (`AreaId`, `AreaName`, `Order`)
* **Membership Associations (`ERP.Attendance.EmployeeRosterAssignments`):**
  - Records **that** an employee works a specific shift on a board (dateless master linkage).
  - Fields: `BoardId`, `MembershipId`, `EmployeeId`, `WorkPlanId`, `AreaId`, `Colour`, `ShortCode`

---

#### 8. `ERP.Attendance.RosterSchedulePeriods`
* **Purpose:** Manages the publish lifecycle of a roster board for a specific pay period.
* **Fields:** `BoardId`, `PeriodStart`, `PeriodEnd`, `PeriodLabel`, `Status` (Draft or Published), `Version`, `PublishedAt/By`, `UnpublishedAt/By`, `RepublishRequired`, `PublishedEmployeeCount`, `PublishedSlotCount`

---

#### 9. `ERP.Attendance.ShiftRotationBoard`
* **Purpose:** Controls cyclical shift patterns across rotating teams.
* **Fields:**
  - `RotationName`, `LocationId`, `PatternType` (1=Alternating, 2=Repeating), `WeeksPerStep`
  - `Plans[]`: Snapshots of rotation work plans
  - `Teams[]`: Array of teams (`TeamId`, `TeamName`, `RotationPattern[]` plan step indexes)
  - `Members[]`: Enrolled employees (`MembershipId`, `TeamId`, `StartStepIndex`, `GeneratedThrough`)

---

### Attendance Log Pipeline Collections Detail

#### 10. `ERP.Attendance.Log.AttGlobalSessionMaster`
* **Purpose:** Header record for one monthly import session.
* **Fields:** `SessionId`, `SessionKey` (e.g., `Mar16_2026_to_Apr15_2026`), `PayGroupId`, `LocationId`, `DeclaredLevel` (L3), `State` (Imported, Processed, Finalised, Published), `Files[]`, `ImportProgress`, `ProcessingProgress`, `ActiveOperation` (concurrency lock).

---

#### 11. `ERP.Attendance.Log.DailyProcessedL3`
* **Purpose:** Stores daily biometric punch records for one employee for one pay period.
* **Structure:**
  - `DailyKey`, `SessionKey`, `PeriodStart`, `PeriodEnd`, `EmployeeInfo`, `EnrollmentRef`
  - `AttendanceRecords[]`: Array of 30/31 day items:
    * `WorkDate`, `Status` (1=Imported, 3=Processed, 4=ModifiedAfterProcessed, 5=Published, 7=Settled)
    * `DayType`: Enum (1=Weekday, 2=DayOff, 3=Holiday, 4=HolidayOnDayOff)
    * `AttendanceTags[]`: Array of tags (`Present`, `LateArrival`, `EarlyDeparture`, `Absent`, `WeekdayOvertime`, `ManualOverride`)
    * `Record`: `{ ShiftStart, ShiftEnd, RequiredHours, EntryTime, ExitTime, HoursWorked, LateCheckin, EarlyCheckout, TotalShortfall, DeductionHours, NormalExtraHours, WeekendExtraHours, HolidayExtraHours }`
    * `AuditLog[]`: History of manual overrides and regularization reasons.

---

#### 12. `ERP.Attendance.Log.MonthlyLogL4` & `MonthlySummaryForPayrollL5`
* **`MonthlyLogL4` (Official Monthly Summary):**
  - Fields: `EmployeeCode`, `EmployeeName`, `PeriodStart`, `PeriodEnd`, `Status`
  - `Aggregate`: `{ TotalMonthlyHoursWorked, TotalMonthlyLateCheckIn, TotalMonthlyEarlyCheckout, TotalMonthlyShortfall, TotalMonthlyDeduction, TotalMonthlyNormalExtraHours, TotalMonthlyWeekendExtraHours, TotalMonthlyHolidayExtraHours, TotalDaysInMonth, TotalAbsentDays, TotalHolidayDays, TotalWeekendDays, TotalLateDays }`
  - `AttendanceTagCounts`: Dictionary with string names as keys (`{ "Present": 22, "LateArrival": 3 }`)
  - `DayTypeCounts`: Dictionary with string names (`{ "Weekday": 22, "DayOff": 8, "Holiday": 1 }`)
* **`MonthlySummaryForPayrollL5` (Legacy Payroll Export):**
  - Legacy overtime export containing `NormalDaysExtraHours`, `WeekendExtraHours`, `HolidayExtraHours`, `IsNewJoinee`.

---

#### 13. `ERP.Attendance.Log.Errors` & `EmpAttProcessState`
* **`Errors`:** Tracks blocking errors preventing session finalization (`ErrorCode`, `Message`, `Severity`, `OccurredAt`, `IsResolved`, `LevelData.L3`).
* **`EmpAttProcessState`:** Tracks single-employee lifecycle (`CompletedLevels`, `CurrentLevel`, `FailurePoint`, `AuditLog`).

---

#### 14. `ERP.Attendance.Log.AttGlobalConfig` & GridFS
* **`AttGlobalConfig`:** Company attendance settings: `DayOffs` (default Friday/Saturday or Saturday/Sunday), `AllowedFileLevel` (L3), `MaxFileSizeInMB` (50MB), `Headers` (expected CSV headers).
* **GridFS (`fs.files`, `fs.chunks`):** Binary chunks of original uploaded monthly CSV files.

---

### Shared & System Collections Detail

#### 15. `EmployeeEnrollments` (HR Service Shared Collection — Read-Only)
* **Owned by:** Employee / HR Microservice.
* **Attendance 2 Role:** Read-only access.
* **Fields Read:** `EmployeeId`, `EmployeeCode`, `PayGroupId`, `PayGroupName`, `EmployeeName`, `Department`, `Designation`, `ReportingTo`, `DateOfJoining`, `IsActive`.

---

### Collection Entity-Relationship Architecture Diagram

```text
========================================================================================================
                                 MONGODB PERSISTENCE ARCHITECTURE (SAHAB)
========================================================================================================

WorkTemplates (ERP.Attendance.WorkTemplates)
    │
    └── embedded copy ──▶ WorkPlans (ERP.Attendance.WorkPlans)
                              │  ▲
Policies (Policies) ──────────┘  │
    └── embedded copy ───────────┤
                                 │
RosterBoards ── WorkPlans[] ─────┤
    │  └── Employees[] (members) │
    ├── EmployeeRosterAssignments│
    └── RosterSchedulePeriods    │
                                 │
ShiftRotationBoard ──────────────┘
    ├── Plans[] (RotationWorkPlan)
    └── Members[]
                                 │
                                 ▼
                     WorkAssignmentMaps ◀────── WorkAssignments (Header)
                     (Single truth for location
                      & expected daily shift)
                                 │
                                 │   ┌── HolidayCalendars (Company -> Inherited Locations)
                                 │   └── Configs (Employee Attendance Exemptions)
                                 ▼
AttGlobalConfig
AttGlobalSessionMaster ── Files[] ──▶ fs.files / fs.chunks (GridFS CSV files)
    │
    ├── DailyProcessedL3 (Imported punches reconciled against WorkAssignmentMaps)
    │       │
    │       └── Process ──▶ MonthlyLogL4 (Official Monthly Hours & Deductions)
    │                           │
    │                           └── Export ──▶ MonthlySummaryForPayrollL5 (Legacy OT)
    ├── EmpAttProcessState
    └── Errors (Finalization Blockers)

EmployeeEnrollments (Shared HR Master Data - Read Only)
========================================================================================================
```
"""

full_content = existing_content + part_4_content

with open(md_path, 'w', encoding='utf-8') as f:
    f.write(full_content)

print('Successfully updated markdown guide with complete Database Collections!')
print('New file size:', len(full_content), 'bytes')

