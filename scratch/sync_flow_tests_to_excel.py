# -*- coding: utf-8 -*-
import openpyxl
from copy import copy

flow_test_cases = [
    ("WA-FLOW-001", "E. End-to-End POST & PATCH Sequence Flows", "Clean Creation Flow (Happy Path)", 
     "Step 1: POST /check-conflicts [E1, E2] clean -> Step 2: POST /workassignments [E1, E2]", 
     "Step 1: allowedEmployeeIds [E1, E2], canProceed: true. Step 2: HTTP 200 OK, 1 Header in WorkAssignments + 2 Maps in WorkAssignmentMaps.", "P0", "smoke", "dev"),
    
    ("WA-FLOW-002", "E. End-to-End POST & PATCH Sequence Flows", "Mixed Cohort POST & Adjust Flow", 
     "Step 1: /check-conflicts (E1 clean, E2 adjustable) -> Step 2: POST /workassignments -> Step 3: POST /adjust", 
     "Step 1: E2 adjustable. Step 2: E1 assigned, E2 returned in conflictedEmployeeIds. Step 3: E2 old regular map cut/split, new map created.", "P0", "regression", "dev"),
    
    ("WA-FLOW-003", "E. End-to-End POST & PATCH Sequence Flows", "Blocked Roster/Rotation Overlap Flow", 
     "Step 1: /check-conflicts (E_rost blocked) -> Attempt Step 3: POST /adjust directly", 
     "Step 1: blockedEmployeeIds [E_rost], canProceed: false. Step 3: HTTP 400 Cit.Attendance:1408 (Cannot adjust Roster/Rotation overlap). Zero DB cuts.", "P0", "negative", "dev"),
    
    ("WA-FLOW-004", "E. End-to-End POST & PATCH Sequence Flows", "Atomic Batch Adjust Failure Flow", 
     "Cohort of 5 employees: 4 regular overlap, 1 Roster overlap. Submit all 5 to POST /adjust", 
     "Entire request rejected with HTTP 400 Cit.Attendance:1408. Atomic Rollback: 0 old rows cut; none of the 4 valid employees assigned.", "P1", "negative", "dev"),
    
    ("WA-FLOW-005", "E. End-to-End POST & PATCH Sequence Flows", "Out-of-Order Execution: Adjust Before Create", 
     "Call POST /workassignments/adjust with non-existent or un-created workAssignmentId", 
     "HTTP 400/404 Work assignment not found. Enforces Header must exist prior to adjustment.", "P1", "negative", "dev"),
    
    ("WA-FLOW-006", "E. End-to-End POST & PATCH Sequence Flows", "Payload Date Mismatch in POST Flow", 
     "Step 1: Header created for Dec 01-31 -> Step 2: POST /adjust payload sends Jan 01-31", 
     "HTTP 400 Bad Request. Adjust dates must strictly match the referenced Header dates.", "P1", "negative", "dev"),
    
    ("WA-FLOW-007", "E. End-to-End POST & PATCH Sequence Flows", "Effective Period Edit Flow (Future Shift)", 
     "Step 1: GET /current-plans -> Step 2: POST /check-conflicts?skipAssignmentId={id} -> Step 3: PATCH .../effective-period", 
     "Step 2: hasConflicts: false. Step 3: HTTP 200 OK. WorkAssignmentMaps dates updated in-place; Header dates remain cohort envelope.", "P0", "regression", "dev"),
    
    ("WA-FLOW-008", "E. End-to-End POST & PATCH Sequence Flows", "Active Assignment Start-Date Lock Flow", 
     "Step 1: Ongoing assignment (startDate <= today) -> Step 2: PATCH .../effective-period modify startDate -> Step 3: modify endDate only", 
     "Step 2: HTTP 400 Cit.Attendance:1406 (Cannot modify start date of active assignment). Step 3: HTTP 200 OK (endDate modified).", "P0", "business", "dev"),
    
    ("WA-FLOW-009", "E. End-to-End POST & PATCH Sequence Flows", "Move to Regular Work Plan Flow", 
     "Step 1: POST .../move/check-conflicts (WorkPlan) -> Step 2: PATCH .../move (adjustConflicts: true)", 
     "Step 1: canProceed: true. Step 2: HTTP 200 OK, createdWorkAssignmentId. Source map ends effectiveFrom-1 day; Target map created.", "P0", "regression", "dev"),
    
    ("WA-FLOW-010", "E. End-to-End POST & PATCH Sequence Flows", "Move to Roster Board Flow", 
     "Step 1: POST .../move/check-conflicts (Board) -> Step 2: PATCH .../move (targetType: Board)", 
     "Step 1: canProceed: true. Step 2: HTTP 200 OK, targetMembershipId. Source regular map ends; employee added to Roster Board membership.", "P0", "regression", "dev"),
    
    ("WA-FLOW-011", "E. End-to-End POST & PATCH Sequence Flows", "Move to Shift Rotation Flow", 
     "Step 1: POST .../move/check-conflicts (Rotation) -> Step 2: PATCH .../move (targetType: Rotation)", 
     "Step 1: canProceed: true. Step 2: HTTP 200 OK, targetMembershipId. Source regular map ends; employee enrolled into rotation team.", "P0", "regression", "dev"),
    
    ("WA-FLOW-012", "E. End-to-End POST & PATCH Sequence Flows", "Move Unstarted Assignment Flow", 
     "Assignment starting next month (startDate > today). Move executed with effectiveFrom: tomorrow", 
     "Source map marked IsActive: false (deactivated, not truncated). New target assignment begins from effectiveFrom.", "P1", "edge", "dev"),
    
    ("WA-FLOW-013", "E. End-to-End POST & PATCH Sequence Flows", "Move Unconfirmed Adjustment Rejection", 
     "Target plan has regular overlap. Caller sends adjustConflicts: false in PATCH .../move", 
     "HTTP 400 Cit.Attendance:1409 (Adjustment not confirmed). Source row untouched; move aborted.", "P1", "negative", "dev"),
    
    ("WA-FLOW-014", "E. End-to-End POST & PATCH Sequence Flows", "Employee Removal Lifecycle Flow", 
     "Step 1: GET /details/{id} -> Step 2: PATCH /details/{id}/remove -> Step 3: GET /details?state=active vs inactive", 
     "Step 2: HTTP 200 OK. WorkAssignmentMaps sets IsActive: false. Step 3: omitted from state=active; present in state=inactive.", "P0", "regression", "dev"),
    
    ("WA-FLOW-015", "E. End-to-End POST & PATCH Sequence Flows", "Double Move / Race Condition Guard", 
     "Step 1: PATCH .../move to Plan B -> Step 2: Replay same move on original detail id", 
     "First call HTTP 200 OK. Second call HTTP 400/404 (Source detail row already terminated/inactive).", "P1", "concurrency", "dev"),
]

