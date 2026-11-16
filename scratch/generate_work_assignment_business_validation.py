# -*- coding: utf-8 -*-
import os

content = """# 🏢 Work Assignments Module — Business & Overlap Invariant Validation Dossier

> **Target Microservices:** `SP.AttendanceSvc` (.NET 9) & `SP.CompanySvc` (.NET 8)  
> **Target Database:** MongoDB `Sahab` (`ERP.Attendance.WorkAssignments`, `ERP.Attendance.WorkAssignmentMaps`, `ERP.Attendance.WorkPlans`)  
> **Environment:** DEV (`sp.dev.zoolwork.com` / `gw8.dev.zoolwork.com`)  
> **QA Level:** Senior Staff QA Automation & Microservice Specialist  

---

## 📑 Table of Contents
1. [Core Business Architecture: The "Copies, Not Links" Model](#1-core-business-architecture-the-copies-not-links-model)
2. [Conflict Detection & Categorization Engine](#2-conflict-detection--categorization-engine)
3. [The 4 Overlap Cutting Behaviors (Detailed Date Walkthroughs)](#3-the-4-overlap-cutting-behaviors-detailed-date-walkthroughs)
4. [Cross-Schedule Move Transitions (Polymorphic Move Engine)](#4-cross-schedule-move-transitions-polymorphic-move-engine)
5. [Effective Period Lifecycle & Immutability Rules](#5-effective-period-lifecycle--immutability-rules)
6. [Temporal Evaluation Rules for GET /current-plans](#6-temporal-evaluation-rules-for-get-current-plans)
7. [MongoDB Audit & Cross-Collection Consistency Verification](#7-mongodb-audit--cross-collection-consistency-verification)
8. [Test Data Prerequisites & Execution Checklist](#8-test-data-prerequisites--execution-checklist)

---

## 1. Core Business Architecture: The "Copies, Not Links" Model

The Sahab Attendance platform operates on a strict **snapshot / denormalized copy model**:

```
[Template] ──embedded copy──► [WorkPlan] ──embedded copy──► [WorkAssignmentMaps] ◄── [WorkAssignments]
                                                              (Single Source of Truth)  (Cohort Header)
```

1. **Why Copies?**
   - Payroll, overtime, and punctuality calculations are historical facts. An employee working an 8-hour shift on October 1st cannot have their historical calculation altered because HR changed the underlying Work Template or Break Policy on November 15th.
2. **Where Does the Snapshot Live?**
   - The snapshot lives in `ERP.Attendance.WorkAssignmentMaps.WorkPlanData`.
   - It captures the template name, short code, daily schedule duration, fixed time slots, break windows, and embedded policy rules (Overtime, Grace Period, Breaks).
3. **Immutability of In-Use Plans:**
   - Once a Work Plan is referenced by an assignment map, it cannot be deleted (`DELETE /workplans/{id}` returns `400 Cit.Attendance:1304`).
   - If a Work Plan is updated via `PATCH`, only template swaps propagate to assignment maps; name and policy edits do **not** propagate (documented as `DEFECT-20261112-08`).

---

## 2. Conflict Detection & Categorization Engine

Whenever an assignment action (create, edit, or move) is initiated, the engine executes a preflight collision check against `ERP.Attendance.WorkAssignmentMaps` for the target employee at the specified location.

| Collision Category | Source of Overlap | Allowed to Proceed? | Can be Adjusted? | System Action / Error Code |
| :--- | :--- | :---: | :---: | :--- |
| 🟢 **Allowed (Clean)** | None (no active rows in range) | **YES** | N/A | Assignment created immediately. |
| 🟡 **Adjustable** | Existing **Regular Work Plan** at the same location | **YES** (with confirmation) | **YES** | Old regular row is cut/split via `/adjust`. New row created. |
| 🔴 **Blocked** | **Roster Board** shift or **Shift Rotation** step | **NO** | **NO** | Preflight returns `canProceed: false`. Adjust/Move rejected with **`Cit.Attendance:1408`**! |

> [!IMPORTANT]
> **Strict Atomic Rejection on Batch Adjust:**
> If a batch of 10 employees is submitted to `POST /workassignments/adjust`, and **even 1 employee** has a Blocked overlap (Roster or Rotation), the microservice must reject the **entire request** with HTTP 400 `Cit.Attendance:1408`. It must never perform a partial adjust!

---

## 3. The 4 Overlap Cutting Behaviors (Detailed Date Walkthroughs)

When an overlap with an existing Regular Work Plan is confirmed for adjustment, `POST /workassignments/adjust` applies one of four deterministic geometric cutting algorithms to the existing `WorkAssignmentMaps` row:

### Strategy 1: Ends Early
- **Condition:** Old assignment starts before the new period and ends inside it.
- **Formula:** `OldRow.EndDate = NewStart - 1 day`
- **Example:**
  - Existing Assignment: `2026-10-01` → `2026-12-15` (General Shift)
  - New Assignment: `2026-12-01` → `2026-12-31` (Night Shift)
  - **Result in DB:**
    - Modified Old Row: `2026-10-01` → `2026-11-30` (General Shift)
    - New Row Created: `2026-12-01` → `2026-12-31` (Night Shift)

### Strategy 2: Split (Cut & Resume)
- **Condition:** Old assignment starts before the new period and runs past its end date.
- **Formula:**
  - Segment 1: `OldRow.EndDate = NewStart - 1 day`
  - Middle: New Assignment Created `NewStart` → `NewEnd`
  - Segment 2: New Resumed Row Created `OldRow_Resumed.StartDate = NewEnd + 1 day`, `EndDate = OldEnd`
- **Example:**
  - Existing Assignment: `2026-10-01` → `2027-03-31` (General Shift)
  - New Assignment: `2026-12-01` → `2026-12-31` (Night Shift)
  - **Result in DB:**
    - Truncated Old Row: `2026-10-01` → `2026-11-30` (General Shift)
    - New Row: `2026-12-01` → `2026-12-31` (Night Shift)
    - Resumed Old Row: `2027-01-01` → `2027-03-31` (General Shift)

### Strategy 3: Starts Later
- **Condition:** Old assignment starts inside a closed new period and runs past its end.
- **Formula:** `OldRow.StartDate = NewEnd + 1 day`
- **Example:**
  - Existing Assignment: `2026-12-15` → `2027-03-31` (General Shift)
  - New Assignment: `2026-12-01` → `2026-12-31` (Night Shift)
  - **Result in DB:**
    - Modified Old Row: `2027-01-01` → `2027-03-31` (General Shift)
    - New Row: `2026-12-01` → `2026-12-31` (Night Shift)

### Strategy 4: Completely Encompassed (Deactivated)
- **Condition:** Old assignment lies completely inside the new assignment window.
- **Formula:** `OldRow.IsActive = false`, `Status = Inactive` (Kept for audit trail)
- **Example:**
  - Existing Assignment: `2026-12-05` → `2026-12-20` (General Shift)
  - New Assignment: `2026-12-01` → `2026-12-31` (Night Shift)
  - **Result in DB:**
    - Old Row: Marked `IsActive: false`
    - New Row: `2026-12-01` → `2026-12-31` (Night Shift)

---

## 4. Cross-Schedule Move Transitions (Polymorphic Move Engine)

The Move Employee API (`PATCH /workassignments/details/{id}/move`) is a polymorphic transition engine that can move an employee off their current regular plan into one of three target schedule types:

```
                          ┌──────────────────────────┐
                          │ Current Regular Detail   │
                          │   (WorkAssignmentMap)    │
                          └─────────────┬────────────┘
                                        │
           ┌────────────────────────────┼────────────────────────────┐
           ▼                            ▼                            ▼
[TargetType: 2 WorkPlan]      [TargetType: 1 Board]       [TargetType: 3 Rotation]
- Source row ends E-1 day     - Source row ends E-1 day    - Source row ends E-1 day
- Creates new Regular Map     - Adds employee to Board     - Enrolls in Rotation Team
- Returns createdAssignmentId - Returns targetMembershipId - Returns targetMembershipId
```

### Move Invariants:
1. **Effective Date Floor:** `effectiveFrom` cannot be earlier than **tomorrow** (`effectiveFrom > today`).
2. **Unstarted Move:** If the current assignment has not started yet (`startDate > today`), moving the employee permanently deactivates the source row (`IsActive: false`) instead of shortening it.
3. **Location Scoping:** The move target must belong to the **same location** as the source assignment. Cross-location moves must be rejected.
4. **Target Compatibility:** `targetType: "WorkPlan"` accepts only Regular Work Plans (`PlanType=1`). If the caller supplies a Rotation or Roster plan ID, the request must fail with `Cit.Attendance:1104`.

---

## 5. Effective Period Lifecycle & Immutability Rules

Modifying an employee's assignment dates via `PATCH /details/{id}/effective-period` follows strict temporal state guards:

| Current Row Status | Start Date Modifiable? | End Date Modifiable? | Date Constraints | Target Error if Violated |
| :--- | :---: | :---: | :--- | :--- |
| **Upcoming** (`startDate > today`) | **YES** | **YES** | `startDate >= today`<br>`endDate >= startDate` | `400 Cit.Attendance:1405` |
| **Active / Ongoing** (`startDate <= today`) | ❌ **LOCKED** | **YES** | `startDate` must remain unchanged.<br>`endDate >= today` | `400 Cit.Attendance:1406` |
| **Past / Expired** (`endDate < today`) | ❌ **LOCKED** | ❌ **LOCKED** | Cannot edit historical completed periods. | `400 Cit.Attendance:1406` |
| **Deactivated** (`IsActive == false`) | ❌ **LOCKED** | ❌ **LOCKED** | Cannot edit deactivated rows. | `400 Bad Request` |

---

## 6. Temporal Evaluation Rules for GET /current-plans

The endpoint `GET /api/companies/{companyId}/workassignments/current-plans` is the core query powering employee pickers across the UI:
1. **Resolution Hierarchy:**
   - On date `D`, if an employee has multiple active maps (e.g. during an ongoing transition), the system returns the active map covering `D` with the **latest start date**.
2. **Plan Type Tagging:**
   - The response returns the active plan with its underlying type: `"Regular"`, `"Roster"`, or `"Rotation"`.
3. **Defaulting:**
   - If `asOf` is omitted, the system evaluates against the current UTC date.
   - If the employee has no assignment on `D`, the response returns a clean null entry for that employee, never a 404 error.

---

## 7. MongoDB Audit & Cross-Collection Consistency Verification

When running automated test suites, verify the following database invariants in MongoDB `Sahab`:

```javascript
// 1. Verify Header Record
db.getSiblingDB("Sahab").getCollection("ERP.Attendance.WorkAssignments").findOne({
  "_id": UUID("..."),
  "CompanyId": UUID("..."),
  "LocationId": UUID("..."),
  "WorkPlanId": UUID("..."),
  "IsDeleted": false
});

// 2. Verify Employee Detail Maps (Points back via WorkAssignmentId)
db.getSiblingDB("Sahab").getCollection("ERP.Attendance.WorkAssignmentMaps").find({
  "WorkAssignmentId": UUID("..."),
  "AssignmentType": 1,
  "IsActive": true
});

// 3. Verify Embedded WorkPlanData Snapshot
var map = db.getSiblingDB("Sahab").getCollection("ERP.Attendance.WorkAssignmentMaps").findOne({
  "EmployeeId": UUID("...")
});
assert(map.WorkPlanData != null, "WorkPlanData snapshot must be embedded!");
assert(map.WorkPlanData.WorkTemplate != null, "WorkTemplate snapshot must be embedded!");
assert(map.WorkPlanData.Policies != null, "Policies snapshot must be embedded!");
```

---

## 8. Test Data Prerequisites & Execution Checklist

Before executing the Work Assignment test cases:
1. Ensure a valid Company exists (e.g. `Attendance 10` `3a249872-e23c-a401-7d8b-4a8049ac8c9b`).
2. Ensure active Locations exist under the Company.
3. Ensure at least one Regular Work Plan exists with an embedded Fixed Work Template.
4. Ensure active Employees exist in the Employee Hierarchy for the target location.
5. Store the active Bearer token in `scratch/current_token.json`.
"""

bv_path = os.path.join('reports', 'WORK_ASSIGNMENT_BUSINESS_VALIDATION.md')
with open(bv_path, 'w', encoding='utf-8') as f:
    f.write(content)

print(f"Generated {bv_path} ({len(content):,} bytes)")
