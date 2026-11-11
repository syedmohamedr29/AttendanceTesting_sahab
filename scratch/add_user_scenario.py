import openpyxl, sys
sys.stdout.reconfigure(encoding='utf-8')

wb_path = 'AttendanceTestCases_Master_Consolidated.xlsx'
wb = openpyxl.load_workbook(wb_path)
ws = wb['User Scenarios (Add Here)']

# Row 2 is USER-01
ws.cell(row=2, column=2, value="Cross-Service Integration - Company Checklist Sync")
ws.cell(row=2, column=3, value="Verify CompanyChecklist.WorkSchedulesCreated in CompanyMaster collection updates to true upon creating Company Default Work Schedule")
ws.cell(row=2, column=4, value="Preconditions: New or active company with CompanyChecklist.WorkSchedulesCreated == false. Body: POST /api/companies/{companyId}/worktemplates/fixed (valid Sun-Thu 09:00-17:00, no locationId)")
ws.cell(row=2, column=5, value="1. Attendance DB: ERP.Attendance.WorkTemplates inserts CDWT (IsDefault=true, v1.0) and cascades N location templates.\n2. Attendance DB: ERP.Attendance.WorkPlans inserts N LOCWOPL default plans.\n3. Company Service DB: CompanyMaster.CompanyChecklist.WorkSchedulesCreated is updated from false to true.")
ws.cell(row=2, column=6, value="P1")
ws.cell(row=2, column=7, value="integration")
ws.cell(row=2, column=8, value="dev")
ws.cell(row=2, column=9, value="Failed (Defect)")
ws.cell(row=2, column=10, value="DEFECT: After default work schedule is created (HTTP 200), CompanyChecklist.WorkSchedulesCreated in CompanyMaster remains false. Integration event/callback to SP.CompanySvc is missing or failing.")
ws.cell(row=2, column=11, value="User Custom (QA Handover)")

wb.save(wb_path)
print("Successfully updated USER-01 in AttendanceTestCases_Master_Consolidated.xlsx!")

