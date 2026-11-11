import openpyxl
from openpyxl.styles import PatternFill, Font, Alignment
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open("scratch/live_cdwt_dto_results.json", "r", encoding='utf-8') as f:
    results = json.load(f)

wb = openpyxl.load_workbook("AttendanceTestCases_Master_Consolidated.xlsx")

# Fills
pass_fill = PatternFill(start_color="DCFCE7", end_color="DCFCE7", fill_type="solid") # light green
fail_fill = PatternFill(start_color="FEE2E2", end_color="FEE2E2", fill_type="solid") # light red
bold_font = Font(name="Calibri", size=10, bold=True)
regular_font = Font(name="Calibri", size=10)

updated_count = 0

for res in results:
    sheet_name = res["sheet"]
    row_num = res["row"]
    status = res["result_status"]
    remark = res["qa_remark"]
    
    ws = wb[sheet_name]
    
    # Column 9: Status
    cell_status = ws.cell(row=row_num, column=9)
    cell_status.value = status
    cell_status.font = bold_font
    cell_status.alignment = Alignment(horizontal="center", vertical="center")
    if status == "Pass":
        cell_status.fill = pass_fill
    else:
        cell_status.fill = fail_fill
        
    # Column 10: QA Remarks
    cell_remark = ws.cell(row=row_num, column=10)
    cell_remark.value = remark
    cell_remark.font = regular_font
    cell_remark.alignment = Alignment(vertical="center", wrap_text=True)
    
    # Column 8: Env -> Dev
    ws.cell(row=row_num, column=8).value = "dev"
    
    updated_count += 1
    print(f"Updated {sheet_name} Row {row_num:3d} ({res['tc_id']}): {status}")

wb.save("AttendanceTestCases_Master_Consolidated.xlsx")
print(f"\nSuccessfully updated {updated_count} test cases in AttendanceTestCases_Master_Consolidated.xlsx!")

