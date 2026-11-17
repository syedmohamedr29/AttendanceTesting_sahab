# coding: utf-8

def get_content():
    return """
## 5. Positive Test Scenarios

| TC ID | Submodule | Scenario Description | Input Data & Conditions | Expected HTTP Status | Expected Response & DB State |
|---|---|---|---|---|---|
| `POS-BRD-01` | Boards | Create Roster Board with Weekly frequency and 2 Areas | Valid EN/AR name, supervisor UUID, `publishingFrequency = 1`, `hasAreas = true`, 2 areas | `200 OK` | Board created in `ERP.Attendance.RosterBoards` with 2 areas. Returns board ID and details. |
| `POS-BRD-02` | Boards | Create Roster Board with Bi-Weekly frequency without Areas | Valid EN name, supervisor UUID, `publishingFrequency = 2`, `hasAreas = false`, `areas = []` | `200 OK` | Board created with empty areas array. |
| `POS-BRD-03` | Boards | Create Roster Board with Monthly frequency (Frequency 3) | Valid EN name, supervisor UUID, `publishingFrequency = 3` | `200 OK` | Board created with monthly planning cycle. |
| `POS-BRD-04` | Boards | Edit Roster Board name and supervisor | Updated `boardName.en`, new active supervisor UUID | `200 OK` | `updatedFields` returns modified properties. DB reflects new name and supervisor. |
| `POS-BRD-05` | Boards | Add new area to existing board | `addedAreas = [{"name": {"en": "Pharmacy Ward"}}]` | `200 OK` | New area inserted into `areas[]` array with generated area UUID. |
| `POS-BRD-06` | Boards | Rename existing area | Target `areaId`, `name = {"en": "ICU Ward B"}` | `200 OK` | Area name updated in board document and all associated roster days updated. |
| `POS-SHF-01` | Templates | Create standard day roster shift (08:00 - 16:00) | `code = "DAY01"`, `colour = "#14B8A6"`, 7 working days, duration 480 min | `200 OK` | WorkPlan and WorkTemplate (Type 4) created. `boardShiftCount` incremented. |
| `POS-SHF-02` | Templates | Create overnight roster shift (22:00 - 06:00) | `startTime = "22:00"`, `endTime = "06:00"`, `isOvernight = true`, duration 480 min | `200 OK` | Overnight shift persisted correctly with midnight cross flag. |
| `POS-SHF-03` | Templates | Create roster shift with Break & Overtime policies | `policyIds = [breakPolicyId, overtimePolicyId]`, enabled flags `true` | `200 OK` | Shift created with policies attached. Verified via `GET /workplans/{id}`. |
| `POS-SHF-04` | Templates | Edit roster shift timing before any scheduled days | Updated `rosterTimeSlots[]` (07:00 - 15:00) | `200 OK` | Shift timings updated. `republishRequired = false`. |
| `POS-MEM-01` | Employees | Check conflicts for clean employees (no prior assignments) | 3 active employee UUIDs, start date next Sunday | `200 OK` | `cleanEmployeeIds` contains all 3, `blockedEmployeeIds = []`, `canProceed = true`. |
| `POS-MEM-02` | Employees | Add employees with open-ended period (`endDate = null`) | 2 clean employees, `startDate = tomorrow`, `endDate = null` | `200 OK` | Members added to `RosterBoards.employees[]` with `endDate: null`. |
| `POS-MEM-03` | Employees | Add employee with specific area assigned | 1 clean employee, `areaId = area1UUID` | `200 OK` | Member added with `areaId` stamped. Reflected in `GET .../areas/employees`. |
| `POS-MEM-04` | Employees | Enroll employee with conflicting regular plan (`adjustConflicts: true`) | Employee on regular plan, `adjustConflicts = true` | `200 OK` | Regular plan ended early/split; employee enrolled on roster board. |
| `POS-MEM-05` | Employees | Edit effective period of upcoming membership | Update `startDate` and `endDate` | `200 OK` | Membership dates updated in MongoDB. |
| `POS-MEM-06` | Employees | Move active member to another board at same location | Target `boardId`, `effectiveFrom = tomorrow`, `adjustConflicts = false` | `200 OK` | Old membership ends day before; new membership created on target board. |
| `POS-PLN-01` | Planner | Query Schedule Plans list for current month | `frequency = Weekly`, `anchor = currentSunday` | `200 OK` | Returns all boards of company with period statuses, counts, and publish flags. |
| `POS-PLN-02` | Planner | Query Schedule Grid for specific anchor week | `anchor = 2026-11-22` | `200 OK` | Returns areas, employee rows, 7 day cells with `state` and `isAssignable`. |
| `POS-PLN-03` | Planner | Assign roster shift to multiple employees and dates | Valid `workPlanId`, `slots` with 2 employees across 4 dates | `200 OK` | `WorkAssignmentMaps` records created with `AssignmentType = 2`. |
| `POS-PLN-04` | Planner | Assign Day Off to employees | `dayOff = true`, `workPlanId = null`, 2 dates | `200 OK` | Rest day records inserted with `isDayOff: true`. |
| `POS-PLN-05` | Planner | Copy previous period shifts into empty cells | `POST /copy-previous` with valid anchor | `200 OK` | Empty cells populated matching previous week offset. Returns copied count. |
| `POS-PLN-06` | Planner | Clear draft shift assignments for specific dates | `POST /clear` with `dates = ["2026-11-25"]` | `200 OK` | Target date slots deleted. Past dates skipped. |
| `POS-PUB-01` | Publish | Publish completely filled period (`allowEmpty = false`) | All member slots filled with shift or day off, `version = 0` | `200 OK` | Status transitions to `Published`, `version = 1`, `publishedAt` recorded. |
| `POS-PUB-02` | Publish | Publish empty roster with `allowEmpty = true` | 0 shifts assigned, `allowEmpty = true` | `200 OK` | Successfully published with 0 slots. Status = `Published`. |
| `POS-PUB-03` | Publish | Republish modified published period | Period has `republishRequired = true`, send `version = 1` | `200 OK` | Period republished, `version` incremented to 2, `republishRequired = false`. |
| `POS-PUB-04` | Publish | Unpublish unstarted period | Future published period, `force = false` | `200 OK` | Status reverts to `Pending` (draft). |
| `POS-PUB-05` | Publish | Unpublish started period with force override | Period has started today, `force = true` | `200 OK` | Warning acknowledged, status reverts to `Pending`. |
| `POS-OVR-01` | Overview | Query Overview KPI summary | `from` and `to` within 7 days | `200 OK` | Returns `boardCount`, `boardsWithMembers`, `employees`, `periodsToPublish`. |
| `POS-OVR-02` | Overview | Query Today shift timeline Gantt | Current date | `200 OK` | Returns `onShiftNow`, `startingLater`, `ended`, and board timeline segments. |
| `POS-SCH-01` | Schedules | Query Schedules 7-day grid with pagination | `page = 1`, `pageSize = 10` | `200 OK` | Returns member rows with dayType (`Shift`, `DayOff`, `Holiday`, `NotPlanned`). |
| `POS-SCH-02` | Schedules | Query Member Schedule Card | Target `employeeId`, valid week anchor | `200 OK` | Returns member header, 7-day strip, side cards (board, policies, totals). |

---

## 6. Negative Test Scenarios

| TC ID | Submodule | Negative Test Scenario | Input Data & Trigger | Expected HTTP Status | Expected Error Code & Validation Error |
|---|---|---|---|---|---|
| `NEG-BRD-01` | Boards | Create board without mandatory English name | `boardName: {"en": "", "ar": "طوارئ"}` | `400 Bad Request` | `validationErrors: ["boardName.en is required."]` |
| `NEG-BRD-02` | Boards | Create board with invalid publishing frequency | `publishingFrequency: 99` | `400 Bad Request` | `validationErrors: ["publishingFrequency must be 1, 2, or 3."]` |
| `NEG-BRD-03` | Boards | Create board with supervisor from another location | Supervisor UUID belonging to Location B | `400 Bad Request` | `Cit.Attendance:9002` (Location mismatch) |
| `NEG-BRD-04` | Boards | Create board with inactive supervisor | Supervisor UUID with `IsActive: false` in EmployeeSvc | `400 Bad Request` | `Cit.Attendance:Validation` (Supervisor must be active) |
| `NEG-BRD-05` | Boards | Create board with duplicate area names | `areas = [{"name": {"en": "ICU"}}, {"name": {"en": "ICU"}}]` | `400 Bad Request` | `validationErrors: ["Area names must be unique within the board."]` |
| `NEG-BRD-06` | Boards | Delete board with active or past employee memberships | Target `boardId` having 1 past member row | `400 Bad Request` | `Cit.Attendance:1901` ("Board has employees - cannot delete") |
| `NEG-BRD-07` | Boards | Delete board with shifts scheduled today or in future | Board with 0 members but shift scheduled tomorrow | `400 Bad Request` | `Cit.Attendance:1902` ("Shift scheduled today or later") |
| `NEG-BRD-08` | Boards | Delete area currently assigned to a member | Target `areaId` assigned to 1 past or active member | `400 Bad Request` | `Cit.Attendance:1903` ("Area is used by a member - cannot delete") |
| `NEG-BRD-09` | Boards | Disable areas (`hasAreas = false`) while members have areas | Board with active members in areas, send `hasAreas: false` | `400 Bad Request` | `Cit.Attendance:1904` ("Cannot disable areas while members have areas") |
| `NEG-SHF-01` | Templates | Create roster shift exceeding 20-template location limit | Location already has 20 work templates, attempt 21st | `400 Bad Request` | `Cit.Attendance:1203` ("Maximum template limit of 20 reached for location") |
| `NEG-SHF-02` | Templates | Create roster shift with duplicate code | `code: "MORN01"` already used by a regular work plan | `400 Bad Request` | `Cit.Attendance:1106` ("Duplicate work template code") |
| `NEG-SHF-03` | Templates | Edit roster shift code | Send PATCH with modified `code: "NEWCODE"` | `400 Bad Request` | `Cit.Attendance:1107` ("Work template code cannot be modified") |
| `NEG-SHF-04` | Templates | Edit roster shift that has scheduled days on or before today | Shift with assigned roster day yesterday | `400 Bad Request` | `Cit.Attendance:1905` ("Shift already has scheduled days up to today") |
| `NEG-SHF-05` | Templates | Delete roster shift scheduled today or in future | Shift with roster day assigned for today | `400 Bad Request` | `Cit.Attendance:1304` ("Shift is in use today or later - cannot delete") |
| `NEG-SHF-06` | Templates | Create roster shift with inactive policy | Policy UUID with `isActive: false` | `400 Bad Request` | `Cit.Attendance:1506` ("Policy is inactive") |
| `NEG-SHF-07` | Templates | Create roster shift with two policies of same type | 2 Break policy UUIDs in `policyIds[]` | `400 Bad Request` | `Cit.Attendance:1508` ("Multiple policies of same type not allowed") |
| `NEG-MEM-01` | Employees | Add employee who is committed on another board | Employee currently on Board B for overlapping dates | `400 Bad Request` | `Cit.Attendance:1914` ("Employee is committed on another board/rotation") |
| `NEG-MEM-02` | Employees | Add employee on regular plan without confirming adjustment | `adjustConflicts: false`, employee on regular plan | `400 Bad Request` | `Cit.Attendance:1409` ("Regular plan in the way, adjustment not confirmed") |
| `NEG-MEM-03` | Employees | Add employee with start date in the past | New membership with `startDate = yesterday` | `400 Bad Request` | `validationErrors: ["startDate cannot be in the past for new memberships."]` |
| `NEG-MEM-04` | Employees | Add employee with `endDate < startDate` | `startDate = 2026-11-25`, `endDate = 2026-11-20` | `400 Bad Request` | `validationErrors: ["endDate cannot be earlier than startDate."]` |
| `NEG-MEM-05` | Employees | Edit period narrowing dates leaving scheduled days outside | Membership with shift on Nov 30, set `endDate = Nov 25` | `400 Bad Request` | `Cit.Attendance:Validation` (Scheduled days fall outside new period) |
| `NEG-MEM-06` | Employees | Remove member who has historical scheduled roster days | Member with 1 past roster day last month | `400 Bad Request` | `Cit.Attendance:InvalidState` ("Remove refused: member has scheduled days") |
| `NEG-MEM-07` | Employees | Move member to another board with start date in the past | `effectiveFrom = yesterday` | `400 Bad Request` | `validationErrors: ["effectiveFrom cannot be earlier than today."]` |
| `NEG-PLN-01` | Planner | Assign shift to employee not placed in an area on area board | Board has `hasAreas = true`, employee `areaId = null` | `400 Bad Request` | `Cit.Attendance:1906` ("Employee must be placed in an area before scheduling") |
| `NEG-PLN-02` | Planner | Assign shift to non-existent employee UUID | Random generated UUID in `slots[].employeeId` | `404 Not Found` | `Cit.Attendance:404` ("Employee not found on board") |
| `NEG-PLN-03` | Planner | Clear schedule specifying dates outside target period | `anchor = 2026-11-22` (Weekly), `dates = ["2026-12-15"]` | `400 Bad Request` | `Cit.Attendance:1913` ("Clear: date outside the period") |
| `NEG-PLN-04` | Planner | Copy previous on board with deleted area structure | Board with areas enabled but all areas deleted | `400 Bad Request` | `Cit.Attendance:1906` ("Unassigned area employees exist") |
| `NEG-PUB-01` | Publish | Publish period with unfilled member days (`allowEmpty = false`) | 3 member slots empty in period | `400 Bad Request` | `Cit.Attendance:1907` ("Unfilled days remain in period", lists unfilled slots) |
| `NEG-PUB-02` | Publish | Publish empty roster without setting `allowEmpty: true` | 0 shifts assigned, `allowEmpty = false` | `400 Bad Request` | `Cit.Attendance:1908` ("Period is empty and allowEmpty is false") |
| `NEG-PUB-03` | Publish | Publish completed past period | Period ended last week | `400 Bad Request` | `Cit.Attendance:1909` ("Period has ended - cannot publish or unpublish") |
| `NEG-PUB-04` | Publish | Publish with mismatched version token (concurrency conflict) | Current DB `version = 2`, client sends `version: 1` | `400 Bad Request` | `Cit.Attendance:1910` ("Concurrency conflict: version has changed") |
| `NEG-PUB-05` | Publish | Unpublish unstarted period without publish record | Period in `Pending` (draft) state | `400 Bad Request` | `Cit.Attendance:1912` ("Period is not published") |
| `NEG-PUB-06` | Publish | Unpublish started period with `force: false` | Period started yesterday, `force = false` | `400 Bad Request` | `Cit.Attendance:1911` ("Period has already started; force override required") |
| `NEG-OVR-01` | Overview | Query Overview with inverted date range (`from > to`) | `from = 2026-11-30`, `to = 2026-11-01` | `400 Bad Request` | `Cit.Attendance:2204` ("Invalid date range: to cannot be before from") |
| `NEG-OVR-02` | Overview | Query Overview with range exceeding 31 days | `from = 2026-11-01`, `to = 2026-12-15` (45 days) | `400 Bad Request` | `Cit.Attendance:2204` ("Date range cannot exceed 31 days") |
| `NEG-SCH-01` | Schedules | Query Member Schedule for employee never on any board | Employee UUID with 0 board memberships | `404 Not Found` | `Cit.Attendance:2207` ("Employee was never on a board") |

---

## 7. Equivalence Partitioning (EP) Test Scenarios

### EP Analysis: Input Partitions across Core Entities

```mermaid
graph TD
    subgraph EP_Frequencies ["Publishing Frequency EP"]
        V_Freq["Valid Class: [1 (Weekly), 2 (BiWeekly), 3 (Monthly)]"]
        INV_Freq["Invalid Class: [<1, >3, Non-integer, String]"]
    end
    subgraph EP_Publish ["Publish Period Completeness EP"]
        V_Full["Valid Class: 100% slots filled (Shift or DayOff)"]
        V_Emp["Valid Class: 0% slots filled + allowEmpty=true"]
        INV_Part["Invalid Class: Partial fill (1-99% slots) + allowEmpty=false"]
    end
    subgraph EP_Dates ["Date Range Query EP (Overview / Schedules)"]
        V_Range["Valid Class: 1 <= (to - from) <= 31 days AND from <= to"]
        INV_Inv["Invalid Class: from > to"]
        INV_Over["Invalid Class: (to - from) > 31 days"]
        INV_Single["Invalid Class: Only 'to' provided without 'from'"]
    end
```

| Partition ID | Field / Parameter | Equivalence Class Definition | Representative Test Input | Expected System Behavior |
|---|---|---|---|---|
| `EP-FREQ-01` | `publishingFrequency` | Valid: Supported integer frequencies | `1` (Weekly), `2` (BiWeekly), `3` (Monthly) | Accepted (`200 OK`). Sets period window. |
| `EP-FREQ-02` | `publishingFrequency` | Invalid: Out-of-bounds integers | `0`, `4`, `-5` | Rejected (`400 Bad Request`). Validation failure. |
| `EP-FREQ-03` | `publishingFrequency` | Invalid: Non-numeric / String types | `"Weekly"`, `null`, `1.5` | Rejected (`400 Bad Request`). Schema type mismatch. |
| `EP-PUB-01` | Publish Eligibility | Valid: 100% filled period | Every member has assigned shift or day off | Accepted (`200 OK`). Transitions to `Published`. |
| `EP-PUB-02` | Publish Eligibility | Valid: Empty period with override flag | 0 slots filled, `allowEmpty = true` | Accepted (`200 OK`). Empty period published. |
| `EP-PUB-03` | Publish Eligibility | Invalid: Incompletely filled period | 1 or more member days empty, `allowEmpty = false` | Rejected (`400 Bad Request`, `1907`). Unfilled list returned. |
| `EP-PUB-04` | Publish Eligibility | Invalid: Empty period without override flag | 0 slots filled, `allowEmpty = false` | Rejected (`400 Bad Request`, `1908`). |
| `EP-RNG-01` | Query Date Window | Valid: Normal date window within 31 days | `from = 2026-11-01`, `to = 2026-11-20` (20 days) | Accepted (`200 OK`). Data returned. |
| `EP-RNG-02` | Query Date Window | Valid: Boundary maximum range (31 days) | `from = 2026-11-01`, `to = 2026-12-01` (31 days) | Accepted (`200 OK`). |
| `EP-RNG-03` | Query Date Window | Invalid: Inverted dates (`from > to`) | `from = 2026-12-01`, `to = 2026-11-01` | Rejected (`400 Bad Request`, `2204`). |
| `EP-RNG-04` | Query Date Window | Invalid: Date range exceeding 31 days | `from = 2026-11-01`, `to = 2026-12-10` (40 days) | Rejected (`400 Bad Request`, `2204`). |
| `EP-RNG-05` | Query Date Window | Invalid: Only `to` provided without `from` | `from = null`, `to = 2026-11-20` | Rejected (`400 Bad Request`, `2204`). |

---

## 8. Boundary Value Analysis (BVA) Test Scenarios

| BVA ID | Parameter / Constraint | Boundary Level | Test Value / Condition | Expected Result & Error Code |
|---|---|---|---|---|
| `BVA-STR-01` | `boardName.en` length | Min - 1 (0 chars) | `""` (Empty string) | Rejected (`400 Bad Request`). Required field. |
| `BVA-STR-02` | `boardName.en` length | Min (1 char) | `"A"` | Accepted (`200 OK`). |
| `BVA-STR-03` | `boardName.en` length | Max (100 chars) | String of exactly 100 characters | Accepted (`200 OK`). |
| `BVA-STR-04` | `boardName.en` length | Max + 1 (101 chars) | String of 101 characters | Rejected (`400 Bad Request`). MaxLength exceeded. |
| `BVA-TPL-01` | Location Templates Limit | Current = 19 (Max - 1) | Create 20th template of any type | Accepted (`200 OK`). Total reaches 20. |
| `BVA-TPL-02` | Location Templates Limit | Current = 20 (Max) | Create 21st template of any type | Rejected (`400 Bad Request`, `1203`). Limit reached. |
| `BVA-RNG-01` | Date Range Days | Min (1 day) | `from = 2026-11-15`, `to = 2026-11-15` | Accepted (`200 OK`). Single day data returned. |
| `BVA-RNG-02` | Date Range Days | Max - 1 (30 days) | `from = 2026-11-01`, `to = 2026-11-30` | Accepted (`200 OK`). |
| `BVA-RNG-03` | Date Range Days | Max (31 days) | `from = 2026-11-01`, `to = 2026-12-01` | Accepted (`200 OK`). Exactly 31 days. |
| `BVA-RNG-04` | Date Range Days | Max + 1 (32 days) | `from = 2026-11-01`, `to = 2026-12-02` | Rejected (`400 Bad Request`, `2204`). Max range exceeded. |
| `BVA-SLT-01` | `rosterTimeSlots[]` count | Boundary < 7 (6 items) | Array with 6 daily slots | Rejected (`400 Bad Request`). Exactly 7 slots required. |
| `BVA-SLT-02` | `rosterTimeSlots[]` count | Boundary = 7 (7 items) | Array with 7 daily slots (Sunday to Saturday) | Accepted (`200 OK`). Valid weekly profile. |
| `BVA-SLT-03` | `rosterTimeSlots[]` count | Boundary > 7 (8 items) | Array with 8 daily slots | Rejected (`400 Bad Request`). |

---

## 9. Decision Table Test Scenarios

### Decision Table 1: Period Publishing Eligibility Matrix
| Condition / Rule | Rule 1 | Rule 2 | Rule 3 | Rule 4 | Rule 5 | Rule 6 |
|---|---|---|---|---|---|---|
| Period has ended (past anchor)? | **Yes** | No | No | No | No | No |
| Sent version matches current DB version? | - | **No** | Yes | Yes | Yes | Yes |
| 100% member slots filled (shift or day off)? | - | - | **Yes** | No | No | No |
| Period is completely empty (0 slots)? | - | - | No | **Yes** | **Yes** | No |
| `allowEmpty` flag set to `true`? | - | - | - | **Yes** | **No** | - |
| **Expected Outcome** | **Fail** | **Fail** | **Pass** | **Pass** | **Fail** | **Fail** |
| **Returned Code / Status** | `1909` (Period ended) | `1910` (Concurrency) | `200 OK` (Published) | `200 OK` (Published) | `1908` (Empty refused) | `1907` (Unfilled days) |

### Decision Table 2: Employee Enrollment Conflict Preflight Matrix
| Condition / Rule | Case 1: Clean | Case 2: Blocked | Case 3: Adjustable | Case 4: Duplicate |
|---|---|---|---|---|
| Employee active in EmployeeSvc at board location? | Yes | Yes | Yes | Yes |
| Already active member of another Roster Board for dates? | No | **Yes** | No | No |
| Currently enrolled in a Shift Rotation for dates? | No | **Yes** | No | No |
| Currently assigned to a Regular Work Plan for dates? | No | No | **Yes** | No |
| Already enrolled on this target Roster Board for dates? | No | No | No | **Yes** |
| **Preflight Conflict Result** | **AVAILABLE** | **BLOCKED** | **ADJUSTABLE** | **ALREADY ON BOARD** |
| **`canProceed` Flag** | `true` | `false` | `false` (until confirmed) | `false` |
| **Action Required** | Directly Add | Must Skip Employee | Confirm Adjust Plan (`adjustConflicts: true`) | View / Skip |

---

## 10. State Transition Scenarios

### 10.1 Period Lifecycle State Transitions
```mermaid
stateDiagram-v2
    [*] --> NOT_PLANNED : Board created, no slots assigned
    NOT_PLANNED --> PENDING : Assign shift / day off
    PENDING --> PENDING : Edit draft slots / Clear / Copy
    PENDING --> PUBLISHED : POST .../publish (100% filled, version 1)
    
    state PUBLISHED {
        [*] --> CleanPublished
        CleanPublished --> ChangesNotPublished : Slot edited / member changed
        ChangesNotPublished --> CleanPublished : POST .../publish (republish, version 2)
    }
    
    PUBLISHED --> PENDING : POST .../unpublish (force if started)
    PUBLISHED --> COMPLETED : Period anchor date passes
    PENDING --> COMPLETED : Period anchor date passes
    NOT_PLANNED --> COMPLETED : Period anchor date passes
    COMPLETED --> [*] : Locked permanently
```

| Transition ID | Current State | Triggering API / Event | Preconditions | Target State | DB Assertions |
|---|---|---|---|---|---|
| `ST-PER-01` | `NOT PLANNED` | `POST .../schedule/assign` | Period has 0 roster days | `PENDING` | `WorkAssignmentMaps` records exist. Period status = `Pending`. |
| `ST-PER-02` | `PENDING` | `POST .../schedule/publish` | All member slots filled, `allowEmpty = false` | `PUBLISHED` | `RosterSchedulePeriods` created with `status: Published`, `version: 1`, `changesNotPublished: false`. |
| `ST-PER-03` | `PUBLISHED` | `POST .../schedule/assign` | Period already published; supervisor modifies slot | `PUBLISHED` (`Changes not published`) | `RosterSchedulePeriods.changesNotPublished = true`. Version remains 1. |
| `ST-PER-04` | `PUBLISHED` (Changed) | `POST .../schedule/publish` | Republish period after modification | `PUBLISHED` | `RosterSchedulePeriods.changesNotPublished = false`. `version = 2`. |
| `ST-PER-05` | `PUBLISHED` | `POST .../schedule/unpublish` | Unstarted period, `force = false` | `PENDING` | Period status reverts to `Pending`. Visible to employees reverts to "Not scheduled". |
| `ST-PER-06` | Any State | Clock advances past period end | Calendar date > Period end date | `COMPLETED` | Read-only. `POST /publish` and `POST /unpublish` return `1909`. |

### 10.2 Board Membership Lifecycle State Transitions
| Transition ID | Current State | Triggering Event | Date Condition | Target State | UI Menu & Operations Permitted |
|---|---|---|---|---|---|
| `ST-MEM-01` | Initial | `PATCH .../employees` | `startDate > today` | `UPCOMING` | Edit effective period, Remove from board. |
| `ST-MEM-02` | `UPCOMING` | Calendar date reaches `startDate` | `startDate <= today <= (endDate ?? inf)` | `ACTIVE` | Move to another plan, Edit effective period (end date only). |
| `ST-MEM-03` | `ACTIVE` | Calendar date passes `endDate` | `today > endDate` | `PAST` | Read-only row. No action menu available. |
"""
