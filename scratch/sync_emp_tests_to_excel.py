# -*- coding: utf-8 -*-
import openpyxl
from copy import copy

emp_test_cases = [
    ("WA-EMP-001", "F. Employee Lifecycle, DOJ & Location Integrity", "Active Employee Assigned On/After DOJ", 
     "IsActive: true, Status: 1 (Active), DOJ: 2026-11-01. startDate: 2026-11-13, endDate: null", 
     "HTTP 200 OK. Assignment Header & Detail Map created in WorkAssignmentMaps.", "P0", "smoke", "dev"),
    
    ("WA-EMP-002", "F. Employee Lifecycle, DOJ & Location Integrity", "Assignment Start Date Precedes DOJ", 
     "IsActive: true, DOJ: 2026-12-01 (Future hire). startDate: 2026-11-13 (Before DOJ)", 
     "HTTP 400 Bad Request Cit.Attendance:Validation. Work assignment startDate cannot precede employee DateOfJoining.", "P0", "negative", "dev"),
    
    ("WA-EMP-003", "F. Employee Lifecycle, DOJ & Location Integrity", "Inactive Employee Assignment Blocked", 
     "IsActive: false, Status: 1. startDate: 2026-11-13, employeeIds: [EMP_INACTIVE]", 
     "HTTP 400 Bad Request Cit.Attendance:Validation. Inactive employee cannot be assigned to a work plan.", "P0", "negative", "dev"),
    
    ("WA-EMP-004", "F. Employee Lifecycle, DOJ & Location Integrity", "Offboarded/Terminated Employee Blocked", 
     "IsActive: false, Status: 6 (Terminated). startDate: 2026-11-13, employeeIds: [EMP_OFFBOARDED]", 
     "HTTP 400 Bad Request Cit.Attendance:Validation. Terminated/Offboarded employee cannot be assigned.", "P0", "negative", "dev"),
    
    ("WA-EMP-005", "F. Employee Lifecycle, DOJ & Location Integrity", "Offboarding Employee Open-Ended Blocked", 
     "IsActive: true, Status: 5 (Notice Period), LWD: 2026-11-30. startDate: 2026-11-13, endDate: null", 
     "HTTP 400 Bad Request Cit.Attendance:Validation. Cannot create open-ended assignment for offboarding employee.", "P1", "negative", "dev"),
    
    ("WA-EMP-006", "F. Employee Lifecycle, DOJ & Location Integrity", "Offboarding Employee Closed Assignment Allowed", 
     "IsActive: true, Status: 5, LWD: 2026-11-30. startDate: 2026-11-13, endDate: 2026-11-25 (Before LWD)", 
     "HTTP 200 OK. Allowed because assignment completes prior to employee Last Working Day.", "P1", "business", "dev"),
    
    ("WA-EMP-007", "F. Employee Lifecycle, DOJ & Location Integrity", "Offboarding Employee Exceeding LWD Blocked", 
     "IsActive: true, Status: 5, LWD: 2026-11-30. startDate: 2026-11-13, endDate: 2026-12-15 (Past LWD)", 
     "HTTP 400 Bad Request Cit.Attendance:Validation. Assignment endDate cannot exceed employee last working day.", "P1", "negative", "dev"),
    
    ("WA-EMP-008", "F. Employee Lifecycle, DOJ & Location Integrity", "Cross-Location Employee Assignment Blocked", 
     "Employee registered at Location 1 (Chennai). Attempt to assign to Plan at Location 2 (Dammam)", 
     "HTTP 400 Bad Request Cit.Attendance:Validation. Employee does not belong to specified work location.", "P0", "negative", "dev"),
    
    ("WA-EMP-009", "F. Employee Lifecycle, DOJ & Location Integrity", "Cross-Company Employee Assignment Blocked", 
     "Employee registered under Company A. Route specifies Company B", 
     "HTTP 400 Bad Request. Multi-tenant company boundary enforced.", "P0", "security", "dev"),
    
    ("WA-EMP-010", "F. Employee Lifecycle, DOJ & Location Integrity", "Start Date Exactly on DOJ Boundary", 
     "IsActive: true, DOJ: 2026-11-13. startDate: 2026-11-13, endDate: null", 
     "HTTP 200 OK. Edge boundary permitted: employee assigned on exact joining day.", "P1", "boundary", "dev"),
    
    ("WA-EMP-011", "F. Employee Lifecycle, DOJ & Location Integrity", "Start Date 1 Day Before DOJ Boundary", 
     "IsActive: true, DOJ: 2026-11-14. startDate: 2026-11-13, endDate: null", 
     "HTTP 400 Bad Request. Off-by-one boundary strictly caught and rejected.", "P1", "boundary", "dev"),
    
    ("WA-EMP-012", "F. Employee Lifecycle, DOJ & Location Integrity", "Today Start Date Boundary (startDate == today)", 
     "IsActive: true, DOJ: 2025-01-01. startDate: 2026-11-13, endDate: null", 
     "HTTP 200 OK. Assignment active immediately (Status: 1, IsActive: true in WorkAssignmentMaps).", "P0", "smoke", "dev"),
    
    ("WA-EMP-013", "F. Employee Lifecycle, DOJ & Location Integrity", "Non-Existent Location ID in Query", 
     "Valid employee and plan. Query ?locationId=00000000-0000-0000-0000-000000000000", 
     "HTTP 400/404 Location not found.", "P1", "negative", "dev"),
    
    ("WA-EMP-014", "F. Employee Lifecycle, DOJ & Location Integrity", "Location Belongs to Different Company", 
     "Route companyId: Company A, query locationId: Company B location", 
     "HTTP 400 Bad Request Cit.Attendance:9002 (Location does not match entity company).", "P1", "security", "dev"),
    
    ("WA-EMP-015", "F. Employee Lifecycle, DOJ & Location Integrity", "Work Plan Embeds Rotation Template", 
     "workPlanId references Rotation Work Template (TemplateType=5)", 
     "HTTP 400 Bad Request Cit.Attendance:1104 (Incompatible template type for regular assignment).", "P0", "business", "dev"),
    
    ("WA-EMP-016", "F. Employee Lifecycle, DOJ & Location Integrity", "Work Plan Embeds Roster Template", 
     "workPlanId references Roster Work Template (TemplateType=4)", 
     "HTTP 400 Bad Request Cit.Attendance:1104 (Incompatible template type for regular assignment).", "P0", "business", "dev"),
    
    ("WA-EMP-017", "F. Employee Lifecycle, DOJ & Location Integrity", "Prerequisite Employee Setup in Employee8 DB", 
     "Query EmployeeSvcNET8test.Employee collection prior to test execution", 
     "Verify IsActive == true, WorkLocation._id == locationId, DateOfJoining <= startDate.", "P1", "prerequisite", "dev"),
    
    ("WA-EMP-018", "F. Employee Lifecycle, DOJ & Location Integrity", "Prerequisite Teardown & Schedule Isolation", 
     "Post-test cleanup of WorkAssignments and WorkAssignmentMaps test documents", 
     "Restores employee schedule to baseline without orphaned records.", "P1", "teardown", "dev"),
]

