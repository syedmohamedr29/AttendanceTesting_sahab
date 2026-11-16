# -*- coding: utf-8 -*-

live_db_sample = """
### Live Verified Sample Pair (Attendance 11 — 13-Nov-2026):
1. **Header Record in `ERP.Attendance.WorkAssignments` (`f9e467c6-fd79-4066-87f6-b4262419c5f8`):**
   - `CompanyId`: `3a24e5e5-302e-91bd-feaa-b07979766dfe` (`Attendance 11`)
   - `LocationId`: `3a24e666-df63-3dc7-0ea7-02ec8be341e7` (`Dammam` / `الدمام`)
   - `WorkPlanId`: `a1ae96cd-587b-4145-8859-3b42877ea4a5` (`Default Work Plan`)
   - `StartDate`: `2026-11-13T00:00:00Z`
   - `EndDate`: `9999-12-31T00:00:00Z` (Open-ended null serialization)
   - `Status`: `1` (Active), `IsActive`: `true`
   - Holds **NO employee array**.

2. **Detail Map Record in `ERP.Attendance.WorkAssignmentMaps` (`b9e30791-da83-4d65-8c3f-25faa251360a`):**
   - `_t`: `["WorkAssignmentMap", "RegularWorkAssignmentMap"]`, `AssignmentType`: `1`
   - `WorkAssignmentId`: `f9e467c6-fd79-4066-87f6-b4262419c5f8` (Matches header above 100%)
   - `EmployeeId`: `f9e1a6d5-6bd5-7d46-ae85-38b81dc80887`
   - `EmployeeCode`: `"SA-EMP-0001"`, `EmployeeName`: `"Faisal Al-Qahtani Al-Qahtani"`
   - `Department`: `GENW` ("Gen Engineer"), `Designation`: `AIENG` ("AI Engineer")
   - `WorkPlanData`: Embeds full snapshot copy of template `LOC0002` (3,240 min, 7 FixedTimeSlots).
"""

with open('reports/WORK_ASSIGNMENT_BUSINESS_VALIDATION.md', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('## 8. Test Data Prerequisites & Execution Checklist')
if idx != -1:
    new_text = text[:idx] + live_db_sample + '\n\n---\n\n' + text[idx:]
    with open('reports/WORK_ASSIGNMENT_BUSINESS_VALIDATION.md', 'w', encoding='utf-8') as f:
        f.write(new_text)
    print('Updated reports/WORK_ASSIGNMENT_BUSINESS_VALIDATION.md with live sample')
else:
    print('ERROR: Section 8 not found in reports/WORK_ASSIGNMENT_BUSINESS_VALIDATION.md')
