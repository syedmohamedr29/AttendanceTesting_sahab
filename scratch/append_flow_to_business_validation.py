# -*- coding: utf-8 -*-

flow_section = """
---

## 9. End-to-End POST & PATCH API Execution Protocol & Flow State Machines

### A. The 3-Step POST Workflow (Creation & Conflict Resolution)
Every Work Assignment creation follows an atomic 3-step sequence:

```
[UI Selection] 
       │
       ▼
[Step 1: POST /workassignments/check-conflicts]
       │
       ├─► 🔴 Blocked (Roster / Rotation) ────► UI disables 'Add' (Must deselect)
       │
       ├─► 🟢 All Clean (No overlaps) ────────► [Step 2: POST /workassignments] ──► Done (Header + Maps created)
       │
       └─► 🟡 Adjustable (Regular overlap) ──► [Step 2: POST /workassignments]
                                                        │ (Assigns Clean, returns conflictedEmployeeIds)
                                                        ▼
                                               [Step 3: POST /workassignments/adjust]
                                                  (Cuts old rows, assigns conflicted to Header)
```

1. **Step 1: `POST /check-conflicts?locationId=`**
   - **Mode:** Read-only simulation (Zero DB mutations).
   - **Validation:** Enforces `startDate >= today` (unless `enforceFutureStart=false`), `endDate >= startDate`, and non-empty employee array.
2. **Step 2: `POST /workassignments?locationId=`**
   - **Mode:** Partial commit.
   - **Execution:** Writes `ERP.Attendance.WorkAssignments` header. Creates `WorkAssignmentMaps` **only for clean employees**. Returns conflicted IDs.
3. **Step 3: `POST /workassignments/adjust?locationId=`**
   - **Mode:** Transactional adjustment.
   - **Precondition:** Requires valid `workAssignmentId` returned from Step 2.
   - **Execution:** Cuts old overlapping regular rows and creates new maps attached to the header. Rejects entire request with `Cit.Attendance:1408` if any employee is on Roster/Rotation.

---

### B. The 3 PATCH Lifecycle Flows (Maintenance & Transitions)

```
[Active Assignment Row (WorkAssignmentMap)]
       │
       ├─► Edit Dates: 
       │     1. POST /check-conflicts?skipAssignmentId={id}&enforceFutureStart=false
       │     2. PATCH /details/{id}/effective-period?locationId=...
       │        (Locked start date if started; adjustConflicts cuts overlaps)
       │
       ├─► Move Employee: 
       │     1. POST /details/{id}/move/check-conflicts?locationId=...
       │     2. PATCH /details/{id}/move?locationId=...
       │        (Old row ends effectiveFrom-1 day; Target Regular/Board/Rotation created)
       │
       └─► Remove Employee:
             1. PATCH /details/{id}/remove?locationId=...
                (Sets IsActive: false; preserves audit history)
```

| Flow Type | Preflight API | Primary Execution API | Core Invariant Enforced |
| :--- | :--- | :--- | :--- |
| **Edit Effective Period** | `POST /check-conflicts` with `skipAssignmentId={id}` | `PATCH /details/{id}/effective-period` | If `startDate <= today`, start date is **LOCKED** (`Cit.Attendance:1406`). Only `endDate` can be changed. |
| **Move Employee** | `POST /details/{id}/move/check-conflicts` | `PATCH /details/{id}/move` | `effectiveFrom` must be **tomorrow or later**. Old row terminates the day before. |
| **Remove Employee** | None (direct) | `PATCH /details/{id}/remove` | Sets `IsActive: false`. Does not delete historical document. |
"""

with open('reports/WORK_ASSIGNMENT_BUSINESS_VALIDATION.md', 'r', encoding='utf-8') as f:
    text = f.read()

# Add to TOC
toc_target = '8. [Test Data Prerequisites & Execution Checklist](#8-test-data-prerequisites--execution-checklist)\n'
toc_addition = '9. [End-to-End POST & PATCH API Execution Protocol & Flow State Machines](#9-end-to-end-post--patch-api-execution-protocol--flow-state-machines)\n'
new_text = text.replace(toc_target, toc_target + toc_addition)
new_text += flow_section

with open('reports/WORK_ASSIGNMENT_BUSINESS_VALIDATION.md', 'w', encoding='utf-8') as f:
    f.write(new_text)

print('Updated reports/WORK_ASSIGNMENT_BUSINESS_VALIDATION.md with Section 9')
