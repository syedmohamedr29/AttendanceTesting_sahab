import openpyxl
import sys

sys.stdout.reconfigure(encoding='utf-8')

wb_path = 'AttendanceTestCases_Master_Consolidated.xlsx'
wb = openpyxl.load_workbook(wb_path)
ws = wb['User Scenarios (Add Here)']

# Row 129: USER-128
r128 = 129
ws.cell(row=r128, column=9).value = 'Fail'
ws.cell(row=r128, column=10).value = (
    "[Re-Verified 2026-11-04 on Attendance 3 - DEFECT-20261026-01]: NOT FIXED. "
    "Re-queried GET /api/company/companies/3a247435-e31d-ef15-8cc9-62c587f4eb3f/getChecklist on Company Service. "
    "workSchedulesCreated remains False despite active CDWT in Attendance Service. Integration event still missing."
)

# Row 130: USER-129
r129 = 130
ws.cell(row=r129, column=9).value = 'Fail'
ws.cell(row=r129, column=10).value = (
    "[Re-Verified 2026-11-04 on Attendance 3 - DEFECT-20261026-02]: NOT FIXED. "
    "Attendance 3 v1.0 document cf2e401b-... created with clean payload persists TenantName: {} (empty object). "
    "Server-side auto-population from _currentTenant.Name is still not implemented."
)

# Row 131: USER-130
r130 = 131
ws.cell(row=r130, column=9).value = 'Fail'
ws.cell(row=r130, column=10).value = (
    "[Re-Verified 2026-11-04 on Attendance 3 - DEFECT-20261026-03]: NOT FIXED. "
    "Attendance 3 templates (v1.0, v2.0, v3.0) persist CreatedBy: 'syed.mohamed@comm-it.in' as a plain string email "
    "instead of structured composite identity object. Alignment with Khalid pending."
)

# Row 132: USER-131
r131 = 132
ws.cell(row=r131, column=9).value = 'Fail'
ws.cell(row=r131, column=10).value = (
    "[Re-Verified 2026-11-04 on Attendance 3 - DEFECT-20261026-04]: NOT FIXED. "
    "Sent PATCH /worktemplates/fixed/27aa7562-... with tenantName: {'en': 'Re-verified Spoofed Tenant 04-Nov'}. "
    "Server returned HTTP 200 OK and created v3.0 document 56262fcf-... storing spoofed TenantName into MongoDB."
)

wb.save(wb_path)
print("Updated AttendanceTestCases_Master_Consolidated.xlsx rows 129-132 successfully.")

