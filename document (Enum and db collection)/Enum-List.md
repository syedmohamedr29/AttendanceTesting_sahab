# Attendance 2: Enum List

Every enum the Attendance 2 service (`SP.AttendanceSvc`) exposes through its APIs or stores in its
database, grouped by module. The list is built from the source on `main` as deployed in
`dev300-1.0.2` (23 Oct 2026).

## How enums travel

| Where | Format | Example |
|---|---|---|
| API responses | The **name**, as a string | `"templateType": "Roster"` |
| API requests (JSON body or query) | The name (case-insensitive) **or** the number | `"Roster"` or `4` |
| MongoDB documents | The **number** | `TemplateType: 4` |
| Exception: `MonthlyLogL4.AttendanceTagCounts` and `DayTypeCounts` | Dictionary keys stored as **names** | `{ "Present": 20 }` |

Most enums start with `NotApplicable = 0`. It is the default for "not set" and is never a valid
choice in a request. If a request sends it, treat any acceptance as a defect.

Some filters are plain strings rather than enums. They are listed in the
[last section](#string-filters-that-behave-like-enums).

---

## 1. Work Templates

### WorkTemplateType
Used in: `WorkTemplates.TemplateType`, every work template response.

| Value | Name | Meaning |
|---|---|---|
| 0 | NotApplicable | Not set |
| 1 | Fixed | Same start and end time on every working day |
| 2 | Flexi | Required hours per day or per week, no fixed timings |
| 3 | Split | Two time slots per working day with a gap between them |
| 4 | Roster | A shift used on roster boards. Keeps this type for life |
| 5 | Rotation | Fixed-shaped template with 7 day rows. Only rotation plans can use it. Keeps this type for life |

A template can change type only between Fixed, Flexi and Split. Roster and Rotation templates can
never change type, and no other template can become one.

### WorkTemplateStatus
Used in: `WorkTemplates.Status`.

| Value | Name | Meaning |
|---|---|---|
| 0 | NotApplicable | Not set |
| 1 | Active | Can be used |
| 2 | Inactive | Not in use |
| 3 | Archived | Archived; can be restored |

### FlexibleType
Used in: Flexi templates (`FlexibleType`).

| Value | Name | Meaning |
|---|---|---|
| 0 | NotApplicable | Not set |
| 1 | Daily | Required hours are counted per day |
| 2 | Weekly | Required hours are counted per week |

### TimeSlotInterval
Used in: Split template time slots.

| Value | Name | Meaning |
|---|---|---|
| 0 | NotApplicable | Not set |
| 1 | NoInterval | No gap between the slots |
| 2 | OneInterval | One gap between the two slots |

### RecurrenceOfMonth
Used in: day time slots of Fixed, Flexi, Split and Rotation templates (which weeks of the month a day row applies to).

| Value | Name |
|---|---|
| 0 | NotApplicable |
| 1 | First |
| 2 | Second |
| 3 | Third |
| 4 | Fourth |
| 5 | Fifth |

### Day
Used in: template day rows, the default work pattern, issue and blocker rows.

| Value | Name |
|---|---|
| 0 | NotApplicable |
| 1 | Sun |
| 2 | Mon |
| 3 | Tue |
| 4 | Wed |
| 5 | Thu |
| 6 | Fri |
| 7 | Sat |

Note that `Day` starts the week on **Sunday** (Sun = 1), while `DayOfWeekEnum` in the attendance
log starts on **Monday** (Monday = 1).

### WTChangeType
Used in: `WorkTemplates.ChangeLog[]` and the company default version history.

| Value | Name | Meaning |
|---|---|---|
| 0 | NotApplicable | Not set |
| 1 | Created | Template created |
| 2 | WorkType | Template type changed |
| 3 | DayOff | Day-off days changed |
| 4 | Timings | Timings changed |
| 5 | WorkHours | Working hours changed |
| 6 | Name | Name changed |
| 7 | ShortCode | Short code changed |
| 8 | Updated | Any other change |

---

## 2. Work Plans and Work Assignments

### WorkPlanType
Used in: `WorkPlans.PlanType`.

| Value | Name | Meaning |
|---|---|---|
| 0 | NotApplicable | Not set |
| 1 | Regular | A plan employees are assigned to for a period |
| 2 | Roster | A shift on a roster board |
| 3 | Rotation | One plan inside a shift rotation |

### WorkAssignmentType
Used in: `WorkAssignmentMaps.AssignmentType`.

| Value | Name | Meaning |
|---|---|---|
| 0 | NotApplicable | Not set |
| 1 | Regular | Employee assigned to a regular work plan |
| 2 | Roster | One scheduled roster day for an employee |
| 3 | Rotation | Employee's rotation enrolment window |

### WorkAssignmentStatus
Used in: `WorkAssignments.Status`, `WorkAssignmentMaps.Status`.

| Value | Name | Meaning |
|---|---|---|
| 0 | NotApplicable | Not set |
| 1 | Pending | Set on every assignment when it is created |
| 2 | Completed | Closed. A completed assignment's period cannot be edited |

Whether an assignment is current, upcoming or past is worked out from its dates, not from this
status.

### OverlapResolutionAction
Used in: conflict previews for regular work assignments (what happens to an overlapping assignment if you proceed).

| Value | Name | Meaning |
|---|---|---|
| 0 | NotApplicable | Not set |
| 1 | EndsEarly | The existing assignment is cut to end the day before the new one starts |
| 2 | EndsEarlyAndResumes | The existing assignment is cut, then resumes the day after the new one ends |
| 3 | Removed | The existing assignment lies inside the new period and is removed |
| 4 | StartsLater | The existing assignment now starts the day after the new one ends |

---

## 3. Attendance Policies

### PolicyType
Used in: `Policies.Type`.

| Value | Name |
|---|---|
| 0 | NotApplicable |
| 1 | BreakPolicy |
| 2 | OvertimePolicy |
| 3 | GracePeriodPolicy |

### BreakType
Used in: break policy break items.

| Value | Name |
|---|---|
| 0 | NotApplicable |
| 1 | Paid |
| 2 | Unpaid |

### GracePeriodDeviationPeriod
Used in: grace period policy (the window the deviation threshold is counted over).

| Value | Name |
|---|---|
| 0 | NotApplicable |
| 1 | Weekly |
| 2 | BiWeekly |
| 3 | Monthly |

### GracePeriodLeaveDeductionType
Used in: grace period policy (which leave balance is deducted when the threshold is exceeded).

| Value | Name |
|---|---|
| 0 | NotApplicable |
| 1 | AnnualLeave |
| 2 | CasualLeave |
| 3 | SickLeave |

### OvertimeRule
Used in: overtime policy.

| Value | Name | Meaning |
|---|---|---|
| 0 | NotApplicable | Not set |
| 1 | AllExtraTime | All time beyond the shift counts |
| 2 | BeforeShiftStarts | Only time before the shift start counts |
| 3 | AfterShiftEnds | Only time after the shift end counts |

### OvertimeDayRate
Used in: overtime policy rates (one rate per day type).

| Value | Name |
|---|---|
| 0 | NotApplicable |
| 1 | WorkingDay |
| 2 | DayOff |
| 3 | Holiday |

---

## 4. Holiday Calendars

### HolidayCalendarType
Used in: `HolidayCalendars.CalendarType`, the `calendarType` query filter.

| Value | Name | Meaning |
|---|---|---|
| 0 | NotApplicable | Not set |
| 1 | CompanyDefault | The company's calendar, published to locations |
| 2 | LocationDefault | A location's calendar (inherited or customised) |
| 3 | ShiftSchedule | Reserved; not used by any API today |

---

## 5. Roster Boards and the Planner

### SchedulerFrequency
Used in: `RosterBoards.PublishingFrequency`, `RosterSchedulePeriods.Frequency`, the `frequency` query on `GET /schedule-plans`.

| Value | Name | Meaning |
|---|---|---|
| 0 | NotApplicable | Not set |
| 1 | Weekly | One period = one scheduling week (Sunday to Saturday) |
| 2 | BiWeekly | One period = two scheduling weeks |
| 3 | Monthly | One period = one calendar month |
| 4 | Custom | Custom period |

Scheduling weeks start on **Sunday**. They are not ISO weeks.

### RosterPeriodStatus
Used in: `RosterSchedulePeriods.Status`, publish and unpublish responses.

| Value | Name | Meaning |
|---|---|---|
| 0 | NotApplicable | Not set |
| 1 | Draft | Never published, or published and then unpublished |
| 2 | Published | Published to staff. `RepublishRequired = true` means it changed after publishing |

### SchedulePlanStatus
Used in: schedule plans list, board list and detail, the schedule grid.

| Value | Name | Meaning |
|---|---|---|
| 0 | NotApplicable | Not set |
| 1 | NotPlanned | Nothing scheduled in the period |
| 2 | Pending | Something is scheduled but the period is not published |
| 3 | Published | The period is published |
| 4 | Completed | The period is in the past |

### DayState
Used in: schedule grid cells (one employee on one date).

| Value | Name | Meaning |
|---|---|---|
| 0 | NotApplicable | Not set |
| 1 | Empty | Nothing planned (the "+" cell) |
| 2 | Shift | A shift is assigned |
| 3 | Off | Day off assigned |
| 4 | OnLeave | Approved leave from the Leave service (read-only) |
| 5 | Holiday | A holiday with nothing scheduled over it |
| 6 | HolidayWorked | A holiday with a shift scheduled on it |

The Leave service is not yet connected to the planner, so `OnLeave` does not appear on DEV.

### BoardMembershipSegment
Used in: board, work plan and rotation employee lists (the `segment` query value is the lower-case name).

| Value | Name | Meaning |
|---|---|---|
| 0 | NotApplicable | No filter ("all") |
| 1 | Active | Start date ≤ asOf ≤ end date |
| 2 | Upcoming | Start date after asOf |
| 3 | Past | End date before asOf |

### BoardAreaChange
Used in: area assignment results.

| Value | Name | Meaning |
|---|---|---|
| 0 | NotApplicable | Not set |
| 1 | Assigned | Had no area, now has one |
| 2 | Moved | Moved from another area |
| 3 | Unchanged | Already in the target area |
| 4 | NotOnBoard | Not a member of the board |

### CommitmentSource
Used in: board and rotation conflict responses (where the employee is already committed).

| Value | Name |
|---|---|
| 0 | NotApplicable |
| 1 | RegularPlan |
| 2 | Board |
| 3 | Rotation |

### MoveTargetType
Used in: Move Employee requests and responses (the source and the target of a move).

| Value | Name |
|---|---|
| 0 | NotApplicable |
| 1 | Board |
| 2 | WorkPlan |
| 3 | Rotation |

### RosterExportDayStatus
Used in: the roster Excel export only (cell legend). Not returned as JSON.

| Value | Name |
|---|---|
| 0 | NotOnBoard |
| 1 | Shift |
| 2 | HolidayWorked |
| 3 | Holiday |
| 4 | Off |
| 5 | Leave |
| 6 | Unfilled |

---

## 6. Shift Rotations

### RotationPatternType
Used in: `ShiftRotationBoard.PatternType`, rotation create and update.

| Value | Name | Meaning |
|---|---|---|
| 0 | NotApplicable | Not set |
| 1 | Alternating | Every plan appears once, in order (P1 → P2 → P3) |
| 2 | Uneven | A free sequence in which a plan may repeat (P1 → P1 → P2) |

---

## 7. Attendance Log (upload, import, processing)

### AttendanceFileLevel
Used in: sessions (`DeclaredLevel`), config (`AllowedLevels`, `AllowedFileLevel`), process state, error log.

| Value | Name | Meaning |
|---|---|---|
| 0 | NotApplicable | Not set |
| 1 | RawBiometricL1 | Raw biometric punches |
| 2 | FirstEntryLastExitL2 | First entry and last exit per day |
| 3 | DailyProcessedL3 | Daily processed records. **The only level uploaded today** |
| 4 | MonthlyLogL4 | Monthly summary per employee |
| 5 | MonthlySummaryForPayrollL5 | Legacy payroll summary; reporting now stops at L4 |

### AttendanceSessionState
Used in: `AttGlobalSessionMaster.State`.

| Value | Name | Meaning |
|---|---|---|
| 0 | NotApplicable | Not set |
| 1 | Draft | Files uploaded, not yet imported |
| 2 | Importing | Import running (transient) |
| 3 | Imported | All files imported; ready to process |
| 4 | Finalising | Processing running (transient) |
| 5 | Finalised | Processed (UI label "Finalised") |
| 6 | Published | Released to payroll and the employee portal |
| 7 | Settled | Consumed by a payrun; cannot change |

### AttendanceFileStatus
Used in: `AttGlobalSessionMaster.Files[].Status`.

| Value | Name |
|---|---|
| 0 | NotApplicable |
| 1 | Uploaded |
| 2 | Validating |
| 4 | Importing |
| 5 | Imported |
| 6 | PartialBatch |
| 7 | ValidationFailed |
| 8 | Failed |
| 9 | ImportCancelled |
| 10 | ImportedWithIssues |
| 11 | Processing |
| 12 | ProcessedWithIssues |
| 13 | Processed |
| 14 | Rejected |

Value 3 is not used.

### ImportStage
Used in: `AttGlobalSessionMaster.ImportProgress.Stage` (the import progress API).

| Value | Name | Meaning |
|---|---|---|
| 0 | NotStarted | |
| 1 | Preparing | Session locked, config, enrolments and holidays loaded |
| 2 | Parsing | CSV read into memory |
| 3 | Validating | Per-row checks |
| 4 | SavingRows | Daily records and process states saved |
| 5 | SeedingMissing | Missing rows created for employees with no data |
| 6 | Finalizing | Session totals and state updated |
| 7 | Completed | Finished |
| 8 | Failed | Stopped with an error |
| 9 | Cleaning | Override re-import: old errors removed first |

### ProcessingStage
Used in: `AttGlobalSessionMaster.ProcessingProgress.Stage` (the processing progress API).

| Value | Name | Meaning |
|---|---|---|
| 0 | NotStarted | |
| 1 | Preparing | Session locked, files set to Processing |
| 2 | GeneratingL4 | Monthly summaries being built |
| 3 | GeneratingL5 | Legacy payroll summaries being built |
| 4 | Completed | Finished |
| 5 | Failed | Stopped with an error |
| 6 | Cleaning | Override re-process: old errors removed first |

### SessionOperation
Used in: `AttGlobalSessionMaster.ActiveOperation` (the lock that stops two operations running on one session).

| Value | Name |
|---|---|
| 0 | NotApplicable |
| 1 | Uploading |
| 2 | Importing |
| 3 | Processing |
| 4 | Deleting |

### AttProcessingStage
Used in: error log `Stage`, the `stage` query on the error APIs.

| Value | Name |
|---|---|
| 0 | NotApplicable |
| 1 | Upload |
| 2 | Import |
| 3 | Process |

### ErrorSeverity
Used in: error log `Severity`, the `severity` query on the error APIs.

| Value | Name |
|---|---|
| 0 | NotApplicable |
| 1 | Info |
| 2 | Warning |
| 3 | Error |
| 4 | Critical |

### ErrorScope
Used in: error log `Scope` (what the error is about).

| Value | Name |
|---|---|
| 0 | NotApplicable |
| 1 | Session |
| 2 | File |
| 3 | Employee |
| 4 | Record |

### EmpProcessStatus
Used in: `EmpAttProcessState.Status`.

| Value | Name | Meaning |
|---|---|---|
| 0 | NotApplicable | Not set |
| 1 | Pending | Waiting to be processed |
| 2 | Processing | Being processed |
| 3 | Processed | Processed |
| 4 | Failed | Processing failed |
| 5 | Approved | Reviewed (action `review`) |
| 6 | Locked | Approved (action `approve`) |
| 7 | NotUploaded | Enrolled but absent from the uploaded file |
| 8 | Skipped | Skipped by processing |

### L3RecordStatus
Used in: each day row of a daily record (`AttendanceRecords[].Status`).

| Value | Name | Meaning |
|---|---|---|
| 0 | NotApplicable | Not set |
| 1 | Imported | Imported, not yet in a monthly summary |
| 2 | Failed | Processing of this row failed |
| 3 | Processed | Included in the latest monthly summary |
| 4 | ModifiedAfterProcessed | Edited after processing, before publish |
| 5 | Published | Published with this row's numbers |
| 6 | ModifiedAfterPublished | Edited after publish; payroll must wait for re-processing |
| 7 | Settled | Claimed by a payrun; cannot change |

### AggregateStatus
Used in: monthly summary documents (L4, and legacy L5) and the L4 list response: whether the totals still match the daily rows.

| Value | Name | Meaning |
|---|---|---|
| 0 | NotApplicable | Not set |
| 1 | Fresh | Totals match the current daily rows |
| 2 | ModifiedAfterProcessed | Daily rows edited after processing |
| 3 | ModifiedAfterPublished | Daily rows edited after publish; payroll must not use it |
| 4 | Settled | Consumed by a payrun; cannot change |

### DayType
Used in: daily record rows (`DayType`, `FileDayType`), monthly summary `DayTypeCounts`.

| Value | Name |
|---|---|
| 0 | NotApplicable |
| 1 | Weekday |
| 2 | DayOff |
| 3 | Holiday |
| 4 | HolidayOnDayOff |

### AttendanceTag
Used in: daily record rows (`AttendanceTags[]`), monthly summary `AttendanceTagCounts`.

| Value | Name | Meaning |
|---|---|---|
| 0 | NotApplicable | Not set |
| 1 | AttendanceUnavailable | Employee has no data in the uploaded file |
| 2 | AttendanceMissing | Day row is missing |
| 3 | AttendanceIncomplete | Entry or exit missing |
| 4 | InvalidData | Values could not be read or are inconsistent |
| 5 | Present | Present |
| 6 | DayOff | Day off |
| 7 | Holiday | Holiday |
| 8 | HolidayOnDayOff | Holiday that falls on a day off |
| 9 | Absent | Absent |
| 10 | NotCounted | Not counted |
| 11 | LateArrival | Late check-in |
| 12 | EarlyDeparture | Early check-out |
| 13 | GraceApplied | Grace period applied |
| 14 | PaidLeave | Paid leave (annual, sick, emergency, maternity) |
| 15 | UnpaidLeave | Unpaid leave |
| 16 | DayOffOvertime | Worked on a day off |
| 17 | HolidayOvertime | Worked on a holiday |
| 18 | WeekdayOvertime | Extra hours on a working day |
| 19 | RegularizeIncomplete | Regularized a Missing, Incomplete or InvalidData row |
| 20 | RegularizeAbsent | Regularized an Absent row |
| 21 | RegularizeShortfall | Regularized a row with a shortfall |
| 22 | ManualOverride | Tags were set by hand; not recalculated |

Late, early and grace tags are never set on a Holiday or DayOff row.

### L3AuditAction
Used in: the audit trail of daily record rows.

| Value | Name |
|---|---|
| 0 | NotApplicable |
| 1 | Import |
| 2 | CheckInCheckOutEdit |
| 3 | RegularizeIncomplete |
| 4 | RegularizeAbsent |
| 5 | RegularizeShortfall |
| 6 | MarkDayOff |
| 7 | MarkHoliday |
| 8 | OverTimeOverride |
| 9 | ClearManualMark |
| 10 | Settle |
| 11 | Unsettle |
| 12 | DeductionOverride |
| 13 | Edit |

### AttendanceRuleApplied
Used in: daily record rows (`Record.RuleApplied`): whose numbers the row carries.

| Value | Name | Meaning |
|---|---|---|
| 0 | NotApplicable | Not set |
| 1 | External | Values taken from the uploaded file |
| 2 | SystemSetting | Values calculated by Attendance 2 |

### AttImportPolicyMode
Used in: `AttGlobalConfig.ImportPolicyMode`.

| Value | Name | Meaning |
|---|---|---|
| 0 | NotApplicable | Not set |
| 1 | FileSourced | Default. The file's values are used |
| 2 | SystemDefined | Attendance 2 calculates the values |

### DayOfWeekEnum
Used in: daily record rows (`Record.DayOfWeek`).

| Value | Name |
|---|---|
| 0 | NotApplicable |
| 1 | Monday |
| 2 | Tuesday |
| 3 | Wednesday |
| 4 | Thursday |
| 5 | Friday |
| 6 | Saturday |
| 7 | Sunday |

---

## 8. Self Service (`/me` and `/team`)

### ProcessedPeriodStatus
Used in: `/me/periods`, `/me/attendance/*`, `/team/*`.

| Value | Name | Meaning |
|---|---|---|
| 0 | NotProcessed | No processed numbers for the period |
| 1 | Processed | Session finalised |
| 2 | Published | Session published or settled |
| 3 | Partial | `/team` only: some reportees have numbers for the period and others do not |

### AttendanceDayStatus
Used in: `/me/attendance/days`, `/team/attendance/{employeeId}/days`.

| Value | Name |
|---|---|
| 1 | Present |
| 2 | Absent |
| 3 | Leave |
| 4 | HalfDay |
| 5 | WeeklyOff |
| 6 | Holiday |
| 7 | Incomplete |
| 8 | Missing |
| 9 | NotProcessed |

### AttendanceDayFilter
Used in: the `status` query on the attendance days APIs (case-insensitive name).

| Value | Name |
|---|---|
| 1 | Absent |
| 2 | Late |
| 3 | Early |
| 4 | Incomplete |
| 5 | Overtime |
| 6 | ShortHours |
| 7 | WorkedOnOff |
| 8 | Present |
| 9 | Leave |
| 10 | HalfDay |

### OvertimeDayType
Used in: overtime lines in self-service attendance responses.

| Value | Name |
|---|---|
| 1 | Weekday |
| 2 | WeeklyOff |
| 3 | Holiday |

### ScheduleDayType
Used in: `/me/schedule`, `/team/schedule`.

| Value | Name |
|---|---|
| 1 | Workday |
| 2 | Weekend |
| 3 | DayOff |
| 4 | Holiday |
| 5 | HolidayOnDayOff |
| 6 | NotScheduled |
| 7 | NoAssignment |

### ScheduleSource
Used in: `/me/schedule` (which kind of plan produced the day).

| Value | Name |
|---|---|
| 1 | Regular |
| 2 | Roster |
| 3 | Rotation |

### TeamSchedulePeriodStatus
Used in: `/team/schedule`.

| Value | Name |
|---|---|
| 1 | Published |
| 2 | Draft |
| 3 | NotPlanned |

---

## 9. Leave Service Integration

### LeaveCalendarDateTypeEnum
Used in: `GET /api/attendance/v1/companies/{companyId}/employees/{employeeId}/calendar/day-classification`.

| Value | Name | Meaning |
|---|---|---|
| 0 | NotApplicable | Error fallback only |
| 1 | Workday | Normal working day |
| 2 | Weekend | Non-working day by the employee's pattern |
| 3 | Holiday | Holiday on a working day |
| 4 | HolidayOnWeekend | Holiday on a non-working day |

### LeaveCalendarDayOfWeek
Used in: the same day-classification response.

| Value | Name |
|---|---|
| 0 | NotApplicable |
| 1 | Sun |
| 2 | Mon |
| 3 | Tue |
| 4 | Wed |
| 5 | Thu |
| 6 | Fri |
| 7 | Sat |

---

## String filters that behave like enums

These query values are plain strings. They are case-insensitive. An unknown value returns an error
unless the table says otherwise.

| API | Parameter | Accepted values |
|---|---|---|
| `GET /worktemplates` | `state` | `active`, `inactive`, `archived` |
| `GET /worktemplates` | `templateType` | `regular` (= fixed + flexi + split), `fixed`, `flexi`, `split`, `roster`, `rotation` |
| `GET /workplans` | `state` | `active`, `deleted` |
| `GET /workplans` | `type` | `regular`, `roster`, `rotation`. **If omitted, only regular plans are returned** |
| `GET /workassignments/details` | `state` | `active`, `inactive` |
| `GET /attpolicies` | `state` | `active`, `inactive` |
| `GET /attpolicies` | `type` | `break`, `graceperiod`, `overtime` |
| `GET /holidaylist/{year}` | `state` | `active`, `inactive` |
| Board, work plan and rotation employee lists | `segment` | `all` (or empty), `active`, `upcoming`, `past` |
| `PATCH /att-log/state/{dateRangeKey}/{employeeCode}` | body `action` | `review` (→ Approved), `approve` (→ Locked), `revert_to_draft` (→ Pending) |
| `GET /att-log/sessions/{sessionId}/grid` | `tag` | `Absent`, `AttendanceIncomplete`, `AttendanceMissing`, `AttendanceUnavailable`, `InvalidData`, `NewJoinee`. Unknown values are ignored, not rejected |
| `GET /att-log/sessions/{sessionId}/grid` | `sortBy` / `sortDir` | `employeeCode` (otherwise sorted by name) / `asc`, `desc` |
| `/me` and `/team` attendance APIs | `period` | `latest` (default), `current`, `ytd`, a salary month `YYYY-MM` (or `month:YYYY-MM`), or a session key |
| `/me` and `/team` attendance days | `status` | Any `AttendanceDayFilter` name |

### Session key format

Attendance-log URLs take a `sessionKey` or `dateRangeKey`. It names one pay period, which runs from
the 16th of one month to the 15th of the next and is named after the month it ends in. The format is
`MMMdd_yyyy_to_MMMdd_yyyy`. For example, the October 2026 salary month is
`Sep16_2026_to_Oct15_2026`.
