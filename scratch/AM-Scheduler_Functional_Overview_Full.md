

# === PAGE 1 ===

Scheduler (Roster) – Functional Overview
This page explains the Scheduler screen (Attendance → Scheduler): how a roster
board is set up, how roster shifts (work plans) are created, how employees are added to
a board (work assignment), how shifts are planned day by day, how a period is
published, and what the Overview and Schedules tabs show. Each section gives the
user steps on screen, the business rules and the APIs behind them. It was written from
the backend (SP.AttendanceSvc) and the frontend (ZW.Manage-UI, zw-
attendance/modules/scheduler ) as of Nov 17, 2026. For regular plans and
rotations see Shifts & Rotation Planner – Functional Overview; for the full Attendance
flow see Attendance Module – Functional Overview.
Table Of Contents
1. Module at a glance
1.1 Terms used on this page
2. End-to-end flow
3. Before you start (prerequisites)
4. Roster shifts (Work Plan) – Templates tab
4.1 Functional steps
4.2 Business rules
4.3 APIs – Roster shift
5. Boards and areas – Boards tab
5.1 Functional steps
5.2 Business rules
5.3 APIs – Board and areas
6. Board employees (Work Assignment)
6.1 Functional steps – Add Employees
6.2 Functional steps – maintaining board employees
6.3 Business rules
6.4 APIs – Board employees
7. Planner – planning shifts day by day
7.1 Schedule Plans list
7.2 Setup step (boards with areas)
7.3 Planner grid – assign shifts and day off
7.4 Business rules
7.5 APIs – Planner
8. Publishing a period
8.1 Functional steps
8.2 Period status
8.3 Business rules
8.4 APIs – Publish
9. Overview tab
9.1 Filters
9.2 What each widget shows

### TABLES ON PAGE 1

| Scheduler (Roster) – Functional Overview This page explains the Scheduler screen (Attendance → Scheduler): how a roster board is set up, how roster shifts (work plans) are created, how employees are added to a board (work assignment), how shifts are planned day by day, how a period is published, and what the Overview and Schedules tabs show. Each section gives the user steps on screen, the business rules and the APIs behind them. It was written from the backend (SP.AttendanceSvc) and the frontend (ZW.Manage-UI, zw- attendance/modules/scheduler ) as of Nov 17, 2026. For regular plans and rotations see Shifts & Rotation Planner – Functional Overview; for the full Attendance flow see Attendance Module – Functional Overview. Table Of Contents 1. Module at a glance 1.1 Terms used on this page 2. End-to-end flow 3. Before you start (prerequisites) 4. Roster shifts (Work Plan) – Templates tab 4.1 Functional steps 4.2 Business rules 4.3 APIs – Roster shift 5. Boards and areas – Boards tab 5.1 Functional steps 5.2 Business rules 5.3 APIs – Board and areas 6. Board employees (Work Assignment) 6.1 Functional steps – Add Employees 6.2 Functional steps – maintaining board employees 6.3 Business rules 6.4 APIs – Board employees 7. Planner – planning shifts day by day 7.1 Schedule Plans list 7.2 Setup step (boards with areas) 7.3 Planner grid – assign shifts and day off 7.4 Business rules 7.5 APIs – Planner 8. Publishing a period 8.1 Functional steps 8.2 Period status 8.3 Business rules 8.4 APIs – Publish 9. Overview tab 9.1 Filters |
| 9.2 What each widget shows |

|  |
| Scheduler (Roster) – Functional Overview |
|  |
| This page explains the Scheduler screen (Attendance → Scheduler): how a roster board is set up, how roster shifts (work plans) are created, how employees are added to |
| a board (work assignment), how shifts are planned day by day, how a period is published, and what the Overview and Schedules tabs show. Each section gives the user steps on screen, the business rules and the APIs behind them. It was written from the backend (SP.AttendanceSvc) and the frontend (ZW.Manage-UI, zw- attendance/modules/scheduler ) as of Nov 17, 2026. For regular plans and rotations see Shifts & Rotation Planner – Functional Overview; for the full Attendance flow see Attendance Module – Functional Overview. |
| Table Of Contents 1. Module at a glance 1.1 Terms used on this page 2. End-to-end flow 3. Before you start (prerequisites) 4. Roster shifts (Work Plan) – Templates tab 4.1 Functional steps 4.2 Business rules 4.3 APIs – Roster shift 5. Boards and areas – Boards tab 5.1 Functional steps 5.2 Business rules 5.3 APIs – Board and areas 6. Board employees (Work Assignment) 6.1 Functional steps – Add Employees 6.2 Functional steps – maintaining board employees 6.3 Business rules 6.4 APIs – Board employees 7. Planner – planning shifts day by day 7.1 Schedule Plans list 7.2 Setup step (boards with areas) 7.3 Planner grid – assign shifts and day off 7.4 Business rules 7.5 APIs – Planner 8. Publishing a period 8.1 Functional steps 8.2 Period status 8.3 Business rules |



# === PAGE 2 ===

