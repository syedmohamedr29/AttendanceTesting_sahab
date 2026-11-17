import openpyxl

wb_path = 'AttendanceTestCases_Master_Consolidated.xlsx'
wb = openpyxl.load_workbook(wb_path)
ws = wb['User Scenarios (Add Here)']

updates = {
    3: "[Live Verified 16-Nov-2026 - DEFECT-20261028-05 / DEFECT-20261026-02]: STILL NOT FIXED. TenantName persists as Object (empty) {} in MongoDB Sahab.ERP.Attendance.WorkTemplates. Synced to Confluence Row 2.",
    5: "[Live Verified 16-Nov-2026 - DEFECT-20261028-06 / DEFECT-20261026-04]: STILL NOT FIXED. All 26 POST/PATCH DTOs expose tenantName and accept client spoofing with 200 OK. Synced to Confluence Row 4.",
    123: "[Live Verified 16-Nov-2026 - DEFECT-20261028-06 / USER-122]: STILL NOT FIXED. PATCH endpoints accept client-spoofed tenantName with HTTP 200 OK. Synced to Confluence Row 4.",
    130: "[Live Verified 16-Nov-2026 - DEFECT-20261028-05 / USER-129]: STILL NOT FIXED. Fresh templates persist TenantName: {} (empty object). Ambient tenant pre-population still missing. Synced to Confluence Row 2.",
    132: "[Live Verified 16-Nov-2026 - DEFECT-20261028-06 / USER-131]: STILL NOT FIXED. PATCH requests with client-supplied tenantName accepted with 200 OK. Synced to Confluence Row 4."
}

for row_idx, note in updates.items():
    ws.cell(row=row_idx, column=10).value = note
    print(f"Updated Row {row_idx}: {ws.cell(row=row_idx, column=1).value}")

wb.save(wb_path)
print("Successfully updated AttendanceTestCases_Master_Consolidated.xlsx for User Scenarios!")
