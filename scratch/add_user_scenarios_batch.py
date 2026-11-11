import openpyxl, sys
sys.stdout.reconfigure(encoding='utf-8')

wb_path = 'AttendanceTestCases_Master_Consolidated.xlsx'
wb = openpyxl.load_workbook(wb_path)
ws = wb['User Scenarios (Add Here)']

# USER-02: TenantName hardcoded placeholder
ws.cell(row=3, column=2, value="Master Data - Tenant Name Persistence")
ws.cell(row=3, column=3, value="Verify TenantName in ERP.Attendance.WorkTemplates reflects actual tenant name instead of hardcoded placeholder")
ws.cell(row=3, column=4, value="Create Company Default WT (POST /worktemplates/fixed). Inspect MongoDB document in Sahab > ERP.Attendance.WorkTemplates")
ws.cell(row=3, column=5, value="TenantName should be populated with actual tenant name (e.g., {'en': 'Attendance', 'ar': 'شركة افتراضية'} or tenant name from token/Identity Svc).")
ws.cell(row=3, column=6, value="P1")
ws.cell(row=3, column=7, value="data-integrity")
ws.cell(row=3, column=8, value="dev")
ws.cell(row=3, column=9, value="Failed (Defect)")
ws.cell(row=3, column=10, value="DEFECT: TenantName is hardcoded to {'en': 'Placeholder Tenant', 'ar': 'شركة افتراضية'} in MongoDB after template creation. Should resolve actual tenant.")
ws.cell(row=3, column=11, value="User Custom (QA Exploratory)")

# USER-03: CreatedBy format consistency
ws.cell(row=4, column=2, value="Audit Trail - CreatedBy Formatting & Consistency")
ws.cell(row=4, column=3, value="Verify CreatedBy field across modules stores standard identity format (Email vs User GUID vs Object)")
ws.cell(row=4, column=4, value="Create entities across WorkTemplates, WorkPlans, Policies, Assignments under authenticated JWT token")
ws.cell(row=4, column=5, value="CreatedBy format should be consistent across all collections (document whether string email, GUID, or full user identity object is expected).")
ws.cell(row=4, column=6, value="P2")
ws.cell(row=4, column=7, value="consistency")
ws.cell(row=4, column=8, value="dev")
ws.cell(row=4, column=9, value="Clarification Needed")
ws.cell(row=4, column=10, value="Currently stores plain email (e.g. syed.mohamed@comm-it.in). Engineering clarification required if login ID/user GUID should be included.")
ws.cell(row=4, column=11, value="User Custom (QA Exploratory)")

# USER-04: API Design Inconsistency on Scoping Parameters
ws.cell(row=5, column=2, value="API Design - Scoping Parameters Consistency")
ws.cell(row=5, column=3, value="Verify scoping parameters (tenantId, companyId, locationId) follow uniform REST convention across all modules")
ws.cell(row=5, column=4, value="Compare POST /worktemplates/fixed (body contains tenantId, companyId, locationId) vs WorkPlans/Assignments (query/route only)")
ws.cell(row=5, column=5, value="All modules should follow unified convention: companyId in route, locationId in query, tenantId from JWT token. Body parameters should be deprecated.")
ws.cell(row=5, column=6, value="P2")
ws.cell(row=5, column=7, value="design-consistency")
ws.cell(row=5, column=8, value="dev")
ws.cell(row=5, column=9, value="Open Suggestion")
ws.cell(row=5, column=10, value="Fixed WT body leaks tenantId/companyId/locationId into request DTO. Recommend standardizing on Route/Query params.")
ws.cell(row=5, column=11, value="User Custom (QA Architecture)")

wb.save(wb_path)
print("Successfully added USER-02, USER-03, USER-04 to Master Consolidated Excel!")

