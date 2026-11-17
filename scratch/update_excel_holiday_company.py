# -*- coding: utf-8 -*-
import openpyxl
from openpyxl.styles import PatternFill, Font, Alignment, Border, Side

excel_path = 'AttendanceTestCases_Master_Consolidated.xlsx'
wb = openpyxl.load_workbook(excel_path)
sheet = wb['Holiday Calendar - Company']

# Define styles
green_fill = PatternFill(start_color="D4EDDA", end_color="D4EDDA", fill_type="solid")
green_font = Font(name="Segoe UI", size=10, bold=True, color="155724")

red_fill = PatternFill(start_color="F8D7DA", end_color="F8D7DA", fill_type="solid")
red_font = Font(name="Segoe UI", size=10, bold=True, color="721C24")

blue_fill = PatternFill(start_color="D1ECF1", end_color="D1ECF1", fill_type="solid")
blue_font = Font(name="Segoe UI", size=10, bold=True, color="0C5460")

regular_font = Font(name="Segoe UI", size=10)

from evaluate_all_sheet6 import audit_list

updated_count = 0
pass_count = 0
fail_count = 0
by_design_count = 0

for r, tc_id, section, scenario, pri, status, notes in audit_list:
    status_cell = sheet.cell(row=r, column=9)
    remarks_cell = sheet.cell(row=r, column=10)
    
    status_cell.value = status
    remarks_cell.value = notes
    remarks_cell.font = regular_font
    
    if status == 'Pass':
        status_cell.fill = green_fill
        status_cell.font = green_font
        pass_count += 1
    elif status == 'FAIL':
        status_cell.fill = red_fill
        status_cell.font = red_font
        fail_count += 1
    elif 'By Design' in status:
        status_cell.fill = blue_fill
        status_cell.font = blue_font
        by_design_count += 1
        
    status_cell.alignment = Alignment(horizontal="center", vertical="center")
    updated_count += 1

# Also check INDEX sheet
if 'INDEX' in wb.sheetnames:
    index_sheet = wb['INDEX']
    # find row for Holiday Calendar - Company
    for r in range(1, index_sheet.max_row + 1):
        cell_val = str(index_sheet.cell(row=r, column=2).value or '')
        if 'Holiday Calendar - Company' in cell_val or index_sheet.cell(row=r, column=1).value == 6:
            print(f"Updating INDEX row {r} for Holiday Calendar - Company")
            # columns: [Sheet #, Sheet Name, Description, Total TCs, Executed, Pass, Fail, Blocked, Pass Rate, Status]
            index_sheet.cell(row=r, column=4).value = updated_count # Total
            index_sheet.cell(row=r, column=5).value = updated_count # Executed
            index_sheet.cell(row=r, column=6).value = pass_count + by_design_count # Pass
            index_sheet.cell(row=r, column=7).value = fail_count # Fail
            index_sheet.cell(row=r, column=8).value = 0 # Blocked
            pass_rate = round(((pass_count + by_design_count) / updated_count) * 100, 1)
            index_sheet.cell(row=r, column=9).value = f"{pass_rate}%"
            index_sheet.cell(row=r, column=10).value = "Completed (Live Audited)"
            break

wb.save(excel_path)
print(f"Successfully updated {updated_count} test cases in {excel_path} Sheet 6 'Holiday Calendar - Company'.")
print(f"Pass: {pass_count}, Pass (By Design): {by_design_count}, FAIL: {fail_count}")
