import openpyxl
from datetime import datetime
import sys

sys.stdout.reconfigure(encoding='utf-8')

wb_path = 'AttendanceTestCases_Master_Consolidated.xlsx'
wb = openpyxl.load_workbook(wb_path)
ws = wb['User Scenarios (Add Here)']

remarks_text = (
    "[Re-Verified 2026-11-04 - DEFECT-20261026-04]: NOT FIXED. Exhaustively tested all 6 Work Template endpoints "
    "(POST/PATCH across Fixed, Flexi, Split). All 6 endpoints accept client-spoofed tenantName with HTTP 200 OK and "
    "persist it directly into MongoDB (ERP.Attendance.WorkTemplates). All 6 Swagger DTO schemas still declare tenantName."
)

updated_count = 0
for r in range(2, ws.max_row + 1):
    tc_id = ws.cell(row=r, column=1).value
    if tc_id in ['USER-04', 'USER-122', 'USER-131']:
        # Update Status to Fail (confirming still open)
        ws.cell(row=r, column=9).value = 'Fail'
        # Update QA Remarks (column 10)
        ws.cell(row=r, column=10).value = remarks_text
        updated_count += 1
        print(f"Updated row {r}: {tc_id}")

wb.save(wb_path)
print(f"Successfully saved {wb_path} with {updated_count} rows updated.")