excels = [
    'AttendanceTestCases_Master_Consolidated.xlsx',
    'AttendanceTestCases.xlsx',
    'Attendance_Policies_Manual_API_TestCases_MongoDB.xlsx'
]

for ef in excels:
    wb = openpyxl.load_workbook(ef)
    ws = wb['Work Assignments']
    
    existing_ids = set()
    for r in range(2, ws.max_row + 1):
        v = ws.cell(row=r, column=1).value
        if v:
            existing_ids.add(str(v).strip())
            
    added_count = 0
    ref_row = ws.max_row
    for item in emp_test_cases:
        tc_id = item[0]
        if tc_id not in existing_ids:
            row_idx = ws.max_row + 1
            for col_idx, val in enumerate(item, start=1):
                cell = ws.cell(row=row_idx, column=col_idx, value=val)
                ref_cell = ws.cell(row=ref_row, column=col_idx)
                if ref_cell.has_style:
                    cell.font = copy(ref_cell.font)
                    cell.border = copy(ref_cell.border)
                    cell.fill = copy(ref_cell.fill)
                    cell.alignment = copy(ref_cell.alignment)
            added_count += 1
            
    wb.save(ef)
    print(f'{ef} -> Added {added_count} emp lifecycle test cases. Total rows now: {ws.max_row}')
    wb.close()