excels = [
    'AttendanceTestCases_Master_Consolidated.xlsx',
    'AttendanceTestCases.xlsx',
    'Attendance_Policies_Manual_API_TestCases_MongoDB.xlsx'
]

for ef in excels:
    wb = openpyxl.load_workbook(ef)
    ws = wb['Work Assignments']
    
    # check if already added
    existing_ids = set()
    for r in range(2, ws.max_row + 1):
        v = ws.cell(row=r, column=1).value
        if v:
            existing_ids.add(str(v).strip())
            
    added_count = 0
    ref_row = ws.max_row
    for item in flow_test_cases:
        tc_id = item[0]
        if tc_id not in existing_ids:
            row_idx = ws.max_row + 1
            for col_idx, val in enumerate(item, start=1):
                cell = ws.cell(row=row_idx, column=col_idx, value=val)
                # copy style from previous row
                ref_cell = ws.cell(row=ref_row, column=col_idx)
                if ref_cell.has_style:
                    cell.font = copy(ref_cell.font)
                    cell.border = copy(ref_cell.border)
                    cell.fill = copy(ref_cell.fill)
                    cell.alignment = copy(ref_cell.alignment)
            added_count += 1
            
    wb.save(ef)
    print(f'{ef} -> Added {added_count} flow test cases. Total rows now: {ws.max_row}')
    wb.close()