9.3 Business rules
9.4 APIs – Overview
10. Schedules tab and member schedule
10.1 Functional steps
10.2 Member schedule page
10.3 Business rules
10.4 APIs – Schedules
11. How the Scheduler works with the other modules
12. Error codes
13. Points to note for testing
13.1 Screen
13.2 API behaviour worth checking
1. Module at a glance
The Scheduler is for teams whose shifts change day by day. A supervisor keeps a board of
employees, plans a shift or a day off for every employee on every day of a period, and
publishes the period so employees can see it. It has five top tabs; the open tab is kept in the
URL as /attendance/Scheduler?
tab=overview|schedules|planner|boards|templates (default Overview).
Tab What the user does there Main APIs
Overview Read-only dashboard: employees roster-
on boards, periods still to publish, boards/overview/*
publishing status per board,
today's published shifts, this week
per board (section 9).
Schedules Read-only employee × day grid roster-
per board for a week, and a boards/schedules ,
schedule page per member roster-
(section 10). boards/schedules/e
mployees/{id}
Planner Schedule Plans list (one row per schedule-plans ,
board, one cell per period). Open roster-
a plan to place employees in boards/{id}/schedu
areas, assign shifts / day off, copy, le/*
clear, export and publish (sections
7–8).

### TABLES ON PAGE 2

| Tab | What the user does there | Main APIs |
| Overview | Read-only dashboard: employees on boards, periods still to publish, publishing status per board, today's published shifts, this week per board (section 9). | roster- boards/overview/* |
| Schedules | Read-only employee × day grid per board for a week, and a schedule page per member (section 10). | roster- boards/schedules , roster- boards/schedules/e mployees/{id} |
| Planner | Schedule Plans list (one row per board, one cell per period). Open a plan to place employees in areas, assign shifts / day off, copy, clear, export and publish (sections 7–8). | schedule-plans , roster- boards/{id}/schedu le/* |

|  |  |  |



# === PAGE 3 ===

Boards Create and maintain boards roster-boards ,
(location, supervisor, publishing roster-
frequency, areas) and their boards/{id}/employ
employees (sections 5–6). ees , …/areas
Templates Create and maintain the roster workplans/roster ,
shifts of each board: name, code, workplans?
colour, timing, policies (section 4). type=roster
Regular work plans and shift rotations are a separate menu, Shifts & Rotation. They share the
same schedule store and conflict rules (section 11).
1.1 Terms used on this page
Term Meaning Collection
Board A team planned day by day at one ERP.Attendan
location, with one supervisor, a ce.RosterBoa
publishing frequency and optional rds
areas.
Area A sub-group of a board (for inside the board
example Tool Room). On a board
with areas, every employee must be
placed in an area before they can
be scheduled.
Shift (roster work A work plan of PlanType Roster (2) ERP.Attendan
plan) that belongs to one board. Each ce.WorkPlans
shift owns its own Roster template +
(type 4) with time, colour and code, WorkTemplate
plus optional Break / Overtime / s
Grace policies. The Templates tab
shows these shifts.
Membership An employee's period on a board: inside the board
(board start, optional end, area. Segments:
employee) Upcoming (starts after today),
Active, Past (ended before today).
Period The planning and publishing calculated
window set by the board's
frequency: Weekly (Sunday–

### TABLES ON PAGE 3

| Boards | Create and maintain boards (location, supervisor, publishing frequency, areas) and their employees (sections 5–6). | roster-boards , roster- boards/{id}/employ ees , …/areas |
| Templates | Create and maintain the roster shifts of each board: name, code, colour, timing, policies (section 4). | workplans/roster , workplans? type=roster |

| Term | Meaning | Collection |
| Board | A team planned day by day at one location, with one supervisor, a publishing frequency and optional areas. | ERP.Attendan ce.RosterBoa rds |
| Area | A sub-group of a board (for example Tool Room). On a board with areas, every employee must be placed in an area before they can be scheduled. | inside the board |
| Shift (roster work plan) | A work plan of PlanType Roster (2) that belongs to one board. Each shift owns its own Roster template (type 4) with time, colour and code, plus optional Break / Overtime / Grace policies. The Templates tab shows these shifts. | ERP.Attendan ce.WorkPlans + WorkTemplate s |
| Membership (board employee) | An employee's period on a board: start, optional end, area. Segments: Upcoming (starts after today), Active, Past (ended before today). | inside the board |
| Period | The planning and publishing window set by the board's frequency: Weekly (Sunday– | calculated |
|  |  |  |



# === PAGE 4 ===

Saturday), Bi-weekly (fortnight) or
Monthly (calendar month).
Roster day The per-employee, per-date record: ERP.Attendan
a shift or a Day Off. AssignmentType ce.WorkAssig
Roster (2). This is the roster's "work nmentMaps
assignment".
Schedule period One row per board and period once ERP.Attendan
(publish state) it is first published: Draft / ce.RosterSch
Published, version, "changes not edulePeriods
published" flag, published by / at.
Period status (shown as "New plan"), calculated
NOT PLANNED
, , (section
PENDING PUBLISHED COMPLETED
8.2).
2. End-to-end flow
1 BOARDS tab TEMPLATES tab
PLANNER tab
2 ────────── ─────────────
───────────
3 Create Board ───────────────────────────► Roster shift (belongs to
board)
4 (location, supervisor, name, code, colour, time,
5 frequency, areas) policies → own Roster
template
6 │
7 ▼
8 Add Employees ─► check-conflicts ─► add (adjust regular plans) ─►
Board membership
9
│
10
▼
11 (board has areas) Assign
employees to areas
12
│
13
▼
14 Schedule Plans ─► open
period ─► assign shift / Day off,
15
copy previous, clear
16
│ writes
17
▼
18
Roster days (employee × date)
19
│
20
▼
21
Publish period ─► ESS shows the days
22
│

### TABLES ON PAGE 4

|  | Saturday), Bi-weekly (fortnight) or Monthly (calendar month). |  |
| Roster day | The per-employee, per-date record: a shift or a Day Off. AssignmentType Roster (2). This is the roster's "work assignment". | ERP.Attendan ce.WorkAssig nmentMaps |
| Schedule period (publish state) | One row per board and period once it is first published: Draft / Published, version, "changes not published" flag, published by / at. | ERP.Attendan ce.RosterSch edulePeriods |
| Period status | (shown as "New plan"), NOT PLANNED , , (section PENDING PUBLISHED COMPLETED 8.2). | calculated |

| 1 BOARDS tab TEMPLATES tab PLANNER tab 2 ────────── ───────────── ─────────── 3 Create Board ───────────────────────────► Roster shift (belongs to board) 4 (location, supervisor, name, code, colour, time, 5 frequency, areas) policies → own Roster template 6 │ 7 ▼ 8 Add Employees ─► check-conflicts ─► add (adjust regular plans) ─► Board membership 9 │ 10 ▼ 11 (board has areas) Assign employees to areas 12 │ 13 ▼ 14 Schedule Plans ─► open period ─► assign shift / Day off, 15 copy previous, clear 16 │ writes 17 ▼ 18 Roster days (employee × date) 19 │ 20 ▼ 21 Publish period ─► ESS shows the days 22 │ |
|  |



# === PAGE 5 ===

23 OVERVIEW tab / SCHEDULES tab / Excel export ◄──
read boards, periods, roster days
Key principle: publish is a flag, not a copy. Publishing marks a board's period as visible.
Employees always see the current roster days of a published period, so a change after
publishing is visible at once and the period is flagged Changes not published until it is
published again.
3. Before you start (prerequisites)
1. Work locations exist in the Company / Employee Hierarchy service. A board, its shifts and
its employees belong to one location.
2. Policies (Break, Overtime, Grace Period) exist under Configuration if a shift needs them.
Only active policies are offered.
3. Employees are active in the Employee service at the board's location. The picker lists only
that location's employees.
4. Holiday calendars for the location (or the company default calendar) mark holidays on the
grid.
5. The order is fixed: create the board first, then its shifts (a shift is always created for a
board), then add employees, then plan.
4. Roster shifts (Work Plan) – Templates tab
4.1 Functional steps
Action Steps on screen API
View shifts Templates tab. Grouped location → GET workplans?
board. Each card: colour, name, type=roster
code, timing (with "Varies by day"),
total hours, policies. Search by
location, board, name or code.
Expand all / Collapse all in ⋮.
Create shift 1. Click + Shift (or, in the Planner GET
grid, Add Shift → Shift From worktemplates/
Scratch, where the board is short-
already set). code/availabil
2. Choose Location, then Board ity?code=
(enabled after location). GET
attpolicies?
3. Enter Shift name (EN required, AR
state=active&t
optional).
ype=… (×3)
4. Enter Code: exactly 7 letters/digits,
POST
upper-cased; checked live for

### TABLES ON PAGE 5

| Key princ Employee publishin published 3. Before 1. Work l its emp 2. Policie Only a 3. Emplo that loc 4. Holida grid. 5. The or board), 4. Roster 4.1 Functio | 23 OVERVIEW tab / SCHEDULES tab / Excel export ◄── read boards, periods, roster days |  |  | ible. er is hifts and them. lists only ys on the or a |
|  | iple: publish is a flag, not a copy. Publishing marks a board's period as vis s always see the current roster days of a published period, so a change aft g is visible at once and the period is flagged Changes not published until it again. you start (prerequisites) ocations exist in the Company / Employee Hierarchy service. A board, its s loyees belong to one location. s (Break, Overtime, Grace Period) exist under Configuration if a shift needs ctive policies are offered. yees are active in the Employee service at the board's location. The picker ation's employees. y calendars for the location (or the company default calendar) mark holida der is fixed: create the board first, then its shifts (a shift is always created f then add employees, then plan. shifts (Work Plan) – Templates tab nal steps |  |  |  |
|  | Action | Steps on screen | API |  |
|  | View shifts | Templates tab. Grouped location → board. Each card: colour, name, | GET workplans? type=roster |  |
|  |  | code, timing (with "Varies by day"), total hours, policies. Search by location, board, name or code. Expand all / Collapse all in ⋮. |  |  |
|  | Create shift | 1. Click + Shift (or, in the Planner grid, Add Shift → Shift From Scratch, where the board is already set). 2. Choose Location, then Board (enabled after location). 3. Enter Shift name (EN required, AR optional). 4. Enter Code: exactly 7 letters/digits, upper-cased; checked live for | GET worktemplates/ short- code/availabil ity?code= GET attpolicies? state=active&t ype=… (×3) POST |  |
|  |  |  |  |  |



# === PAGE 6 ===

availability. workplans/rost
5. Pick a Colour (8 swatches). er?
locationId=
6. Set Starts / Ends. An end earlier
than the start means an overnight
shift; the length is shown live.
7. Optionally switch on Break /
Overtime / Grace Period and pick
one policy for each.
8. Save.
View shift Click a card or ⋮ → View. Read-only GET
details page: code, timings, overnight flag, workplans/{id
total hours, per-day strip, policies. }
Back returns to where it was opened
from (Templates, Board details or the
grid).
Edit shift ⋮ → Edit (Templates tab or the grid's PATCH
Saved shifts). Location, board and workplans/rost
code are locked. The toast reports er/{id}?
how many planned days were locationId=
updated and whether a republish is
needed.
Delete shift ⋮ → Delete → confirm. If the shift is DELETE
still in use, a popup says how many workplans/{id}
employees it is assigned to. ?locationId=
4.2 Business rules
A shift belongs to exactly one board and cannot be moved to another board. The board
must be at the given location (9001 / 9002).
Creating a shift creates two records: its own Roster work template (type 4) and the roster
work plan, and adds the shift to the board's palette.
Code becomes the template's short code: 7 letters/digits, upper case, unique across the
whole company and all template types, including deleted ones (1106). It can never change
(1107).
Name must be unique on the board (case-insensitive).
Colour is HEX ( #RGB or #RRGGBB ). A working day needs a duration above 0 and at most
23:59, with start ≠ end. Shifts may cross midnight.

### TABLES ON PAGE 6

|  | availability. 5. Pick a Colour (8 swatches). 6. Set Starts / Ends. An end earlier than the start means an overnight shift; the length is shown live. 7. Optionally switch on Break / Overtime / Grace Period and pick one policy for each. 8. Save. | workplans/rost er? locationId= |
| View shift details | Click a card or ⋮ → View. Read-only page: code, timings, overnight flag, total hours, per-day strip, policies. Back returns to where it was opened from (Templates, Board details or the grid). | GET workplans/{id } |
| Edit shift | ⋮ → Edit (Templates tab or the grid's Saved shifts). Location, board and code are locked. The toast reports how many planned days were updated and whether a republish is needed. | PATCH workplans/rost er/{id}? locationId= |
| Delete shift | ⋮ → Delete → confirm. If the shift is still in use, a popup says how many employees it is assigned to. | DELETE workplans/{id} ?locationId= |



# === PAGE 7 ===

A location can hold at most 20 work templates of all types (1203); every roster shift uses
one.
Policies: one per type, active and of an enabled type (1501, 1506, 1507, 1508). Sending no
policies on edit leaves them unchanged.
Edit is refused for ever once the shift has any scheduled day on or before today (1905). A
successful edit rebuilds the shift's future roster days and flags published periods from
today as Changes not published.
Delete is refused while the shift has a roster day today or later (1304). A successful delete
retires past days, removes the shift from the board and deletes its template.
If a shift is assigned on a weekday its template marks as non-working, that day uses the
template's first working time.
4.3 APIs – Roster shift
Base path: /api/companies/{companyId}/workplans . Company comes from the route
and location from locationId ; request bodies carry no tenant, company or location IDs.
Method and path Purpose and usage
GET /workplans? Roster shifts, used by the Templates tab and the
type=roster&locat board's Work Plan tab.
ionId=
GET One shift with its template and policies. 1301 if
/workplans/{id} not found.
POST Creates a shift. Body: tenantName , boardId ,
/workplans/roster shiftName{en,ar} , code , colour ,
?locationId= description , rosterTimeSlots[]
( dayEnum , isWorkingDay , startTime ,
endTime , workDurationInMinutes ),
totalWorkDurationInMinutes ,
totalWorkingDays , totalDaysOff , the
three policy flags, policyIds[] . Returns
workPlan , workTemplate , boardId ,
boardShiftCount . Errors: validation 400, 404
board, 9001, 9002, 1106, 1203, 1501, 1506–1508,
duplicate name.

### TABLES ON PAGE 7

| Method and path | Purpose and usage |
| GET /workplans? type=roster&locat ionId= | Roster shifts, used by the Templates tab and the board's Work Plan tab. |
| GET /workplans/{id} | One shift with its template and policies. 1301 if not found. |
| POST /workplans/roster ?locationId= | Creates a shift. Body: tenantName , boardId , shiftName{en,ar} , code , colour , description , rosterTimeSlots[] ( dayEnum , isWorkingDay , startTime , endTime , workDurationInMinutes ), totalWorkDurationInMinutes , totalWorkingDays , totalDaysOff , the three policy flags, policyIds[] . Returns workPlan , workTemplate , boardId , boardShiftCount . Errors: validation 400, 404 board, 9001, 9002, 1106, 1203, 1501, 1506–1508, duplicate name. |

| totalWorkingDays | , | totalDaysOff |

|  |  |



# === PAGE 8 ===

PATCH Edits a shift (all fields optional). Returns
/workplans/roster affectedAssignmentMapCount and
/{id}? republishRequired . Errors: 1905 already
locationId= scheduled, 1107 code change, other board,
duplicate name, policy errors.
DELETE Deletes a shift. Returns
/workplans/{id}? deactivatedAssignmentMapCount . 1304 if
locationId= scheduled today or later.
GET Live check that a code is free, used by the shift
/worktemplates/sh form.
ort-
code/availability
?code=
Sample request – create a roster shift (Morning, 06:00–14:00)
1 POST /api/companies/{companyId}/workplans/roster?locationId=
{locationId}
2 {
3 "tenantName": "Demo Tenant",
4 "boardId": "b0b0…",
5 "shiftName": { "en": "Morning", "ar": "" },
6 "code": "MORN001",
7 "colour": "#14B8A6",
8 "description": "",
9 "rosterTimeSlots": [
10 { "dayEnum": 0, "isWorkingDay": true, "startTime": "06:00",
"endTime": "14:00", "workDurationInMinutes": 480 }
11 // … one row per day, Sunday to Saturday
12 ],
13 "totalWorkDurationInMinutes": 3360, "totalWorkingDays": 7,
"totalDaysOff": 0,
14 "isBreakPolicyEnabled": true, "isOvertimePolicyEnabled": false,
"isGracePeriodPolicyEnabled": false,
15 "policyIds": [ "br01…" ]
16 }
5. Boards and areas – Boards tab
5.1 Functional steps
Action Steps on screen API
View boards Boards tab. Grouped by location ("N GET roster-
boards · M employees"); a location boards/?
with no board shows New Board. locationId=
Each card: name, status, "Changes
not published" tag, Supervisor,
Publishing, Areas, Employees

### TABLES ON PAGE 8

| PATCH /workplans/roster /{id}? locationId= | Edits a shift (all fields optional). Returns affectedAssignmentMapCount and republishRequired . Errors: 1905 already scheduled, 1107 code change, other board, duplicate name, policy errors. |
| DELETE /workplans/{id}? locationId= | Deletes a shift. Returns deactivatedAssignmentMapCount . 1304 if scheduled today or later. |
| GET /worktemplates/sh ort- code/availability ?code= | Live check that a code is free, used by the shift form. |

| Action | Steps on screen | API |
| View boards | Boards tab. Grouped by location ("N boards · M employees"); a location with no board shows New Board. Each card: name, status, "Changes not published" tag, Supervisor, Publishing, Areas, Employees | GET roster- boards/? locationId= |
|  |  |  |



# === PAGE 9 ===

("active → projected" when people
join later) and a strip "N employees
joining from …". Search by location or
board name.
Create board 1. Create Board (or New Board on POST roster-
an empty location, which pre-fills boards/?
it). locationId=
2. Enter Name (EN, AR optional),
Location, Supervisor and
Publishing frequency (Weekly / Bi-
Weekly).
3. Optionally switch on Areas and
add area names (unique).
4. Create Board (back to Boards) or
Create Board & Add Employees
(opens Add Employees for the new
board).
Board details Click a card. Header with Supervisor, GET roster-
Publishing, Areas, Employees, Add boards/{id}
Employee. Tabs: Employees (search, GET workplans?
department, designation, "Show type=roster&lo
past"), Area, Work Plan (the board's cationId=
shifts; click to open details).
Edit board ⋮ → Edit board. Location is read- PATCH roster-
only. Only changed fields are sent; boards/{id}
with no change the screen says "No
changes to save". If an area is still in
use, it is put back and a message
explains.

### TABLES ON PAGE 9

|  | ("active → projected" when people join later) and a strip "N employees joining from …". Search by location or board name. |  |
| Create board | 1. Create Board (or New Board on an empty location, which pre-fills it). 2. Enter Name (EN, AR optional), Location, Supervisor and Publishing frequency (Weekly / Bi- Weekly). 3. Optionally switch on Areas and add area names (unique). 4. Create Board (back to Boards) or Create Board & Add Employees (opens Add Employees for the new board). | POST roster- boards/? locationId= |
| Board details | Click a card. Header with Supervisor, Publishing, Areas, Employees, Add Employee. Tabs: Employees (search, department, designation, "Show past"), Area, Work Plan (the board's shifts; click to open details). | GET roster- boards/{id} GET workplans? type=roster&lo cationId= |
| Edit board | ⋮ → Edit board. Location is read- only. Only changed fields are sent; with no change the screen says "No changes to save". If an area is still in use, it is put back and a message explains. | PATCH roster- boards/{id} |

|  |  |  |



# === PAGE 10 ===

Areas Board details → Area tab: Add Area; PATCH roster-
per area ⋮ Rename or Delete. boards/{id}
( addedAreas )
PATCH
…/areas/{areaI
d}/rename
DELETE
…/areas/{areaI
d}
Delete board ⋮ → Delete board → confirm. If DELETE roster-
refused, an "Unable to delete" popup boards/{id}
gives the reason; for employees,
Okay opens the Employees tab with
past members shown.
5.2 Business rules
A board belongs to one location, which can never change. It has a single supervisor.
Publishing frequency: Weekly (1), Bi-weekly (2), Monthly (3). The screen offers Weekly
and Bi-weekly; Custom is refused.
Periods: weeks run Sunday–Saturday and are labelled with the ISO week of the Sunday
("Week 42" for 18–24 Oct 2026); fortnights are fixed from 2 Jan 2000 ("Fortnight n");
monthly is a calendar month.
English name is required when editing. Board names are not checked for uniqueness.
Area rules: an area used by any member row (past rows included) cannot be deleted
(1903); areas cannot be switched off while any member has an area (1904). Renaming an
area updates the roster days.
Delete is refused when the board has any member row, past rows included (1901), or any
of its shifts has a day today or later (1902). On success, shifts and their templates are
deleted and the board's roster days are deactivated.
Changing the frequency is allowed at any time; existing publish rows are not touched (see
13.2).
5.3 APIs – Board and areas
Base path: /api/companies/{companyId}/roster-boards .
Method and path Purpose and usage
GET /?locationId= Boards grouped by location, with counts.

### TABLES ON PAGE 10

| Areas | Board details → Area tab: Add Area; per area ⋮ Rename or Delete. | PATCH roster- boards/{id} ( addedAreas ) PATCH …/areas/{areaI d}/rename DELETE …/areas/{areaI d} |
| Delete board | ⋮ → Delete board → confirm. If refused, an "Unable to delete" popup gives the reason; for employees, Okay opens the Employees tab with past members shown. | DELETE roster- boards/{id} |

| Method and path | Purpose and usage |
| GET /?locationId= | Boards grouped by location, with counts. |

|  |  |



# === PAGE 11 ===

GET /{boardId} One board: areas, shifts, employees (all
segments), counts.
POST /?locationId= Creates a board. Body: tenantName ,
boardName{en,ar} ,
supervisor{employeeId,name,employee
Code} , publishingFrequency (1–3),
hasAreas , areas[{name}] .
PATCH /{boardId} Edits a board. Any of boardName ,
supervisor , publishingFrequency ,
hasAreas , addedAreas[] ,
removedAreaIds[] . Returns
updatedFields . Errors: 1903, 1904, 404
area.
DELETE /{boardId} Deletes a board. Errors: 1901 has employees,
1902 shift scheduled today or later.
PATCH Body { name: { en, ar } } (EN
/{boardId}/areas/{ required). 404 if the area does not exist.
areaId}/rename
DELETE Deletes an area. 1903 if any member row uses
/{boardId}/areas/{ it.
areaId}
Sample request – create a board with two areas
1 POST /api/companies/{companyId}/roster-boards/?locationId=
{locationId}
2 {
3 "tenantName": "Demo Tenant",
4 "boardName": { "en": "Warehouse Team", "ar": "" },
5 "supervisor": { "employeeId": "e900…", "name": "Supervisor Name",
"employeeCode": "AP004" },
6 "publishingFrequency": 1,
7 "hasAreas": true,
8 "areas": [ { "name": { "en": "Tool Room" } }, { "name": { "en":
"Loading Bay" } } ]
9 }
6. Board employees (Work Assignment)
Adding an employee to a board creates a membership (who is on the board, from when, until
when, in which area). The day-by-day shifts are then planned on the Planner (section 7).
6.1 Functional steps – Add Employees

### TABLES ON PAGE 11

| GET /{boardId} | One board: areas, shifts, employees (all segments), counts. |
| POST /?locationId= | Creates a board. Body: tenantName , boardName{en,ar} , supervisor{employeeId,name,employee Code} , publishingFrequency (1–3), hasAreas , areas[{name}] . |
| PATCH /{boardId} | Edits a board. Any of boardName , supervisor , publishingFrequency , hasAreas , addedAreas[] , removedAreaIds[] . Returns updatedFields . Errors: 1903, 1904, 404 area. |
| DELETE /{boardId} | Deletes a board. Errors: 1901 has employees, 1902 shift scheduled today or later. |
| PATCH /{boardId}/areas/{ areaId}/rename | Body { name: { en, ar } } (EN required). 404 if the area does not exist. |
| DELETE /{boardId}/areas/{ areaId} | Deletes an area. 1903 if any member row uses it. |



# === PAGE 12 ===

Entry points: Add employees on a board card, Add Employee on Board details, Create Board
& Add Employees, or Add employees in the Planner setup step.
1. Set Start date (default today, cannot be in the past) and, optionally, End date ("+ Add end
date", not before the start). Empty means open-ended.
2. Select employees (active employees at the board's location; search, department filter,
page size). The Current Plan column shows what each employee is on today.
3. About 0.4 s after any change to the selection or dates the screen runs a conflict check
(preview, nothing saved) and shows:
red "Committed elsewhere": the employee is on another board or a rotation for
BLOCKED
those dates. View shows the blocking plans; the user must Skip employees.
amber "Already on another plan": the employee has a regular work plan for
ADJUSTABLE
those dates. Adjust plan shows how each regular plan will end early, split or be removed,
and the user confirms; or Skip employees.
red "Already on this board for these dates": View details or Skip
ALREADY ON BOARD
employees.
no banner.
AVAILABLE
4. Click Add. It stays disabled while the check runs, while a blocked or unconfirmed
adjustable employee is selected, or when everyone selected is already on the board.
5. A toast reports how many were added and skipped; the screen returns to the Boards tab.
6.2 Functional steps – maintaining board employees
Action Steps and rules API
Assign to Planner → open the plan → setup GET roster-
areas step "Assign employees to areas", or boards/{id}/ar
the grid's ⋮ → Move employees. eas/employees?
Choose an Area and the employees; asOf=
Assign area / Move employees. PATCH roster-
Updates every not-yet-ended boards/{id}/ar
membership row of the employee eas/{areaId}/e
and the area on roster days from mployees
today.
Edit effective Board details → Employees → row ⋮ POST
period (Upcoming members) or the …/employees/ch
Upcoming employees page. Start eck-conflicts
editable only before it starts (today ( excludeMember
or later); end not before today or the shipId )
start, or cleared. A conflict check PATCH

### TABLES ON PAGE 12

| Action | Steps and rules | API |
| Assign to areas | Planner → open the plan → setup step "Assign employees to areas", or the grid's ⋮ → Move employees. Choose an Area and the employees; Assign area / Move employees. Updates every not-yet-ended membership row of the employee and the area on roster days from today. | GET roster- boards/{id}/ar eas/employees? asOf= PATCH roster- boards/{id}/ar eas/{areaId}/e mployees |
| Edit effective period | Board details → Employees → row ⋮ (Upcoming members) or the Upcoming employees page. Start editable only before it starts (today or later); end not before today or the start, or cleared. A conflict check | POST …/employees/ch eck-conflicts ( excludeMember shipId ) PATCH |
|  |  |  |



# === PAGE 13 ===

excluding this membership runs first; …/employees/{m
blocked → Save disabled; regular embershipId}/p
overlap → "Adjust & Save". Refused if eriod
already scheduled days would fall
outside the new period.
Move to Row ⋮ (Active members) → Move. POST
another plan Tabs: Scheduler Board (another …/employees/{m
board at the same location) or Work embershipId}/m
Plan (a regular plan or a rotation ove/check-
team). From date defaults to and conflicts
cannot be earlier than tomorrow; To PATCH
date optional. Preflight first; blocked …/employees/{m
stops the move, a regular overlap embershipId}/m
changes the button to "Adjust & ove
Move".
Remove from Row ⋮ (Upcoming members) → DELETE
board Remove → confirm. Not-yet-started …/employees/{m
membership is deleted; an active one embershipId}
with nothing scheduled ends today.
If days are already scheduled, a
popup suggests Edit effective period
instead.
Upcoming Board card strip → "View GET
employees employees". Lists members whose …/employees?
start is after today, with Edit period segment=upcomi
and Remove. ng
6.3 Business rules
One commitment at a time. For any date an employee can be on only one board or
rotation. Another board or a rotation blocks the whole request (1914). A regular work plan is
adjustable: without confirmation the request is refused (1409); with
adjustConflicts=true the regular plan is ended early, split or deactivated. Conflicts
are checked within the board's location.
An employee already on this board for an overlapping window is skipped, not an error. Two
rows of the same employee on one board cannot overlap.
Add: start today or later, end on or after start, 1+ unique employees. Employees the
Employee service cannot find are returned as not found.

### TABLES ON PAGE 13

|  | excluding this membership runs first; blocked → Save disabled; regular overlap → "Adjust & Save". Refused if already scheduled days would fall outside the new period. | …/employees/{m embershipId}/p eriod |
| Move to another plan | Row ⋮ (Active members) → Move. Tabs: Scheduler Board (another board at the same location) or Work Plan (a regular plan or a rotation team). From date defaults to and cannot be earlier than tomorrow; To date optional. Preflight first; blocked stops the move, a regular overlap changes the button to "Adjust & Move". | POST …/employees/{m embershipId}/m ove/check- conflicts PATCH …/employees/{m embershipId}/m ove |
| Remove from board | Row ⋮ (Upcoming members) → Remove → confirm. Not-yet-started membership is deleted; an active one with nothing scheduled ends today. If days are already scheduled, a popup suggests Edit effective period instead. | DELETE …/employees/{m embershipId} |
| Upcoming employees | Board card strip → "View employees". Lists members whose start is after today, with Edit period and Remove. | GET …/employees? segment=upcomi ng |



# === PAGE 14 ===

Edit period: a started membership cannot change its start; its end cannot be before today.
Narrowing is refused while scheduled days fall outside (the response lists the dates).
Remove is refused once the membership has any roster day, past days included; use Edit
period or Move instead.
Move: effectiveFrom defaults to tomorrow (today allowed by the API, past refused);
the end defaults to the current end. The target must be at the same location (9002), not
hold the employee already, and not be blocked (1408); a regular overlap needs
confirmation (1409). From a board, the employee's roster days from effectiveFrom are
deleted and the membership ends the day before (or is deleted if not started). On a board-
to-board move the area is cleared, so the employee must be placed again on an area
board.
Membership changes that affect published periods flag them Changes not published
(table in 8.3). Adding employees does not.
6.4 APIs – Board employees
Base path: /api/companies/{companyId}/roster-boards/{boardId} . Writes need
?locationId= matching the board.
Method and path Purpose and usage
POST Preview, writes nothing. Body:
/employees/check- employeeIds[] , startDate , endDate? ,
conflicts excludeMembershipId? (when editing;
then a past start is allowed). Returns
cleanEmployeeIds , alreadyMembers[] ,
adjustableEmployeeIds ,
blockedEmployeeIds , conflicts[] ,
canProceed .
PATCH /employees Adds employees. Body: employeeIds[] ,
startDate , endDate? , areaId? ,
adjustConflicts . Returns
addedEmployees , skippedEmployeeIds ,
notFoundEmployeeIds ,
totalEmployeeCount . Errors 1914, 1409.
GET /employees? Members, paged. segment = upcoming |
segment=&asOf=&sea active | past | all. pageSize default 50, max
rch=&department=&a 500.
reaId=&page=&pageS
ize=

### TABLES ON PAGE 14

| Method and path | Purpose and usage |
| POST /employees/check- conflicts | Preview, writes nothing. Body: employeeIds[] , startDate , endDate? , excludeMembershipId? (when editing; then a past start is allowed). Returns cleanEmployeeIds , alreadyMembers[] , adjustableEmployeeIds , blockedEmployeeIds , conflicts[] , canProceed . |
| PATCH /employees | Adds employees. Body: employeeIds[] , startDate , endDate? , areaId? , adjustConflicts . Returns addedEmployees , skippedEmployeeIds , notFoundEmployeeIds , totalEmployeeCount . Errors 1914, 1409. |
| GET /employees? segment=&asOf=&sea rch=&department=&a reaId=&page=&pageS ize= | Members, paged. segment = upcoming | active | past | all. pageSize default 50, max 500. |

| addedEmployees | , | skippedEmployeeIds |

|  |  |



# === PAGE 15 ===

PATCH Changes a membership's dates. Body:
/employees/{member startDate , endDate? ,
shipId}/period adjustConflicts . Returns
publishReverted . Errors 1914, 1409, date
rules, scheduled days outside.
DELETE Removes or ends a membership (rules in 6.3).
/employees/{member Returns removed or endedOn .
shipId}
POST Move preflight. Body: targetType (1 Board,
/employees/{member 2 WorkPlan, 3 Rotation), targetBoardId |
shipId}/move/check targetWorkPlanId | targetRotationId
-conflicts + targetTeamId , effectiveFrom? ,
endDate? . Returns hasConflicts ,
heldByBoardOrRotation ,
requiresAdjustment , reason .
PATCH Executes the move (same body +
/employees/{member adjustConflicts ). Returns
shipId}/move releasedScheduleCount ,
republishRequiredBoardIds . Errors
1408, 1409, 9002.
GET Areas with their employees, plus employees
/areas/employees? without an area. Feeds the setup step and
asOf= progress ("X of Y assigned").
PATCH Places or moves employees into an area. Body
/areas/{areaId}/em { employeeIds[] } . Returns
ployees assignedEmployeeIds ,
movedEmployeeIds ,
alreadyInAreaEmployeeIds ,
notOnBoardEmployeeIds ,
scheduleSyncedCount .

### TABLES ON PAGE 15

| PATCH /employees/{member shipId}/period | Changes a membership's dates. Body: startDate , endDate? , adjustConflicts . Returns publishReverted . Errors 1914, 1409, date rules, scheduled days outside. |
| DELETE /employees/{member shipId} | Removes or ends a membership (rules in 6.3). Returns removed or endedOn . |
| POST /employees/{member shipId}/move/check -conflicts | Move preflight. Body: targetType (1 Board, 2 WorkPlan, 3 Rotation), targetBoardId | targetWorkPlanId | targetRotationId + targetTeamId , effectiveFrom? , endDate? . Returns hasConflicts , heldByBoardOrRotation , requiresAdjustment , reason . |
| PATCH /employees/{member shipId}/move | Executes the move (same body + adjustConflicts ). Returns releasedScheduleCount , republishRequiredBoardIds . Errors 1408, 1409, 9002. |
| GET /areas/employees? asOf= | Areas with their employees, plus employees without an area. Feeds the setup step and progress ("X of Y assigned"). |
| PATCH /areas/{areaId}/em ployees | Places or moves employees into an area. Body { employeeIds[] } . Returns assignedEmployeeIds , movedEmployeeIds , alreadyInAreaEmployeeIds , notOnBoardEmployeeIds , scheduleSyncedCount . |

|  |  |



# === PAGE 16 ===

GET What each employee is on today (regular plan,
/api/companies/{co board or rotation). Feeds the Current Plan
mpanyId}/workassig column.
nments/current-
plans?
locationId=&employ
eeIds=
Sample requests – add employees with adjustment
1 // 1. preview
2 POST /api/companies/{companyId}/roster-
boards/{boardId}/employees/check-conflicts?locationId={locationId}
3 { "employeeIds": ["e1…", "e2…"], "startDate": "2026-11-22",
"endDate": null }
4 // → cleanEmployeeIds: ["e1…"], adjustableEmployeeIds: ["e2…"],
blockedEmployeeIds: [], canProceed: true
5
6 // 2. add (confirming the regular-plan adjustment for e2)
7 PATCH /api/companies/{companyId}/roster-boards/{boardId}/employees?
locationId={locationId}
8 { "employeeIds": ["e1…", "e2…"], "startDate": "2026-11-22",
"endDate": null, "adjustConflicts": true }
9
10 // 3. place both in an area (board with areas)
11 PATCH /api/companies/{companyId}/roster-
boards/{boardId}/areas/{areaId}/employees?locationId={locationId}
12 { "employeeIds": ["e1…", "e2…"] }
7. Planner – planning shifts day by day
7.1 Schedule Plans list
1. Open the Planner tab. Boards are listed grouped by location, one row per board
("frequency · N employees") and one cell per period inside the view window.
2. Use the toolbar: View (Weekly / Bi-weekly), ‹ date range ›, Today, Location and Status (All /
Published / Pending / Completed / Not planned). Count pills show Plans, Published and
Pending.
3. Each period cell shows its label ("Week 47", "Fortnight 15"), a status chip, a ⚠ when
Changes not published, and for the current period the setup progress ("X of Y assigned ·
Open plan →").
4. Click a board or a cell to open that plan. If the board has areas and no employee is placed
yet, the setup step opens first.
7.2 Setup step (boards with areas)
1. "Assign employees to areas" lists each area with its employee count and the "X of Y
assigned" progress.
2. Assign places unassigned employees in an area; Move employees moves them from one
area to another (6.2).

### TABLES ON PAGE 16

| GET /api/companies/{co mpanyId}/workassig nments/current- plans? locationId=&employ eeIds= | What each employee is on today (regular plan, board or rotation). Feeds the Current Plan column. |



# === PAGE 17 ===

3. When everyone is placed, Start scheduling → opens the grid. With nobody on the board,
the step offers Add employees.
7.3 Planner grid – assign shifts and day off
1. The header shows the board, status chip, "Published at …", ‹ period ›, Today, and the
Publish buttons (section 8). Use the Area filter, and the week navigator when the period is
longer than a week ("Week i of n", "N slots unfilled").
2. Rows are grouped in area bands. The Unassigned band is locked with "Area required
before scheduling" and an Assign areas link. Each row shows scheduled hours against the
weekly cap.
3. Select slots: click a cell; click a name for that row's visible week; click a day header for that
column.
4. The Add Shift panel opens. Under Saved shifts click a shift to apply it, or Day off. Each
shift's ⋮ has View, Edit and Delete. Shift from scratch creates a new shift for this board.
5. If a selected slot already holds a shift or a day off, a Replace dialog asks first ("X of Y slots
already hold …").
6. The shift is saved; a toast reports the slots applied (and any outside membership or not on
board); if the period was published, "Republish needed". The grid reloads.
Other action What it does API
(⋮ menu)
Copy previous Confirm, then copies the whole POST
week previous period into empty cells only. …/schedule/c
Skips holidays in the source, past opy-previous
dates, filled cells, dates outside
membership and deleted shifts; the
toast lists what was skipped.
Clear shifts Clears by selection: nothing selected POST
= whole period (or the filtered area); …/schedule/c
whole rows = those employees; whole lear
columns = those dates; a block =
employees × dates. Ragged
selections are not allowed. Past days
are kept; today is cleared. Shifts and
day offs are removed.
Move Moves employees between areas PATCH
employees (boards with areas only). …/areas/{are

### TABLES ON PAGE 17

| Other action (⋮ menu) | What it does | API |
| Copy previous week | Confirm, then copies the whole previous period into empty cells only. Skips holidays in the source, past dates, filled cells, dates outside membership and deleted shifts; the toast lists what was skipped. | POST …/schedule/c opy-previous |
| Clear shifts | Clears by selection: nothing selected = whole period (or the filtered area); whole rows = those employees; whole columns = those dates; a block = employees × dates. Ragged selections are not allowed. Past days are kept; today is cleared. Shifts and day offs are removed. | POST …/schedule/c lear |
| Move employees | Moves employees between areas (boards with areas only). | PATCH …/areas/{are |
|  |  |  |



# === PAGE 18 ===

aId}/employe
es
Export Downloads an Excel workbook of the GET
period (areas filter applied). Export …/schedule/e
PDF is shown but disabled. xport/excel
What a grid cell can show:
Cell state Look Selectable
Shift / Holiday Shift colour, name, time ("+1d" Yes
worked overnight); holiday tag when on a
holiday
Off "Off" Yes
Empty "+" (counts as unfilled; blocks Yes
publish)
Holiday (open) Holiday name and "+"; filling it is Yes
optional
On leave / Greyed label No
outside
membership
7.4 Business rules
There is one roster day per employee per date. Assigning overwrites whatever was there
(shift or day off).
The shift must exist (1301), be a roster shift and belong to this board (1104).
On a board with areas, every employee being scheduled must have an area (1906).
Dates not covered by the employee's membership are skipped and returned as
outsideMembershipSlots .
Clear: dates must be inside the period (1913). Past days are kept; today and later are
deleted.
Copy previous copies by day offset; for monthly boards weekdays do not line up and
longer months leave extra days empty.
The row hours are compared against a 48-hour weekly cap; weeks over the cap and
double bookings are counted by the API but not shown on screen.

### TABLES ON PAGE 18

|  |  |  |
|  |  | aId}/employe es |
| Export | Downloads an Excel workbook of the period (areas filter applied). Export PDF is shown but disabled. | GET …/schedule/e xport/excel |

| Cell state | Look | Selectable |
| Shift / Holiday worked | Shift colour, name, time ("+1d" overnight); holiday tag when on a holiday | Yes |
| Off | "Off" | Yes |
| Empty | "+" (counts as unfilled; blocks publish) | Yes |
| Holiday (open) | Holiday name and "+"; filling it is optional | Yes |
| On leave / outside membership | Greyed label | No |



# === PAGE 19 ===

Planner, Publish and Export use the UTC date as "today" (Overview and Schedules use
Riyadh time).
7.5 APIs – Planner
Base path: /api/companies/{companyId}/roster-boards/{boardId}/schedule .
Writes need ?locationId= .
Method and path Purpose and usage
GET Schedule Plans list. frequency = Weekly
/api/companies/{co (default) | BiWeekly | Monthly. Returns all
mpanyId}/schedule- boards of the company and locations without
plans? boards. Each board is cut into its own periods
frequency=&anchor= inside the view window (a monthly board in a
weekly view is "clipped"). Per period:
status , employeeCount ,
totalSlotCount , scheduledSlotCount ,
dayOffSlotCount ,
assignableSlotCount ,
unfilledSlotCount ,
unassignedAreaEmployeeCount ,
conflicts (over weekly cap, double
booked), republishRequired ,
publishedAt , version ; plus totals and
previous / next anchors.
GET ?anchor= Grid for the period containing anchor
(default today): areas → employee rows →
cells ( state , isAssignable ), weekly hours
vs cap, summary with isReadyToPublish ,
version , republishRequired .
POST /assign Assign a shift or a day off. Body:
slots[{employeeId, dates[]}] and
either workPlanId or dayOff:true .
Returns appliedSlotCount ,
notOnBoardEmployeeIds ,
outsideMembershipSlots ,
unresolvedEmployeeIds , periods[] ,
publishReverted . Errors 1301, 1104, 1906,
9001, 9002.

### TABLES ON PAGE 19

| Method and path | Purpose and usage |
| GET /api/companies/{co mpanyId}/schedule- plans? frequency=&anchor= | Schedule Plans list. frequency = Weekly (default) | BiWeekly | Monthly. Returns all boards of the company and locations without boards. Each board is cut into its own periods inside the view window (a monthly board in a weekly view is "clipped"). Per period: status , employeeCount , totalSlotCount , scheduledSlotCount , dayOffSlotCount , assignableSlotCount , unfilledSlotCount , unassignedAreaEmployeeCount , conflicts (over weekly cap, double booked), republishRequired , publishedAt , version ; plus totals and previous / next anchors. |
| GET ?anchor= | Grid for the period containing anchor (default today): areas → employee rows → cells ( state , isAssignable ), weekly hours vs cap, summary with isReadyToPublish , version , republishRequired . |
| POST /assign | Assign a shift or a day off. Body: slots[{employeeId, dates[]}] and either workPlanId or dayOff:true . Returns appliedSlotCount , notOnBoardEmployeeIds , outsideMembershipSlots , unresolvedEmployeeIds , periods[] , publishReverted . Errors 1301, 1104, 1906, 9001, 9002. |

| or | dayOff:true |

|  |  |



# === PAGE 20 ===

POST /clear Body: anchor? , employeeIds? , dates? .
Returns cleared and skipped-past counts. Error
1913.
POST /copy- Body: anchor? . Copies the previous period
previous into empty cells. Returns copied and skipped
counts (filled, past, outside membership,
deleted shifts, unmappable). Error 1906.
GET /export/excel? Excel file for the board's period containing
anchor=&areaIds=&t anchor (no 31-day limit). Sheets: Schedule
imeZone= (employees × days, weekly hours with over-48
h in red, totals), Shift List (one row per day ×
employee), Coverage (headcount per shift per
day plus Off, Leave, Holiday, Unfilled), Legend
(shift codes, period summary). The status line
says Published / changed since / Draft / Not
planned. timeZone only affects the time
stamps. No PDF.
Sample requests – assign a shift and a day off
1 POST /api/companies/{companyId}/roster-
boards/{boardId}/schedule/assign?locationId={locationId}
2 { "workPlanId": "sh01…", "dayOff": false,
3 "slots": [ { "employeeId": "e1…", "dates": ["2026-11-22", "2026-
11-23", "2026-11-24"] },
4 { "employeeId": "e2…", "dates": ["2026-11-22"] } ] }
5
6 POST /api/companies/{companyId}/roster-
boards/{boardId}/schedule/assign?locationId={locationId}
7 { "dayOff": true, "slots": [ { "employeeId": "e1…", "dates": ["2026-
11-27", "2026-11-28"] } ] }
8. Publishing a period
8.1 Functional steps
Action When the button shows, and what API
happens
Publish Not published and not completed. POST
Enabled only when every day of …/schedule/pub
every member is filled (shift or day lish
off); otherwise the header says "N
slots unfilled". Confirm → status
becomes Published with the publish

### TABLES ON PAGE 20

| POST /clear | Body: anchor? , employeeIds? , dates? . Returns cleared and skipped-past counts. Error 1913. |
| POST /copy- previous | Body: anchor? . Copies the previous period into empty cells. Returns copied and skipped counts (filled, past, outside membership, deleted shifts, unmappable). Error 1906. |
| GET /export/excel? anchor=&areaIds=&t imeZone= | Excel file for the board's period containing anchor (no 31-day limit). Sheets: Schedule (employees × days, weekly hours with over-48 h in red, totals), Shift List (one row per day × employee), Coverage (headcount per shift per day plus Off, Leave, Holiday, Unfilled), Legend (shift codes, period summary). The status line says Published / changed since / Draft / Not planned. timeZone only affects the time stamps. No PDF. |

| Action | When the button shows, and what happens | API |
| Publish | Not published and not completed. Enabled only when every day of every member is filled (shift or day off); otherwise the header says "N slots unfilled". Confirm → status becomes Published with the publish | POST …/schedule/pub lish |
|  |  |  |



# === PAGE 21 ===

time. If refused for unfilled days, the
dialog stays open with "N unfilled
days remain" and the rows are
highlighted.
Publish Shown when there is nothing to POST
empty roster assign and no open holiday. Sends …/schedule/pub
allowEmpty:true . lish
Republish Published period with Changes not POST
published. Same checks as Publish; …/schedule/pub
clears the flag and increases the lish
version.
Unpublish Published period. For a period that POST
has started, the dialog warns and …/schedule/unp
sends force:true ("Unpublish ublish
anyway"). The period becomes
Pending (draft) again.
8.2 Period status
Status Rule (checked in this order)
No roster day in the period and not published. The
NOT PLANNED
screen calls it "New plan".
The period has ended (even if it was never published).
COMPLETED
No buttons; cannot be published or unpublished.
PUBLISHED Published (latest version). May carry the ⚠ Changes not
published flag.
Has roster days but not published (draft).
PENDING
8.3 Business rules
A publish row is created only on the first successful publish of a (board, period).
Publish checks, in order: period over (1909; a period ending today can still be published)
→ version sent and different (1910, someone changed it) → nothing planned and no open
holiday without allowEmpty (1908) → any member day in the period, past days
included, still empty (1907).
Unpublish checks: period over (1909) → not published (1912) → period already started
and force not set (1911).

### TABLES ON PAGE 21

|  | time. If refused for unfilled days, the dialog stays open with "N unfilled days remain" and the rows are highlighted. |  |
| Publish empty roster | Shown when there is nothing to assign and no open holiday. Sends allowEmpty:true . | POST …/schedule/pub lish |
| Republish | Published period with Changes not published. Same checks as Publish; clears the flag and increases the version. | POST …/schedule/pub lish |
| Unpublish | Published period. For a period that has started, the dialog warns and sends force:true ("Unpublish anyway"). The period becomes Pending (draft) again. | POST …/schedule/unp ublish |

| Status | Rule (checked in this order) |
| NOT PLANNED | No roster day in the period and not published. The screen calls it "New plan". |
| COMPLETED | The period has ended (even if it was never published). No buttons; cannot be published or unpublished. |
| PUBLISHED | Published (latest version). May carry the ⚠ Changes not published flag. |
| PENDING | Has roster days but not published (draft). |



# === PAGE 22 ===

What publishing changes: only what employees see in self-service. A roster day in an
unpublished period shows to the employee as "Not scheduled"; in a published period it
shows the shift / day off. The Overview "Today on boards" also uses published days only.
Roster days are always stored as active, published or not.
A change to a published period does not unpublish it. It stays Published and is flagged
Changes not published:
Change Periods flagged "Changes not published"
Assign shift / day off Periods containing the dates written
Clear, Copy previous The period worked on
Edit membership period Periods between the old and new dates
Remove member, Move out From the end / effective date onward
of the board
Edit or delete a shift that From today onward
has assignments
Add employees, area Not flagged
moves, board or area
rename, frequency change
8.4 APIs – Publish
Method and path Purpose and usage
POST Body: anchor (period start), version? ,
…/schedule/publish allowEmpty . Returns status , version ,
?locationId= publishedAt , publishedBy ,
republishRequired ,
publishedSlotCount ,
publishedEmployeeCount . Errors 1907
(with unfilledSlotCount and employees),
1908, 1909, 1910.
POST Body: anchor , force . Errors 1909, 1911,
…/schedule/unpubli 1912.
sh?locationId=
Sample request – publish a week

### TABLES ON PAGE 22

| Change | Periods flagged "Changes not published" |
| Assign shift / day off | Periods containing the dates written |
| Clear, Copy previous | The period worked on |
| Edit membership period | Periods between the old and new dates |
| Remove member, Move out of the board | From the end / effective date onward |
| Edit or delete a shift that has assignments | From today onward |
| Add employees, area moves, board or area rename, frequency change | Not flagged |

| Method and path | Purpose and usage |
| POST …/schedule/publish ?locationId= | Body: anchor (period start), version? , allowEmpty . Returns status , version , publishedAt , publishedBy , republishRequired , publishedSlotCount , publishedEmployeeCount . Errors 1907 (with unfilledSlotCount and employees), 1908, 1909, 1910. |
| POST …/schedule/unpubli sh?locationId= | Body: anchor , force . Errors 1909, 1911, 1912. |

| Sample request – publish a week |
|  |



# === PAGE 23 ===

1 POST /api/companies/{companyId}/roster-
boards/{boardId}/schedule/publish?locationId={locationId}
2 { "anchor": "2026-11-22", "version": 0, "allowEmpty": false }
3 // → { "status": "Published", "version": 1, "publishedAt": "2026-11-
20T09:15:00Z",
4 // "republishRequired": false, "publishedSlotCount": 84,
"publishedEmployeeCount": 12 }
9. Overview tab
A read-only dashboard of boards, publishing and shifts. It never changes data.
9.1 Filters
Control Behaviour Sent as
Location "All Locations" plus each location; shown locationId
switch only when more than one location has
boards. Clears board and area.
Board Boards in scope. Clears area. boardId
Area Enabled after a board is chosen. areaId
Department Department list; matched by name (EN department
or AR, exact, case-insensitive).
Clear all Clears board, area and department; –
keeps the location.
Filters apply immediately, are shared with the Schedules tab and are kept when switching
tabs. The Overview sends no dates, so the APIs use the current week.
9.2 What each widget shows
Widget What the user sees API and fields
KPI tiles Employees on boards ("N boards"), GET
Periods to publish ("of N boards", overview/summar
amber when above 0), On leave this y → employees ,
week ("Leave data not available"). boardCount ,
periodsToPublis
h ,
boardsToPublish
Publishing One row per board: board (location · GET
status areas · members), supervisor, overview/publish
frequency, current period and next ing → boards[]
period with status chip and caption with current ,

### TABLES ON PAGE 23

| Control | Behaviour | Sent as |
| Location switch | "All Locations" plus each location; shown only when more than one location has boards. Clears board and area. | locationId |
| Board | Boards in scope. Clears area. | boardId |
| Area | Enabled after a board is chosen. | areaId |
| Department | Department list; matched by name (EN or AR, exact, case-insensitive). | department |
| Clear all | Clears board, area and department; keeps the location. | – |

| Widget | What the user sees | API and fields |
| KPI tiles | Employees on boards ("N boards"), Periods to publish ("of N boards", amber when above 0), On leave this week ("Leave data not available"). | GET overview/summar y → employees , boardCount , periodsToPublis h , boardsToPublish |
| Publishing status | One row per board: board (location · areas · members), supervisor, frequency, current period and next period with status chip and caption | GET overview/publish ing → boards[] with current , |
|  |  |  |

| y | → |

| ing | → | boards[] |



# === PAGE 24 ===

(planned members). View planner next ( status ,
opens the Planner. members ,
membersPlanned )
Today on Tiles: On shift now, Starting later, GET
boards Shifts ended, On leave today ("–"), overview/today
Boards not published. A 24-hour → stats ,
timeline per board with a moving groups[].rows[].
"now" line; 3 boards shown, "Show segments[] ,
all boards" for the rest. Hover: shift, nowMinute ,
members, time left, areas. Empty: isEmpty
"No shifts today".
Employee Rows = boards, columns = days, GET
schedules plus an "All published boards" total overview/week →
this week row. Cells: Not published / Pending, boards[].cells[
"N on shift · All set", "N not planned" ] ,
(orange), Holiday. Click a cell for On publishedTotals ,
shift, Day off, Not planned, Holiday, drafts
Published at. View schedules opens
the Schedules tab on this week.
Empty states: no boards and no filter → "No boards yet" with Create board; filters matching
no members → "No members for filters". Each widget has its own spinner and "Something
went wrong · Retry".
9.3 Business rules
"Today" is Riyadh time (UTC+3), fixed for every company.
Employees on boards = distinct employees whose membership overlaps the week (not
planned days).
Periods to publish = periods in the week, on boards with members, that are not published
and not over. Future periods with nothing planned are included.
Publishing status: current period = the one holding the week start; next = the one after. A
published period counts all members as planned; otherwise a member is planned when
every day of theirs in the period has a shift, day off or holiday. Boards without members are
also listed (unless area or department is filtered). Sorted Pending → Not planned →
Published → Completed, then name.
Today on boards uses only days in published periods. An overnight shift from yesterday
shows as a carry-over. Members are counted per roster day.

### TABLES ON PAGE 24

|  | (planned members). View planner opens the Planner. | next ( status , members , membersPlanned ) |
| Today on boards | Tiles: On shift now, Starting later, Shifts ended, On leave today ("–"), Boards not published. A 24-hour timeline per board with a moving "now" line; 3 boards shown, "Show all boards" for the rest. Hover: shift, members, time left, areas. Empty: "No shifts today". | GET overview/today → stats , groups[].rows[]. segments[] , nowMinute , isEmpty |
| Employee schedules this week | Rows = boards, columns = days, plus an "All published boards" total row. Cells: Not published / Pending, "N on shift · All set", "N not planned" (orange), Holiday. Click a cell for On shift, Day off, Not planned, Holiday, Published at. View schedules opens the Schedules tab on this week. | GET overview/week → boards[].cells[ ] , publishedTotals , drafts |

| next | ( | status |



# === PAGE 25 ===

Week cells: on shift = working roster days (drafts included); day off = other roster days;
not planned = members without a roster day (on a holiday it is an open holiday). The total
row adds only published periods.
Leave is not integrated: every leave field is null and shown as "–" or "Leave data not
available".
9.4 APIs – Overview
Base path: /api/companies/{companyId}/roster-boards/overview . Filters:
locationId , boardId , areaId , department (name). Range: from / to optional
(default the current Sunday–Saturday week; only from → 7 days; only to , to before
from or more than 31 days → 2204).
Method and path Purpose and usage
GET /summary? KPI tiles: boardCount ,
from=&to= boardsWithMembers , employees ,
boardsToPublish , periodsToPublish ;
leave fields null.
GET /publishing? Publishing table: per board board (areas,
from=&to= supervisor, frequency), members , current
and next period ( status , isPublished ,
members , membersPlanned , published at).
GET /today Today card (no range): stats
( onShiftNow , startingLater , ended ,
nextHandover , boardsNotPublished ),
groups per board with rows (shift, members,
segments with status), isEmpty .
GET /week? Week card: members , boards[]
from=&to= ( isPublished , cells[] with members ,
onShift , dayOff , notPlanned ,
openHoliday , period ),
publishedTotals , drafts[] ,
boardsPublished , weekLabel .
10. Schedules tab and member schedule
10.1 Functional steps
1. Open Schedules (or View schedules on the Overview). The filter bar is the same as on the
Overview; the header search box searches by name or code.

### TABLES ON PAGE 25

| Method and path | Purpose and usage |
| GET /summary? from=&to= | KPI tiles: boardCount , boardsWithMembers , employees , boardsToPublish , periodsToPublish ; leave fields null. |
| GET /publishing? from=&to= | Publishing table: per board board (areas, supervisor, frequency), members , current and next period ( status , isPublished , members , membersPlanned , published at). |
| GET /today | Today card (no range): stats ( onShiftNow , startingLater , ended , nextHandover , boardsNotPublished ), groups per board with rows (shift, members, segments with status), isEmpty . |
| GET /week? from=&to= | Week card: members , boards[] ( isPublished , cells[] with members , onShift , dayOff , notPlanned , openHoliday , period ), publishedTotals , drafts[] , boardsPublished , weekLabel . |



# === PAGE 26 ===

2. Use the week navigator (‹ › This week, Sunday–Saturday).
3. Read the grid: one block per board with its period status ("Published · 16 Oct, 14:20",
"Pending · draft, not published", "Not planned"), then one row per member (name, code ·
area) with 7 day cells. 10 members per page.
4. Hover a cell for shift, time, hours, board · area, period (published on / draft), supervisor and
holiday.
5. Click a row to open the member schedule page.
Cell dayType Shown
Shift Shift time and name; "· Draft" in amber when the
period is not published
HolidayWorked Shift on a holiday
DayOff "Day off" (also when the day off falls on a holiday)
Holiday Holiday with nothing planned
NotPlanned Member on the board, no roster day
NotOnBoard Date outside the member's period
10.2 Member schedule page
Route /attendance/Scheduler/member-schedule/{employeeId}?week=yyyy-MM-
dd . Header: name, code · location · area · reports to. Week list: one line per day (shift, day
off, holiday, not planned, other board's name when the member changed boards in the
week). Side cards: Board (supervisor, area, current / next period status, member since,
published on), Shifts this week with holidays / days off, Attendance policy per shift (grace,
break, overtime). Open board opens the Planner on that board. An employee never on a
board shows "Employee was never on a board".
10.3 Business rules
Rows are per board and member; split membership rows on one board are merged (a gap
between them shows as Not planned).
Order: board name, then employee name, then code.
Member page: the board card describes the membership covering today (else the latest in
the week, else the next, else the last). Days in the week use the board each day belongs to.
Drafts are shown on Schedules (marked Draft), unlike employee self-service.
10.4 APIs – Schedules
Method and path Purpose and usage

### TABLES ON PAGE 26

| Cell dayType | Shown |
| Shift | Shift time and name; "· Draft" in amber when the period is not published |
| HolidayWorked | Shift on a holiday |
| DayOff | "Day off" (also when the day off falls on a holiday) |
| Holiday | Holiday with nothing planned |
| NotPlanned | Member on the board, no roster day |
| NotOnBoard | Date outside the member's period |

| Method and path | Purpose and usage |
|  |  |



# === PAGE 27 ===

GET roster- Grid. Same range rules as the Overview (max
boards/schedules? 31 days, 2204). search up to 100 characters
from=&to=&search=& (code or name). page default 1; pageSize
page=&pageSize= + default 10, max 100. Returns groups[]
filters (board, periods[] , members with
cells[] : dayType , shift with times,
colour, breakMinutes , area , holiday ,
isDraft , leave = null), total ,
employees , boardCount , totalPages ,
weekLabel .
GET roster- Member page (no filters): employee , board
boards/schedules/e card ( current , next , memberSince ,
mployees/{employee memberUntil ), days[] , totals ,
Id}?from=&to= shiftsThisWeek[] , policies[] per
shift. 404 2207 when the employee was never
on a board.
11. How the Scheduler works with the other modules
1. One schedule store. Roster days, regular assignments and rotation steps are all Work
Assignment Maps in one collection (AssignmentType 1 Regular, 2 Roster, 3 Rotation).
When readers resolve an employee's day, a roster day comes first, then the rotation step,
then the regular plan with the latest start. So the Shifts & Rotation Schedules grid shows a
board employee's roster days too.
2. Shifts are work plans. A roster shift is a work plan (PlanType 2) with its own Roster
template (type 4). It uses the same workplans / worktemplates collections as Shifts
& Rotation, so codes are unique across both, and the regular work plan endpoints refuse
roster plans (1104).
3. Commitment rules (same in both modules):
Employee joins… …while already on
a roster board a regular plan → adjustable (ended early / split
on confirm; 1409 without). Another board or a
rotation → blocked (1914).
a regular plan (Shifts & a roster board or rotation → blocked (1408).
Rotation)
a rotation team (Shifts a roster board or another rotation → blocked
& Rotation) (2016).

### TABLES ON PAGE 27

| GET roster- boards/schedules? from=&to=&search=& page=&pageSize= + filters | Grid. Same range rules as the Overview (max 31 days, 2204). search up to 100 characters (code or name). page default 1; pageSize default 10, max 100. Returns groups[] (board, periods[] , members with cells[] : dayType , shift with times, colour, breakMinutes , area , holiday , isDraft , leave = null), total , employees , boardCount , totalPages , weekLabel . |
| GET roster- boards/schedules/e mployees/{employee Id}?from=&to= | Member page (no filters): employee , board card ( current , next , memberSince , memberUntil ), days[] , totals , shiftsThisWeek[] , policies[] per shift. 404 2207 when the employee was never on a board. |

| Employee joins… | …while already on |
| a roster board | a regular plan → adjustable (ended early / split on confirm; 1409 without). Another board or a rotation → blocked (1914). |
| a regular plan (Shifts & Rotation) | a roster board or rotation → blocked (1408). |
| a rotation team (Shifts & Rotation) | a roster board or another rotation → blocked (2016). |



# === PAGE 28 ===

4. Move is the bridge. A board member can be moved to another board, a regular plan or a
rotation team (Board details → Move), and a regular-plan or rotation employee can be
moved onto a board from Shifts & Rotation. The old commitment ends the day before the
effective date.
5. Current Plan column. The Add Employees picker shows each employee's current regular
plan, board or rotation ( workassignments/current-plans ).
6. Employee self-service ( me/* ) shows only published roster days; unpublished days
appear as "Not scheduled".
7. Leave is not connected to the Scheduler yet: grids never show leave, leave counts are null
/ 0, and leave does not lock cells.
12. Error codes
All errors are returned as Cit.Attendance:<code> . A failed field validation returns 400
with a validationErrors list. Some rules use the generic InvalidState error, whose
message explains the case (shift on another board, duplicate shift name, invalid segment,
remove refused, …).
Code Meaning
1901 Board has employees (any membership row, past included) –
cannot delete
1902 A board shift is scheduled today or later – cannot delete the
board
1903 Area is used by a member – cannot delete / remove it
1904 Areas cannot be switched off while members have an area
1905 Shift already has scheduled days up to today – cannot be
edited
1906 Employee has no area on a board with areas – cannot be
scheduled
1907 Period has unfilled days – cannot publish
1908 Nothing planned – publish with allowEmpty
1909 Period is over – cannot publish / unpublish
1910 Version mismatch – the schedule changed elsewhere, reload
1911 Period has started – unpublish needs force

### TABLES ON PAGE 28

| Code | Meaning |
| 1901 | Board has employees (any membership row, past included) – cannot delete |
| 1902 | A board shift is scheduled today or later – cannot delete the board |
| 1903 | Area is used by a member – cannot delete / remove it |
| 1904 | Areas cannot be switched off while members have an area |
| 1905 | Shift already has scheduled days up to today – cannot be edited |
| 1906 | Employee has no area on a board with areas – cannot be scheduled |
| 1907 | Period has unfilled days – cannot publish |
| 1908 | Nothing planned – publish with allowEmpty |
| 1909 | Period is over – cannot publish / unpublish |
| 1910 | Version mismatch – the schedule changed elsewhere, reload |
| 1911 | Period has started – unpublish needs force |

|  |  |



# === PAGE 29 ===

1912 Period is not published
1913 Clear: date outside the period
1914 Employee is on another board or a rotation for those dates
1408 / Move target refused (held by a board or rotation) / regular plan
1409 in the way, adjustment not confirmed
1101 / Template not found / type change / duplicate code / code
1105 / change / template deleted
1106 /
1107 / 1110
1203 / 20-template limit per location reached / template used by a
1206 plan
1301 / Shift (work plan) not found / shift in use, cannot delete
1304
1501 / Policy not found / inactive / type not enabled / two policies of
1506 / one type
1507 /
1508
2204 Overview / Schedules date range invalid (only to , to before
from , more than 31 days)
2207 Member schedule: employee was never on a board (404)
9001 / Record belongs to another company / location
9002
13. Points to note for testing
These come from comparing the screens with the APIs. They are current behaviour, not
confirmed requirements; raise a ticket where the behaviour looks wrong.
13.1 Screen
Supervisor list is hard-coded to a single employee ("Sayed Khan – AP004") with a fixed
id. On other tenants, board create / edit may fail or save a wrong supervisor.
Editing a shift resets its weekly pattern: the form always sends 7 identical working days,
so a shift that varied by day or had days off loses that. New shifts are always 7 working
days.

### TABLES ON PAGE 29

| 1912 | Period is not published |
| 1913 | Clear: date outside the period |
| 1914 | Employee is on another board or a rotation for those dates |
| 1408 / 1409 | Move target refused (held by a board or rotation) / regular plan in the way, adjustment not confirmed |
| 1101 / 1105 / 1106 / 1107 / 1110 | Template not found / type change / duplicate code / code change / template deleted |
| 1203 / 1206 | 20-template limit per location reached / template used by a plan |
| 1301 / 1304 | Shift (work plan) not found / shift in use, cannot delete |
| 1501 / 1506 / 1507 / 1508 | Policy not found / inactive / type not enabled / two policies of one type |
| 2204 | Overview / Schedules date range invalid (only to , to before from , more than 31 days) |
| 2207 | Member schedule: employee was never on a board (404) |
| 9001 / 9002 | Record belongs to another company / location |



# === PAGE 30 ===

Add / Edit Shift button state: choosing the colour last leaves Add disabled until another
field is touched; a policy switch on with no policy leaves Add enabled but clicking does
nothing.
Planner period is lost on refresh, on Back from shift details, on "Open board" from a
member page and on Retry: the grid always reopens on the current period.
Schedules page number is not reset when the week changes, which can give an empty
page.
Upcoming employees page shows only the first 50 members (no paging).
Add Employees always returns to the Boards tab, even when opened from the Planner
setup step or Board details. If the board is not in the cached list, employees of all locations
are listed and submit fails.
A failed conflict check looks like "all clear" on Add Employees (Add becomes enabled);
Edit period saves anyway. The server still refuses real conflicts.
Row menu limits: Remove only for Upcoming members, Move only for Active members,
nothing for Past. The API also allows ending an Active membership.
Area tab: Add Area is shown when areas are switched off; Rename has no duplicate
check, starts empty and changes only the English name.
"Copy previous week" is labelled week also on bi-weekly boards (it copies the previous
fortnight).
Not built / placeholders: Export PDF (disabled), Add Employees "Schedule" filter
(disabled), Board details checkboxes (no bulk action), Planner footer note, over-cap and
double-booking counts (not shown), Publishing status rows (not clickable), On leave (no
data).
The route /attendance/Scheduler/board-view is an old mock screen with made-up
employees; it is reachable only by typing the URL.
Browser date and time zone are used for the default start date, "today" limits, "tomorrow"
for Move, Clear's past/future split, the Schedules "This week" button and the export time
stamps. Bi-weekly periods in the setup step are worked out in the browser and may differ
from the grid's fortnight.
Two error messages for some failures (global red toast plus the screen's own message).
The member page treats any 404 as "never on a board". Planner list failures fall back
silently without status chips.
Names of boards, areas, shifts and employees always show in English, also in an Arabic
session.
Monthly is not offered in the UI, but a Monthly board (created through the API) is shown
clipped in Weekly view. "Not planned" is labelled "New plan" on chips.

# === PAGE 31 ===

Location list is loaded with isActive=No ; check whether inactive locations appear. The
employeeHierarchy API is configured only in the dev environments; check production /
UAT.
13.2 API behaviour worth checking
Assign has no date check: past days, holidays and Completed periods can be scheduled
through the API, so published history can be rewritten. Publish in turn requires past days of
the period to be filled (1907).
Publish is a flag, not a snapshot: changes after publishing are visible to employees at
once; only the "Changes not published" flag shows it.
Leave is not integrated: no cell is ever On leave, leave counts are null (Overview) or 0
(Excel), and leave never protects cells from Clear.
Shift becomes uneditable for ever (1905) once any of its days is on or before today;
delete is blocked while any future day exists.
20-template limit per location counts all template types; every roster shift uses one.
Boards with history can never be deleted: 1901 counts past membership rows, and
Remove is refused once a member has any roster day.
Frequency change leaves old publish rows; a new period starting on the same date as an
old one (for example weekly → bi-weekly) inherits its Published state.
Deleting every area leaves the board "with areas" but none defined, so every assign and
copy fails with 1906.
If shift creation fails on a policy error, the new template is left behind and holds the code
and a slot of the 20 limit. Deleting a shift's template directly returns a misleading
"Company default in use" (1007).
Two clocks: Overview and Schedules use Riyadh time; Planner, Publish and Export use
UTC. Between 00:00 and 03:00 Riyadh time they disagree on today and the current
period.
Overview counts roster days without checking membership, so a week cell's on shift +
day off can exceed members. "Periods to publish" includes future periods with nothing
planned; a past period is Completed even if never published. "Today on boards" is not
empty when only yesterday's overnight shift carries over.
Member page can show another board's roster day on a day of this board, and its policies
list can differ from "Shifts this week".
Landing counters for clipped periods (monthly board in weekly view) overstate unfilled
slots.
A board-to-board move clears the area; the employee then cannot be scheduled on an
area board until placed again (1906). Adding employees and area moves do not flag
published periods.

# === PAGE 32 ===

Conflicts are checked only within the board's location. Board names are not checked for
uniqueness and English is not required on create.
The Excel export with an area filter always drops the Unassigned band; its Leave column is
always 0.