# Attendance 2: Services List

This document covers the Attendance 2 service: its functional modules, the services it calls and the
services that call it. It reflects `main` as deployed on DEV in `dev300-1.0.2` (23 Oct 2026).

## 1. The service

| | |
|---|---|
| Name | **Attendance 2** (Leave-facing attendance) |
| Repository | `SP.AttendanceSvc` |
| Docker image | `zwregistry.azurecr.io/attendancesvc2` |
| DEV release | `dev300-1.0.2`, built from `main` |
| DEV base URL | `https://attendance2.dev.zoolwork.com` |
| Swagger UI | `https://attendance2.dev.zoolwork.com/swagger` |
| Database | MongoDB, database `Sahab` (see [Database-Collections.md](Database-Collections.md)) |
| Runtime | .NET 9, ASP.NET Core |

**Attendance 2 is not Attendance 1.** Attendance 1 is the payroll-facing service (`ZW.AttendanceSvc`,
image `attendancesvc`). The two have separate code, collections and URLs. Make sure a defect is
logged against the right one.

### Calling the APIs

- Every route except the Leave integration starts with `/api/companies/{companyId}/…`.
- Most location-scoped calls also need a `locationId` query parameter.
- Send a JWT as `Authorization: Bearer <token>`. In Swagger, use the **Authorize** button and paste
  the token without the `Bearer ` prefix. The tenant is read from the token, and data from other
  tenants is never returned.
- Enum values go in and come out as names. See [Enum-List.md](Enum-List.md).
- A business rule failure returns an error body with a code of the form `Cit.Attendance:<number>`
  and a readable message.

---

## 2. Functional modules

Each module is one group in Swagger. Endpoint counts are for this release.

| # | Module (Swagger group) | Base route | Endpoints | What it covers |
|---|---|---|---|---|
| 1 | Work Templates | `/api/companies/{companyId}/worktemplates` | 20 | Fixed, Flexi, Split, Roster and Rotation templates; company default versioning and sync to locations; short codes; archive, restore, delete |
| 2 | Work Plans | `/api/companies/{companyId}/workplans` | 9 | Regular work plans, the location default plan, roster shifts (template and plan together), plan employees |
| 3 | Work Assignments | `/api/companies/{companyId}/workassignments` | 13 | Assigning employees to regular plans, conflict checks and adjustments, effective period edits, removal, moving employees between plans, current plan lookup |
| 4 | Attendance Policies | `/api/companies/{companyId}/attpolicies` | 9 | Break, grace period and overtime policies |
| 5 | Holiday Calendars | `/api/companies/{companyId}/holidaylist` | 7 | Company and location holiday calendars per year, publishing to locations, customising a location |
| 6 | Employee Exceptions | `/api/companies/{companyId}/config/attendance/employee-exemp` | 5 | Employees exempted from attendance tracking for a period |
| 7 | Roster Boards | `/api/companies/{companyId}/roster-boards` | 16 | Boards, board membership and periods, areas, moving employees, board edit and delete |
| 8 | Roster Schedule (Planner) | `/api/companies/{companyId}/roster-boards/{boardId}/schedule` and `/schedule-plans` | 8 | Planner landing page, schedule grid, assigning shifts and days off, publish and unpublish per period, clear, copy previous period, Excel export |
| 9 | Shift Rotations | `/api/companies/{companyId}/shift-rotations` | 17 | Rotations with teams and patterns, preview, enrolment, schedule generation, member edits and moves |
| 10 | Attendance Log: Upload, Import & Process | `/api/companies/{companyId}/att-log` | 7 | Uploading the monthly L3 CSV, importing it, processing, re-processing, publishing |
| 11 | Attendance Log: Sessions & Files | `/api/companies/{companyId}/att-log` | 14 | Session cards and detail, progress polling, uploaded files, session grid, employee monthly detail, session delete |
| 12 | Attendance Log: Issues & Errors | `/api/companies/{companyId}/att-log` | 7 | Blockers, issue summary and list, error logs, issue export, resolving errors |
| 13 | Attendance Log: Daily Records (L3) | `/api/companies/{companyId}/att-log` | 13 | Reading daily records, edits (edit, regularize, mark day off or holiday, overrides, clear), settle and unsettle |
| 14 | Attendance Log: Monthly Summaries (L4 / L5) | `/api/companies/{companyId}/att-log` | 6 | Monthly summaries (L4) and their Excel export; legacy L5 payroll summaries |
| 15 | Attendance Log: Configuration & Process State | `/api/companies/{companyId}/att-log` | 7 | Company attendance-log config, default work pattern, per-employee processing state |
| 16 | Self Service: My Attendance | `/api/companies/{companyId}/me` | 7 | The signed-in employee's periods, schedule, assignment, holidays, policy, attendance summary and days |
| 17 | Self Service: My Team | `/api/companies/{companyId}/team` | 8 | A manager's reportees: attendance summary, per-employee attendance, schedule, work plans, Excel reports |
| 18 | Leave Service Integration | `/api/attendance/v1/companies/{companyId}/employees/{employeeId}/calendar` | 1 | Day classification (workday, weekend, holiday) for the Leave service |
| | **Total** | | **174** | |

