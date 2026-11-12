# Shifts & Rotation Planner – Functional Overview

This page explains the **Shifts & Rotation** screen (Attendance → Shifts & Rotation): how a work plan is set up, how employees are assigned to it, how a shift rotation works, and how both feed the same per-employee schedule. Each section gives the user steps on screen, the business rules and the APIs behind them. It was written from the backend (SP.AttendanceSvc, `main`) and the frontend (ZW.Manage-UI, `zw-attendance`) as of . For the full Attendance flow see [Attendance Module – Functional Overview](https://zoolworks.atlassian.net/wiki/spaces/AM/pages/1542356994/Attendance+Module+Functional+Overview).

Table Of Contents

## 1. Module at a glance

The Shifts & Rotation screen answers one question: **which shift does each employee work on each date?** It has three top tabs.

| Tab | What the user does there | Main APIs |
| --- | --- | --- |
| **Overview** | Read-only dashboard: counts of plans, rotations, assigned employees and templates; coverage per location; plans that need attention. | `workplans`, `shift-rotations`, `worktemplates`, `workassignments/overview/*` |
| **Planner → Regular** | Create and maintain regular work plans per location, and assign employees to them for a period. | `workplans`, `workassignments` |
| **Planner → Rotation** | Create shift rotations (2–4 plans that teams cycle through), and enrol employees into a team. | `shift-rotations` |
| **Templates** | Create the weekly shift patterns (Regular: Fixed / Flexi / Split; Rotation) that plans are built from. | `worktemplates` |

The **Roster** (day-by-day planning on a board) is a separate menu, *Scheduler*. It is not part of this page, but it takes part in conflict checks and moves (see section 7).

### 1.1 Terms used on this page

| Term | Meaning | Collection |
| --- | --- | --- |
| Work Template | Weekly time pattern: one row per weekday with working day / day off, times and duration. | `ERP.Attendance.WorkTemplates` |
| Policy | Break, Overtime or Grace Period rule, set at company level. | `ERP.Attendance.Policies` |
| Work Plan | One template + optional policies, for one location. Employees are assigned to a plan, never to a template. Types: Regular (1), Roster (2), Rotation (3). | `ERP.Attendance.WorkPlans` |
| Work Assignment (header) | One "assign" action on a regular plan: plan, location, start and end date. Holds no employee list. | `ERP.Attendance.WorkAssignments` |
| Work Assignment Map (detail) | The per-employee row: employee × plan × period, with a copy of the plan. This is the record every other part of Attendance reads. The UI calls it the "assignment detail". | `ERP.Attendance.WorkAssignmentMaps` |
| Shift Rotation | Header that owns 2–4 rotation plans (P1–P4), a cycle pattern, teams and members. | `ERP.Attendance.ShiftRotationBoard` |
| Team / Step / Cycle | A step is one block of weeks on one plan; the steps in order form a cycle; each team runs the same cycle starting at a different step. | inside the rotation |
| Enrolment (membership) | An employee's period on one team of a rotation. | inside the rotation |

## 2. End-to-end flow

```text
TEMPLATES tab                 PLANNER → REGULAR                                  RESULT (per employee, per date)
─────────────                 ─────────────────                                  ───────────────────────────────
Regular template ───────────► Work Plan (location, template copy, policies)
 (Fixed / Flexi / Split)          │
Policies (Configuration) ────►    ▼
                              Assign Employee ─► check-conflicts ─► create ─► (adjust) ─► Regular Work Assignment Map
                                                                                         (employee × period)          ┐
                              PLANNER → ROTATION                                                                       │
                              ──────────────────                                                                       ├─► "Which shift does
Rotation template ──────────► Shift Rotation (2–4 plans, pattern, teams)                                               │    employee X work on D?"
 (type 5, 7 days)                 │                                                                                    │    = active map covering D
                                  ▼                                                                                    │      with the latest start
                              Add Employees (team) ─► check-conflicts ─► enrol ─► Rotation Work Assignment Maps        │
                                                                                 (one per step window, 104 weeks)      ┘
SCHEDULER (separate menu)     Roster board ─► daily schedule ─────────────────► Roster Work Assignment Maps (one per day)
```

**Key principle: copies, not links.** A plan stores a copy of its template and policies, and every assignment map stores a copy of the plan. Changing a master record later does not change existing copies unless the system refreshes them on purpose (see 4.4).

## 3. Before you start (prerequisites)

1. **Work locations** exist in the Company / Employee Hierarchy service. Every plan, rotation and assignment belongs to exactly one location.
2. **Policies** (Break, Overtime, Grace Period) are created under Configuration if a plan needs them. Only active policies are offered.
3. **Templates** are created on the Templates tab:
    - *Regular shift* (Fixed, Flexible or Split) for regular plans. One create screen can save the same template to several locations; one API call is made per location.
    - *Rotation shift* (type 5) for rotation plans: Fixed-shaped, all 7 days Sun–Sat present, at least one working day, location level only, never a default, short code of 7 letters/digits.
4. **Employees** are active in the Employee service with a work location. The employee picker only lists employees of the chosen location.

Once a plan uses a template, the template can no longer be edited (1206). It can only be archived.

## 4. Regular work plan

### 4.1 Functional steps

| Action | Steps on screen | API |
| --- | --- | --- |
| **View plans** | Planner → Regular. Plans are grouped by location ("N plans · M employees"). Each card shows name, *Default* tag, working days, timing, policies, active employees, and a strip "N employees join from …" when there are upcoming employees. | `GET workplans?type=regular` |
| **Create plan** | 1. Create New ▾ → Regular Work Plan. 2. Enter Plan Name (EN required, AR optional) and choose Location. 3. Choose Shift Template (enabled after location; only that location's templates). "View calendar" shows the week. 4. Optionally switch on Break / Overtime / Grace Period and pick one policy for each switched-on toggle. 5. *Create Plan* (back to list) or *Create & Add Employees* (opens Add Employees with this plan pre-selected). | `GET worktemplates?templateType=regular` `GET attpolicies?state=active&type=…` (×3) `POST workplans?locationId=` |
| **View plan details** | Click a card. Tabs: Employees, Policy, Template Details. Each employee row has ⋮ Edit Effective Period and Move Employee. | `GET workplans/{id}` `GET workassignments/details?locationId=` |
| **Upcoming employees** | Card → "View upcoming employees". Lists employees whose start date is after today. Same row actions. | `GET workplans/{id}/employees?segment=upcoming` |
| **Edit plan** | ⋮ → Edit Work Plan opens a side panel. Name and policies can be changed. Location and template are read-only in the UI. | `PATCH workplans/{id}?locationId=` |
| **Set as default** | ⋮ → Set as Default (hidden on the current default). The previous default at the location loses the tag. | `PATCH workplans/{id}/default?locationId=` |
| **Delete plan** | ⋮ → Delete Work Plan (hidden on the default plan) → confirm. Soft delete. | `PATCH workplans/{id}/delete?locationId=` |

### 4.2 Business rules

- A location can have at most **10 work plans** (1302). The count currently includes deleted, roster and rotation plans.
- The plan stores a **copy** of the template and of each chosen policy. Creating the plan marks the template as in use.
- `description` is required by the API (min 10 characters). The screen generates it automatically, so the user never types it.
- A plan is created as **default** automatically when its template is the default template. Otherwise the user sets it with Set as Default. The default plan is shown as the "Default" category on the Overview; being default does not assign anyone automatically.
- A plan **cannot be deleted while in use** (1304): it has ever had a work assignment header, or it has any active employee row.
- Roster plans are edited from the Scheduler (`workplans/roster/…`) and rotation plans only through their rotation; the regular endpoints refuse them (1104).

### 4.3 APIs – Work Plan

Base path: `/api/companies/{companyId}/workplans`. Company comes from the route, location from the `locationId` query; request bodies carry no tenant, company or location IDs.

| Method and path | Purpose and usage |
| --- | --- |
| `GET /workplans?locationId=&state=&type=` | Lists plans with `numberOfEmployees`, `activeEmployeeCount`, `upcomingEmployeeCount`, `nextJoinDate`. `type` = regular \| roster \| rotation (default **regular**). `state` = active \| deleted (omitted = both). Invalid value → 1104. |
| `GET /workplans/{id}` | One plan with its template copy and policies. 1301 not found, 9001 other company. |
| `GET /workplans/{id}/employees` | Employees of a **regular** plan. Query: `segment` (upcoming \| active \| past \| all), `asOf` (default today), `search` (name/code), `department`, `designation`, `page`, `pageSize` (default 50, max 500). Each row also shows the employee's current plan. Non-regular plan → 1104. |
| `POST /workplans?locationId=` | Creates a regular plan. Body: `workPlanName{en,ar}`, `description`, `workTemplateId`, `isBreakPolicyEnabled`, `isOvertimePolicyEnabled`, `isGracePeriodPolicyEnabled`, `policyIds[]`, `tenantName`. Errors: validation 400, 1101 template, 1501 policy, 1302 limit. |
| `PATCH /workplans/{id}?locationId=` | Partial edit: any of name, description, policy flags, `policyIds`, `workTemplateId`. Response says whether existing assignments were updated (`propagatedToWorkAssignments`, `affectedWorkAssignmentCount`). Errors: 1301, 9001, 9002, 1104 (roster/rotation plan), 1101, 1501. |
| `PATCH /workplans/{id}/delete?locationId=` | Soft-deletes the plan and releases its template if nothing else uses it. 1304 if in use; 1104 for a rotation plan. |
| `PATCH /workplans/{id}/default?locationId=` | Makes this plan the location default and clears the previous default. 404 if not found, 9001, 9002. |
| `POST /workplans/roster`, `PATCH /workplans/roster/{id}` | Roster shift create/edit, used by the Scheduler only (listed here for completeness). |

```js
POST /api/companies/{companyId}/workplans?locationId={locationId}
{
  "tenantName": "Demo Tenant",
  "workPlanName": { "en": "General Shift", "ar": "" },
  "description": "Work plan based on standard schedule with grace period policies",
  "workTemplateId": "4444…",
  "isBreakPolicyEnabled": false,
  "isOvertimePolicyEnabled": false,
  "isGracePeriodPolicyEnabled": true,
  "policyIds": [ "3333…" ]
}
```

### 4.4 What happens to existing assignments when a plan is edited

| Change on the plan | Effect on employees already assigned |
| --- | --- |
| Name | Copied to every employee row (map). |
| Policies (non-empty `policyIds`) | Copied to every employee row. An empty list is ignored, so policies cannot be cleared through the API. |
| Policy on/off flags | Saved on the plan only; employee rows have no flags. |
| Template (API only; the UI locks it) | Saved on the plan; existing employee rows **keep the old template copy**. |

## 5. Work assignment (assign employees to a regular plan)

### 5.1 Functional steps – Add / Assign Employees

Entry points: **Assign Employee** (header button, nothing pre-selected), **Add Employees** on a plan card or the plan details page (location and plan pre-selected), or *Create & Add Employees* after creating a plan.

1. Choose **Location**, then **Work Plan** (skipped when pre-selected).
2. Set **Effective From** (default today, cannot be in the past) and, optionally, **Effective To** ("Add end date"). Leaving it empty means open-ended.
3. Select employees in the picker (location's active employees; search and department filter). The *Current Plan* column shows what each employee is on today; clicking it shows that plan.
4. On every selection or date change the screen runs a **conflict check** (preview only, nothing saved) and shows:
    - BLOCKED red banner – the employee is on a roster board or a rotation in that period. The user must *Skip Employees*; Add stays disabled while a blocked employee is selected.
    - ADJUSTABLE amber banner – the employee is on another regular plan in that period. The user chooses *Adjust Plan* (review how the old plan will be cut and confirm) or *Skip Employees*.
    - CLEAN no banner – nothing overlaps.
5. Click **Add**. The system creates the assignment for the clean employees. If the user confirmed adjustment, it then runs **adjust** for those employees, which cuts their old regular rows and assigns them.
6. A toast confirms the result and lists any skipped count.

### 5.2 Conflict categories and how "adjust" resolves them

| What overlaps | Category | Result |
| --- | --- | --- |
| Nothing | Allowed | Assigned on create. |
| Another regular plan at the same location | Adjustable | Not assigned on create; assigned by adjust after the old row is cut. |
| Roster board membership / roster day, rotation enrolment / rotation step | Blocked | Never adjusted automatically. Adjust refuses the whole request with 1408. Remove the employee from the board/rotation first, or use Move. |

How an overlapping old regular row is cut:

| Resolution | When | Old row becomes |
| --- | --- | --- |
| Ends early | Old row starts before the new period and does not run past it | Ends the day before the new start |
| Ends early and resumes (split) | Old row starts before a new period that has an end date and runs past that end | Ends the day before; a new row resumes the day after the new end, up to the old end |
| Starts later | Old row starts inside a closed new period and runs past it | Starts the day after the new end |
| Removed | Old row lies fully inside the new period | `IsActive=false` (kept for audit) |

Example: Employee A is on *General Shift* from 2026-10-01, open-ended. A new assignment to *Night Shift* is made for 2026-12-01 to 2026-12-31 with adjust. Result: General Shift 2026-10-01 → 2026-11-30, Night Shift 2026-12-01 → 2026-12-31, General Shift again from 2027-01-01, open-ended.

### 5.3 Functional steps – maintaining an employee's assignment

| Action | Steps and rules | API |
| --- | --- | --- |
| **Edit Effective Period** | Plan details or Upcoming employees → row ⋮ → Edit Effective Period. If the row has **already started**, the start date is locked and the end cannot be before today. If it has **not started**, the start must be today or later. End ≥ start. The screen first runs a conflict check that ignores this row; blocked → cannot save; adjustable → the user reviews the conflicted employees page and confirms; clean → saved directly. | `POST workassignments/check-conflicts?skipAssignmentId={detailId}&enforceFutureStart=false` `PATCH workassignments/details/{detailId}/effective-period` |
| **Move Employee** | Row ⋮ → Move Employee. Choose the target: another **regular plan**, a **roster board** or a **rotation + team**, all at the same location. Effective From defaults to and cannot be earlier than **tomorrow**; End is optional (defaults to the current row's end). The panel runs a preflight; blocked → cannot move; regular overlap → button becomes "Adjust & Move". On move, the current row ends the day before Effective From (or is deactivated if it had not started), then the employee joins the target. | `POST workassignments/details/{detailId}/move/check-conflicts` `PATCH workassignments/details/{detailId}/move` |
| **Remove employee** | **No UI action today.** The API exists: it deactivates the whole row (no end date is set, history included). | `PATCH workassignments/details/{detailId}/remove` |

### 5.4 Business rules

- An employee can have only **one active regular row per date at a location**. Conflicts are checked only against the same location.
- Create: start date today or later (1405); end date strictly after start; `workPlanName.en` must match the plan's name (1305).
- An open end date is stored as `9999-12-31` and returned as `null`. "Today" is the UTC date.
- Create always writes the assignment header, even when every selected employee conflicts. Employee rows are written only for clean employees.
- Each employee row stores a copy of the plan (name, template, policies) and the location's holiday calendar for the start year.
- Upcoming = row start after today; Past = row end before today; Active = otherwise. Deactivated rows are never counted.

### 5.5 APIs – Work Assignment

Base path: `/api/companies/{companyId}/workassignments`.

| Method and path | Purpose and usage |
| --- | --- |
| `POST /check-conflicts?locationId=` | **Preview, writes nothing.** Body: `employeeIds[]`, `startDate`, `endDate?`. Optional query: `skipAssignmentId` (ignore rows being edited), `enforceFutureStart=false` (allow a past start). Returns `allowedEmployeeIds`, `conflictedEmployeeIds`, `adjustableEmployeeIds`, `blockedEmployeeIds`, `canProceed` and `conflictDetails[]` (source Regular/Roster/Rotation, dates, plan name, `isAdjustable`, proposed `resolution`). |
| `POST /?locationId=` | Creates the assignment. Body: `workPlanId`, `workPlanName`, `employeeIds[]`, `startDate`, `endDate?`, `tenantName`. Returns the new header id plus `conflictedEmployeeIds` and `conflictDetails` for the employees not yet assigned. Errors: 1407, 1405, 1301, 1305. |
| `POST /adjust?locationId=` | Second step of create for adjustable employees. Body: create body + `workAssignmentId`. Uses the header's dates and plan, cuts overlapping regular rows (5.2) and adds the employees. 1408 if any employee is blocked (whole request refused). Returns `adjustedEmployeeIds`, `skippedEmployeeIds`. |
| `PATCH /details/{id}/effective-period?locationId=` | Changes one row's dates. Body: `startDate`, `endDate?`, `adjustConflicts`. With `adjustConflicts=false` and a conflict → 200 with `hasConflicts:true`, nothing saved. With `true` → regular overlaps are cut; 1408 if blocked. |
| `POST /details/{id}/move/check-conflicts?locationId=` | Move preflight. Body: `targetType` (1 Board, 2 WorkPlan, 3 Rotation), `targetBoardId` \| `targetWorkPlanId` \| `targetRotationId` + `targetTeamId`, `effectiveFrom?`, `endDate?`. Returns `hasConflicts`, `heldByBoardOrRotation`, `requiresAdjustment`, `canProceed`, `reason`. |
| `PATCH /details/{id}/move?locationId=` | Executes the move (same body + `adjustConflicts`). Errors: 1408 held by board/rotation, 1409 adjustment not confirmed, 1104 invalid target or dates. Returns `sourceRemoved`, `createdWorkAssignmentId`, `targetMembershipId`, `republishBoardIds`. |
| `PATCH /details/{id}/remove?locationId=` | Deactivates one employee row. No UI today. |
| `GET /details?locationId=&state=` | Regular employee rows for a location (`state` = active \| inactive). Used by the plan details page. |
| `GET /details/{id}` | One employee row. 1401 if not found. |
| `GET /current-plans?locationId=&asOf=&employeeIds=` | What each employee is on at a date: regular plan, roster board or rotation. Feeds the "Current Plan" column in every employee picker. |
| `GET /?locationId=`, `GET /{id}`, `GET /upcoming?locationId=` | Assignment headers: all, one, or those starting after today with at least one active employee. |

```js
// 1. preview
POST /api/companies/{companyId}/workassignments/check-conflicts?locationId={locationId}
{ "employeeIds": ["e1…", "e2…"], "startDate": "2026-12-01", "endDate": "2026-12-31" }
// → adjustableEmployeeIds: ["e2…"], blockedEmployeeIds: [], canProceed: true

// 2. create (assigns e1 only, returns e2 as conflicted)
POST /api/companies/{companyId}/workassignments?locationId={locationId}
{ "tenantName": "Demo Tenant", "workPlanId": "1111…", "workPlanName": { "en": "Night Shift" },
  "employeeIds": ["e1…", "e2…"], "startDate": "2026-12-01", "endDate": "2026-12-31" }

// 3. adjust (cuts e2's old regular row and assigns e2)
POST /api/companies/{companyId}/workassignments/adjust?locationId={locationId}
{ "workAssignmentId": "a1a1…", "workPlanId": "1111…", "workPlanName": { "en": "Night Shift" },
  "employeeIds": ["e2…"], "startDate": "2026-12-01", "endDate": "2026-12-31" }
```

## 6. Shift rotation

A rotation belongs to one location. It moves teams through **2 to 4 rotation plans** (P1–P4) in a fixed cycle. Each employee's cycle starts on their own enrolment date; the rotation itself has no start date.

### 6.1 Limits

| Item | Allowed | Error |
| --- | --- | --- |
| Plans per rotation | 2–4 | 2003 |
| Steps in one cycle | 2–8 | 2006 |
| Weeks per step | 1–13 | 2005 |
| Cycle length (sum of steps) | 2–52 weeks | 2007 |
| Teams | Exactly one per step | 2008 |
| Employees per enrol request | 1–200 | 2014 |
| Schedule generated ahead | 104 weeks | – |

**Pattern types.** *Alternating*: the system builds P1 → P2 → … → Pn, each step = weeks per step. *Uneven*: the user gives the exact step sequence (a plan may repeat, e.g. P1 → P1 → P2). Every plan must appear at least once. Two teams may not end up with the same pattern (2009).

### 6.2 Functional steps – create a rotation

1. Create Rotation shift templates (Templates tab → Shift ▾ → Rotation Shift), e.g. Day, Evening, Night. They can also be created from inside the wizard ("Add shift").
2. Planner → Create New ▾ → **Rotation Work Plan**.
3. **Step 1 · Plan Setup**: rotation name (EN required), location, and 2–4 plans. Each plan needs a name and a rotation template (each template can be used once per rotation) and can have Break / Overtime / Grace Period policies.
4. **Step 2 · Rotation Pattern**: pattern (Alternating or Uneven), weeks per shift, and the teams (one per step; each with a name and a unique start position).
5. The screen shows a **preview grid** (which plan each team works each week). Create is enabled only after a preview has loaded.
6. **Create**: the system saves the rotation header, one rotation work plan (PlanType 3) per slot, and the teams. No employees and no schedule yet.

### 6.3 Functional steps – employees in a rotation

| Action | Steps and rules | API |
| --- | --- | --- |
| **Add employees** | Rotation card or details → Add Employees ▾ → pick a team. Pick employees (location only, max 200), join date (today or later) and optional end date (at least one full cycle). Conflict check runs on every change: blocked (on a roster board or another rotation, 2016), already a member (2026), adjustable (regular plan in the way). If anyone is adjustable, the adjust panel opens first. On save, overlapping regular rows are cut (same rules as 5.2), the members are added and their step schedule is generated. | `POST shift-rotations/{rid}/teams/{teamId}/employees/check-conflicts` `POST shift-rotations/{rid}/teams/{teamId}/employees` |
| **View employees** | Rotation details → Employees tab, filter by team, search, department, designation. Each row shows the current step. Past members are hidden by the screen. | `GET shift-rotations/{rid}/employees` |
| **Edit enrolment period** | Row ⋮ → Edit Enrolment Period. Start locked once started; end at least one cycle after start and not before today. Conflict check excludes this enrolment. Steps are regenerated from the changed date. | `PATCH shift-rotations/{rid}/members/{membershipId}` |
| **Move employee** | Row ⋮ → Move Employee to a regular plan, a roster board or a different rotation (same location, from tomorrow by default). The enrolment ends the day before Effective From (or is deleted if not started), then the employee joins the target. | `POST …/members/{membershipId}/move/check-conflicts` `PATCH …/members/{membershipId}/move` |
| **Move to another team** | **API only, no UI.** Changes the team from a date; the cycle still counts from the original start date. | `POST …/members/{membershipId}/move-team` |
| **Remove employee** | **API only, no UI.** Upcoming member → deleted with all steps. Running member → `endDate` required, enrolment ends then. Past member → 2017. | `DELETE …/members/{membershipId}?endDate=` |
| **Edit rotation** | ⋮ → Edit. Allowed only when the rotation has **no current or upcoming members** (2018); the screen locks the whole form once anyone is enrolled. Plans can be added, changed or removed. | `PATCH shift-rotations/{rid}` |
| **Delete rotation** | ⋮ → Delete. Allowed only with no current or upcoming members (2018; the dialog lists them). Future steps are deactivated, plans soft-deleted, templates released; past member history is kept. | `DELETE shift-rotations/{rid}` |

### 6.4 How the schedule is generated

- Day 0 of an employee's cycle is their join date (any weekday). Their team decides which step comes first.
- The system writes **one rotation work assignment map per step window** (AssignmentType 3), up to the end of the step that contains today + 104 weeks, or the enrolment end if sooner. *Generate schedule* tops this up and is safe to run again.
- The daily hours come from that step's rotation template row for the weekday. A rotation day that falls on a holiday is not a working day.

Example: Team B has pattern P2 → P3 → P1, 2 weeks each. An employee joins on 2026-10-04: P2 from 10-04 to 10-17, P3 from 10-18 to 10-31, P1 from 11-01 to 11-14, then the cycle repeats.

### 6.5 APIs – Shift Rotation

Base path: `/api/companies/{companyId}/shift-rotations`.

| Method and path | Purpose and usage |
| --- | --- |
| `GET /?locationId=` | Rotation cards grouped by location with plan, team and employee counts. |
| `GET /{rid}` | One rotation: plans (with template and policies), pattern, teams. 2012 not found. |
| `POST /preview?locationId=&cycles=` | Builds the rotation in memory and returns the grid; saves nothing. Same body and rules as create, without the name check. |
| `POST /?locationId=` | Creates the rotation. Body: `rotationName`, `patternType` (1 Alternating, 2 Uneven), `weeksPerStep`, `plans[]` (`planIndex`, `workPlanName`, `workTemplateId`, policy flags, `policyIds`), `steps[]` (Uneven only), `teams[]` (`teamName`, `startSequenceOrder`). Errors: 2001–2009, 2025, template/policy not found. |
| `PATCH /{rid}?locationId=` | Edits the whole rotation. Plans carry `workPlanId` to keep, none to add; `removedPlanIds[]` to remove. Errors: 2018 has members, 2028/2029 plan list stale, plus the create rules. |
| `DELETE /{rid}?locationId=` | Soft-deletes the rotation. 2018 if it has current or upcoming members. |
| `GET /{rid}/rotation-grid?from=&to=&cycles=` | Which plan each team works per day, for a window. |
| `POST /{rid}/generate-schedule` | Tops up every member's step maps to the 104-week horizon. |
| `POST /{rid}/teams/{teamId}/employees/check-conflicts` | Enrol preview. Body: `employeeIds[]`, `startDate`, `endDate?`. Query `excludeMembershipId` when editing. Returns `cleanEmployeeIds`, `adjustableEmployeeIds`, `blockedEmployeeIds`, `alreadyMembers`, `conflicts[]`, `firstSteps`, `canProceed`. |
| `POST /{rid}/teams/{teamId}/employees` | Enrols employees (body + `adjustConflicts`). Errors: 2013, 2014, 2015 (past date), 2019 (shorter than one cycle; returns `earliestEndDate`), 2026, 2016, 1409. |
| `GET /{rid}/employees` | Members, paged. Query: `teamId`, `segment`, `asOf`, `search`, `department`, `designation`, `page`, `pageSize`. |
| `GET /{rid}/employees/{employeeId}/schedule?from=&to=` | One employee's generated steps (dates, plan, cycle number, team, partial flag). |
| `PATCH /{rid}/members/{membershipId}` | Edit enrolment period. Body: `startDate`, `endDate?`, `adjustConflicts`. |
| `POST /{rid}/members/{membershipId}/move-team` | Move to another team of the same rotation. Body: `teamId`, `effectiveFrom`. |
| `POST …/move/check-conflicts`, `PATCH …/move` | Move off this rotation to a board, regular plan or another rotation (same body as 5.5). |
| `DELETE /{rid}/members/{membershipId}?endDate=` | Remove or end an enrolment (rules in 6.3). |
| `POST /worktemplates/rotation?locationId=` `PATCH /worktemplates/rotation/{id}` | Create / edit a rotation template (errors 2030–2035; 1206 once used by a plan). |

```js
POST /api/companies/{companyId}/shift-rotations?locationId={locationId}
{
  "tenantName": "Demo Tenant",
  "rotationName": { "en": "Plant Ops 3-Shift" },
  "patternType": 1, "weeksPerStep": 2,
  "plans": [
    { "planIndex": 1, "workPlanName": { "en": "Day" },     "workTemplateId": "t-day…",   "isGracePeriodPolicyEnabled": true, "policyIds": ["g…"] },
    { "planIndex": 2, "workPlanName": { "en": "Evening" }, "workTemplateId": "t-eve…",   "policyIds": [] },
    { "planIndex": 3, "workPlanName": { "en": "Night" },   "workTemplateId": "t-night…", "policyIds": [] }
  ],
  "teams": [
    { "teamName": "Team A", "startSequenceOrder": 1 },
    { "teamName": "Team B", "startSequenceOrder": 2 },
    { "teamName": "Team C", "startSequenceOrder": 3 }
  ]
}
```

## 7. How Shift & Rotation integrates with the Planner

1. **One schedule store.** Regular assignments, rotation steps and roster days all end up as **Work Assignment Maps** in the same collection (AssignmentType 1 Regular, 2 Roster, 3 Rotation). Every reader (Overview, Schedules, ESS `me/*`, Leave day classification, attendance) reads that one store: for employee X on date D it takes the active map covering D with the latest start date.
2. **Templates feed plans.** Regular templates can only be used by regular plans; rotation templates (type 5) are the only templates a rotation plan accepts (2004). A used template is locked.
3. **Rotation plans are work plans.** Creating a rotation creates one work plan (PlanType 3) per slot. They are listed under the rotation, not on the Regular tab, and can be changed only through the rotation.
4. **Cross-checks between Regular, Rotation and Roster.**

| Employee joins… | …while already on |
| --- | --- |
| a regular plan | another regular plan → adjustable (old row cut on confirm). A rotation or roster board → blocked (1408). |
| a rotation team | a regular plan → adjustable (old row cut on confirm, 1409 without confirmation). A roster board or another rotation → blocked (2016). Already on this rotation → 2026. |
| a roster board (Scheduler) | a regular plan → adjustable. A rotation or another board → blocked. |
5. **Move is the bridge.** To take an employee from one kind of plan to another (regular ↔ rotation ↔ roster board), use Move Employee rather than removing and adding. It ends the old commitment the day before Effective From and joins the target in one action.
6. **Current Plan column.** Every employee picker calls `workassignments/current-plans`, so the user can see whether an employee is currently on a regular plan, a rotation or a roster board before selecting them.
7. **Default plan.** Employees on a location's default plan are shown as the "Default" category on the Overview and Schedules, separately from other regular plans.

## 8. Overview and Schedules APIs

The Overview tab currently builds its tiles from the list APIs (`workplans?type=regular`, `shift-rotations`, `worktemplates`). The dashboard APIs below are built and will back the new Overview and Schedules design. They cover regular and rotation only (roster has its own under `roster-boards/overview`). Common filters: `locationId`, `planType` (regular | rotation | default), `workPlanId`, `rotationId`, `departmentId`.

| Method and path | Purpose |
| --- | --- |
| `GET workassignments/overview/summary` | Today's headcount cards: regular / rotation / default, with percentages. |
| `GET workassignments/overview/today` | Today's timeline per plan (completed / in progress / pending), overnight carry-over, holidays. |
| `GET workassignments/overview/week?from=&to=` | Scheduled employees per day; default is the Sunday-start week, max 31 days. |
| `GET workassignments/overview/active-plans` | Regular plans with employees today, rotation positions and next switches. |
| `GET workassignments/overview/default-plan-employees?group=this-week\|earlier` | Employees on a default plan, newest first (page size default 5). |
| `GET holidaylist/upcoming?locationId=&from=&limit=` | Next holidays (default 4). |
| `GET workassignments/schedules?from=&to=` | Employee × day grid (max 31 days), ordered regular → default → rotation; search, paging (default 10). |
| `GET workassignments/schedules/employees/{employeeId}?from=&to=` | One employee's days, plan and policies. |

## 9. Error codes

All errors are returned as `Cit.Attendance:<code>`. A failed field validation returns 400 with code `Cit.Attendance:Validation` and a `validationErrors` list.

| Code | Meaning |
| --- | --- |
| 1101 | Work template not found or deleted |
| 1104 | Invalid state – generic; the message explains the case (wrong plan type, invalid filter, move date in the past, …) |
| 1206 | Template is used by a plan and cannot be edited |
| 1301 / 1302 | Work plan not found / location already has 10 plans |
| 1304 | Work plan in use, cannot be deleted |
| 1305 | Work plan name in the request does not match the plan |
| 1401 | Work assignment not found |
| 1405 | Start date is in the past (today is allowed) |
| 1407 | Location is required |
| 1408 | Employee is held by a roster board or rotation – cannot be adjusted |
| 1409 | A regular plan is in the way and the adjustment was not confirmed |
| 1501 | Policy not found |
| 9001 / 9002 | Record belongs to another company / location |
| 2001 / 2002 | Rotation name already used at this location / location missing |
| 2003–2009 | Structure: plan count, template not a rotation template (2004), weeks per step, step count, cycle length, team count, duplicate team patterns |
| 2012 / 2013 | Rotation not found / team not on this rotation (or already on that team) |
| 2014 | 1–200 employees per enrol request |
| 2015 | Date rule broken (start in the past, started enrolment's start changed, end before start or before today) |
| 2016 | Employee is on a roster board or another rotation in that period |
| 2017 | Member cannot be removed (already ended, or end date missing for a running member) |
| 2018 | Rotation has current or upcoming members – cannot be edited or deleted |
| 2019 | Enrolment shorter than one full cycle |
| 2025 / 2026 / 2027 | Team pattern not a rotation of the cycle / employee already a member / rotation has no pattern |
| 2028 / 2029 | Edit: plan id not on this rotation / plan list inconsistent (reload the page) |
| 2030–2035 | Rotation template: location missing, company-level, not all 7 days, duplicate day, no working day, working day with no time |

## 10. Points to note for testing

These come from comparing the screens with the APIs. They are current behaviour, not confirmed requirements; raise a ticket where the behaviour looks wrong.

- **Planner sub-tab and URL.** The Planner's Regular/Rotation sub-tab is not read from the `tab` query parameter (only the Templates tab uses it). Opening `?view=planner&tab=rotation` still shows Regular.
- **No "remove employee" in the UI** for regular plans or rotations, and no "move to another team" for rotations. The APIs exist (5.5, 6.5).
- **End date equal to start**: the Add Employees date picker allows it but submit rejects it (the API also requires end \> start). Edit Effective Period allows it (API: end ≥ start).
- **Edit Effective Period** has no date limits in the picker; only the API enforces the rules.
- **Move** starts tomorrow at the earliest; Add Employees and rotation joins allow today.
- **Rotation wizard** lets a policy toggle be ON with no policy selected; the regular plan form blocks this.
- **Edit rotation** is locked in the UI when anyone has ever been enrolled; the API (2018) blocks only current or upcoming members.
- **Empty location card → "New Rotation Plan"** opens the wizard without pre-selecting that location.
- **Create regular plan** loads templates without `state=active`; check that archived templates are not offered.
- **API-only behaviour** hidden by the UI: the default plan can be deleted, a deleted or non-regular plan can be set as default, and a plan's template can be changed without updating existing assignments (4.4).
- The 10-plan limit per location counts deleted, roster and rotation plans.
- Move ends the source before joining the target. If the target join fails after the preflight passed, the employee could be left without a plan.
