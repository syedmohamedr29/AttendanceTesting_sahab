# -*- coding: utf-8 -*-
import re

flow_section = """
### 5.14 End-to-End Multi-Step Workflow & Sequence Test Cases (POST & PATCH Flows)
- **Scope:** Validates multi-step, transactional sequence integrity between Preview, Create, Adjust, Edit, Move, and Remove endpoints.
- **Methodology:** Workflow Integration, State Transition Verification, Out-of-Order Execution Traps, and Cross-Step Data Propagation.

| Test Case ID | Workflow Stage & Title | Flow Sequence & Endpoint Order | Input Preconditions & Payloads | Expected System & Database Result |
| :--- | :--- | :--- | :--- | :--- |
| `WA-FLOW-001` | **Clean Creation Flow (Happy Path)** | **Step 1:** `POST /check-conflicts`<br>⬇️<br>**Step 2:** `POST /workassignments` | **Step 1:** Check conflicts for clean `[E1, E2]`.<br>**Step 2:** Call create with clean `[E1, E2]`, `startDate: tomorrow`, `endDate: null`. | • Step 1 returns `allowedEmployeeIds: [E1, E2]`, `canProceed: true`.<br>• Step 2 creates 1 Header in `WorkAssignments` + 2 Maps in `WorkAssignmentMaps`.<br>• `conflictedEmployeeIds: []`. |
| `WA-FLOW-002` | **Mixed Cohort POST & Adjust Flow** | **Step 1:** `POST /check-conflicts`<br>⬇️<br>**Step 2:** `POST /workassignments`<br>⬇️<br>**Step 3:** `POST /workassignments/adjust` | **Step 1:** Cohort with Clean `E1` and Overlapping Regular `E2`.<br>**Step 2:** Submit both to create.<br>**Step 3:** Submit `E2` + returned `workAssignmentId` to adjust. | • Step 1 flags `E2` as `adjustable`.<br>• Step 2 creates Header + Map for `E1` ONLY; returns `conflictedEmployeeIds: [E2]`.<br>• Step 3 cuts `E2`'s old regular map and creates new map attached to Header. |
| `WA-FLOW-003` | **Blocked Roster/Rotation Overlap Flow** | **Step 1:** `POST /check-conflicts`<br>⬇️<br>**Step 2:** `POST /workassignments/adjust` (Bypass check) | **Step 1:** Employee `E_rost` scheduled on Roster Board.<br>**Step 2:** Attempt to call `POST /adjust` directly on `E_rost`. | • Step 1 returns `blockedEmployeeIds: [E_rost]`, `canProceed: false`.<br>• Step 2 strictly rejected with **HTTP 400 `Cit.Attendance:1408`** ("Cannot adjust Roster/Rotation overlap"). Zero DB cuts! |
| `WA-FLOW-004` | **Atomic Batch Adjust Failure Flow** | **Step 1:** `POST /workassignments`<br>⬇️<br>**Step 2:** `POST /workassignments/adjust` | Cohort of 5 employees: 4 have regular plan overlaps, 1 has a Roster overlap. Submit all 5 to `/adjust`. | • Entire `/adjust` request rejected with **HTTP 400 `Cit.Attendance:1408`**.<br>• **Atomic Rollback:** 0 old rows cut; none of the 4 valid employees assigned. |
| `WA-FLOW-005` | **Out-of-Order Execution Trap: Adjust Before Create** | **Direct Call:** `POST /workassignments/adjust` | Call `POST /adjust` with a random non-existent `workAssignmentId` or without calling `POST /workassignments` first. | • Rejected with **HTTP 400/404 `Work assignment not found`**.<br>• Enforces that header must exist before adjustment can execute. |
| `WA-FLOW-006` | **Payload Date Mismatch in POST Flow** | **Step 1:** `POST /workassignments`<br>⬇️<br>**Step 2:** `POST /workassignments/adjust` | **Step 1:** Header created for `2026-12-01` → `2026-12-31`.<br>**Step 2:** Adjust payload sends mismatched dates `2027-01-01` → `2027-01-31`. | • Rejected with **HTTP 400 Bad Request**.<br>• Adjust dates must strictly match the referenced Header's dates. |
| `WA-FLOW-007` | **Effective Period Edit Flow (Future Shift)** | **Step 1:** `GET /current-plans`<br>⬇️<br>**Step 2:** `POST /check-conflicts?skipAssignmentId={id}`<br>⬇️<br>**Step 3:** `PATCH /details/{id}/effective-period` | **Step 1:** Verify future row `2026-12-15` → `2027-01-15`.<br>**Step 2:** Run preflight with `skipAssignmentId`.<br>**Step 3:** PATCH with new clean dates `2026-12-20` → `2027-01-31`. | • Step 2 returns `hasConflicts: false`.<br>• Step 3 returns `200 OK`. `WorkAssignmentMaps` dates updated in-place.<br>• Header dates remain cohort envelope. |
| `WA-FLOW-008` | **Active Assignment Start-Date Lock Flow** | **Step 1:** Inspect ongoing row<br>⬇️<br>**Step 2:** `PATCH /details/{id}/effective-period` (Violate lock)<br>⬇️<br>**Step 3:** `PATCH /details/{id}/effective-period` (Valid edit) | **Step 1:** Assignment started yesterday (`startDate <= today`).<br>**Step 2:** Attempt to modify `startDate`.<br>**Step 3:** Modify `endDate` only. | • Step 2 rejected with **HTTP 400 `Cit.Attendance:1406`** (Cannot modify start date of active assignment).<br>• Step 3 accepted with **HTTP 200 OK** (`endDate` updated). |
| `WA-FLOW-009` | **Move to Regular Work Plan Flow** | **Step 1:** `POST /details/{id}/move/check-conflicts`<br>⬇️<br>**Step 2:** `PATCH /details/{id}/move` | **Step 1:** Preflight with `targetType: "WorkPlan"`, `effectiveFrom: tomorrow`.<br>**Step 2:** Execute move with `adjustConflicts: true`. | • Step 1 returns `canProceed: true`.<br>• Step 2 returns `200 OK`, `createdWorkAssignmentId`.<br>• Source map ends `effectiveFrom - 1 day`; Target map created from `effectiveFrom`. |
| `WA-FLOW-010` | **Move to Roster Board Flow** | **Step 1:** `POST /details/{id}/move/check-conflicts`<br>⬇️<br>**Step 2:** `PATCH /details/{id}/move` | **Step 1:** Preflight with `targetType: "Board"`, valid `targetBoardId`.<br>**Step 2:** Execute move with `adjustConflicts: true`. | • Step 1 returns `canProceed: true`.<br>• Step 2 returns `200 OK`, `targetMembershipId`.<br>• Source regular map ends `effectiveFrom - 1 day`; Employee added to Roster Board membership. |
| `WA-FLOW-011` | **Move to Shift Rotation Flow** | **Step 1:** `POST /details/{id}/move/check-conflicts`<br>⬇️<br>**Step 2:** `PATCH /details/{id}/move` | **Step 1:** Preflight with `targetType: "Rotation"`, `targetRotationId`, `targetTeamId`.<br>**Step 2:** Execute move. | • Step 1 returns `canProceed: true`.<br>• Step 2 returns `200 OK`, `targetMembershipId`.<br>• Source regular map ends `effectiveFrom - 1 day`; Employee enrolled into rotation team. |
| `WA-FLOW-012` | **Move Unstarted Assignment Flow** | **Step 1:** Verify unstarted row<br>⬇️<br>**Step 2:** `PATCH /details/{id}/move` | Assignment with `startDate > today` (e.g. starts next month). Move executed with `effectiveFrom: tomorrow`. | • Source map is marked **`IsActive: false`** (completely deactivated, not truncated).<br>• New target assignment begins from `effectiveFrom`. |
| `WA-FLOW-013` | **Move Unconfirmed Adjustment Rejection** | **Step 1:** `POST /details/{id}/move/check-conflicts`<br>⬇️<br>**Step 2:** `PATCH /details/{id}/move` (adjustConflicts: false) | Target plan has regular overlap (`requiresAdjustment: true`). Caller sends `adjustConflicts: false` in Step 2. | • Step 2 rejected with **HTTP 400 `Cit.Attendance:1409`** ("Adjustment not confirmed").<br>• Source row untouched; move aborted. |
| `WA-FLOW-014` | **Employee Removal Lifecycle Flow** | **Step 1:** `GET /details/{id}`<br>⬇️<br>**Step 2:** `PATCH /details/{id}/remove`<br>⬇️<br>**Step 3:** `GET /details?state=active` vs `state=inactive` | Active assignment row `id`. Execute remove, then verify state queries and MongoDB. | • Step 1 confirms active row.<br>• Step 2 returns `200 OK`. `WorkAssignmentMaps` sets `IsActive: false`.<br>• Step 3: Row omitted from `state=active`; present in `state=inactive`. |
| `WA-FLOW-015` | **Double Move / Race Condition Guard** | **Step 1:** `PATCH /details/{id}/move`<br>⬇️<br>**Step 2:** `PATCH /details/{id}/move` (Replay) | Execute move to Plan B. Replay the same move request on the original source detail `id`. | • First call succeeds (`200 OK`).<br>• Second call fails with **HTTP 400/404** (Source detail row already terminated/inactive). |
"""

