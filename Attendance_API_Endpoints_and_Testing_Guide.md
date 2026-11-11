# Attendance 2: Comparative Analysis, Architecture & Complete API Table Directory

> **Service:** `SP.AttendanceSvc` (.NET 9 / ASP.NET Core)  

> **Release:** `dev300-1.0.2` (main branch, deployed 22–23 October 2026)  

> **DEV Base URL:** `https://attendance2.dev.zoolwork.com`  

> **Swagger UI:** `https://attendance2.dev.zoolwork.com/swagger`  

> **Primary Database:** MongoDB `Sahab` on host `10.1.0.4:27018`  

---

## Table of Contents

1. [Part 1: Comparative Analysis of the Two Test Cases Files](#part-1-comparative-analysis-of-the-two-test-cases-files)

   - [Executive Comparison Summary](#executive-comparison-summary)

   - [Tab-by-Tab Comparison Matrix](#tab-by-tab-comparison-matrix)

   - [Master Consolidated Workbook Overview](#master-consolidated-workbook-overview)

2. [Part 2: Sequential Testing Flow API Tables (Step 1 to Step 12)](#part-2-sequential-testing-flow-api-tables-step-1-to-step-12)

   - [Phase 1: Company Setup & Global Baselines (Steps 1–4)](#phase-1-company-setup--global-baselines)

   - [Phase 2A: Shifts & Rotation — Standard Scheduling (Steps 5–8)](#phase-2a-shifts--rotation--standard-scheduling)

   - [Phase 2B: Dynamic Roster Scheduler (Steps 9–11)](#phase-2b-dynamic-roster-scheduler)

   - [Phase 3: Attendance Capture & Processing Pipeline (Step 12 — Pending KT)](#phase-3-attendance-capture--processing-pipeline)

3. [Part 3: Complete API Catalog by Functional Module (All 18 Modules in Tables)](#part-3-complete-api-catalog-by-functional-module)

   - [Module 1: Work Templates (20 Endpoints)](#module-1-work-templates-20-endpoints)

   - [Module 2: Work Plans (9 Endpoints)](#module-2-work-plans-9-endpoints)

   - [Module 3: Work Assignments (13 Endpoints)](#module-3-work-assignments-13-endpoints)

   - [Module 4: Attendance Policies (9 Endpoints)](#module-4-attendance-policies-9-endpoints)

   - [Module 5: Holiday Calendars (7 Endpoints)](#module-5-holiday-calendars-7-endpoints)

   - [Module 6: Employee Exceptions & Exemptions (5 Endpoints)](#module-6-employee-exceptions--exemptions-5-endpoints)

   - [Module 7: Roster Boards (16 Endpoints)](#module-7-roster-boards-16-endpoints)

   - [Module 8: Roster Schedule Planner (8 Endpoints)](#module-8-roster-schedule-planner-8-endpoints)

   - [Module 9: Shift Rotations (17 Endpoints)](#module-9-shift-rotations-17-endpoints)

   - [Modules 10–15: Attendance Log Pipeline (47 Endpoints)](#modules-1015-attendance-log-pipeline-47-endpoints)

   - [Module 16: Self Service — My Attendance (7 Endpoints)](#module-16-self-service--my-attendance-7-endpoints)

   - [Module 17: Self Service — My Team (8 Endpoints)](#module-17-self-service--my-team-8-endpoints)

   - [Module 18: Leave Integration (1 Endpoint)](#module-18-leave-integration-1-endpoint)

   - [External Integrated Services Matrix](#external-integrated-services-matrix)

4. [Part 4: MongoDB Database Collections & Architecture (All 23 Collections)](#part-4-mongodb-database-collections--architecture)

   - [Database Conventions & Querying Rules](#database-conventions--querying-rules)

   - [Master Collections Inventory (All 23 Collections)](#master-collections-inventory-all-23-collections)

   - [Master Data Collections Detail](#master-data-collections-detail)

   - [Roster & Rotation Collections Detail](#roster--rotation-collections-detail)

   - [Attendance Log Pipeline Collections Detail](#attendance-log-pipeline-collections-detail)

   - [Shared & System Collections Detail](#shared--system-collections-detail)

   - [Collection Entity-Relationship Architecture Diagram](#collection-entity-relationship-architecture-diagram)

---

# Part 1: Comparative Analysis of the Two Test Cases Files

### Executive Comparison Summary

| Attribute | Root File (`AttendanceTestCases.xlsx`) | Document Subfolder File (`document/.../AttendanceTestCases.xlsx`) |

|---|---|---|

| **Title** | `Sahab.Attendance - Test Case Master Workbook` | `Attendance 2 - Test Cases` |

| **Owner / Origin** | QA Team (compiled from `.md` test specs) | Backend Engineering Team (`main` branch, dated 2026-10-26) |

| **Primary Scope** | **End-to-End System & Processing Pipeline**: Master setup + full Attendance Log pipeline (L1–L5) | **Deep Microservice API Foundation**: Work Templates, Plans, Roster/Rotation templates, and Assignment conflict engines |

| **Active Test Cases** | **655** test cases | **424** test cases (711 total rows with metadata & test setup) |

| **Architecture Depth** | Black-box / Functional validation | White-box / Deep API: Explicit CQRS Commands, Queries, and Handlers |

| **Known Issues** | Not tracked inline | **56 known backend issues** explicitly documented with code references |

| **Specification Engine** | Standard Excel tabular layout | Driven by an embedded JSON specification sheet (`_spec`) |

---

### Tab-by-Tab Comparison Matrix

| Functional Area | Root Tab | Root TCs | Doc Tab | Doc TCs | Key Focus & Coverage |

|---|---|:---:|---|:---:|---|

| **Work Templates (Company)** | `Work Template - Company` | 59 | `Work Template - Company` | 52 | **Root:** Layer 1 & 2 validation rules. **Doc:** CQRS commands (`CreateFixedWTCommand`), setup fixtures, 3 known issues. |

| **Work Templates (Location)** | `Work Template - Location` | 57 | `Work Template - Location` | 46 | **Doc:** Adds multi-location bulk creation and type conversion constraints (Fixed $\leftrightarrow$ Flexi $\leftrightarrow$ Split). |

| **Versioning & Roster WT** | `Work Template - Versioning` | 39 | `Work Template - Roster+Rotation` | 36 | **Root:** Rollback & version history. **Doc:** Roster (Type 4) & Rotation (Type 5) immutable templates. |

| **Holiday Calendars** | `Holiday Calendar - Company`<br>`Holiday Calendar - Location` | 47<br>27 | `Holiday Calendar - Company`<br>`Holiday Calendar - Location` | 36<br>23 | Both test fan-out and location overrides. **Doc** documents 9 known issues around publish status and route scoping. |

| **Work Plans** | `Work Plan` *(single tab)* | 70 | `Work Plan - Regular`<br>`Work Plan - Lists & Employees`<br>`Work Plan - Roster Shift` | 42<br>21<br>34 | **Doc** splits into 3 granular tabs (97 TCs total) covering roster shifts (template + plan in one payload) and location defaults. |

| **Attendance Policies** | `Policy (Break-Grace-Overtime)` | 65 | `Policy - Create & Edit`<br>`Policy - Delete, Lists & Usage` | 32<br>18 | **Doc** splits into 2 tabs (50 TCs total), testing the 30-policy company cap and embedded policy snapshots. |

| **Work Assignments** | `Work Assignment (+ Map)` | 65 | `Work Assignment - Assign`<br>`Work Assignment - Edit & Move`<br>`Work Assignment - Queries` | 34<br>30<br>20 | **Doc** splits into 3 tabs (84 TCs total) covering conflict preview (`check-conflicts`), auto-adjusting overlaps, and moves. |

| **Attendance Log: Upload** | `Att Log - Upload & Import` | 36 | *Not present* | — | **Unique to Root:** Tests CSV upload, session generation, file validation, and tenancy checks. |

| **Attendance Log: Finalise** | `Att Log - Processing Finalise` | 19 | *Not present* | — | **Unique to Root:** Tests finalizing daily logs and state transitions. |

| **Attendance Log: Edits** | `Att Log - Edit & Refinalise` | 99 | *Not present* | — | **Unique to Root:** Tests manual edits, regularization, holiday overrides, and clearing changes. |

| **Attendance Log: Issues** | `Att Log - Issues` | 23 | *Not present* | — | **Unique to Root:** Tests blockers, unmapped punches, missing shifts, and issue export. |

| **Attendance Log: L4/L5** | `Att Log - L4-L5 Data` | 19 | *Not present* | — | **Unique to Root:** Tests monthly summary calculations (worked hours, late/early deductions) and payroll outputs. |

| **Attendance Exemptions** | `Attendance Config (Exemptions)` | 30 | *Not present* | — | **Unique to Root:** Tests employee attendance exemption date ranges and rules. |

| **JSON Spec Engine** | *Not present* | — | `_spec` | *(JSON)* | **Unique to Doc:** Complete programmatic schema definitions driving the workbook. |

| **TOTALS** | **14 Test Sheets** | **655** | **13 Test Sheets** | **424** | **Root = Broader pipeline coverage; Doc = Deeper Attendance 2 core API coverage.** |

---

### Master Consolidated Workbook Overview

* **Consolidated File:** `AttendanceTestCases_Master_Consolidated.xlsx` (Created clean; existing baseline sheets remain 100% untouched).

* **Total Tests:** **1,516 test cases** across **17 structured tabs**:

  - `INDEX` Dashboard with auto-counters across all 16 modules.

  - `User Scenarios (Add Here)` dedicated custom scenarios tab (127 TCs).

  - 10 Active Master Setup & Scheduling tabs (Blue & Green), including `Holiday Calendar - Test Cases` (310 TCs).

  - 5 Attendance Log processing tabs (Rose, tagged with `(KT)` as deferred).

  - Priority Breakdown: **P0: 659** | **P1: 647** | **P2: 197** | **P3: 13**.

---

# Part 2: Sequential Testing Flow API Tables (Step 1 to Step 12)

Every API endpoint mapped in the exact order of the verified testing flow.

---

## Phase 1: Company Setup & Global Baselines

### Step 1: Create Company & Active Locations (Prerequisite)

* **Goal:** Verify that the Company and its Work Locations exist and are active prior to CDWT creation.

* **Microservices:** **Company Service** (`company8.dev.zoolwork.com`) & **Identity Server** (`auth8.dev.zoolwork.com`)

| Step | Method | Service (`svc`) | Full Endpoint URL | Query / Route Params | Request Body / Payload | Expected Response & HTTP Code | MongoDB Collection |

|---|:---:|---|---|---|---|---|---|

| **1.1** | `POST` | **Identity Server** | `https://auth8.dev.zoolwork.com/connect/token` | None | `grant_type=client_credentials`<br>`&client_id={id}`<br>`&client_secret={sec}` | **HTTP 200**: Returns JWT `Bearer <token>` with tenant claim | — |

| **1.2** | `GET` | **Company Svc** | `https://company8.dev.zoolwork.com/api/company/companies` | None | None | **HTTP 200**: Returns company list; confirms `{companyId}` | `Sahab.Companies` |

| **1.3** | `GET` | **Company Svc** | `https://company8.dev.zoolwork.com/api/company/worklocations/companyWorkLocationList` | `?companyId={companyId}` | None | **HTTP 200**: Confirms active locations exist (prerequisite for cascade) | `Sahab.WorkLocations` |

| **1.4** | `GET` | **Company Svc** | `https://company8.dev.zoolwork.com/api/company/{companyId}/holidaytypes` | `{companyId}` | None | **HTTP 200**: Returns valid holiday types (`Public Holiday`, etc.) | `Sahab.HolidayTypes` |

---

### Step 2: Company Default Work Template (CDWT) & Lifecycle Evolution

* **Goal:** Define the company-wide standard working schedule. Trigger automatic creation of location default templates and default plans (`LOCWOPL`). Support multi-version lifecycle across Fixed, Flexible Daily, Flexible Weekly, and Split shifts.

* **Microservice:** **`SP.AttendanceSvc`** (`attendance2.dev.zoolwork.com`)

| Step | Method | Service (`svc`) | Full Endpoint URL | Query / Route Params | Request Body / Payload | Expected Response & HTTP Code | MongoDB Collection |

|---|:---:|---|---|---|---|---|---|

| **2.1** | `POST` | **Attendance 2** | `/api/companies/{companyId}/worktemplates/fixed` | *(No `locationId`)* | `templateName: {"en":"Attendance 1"}`<br>`shortCode: "ATTEDQA"`<br>`fixedTimeSlots: [...]` | **HTTP 201**: CDWT created (`Version: "1.0"`, `IsDefault: true`). **Auto-provisions** Location Default WT and Default Plan (`LOCWOPL`) for each location. | `ERP.Attendance.WorkTemplates`<br>`ERP.Attendance.WorkPlans`<br>*(Cross-Svc: `CompanyMaster`)* |

| **2.2** | `POST` | **Attendance 2** | `/api/companies/{companyId}/worktemplates/flexi` | *(Alternative: Flexi Initial)* | `flexibleType: "Daily"` (or `"Weekly"`)<br>`totalWorkDurationInMinutes: 3240` | **HTTP 201**: Creates Flexi Company Default directly as Version 1.0. | `ERP.Attendance.WorkTemplates` |

| **2.3** | `POST` | **Attendance 2** | `/api/companies/{companyId}/worktemplates/split` | *(Alternative: Split Initial)* | `splitTimeSlots: [...]` | **HTTP 201**: Creates Split Company Default directly as Version 1.0. | `ERP.Attendance.WorkTemplates` |

> [!WARNING] Critical Rule: First-Time Setup Lockout (POST vs. PATCH)

> - **`POST` is EXCLUSIVELY for first-time setup** when no default template exists for the company.

> - Once a default work template exists (`IsDefault: true`), calling `POST /fixed`, `POST /flexi`, or `POST /split` will immediately throw **`HTTP 409 Conflict`** (*"A default work template already exists for this company. Please use PATCH to update or switch template types."*).

> - **To switch template types or update timings, ALWAYS use `PATCH`!**

> [!CAUTION] Critical Header Trap: First-Time Setup Lockout with Location Headers

> - **Do NOT pass `LocationId` or `X-Location-Id` in HTTP Request Headers** when creating the Company Default Work Template (`POST /fixed`, `POST /flexi`, or `POST /split`).

> - If an active `LocationId` is passed in headers when CDWT is not yet configured:

>   - The backend binds the request as a **Location Template creation**.

>   - Because CDWT does not exist yet, the system **STRICTLY BLOCKS CREATION** and throws **`HTTP 400 Bad Request: Cit.Attendance:1205 ('Company default is not available.')`**.

>   - This lockout applies uniformly across **Fixed**, **Flexible**, and **Split Shift** templates!

>   - **Rule:** CDWT creation MUST have `LocationId = 00000000-0000-0000-0000-000000000000` with headers and query strictly free of location identifiers.

> [!WARNING] Critical Cross-Service Integration & Known Defect (`USER-01`)

> * **Expected Behavior:** Upon successful creation of the Company Default Work Schedule, Attendance Service must notify **Company Service** (`SP.CompanySvc`), which must update the company master profile:  

>   `CompanyMaster` collection $\rightarrow$ `CompanyChecklist.WorkSchedulesCreated = true`.

> * **Current Defect Status (Reported by QA):** `CompanyChecklist.WorkSchedulesCreated` remains `false`. The checklist flag is not updated, causing onboarding/setup validation to report incomplete work schedule setup.

#### Subsequent Edits, Shift Type Switching & Version Progression:

| Step | Method | Service (`svc`) | Full Endpoint URL | Query / Route Params | Request Body / Payload | Expected Response & HTTP Code | MongoDB Collection |

|---|:---:|---|---|---|---|---|---|

| **2.4** | `PATCH` | **Attendance 2** | `/api/companies/{companyId}/worktemplates/flexi/{id}` | `{id}` *(No `locationId`)* | `flexibleType: "Daily"`<br>`totalWorkDurationInMinutes: 3240`<br>`flexiTimeSlots: [9h per day]` | **HTTP 200**: Staged edit creates **Version 2.0** (`_id: 23791f16-...`). Marks v1.0 `IsSuperseded: true`. Sets `ChangeLog` (`Fixed -> Flexible`, `6h -> 54h`). Sets `HasPendingLocSync = true`. | `ERP.Attendance.WorkTemplates` |

| **2.5** | `PATCH` | **Attendance 2** | `/api/companies/{companyId}/worktemplates/flexi/{id}` | `{id}` *(No `locationId`)* | `flexibleType: "Weekly"`<br>`totalWorkDurationInMinutes: 3240`<br>`flexiTimeSlots: [days only]` | **HTTP 200**: Staged edit creates **Version 3.0** (`_id: 718b74a7-...`). Marks v2.0 `IsSuperseded: true`. Stores `FlexibleType: 2`. Sets `ChangeLog` (`ChangeType: 8` "Updated"). Sets `HasPendingLocSync = true`. | `ERP.Attendance.WorkTemplates` |

| **2.6** | `PATCH` | **Attendance 2** | `/api/companies/{companyId}/worktemplates/split/{id}` | `{id}` *(No `locationId`)* | `splitTimeSlots: [2 intervals/day]`<br>`totalWorkDurationInMinutes: 2880` | **HTTP 200**: Staged edit creates **Version 4.0** (`_id: 6bc32276-...`). Marks v3.0 `IsSuperseded: true`. Stores `TemplateType: 3` (Split). Captures ChangeLog: [Work Type: Flexible → Split, Timings Changed, Weekly hours: 54h → 48h]. Sets `HasPendingLocSync = true`. | `ERP.Attendance.WorkTemplates` |

| **2.7** | `GET` | **Attendance 2** | `/api/companies/{companyId}/worktemplates/company-default/sync-status` | None | None | **HTTP 200**: Returns `{ hasPendingLocSync: true }` when CDWT has unsynced major versions. | `ERP.Attendance.WorkTemplates` |

| **2.8** | `POST` | **Attendance 2** | `/api/companies/{companyId}/worktemplates/apply-sync` | None | None | **HTTP 200**: Pushes active version down to all inheriting location templates. Sets `HasPendingLocSync = false`. | `ERP.Attendance.WorkTemplates` |

| **2.9** | `GET` | **Attendance 2** | `/api/companies/{companyId}/worktemplates/company-default/versions` | None | None | **HTTP 200**: Returns full version chain descending: `[v3.0 (isCurrent: true), v2.0 (isCurrent: false), v1.0 (isCurrent: false)]`. | `ERP.Attendance.WorkTemplates` |

> [!IMPORTANT] Architectural Distinction: Immutable Versioning vs. In-Place Mutation

> - **Company Default (`LocationId == 000...000`):** Always uses **Immutable Versioning**. Every PATCH creates a brand new MongoDB document with an incremented major version number (`1.0` $\rightarrow$ `2.0` $\rightarrow$ `3.0`), archives the prior document, and tracks all delta messages in `ChangeLog`.

> - **Location Work Template (`LocationId != 000...000`):** Always modifies the **exact same MongoDB document in-place**. The `_id` is retained, no new documents are created, and `Version` remains `1.0`.

---

### Step 3: Company Holiday Calendar & Publishing Lifecycle

* **Goal:** Create public holidays per year across 5 enum types. Enforce From Date Only mandatory rule. Stage changes, validate Work Template & compulsory $\ge 1$ holiday prerequisites, publish to overwrite inheriting locations, synchronize Company Service checklist, handle post-publish mutations, and re-publish round 2.

* **Microservices:** **`SP.AttendanceSvc`** (Port 5001 / Dev: `attendance2.dev.zoolwork.com`) & **`SP.CompanySvc`** (Port 5000 / Dev: `company8.dev.zoolwork.com`)

#### Key Business & Validation Rules:

1. **5 Holiday Types Dropdown:** `Public Holiday` (1), `Religious Holiday` (2), `National Holiday` (3), `Bank Holiday` (4), `Gazette Holiday` (5).

2. **From Date Only Rule:** Only `StartDate` is mandatory. If `EndDate` is null or omitted, backend auto-assigns `EndDate = StartDate` and `TotalDays = 1`.

3. **End Date Boundary:** If `EndDate < StartDate`, backend rejects with HTTP 400 Bad Request, code `Cit.Attendance:1705`.

4. **Publishing Prerequisites:**

   - **Compulsory $\ge 1$ Holiday:** Cannot publish empty list (`holidayLists: []`). Rejects with HTTP 400 Bad Request, code `Cit.Attendance:1704`.

   - **Mandatory Work Template:** Company Default Work Template (CDWT) must exist and be active before publishing holidays.

5. **Pre-Publish Staging:** `POST /holidaylist`, `PATCH /holidaylist/{id}/{year}` (Add/Edit), and `PATCH /remove/{holidayId}` update company default in staged mode (`IsPublished = false`). Inherited locations are NOT touched until published.

6. **Publish Execution:** `POST /publish/{year}` sets `IsPublished = true`, sets `LastPublishedOn = UTC now`, overwrites all active locations where `IsInherited == true`, and updates Company Service `CompaniesMaster.CompanyChecklist.HolidayCalendarPublished = true`.

7. **Post-Publish Mutations & Re-Publish (Round 2):** Any addition, edit, or removal after initial publish reverts `IsPublished = false` (Unpublished Changes flag). Re-publishing (`POST /publish/{year}`) re-syncs round-2 changes to inheriting locations and refreshes Company Service status.

8. **Location Isolation:** Detached locations (`IsInherited = false`) remain 100% immune across initial publish and all subsequent re-publish rounds.

| Step | Method | Service (`svc`) | Full Endpoint URL | Query / Route Params | Request Body / Payload | Expected Response & HTTP Code | Target DB & Field Updates |

|---|:---:|---|---|---|---|---|---|

| **3.1** | `POST` | **Attendance 2** | `/api/companies/{companyId}/holidaylist` | *(No `locationId`)* | `shortCode: "HC-2026"`<br>`yearlyCalendar: {year: 2026, holidayLists: [...]}` | **HTTP 200**: Creates Company Default (`CalendarType: 1`, `IsPublished: false`). **Auto-fans out** read-only inherited copies (`IsInherited: true`) to all active locations. | `ERP.Attendance.HolidayCalendars`<br>`IsPublished: false` |

| **3.2** | `PATCH` | **Attendance 2** | `/api/companies/{companyId}/holidaylist/{id}/{year}` | `{id}`, `{year}` | Modified `holidayLists` (Add or Edit) | **HTTP 200**: Staged edit: sets `IsPublished = false`. Locations are untouched until publish. | `ERP.Attendance.HolidayCalendars`<br>`IsPublished: false` |

| **3.3** | `PATCH` | **Attendance 2** | `/api/companies/{companyId}/holidaylist/{id}/remove/{holidayId}/{year}` | `{id}`, `{holidayId}`, `{year}` | None | **HTTP 200**: Removes holiday from staged list; `IsPublished = false`. Past holidays rejected (`1709`). | `ERP.Attendance.HolidayCalendars`<br>`Pull from HolidayLists` |

| **3.4** | `POST` | **Attendance 2** | `/api/companies/{companyId}/holidaylist/publish/{year}` | `{year}` | None | **HTTP 200**: **Publish:** Validates CDWT + list $\ge 1$. Overwrites inheriting locations (`IsInherited: true`). Sets `LastPublishedOn`. | Attendance: `IsPublished: true`<br>Company Svc: `CompanyChecklist` sync |

| **3.5** | `PATCH` | **Attendance 2** | `/api/companies/{companyId}/holidaylist/{locationCalendarId}/customise` | `{locationCalendarId}` | None | **HTTP 200**: **Customise (Detach):** Sets `IsInherited = false`. Protects location from future company publishes. | `ERP.Attendance.HolidayCalendars`<br>`IsInherited: false` |

| **3.6** | `GET` | **Attendance 2** | `/api/companies/{companyId}/holidaylist/{year}` | `?locationId={locId}` | None | **HTTP 200**: Returns active calendar applicable to location. Confirms `isPublished` state. | `ERP.Attendance.HolidayCalendars` |

| **3.7** | `GET` | **Attendance 2** | `/api/companies/{companyId}/holidaylist/{id}` | `{id}` | None | **HTTP 200**: Returns specific holiday calendar document details. | `ERP.Attendance.HolidayCalendars` |

| **3.8** | `POST` | **Attendance 2** | `/api/companies/{companyId}/holidaylist/publish/{year}` | `{year}` | None | **HTTP 200**: **Re-Publish (Round 2):** Syncs post-publish additions, edits, and removals to locations. | Attendance & Company Svc |

---

### Step 4: Policy Library Configuration (Grace Period, Overtime, Break)

* **Goal:** Centrally configure policies (max 30 total). Must be configured before creating work plans.

* **Microservice:** **`SP.AttendanceSvc`**

| Step | Method | Service (`svc`) | Full Endpoint URL | Query / Route Params | Request Body / Payload | Expected Response & HTTP Code | MongoDB Collection |

|---|:---:|---|---|---|---|---|---|

| **4.1** | `POST` | **Attendance 2** | `/api/companies/{companyId}/attpolicies/graceperiod` | None | `name: {"en":"Grace 15m"}`<br>`lateCheckInGraceMinutes: 15`<br>`earlyCheckOutGraceMinutes: 10`<br>`deviationPeriod: 3`<br>`deductLeaveFrom: 1` | **HTTP 200**: Creates Grace Period Policy (`Type: 3`). Validates company cap ($\le 30$) and duplicate configs. | `ERP.Attendance.Policies` |

| **4.2** | `POST` | **Attendance 2** | `/api/companies/{companyId}/attpolicies/overtime` | None | `name: {"en":"OT Std"}`<br>`overtimeRule: 1`<br>`dayRates: [{dayRateType: 1, multiplier: 1.5}]` | **HTTP 200**: Creates Overtime Policy (`Type: 2`) | `ERP.Attendance.Policies` |

| **4.3** | `POST` | **Attendance 2** | `/api/companies/{companyId}/attpolicies/break` | None | `name: {"en":"Lunch 1h"}`<br>`breakType: 1` (Paid)<br>`breakDurationInMinutes: 60` | **HTTP 200**: Creates Break Policy (`Type: 1`) | `ERP.Attendance.Policies` |

| **4.4** | `GET` | **Attendance 2** | `/api/companies/{companyId}/attpolicies` | `?state=active&type=graceperiod` | None | **HTTP 200**: Lists active policies available to attach to plans | `ERP.Attendance.Policies` |

| **4.5** | `PATCH` | **Attendance 2** | `/api/companies/{companyId}/attpolicies/{policyId}/delete` | `{policyId}` | None | **HTTP 200**: Soft delete (`IsActive = false`). Does not break plans holding snapshots. | `ERP.Attendance.Policies` |

---

## Phase 2A: Shifts & Rotation — Standard Scheduling

### Step 5: Regular Location Shift Templates

* **Goal:** Create location-specific shift timings with unique 7-character short codes.

* **Microservice:** **`SP.AttendanceSvc`**

| Step | Method | Service (`svc`) | Full Endpoint URL | Query / Route Params | Request Body / Payload | Expected Response & HTTP Code | MongoDB Collection |

|---|:---:|---|---|---|---|---|---|

| **5.1** | `GET` | **Attendance 2** | `/api/companies/{companyId}/worktemplates/short-code/availability` | `?code=MORN001` | None | **HTTP 200**: Returns `{ isAvailable: true }` | `ERP.Attendance.WorkTemplates` |

| **5.2** | `POST` | **Attendance 2** | `/api/companies/{companyId}/worktemplates/fixed` | `?locationId={locId}` | `templateName: {"en":"Morning 8-4"}`<br>`shortCode: "MORN001"`<br>`fixedTimeSlots: [...]` | **HTTP 200**: Creates location Fixed template (`LocationId: {locId}`) | `ERP.Attendance.WorkTemplates` |

| **5.3** | `PATCH` | **Attendance 2** | `/api/companies/{companyId}/worktemplates/fixed/{id}` | `{id}?locationId={locId}` | Updated timing slots | **HTTP 200**: Updates template timings | `ERP.Attendance.WorkTemplates` |

| **5.4** | `PATCH` | **Attendance 2** | `/api/companies/{companyId}/worktemplates/{id}/archive` | `{id}?locationId={locId}` | None | **HTTP 200**: Archives template (rejected if plan is using it) | `ERP.Attendance.WorkTemplates` |

---

### Step 6: Rotation Shift Templates (Cyclical 7-Day Templates)

* **Goal:** Create 7-day fixed-shaped templates for shift rotation cycles.

* **Microservice:** **`SP.AttendanceSvc`**

| Step | Method | Service (`svc`) | Full Endpoint URL | Query / Route Params | Request Body / Payload | Expected Response & HTTP Code | MongoDB Collection |

|---|:---:|---|---|---|---|---|---|

| **6.1** | `POST` | **Attendance 2** | `/api/companies/{companyId}/worktemplates/rotation` | `?locationId={locId}` | `templateName: {"en":"Rot Wk A"}`<br>`shortCode: "ROTA001"`<br>`rotationTimeSlots: [...]` | **HTTP 200**: Creates Rotation Template (`TemplateType: 5`). Requires all 7 days. Type is **immutable**. | `ERP.Attendance.WorkTemplates` |

| **6.2** | `GET` | **Attendance 2** | `/api/companies/{companyId}/worktemplates` | `?locationId={locId}&templateType=Rotation` | None | **HTTP 200**: Lists rotation templates for location | `ERP.Attendance.WorkTemplates` |

---

### Step 7: Regular Work Plans & Employee Assignments

* **Goal:** Package templates with policy snapshots. Assign employees, check conflicts, and auto-adjust.

* **Microservices:** **`SP.AttendanceSvc`** & **Org Hierarchy Service**

| Step | Method | Service (`svc`) | Full Endpoint URL | Query / Route Params | Request Body / Payload | Expected Response & HTTP Code | MongoDB Collection |

|---|:---:|---|---|---|---|---|---|

| **7.1** | `POST` | **Attendance 2** | `/api/companies/{companyId}/workplans` | `?locationId={locId}` | `workPlanName: {"en":"HQ Plan"}`<br>`workTemplateId: "{templateId}"`<br>`policyIds: ["{graceId}","{otId}"]` | **HTTP 200**: Creates Work Plan. Embeds **immutable snapshot** of template and policies. | `ERP.Attendance.WorkPlans` |

| **7.2** | `POST` | **Attendance 2** | `/api/companies/{companyId}/workassignments/check-conflicts` | `?locationId={locId}` | `workPlanId`, `employeeIds: [...]`, `startDate`, `endDate` | **HTTP 200**: Conflict preview (`conflicts: []`, `canProceed: true/false`) | `ERP.Attendance.WorkAssignmentMaps` |

| **7.3** | `POST` | **Attendance 2** | `/api/companies/{companyId}/workassignments` | `?locationId={locId}` | `workPlanId`, `employeeIds: [...]`, `startDate`, `endDate` | **HTTP 200**: Creates Header (`WorkAssignments`) and rows (`WorkAssignmentMaps`) | `ERP.Attendance.WorkAssignments`<br>`ERP.Attendance.WorkAssignmentMaps` |

| **7.4** | `POST` | **Attendance 2** | `/api/companies/{companyId}/workassignments/adjust` | `?locationId={locId}` | `workPlanId`, `employeeIds: [...]`, `startDate`, `endDate` | **HTTP 200**: Assigns and **auto-splits/shortens** overlapping dates | `ERP.Attendance.WorkAssignmentMaps` |

| **7.5** | `GET` | **Attendance 2** | `/api/companies/{companyId}/workassignments/current-plans` | `?locationId={locId}&asOf=2026-11-01` | None | **HTTP 200**: Returns active plan for every employee as of date | `ERP.Attendance.WorkAssignmentMaps` |

| **7.6** | `PATCH` | **Attendance 2** | `/api/companies/{companyId}/workassignments/details/{id}/move` | `{id}?locationId={locId}` | `targetPlanId`, `effectiveFrom` | **HTTP 200**: Moves employee to another work plan | `ERP.Attendance.WorkAssignmentMaps` |

---

### Step 8: Rotation Work Plans & Team Enrolment

* **Goal:** Create cyclical rotation boards, configure steps, and generate concrete employee schedules.

* **Microservice:** **`SP.AttendanceSvc`**

| Step | Method | Service (`svc`) | Full Endpoint URL | Query / Route Params | Request Body / Payload | Expected Response & HTTP Code | MongoDB Collection |

|---|:---:|---|---|---|---|---|---|

| **8.1** | `POST` | **Attendance 2** | `/api/companies/{companyId}/shift-rotations` | None | `rotationName: {"en":"Ops 2-Shift"}`<br>`locationId`, `patternType: 1`<br>`weeksPerStep: 2`, `plans: [...]` | **HTTP 200**: Creates Rotation Board with cyclical steps (2 wks Day $\rightarrow$ 2 wks Night) | `ERP.Attendance.ShiftRotationBoard` |

| **8.2** | `POST` | **Attendance 2** | `/api/companies/{companyId}/shift-rotations/{id}/preview` | `{id}` | `startDate: "2026-11-01"`, `weeksCount: 8` | **HTTP 200**: Previews rotational pattern matrix | `ERP.Attendance.ShiftRotationBoard` |

| **8.3** | `POST` | **Attendance 2** | `/api/companies/{companyId}/shift-rotations/{id}/enrol` | `{id}` | `teamId`, `employeeIds: [...]`, `startStepIndex: 1` | **HTTP 200**: Enrolls employees into rotation teams | `ERP.Attendance.ShiftRotationBoard` |

| **8.4** | `POST` | **Attendance 2** | `/api/companies/{companyId}/shift-rotations/{id}/generate-schedule` | `{id}` | `fromDate: "2026-11-01"`, `toDate: "2026-12-31"` | **HTTP 200**: Generates concrete date assignment rows in database | `ERP.Attendance.WorkAssignmentMaps` |

---

## Phase 2B: Dynamic Roster Scheduler

### Step 9: Schedule Shift Template (Roster Shifts)

* **Goal:** Define roster shifts with start/end time, hex color, and overnight shift auto-detection.

* **Microservice:** **`SP.AttendanceSvc`**

| Step | Method | Service (`svc`) | Full Endpoint URL | Query / Route Params | Request Body / Payload | Expected Response & HTTP Code | MongoDB Collection |

|---|:---:|---|---|---|---|---|---|

| **9.1** | `POST` | **Attendance 2** | `/api/companies/{companyId}/workplans/roster` | `?locationId={locId}` | `workPlanName: {"en":"Morning Shift"}`<br>`shortCode: "RST-M01"`<br>`startTime: "07:00:00"`, `endTime: "15:30:00"`<br>`colour: "#3B82F6"`, `boardId: "{id}"` | **HTTP 200**: Single call provisions both `RosterWorkTemplate` and `RosterWorkPlan`. Auto-detects overnight if `EndTime < StartTime`. | `ERP.Attendance.WorkTemplates`<br>`ERP.Attendance.WorkPlans` |

| **9.2** | `PATCH` | **Attendance 2** | `/api/companies/{companyId}/workplans/roster/{id}` | `{id}?locationId={locId}` | Updated timing or hex color | **HTTP 200**: Updates both template and plan halves | `ERP.Attendance.WorkPlans` |

---

### Step 10: Create Schedule Board & Configure Areas

* **Goal:** Create a roster planning unit, define working areas (e.g. Ramp, Gate), and enroll member employees.

* **Microservices:** **`SP.AttendanceSvc`** & **Org Hierarchy Service**

| Step | Method | Service (`svc`) | Full Endpoint URL | Query / Route Params | Request Body / Payload | Expected Response & HTTP Code | MongoDB Collection |

|---|:---:|---|---|---|---|---|---|

| **10.1** | `POST` | **Attendance 2** | `/api/companies/{companyId}/roster-boards` | None | `boardName: {"en":"Airport Ground Ops"}`<br>`locationId`, `description` | **HTTP 200**: Creates Roster Board header | `ERP.Attendance.RosterBoards` |

| **10.2** | `POST` | **Attendance 2** | `/api/companies/{companyId}/roster-boards/{id}/areas` | `{id}` | `areaName: {"en":"Gate 14 Ramp Area"}` | **HTTP 200**: Adds physical working area | `ERP.Attendance.RosterBoards` |

| **10.3** | `POST` | **Attendance 2** | `/api/companies/{companyId}/roster-boards/{id}/shifts` | `{id}` | `shiftIds: ["{rosterShift1Id}", "{rosterShift2Id}"]` | **HTTP 200**: Links shifts from Step 9 to this board | `ERP.Attendance.RosterBoards` |

| **10.4** | `POST` | **Attendance 2** | `/api/companies/{companyId}/roster-boards/{id}/members` | `{id}` | `employeeIds: ["{emp1}", "{emp2}"]` | **HTTP 200**: Enrolls employees as active board members | `ERP.Attendance.EmployeeRosterAssignments` |

---

### Step 11: Schedule Plan (Roster Planner Grid & Publishing)

* **Goal:** Populate the monthly planner grid, copy schedules, and publish periods for attendance matching.

* **Microservice:** **`SP.AttendanceSvc`**

| Step | Method | Service (`svc`) | Full Endpoint URL | Query / Route Params | Request Body / Payload | Expected Response & HTTP Code | MongoDB Collection |

|---|:---:|---|---|---|---|---|---|

| **11.1** | `GET` | **Attendance 2** | `/api/companies/{companyId}/roster-boards/{boardId}/schedule/grid` | `?startDate=2026-11-16&endDate=2026-12-15` | None | **HTTP 200**: Returns Planner Grid (Employees $\times$ Dates) with assigned shifts & Day Offs | `ERP.Attendance.WorkAssignmentMaps` |

| **11.2** | `POST` | **Attendance 2** | `/api/companies/{companyId}/roster-boards/{boardId}/schedule/assign` | None | `employeeId`, `date: "2026-11-17"`<br>`shiftId`, `areaId`, `isDayOff: false` | **HTTP 200**: Assigns shift/Day Off to a cell | `ERP.Attendance.WorkAssignmentMaps` |

| **11.3** | `POST` | **Attendance 2** | `/api/companies/{companyId}/roster-boards/{boardId}/schedule/copy-previous` | None | `sourcePeriodId`, `targetStartDate`, `targetEndDate` | **HTTP 200**: Clones entire schedule from previous pay period | `ERP.Attendance.WorkAssignmentMaps` |

| **11.4** | `POST` | **Attendance 2** | `/api/companies/{companyId}/roster-boards/{boardId}/schedule/publish` | None | `boardId`, `periodStart: "2026-11-16"`, `periodEnd: "2026-12-15"` | **HTTP 200**: **Publish:** Locks period (`IsPublished = true`). Generates live assignment records. | `ERP.Attendance.RosterSchedulePeriods` |

| **11.5** | `GET` | **Attendance 2** | `/api/companies/{companyId}/roster-boards/{boardId}/schedule/export` | `?periodId={periodId}` | None | **HTTP 200**: Downloads formatted Excel roster schedule (`.xlsx`) | — |

---

## Phase 3: Attendance Capture & Processing Pipeline

> **Note for QA:** Testing of this phase is currently **deferred** pending completion of Knowledge Transfer (KT). The table below documents the full pipeline sequence.

### Step 12: Monthly Attendance Processing Pipeline (Upload $\rightarrow$ Process $\rightarrow$ Edit $\rightarrow$ L4/L5)

* **Goal:** Import monthly biometric punches (L3), reconcile against assigned schedules, resolve blockers, and finalize.

* **Microservice:** **`SP.AttendanceSvc`**

| Step | Method | Service (`svc`) | Full Endpoint URL | Query / Route Params | Request Body / Payload | Expected Response & HTTP Code | MongoDB Collection |

|---|:---:|---|---|---|---|---|---|

| **12.1** | `POST` | **Attendance 2** | `/api/companies/{companyId}/att-log/uploadfile` | None | Multipart form-data: `.csv` file, `periodStart`, `periodEnd`, `payGroupId`, `locationId` | **HTTP 200**: Uploads raw CSV file into MongoDB GridFS (`fs.files`) | `fs.files`<br>`ERP.Attendance.Log.AttGlobalSessionMaster` |

| **12.2** | `POST` | **Attendance 2** | `/api/companies/{companyId}/att-log/data-import/{sessionId}` | `{sessionId}` | None | **HTTP 200**: Parses CSV and writes rows into `DailyProcessedL3` | `ERP.Attendance.Log.DailyProcessedL3` |

| **12.3** | `GET` | **Attendance 2** | `/api/companies/{companyId}/att-log/sessions/{sessionId}/grid` | `?page=1&pageSize=50` | None | **HTTP 200**: Renders interactive daily timecard grid | `ERP.Attendance.Log.DailyProcessedL3` |

| **12.4** | `GET` | **Attendance 2** | `/api/companies/{companyId}/att-log/blockers` | `?sessionId={sessionId}` | None | **HTTP 200**: Checks blocking errors preventing finalization | `ERP.Attendance.Log.Errors` |

| **12.5** | `PATCH` | **Attendance 2** | `/api/companies/{companyId}/att-log/L3/{rowId}/override-checkinout` | `{rowId}` | `entryTime: "08:15:00"`, `exitTime: "17:30:00"`, `reason` | **HTTP 200**: Corrects daily punches; recalculates shortfall and overtime | `ERP.Attendance.Log.DailyProcessedL3` |

| **12.6** | `PATCH` | **Attendance 2** | `/api/companies/{companyId}/att-log/L3/{rowId}/regularize` | `{rowId}` | `reason: "Approved onsite duty"` | **HTTP 200**: Regularizes absent day or shortfall hours | `ERP.Attendance.Log.DailyProcessedL3` |

| **12.7** | `PATCH` | **Attendance 2** | `/api/companies/{companyId}/att-log/L3/{rowId}/mark-holiday` | `{rowId}` | `reason: "Declared holiday"` | **HTTP 200**: Reclassifies day to Holiday; clears deductions | `ERP.Attendance.Log.DailyProcessedL3` |

| **12.8** | `POST` | **Attendance 2** | `/api/companies/{companyId}/att-log/start-process/{sessionKey}` | `{sessionKey}` | None | **HTTP 200**: **Finalise:** Aggregates L3 rows into **L4 Monthly Summary** | `ERP.Attendance.Log.MonthlyLogL4` |

| **12.9** | `GET` | **Attendance 2** | `/api/companies/{companyId}/att-log/L4/{sessionKey}` | `?employeeCode=EMP-0001` | None | **HTTP 200**: Returns worked hours, late count, early checkout, deductions | `ERP.Attendance.Log.MonthlyLogL4` |

| **12.10** | `GET` | **Attendance 2** | `/api/companies/{companyId}/att-log/L5/export` | `?sessionKey={sessionKey}` | None | **HTTP 200**: Exports final Payroll overtime summary (Normal OT, Weekend OT, Holiday OT) | `ERP.Attendance.Log.MonthlySummaryForPayrollL5` |

| **12.11** | `PATCH` | **Attendance 2** | `/api/companies/{companyId}/att-log/publish/{sessionKey}` | `{sessionKey}` | None | **HTTP 200**: Locks session from future edits; ready for payroll disbursement | `ERP.Attendance.Log.AttGlobalSessionMaster` |

---

# Part 3: Complete API Catalog by Functional Module

Comprehensive tables for all **18 functional modules (174 endpoints)**.

---

### Module 1: Work Templates (20 Endpoints)

**Base Route:** `/api/companies/{companyId}/worktemplates` | **Controller:** `WorkTemplateController`

| # | Method | Endpoint Path | Query / Route Parameters | Summary & Description |

|---|:---:|---|---|---|

| 1 | `POST` | `/worktemplates/fixed` | None (Company) or `?locationId=` | Create Fixed work template (Company Default or Location) |

| 2 | `POST` | `/worktemplates/flexi` | None (Company) or `?locationId=` | Create Flexi work template (Daily or Weekly hours) |

| 3 | `POST` | `/worktemplates/split` | None (Company) or `?locationId=` | Create Split shift work template (2 intervals with gap) |

| 4 | `POST` | `/worktemplates/roster` | `?locationId={guid}` | Create Roster shift template (Type 4, requires hex `Colour`) |

| 5 | `POST` | `/worktemplates/rotation` | `?locationId={guid}` | Create Rotation template (Type 5, all 7 days required) |

| 6 | `PATCH` | `/worktemplates/fixed/{id}` | `{id}` (Optionally `?locationId=`) | Edit Fixed template (no locationId stages Version 2.0) |

| 7 | `PATCH` | `/worktemplates/flexi/{id}` | `{id}` (Optionally `?locationId=`) | Edit Flexi template |

| 8 | `PATCH` | `/worktemplates/split/{id}` | `{id}` (Optionally `?locationId=`) | Edit Split template |

| 9 | `PATCH` | `/worktemplates/roster/{id}` | `{id}?locationId={guid}` | Edit Roster template |

| 10 | `PATCH` | `/worktemplates/rotation/{id}` | `{id}?locationId={guid}` | Edit Rotation template |

| 11 | `GET` | `/worktemplates` | `?locationId=&state=&isDefault=&templateType=` | Filter and list work templates |

| 12 | `GET` | `/worktemplates/{id}` | `{id}` (Optionally `?locationId=`) | Get work template details by ID |

| 13 | `GET` | `/worktemplates/company-default/versions` | None | Get version history of Company Default template |

| 14 | `GET` | `/worktemplates/company-default/sync-status` | None | Check pending location sync status (`HasPendingLocSync`) |

| 15 | `POST` | `/worktemplates/apply-sync` | None | Pushes updated company default to all inheriting locations |

| 16 | `PATCH` | `/worktemplates/{id}/restore` | `{id}` (Optionally `?locationId=`) | Restore archived template or rollback version |

| 17 | `PATCH` | `/worktemplates/{id}/archive` | `{id}` (Optionally `?locationId=`) | Archive template (locked if plan is using it) |

| 18 | `PATCH` | `/worktemplates/{id}/delete` | `{id}` (Optionally `?locationId=`) | Soft delete template (`IsDeleted = true`) |

| 19 | `GET` | `/worktemplates/short-code/availability` | `?code={shortCode}` | Validate unique 7-char short code availability |

| 20 | `GET` | `/worktemplates/short-code/suggestions` | `?baseCode=&count=` | Generate alphanumeric short code suggestions |

---

### Module 2: Work Plans (9 Endpoints)

**Base Route:** `/api/companies/{companyId}/workplans` | **Controller:** `WorkPlanController`

| # | Method | Endpoint Path | Query / Route Parameters | Summary & Description |

|---|:---:|---|---|---|

| 1 | `POST` | `/workplans` | `?locationId={guid}` | Create Regular Work Plan (packages template + policy snapshots) |

| 2 | `POST` | `/workplans/roster` | `?locationId={guid}` | Create Roster Shift (provisions `RosterWorkTemplate` + Plan together) |

| 3 | `PATCH` | `/workplans/{id}` | `{id}?locationId={guid}` | Edit Regular Work Plan |

| 4 | `PATCH` | `/workplans/roster/{id}` | `{id}?locationId={guid}` | Edit Roster Shift |

| 5 | `PATCH` | `/workplans/{id}/default` | `{id}?locationId={guid}` | Set Work Plan as Location Default plan |

| 6 | `PATCH` | `/workplans/{id}/delete` | `{id}?locationId={guid}` | Soft delete Work Plan |

| 7 | `GET` | `/workplans` | `?locationId=&state=&type=` | List plans with active employee count indicators |

| 8 | `GET` | `/workplans/{id}` | `{id}` | Get Work Plan details by ID |

| 9 | `GET` | `/workplans/{id}/employees` | `{id}?search=&page=&pageSize=` | Get paginated list of employees assigned to this plan |

---

### Module 3: Work Assignments (13 Endpoints)

**Base Route:** `/api/companies/{companyId}/workassignments` | **Controller:** `WorkAssignmentController`

| # | Method | Endpoint Path | Query / Route Parameters | Summary & Description |

|---|:---:|---|---|---|

| 1 | `POST` | `/workassignments/check-conflicts` | `?locationId=&skipAssignmentId=` | Conflict preview before assigning employees |

| 2 | `POST` | `/workassignments` | `?locationId={guid}` | Assign employees to plan for date range |

| 3 | `POST` | `/workassignments/adjust` | `?locationId={guid}` | Assign employees and auto-adjust/split overlapping assignments |

| 4 | `GET` | `/workassignments` | `?locationId={guid}` | List assignment headers by location |

| 5 | `GET` | `/workassignments/upcoming` | `?locationId={guid}` | List assignment headers starting in the future |

| 6 | `GET` | `/workassignments/{id}` | `{id}` | Get assignment header by ID |

| 7 | `GET` | `/workassignments/details` | `?locationId=&state=` | List per-employee assignment rows (`WorkAssignmentMaps`) |

| 8 | `GET` | `/workassignments/details/{id}` | `{id}` | Get single employee assignment row by ID |

| 9 | `PATCH` | `/workassignments/details/{id}/effective-period` | `{id}?locationId={guid}` | Update start date / end date of employee assignment |

| 10 | `PATCH` | `/workassignments/details/{id}/remove` | `{id}?locationId={guid}` | Remove employee from plan (ends assignment) |

| 11 | `POST` | `/workassignments/details/{id}/move/check-conflicts` | `{id}?locationId={guid}` | Conflict preview for moving employee to another plan/board |

| 12 | `PATCH` | `/workassignments/details/{id}/move` | `{id}?locationId={guid}` | Move employee to another regular plan, board, or rotation |

| 13 | `GET` | `/workassignments/current-plans` | `?locationId=&asOf=&employeeIds=` | Query active assigned plans as of date |

---

### Module 4: Attendance Policies (9 Endpoints)

**Base Route:** `/api/companies/{companyId}/attpolicies` | **Controller:** `PolicyController`

| # | Method | Endpoint Path | Query / Route Parameters | Summary & Description |

|---|:---:|---|---|---|

| 1 | `POST` | `/attpolicies/break` | None | Create Break Policy (Paid vs. Unpaid, duration, thresholds) |

| 2 | `POST` | `/attpolicies/graceperiod` | None | Create Grace Period Policy (Late In/Early Out, deductions) |

| 3 | `POST` | `/attpolicies/overtime` | None | Create Overtime Policy (Rules, day multipliers) |

| 4 | `PATCH` | `/attpolicies/break/{policyId}` | `{policyId}` | Edit Break Policy |

| 5 | `PATCH` | `/attpolicies/graceperiod/{policyId}` | `{policyId}` | Edit Grace Period Policy |

| 6 | `PATCH` | `/attpolicies/overtime/{policyId}` | `{policyId}` | Edit Overtime Policy |

| 7 | `PATCH` | `/attpolicies/{policyId}/delete` | `{policyId}` | Soft delete policy (`IsActive = false`) |

| 8 | `GET` | `/attpolicies` | `?state=active&type=graceperiod` | List policies (enforces max 30 company cap) |

| 9 | `GET` | `/attpolicies/{policyId}` | `{policyId}` | Get policy details by ID |

---

### Module 5: Holiday Calendars (7 Endpoints)

**Base Route:** `/api/companies/{companyId}/holidaylist` | **Controller:** `HolidayCalendarController`

| # | Method | Endpoint Path | Query / Route Parameters | Summary & Description |

|---|:---:|---|---|---|

| 1 | `POST` | `/holidaylist` | None (Company) or `?locationId=` | Create calendar (no locationId = Company Default + fanout) |

| 2 | `PATCH` | `/holidaylist/{id}/{year}` | `{id}`, `{year}` | Add or edit holidays in calendar (staged: sets `IsPublished = false`) |

| 3 | `PATCH` | `/holidaylist/{id}/remove/{holidayId}/{year}` | `{id}`, `{holidayId}`, `{year}` | Remove holiday from calendar |

| 4 | `POST` | `/holidaylist/publish/{year}` | `{year}` | Publish company calendar to overwrite inheriting locations |

| 5 | `PATCH` | `/holidaylist/{id}/customise` | `{id}` | Customise (detach) location calendar (`IsInherited = false`) |

| 6 | `GET` | `/holidaylist/{year}` | `?locationId=&state=&calendarType=` | List holiday calendars for year |

| 7 | `GET` | `/holidaylist/{id}` | `{id}` | Get holiday calendar details by ID |

> **Consolidated Master Test Suite Reference:**
> All Holiday Calendar test cases are consolidated into a single dedicated tab in [`AttendanceTestCases_Master_Consolidated.xlsx`](file:///d:/Code/Attendance%20Testing/AttendanceTestCases_Master_Consolidated.xlsx):
> * **Sheet Name:** `Holiday Calendar - Test Cases` (310 Test Cases | P0: 172, P1: 130, P2: 8)
> * **Coverage Breakdown:**
>   1. **DTO Validations (125 TCs):** POST & PATCH mandatory vs optional, min/max lengths, leap year Feb 29/30, month/day boundaries, chronological inversions (`1705`), overlaps (`1707`).
>   2. **Dedicated GUID Validations (31 TCs):** `companyId`, `holidayId`, `locationId`, route, query, header, empty GUID, malformed hex, and tenant claims.
>   3. **Business Logic & 5 Types (50 TCs):** `Public Holiday` (1), `Religious Holiday` (2), `National Holiday` (3), `Bank Holiday` (4), `Gazette Holiday` (5), bilingual `en`/`ar`, and "From Date Only Mandatory" rule (auto `EndDate = StartDate`).
>   4. **Multiple Combinations (45 TCs):** Multi-day, month-spanning, weekend-overlapping (`HolidayOnDayOff`), mixed 5-type calendars, and type mutation matrix.
>   5. **Removal Scenarios (15 TCs):** Future deletion resets `IsPublished: false`, past deletion rejected (`1709`), and inherited location deletion blocked (`1714`).
>   6. **Publishing Lifecycle & Prerequisites (20 TCs):** Compulsory $\ge 1$ holiday list rule (`1704`), CDWT prerequisite, pre-publish staging, Company Service `CompanyChecklist` sync, post-publish mutations, round-2 re-publishing, and detached location immunity.
>   7. **Location Auto-Assignment & Provisioning (24 TCs):** Dual publish auto-set, single existing location auto-set, late location creation auto-provisioning, multiple location bulk auto-set, publish cascade across multiple locations, and multiple staged default work template edits while/until published (`apply-sync`).

---

### Module 6: Employee Exceptions & Exemptions (5 Endpoints)

**Base Route:** `/api/companies/{companyId}/config/attendance/employee-exemp` | **Controller:** `EmployeeExemptionController`

| # | Method | Endpoint Path | Query / Route Parameters | Summary & Description |

|---|:---:|---|---|---|

| 1 | `POST` | `/config/attendance/employee-exemp` | None | Create attendance tracking exemption for employee date range |

| 2 | `PUT` | `/config/attendance/employee-exemp/{id}` | `{id}` | Edit employee attendance exemption |

| 3 | `GET` | `/config/attendance/employee-exemp` | `?locationId=&search=` | List exempt employees |

| 4 | `GET` | `/config/attendance/employee-exemp/{id}` | `{id}` | Get exemption record by ID |

| 5 | `DELETE` | `/config/attendance/employee-exemp/{id}` | `{id}` | Remove employee attendance exemption |

---

### Module 7: Roster Boards (16 Endpoints)

**Base Route:** `/api/companies/{companyId}/roster-boards` | **Controller:** `RosterBoardController`

| # | Method | Endpoint Path | Query / Route Parameters | Summary & Description |

|---|:---:|---|---|---|

| 1 | `POST` | `/roster-boards` | None | Create Roster Board |

| 2 | `GET` | `/roster-boards` | `?locationId={guid}` | List Roster Boards by location |

| 3 | `GET` | `/roster-boards/{id}` | `{id}` | Get Roster Board configuration |

| 4 | `PATCH` | `/roster-boards/{id}` | `{id}` | Edit Roster Board name, description |

| 5 | `DELETE` | `/roster-boards/{id}` | `{id}` | Soft delete Roster Board |

| 6 | `POST` | `/roster-boards/{id}/members` | `{id}` | Enroll employees onto Roster Board |

| 7 | `GET` | `/roster-boards/{id}/members` | `{id}` | List members enrolled on board |

| 8 | `DELETE` | `/roster-boards/{id}/members/{employeeId}` | `{id}`, `{employeeId}` | Remove employee from board |

| 9 | `POST` | `/roster-boards/{id}/areas` | `{id}` | Add physical working area |

| 10 | `PATCH` | `/roster-boards/{id}/areas/{areaId}` | `{id}`, `{areaId}` | Edit physical working area |

| 11 | `DELETE` | `/roster-boards/{id}/areas/{areaId}` | `{id}`, `{areaId}` | Remove physical area |

| 12 | `GET` | `/roster-boards/{id}/shifts` | `{id}` | List shifts associated with this board |

| 13 | `POST` | `/roster-boards/{id}/shifts` | `{id}` | Link existing shift template to board |

| 14 | `DELETE` | `/roster-boards/{id}/shifts/{shiftId}` | `{id}`, `{shiftId}` | Unlink shift from board |

| 15 | `POST` | `/roster-boards/{id}/move-members` | `{id}` | Move members between roster boards |

| 16 | `GET` | `/roster-boards/{id}/periods` | `{id}` | List schedule periods for board |

---

### Module 8: Roster Schedule Planner (8 Endpoints)

**Base Route:** `/api/companies/{companyId}/roster-boards/{boardId}/schedule` and `/schedule-plans`

| # | Method | Endpoint Path | Query / Route Parameters | Summary & Description |

|---|:---:|---|---|---|

| 1 | `GET` | `/roster-boards/{boardId}/schedule/grid` | `?startDate=&endDate=` | Get Planner Grid (Employees $\times$ Dates) |

| 2 | `POST` | `/roster-boards/{boardId}/schedule/assign` | None | Assign shift or Day Off to employee cell |

| 3 | `POST` | `/roster-boards/{boardId}/schedule/publish` | None | Publish roster period (`IsPublished = true`) |

| 4 | `POST` | `/roster-boards/{boardId}/schedule/unpublish` | None | Unpublish roster period for editing |

| 5 | `POST` | `/roster-boards/{boardId}/schedule/copy-previous` | None | Copy schedule from previous pay period |

| 6 | `POST` | `/roster-boards/{boardId}/schedule/clear` | None | Clear shifts for selected range |

| 7 | `GET` | `/roster-boards/{boardId}/schedule/export` | `?periodId={guid}` | Export roster schedule to Excel (`.xlsx`) |

| 8 | `GET` | `/schedule-plans/overview` | None | Planner landing page summary across all boards |

---

### Module 9: Shift Rotations (17 Endpoints)

**Base Route:** `/api/companies/{companyId}/shift-rotations` | **Controller:** `ShiftRotationController`

| # | Method | Endpoint Path | Query / Route Parameters | Summary & Description |

|---|:---:|---|---|---|

| 1 | `POST` | `/shift-rotations` | None | Create Shift Rotation (pattern, weeks per step) |

| 2 | `GET` | `/shift-rotations` | `?locationId={guid}` | List shift rotations |

| 3 | `GET` | `/shift-rotations/{id}` | `{id}` | Get rotation details with plan steps |

| 4 | `PATCH` | `/shift-rotations/{id}` | `{id}` | Edit rotation configuration |

| 5 | `DELETE` | `/shift-rotations/{id}` | `{id}` | Soft delete rotation |

| 6 | `POST` | `/shift-rotations/{id}/preview` | `{id}` | Preview cyclical pattern generation |

| 7 | `POST` | `/shift-rotations/{id}/enrol` | `{id}` | Enrol employees into rotation teams |

| 8 | `GET` | `/shift-rotations/{id}/members` | `{id}` | List members enrolled in rotation |

| 9 | `PATCH` | `/shift-rotations/{id}/members/{employeeId}` | `{id}`, `{employeeId}` | Edit member step offset / start date |

| 10 | `DELETE` | `/shift-rotations/{id}/members/{employeeId}` | `{id}`, `{employeeId}` | Remove member from rotation |

| 11 | `POST` | `/shift-rotations/{id}/generate-schedule` | `{id}` | Generate concrete `WorkAssignmentMap` records |

| 12 | `POST` | `/shift-rotations/{id}/teams` | `{id}` | Add or edit rotation team definition |

| 13 | `DELETE` | `/shift-rotations/{id}/teams/{teamId}` | `{id}`, `{teamId}` | Remove rotation team |

| 14 | `POST` | `/shift-rotations/{id}/move-members` | `{id}` | Move employees between teams or rotations |

| 15 | `GET` | `/shift-rotations/{id}/calendar` | `{id}` | View calendar visualization of rotation |

| 16 | `POST` | `/shift-rotations/{id}/pause` | `{id}` | Temporarily pause rotation schedule |

| 17 | `POST` | `/shift-rotations/{id}/resume` | `{id}` | Resume paused rotation |

---

### Modules 10–15: Attendance Log Pipeline (47 Endpoints)

**Base Route:** `/api/companies/{companyId}/att-log` | **Controller:** `AttendanceLogController`

| # | Sub-Module | Method | Endpoint Path | Query / Route Params | Summary & Description |

|---|---|:---:|---|---|---|

| 1 | **10. Upload & Import** | `POST` | `/att-log/uploadfile` | Form-data | Upload monthly L3 CSV into GridFS (`fs.files`) |

| 2 | | `POST` | `/att-log/data-import/{sessionId}` | `{sessionId}` | Import uploaded CSV into `DailyProcessedL3` |

| 3 | | `POST` | `/att-log/start-process/{sessionKey}` | `{sessionKey}` | Aggregate L3 records into L4 Monthly Summary |

| 4 | | `POST` | `/att-log/re-process/{sessionKey}` | `{sessionKey}` | Re-process only employees with modified rows |

| 5 | | `POST` | `/att-log/re-process/{sessionKey}/{emp}` | `{sessionKey}`, `{emp}` | Re-process single employee |

| 6 | | `PATCH` | `/att-log/publish/{sessionKey}` | `{sessionKey}` | Lock session for payroll export |

| 7 | | `PATCH` | `/att-log/sessions/detail/{id}` | `{id}` | Update session card metadata |

| 8 | **11. Sessions & Files** | `GET` | `/att-log/sessions` | `?page=&pageSize=` | List session cards with processing status |

| 9 | | `GET` | `/att-log/sessions/{sessionId}` | `{sessionId}` | Get session details |

| 10 | | `GET` | `/att-log/sessions/{sessionId}/grid` | `?page=&pageSize=` | Interactive daily timecard grid |

| 11 | | `GET` | `/att-log/sessions/{sessionId}/progress` | `{sessionId}` | Poll session processing progress percentage |

| 12 | | `GET` | `/att-log/sessions/{sessionId}/files` | `{sessionId}` | List files uploaded to session |

| 13 | | `GET` | `/att-log/sessions/{sessionId}/files/{fileId}/download` | `{sessionId}`, `{fileId}` | Download raw uploaded CSV file from GridFS |

| 14 | | `DELETE`| `/att-log/sessions/{sessionId}/files/{fileId}` | `{sessionId}`, `{fileId}` | Remove uploaded file from session |

| 15 | | `DELETE`| `/att-log/sessions/{sessionId}` | `{sessionId}` | Delete session and purge records |

| 16 | | `GET` | `/att-log/sessions/{sessionId}/employees/{emp}` | `{sessionId}`, `{emp}` | Employee monthly punch detail view |

| 17 | **12. Issues & Errors** | `GET` | `/att-log/blockers` | `?sessionId={guid}` | Get blocking errors preventing finalization |

| 18 | | `GET` | `/att-log/errors` | `?sessionId={guid}` | List processing and validation errors |

| 19 | | `GET` | `/att-log/errors/summary` | `?sessionId={guid}` | Error summary counts by category |

| 20 | | `PATCH` | `/att-log/errors/{sessionKey}/resolve` | `{sessionKey}` | Mark error logs resolved |

| 21 | | `GET` | `/att-log/errors/{sessionKey}/export` | `{sessionKey}` | Export error logs to Excel |

| 22 | **13. Daily Records (L3)** | `PATCH` | `/att-log/L3/{id}/override-checkinout` | `{id}` | Correct daily check-in / check-out punches |

| 23 | | `PATCH` | `/att-log/L3/{id}/regularize` | `{id}` | Regularize absent day or shortfall |

| 24 | | `PATCH` | `/att-log/L3/{id}/mark-dayoff` | `{id}` | Reclassify day to Day Off; moves hours to weekend OT |

| 25 | | `PATCH` | `/att-log/L3/{id}/mark-holiday` | `{id}` | Reclassify day to Holiday; clears shortfall |

| 26 | | `PATCH` | `/att-log/L3/{id}/override-overtime` | `{id}` | Set total extra overtime hours manually |

| 27 | | `PATCH` | `/att-log/L3/{id}/override-deduction` | `{id}` | Set penalty deduction hours manually |

| 28 | | `PATCH` | `/att-log/L3/{id}/clear` | `{id}` | Revert last edit (one step back) |

| 29 | | `POST` | `/att-log/L3/settle` | None | Lock days claimed by advance payrun |

| 30 | | `POST` | `/att-log/L3/unsettle` | None | Unlock settled days |

| 31 | **14. Monthly Summaries** | `GET` | `/att-log/L4/{sessionKey}` | `?employeeCode=` | Query L4 monthly aggregated hours and deductions |

| 32 | | `GET` | `/att-log/L4/export` | `?sessionKey=` | Export L4 monthly summary to Excel |

| 33 | | `GET` | `/att-log/L5/{sessionKey}` | `?sessionKey=` | Fetch legacy L5 payroll overtime records |

| 34 | | `GET` | `/att-log/L5/export` | `?sessionKey=` | Export L5 payroll overtime to Excel |

| 35 | **15. Config & State** | `GET` | `/att-log/config` | None | Get company attendance configuration (day-offs, headers) |

| 36 | | `PATCH` | `/att-log/config` | None | Update company attendance global config |

| 37 | | `GET` | `/att-log/state/{dateRangeKey}/{emp}` | `{dateRangeKey}`, `{emp}` | View single employee processing state |

---

### Module 16: Self Service — My Attendance (7 Endpoints)

**Base Route:** `/api/companies/{companyId}/me` | **Controller:** `MyAttendanceController`

| # | Method | Endpoint Path | Query / Route Parameters | Summary & Description |

|---|:---:|---|---|---|

| 1 | `GET` | `/me/periods` | None | Get available pay periods for signed-in employee |

| 2 | `GET` | `/me/schedule` | `?startDate=&endDate=` | Get employee's schedule calendar for date range |

| 3 | `GET` | `/me/current-assignment` | None | Get active work plan / assignment details |

| 4 | `GET` | `/me/holidays` | `?year=` | Get applicable holidays for employee's location and year |

| 5 | `GET` | `/me/policy` | None | Get active grace period, break, and overtime policies |

| 6 | `GET` | `/me/summary` | `?periodId=` | Get monthly attendance summary (hours worked, deductions) |

| 7 | `GET` | `/me/daily-records` | `?startDate=&endDate=` | Get daily punch records and attendance tags |

---

### Module 17: Self Service — My Team (8 Endpoints)

**Base Route:** `/api/companies/{companyId}/team` | **Controller:** `TeamAttendanceController`

| # | Method | Endpoint Path | Query / Route Parameters | Summary & Description |

|---|:---:|---|---|---|

| 1 | `GET` | `/team/summary` | `?date=` | Team attendance summary cards (Present, Late, Absent, Leave counts) |

| 2 | `GET` | `/team/employees` | `?page=&pageSize=` | List reporting employees under the logged-in manager |

| 3 | `GET` | `/team/daily-attendance` | `?date=` | Daily attendance grid of all team reportees |

| 4 | `GET` | `/team/schedule` | `?startDate=&endDate=` | Schedule calendar of all team reportees |

| 5 | `GET` | `/team/work-plans` | None | Active work plans across team members |

| 6 | `GET` | `/team/export/summary` | `?periodId=` | Export team monthly attendance to Excel |

| 7 | `GET` | `/team/export/daily` | `?date=` | Export team daily attendance to Excel |

| 8 | `GET` | `/team/exceptions` | `?date=` | Team members with pending attendance issues |

---

### Module 18: Leave Integration (1 Endpoint)

**Base Route:** `/api/attendance/v1/companies/{companyId}/employees/{employeeId}/calendar` | **Controller:** `DayClassificationController`

| # | Method | Endpoint Path | Query / Route Parameters | Summary & Description |

|---|:---:|---|---|---|

| 1 | `GET` | `/calendar/day-classification` | `?startDate=&endDate=` | Returns classification: `Workday`, `DayOff`, or `Holiday`. Consumed by Leave microservice. |

---

### External Integrated Services Matrix

| Service | DEV Base URL | Primary Responsibility | Integrated Endpoint / Collection |

|---|---|---|---|

| **Company Service** | `https://company8.dev.zoolwork.com` | Master company profiles, location lists, onboarding checklist (`CompanyMaster`) | `GET /api/company/worklocations/companyWorkLocationList`<br>`GET /api/company/{companyId}/holidaytypes`<br>`CompanyMaster` collection (`CompanyChecklist.WorkSchedulesCreated`) |

| **Org Hierarchy Service** | `https://orghierarchyservice-api.dev.zoolwork.com` | Employee identity & reporting structures | `GET /api/companies/{companyId}/employees/{id}` |

| **Employee Service** | `https://employee8.dev.zoolwork.com` | Manager team reporting hierarchy | `GET /api/Employees/companies/{companyId}/employeesBasicList?HierarchyFilter=ReportingManager` |

| **Identity Server** | `https://auth8.dev.zoolwork.com` | Issues JWT bearer tokens | `POST /connect/token` |

| **MongoDB Database** | `10.1.0.4:27018` (`Sahab`) | Direct read/write persistence | All `ERP.Attendance.*` collections |

| **HR Enrolment Data** | Shared collection `EmployeeEnrollments` | Read-only employee identity, pay group, joining date | Attendance Log import & Self-Service |

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

#### Cross-Service Impact: `CompanyMaster` (Company Service DB)

> **Owner Service:** `SP.CompanySvc` (Company Service)  

> **Collection:** `CompanyMaster` (or `Companies`)  

> **Key Object / Field:** `CompanyChecklist.WorkSchedulesCreated` (`Boolean`)  

> 

> **Integration Contract:**  

> When the initial Company Default Work Schedule is provisioned in Attendance 2 (`POST /worktemplates/{type}`), an integration event or internal API call must trigger an update in Company Service to mark `CompanyChecklist.WorkSchedulesCreated: true`.  

> 

> **QA Defect Alert (`USER-01`):**  

> In current DEV builds, `CompanyChecklist.WorkSchedulesCreated` is **NOT updated to true** and remains **`false`**. This is a confirmed integration defect tracked under test case `USER-01`.

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

