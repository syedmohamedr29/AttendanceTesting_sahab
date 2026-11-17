# coding: utf-8

def get_content():
    return """
## 16. Database Verification Queries (MongoDB)

All database queries must be executed in read-only mode against MongoDB host `10.1.0.4:27018`, database `Sahab`.

### 16.1 Verify Roster Board Structure & Embedded Memberships
```javascript
// Query Roster Board by Board ID
db.getCollection("ERP.Attendance.RosterBoards").find(
  { "_id": UUID("b0b0a1a2-3b4c-5d6e-7f8a-9b0c1d2e3f4a") },
  { "boardName": 1, "locationId": 1, "publishingFrequency": 1, "hasAreas": 1, "areas": 1, "employees": 1 }
).pretty();

// Verify Employee Membership count & active status inside board
db.getCollection("ERP.Attendance.RosterBoards").aggregate([
  { "$match": { "_id": UUID("b0b0a1a2-3b4c-5d6e-7f8a-9b0c1d2e3f4a") } },
  { "$unwind": "$employees" },
  { "$project": {
      "employeeId": "$employees.employeeId",
      "startDate": "$employees.startDate",
      "endDate": "$employees.endDate",
      "areaId": "$employees.areaId"
    }
  }
]);
```

### 16.2 Verify Roster Work Plan & Underlying Roster Work Template
```javascript
// Verify Roster Work Plan (PlanType = 2)
db.getCollection("ERP.Attendance.WorkPlans").find(
  { "_id": UUID("a1ae96cd-587b-4145-8859-3b42877ea4a5"), "planType": 2 },
  { "workPlanName": 1, "boardId": 1, "workTemplateId": 1, "planType": 1 }
);

// Verify Underlying Work Template (TemplateType = 4)
db.getCollection("ERP.Attendance.WorkTemplates").find(
  { "_id": UUID("c5efa2f2-d219-4ad7-9c77-947353e853e5"), "templateType": 4 },
  { "templateName": 1, "code": 1, "colour": 1, "rosterTimeSlots": 1, "policyIds": 1 }
);
```

### 16.3 Verify Atomic Daily Schedule Slots (`WorkAssignmentMaps`)
```javascript
// Verify Roster Slots for target employee in period (AssignmentType = 2)
db.getCollection("ERP.Attendance.WorkAssignmentMaps").find(
  {
    "companyId": UUID("3a24e5e5-302e-91bd-feaa-b07979766dfe"),
    "employeeId": UUID("39879386-4c24-ee4c-84ec-6eb7daa765ac"),
    "assignmentType": 2,
    "date": { "$gte": ISODate("2026-11-22T00:00:00Z"), "$lte": ISODate("2026-11-28T23:59:59Z") }
  },
  { "date": 1, "workPlanId": 1, "isDayOff": 1, "areaId": 1, "assignmentType": 1 }
).sort({ "date": 1 });
```

### 16.4 Verify Period Publication State (`RosterSchedulePeriods`)
```javascript
// Verify published period status, version, and changes flag
db.getCollection("ERP.Attendance.RosterSchedulePeriods").find(
  {
    "boardId": UUID("b0b0a1a2-3b4c-5d6e-7f8a-9b0c1d2e3f4a"),
    "anchor": "2026-11-22"
  },
  { "status": 1, "version": 1, "changesNotPublished": 1, "publishedAt": 1, "publishedBy": 1 }
);
```

---

## 17. Cross-Module Regression Test Cases

| TC ID | Dependent Module | Regression Scenario Description | Verification Point & Expected Behavior |
|---|---|---|---|
| `REG-ATT-01` | Daily Attendance Engine | Evaluate actual biometric punch against published roster slot | When employee punches at 06:55 and 15:05 on a day scheduled with "Morning Shift" (07:00-15:00), Attendance Log resolves shift boundaries from Roster day slot. Status = `Present`, 0 min late. |
| `REG-ATT-02` | Daily Attendance Engine | Biometric punch on scheduled Day Off | Employee punches on a date with `isDayOff: true`. Attendance Log records Rest Day Work / Overtime according to the active Overtime Policy. |
| `REG-ATT-03` | Shifts & Rotation | Precedence of Roster day over Regular Work Plan | Employee has a continuous Regular Work Plan (Fixed 09:00-17:00) and is assigned a Roster Shift (07:00-15:00) on 2026-11-23. Reader must resolve Roster Day first (`AssignmentType: 2` overrides `AssignmentType: 1`). |
| `REG-HOL-01` | Holiday Calendar | Assigning roster shift on an official Public Holiday | When a roster shift is assigned on a declared Public Holiday, the grid displays `HolidayWorked`. Attendance Log calculates holiday compensation rate per Attendance Policy. |
| `REG-LEA-01` | Leave Module | Scheduled employee submits Annual Leave | Leave submitted and approved. Verify whether grid reflects leave or if Scheduler remains unaware (Validates documented Leave integration status). |
| `REG-OVT-01` | Overtime Calculation | Weekly hours exceeding statutory cap (>48 hours) | Assigning 7 consecutive 8-hour shifts (56 hours). Planner and Excel export must highlight hours over 48 in red; Overtime Engine triggers weekly overtime threshold calculation. |

---

## 18. Security, Tenant Isolation & Data Integrity Test Cases

| TC ID | Security Category | Attack Vector / Negative Condition | Execution Steps & Payload | Expected Result & Audit Log |
|---|---|---|---|---|
| `SEC-IDOR-01` | IDOR / Tenant Isolation | Cross-Company Board Access | Send `GET /api/companies/{CompanyA}/roster-boards/{BoardOfCompanyB}` | Returns `HTTP 404 Not Found` or `403 Forbidden` (`Cit.Attendance:9001`). No cross-tenant data leak. |
| `SEC-IDOR-02` | IDOR / Tenant Isolation | Cross-Company Slot Mutation | Send `POST /schedule/assign` under Company A using a `workPlanId` belonging to Company B | Returns `HTTP 400 Bad Request` (`Cit.Attendance:9001`). Cross-tenant entity mapping blocked. |
| `SEC-LOC-01` | Location Boundary | Cross-Location Supervisor Assignment | Create Roster Board at Location 1 specifying supervisor belonging to Location 2 | Returns `HTTP 400 Bad Request` (`Cit.Attendance:9002`). Physical location boundaries enforced. |
| `SEC-LOC-02` | Location Boundary | Cross-Location Board Move | Send `PATCH .../move` targeting a board at a different physical location | Returns `HTTP 400 Bad Request` (`Cit.Attendance:9002`). Cross-location transfer refused. |
| `SEC-EMP-01` | Data Integrity | Inactive Employee Assignment Leakage | Send `PATCH .../employees` with an inactive employee (`SA-EMP-0006`, `IsActive: false`) | Must return `HTTP 400 Bad Request`. Prevents orphaned header bug (*Defect 59 & Defect 69*). |
| `SEC-CON-01` | Concurrency Control | Concurrent Period Publication Conflict | User A and User B simultaneously publish period; User B sends stale `version = 0` after User A incremented to `1` | User A succeeds (`200 OK`, `version = 1`); User B is rejected (`HTTP 400`, `Cit.Attendance:1910`). |
| `SEC-AUTH-01` | Authentication | Request without Authorization Header | Send `POST /roster-boards` omitting `Authorization: Bearer <token>` | Returns `HTTP 401 Unauthorized`. |
| `SEC-AUTH-02` | Authorization | Low-privilege Employee role mutation | Send `POST /schedule/publish` using token belonging to a basic non-supervisor employee | Returns `HTTP 403 Forbidden`. |

---

## 19. Requirement Traceability Matrix (RTM)

| Requirement ID | Business Requirement Description | API Endpoint Covered | Field / Business Rule | Associated Test Case IDs | Test Type | Priority | Coverage Status |
|---|---|---|---|---|---|---|---|
| `REQ-SCHED-01` | Provision Roster Board with location, supervisor, frequency & areas | `POST /roster-boards` | `boardName`, `supervisor`, `frequency`, `areas` | `POS-BRD-01`, `POS-BRD-02`, `NEG-BRD-01`, `TC-POST-01` | Functional / API | Critical | Covered |
| `REQ-SCHED-02` | Enforce single supervisor active at board location | `POST /roster-boards` | `supervisor.employeeId` | `NEG-BRD-03`, `NEG-BRD-04`, `SEC-LOC-01` | Security / Business | High | Covered |
| `REQ-SCHED-03` | Enforce frequency domain (1=Weekly, 2=BiWeekly, 3=Monthly) | `POST /roster-boards` | `publishingFrequency` | `POS-BRD-03`, `NEG-BRD-02`, `EP-FREQ-01` | BVA / EP | High | Covered |
| `REQ-SCHED-04` | Prevent board deletion with existing active or past members | `DELETE /roster-boards/{id}` | Rule `1901` | `NEG-BRD-06`, Rule 1 Suite | Business Rule | Critical | Covered |
| `REQ-SCHED-05` | Prevent board deletion with shifts scheduled today or future | `DELETE /roster-boards/{id}` | Rule `1902` | `NEG-BRD-07`, Rule 2 Suite | Business Rule | Critical | Covered |
| `REQ-SCHED-06` | Prevent area deletion while assigned to any member | `DELETE .../areas/{id}` | Rule `1903` | `NEG-BRD-08`, Rule 3 Suite | Business Rule | High | Covered |
| `REQ-SCHED-07` | Prevent disabling areas while assigned members exist | `PATCH /roster-boards/{id}` | Rule `1904` | `NEG-BRD-09`, Rule 4 Suite | Business Rule | High | Covered |
| `REQ-SCHED-08` | Create board-specific Roster Shift & Template (Type 4) | `POST /workplans/roster` | `rosterTimeSlots`, `code`, `colour` | `POS-SHF-01`, `POS-SHF-02`, `TC-POST-02` | Functional / API | Critical | Covered |
| `REQ-SCHED-09` | Enforce 20-template limit per physical location | `POST /workplans/roster` | Rule `1203` | `NEG-SHF-01`, `BVA-TPL-02`, Rule 8 Suite | Boundary / Business | Critical | Covered |
| `REQ-SCHED-10` | Enforce global code uniqueness across work plans | `POST /workplans/roster` | `code`, Rule `1106` | `NEG-SHF-02` | Data Integrity | High | Covered |
| `REQ-SCHED-11` | Lock shift code from modification on edit | `PATCH /workplans/roster/{id}` | `code`, Rule `1107` | `NEG-SHF-03` | Immutability | Medium | Covered |
| `REQ-SCHED-12` | Lock shift from edit once scheduled on or before today | `PATCH /workplans/roster/{id}` | Rule `1905` | `NEG-SHF-04`, Rule 5 Suite | Business Rule | Critical | Covered |
| `REQ-SCHED-13` | Preflight employee conflict check before enrollment | `POST .../check-conflicts` | `employeeIds`, `startDate` | `POS-MEM-01`, `TC-POST-03`, Decision Table 2 | Preflight | Critical | Covered |
| `REQ-SCHED-14` | Prevent enrollment of employee committed on another board | `PATCH .../employees` | Rule `1914` | `NEG-MEM-01` | Business Rule | Critical | Covered |
| `REQ-SCHED-15` | Support regular work plan adjustment on enrollment | `PATCH .../employees` | `adjustConflicts`, Rule `1409` | `POS-MEM-04`, `NEG-MEM-02`, `TC-PAT-02` | Integration | Critical | Covered |
| `REQ-SCHED-16` | Prevent new membership start date in the past | `PATCH .../employees` | `startDate` validation | `NEG-MEM-03` | Input Validation | High | Covered |
| `REQ-SCHED-17` | Require area assignment before scheduling on area boards | `POST .../schedule/assign` | Rule `1906` | `NEG-PLN-01`, Rule 6 Suite | Business Rule | Critical | Covered |
| `REQ-SCHED-18` | Assign shift slots across dates and employees | `POST .../schedule/assign` | `slots[]`, `workPlanId` | `POS-PLN-03`, `TC-POST-04` | Functional | Critical | Covered |
| `REQ-SCHED-19` | Assign scheduled Day Off rest days | `POST .../schedule/assign` | `dayOff = true` | `POS-PLN-04`, `TC-POST-05` | Functional | High | Covered |
| `REQ-SCHED-20` | Clone previous period assignments | `POST .../copy-previous` | `anchor` | `POS-PLN-05` | Functional | Medium | Covered |
| `REQ-SCHED-21` | Clear draft slots with date boundary protection | `POST .../clear` | `dates`, Rule `1913` | `POS-PLN-06`, `NEG-PLN-03` | Functional / Business | Medium | Covered |
| `REQ-SCHED-22` | Require 100% slot completion to publish period | `POST .../publish` | Rule `1907`, `1908` | `POS-PUB-01`, `NEG-PUB-01`, `NEG-PUB-02` | Business Rule | Critical | Covered |
| `REQ-SCHED-23` | Support empty roster publishing with explicit flag | `POST .../publish` | `allowEmpty = true` | `POS-PUB-02` | Business Rule | Medium | Covered |
| `REQ-SCHED-24` | Prevent publishing or unpublishing ended periods | `POST .../publish`, `unpublish` | Rule `1909` | `NEG-PUB-03` | Lifecycle | High | Covered |
| `REQ-SCHED-25` | Concurrency control via version token on publish | `POST .../publish` | `version`, Rule `1910` | `NEG-PUB-04`, `SEC-CON-01` | Concurrency | High | Covered |
| `REQ-SCHED-26` | Force override required to unpublish started period | `POST .../unpublish` | `force`, Rule `1911` | `POS-PUB-05`, `NEG-PUB-06`, `TC-POST-07` | Business Rule | Critical | Covered |
| `REQ-SCHED-27` | Real-time visibility to employees on publish | `GET /me/schedule` | Published vs Draft | Workflow 1, `ST-PER-02` | ESS Integration | Critical | Covered |
| `REQ-SCHED-28` | Flag modified published periods as Changes not published | `POST .../assign` | `changesNotPublished` | Workflow 2, `ST-PER-03`, `POS-PUB-03` | Lifecycle | Critical | Covered |
| `REQ-SCHED-29` | Restrict query date windows to 31 days | `GET overview/*`, `schedules` | Rule `2204` | `NEG-OVR-01`, `NEG-OVR-02`, `BVA-RNG-04` | Input Validation | Medium | Covered |
| `REQ-SCHED-30` | Return 404 for member schedule never on a board | `GET schedules/employees/{id}` | Rule `2207` | `NEG-SCH-01` | Error Handling | Low | Covered |

---

## 20. Requirement Coverage Analysis & Metrics

### 20.1 Coverage Dashboard
- **Total Functional Requirements Identified:** 30
- **Requirements Covered by Test Suite:** 30
- **Requirement Coverage Percentage:** $$\\frac{30}{30} \\times 100 = 100.0\\%$$
- **Total Test Scenarios Formulated:**
  - Positive Test Cases: 31
  - Negative Test Cases: 36
  - Equivalence Partitioning Cases: 12
  - Boundary Value Analysis Cases: 13
  - Decision Table Combinations: 10
  - State Transition Scenarios: 9
  - Dedicated POST Scenarios: 7
  - Dedicated PATCH Scenarios: 5
  - Dedicated GET Verification Scenarios: 10
  - Cross-Module Regression Scenarios: 6
  - Security & Isolation Scenarios: 8
  - **Total Test Suite Executable Items:** **147 Scenarios**

### 20.2 Priority Distribution
- **Critical Priority (P1):** 62 Scenarios (42.2%) — Board/Shift creation, Conflict resolution, Slot assignment, Publishing, Immutability.
- **High Priority (P2):** 54 Scenarios (36.7%) — State transitions, Location scoping, Unpublishing override, Concurrency, Quotas.
- **Medium Priority (P3):** 24 Scenarios (16.3%) — Pagination, Area renaming, Copy-previous, Search filters.
- **Low Priority (P4):** 7 Scenarios (4.8%) — Multilingual Arabic labels, Legend display, 404 messaging.

---

## 21. Developer Clarification & Architectural Gap List

The following 10 UI inconsistencies and 6 Backend architectural quirks were discovered from the technical specification and live microservice inspection. They are cataloged for engineering review:

### A. Backend Architecture & Validation Quirks
1. **API Missing Date Range Check on `POST /schedule/assign`:** The API allows scheduling shifts on past dates, public holidays, and completed periods without validation error. However, `POST /publish` subsequently requires past days to be filled (Rule 1907). *Recommendation: Enforce past-date guard on Assign unless retroactive backfill permission is granted.*
2. **Publish is a Status Flag, Not an Immutable Snapshot:** Changes made to a published period are immediately visible to employees in Self-Service (`/me/schedule`). The system merely sets `changesNotPublished = true`. *Recommendation: Introduce formal versioned snapshotting so employees see the last published baseline until republishing.*
3. **Leave Module Integration Void:** Leave records are currently not integrated into the Scheduler. Cells never display "On Leave", leave counts in Overview return `null`, and Excel exports report `0`. Furthermore, leave does not protect a slot from being overwritten by `POST /clear`. *Recommendation: Integrate with LeaveSvc to block shift assignments over approved leaves.*
4. **20-Template Limit Leakage on Policy Error:** If roster shift creation fails due to a policy error (e.g. inactive policy), the underlying template has already been created in `ERP.Attendance.WorkTemplates`, consuming one slot of the 20-template limit and locking the short code. *Recommendation: Wrap WorkPlan and WorkTemplate creation in a MongoDB multi-document transaction.*
5. **Area Deletion Trap (Rule 1906 Cascade):** Deleting all areas from an area-enabled board leaves the board with `hasAreas: true` but zero areas. Consequently, every future `assign` and `copy-previous` call fails with `Cit.Attendance:1906`. *Recommendation: Automatically toggle `hasAreas = false` when the last area is deleted.*
6. **Timezone Discrepancy (UTC vs. Riyadh Time):** Planner, Publish, and Export calculate "today" using UTC date, whereas Overview and Schedules evaluate "today" using Asia/Riyadh (UTC+3). This causes shifts between 00:00 and 03:00 to appear on different dates across tabs.

### B. UI / Frontend Inconsistencies (`ZW.Manage-UI`)
1. **Add/Edit Shift Button State Trap:** Choosing the shift color swatch last leaves the "Add" button disabled until another form input is focused.
2. **Planner Context Loss:** Refreshing the browser, navigating back from Shift Details, or clicking "Open board" from a member schedule resets the planner grid to the current period, losing the selected anchor.
3. **Schedules Pagination Desynchronization:** Changing weeks on the Schedules tab does not reset the page number to 1, frequently resulting in an empty page.
4. **Upcoming Employees List Hardcoded Cap:** The Upcoming Members flyout displays only the first 50 members without pagination controls.
5. **Add Employees Location Fallback Failure:** If a board is absent from the client-side cache, the employee picker lists employees from all company locations; subsequent submission fails with `Cit.Attendance:9002`.

---

## 22. Final Senior QA Execution Checklist & Sign-Off Gate

| Gate # | Verification Milestone | Mandatory Verification Criteria | Sign-Off Status |
|---|---|---|---|
| **Gate 1** | Foundation & Prerequisites | Locations, Active Employees, Policies, and Holiday Calendars exist. Max 20 templates not exceeded. | `[ ] PENDING` |
| **Gate 2** | Board Lifecycle Verification | Board created, edited, frequency locked. Negative checks (1901, 1902, 1903, 1904) verified. | `[ ] PENDING` |
| **Gate 3** | Roster Shift Immutability | Roster Shift created with underlying template. Editing blocked once scheduled on/before today (1905). | `[ ] PENDING` |
| **Gate 4** | Conflict Preflight Engine | Preflight engine correctly identifies `BLOCKED`, `ADJUSTABLE`, and `AVAILABLE` candidates. | `[ ] PENDING` |
| **Gate 5** | Regular Plan Conflict Adjustment | Confirming `adjustConflicts: true` correctly truncates/splits regular plans without orphan headers. | `[ ] PENDING` |
| **Gate 6** | Planner Grid & Area Enforcement | Area assignment enforced before scheduling (1906). Day Off rest days correctly persisted. | `[ ] PENDING` |
| **Gate 7** | Publishing State Engine | 100% fill enforced (1907). Concurrency version enforced (1910). Force unpublish verified (1911). | `[ ] PENDING` |
| **Gate 8** | Database Consistency Audit | Direct MongoDB queries confirm data integrity across all 5 collections without schema leakage. | `[ ] PENDING` |
| **Gate 9** | ESS & Downstream Integration | Published roster days accurately displayed on `/me/schedule` and processed by Daily Attendance Engine. | `[ ] PENDING` |
| **Gate 10** | Security & Tenant Boundaries | Multi-company (9001) and multi-location (9002) isolation verified. Inactive employees rejected. | `[ ] PENDING` |
"""
