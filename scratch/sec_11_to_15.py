# coding: utf-8

def get_content():
    return """
## 11. Dedicated POST API Test Cases

### TC-POST-01: Create Roster Board with Multi-Area Setup
- **Endpoint:** `POST /api/companies/{companyId}/roster-boards?locationId={locationId}`
- **Scenario:** Senior manager provisions a new departmental roster board with Weekly frequency and two operational areas.
- **Request Payload:**
```json
{
  "tenantName": { "en": "Demo Tenant", "ar": "المستأجر التجريبي" },
  "boardName": { "en": "Critical Care Roster", "ar": "جدول العناية المركزة" },
  "supervisor": {
    "employeeId": "39879386-4c24-ee4c-84ec-6eb7daa765ac",
    "name": { "en": "Dr. Tariq Supervisor", "ar": "د. طارق المشرف" },
    "employeeCode": "EMP-0091"
  },
  "publishingFrequency": 1,
  "hasAreas": true,
  "areas": [
    { "name": { "en": "Trauma ICU", "ar": "عناية الحوادث" } },
    { "name": { "en": "Surgical ICU", "ar": "العناية الجراحية" } }
  ]
}
```
- **Execution Steps:**
  1. Authenticate with valid Bearer token.
  2. Send `POST` to endpoint with valid `locationId` in query.
  3. Validate HTTP status `200 OK`.
  4. Capture generated `boardId` from response.
- **Expected Response:** `HTTP 200 OK` with full board representation, generated board UUID, and area UUIDs.
- **DB Verification:** `db.getCollection("ERP.Attendance.RosterBoards").findOne({"_id": UUID("...")})` confirms document persisted with `hasAreas: true` and 2 embedded areas.

---

### TC-POST-02: Create Custom Roster Shift (Work Plan & Template)
- **Endpoint:** `POST /api/companies/{companyId}/workplans/roster?locationId={locationId}`
- **Scenario:** Define a custom 8-hour morning shift linked to the newly created Roster Board with Break Policy attached.
- **Request Payload:**
```json
{
  "tenantName": { "en": "Demo Tenant" },
  "boardId": "b0b0a1a2-3b4c-5d6e-7f8a-9b0c1d2e3f4a",
  "shiftName": { "en": "Morning Shift A", "ar": "وردية الصباح أ" },
  "code": "MSHIFT-01",
  "colour": "#14B8A6",
  "description": "Standard morning acute care shift",
  "rosterTimeSlots": [
    { "dayEnum": 0, "isWorkingDay": true, "startTime": "07:00", "endTime": "15:00", "workDurationInMinutes": 480 },
    { "dayEnum": 1, "isWorkingDay": true, "startTime": "07:00", "endTime": "15:00", "workDurationInMinutes": 480 },
    { "dayEnum": 2, "isWorkingDay": true, "startTime": "07:00", "endTime": "15:00", "workDurationInMinutes": 480 },
    { "dayEnum": 3, "isWorkingDay": true, "startTime": "07:00", "endTime": "15:00", "workDurationInMinutes": 480 },
    { "dayEnum": 4, "isWorkingDay": true, "startTime": "07:00", "endTime": "15:00", "workDurationInMinutes": 480 },
    { "dayEnum": 5, "isWorkingDay": true, "startTime": "07:00", "endTime": "15:00", "workDurationInMinutes": 480 },
    { "dayEnum": 6, "isWorkingDay": true, "startTime": "07:00", "endTime": "15:00", "workDurationInMinutes": 480 }
  ],
  "totalWorkDurationInMinutes": 3360,
  "totalWorkingDays": 7,
  "totalDaysOff": 0,
  "isBreakPolicyEnabled": true,
  "isOvertimePolicyEnabled": false,
  "isGracePeriodPolicyEnabled": false,
  "policyIds": ["c1a2b3d4-e5f6-7a8b-9c0d-1e2f3a4b5c6d"]
}
```
- **Expected Response:** `HTTP 200 OK` returning `workPlan` and `workTemplate` objects.
- **DB Verification:** `ERP.Attendance.WorkPlans` has `PlanType: 2`; `ERP.Attendance.WorkTemplates` has `TemplateType: 4` and `LocationId` matching query.

---

### TC-POST-03: Preflight Conflict Check for Employee Enrollment
- **Endpoint:** `POST /api/companies/{companyId}/roster-boards/{boardId}/employees/check-conflicts?locationId={locationId}`
- **Scenario:** Verify conflict resolution engine before committing employee assignments.
- **Request Payload:**
```json
{
  "employeeIds": [
    "39879386-4c24-ee4c-84ec-6eb7daa765ac",
    "4a5b6c7d-8e9f-0a1b-2c3d-4e5f6a7b8c9d"
  ],
  "startDate": "2026-11-22",
  "endDate": "2027-11-21"
}
```
- **Expected Response:** `HTTP 200 OK` categorizing candidates into `cleanEmployeeIds`, `adjustableEmployeeIds`, and `blockedEmployeeIds`.

---

### TC-POST-04: Assign Roster Shifts to Multiple Employees and Dates
- **Endpoint:** `POST /api/companies/{companyId}/roster-boards/{boardId}/schedule/assign?locationId={locationId}`
- **Scenario:** Allocate "Morning Shift A" to 2 nurses across Sunday through Tuesday.
- **Request Payload:**
```json
{
  "workPlanId": "a1ae96cd-587b-4145-8859-3b42877ea4a5",
  "dayOff": false,
  "slots": [
    {
      "employeeId": "39879386-4c24-ee4c-84ec-6eb7daa765ac",
      "dates": ["2026-11-22", "2026-11-23", "2026-11-24"]
    },
    {
      "employeeId": "4a5b6c7d-8e9f-0a1b-2c3d-4e5f6a7b8c9d",
      "dates": ["2026-11-22", "2026-11-23"]
    }
  ]
}
```
- **Expected Response:** `HTTP 200 OK` with assigned slot count = 5.
- **DB Verification:** 5 records inserted into `ERP.Attendance.WorkAssignmentMaps` with `AssignmentType: 2` and `WorkPlanId`.

---

### TC-POST-05: Assign Scheduled Day Off
- **Endpoint:** `POST /api/companies/{companyId}/roster-boards/{boardId}/schedule/assign?locationId={locationId}`
- **Scenario:** Allocate scheduled rest days (Day Off) for the remainder of the week.
- **Request Payload:**
```json
{
  "workPlanId": null,
  "dayOff": true,
  "slots": [
    {
      "employeeId": "39879386-4c24-ee4c-84ec-6eb7daa765ac",
      "dates": ["2026-11-25", "2026-11-26", "2026-11-27", "2026-11-28"]
    }
  ]
}
```
- **Expected Response:** `HTTP 200 OK`.
- **DB Verification:** 4 records inserted into `ERP.Attendance.WorkAssignmentMaps` with `IsDayOff: true`.

---

### TC-POST-06: Publish Schedule Period
- **Endpoint:** `POST /api/companies/{companyId}/roster-boards/{boardId}/schedule/publish?locationId={locationId}`
- **Scenario:** Commit and lock the weekly period once 100% of member slots are allocated.
- **Request Payload:**
```json
{
  "anchor": "2026-11-22",
  "version": 0,
  "allowEmpty": false
}
```
- **Expected Response:** `HTTP 200 OK` returning `status: "Published"`, `version: 1`, `publishedSlotCount: 14`, `publishedEmployeeCount: 2`.
- **DB Verification:** `ERP.Attendance.RosterSchedulePeriods` contains record with `Status: "Published"`, `Version: 1`.

---

### TC-POST-07: Unpublish Period with Force Override
- **Endpoint:** `POST /api/companies/{companyId}/roster-boards/{boardId}/schedule/unpublish?locationId={locationId}`
- **Scenario:** Supervisor unlocks a started period to accommodate emergency doctor swapping.
- **Request Payload:**
```json
{
  "anchor": "2026-11-22",
  "force": true
}
```
- **Expected Response:** `HTTP 200 OK` returning `status: "Pending"`.

---

## 12. Dedicated PATCH API Test Cases

### TC-PAT-01: Update Board Configuration and Add Areas
- **Endpoint:** `PATCH /api/companies/{companyId}/roster-boards/{boardId}?locationId={locationId}`
- **Scenario:** Partial update to rename board and add a new area.
- **Request Payload:**
```json
{
  "boardName": { "en": "Updated ICU & Trauma Roster" },
  "addedAreas": [
    { "name": { "en": "Burn Unit", "ar": "وحدة الحروق" } }
  ]
}
```
- **Expected Response:** `HTTP 200 OK` with `updatedFields` containing `["boardName", "addedAreas"]`.
- **Assertions:** Existing supervisor, frequency, and previously created areas remain unchanged in MongoDB.

---

### TC-PAT-02: Enroll Employees onto Roster Board with Regular Plan Adjustment
- **Endpoint:** `PATCH /api/companies/{companyId}/roster-boards/{boardId}/employees?locationId={locationId}`
- **Scenario:** Commit enrollment of employees, confirming adjustment of overlapping regular work plans.
- **Request Payload:**
```json
{
  "employeeIds": [
    "39879386-4c24-ee4c-84ec-6eb7daa765ac",
    "4a5b6c7d-8e9f-0a1b-2c3d-4e5f6a7b8c9d"
  ],
  "startDate": "2026-11-22",
  "endDate": null,
  "areaId": "a900b1c2-3d4e-5f6a-7b8c-9d0e1f2a3b4c",
  "adjustConflicts": true
}
```
- **Expected Response:** `HTTP 200 OK` reporting `addedCount: 2`, `skippedCount: 0`.
- **DB Verification:** `RosterBoards.employees[]` array contains 2 membership elements with `areaId` stamped.

---

### TC-PAT-03: Update Membership Effective Period
- **Endpoint:** `PATCH /api/companies/{companyId}/roster-boards/{boardId}/employees/{membershipId}/period?locationId={locationId}`
- **Scenario:** Extend an employee's assignment end date.
- **Request Payload:**
```json
{
  "startDate": "2026-11-22",
  "endDate": "2027-06-30",
  "adjustConflicts": false
}
```
- **Expected Response:** `HTTP 200 OK` with `publishReverted: false`.

---

### TC-PAT-04: Execute Member Move to Another Roster Board
- **Endpoint:** `PATCH /api/companies/{companyId}/roster-boards/{boardId}/employees/{membershipId}/move?locationId={locationId}`
- **Scenario:** Transfer an active employee to a different board within the same hospital location.
- **Request Payload:**
```json
{
  "targetType": 1,
  "targetBoardId": "c5efa2f2-d219-4ad7-9c77-947353e853e5",
  "effectiveFrom": "2026-11-25",
  "endDate": null,
  "adjustConflicts": true
}
```
- **Expected Response:** `HTTP 200 OK` returning `releasedScheduleCount` (slots deleted from effective date onward).
- **Assertions:** Original membership ends on `2026-11-24`; new membership created on target board starting `2026-11-25` with `areaId: null`.

---

### TC-PAT-05: Assign Employees to Area (Setup Step)
- **Endpoint:** `PATCH /api/companies/{companyId}/roster-boards/{boardId}/areas/{areaId}/employees?locationId={locationId}`
- **Scenario:** Allocate unassigned board members into "Trauma ICU" area.
- **Request Payload:**
```json
{
  "employeeIds": [
    "39879386-4c24-ee4c-84ec-6eb7daa765ac"
  ]
}
```
- **Expected Response:** `HTTP 200 OK` with `assignedEmployeeIds` containing the target employee.

---

## 13. Dedicated GET API Verification Test Cases

| TC ID | Endpoint & Query | Verification Scope | Payload vs GET vs DB Assertions |
|---|---|---|---|
| `GET-VER-01` | `GET /workplans?type=roster&locationId={id}` | List roster shifts | Returns all shifts with `planType = 2`. Verify shift name, code, colour, total duration, and policy badges. |
| `GET-VER-02` | `GET /workplans/{id}` | Shift details by ID | Compare with POST request: `rosterTimeSlots` (all 7 days), overnight flag, attached policy IDs match MongoDB. |
| `GET-VER-03` | `GET /roster-boards?locationId={id}` | List boards for location | Verify board name, supervisor name/code, frequency enum, member counts, area counts match MongoDB. |
| `GET-VER-04` | `GET /roster-boards/{boardId}` | Board full details | Verify embedded `areas[]`, `employees[]` (upcoming, active, past), counts, and linked work plans. |
| `GET-VER-05` | `GET /schedule-plans?frequency=Weekly&anchor={date}` | Schedule plans dashboard | Verify board row contains accurate `status` (Not planned, Pending, Published, Completed), unfilled slot count, and version. |
| `GET-VER-06` | `GET /roster-boards/{boardId}/schedule?anchor={date}` | Interactive planner grid | Verify employee rows grouped by area, each cell contains `dayType`, `workPlanId`, `isDayOff`, and `isAssignable`. |
| `GET-VER-07` | `GET /overview/summary?from={date}&to={date}` | Executive KPI summary | Verify `boardCount`, `boardsWithMembers`, `employees`, `periodsToPublish`. Note: leave fields expected null. |
| `GET-VER-08` | `GET /overview/today` | Real-time shift timeline | Verify `onShiftNow`, `startingLater`, `ended`, and board timeline segments against current UTC/Riyadh time. |
| `GET-VER-09` | `GET /schedules?from={date}&to={date}` | Read-only schedules grid | Verify 10 members per page, pagination tokens, cell states (`Shift`, `DayOff`, `Holiday`, `NotPlanned`, `NotOnBoard`). |
| `GET-VER-10` | `GET /schedules/employees/{empId}?from={date}&to={date}` | Member schedule card | Verify member header, daily shift list, attached policies (grace, break, overtime), and side cards. |

---

## 14. End-to-End Functional Workflows

### Workflow 1: Green-Field Board Setup to Published Roster
```mermaid
sequenceDiagram
    autonumber
    actor HR as HR / Supervisor
    participant Svc as SP.AttendanceSvc
    participant DB as MongoDB

    HR->>Svc: POST /roster-boards (Name, Weekly, Supervisor, 2 Areas)
    Svc->>DB: Insert ERP.Attendance.RosterBoards
    Svc-->>HR: HTTP 200 OK (boardId generated)

    HR->>Svc: POST /workplans/roster (Morning Shift 07:00-15:00)
    Svc->>DB: Insert ERP.Attendance.WorkPlans & WorkTemplates (Type 4)
    Svc-->>HR: HTTP 200 OK (workPlanId generated)

    HR->>Svc: POST .../employees/check-conflicts (2 Employees)
    Svc-->>HR: HTTP 200 OK (cleanEmployeeIds: 2, canProceed: true)

    HR->>Svc: PATCH .../employees (Enroll 2 Employees, Area 1)
    Svc->>DB: Push to RosterBoards.employees[]
    Svc-->>HR: HTTP 200 OK

    HR->>Svc: GET .../schedule?anchor=2026-11-22
    Svc-->>HR: HTTP 200 OK (14 unfilled slots)

    HR->>Svc: POST .../schedule/assign (Assign Morning Shift to all slots)
    Svc->>DB: Insert 14 slots in ERP.Attendance.WorkAssignmentMaps
    Svc-->>HR: HTTP 200 OK

    HR->>Svc: POST .../schedule/publish (anchor, version: 0, allowEmpty: false)
    Svc->>DB: Insert ERP.Attendance.RosterSchedulePeriods (Published, version: 1)
    Svc-->>HR: HTTP 200 OK (Period Published!)

    HR->>Svc: GET /me/schedule (as Employee)
    Svc-->>HR: HTTP 200 OK (Published shifts visible on mobile/ESS)
```

---

### Workflow 2: Mid-Period Schedule Adjustment & Republishing Lifecycle
```mermaid
sequenceDiagram
    autonumber
    actor Sup as Supervisor
    participant Svc as SP.AttendanceSvc
    participant DB as MongoDB

    Note over Sup,DB: Period 2026-11-22 is currently PUBLISHED (version: 1)

    Sup->>Svc: POST .../schedule/assign (Modify Tuesday slot for Nurse A to Day Off)
    Svc->>DB: Update WorkAssignmentMaps (IsDayOff: true)
    Svc->>DB: Set RosterSchedulePeriods.changesNotPublished = true
    Svc-->>Sup: HTTP 200 OK

    Sup->>Svc: GET .../schedule?anchor=2026-11-22
    Svc-->>Sup: HTTP 200 OK (Status: Published, republishRequired: true)

    Sup->>Svc: POST .../schedule/publish (anchor, version: 1)
    Svc->>DB: Set RosterSchedulePeriods.changesNotPublished = false, version = 2
    Svc-->>Sup: HTTP 200 OK (Republished!)
```

---

### Workflow 3: Conflict Preflight, Regular Plan Adjustment & Cross-Board Move
```mermaid
sequenceDiagram
    autonumber
    actor HR as HR Admin
    participant Svc as SP.AttendanceSvc
    participant DB as MongoDB

    HR->>Svc: POST .../employees/check-conflicts (Doctor B on Regular Plan)
    Svc-->>HR: HTTP 200 OK (adjustableEmployeeIds: [DocB], canProceed: false)

    HR->>Svc: PATCH .../employees (adjustConflicts: true)
    Svc->>DB: Truncate Doctor B's Regular Plan in ERP.Attendance.WorkAssignmentMaps
    Svc->>DB: Add Doctor B to Roster Board
    Svc-->>HR: HTTP 200 OK (Adjusted & Enrolled)

    Note over HR,DB: 2 Weeks Later: Doctor B moves to Emergency Board

    HR->>Svc: POST .../move/check-conflicts (targetBoardId, effectiveFrom: nextWeek)
    Svc-->>HR: HTTP 200 OK (hasConflicts: false)

    HR->>Svc: PATCH .../move (targetBoardId, effectiveFrom: nextWeek)
    Svc->>DB: Terminate membership on old board at effectiveFrom - 1
    Svc->>DB: Delete old future roster slots
    Svc->>DB: Create new membership on target board (areaId: null)
    Svc-->>HR: HTTP 200 OK (Transfer complete)
```

---

## 15. Business Rule Validation Suite

### Rule 1: 1901 — Board Deletion Blocked by Existing Memberships
- **Business Requirement:** A Roster Board with any historical or active employee membership records cannot be deleted.
- **Preconditions:** Board exists with at least 1 past member row.
- **Execution:** Send `DELETE /api/companies/{companyId}/roster-boards/{boardId}?locationId={locationId}`.
- **Expected API Result:** `HTTP 400 Bad Request` with error code `Cit.Attendance:1901` ("Board has employees - cannot delete").
- **Expected DB State:** Board remains intact in `ERP.Attendance.RosterBoards`.

### Rule 2: 1902 — Board Deletion Blocked by Scheduled Shifts Today or Later
- **Business Requirement:** A board with 0 members but having shifts scheduled today or in the future cannot be deleted.
- **Preconditions:** Board has no members, but a shift has an assigned date today or later.
- **Execution:** Send `DELETE /api/companies/{companyId}/roster-boards/{boardId}`.
- **Expected API Result:** `HTTP 400 Bad Request` with `Cit.Attendance:1902`.

### Rule 3: 1903 — Area Deletion Blocked by Member Assignment
- **Business Requirement:** An area assigned to any employee (active or past) cannot be deleted.
- **Preconditions:** Area assigned to at least 1 membership row.
- **Execution:** Send `DELETE /api/companies/{companyId}/roster-boards/{boardId}/areas/{areaId}`.
- **Expected API Result:** `HTTP 400 Bad Request` with `Cit.Attendance:1903` ("Area is used by a member - cannot delete").

### Rule 4: 1904 — Areas Cannot Be Disabled While Assigned Members Exist
- **Business Requirement:** `hasAreas` cannot be updated from `true` to `false` if any member has an assigned area.
- **Execution:** Send `PATCH /roster-boards/{boardId}` with `{"hasAreas": false}`.
- **Expected API Result:** `HTTP 400 Bad Request` with `Cit.Attendance:1904`.

### Rule 5: 1905 — Roster Shift Immutability Once Scheduled
- **Business Requirement:** A roster shift (work plan) cannot be edited once any of its assigned days falls on or before today.
- **Preconditions:** Shift was assigned to an employee yesterday.
- **Execution:** Send `PATCH /workplans/roster/{id}` with modified timings.
- **Expected API Result:** `HTTP 400 Bad Request` with `Cit.Attendance:1905` ("Shift already has scheduled days up to today - cannot be edited").

### Rule 6: 1906 — Area Enforcement in Schedule Allocation
- **Business Requirement:** On a board where areas are enabled (`hasAreas = true`), an employee must be placed into an area before any shift or day off can be scheduled.
- **Preconditions:** Member enrolled on area board with `areaId: null`.
- **Execution:** Send `POST .../schedule/assign` targeting the unassigned member.
- **Expected API Result:** `HTTP 400 Bad Request` with `Cit.Attendance:1906` ("Employee must be placed in an area before scheduling").

### Rule 7: 1907 — Incomplete Period Publishing Blocked
- **Business Requirement:** Publishing a period requires 100% of member slots across all dates to be filled with either a shift or a day off.
- **Preconditions:** Period has 1 unfilled slot.
- **Execution:** Send `POST .../schedule/publish` with `allowEmpty: false`.
- **Expected API Result:** `HTTP 400 Bad Request` with `Cit.Attendance:1907`, returning `unfilledSlotCount` and the list of incomplete employees.

### Rule 8: 1203 — 20-Template Limit per Location Enforcement
- **Business Requirement:** A physical location can hold at most 20 work templates of all types combined.
- **Preconditions:** Location currently has 20 active work templates.
- **Execution:** Send `POST /workplans/roster` targeting this location.
- **Expected API Result:** `HTTP 400 Bad Request` with `Cit.Attendance:1203` ("Maximum template limit of 20 reached for location").
"""