with open('reports/WORK_ASSIGNMENT_TEST_CASES.md', 'r', encoding='utf-8') as f:
    text = f.read()

# Insert before Section 6
idx = text.find('## 6. Cross-Cutting BVA, DTO Schema Invariants')
if idx != -1:
    new_text = text[:idx] + flow_section + '\n---\n\n' + text[idx:]
    # Update TOC
    toc_target = '   - [5.13 Endpoint 13: PATCH /workassignments/details/{id}/remove (Deactivate Assignment Row)](#513-endpoint-13-patch-workassignmentsdetailsidremove-deactivate-assignment-row)\n'
    toc_addition = '   - [5.14 End-to-End Multi-Step Workflow & Sequence Test Cases (POST & PATCH Flows)](#514-end-to-end-multi-step-workflow--sequence-test-cases-post--patch-flows)\n'
    new_text = new_text.replace(toc_target, toc_target + toc_addition)
    
    # Update title count from 158 to 173
    new_text = new_text.replace('158 Comprehensive Scenarios', '173 Comprehensive Scenarios')
    new_text = new_text.replace('158 Test Cases', '173 Test Cases')
    new_text = new_text.replace('158 comprehensive test scenarios', '173 comprehensive test scenarios')
    
    with open('reports/WORK_ASSIGNMENT_TEST_CASES.md', 'w', encoding='utf-8') as f:
        f.write(new_text)
    print('Updated reports/WORK_ASSIGNMENT_TEST_CASES.md with Flow Section 5.14 (15 new TCs, total 173 TCs)')
else:
    print('ERROR: Section 6 not found in reports/WORK_ASSIGNMENT_TEST_CASES.md')
