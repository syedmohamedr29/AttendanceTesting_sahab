import sys
import openpyxl
from openpyxl.styles import PatternFill, Font

sys.stdout.reconfigure(encoding='utf-8')

fail_fill = PatternFill(start_color="FEE2E2", end_color="FEE2E2", fill_type="solid")
fail_font = Font(name="Calibri", size=9, bold=True, color="991B1B")

for wb_path in [
    "AttendanceTestCases_Master_Consolidated.xlsx",
    "Attendance_Policies_Manual_API_TestCases_MongoDB.xlsx"
]:
    wb = openpyxl.load_workbook(wb_path)
    sheet_name = "Policies - DTO Validations"
    if sheet_name in wb.sheetnames:
        ws = wb[sheet_name]
        for r in range(2, ws.max_row + 1):
            tc_id = str(ws.cell(r, 1).value or "").strip()
            if tc_id == "POL-DTO-58":
                ws.cell(r, 12, "Fail / Defect Logged")
                ws.cell(r, 12).fill = fail_fill
                ws.cell(r, 12).font = fail_font
                ws.cell(r, 13, "200 OK (CRITICAL DEFECT)")
                ws.cell(r, 13).fill = fail_fill
                ws.cell(r, 13).font = fail_font
                ws.cell(r, 14, "Overtime policy created with negative multiplier -1.5 (DEFECT-20261105-03). Corrupts payroll calculations.")
                ws.cell(r, 15, "DEFECT-20261105-03")
                print(f"[{wb_path}] Updated POL-DTO-58 status to Fail / Defect Logged!")
            elif tc_id == "POL-DTO-61":
                ws.cell(r, 12, "Fail / Defect Logged")
                ws.cell(r, 12).fill = fail_fill
                ws.cell(r, 12).font = fail_font
                ws.cell(r, 13, "200 OK (TenantName empty)")
                ws.cell(r, 14, "Policy created, but TenantName persists as Object (empty) {} in MongoDB (DEFECT-20261105-04).")
                ws.cell(r, 15, "DEFECT-20261105-04")
                print(f"[{wb_path}] Updated POL-DTO-61 status to Fail / Defect Logged!")
                
    wb.save(wb_path)
    print(f"Saved {wb_path} successfully!")

