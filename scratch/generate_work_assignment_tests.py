# -*- coding: utf-8 -*-
"""
Generator for Work Assignments Senior QA Test Suite (13 Endpoints, 158 Test Cases)
Methodology: Full RTM, Positive, Negative, Standalone, Business Invariants, BVA/EP, Missing/Extra DTO Payloads, DB Assertions.
"""
import os

content = """# 📋 Work Assignments Module — Master Senior QA Test Specification & RTM

> **Target Microservice:** `SP.AttendanceSvc` (.NET 9 / ASP.NET Core)  
> **Environment:** DEV (`https://attendance2.dev.zoolwork.com` / `https://gw8.dev.zoolwork.com`)  
> **Databases:** MongoDB `Sahab` on `10.1.0.4:27018` (`ERP.Attendance.WorkAssignments`, `ERP.Attendance.WorkAssignmentMaps`, `ERP.Attendance.WorkPlans`)  
> **QA Level:** Senior Staff QA Automation & Microservice Specialist  
> **Methodology:** Requirements Traceability Matrix (RTM), Equivalence Partitioning (EP), Boundary Value Analysis (BVA), Error Guessing, Business Workflow Integration, DTO Contract Tampering, Multi-Tenant Security, & MongoDB Deep Invariant Audit.

---

## 📑 Table of Contents
1. [Executive Test Strategy & Architectural Foundations](#1-executive-test-strategy--architectural-foundations)
2. [Master 13-Endpoint Architecture & Parameters Index](#2-master-13-endpoint-architecture--parameters-index)
3. [Requirements Traceability Matrix (RTM)](#3-requirements-traceability-matrix-rtm)
4. [Conflict Detection & Adjustment State Machine](#4-conflict-detection--adjustment-state-machine)
5. [Detailed Test Case Suite (158 Comprehensive Scenarios)](#5-detailed-test-case-suite-158-comprehensive-scenarios)
   - [5.1 Endpoint 1: GET /workassignments (List Headers)](#51-endpoint-1-get-workassignments-list-headers)
   - [5.2 Endpoint 2: GET /workassignments/upcoming (List Upcoming)](#52-endpoint-2-get-workassignmentsupcoming-list-upcoming)
   - [5.3 Endpoint 3: GET /workassignments/{id} (Get Header by ID)](#53-endpoint-3-get-workassignmentsid-get-header-by-id)
   - [5.4 Endpoint 4: POST /workassignments/check-conflicts (Preview Preflight)](#54-endpoint-4-post-workassignmentscheck-conflicts-preview-preflight)
   - [5.5 Endpoint 5: POST /workassignments (Create Assignment Header & Detail Maps)](#55-endpoint-5-post-workassignments-create-assignment-header--detail-maps)
   - [5.6 Endpoint 6: POST /workassignments/adjust (Adjust Overlaps & Assign)](#56-endpoint-6-post-workassignmentsadjust-adjust-overlaps--assign)
   - [5.7 Endpoint 7: GET /workassignments/current-plans (Temporal Employee Plan Query)](#57-endpoint-7-get-workassignmentscurrent-plans-temporal-employee-plan-query)
   - [5.8 Endpoint 8: GET /workassignments/details (List Detail Maps by Location & State)](#58-endpoint-8-get-workassignmentsdetails-list-detail-maps-by-location--state)
   - [5.9 Endpoint 9: GET /workassignments/details/{id} (Get Detail Map by ID)](#59-endpoint-9-get-workassignmentsdetailsid-get-detail-map-by-id)
   - [5.10 Endpoint 10: PATCH /workassignments/details/{id}/effective-period (Edit Dates & Cut)](#510-endpoint-10-patch-workassignmentsdetailsideffective-period-edit-dates--cut)
   - [5.11 Endpoint 11: POST /workassignments/details/{id}/move/check-conflicts (Move Preflight)](#511-endpoint-11-post-workassignmentsdetailsidmovecheck-conflicts-move-preflight)
   - [5.12 Endpoint 12: PATCH /workassignments/details/{id}/move (Execute Move Across Targets)](#512-endpoint-12-patch-workassignmentsdetailsidmove-execute-move-across-targets)
   - [5.13 Endpoint 13: PATCH /workassignments/details/{id}/remove (Deactivate Assignment Row)](#513-endpoint-13-patch-workassignmentsdetailsidremove-deactivate-assignment-row)
6. [Cross-Cutting BVA, DTO Schema Invariants & Multi-Tenancy Security](#6-cross-cutting-bva-dto-schema-invariants--multi-tenancy-security)
7. [MongoDB Cross-Collection Integrity & Denormalization Checklist](#7-mongodb-cross-collection-integrity--denormalization-checklist)

---

## 1. Executive Test Strategy & Architectural Foundations

Work Assignment is the operational core of the Attendance system. It bridges **abstract schedules (Work Plans & Templates)** to **living employees (Work Assignment Maps)** across dates.

### 🔑 Core Principles of Work Assignment Architecture:
1. **Copies, Not Links (Denormalized Snapshotting):**
   - When an assignment is created, the system copies the entire Work Plan (including its embedded Work Template, Fixed Time Slots, and Policies array) into `ERP.Attendance.WorkAssignmentMaps.WorkPlanData`.
   - Modifying a Work Plan later does **not** dynamically change existing assignment maps unless explicitly propagated.
2. **Dual-Collection Structure:**
   - `ERP.Attendance.WorkAssignments`: Header document representing an "Assign" action (`WorkPlanId`, `LocationId`, `StartDate`, `EndDate`, `Status`, `IsActive`). Holds **no employee array**!
   - `ERP.Attendance.WorkAssignmentMaps`: One document per employee per continuous assignment window. This is the **single source of truth** for platform-wide attendance evaluation.
3. **Strict Location & Conflict Isolation:**
   - An employee can have only **one active regular row per date at a location**.
   - Conflicts are categorized strictly as:
     - **Allowed (Clean):** No overlapping assignments.
     - **Adjustable (Regular Overlap):** Overlaps an existing regular plan at the same location. Can be cut/split via `/adjust`.
     - **Blocked (Hard Overlap):** Overlaps a Roster Board shift or a Shift Rotation step. **Never automatically adjusted!** Returns error `Cit.Attendance:1408`.
4. **Temporal Conventions:**
   - Open-ended assignments have `endDate: null` in DTOs, stored as `9999-12-31T23:59:59.999Z` in MongoDB.
   - Retroactive assignments (`startDate < today`) are forbidden on standard creation (Error `Cit.Attendance:1405`) unless `enforceFutureStart=false` query flag is authorized.
   - Ongoing assignments (`startDate <= today`) have locked start dates when editing effective periods.

---

## 2. Master 13-Endpoint Architecture & Parameters Index

| # | HTTP Method & Route Template | Primary Purpose | Route & Query Parameters | Request Body DTO |
| :-: | :--- | :--- | :--- | :--- |
| **1** | `GET /api/companies/{companyId}/workassignments` | List assignment headers | `companyId` (Path, UUID)<br>`locationId` (Query, UUID) | *None* |
| **2** | `GET /api/companies/{companyId}/workassignments/upcoming` | List upcoming headers | `companyId` (Path, UUID)<br>`locationId` (Query, UUID) | *None* |
| **3** | `GET /api/companies/{companyId}/workassignments/{id}` | Get assignment header by ID | `companyId` (Path, UUID)<br>`id` (Path, UUID) | *None* |
| **4** | `POST /api/companies/{companyId}/workassignments/check-conflicts` | Preview conflict detection | `companyId` (Path, UUID)<br>`locationId` (Query, UUID)<br>`skipAssignmentId` (Query, UUID[])<br>`enforceFutureStart` (Query, bool) | `WorkAssignmentDto` |
| **5** | `POST /api/companies/{companyId}/workassignments` | Create assignment & clean maps | `companyId` (Path, UUID)<br>`locationId` (Query, UUID) | `WorkAssignmentDto` |
| **6** | `POST /api/companies/{companyId}/workassignments/adjust` | Resolve overlaps & assign | `companyId` (Path, UUID)<br>`locationId` (Query, UUID) | `AdjustWorkAssignmentEmployeesDto` |
| **7** | `GET /api/companies/{companyId}/workassignments/current-plans` | Get current plan per employee | `companyId` (Path, UUID)<br>`locationId` (Query, UUID)<br>`asOf` (Query, date)<br>`employeeIds` (Query, UUID[]) | *None* |
| **8** | `GET /api/companies/{companyId}/workassignments/details` | List employee assignment maps | `companyId` (Path, UUID)<br>`locationId` (Query, UUID)<br>`state` (Query, string: active/inactive) | *None* |
| **9** | `GET /api/companies/{companyId}/workassignments/details/{id}` | Get one employee assignment map | `companyId` (Path, UUID)<br>`id` (Path, UUID) | *None* |
| **10** | `PATCH /api/companies/{companyId}/workassignments/details/{id}/effective-period` | Edit row dates & adjust | `companyId` (Path, UUID)<br>`id` (Path, UUID)<br>`locationId` (Query, UUID) | `EditEffectivePeriodDto` |
| **11** | `POST /api/companies/{companyId}/workassignments/details/{id}/move/check-conflicts` | Preflight check for move | `companyId` (Path, UUID)<br>`id` (Path, UUID)<br>`locationId` (Query, UUID) | `MoveEmployeeDto` |
| **12** | `PATCH /api/companies/{companyId}/workassignments/details/{id}/move` | Execute move across targets | `companyId` (Path, UUID)<br>`id` (Path, UUID)<br>`locationId` (Query, UUID) | `MoveEmployeeDto` |
| **13** | `PATCH /api/companies/{companyId}/workassignments/details/{id}/remove` | Deactivate employee row | `companyId` (Path, UUID)<br>`id` (Path, UUID)<br>`locationId` (Query, UUID) | *None* |

---

## 3. Requirements Traceability Matrix (RTM)

| Requirement Code | Business Requirement / System Invariant | Applicable Endpoints | Target Error Code / Success Behavior |
| :--- | :--- | :--- | :--- |
| **REQ-WA-001** | Location-Scoping: All operations require valid `companyId` and `locationId` belonging to the tenant. | Endpoints 1 to 13 | 400 `Cit.Attendance:Validation` / 404 `Cit.Sbp:NotFound` |
| **REQ-WA-002** | Start Date Invariant: Assignment start date must be today or in future (`startDate >= today`). | Endpoints 4, 5, 6, 10 | 400 `Cit.Attendance:1405` |
| **REQ-WA-003** | End Date Invariant: If provided, `endDate >= startDate`. Inverted dates strictly blocked. | Endpoints 4, 5, 6, 10, 11, 12 | 400 `Cit.Attendance:Validation` |
| **REQ-WA-004** | Open-Ended Assignment: If `endDate` is omitted/null, stored as `9999-12-31` and returned as `null`. | Endpoints 4, 5, 6, 10 | 200 OK (`endDate: null`) |
| **REQ-WA-005** | Plan Name Integrity: `workPlanName.en` must match the actual plan name referenced by `workPlanId`. | Endpoints 4, 5, 6 | 400 `Cit.Attendance:1305` |
| **REQ-WA-006** | Plan Existence & State: Referenced `workPlanId` must exist, belong to same company/location, and `isDeleted == false`. | Endpoints 4, 5, 6, 11, 12 | 400 `Cit.Attendance:1301` / `1304` |
| **REQ-WA-007** | Non-Regular Plan Guard: Regular work assignments cannot be created for Roster or Rotation plans. | Endpoints 4, 5, 6 | 400 `Cit.Attendance:1104` |
| **REQ-WA-008** | In-Use Plan Lock: Assigning an employee marks the Work Plan as in-use (`HasWorkAssignments = true`). Cannot delete plan. | Endpoints 5, 6 | Plan DELETE blocked with `1304` |
| **REQ-WA-009** | Conflict Categorization: Preflight accurately splits employees into `allowed`, `adjustable`, and `blocked`. | Endpoint 4 | 200 OK (`canProceed: bool`) |
| **REQ-WA-010** | Partial Header Creation: `POST /workassignments` creates header and clean maps, returning conflicted list. | Endpoint 5 | 200 OK (`id`, `conflictedEmployeeIds`) |
| **REQ-WA-011** | Hard Roster/Rotation Overlap Guard: `POST /adjust` and `/move` reject hard overlaps with Roster/Rotation. | Endpoints 6, 10, 12 | 400 `Cit.Attendance:1408` |
| **REQ-WA-012** | Overlap Cutting Logic: `POST /adjust` cuts overlapping regular rows into: Ends Early, Split, Starts Later, or Deactivated. | Endpoint 6 | 200 OK (`adjustedEmployeeIds`) |
| **REQ-WA-013** | Detail Immutability: When assignment is active (`startDate <= today`), `startDate` is locked on edit. | Endpoint 10 | 400 `Cit.Attendance:1406` / Date locked |
| **REQ-WA-014** | Move Target Polymorphism: Target type can be `WorkPlan` (2), `Board` (1), or `Rotation` (3) with respective IDs. | Endpoints 11, 12 | 200 OK (`createdWorkAssignmentId` / `targetMembershipId`) |
| **REQ-WA-015** | Soft-Deactivation: `PATCH /details/{id}/remove` sets `IsActive: false` in `WorkAssignmentMaps`. | Endpoint 13 | 200 OK (`IsActive: false`) |
| **REQ-WA-016** | DTO Sanitization: Client-injected `tenantName`, `id`, `isDeleted` must be rejected or stripped. | Endpoints 4, 5, 6, 10, 11, 12 | 400 Validation / Stripped |

---

## 4. Conflict Detection & Adjustment State Machine

When assigning an employee to a new regular plan `[NewStart, NewEnd]`, existing overlapping assignments are resolved as follows:

```
                           ┌────────────────────────────────────────┐
                           │ Existing Assignment in [NewStart, End] │
                           └───────────────────┬────────────────────┘
                                               │
                    ┌──────────────────────────┴──────────────────────────┐
                    ▼                                                     ▼
        [Type 1: Regular Plan]                               [Type 2: Roster / Type 3: Rotation]
                    │                                                     │
        ┌───────────┴───────────┐                                         ▼
        │ Resolution Strategy   │                               ❌ HARD CONFLICT (1408)
        ▼                       ▼                            Cannot adjust automatically!
[IsAdjustConfirmed=False]  [IsAdjustConfirmed=True]          Must remove from Board/Rotation first.
        │                       │
        ▼                       ▼
Returned as Conflicted     OVERLAP CUTTING:
(Header created, map       1. Ends Early: OldEnd = NewStart - 1 day
 not created)              2. Split: OldRow1 ends NewStart-1; OldRow2 starts NewEnd+1
                           3. Starts Later: OldStart = NewEnd + 1 day
                           4. Deactivated: IsActive = false (encompassed)
```

---

## 5. Detailed Test Case Suite (158 Comprehensive Scenarios)

### 5.1 Endpoint 1: GET /workassignments (List Headers)
- **Route:** `GET /api/companies/{companyId}/workassignments?locationId={locationId}`
- **Scope:** Retrieves all work assignment header documents for a location.

| Test Case ID | Test Scenario Description | Category | Query / Path Parameters | Expected HTTP | Expected Response / DB State |
| :--- | :--- | :---: | :--- | :---: | :--- |
| `WA-GET-001` | Positive: Retrieve headers for location with multiple assignments | POS | Valid `companyId`, `locationId` | `200 OK` | Returns array of headers (`id`, `workPlanId`, `workPlanName`, `startDate`, `endDate`, `status`, `isActive: true`). |
| `WA-GET-002` | Positive: Location with zero assignments returns empty array | POS | Valid `companyId`, empty location | `200 OK` | `[]` (empty list, not 404 or null). |
| `WA-GET-003` | Boundary: Assignment with `endDate == null` returned correctly | POS | Valid `companyId`, `locationId` | `200 OK` | Documents with `endDate: null` (DB has `9999-12-31`). |
| `WA-GET-004` | Negative: Missing `locationId` query parameter | NEG | Valid `companyId`, omitted `locationId` | `400 Bad Request` | `Cit.Attendance:Validation` / Missing location. |
| `WA-GET-005` | Negative: Invalid UUID format for `companyId` | NEG | `companyId: "invalid-uuid"`, valid `locationId` | `400 Bad Request` | `One or more validation errors occurred`. |
| `WA-GET-006` | Negative: Invalid UUID format for `locationId` | NEG | Valid `companyId`, `locationId: "12345"` | `400 Bad Request` | `One or more validation errors occurred`. |
| `WA-GET-007` | Negative: Non-existent `companyId` | NEG | Random non-existent UUID, valid `locationId` | `404 / 500` | Verify sanitized 404, check against `DEFECT-20261106-02`. |
| `WA-GET-008` | Negative: Location belonging to different company (Cross-Company) | SEC | Company A, Location belonging to Company B | `400 / 404` | Block cross-company traversal. |
| `WA-GET-009` | Security: Call without `Authorization` bearer header | SEC | Valid route, no token | `401 Unauthorized` | Rejected by JWT middleware. |
| `WA-GET-010` | Database Invariant: Verify returned headers match MongoDB | DB | Valid `companyId`, `locationId` | `200 OK` | Every element matches `Sahab.ERP.Attendance.WorkAssignments`. |

---

### 5.2 Endpoint 2: GET /workassignments/upcoming (List Upcoming)
- **Route:** `GET /api/companies/{companyId}/workassignments/upcoming?locationId={locationId}`
- **Scope:** Retrieves only upcoming assignment headers (`startDate > today`) with at least one active employee.

| Test Case ID | Test Scenario Description | Category | Query / Path Parameters | Expected HTTP | Expected Response / DB State |
| :--- | :--- | :---: | :--- | :---: | :--- |
| `WA-UP-001` | Positive: Retrieve upcoming assignments where `startDate > today` | POS | Valid `companyId`, `locationId` | `200 OK` | Array contains only assignments starting tomorrow or later. |
| `WA-UP-002` | Positive: Exclude ongoing assignments (`startDate <= today`) | POS | Valid `companyId`, `locationId` | `200 OK` | Ensure active/ongoing assignments are strictly omitted. |
| `WA-UP-003` | Positive: Exclude past assignments (`endDate < today`) | POS | Valid `companyId`, `locationId` | `200 OK` | Ensure expired assignments are strictly omitted. |
| `WA-UP-004` | Business Rule: Upcoming header with 0 active employees omitted | BUS | Header starting in future but all maps deactivated | `200 OK` | Header must not appear in upcoming list if active employee count == 0. |
| `WA-UP-005` | Negative: Missing `locationId` query parameter | NEG | Valid `companyId`, omitted `locationId` | `400 Bad Request` | Validation failure. |
| `WA-UP-006` | Negative: Malformed `locationId` parameter | NEG | Valid `companyId`, `locationId: "abc"` | `400 Bad Request` | Validation failure. |
| `WA-UP-007` | Negative: Soft-deleted assignment header excluded | DB | Soft-deleted upcoming header in Mongo | `200 OK` | `IsDeleted: true` headers excluded. |
| `WA-UP-008` | Security: Cross-tenant company probe on upcoming | SEC | Company of Tenant B with Tenant A token | `403 / 404` | Cross-tenant access denied. |

---

### 5.3 Endpoint 3: GET /workassignments/{id} (Get Header by ID)
- **Route:** `GET /api/companies/{companyId}/workassignments/{id}` (No locationId query)
- **Scope:** Retrieves a single assignment header by UUID.

| Test Case ID | Test Scenario Description | Category | Query / Path Parameters | Expected HTTP | Expected Response / DB State |
| :--- | :--- | :---: | :--- | :---: | :--- |
| `WA-GETID-001` | Positive: Retrieve existing assignment header by ID | POS | Valid `companyId`, existing `id` | `200 OK` | Returns full header object matching MongoDB. |
| `WA-GETID-002` | Positive: Open-ended assignment header serialization | POS | Header with `endDate: 9999-12-31` | `200 OK` | Response contains `"endDate": null`. |
| `WA-GETID-003` | Negative: Non-existent assignment header UUID | NEG | Valid `companyId`, random UUID | `404 Not Found` | `Cit.Sbp:NotFound` / `1401`. |
| `WA-GETID-004` | Negative: Malformed header `id` UUID | NEG | Valid `companyId`, `id: "not-a-uuid"` | `400 Bad Request` | Format validation error. |
| `WA-GETID-005` | Negative: Header belonging to different company in URL | SEC | Company A in URL, Header belonging to Company B | `404 Not Found` | Header not found under Company A. |
| `WA-GETID-006` | Edge Case: Retrieve soft-deleted assignment header | NEG | `id` of header with `IsDeleted: true` | `404 Not Found` | Must not return 200 OK (verify against `DEFECT-20261112-11`). |
| `WA-GETID-007` | Edge Case: Pass query `?locationId=` (extra parameter ignored) | BVA | Valid `id` with superfluous `locationId` | `200 OK` | Endpoint operates strictly on path `id`. |
| `WA-GETID-008` | Security: Unauthenticated request | SEC | Valid `id`, no Bearer token | `401 Unauthorized` | Unauthorized. |

---

### 5.4 Endpoint 4: POST /workassignments/check-conflicts (Preview Preflight)
- **Route:** `POST /api/companies/{companyId}/workassignments/check-conflicts?locationId={locationId}&skipAssignmentId={}&enforceFutureStart={}`
- **DTO:** `WorkAssignmentDto`
- **Scope:** Read-only simulation. Analyzes requested assignment against existing schedule maps.

| Test Case ID | Test Scenario Description | Category | Query & Payload Parameters | Expected HTTP | Expected Response / DB State |
| :--- | :--- | :---: | :--- | :---: | :--- |
| `WA-CHK-001` | Positive: Clean employees with no overlaps | POS | `employeeIds: [E1, E2]`, future dates, clean | `200 OK` | `canProceed: true`, `allowedEmployeeIds: [E1, E2]`, `conflictedEmployeeIds: []`. |
| `WA-CHK-002` | Business: Employee on existing Regular Plan (Adjustable) | BUS | `employeeIds: [E_reg]`, overlaps Regular Plan | `200 OK` | `canProceed: true`, `adjustableEmployeeIds: [E_reg]`, `conflictDetails` shows `isAdjustable: true`. |
| `WA-CHK-003` | Business: Employee on Roster Board shift (Blocked) | BUS | `employeeIds: [E_rost]`, overlaps Roster day | `200 OK` | `canProceed: false`, `blockedEmployeeIds: [E_rost]`, `conflictDetails` shows `source: "Roster"`. |
| `WA-CHK-004` | Business: Employee on Shift Rotation step (Blocked) | BUS | `employeeIds: [E_rot]`, overlaps Rotation step | `200 OK` | `canProceed: false`, `blockedEmployeeIds: [E_rot]`, `conflictDetails` shows `source: "Rotation"`. |
| `WA-CHK-005` | Business: Mixed cohort (1 Clean, 1 Adjustable, 1 Blocked) | BUS | `employeeIds: [E_clean, E_adj, E_blk]` | `200 OK` | Accurately segments all 3 categories; `canProceed: false` until Blocked skipped. |
| `WA-CHK-006` | Query Flag: `skipAssignmentId` ignores current detail row being edited | BUS | Query: `skipAssignmentId=[CurrentDetailId]` | `200 OK` | Current row is excluded from collision check. |
| `WA-CHK-007` | Query Flag: `enforceFutureStart=true` rejects past `startDate` | NEG | `startDate: yesterday`, `enforceFutureStart=true` | `400 Bad Request` | `Cit.Attendance:1405` (Start date cannot be in past). |
| `WA-CHK-008` | Query Flag: `enforceFutureStart=false` permits past `startDate` | POS | `startDate: yesterday`, `enforceFutureStart=false` | `200 OK` | Conflict detection runs on retroactive range. |
| `WA-CHK-009` | Boundary: `startDate == today` (UTC) | BVA | `startDate: today`, `endDate: null` | `200 OK` | Permitted as valid start boundary. |
| `WA-CHK-010` | Boundary: Inverted dates (`endDate < startDate`) | NEG | `startDate: 2026-12-10`, `endDate: 2026-12-05` | `400 Bad Request` | `Cit.Attendance:Validation` / End date before start. |
| `WA-CHK-011` | Boundary: Single day assignment (`startDate == endDate`) | BVA | `startDate: 2026-12-15`, `endDate: 2026-12-15` | `400 / 200` | Verify whether 1-day regular plan is permitted. |
| `WA-CHK-012` | Plan Mismatch: `workPlanName.en` does not match plan | NEG | Valid `workPlanId`, `workPlanName.en: "Wrong Name"` | `400 Bad Request` | `Cit.Attendance:1305` (Work plan name mismatch). |
| `WA-CHK-013` | Plan Incompatible: `workPlanId` points to Rotation Plan | NEG | `workPlanId` of Rotation (`PlanType=3`) | `400 Bad Request` | `Cit.Attendance:1104` (Incompatible plan type). |
| `WA-CHK-014` | Plan Incompatible: `workPlanId` points to Roster Plan | NEG | `workPlanId` of Roster (`PlanType=2`) | `400 Bad Request` | `Cit.Attendance:1104` (Incompatible plan type). |
| `WA-CHK-015` | Empty Employee Array: `employeeIds: []` | BVA | `employeeIds: []`, valid dates & plan | `400 / 200` | Verify if check allows 0 employees or requires >= 1. |
| `WA-CHK-016` | Database Isolation: Verify 0 writes executed in MongoDB | DB | Run check-conflicts | `200 OK` | MongoDB count of WorkAssignments & Maps unchanged. |

---

### 5.5 Endpoint 5: POST /workassignments (Create Assignment Header & Detail Maps)
- **Route:** `POST /api/companies/{companyId}/workassignments?locationId={locationId}`
- **DTO:** `WorkAssignmentDto`
- **Scope:** Creates the assignment header and writes detail maps for clean employees.

| Test Case ID | Test Scenario Description | Category | Payload Details | Expected HTTP | Expected Response / DB State |
| :--- | :--- | :---: | :--- | :---: | :--- |
| `WA-CRT-001` | Positive: Create assignment with all clean employees (Closed Period) | POS | `[E1, E2]`, `startDate: tomorrow`, `endDate: +30d` | `200 OK` | Returns new assignment `id`; DB creates 1 Header + 2 `WorkAssignmentMaps`. |
| `WA-CRT-002` | Positive: Create open-ended assignment (`endDate: null`) | POS | `[E1]`, `startDate: tomorrow`, `endDate: null` | `200 OK` | DB Header & Map have `EndDate: 9999-12-31`. API returns `endDate: null`. |
| `WA-CRT-003` | Positive: Create assignment starting today (`startDate: today`) | BVA | `[E1]`, `startDate: today`, `endDate: null` | `200 OK` | Assignment active immediately. Header `Status: 1` (Active). |
| `WA-CRT-004` | Partial Success: Cohort with 1 Clean and 1 Conflicted employee | BUS | `[E_clean, E_conflicted]` | `200 OK` | Header created; Map created for `E_clean` ONLY. `conflictedEmployeeIds: [E_conflicted]` returned. |
| `WA-CRT-005` | Edge Case: All selected employees conflict | BUS | `[E_conflicted1, E_conflicted2]` | `200 OK` | Header created with 0 maps; returns all as `conflictedEmployeeIds`. |
| `WA-CRT-006` | Negative: Start date in the past (`startDate < today`) | NEG | `startDate: yesterday` | `400 Bad Request` | `Cit.Attendance:1405` (Start date cannot be in past). |
| `WA-CRT-007` | Negative: Chronological inversion (`endDate < startDate`) | NEG | `startDate: 2026-12-01`, `endDate: 2026-11-20` | `400 Bad Request` | `Cit.Attendance:Validation`. |
| `WA-CRT-008` | Negative: Work Plan Name English mismatch | NEG | `workPlanName.en: "Fake Name"` | `400 Bad Request` | `Cit.Attendance:1305`. |
| `WA-CRT-009` | Negative: Non-existent `workPlanId` | NEG | `workPlanId: random_uuid` | `400 Bad Request` | `Cit.Attendance:1301` / Plan not found. |
| `WA-CRT-010` | Negative: Soft-deleted `workPlanId` | NEG | `workPlanId` has `IsDeleted: true` | `400 Bad Request` | `Cit.Attendance:1304` / Deleted plan. |
| `WA-CRT-011` | Negative: Plan belongs to different location | SEC | Plan created for Location 1, assigned at Location 2 | `400 Bad Request` | Location mismatch rejection. |
| `WA-CRT-012` | Negative: Missing `workPlanId` field | DTO | Body omits `workPlanId` | `400 Bad Request` | Validation failure. |
| `WA-CRT-013` | Negative: Missing `startDate` field | DTO | Body omits `startDate` | `400 Bad Request` | Validation failure. |
| `WA-CRT-014` | Negative: Null employeeIds array (`employeeIds: null`) | DTO | `employeeIds: null` | `400 Bad Request` | Validation failure. |
| `WA-CRT-015` | DTO Leak: Inject client-supplied `tenantName` | DTO | Body includes `"tenantName": {"en": "Spoofed"}` | `400 / Stripped` | Verify against `DEFECT-20261112-01`. |
| `WA-CRT-016` | DTO Leak: Inject client-supplied `id` in body | DTO | Body includes `"id": random_uuid` | `400 / Stripped` | Server-generated ID must be used. |
| `WA-CRT-017` | DB Invariant: Work Plan marked in-use | DB | Assign employee to Plan A | `200 OK` | `ERP.Attendance.WorkPlans` has `HasWorkAssignments: true`. Plan delete blocked (`1304`). |
| `WA-CRT-018` | DB Invariant: Snapshot copy embedded into Map | DB | Inspect created `WorkAssignmentMaps` | `200 OK` | `WorkPlanData` has full copy of Template and Policies. |

---

### 5.6 Endpoint 6: POST /workassignments/adjust (Adjust Overlaps & Assign)
- **Route:** `POST /api/companies/{companyId}/workassignments/adjust?locationId={locationId}`
- **DTO:** `AdjustWorkAssignmentEmployeesDto`
- **Scope:** Resolves overlapping regular assignments by cutting/splitting old rows and attaching employees to `workAssignmentId`.

| Test Case ID | Test Scenario Description | Category | Overlap Scenario & Payload | Expected HTTP | Expected Response / DB State |
| :--- | :--- | :---: | :--- | :---: | :--- |
| `WA-ADJ-001` | Positive: Overlap Resolution 1 — Ends Early | BUS | Old: 2026-10-01 → 2026-12-15.<br>New: 2026-12-01 → 2026-12-31. | `200 OK` | Old map truncated to end `2026-11-30`. New map created `2026-12-01 → 2026-12-31`. |
| `WA-ADJ-002` | Positive: Overlap Resolution 2 — Split (Cut & Resume) | BUS | Old: 2026-10-01 → 2027-03-31.<br>New: 2026-12-01 → 2026-12-31. | `200 OK` | Old map cut to `2026-11-30`. New map created `2026-12-01 → 2026-12-31`. Resumed old map created `2027-01-01 → 2027-03-31`. |
| `WA-ADJ-003` | Positive: Overlap Resolution 3 — Starts Later | BUS | Old: 2026-12-15 → 2027-03-31.<br>New: 2026-12-01 → 2026-12-31. | `200 OK` | Old map start date adjusted to `2027-01-01`. New map created `2026-12-01 → 2026-12-31`. |
| `WA-ADJ-004` | Positive: Overlap Resolution 4 — Completely Encompassed | BUS | Old: 2026-12-05 → 2026-12-20.<br>New: 2026-12-01 → 2026-12-31. | `200 OK` | Old map marked `IsActive: false` (kept for audit). New map created for whole period. |
| `WA-ADJ-005` | Positive: Cut open-ended old assignment | BUS | Old: 2026-10-01 → Open-ended.<br>New: 2026-12-01 → Open-ended. | `200 OK` | Old map updated with `EndDate: 2026-11-30`. New map starts `2026-12-01`, open-ended. |
| `WA-ADJ-006` | Hard Block: Employee overlaps Roster Board shift | BUS | Employee enrolled on Roster shift in period | `400 Bad Request` | `Cit.Attendance:1408` (Cannot adjust Roster overlap). Whole request rejected! |
| `WA-ADJ-007` | Hard Block: Employee overlaps Shift Rotation step | BUS | Employee enrolled on Rotation in period | `400 Bad Request` | `Cit.Attendance:1408` (Cannot adjust Rotation overlap). Whole request rejected! |
| `WA-ADJ-008` | Batch Hard Block: 5 employees adjustable, 1 employee on Roster | BUS | 6 employees total; 1 is on Roster | `400 Bad Request` | `Cit.Attendance:1408`. Atomic rejection: 0 employees adjusted! |
| `WA-ADJ-009` | Negative: Non-existent `workAssignmentId` header | NEG | `workAssignmentId: random_uuid` | `400 / 404` | Assignment header not found. |
| `WA-ADJ-010` | Negative: Dates mismatch between payload and header | BUS | Payload dates differ from `workAssignmentId` | `400 Bad Request` | Adjust must use header dates. |
| `WA-ADJ-011` | Negative: Missing `workAssignmentId` field | DTO | Body omits `workAssignmentId` | `400 Bad Request` | DTO validation failure. |
| `WA-ADJ-012` | Negative: Empty employeeIds array | BVA | `employeeIds: []` | `400 Bad Request` | Cannot adjust empty list. |
| `WA-ADJ-013` | DB Invariant: Verify old map history preserved | DB | After split/cut resolution | `200 OK` | Audit fields `ModifiedAt`, `ModifiedBy` populated on modified maps. |
| `WA-ADJ-014` | Idempotency: Re-running adjust on already adjusted cohort | BUS | Run adjust twice with same payload | `200 OK` | Second run detects no overlaps, skips or confirms no change. |

---

### 5.7 Endpoint 7: GET /workassignments/current-plans (Temporal Employee Plan Query)
- **Route:** `GET /api/companies/{companyId}/workassignments/current-plans?locationId={locationId}&asOf={asOf}&employeeIds={employeeIds}`
- **Scope:** Returns what schedule each employee is actively assigned to on a specific date.

| Test Case ID | Test Scenario Description | Category | Query Parameters | Expected HTTP | Expected Response / DB State |
| :--- | :--- | :---: | :--- | :---: | :--- |
| `WA-CUR-001` | Positive: Query today's active plan for single employee | POS | `asOf: today`, `employeeIds: [E1]` | `200 OK` | Returns plan details (`workPlanId`, `workPlanName`, `planType: "Regular"`, `startDate`, `endDate`). |
| `WA-CUR-002` | Positive: Query multiple employees across Regular, Roster & Rotation | BUS | `employeeIds: [E_reg, E_rost, E_rot]` | `200 OK` | Correctly identifies plan type and source for each employee. |
| `WA-CUR-003` | Positive: Default `asOf` date (omitted query) | POS | `asOf` omitted, `employeeIds: [E1]` | `200 OK` | Defaults to today's UTC date. |
| `WA-CUR-004` | Temporal Query: Historical date in the past | BUS | `asOf: 2026-01-01` | `200 OK` | Returns assignment active on that specific historical date. |
| `WA-CUR-005` | Temporal Query: Future date | BUS | `asOf: 2027-01-01` | `200 OK` | Returns upcoming scheduled plan or null if not yet scheduled. |
| `WA-CUR-006` | Unassigned Employee: Employee has no assignment on `asOf` | POS | `employeeIds: [E_unassigned]` | `200 OK` | Returns entry with null plan or empty indicator. |
| `WA-CUR-007` | Negative: Invalid date format for `asOf` | NEG | `asOf: "invalid-date"` | `400 Bad Request` | Date format validation error. |
| `WA-CUR-008` | Negative: Non-existent employee UUID in query | NEG | `employeeIds: [random_uuid]` | `200 OK` | Returns item with null plan (not 404). |
| `WA-CUR-009` | Boundary: Massive employee batch query (200 employees) | BVA | `employeeIds` with 200 UUIDs | `200 OK` | High-volume query performs without timeout or truncation. |
| `WA-CUR-010` | Boundary: Query on transition boundary date (`asOf == startDate`) | BVA | `asOf == new_plan_startDate` | `200 OK` | Accurately returns the newly starting plan. |
| `WA-CUR-011` | Boundary: Query on transition boundary date (`asOf == endDate`) | BVA | `asOf == old_plan_endDate` | `200 OK` | Accurately returns the expiring plan. |
| `WA-CUR-012` | Security: Employee belonging to different company | SEC | `employeeIds: [E_companyB]` | `200 OK` | Cross-company employee yields null/empty plan. |

---

### 5.8 Endpoint 8: GET /workassignments/details (List Detail Maps by Location & State)
- **Route:** `GET /api/companies/{companyId}/workassignments/details?locationId={locationId}&state={state}`
- **Scope:** Retrieves employee assignment map rows (`WorkAssignmentMaps`) for a location, filtered by state.

| Test Case ID | Test Scenario Description | Category | Query Parameters | Expected HTTP | Expected Response / DB State |
| :--- | :--- | :---: | :--- | :---: | :--- |
| `WA-DET-001` | Positive: Retrieve active assignment detail rows (`state=active`) | POS | `locationId: valid`, `state: "active"` | `200 OK` | Returns array of detail maps where `IsActive: true` and not expired. |
| `WA-DET-002` | Positive: Retrieve inactive/past assignment detail rows (`state=inactive`) | POS | `locationId: valid`, `state: "inactive"` | `200 OK` | Returns array of historical/deactivated maps (`IsActive: false`). |
| `WA-DET-003` | Positive: Omit `state` parameter (default behavior) | POS | `locationId: valid`, `state` omitted | `200 OK` | Returns default active rows. |
| `WA-DET-004` | Filter Inversion Check: Verify active filter does NOT return deleted | BUG | `state: "active"` | `200 OK` | Verify against `DEFECT-20261112-03` (check predicate logic). |
| `WA-DET-005` | Negative: Invalid `state` value | NEG | `state: "invalid_state_999"` | `400 Bad Request` | State validation error. |
| `WA-DET-006` | Negative: Missing `locationId` parameter | NEG | Omitted `locationId` | `400 Bad Request` | Missing location validation. |
| `WA-DET-007` | Boundary: Location with 500+ employee assignment rows | BVA | Large active location | `200 OK` | Verify pagination/result completeness. |
| `WA-DET-008` | Detail Properties Check: Verify embedded employee metadata | DB | Inspect response items | `200 OK` | Each item contains `employeeCode`, `employeeName`, `department`, `designation`. |
| `WA-DET-009` | Detail Properties Check: Verify embedded plan copy | DB | Inspect response items | `200 OK` | Each item contains `workPlanData` with template and policies snapshot. |
| `WA-DET-010` | Security: Cross-tenant location probe | SEC | Tenant A queries Tenant B location | `403 / 404` | Cross-tenant access blocked. |

---

### 5.9 Endpoint 9: GET /workassignments/details/{id} (Get Detail Map by ID)
- **Route:** `GET /api/companies/{companyId}/workassignments/details/{id}` (No locationId query)
- **Scope:** Retrieves a single employee assignment map record by detail UUID.

| Test Case ID | Test Scenario Description | Category | Parameters | Expected HTTP | Expected Response / DB State |
| :--- | :--- | :---: | :--- | :---: | :--- |
| `WA-DETID-001` | Positive: Retrieve existing assignment detail map by ID | POS | Valid `companyId`, existing detail `id` | `200 OK` | Full detail object returned matching `WorkAssignmentMaps`. |
| `WA-DETID-002` | Positive: Open-ended detail map serialization | POS | Detail map with `EndDate: 9999-12-31` | `200 OK` | `"endDate": null`. |
| `WA-DETID-003` | Negative: Non-existent detail map UUID | NEG | Random non-existent UUID | `404 Not Found` | `Cit.Attendance:1401` / Assignment detail not found. |
| `WA-DETID-004` | Negative: Malformed detail UUID | NEG | `id: "xyz-123"` | `400 Bad Request` | UUID format validation error. |
| `WA-DETID-005` | Negative: Detail map belonging to different company in URL | SEC | Company A in URL, Detail belonging to Company B | `404 Not Found` | Cross-company leak prevented. |
| `WA-DETID-006` | Negative: Pass Assignment Header ID instead of Detail Map ID | NEG | `id` of Header record | `404 Not Found` | Correct collection isolation (`WorkAssignments` vs `Maps`). |
| `WA-DETID-007` | Positive: Retrieve deactivated detail map (`IsActive: false`) | POS | `id` of deactivated row | `200 OK` | Returns historical row with `isActive: false`. |
| `WA-DETID-008` | Security: Unauthenticated request | SEC | Valid `id`, no Bearer token | `401 Unauthorized` | Rejected by JWT middleware. |

---

### 5.10 Endpoint 10: PATCH /workassignments/details/{id}/effective-period (Edit Dates & Cut)
- **Route:** `PATCH /api/companies/{companyId}/workassignments/details/{id}/effective-period?locationId={locationId}`
- **DTO:** `EditEffectivePeriodDto`
- **Scope:** Modifies start and end dates of an existing assignment row, optionally cutting conflicts.

| Test Case ID | Test Scenario Description | Category | Payload Details | Expected HTTP | Expected Response / DB State |
| :--- | :--- | :---: | :--- | :---: | :--- |
| `WA-EFP-001` | Positive: Edit future assignment dates (Clean period) | POS | Future row; change start & end to clean dates | `200 OK` | `WorkAssignmentMaps` updated with new dates. |
| `WA-EFP-002` | Positive: Close an open-ended assignment (`endDate: new_date`) | POS | Open-ended row; set `endDate: 2026-12-31` | `200 OK` | `EndDate` updated from `9999-12-31` to `2026-12-31`. |
| `WA-EFP-003` | Positive: Make a closed assignment open-ended (`endDate: null`) | POS | Closed row; set `endDate: null` | `200 OK` | `EndDate` updated to `9999-12-31`. |
| `WA-EFP-004` | Locked Start Date: Ongoing assignment (`startDate <= today`) | BUS | Ongoing row; attempt to change `startDate` | `400 Bad Request` | `Cit.Attendance:1406` (Cannot modify start date of active assignment). |
| `WA-EFP-005` | Permitted End Date: Ongoing assignment (`startDate <= today`) | BUS | Ongoing row; modify `endDate` only | `200 OK` | Allowed! End date modified successfully. |
| `WA-EFP-006` | Ongoing End Date Floor: `endDate < today` on ongoing assignment | NEG | Ongoing row; attempt `endDate: yesterday` | `400 Bad Request` | Cannot close ongoing assignment in the past. |
| `WA-EFP-007` | Conflict Discovery: Conflict exists & `adjustConflicts=false` | BUS | New dates overlap another plan; `adjustConflicts: false` | `200 OK` | `hasConflicts: true`, `conflicts: [...]`. **Nothing saved in DB!** |
| `WA-EFP-008` | Conflict Resolution: Conflict exists & `adjustConflicts=true` | BUS | New dates overlap another regular plan; `adjustConflicts: true` | `200 OK` | Overlapping regular plan cut; dates saved. |
| `WA-EFP-009` | Conflict Block: Overlaps Roster Board shift | BUS | New dates overlap Roster shift; `adjustConflicts: true` | `400 Bad Request` | `Cit.Attendance:1408` (Roster overlap cannot be adjusted). |
| `WA-EFP-010` | Conflict Block: Overlaps Shift Rotation step | BUS | New dates overlap Rotation; `adjustConflicts: true` | `400 Bad Request` | `Cit.Attendance:1408` (Rotation overlap cannot be adjusted). |
| `WA-EFP-011` | Boundary: Inverted dates (`endDate < startDate`) | NEG | `startDate: 2026-12-20`, `endDate: 2026-12-10` | `400 Bad Request` | Date range validation failure. |
| `WA-EFP-012` | Negative: Non-existent detail `id` | NEG | Random UUID | `404 Not Found` | Detail map not found (`1401`). |
| `WA-EFP-013` | Negative: Deactivated detail row (`IsActive: false`) | NEG | Attempt to edit period of deactivated row | `400 Bad Request` | Cannot edit deactivated assignment. |
| `WA-EFP-014` | Negative: Missing `startDate` in body | DTO | Body omits `startDate` | `400 Bad Request` | Mandatory field missing. |
| `WA-EFP-015` | DTO Leak: Inject client-supplied `id` or `isDeleted` | DTO | Body includes `"isDeleted": true` | `400 / Ignored` | DTO injection blocked. |
| `WA-EFP-016` | DB Invariant: Header dates synchronization check | DB | Modify detail row dates | `200 OK` | Check if Header document dates remain untouched (Header = cohort envelope). |

---

### 5.11 Endpoint 11: POST /workassignments/details/{id}/move/check-conflicts (Move Preflight)
- **Route:** `POST /api/companies/{companyId}/workassignments/details/{id}/move/check-conflicts?locationId={locationId}`
- **DTO:** `MoveEmployeeDto`
- **Scope:** Read-only preflight check before moving an employee to another target.

| Test Case ID | Test Scenario Description | Category | Target Configuration | Expected HTTP | Expected Response / DB State |
| :--- | :--- | :---: | :--- | :---: | :--- |
| `WA-MVC-001` | Positive: Move preflight to another Regular Work Plan (Clean) | POS | `targetType: "WorkPlan"`, valid `targetWorkPlanId`, clean | `200 OK` | `canProceed: true`, `hasConflicts: false`, `requiresAdjustment: false`. |
| `WA-MVC-002` | Positive: Move preflight to a Roster Board | POS | `targetType: "Board"`, valid `targetBoardId` | `200 OK` | Preflight verifies board membership and schedule readiness. |
| `WA-MVC-003` | Positive: Move preflight to a Shift Rotation + Team | POS | `targetType: "Rotation"`, `targetRotationId`, `targetTeamId` | `200 OK` | Preflight verifies rotation cycle compatibility. |
| `WA-MVC-004` | Move Overlap: Target has existing regular overlap | BUS | Target plan overlaps existing assignment | `200 OK` | `canProceed: true`, `requiresAdjustment: true`, button becomes "Adjust & Move". |
| `WA-MVC-005` | Move Block: Employee held by Roster Board shift | BUS | Employee scheduled on Roster board in new period | `200 OK` | `canProceed: false`, `heldByBoardOrRotation: true`, `reason: "Roster overlap"`. |
| `WA-MVC-006` | Boundary: Effective From earlier than tomorrow (`effectiveFrom <= today`) | NEG | `effectiveFrom: today` | `400 Bad Request` | `Cit.Attendance:Validation` (Move effectiveFrom must be tomorrow or later). |
| `WA-MVC-007` | Target Validation: `targetType: "WorkPlan"` without `targetWorkPlanId` | NEG | `targetType: "WorkPlan"`, `targetWorkPlanId: null` | `400 Bad Request` | Missing target work plan ID. |
| `WA-MVC-008` | Target Validation: `targetType: "Board"` without `targetBoardId` | NEG | `targetType: "Board"`, `targetBoardId: null` | `400 Bad Request` | Missing target board ID. |
| `WA-MVC-009` | Target Validation: `targetType: "Rotation"` without `targetTeamId` | NEG | `targetType: "Rotation"`, `targetTeamId: null` | `400 Bad Request` | Missing target team ID for rotation. |
| `WA-MVC-010` | Invalid Target Enum: `targetType: "InvalidType"` or `999` | NEG | `targetType: "Random"` | `400 Bad Request` | Enum deserialization failure. |
| `WA-MVC-011` | Non-Existent Target: `targetWorkPlanId` does not exist | NEG | Random UUID | `400 / 404` | Target plan not found (`1301`). |
| `WA-MVC-012` | Database Isolation: 0 mutations during preflight | DB | Run move preflight | `200 OK` | MongoDB completely unchanged. |

---

### 5.12 Endpoint 12: PATCH /workassignments/details/{id}/move (Execute Move Across Targets)
- **Route:** `PATCH /api/companies/{companyId}/workassignments/details/{id}/move?locationId={locationId}`
- **DTO:** `MoveEmployeeDto`
- **Scope:** Executes employee move: cuts/deactivates source row, and creates target assignment.

| Test Case ID | Test Scenario Description | Category | Target & Conflict Parameters | Expected HTTP | Expected Response / DB State |
| :--- | :--- | :---: | :--- | :---: | :--- |
| `WA-MOV-001` | Positive: Move to another Regular Work Plan (Clean) | POS | `targetType: "WorkPlan"`, `effectiveFrom: tomorrow` | `200 OK` | Source map ends day before `effectiveFrom`. New map created for target plan. Returns `createdWorkAssignmentId`. |
| `WA-MOV-002` | Positive: Move unstarted assignment (`startDate > today`) | BUS | Move assignment that has not started yet | `200 OK` | Source map marked `IsActive: false`. Target map created from `effectiveFrom`. |
| `WA-MOV-003` | Positive: Move with regular overlap (`adjustConflicts: true`) | BUS | Target has regular overlap; `adjustConflicts: true` | `200 OK` | Overlaps cut; source terminated; target assigned. |
| `WA-MOV-004` | Negative: Move with regular overlap but `adjustConflicts: false` | NEG | Overlap exists; `adjustConflicts: false` | `400 Bad Request` | `Cit.Attendance:1409` (Adjustment not confirmed). |
| `WA-MOV-005` | Hard Block: Target overlaps Roster Board shift | BUS | Employee scheduled on Roster | `400 Bad Request` | `Cit.Attendance:1408` (Held by board/rotation). Move aborted. |
| `WA-MOV-006` | Positive: Move to Roster Board (`targetType: "Board"`) | BUS | `targetType: "Board"`, valid `targetBoardId` | `200 OK` | Source regular map ends; employee added to board membership. Returns `targetMembershipId`. |
| `WA-MOV-007` | Positive: Move to Shift Rotation (`targetType: "Rotation"`) | BUS | `targetType: "Rotation"`, `targetRotationId`, `targetTeamId` | `200 OK` | Source regular map ends; employee enrolled into rotation team. Returns `targetMembershipId`. |
| `WA-MOV-008` | Target Plan Incompatible: Target is Rotation Plan on `targetType: "WorkPlan"` | NEG | `targetWorkPlanId` is Rotation Plan | `400 Bad Request` | `Cit.Attendance:1104` (Incompatible plan type). |
| `WA-MOV-009` | Target Location Mismatch: Move to target plan at different location | SEC | Target plan belongs to Location 2 | `400 Bad Request` | Move only permitted within same location. |
| `WA-MOV-010` | Negative: Effective From earlier than tomorrow | NEG | `effectiveFrom: today` | `400 Bad Request` | Must be tomorrow or later. |
| `WA-MOV-011` | Negative: Non-existent source detail `id` | NEG | Random UUID | `404 Not Found` | Detail map not found (`1401`). |
| `WA-MOV-012` | Negative: Move already deactivated detail row | NEG | Source row has `IsActive: false` | `400 Bad Request` | Cannot move inactive assignment. |
| `WA-MOV-013` | DB Invariant: Source row truncation verified | DB | Inspect source `WorkAssignmentMaps` | `200 OK` | Source `EndDate` set to `effectiveFrom - 1 day`. |
| `WA-MOV-014` | DB Invariant: Target map snapshot integrity | DB | Inspect new `WorkAssignmentMaps` | `200 OK` | Target map has correct `WorkPlanData` matching target plan. |
| `WA-MOV-015` | Concurrency: Double move race condition | CON | Concurrent move requests on same detail ID | `200 / 409` | First succeeds; second rejected with `400/409`. |
| `WA-MOV-016` | Rollback Integrity: Failure during target creation rolls back source cut | DB | Simulate target error | `500 / 400` | Source map must NOT remain truncated if target creation fails. |

---

### 5.13 Endpoint 13: PATCH /workassignments/details/{id}/remove (Deactivate Assignment Row)
- **Route:** `PATCH /api/companies/{companyId}/workassignments/details/{id}/remove?locationId={locationId}`
- **Scope:** Deactivates an employee's assignment row (`IsActive: false`).

| Test Case ID | Test Scenario Description | Category | Parameters | Expected HTTP | Expected Response / DB State |
| :--- | :--- | :---: | :--- | :---: | :--- |
| `WA-REM-001` | Positive: Remove active assignment detail row | POS | Valid `companyId`, `locationId`, active detail `id` | `200 OK` | Row deactivated. MongoDB `WorkAssignmentMaps` has `IsActive: false`. |
| `WA-REM-002` | Positive: Remove future/upcoming assignment detail row | POS | Detail row where `startDate > today` | `200 OK` | Row deactivated. Will not appear in upcoming queries. |
| `WA-REM-003` | Idempotency / Double Remove: Remove already deactivated row | NEG | Detail row where `IsActive == false` | `400 / 200` | Verify whether API rejects or silently succeeds. |
| `WA-REM-004` | Negative: Non-existent detail `id` | NEG | Random non-existent UUID | `404 Not Found` | `Cit.Attendance:1401`. |
| `WA-REM-005` | Negative: Missing `locationId` query parameter | NEG | Omitted `locationId` | `400 Bad Request` | Missing location validation. |
| `WA-REM-006` | Negative: Location mismatch between URL and detail row | SEC | Location 1 in URL, detail row belongs to Location 2 | `400 / 404` | Cross-location tampering blocked. |
| `WA-REM-007` | Database Invariant: Header document unaffected | DB | Deactivate 1 detail row out of 5 | `200 OK` | `WorkAssignments` header remains intact; other 4 detail maps active. |
| `WA-REM-008` | Database Invariant: All detail rows deactivated leaves header empty | DB | Deactivate all detail rows for a header | `200 OK` | Header remains, but upcoming queries omit it (`activeEmployeeCount == 0`). |
| `WA-REM-009` | Database Invariant: Audit trail populated | DB | Inspect deactivated row in Mongo | `200 OK` | `ModifiedAt` updated; `IsActive: false` persisted; historical dates intact. |
| `WA-REM-010` | Security: Unauthorized removal without bearer token | SEC | No token provided | `401 Unauthorized` | Rejected. |

---

## 6. Cross-Cutting BVA, DTO Schema Invariants & Multi-Tenancy Security

| Test Case ID | Test Category | Target Endpoint | Description & Payload / Query Manipulation | Expected HTTP & Invariant Assertion |
| :--- | :--- | :--- | :--- | :--- |
| `WA-SEC-001` | Cross-Tenant Probe | `POST /workassignments` | Pass `companyId` belonging to Tenant B while authenticated as Tenant A. | `403 Forbidden` / `404 Not Found`. Multi-tenant boundary enforced. |
| `WA-SEC-002` | Cross-Company Policy Leak | `POST /workassignments` | Assign a plan embedding a Policy belonging to a different company. | `400 Bad Request` / Cross-company policy rejected. |
| `WA-SEC-003` | Cross-Location Employee Leak | `POST /workassignments` | Include `employeeId` registered at Location 2 into assignment for Location 1. | `400 Bad Request` / Employee not at location. |
| `WA-DTO-001` | DTO Schema Injection | `POST /workassignments` | Inject `"isDeleted": true` and `"id": "00000000-..."` in body. | Server ignores or rejects fields; generates fresh UUID. |
| `WA-DTO-002` | Empty JSON Body | `POST /workassignments` | Transmit empty body `{}`. | `400 Bad Request` with structured `validationErrors`. |
| `WA-DTO-003` | Null Body | `POST /workassignments` | Transmit `null` body. | `400 Bad Request` (not unhandled 500 NullReferenceException). |
| `WA-DTO-004` | Non-JSON Content-Type | `POST /workassignments` | Send request with `Content-Type: text/plain` or `application/xml`. | `415 Unsupported Media Type`. |
| `WA-BVA-001` | Massive Employee Array | `POST /workassignments` | Submit payload with 500 employee UUIDs. | `200 OK` (handles batch persistence transactionally). |
| `WA-BVA-002` | Duplicate Employees in Array | `POST /workassignments` | Submit `employeeIds: [E1, E1, E1]`. | Dedupes to single map or returns `400 Duplicate employee`. |
| `WA-BVA-003` | Max Future Date Boundary | `POST /workassignments` | `startDate: "9999-12-30"`, `endDate: "9999-12-31"`. | Evaluates without integer/datetime overflow crashes. |
| `WA-BVA-004` | Leap Year Date Boundary | `POST /workassignments` | `startDate: "2028-02-29"`, `endDate: "2028-03-01"`. | Handled cleanly as valid leap day. |
| `WA-BVA-005` | Year Transition Boundary | `POST /workassignments` | `startDate: "2026-12-31"`, `endDate: "2027-01-01"`. | Spanning year boundary handled seamlessly. |

---

## 7. MongoDB Cross-Collection Integrity & Denormalization Checklist

Whenever a Work Assignment is created, adjusted, moved, or deleted, verify these MongoDB collection states:

```
Sahab.ERP.Attendance
├── WorkAssignments (Header)
│   ├── _id: UUID (Server-generated)
│   ├── CompanyId: UUID
│   ├── LocationId: UUID
│   ├── WorkPlanId: UUID
│   ├── WorkPlanName: { en: "...", ar: "..." }
│   ├── StartDate: ISODate (UTC 00:00:00)
│   ├── EndDate: ISODate (9999-12-31 for open-ended)
│   ├── Status: Int (1 = Active, 2 = Completed, etc.)
│   ├── IsActive: Boolean (true)
│   ├── IsDeleted: Boolean (false)
│   └── (NO employee array stored here!)
│
├── WorkAssignmentMaps (Employee Detail Rows)
│   ├── _id: UUID (Server-generated)
│   ├── AssignmentType: Int (1 = Regular, 2 = Roster, 3 = Rotation)
│   ├── WorkAssignmentId: UUID (Points back to WorkAssignments._id)
│   ├── EmployeeId: UUID
│   ├── EmployeeCode: String
│   ├── EmployeeName: { en: "...", ar: "..." }
│   ├── Department: { en: "...", ar: "..." }
│   ├── Designation: { en: "...", ar: "..." }
│   ├── LocationId: UUID
│   ├── StartDate: ISODate
│   ├── EndDate: ISODate
│   ├── Status: Int
│   ├── IsActive: Boolean
│   ├── HolidayCalendarId: UUID (Location's calendar for start year)
│   └── WorkPlanData: Object (FULL EMBEDDED COPY OF PLAN, TEMPLATE & POLICIES!)
│
└── WorkPlans
    └── HasWorkAssignments: Boolean (Flipped to true on first assignment!)
```

---
*Report generated and validated for Senior QA Execution against DEV microservice cluster.*
"""

reports_path = os.path.join('reports', 'WORK_ASSIGNMENT_TEST_CASES.md')
with open(reports_path, 'w', encoding='utf-8') as f:
    f.write(content)

print(f"Generated {reports_path} ({len(content):,} bytes)")