---

## 3. Services Attendance 2 calls

| Service | DEV URL | Used for | Called from |
|---|---|---|---|
| **Company service** | `https://company8.dev.zoolwork.com` | Company details and names (`/api/company/companies`), the company's work locations (`/api/company/worklocations/companyWorkLocationList`), holiday types (`/api/company/{companyId}/holidaytypes`) | Work templates and plans (company and location names), location default set-up, holiday calendars, schedule plans, day classification |
| **Org Hierarchy service** | `https://orghierarchyservice-api.dev.zoolwork.com` | Employee details by id (`/api/companies/{companyId}/employees/{id}`) | Adding employees to work assignments, roster boards and rotations; assigning and copying roster shifts; rotation schedule generation |
| **Employee service** | `https://employee8.dev.zoolwork.com` | The signed-in manager's reporting team (`/api/Employees/companies/{companyId}/employeesBasicList?HierarchyFilter=ReportingManager`) | All `/team` APIs |
| **Identity server** | `https://auth8.dev.zoolwork.com` | Issues the JWT, audience `AttendanceService` | Every authenticated request |
| **MongoDB** | `10.1.0.4:27018`, database `Sahab` | All Attendance 2 data | Everything |
| **HR / Employee enrolment data** | Collection `EmployeeEnrollments` in the same database | Employee identity, pay group, department, designation, reporting line, joining date | Attendance log import and processing, self-service APIs. Read-only |

Calls to the Company, Org Hierarchy and Employee services forward the caller's token. If one of them
is down or returns an error, the Attendance 2 feature that needs it fails or shows missing names;
check the dependency before logging the defect against Attendance 2.

---

## 4. Services that call Attendance 2

| Consumer | APIs used |
|---|---|
| Attendance web app (Sahab front end) | All modules in section 2 except the Leave integration |
| Leave service | `GET …/calendar/day-classification`, to count leave days against working days and holidays |
| Employee self-service and AI Hub | `/me/*` and `/team/*` |

---

## 5. Not connected in this release

Please don't log these as defects. They are known gaps:

| Item | Effect you will see |
|---|---|
| Leave data is not fed into the roster planner | Grid cells never show `OnLeave`, and leave counts in the planner and the roster export are 0 |
| No message queue | Attendance 2 does not publish or consume events in this build. All integration is over HTTP or through the shared database |
| L1 and L2 uploads | Only L3 (daily processed) CSV files can be uploaded |
| L5 payroll summary | Still reachable through the API, but reporting stops at L4 |
| Roster schedule PDF export | Only Excel export is available |

---

## 6. DEV environment notes for testers

- DEV Attendance 2 does **not** validate token signatures (`Authentication:ValidateToken = false` on
  DEV only). Tests about expired or forged tokens are not meaningful on DEV; run them on Staging.
- The service runs with its configuration baked into the image, so DEV, Staging and COMM-IT each run
  their own build. A fix verified on DEV reaches Staging only after it has been ported and deployed
  there.
- The DEV database was migrated to the new roster publish-period data shape on 22 Oct 2026. Some
  template short codes were re-coded by that migration, so codes on older templates may differ from
  what you remember.
