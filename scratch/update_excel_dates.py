import openpyxl, sys
sys.stdout.reconfigure(encoding='utf-8')

wb = openpyxl.load_workbook('AttendanceTestCases_Master_Consolidated.xlsx')
ws = wb['User Scenarios (Add Here)']

# Check headers
headers = [cell.value for cell in ws[1]]
print("Current headers:", headers)

# Update rows with Date Logged in QA Remarks / Section
# USER-01: Found 26-Oct-2026
ws.cell(row=2, column=10, value="[Found: 26-Oct-2026] DEFECT: After default work schedule is created, WorkSchedulesCreated in CompaniesMaster (Company Service) remains false. Missing event/callback.")

# USER-02: Found 26-Oct-2026
ws.cell(row=3, column=10, value="[Found: 26-Oct-2026] DEFECT: TenantName is hardcoded to {'en': 'Placeholder Tenant', 'ar': 'شركة افتراضية'} in MongoDB Sahab > ERP.Attendance.WorkTemplates.")

# USER-03: Found 27-Oct-2026
ws.cell(row=4, column=10, value="[Found: 27-Oct-2026] DTO/AUDIT ISSUE: CreatedBy stores plain email (syed.mohamed@comm-it.in) while other collections (e.g. TaskApprovals) store composite object with LoginId/Employee.")

# USER-04: Found 27-Oct-2026
ws.cell(row=5, column=10, value="[Found: 27-Oct-2026] DTO DESIGN ISSUE: POST /worktemplates/fixed accepts tenantId, companyId, locationId in body DTO, whereas all other modules use Route/Query/Token.")

wb.save('AttendanceTestCases_Master_Consolidated.xlsx')
print("Successfully updated dates in Master Consolidated Excel!")

