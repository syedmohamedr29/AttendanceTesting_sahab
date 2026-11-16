# -*- coding: utf-8 -*-
import openpyxl

excel_files = [
    'AttendanceTestCases_Master_Consolidated.xlsx',
    'AttendanceTestCases.xlsx',
    'Attendance_Policies_Manual_API_TestCases_MongoDB.xlsx'
]

# Results mapping by TC ID prefix or exact TC ID
live_status = {
    # GET suite
    'WA-GET-001': ('Pass', 'HTTP 200 OK verified. Returns active work assignments array.'),
    'WA-GET-002': ('Pass', 'HTTP 200 OK verified. Returns empty array for clean location.'),
    'WA-GET-004': ('Pass', 'HTTP 400 Bad Request verified when locationId omitted.'),
    'WA-UP-001': ('Pass', 'HTTP 200 OK verified. Upcoming assignments returned.'),
    'WA-UP-002': ('Fail', 'BUG-WA-01: Returns 200 OK instead of 400 when locationId omitted.'),
    'WA-GETID-001': ('Pass', 'HTTP 200 OK verified for existing header.'),
    'WA-GETID-002': ('Pass', 'HTTP 404 Not Found verified for non-existent GUID.'),
    'WA-DET-001': ('Pass', 'HTTP 200 OK verified with workAssignmentDetails array.'),
    'WA-DET-003': ('Fail', 'BUG-WA-02: Returns 200 OK across all locations instead of 400.'),
    'WA-DETID-001': ('Pass', 'HTTP 200 OK verified for existing detail map b9e30791...'),
    'WA-CUR-001': ('Pass', 'HTTP 200 OK verified for temporal point-in-time plan query.'),
    
    # CHK suite
    'WA-CHK-001': ('Pass', 'HTTP 200 OK verified. hasConflicts=false, canProceed=true.'),
    'WA-CHK-002': ('Pass', 'HTTP 200 OK verified. hasConflicts=true, resolution=EndsEarly calculated.'),
    'WA-CHK-007': ('Pass', 'HTTP 400 Bad Request verified. Cit.Attendance:1405 past date blocked.'),
    'WA-CHK-008': ('Pass', 'HTTP 200 OK verified when enforceFutureStart=false.'),
    'WA-CHK-010': ('Pass', 'HTTP 400 Bad Request verified for inverted dates (endDate < startDate).'),
    'WA-CHK-011': ('Pass', 'HTTP 400 Bad Request verified for empty employeeIds array.'),
    
    # CRT suite
    'WA-CRT-001': ('Pass', 'HTTP 200 OK verified. Header and Detail Map persisted in MongoDB.'),
    'WA-CRT-002': ('Fail', 'BUG-WA-03: Inactive employee returns 200 OK and creates Orphaned Header with 0 Maps.'),
    
    # EMP suite
    'WA-EMP-001': ('Pass', 'HTTP 200 OK verified for active employee on/after DOJ.'),
    'WA-EMP-002': ('Fail', 'BUG-WA-03: Inactive employee check-conflicts returns canProceed=true.'),
    'WA-EMP-007': ('Pass', 'HTTP 400 Bad Request verified. startDate < DOJ blocked with Cit.Attendance:1405.'),
    'WA-EMP-008': ('Pass', 'HTTP 200 OK verified for startDate == DOJ.'),
    'WA-EMP-009': ('Pass', 'HTTP 200 OK verified for startDate > DOJ.'),
    'WA-EMP-010': ('Pass', 'HTTP 200 OK verified via Swagger PUT /api/Employees/activateemployees. MongoDB confirmed IsActive=true, Status=2.'),
    'WA-EMP-003': ('Pass', 'Offboard invariant tested. Offboard blocked by EmployeeSvc:60003 (Salary prerequisite required).'),
    'WA-EMP-005': ('Pass', 'Exit guard verified. Blocked by EmpSvc_Employee_NotInOffboardingState.'),
    
    # EFP, MOV, REM
    'WA-EFP-001': ('Pass', 'HTTP 200 OK verified. MongoDB confirmed EndDate updated to 2026-12-31.'),
    'WA-MOV-001': ('Pass', 'HTTP 400 Bad Request verified. Move to same plan rejected with Cit.Attendance:1104.'),
    'WA-REM-001': ('Fail', 'BUG-WA-04: PATCH /details/{id}/remove returns HTTP 404 Not Found.')
}

for ef in excel_files:
    wb = openpyxl.load_workbook(ef)
    for sname in ['Work Assignments (Master 203)', 'Work Assignments']:
        if sname in wb.sheetnames:
            ws = wb[sname]
            updated = 0
            for row in ws.iter_rows(min_row=2):
                tc_id = str(row[0].value).strip() if row[0].value else ''
                if tc_id in live_status:
                    status, remarks = live_status[tc_id]
                    row[8].value = status    # Status column (col 9, index 8)
                    row[9].value = remarks   # QA Remarks column (col 10, index 9)
                    updated += 1
            print(f"Updated {updated} live results in {ef} -> '{sname}'")
    wb.save(ef)
    print(f"Saved {ef}")
