import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from copy import copy

master_path = "AttendanceTestCases_Master_Consolidated.xlsx"
pol_path = "Attendance_Policies_Manual_API_TestCases_MongoDB.xlsx"

wb_master = openpyxl.load_workbook(master_path)
wb_pol = openpyxl.load_workbook(pol_path)

ws_master_pol = wb_master["Attendance Policies"]
ws_master_dto = wb_master["Policies - DTO Validations"]

pass_fill = PatternFill(start_color="E2EFDA", end_color="E2EFDA", fill_type="solid")
fail_fill = PatternFill(start_color="FCE4D6", end_color="FCE4D6", fill_type="solid")
pass_font = Font(name="Segoe UI", size=9, color="375623", bold=True)
fail_font = Font(name="Segoe UI", size=9, color="C65911", bold=True)

id_map = {}
for r in range(2, ws_master_pol.max_row + 1):
    tc_id = ws_master_pol.cell(r, 1).value
    if tc_id:
        id_map[tc_id] = r

def apply_row_data(ws_dest, r, src_r, max_cols, ws_src):
    for c in range(1, max_cols + 1):
        val = ws_src.cell(src_r, c).value
        cell = ws_dest.cell(r, c, val)
        if str(val).lower() == "pass":
            cell.fill = pass_fill
            cell.font = pass_font
        elif "fail" in str(val).lower():
            cell.fill = fail_fill
            cell.font = fail_font

# 1. Update Master Test Cases
if "Master Test Cases" in wb_pol.sheetnames:
    ws_dest = wb_pol["Master Test Cases"]
    for r in range(2, ws_dest.max_row + 1):
        tc_id = ws_dest.cell(r, 1).value
        if tc_id in id_map:
            apply_row_data(ws_dest, r, id_map[tc_id], 27, ws_master_pol)
    print("Updated 'Master Test Cases' in Standalone workbook.")

# 2. Update POST API Test Cases
if "POST API Test Cases" in wb_pol.sheetnames:
    ws_dest = wb_pol["POST API Test Cases"]
    for r in range(2, ws_dest.max_row + 1):
        tc_id = ws_dest.cell(r, 1).value
        if tc_id in id_map:
            apply_row_data(ws_dest, r, id_map[tc_id], min(ws_dest.max_column, 27), ws_master_pol)
    print("Updated 'POST API Test Cases' in Standalone workbook.")

# 3. Update PATCH API Test Cases
if "PATCH API Test Cases" in wb_pol.sheetnames:
    ws_dest = wb_pol["PATCH API Test Cases"]
    for r in range(2, ws_dest.max_row + 1):
        tc_id = ws_dest.cell(r, 1).value
        if tc_id in id_map:
            apply_row_data(ws_dest, r, id_map[tc_id], min(ws_dest.max_column, 27), ws_master_pol)
    print("Updated 'PATCH API Test Cases' in Standalone workbook.")

# 4. Update Policies - DTO Validations
if "Policies - DTO Validations" in wb_pol.sheetnames:
    ws_dest = wb_pol["Policies - DTO Validations"]
    dto_map = {}
    for r in range(2, ws_master_dto.max_row + 1):
        tc_id = ws_master_dto.cell(r, 1).value
        if tc_id:
            dto_map[tc_id] = r
            
    for r in range(2, ws_dest.max_row + 1):
        tc_id = ws_dest.cell(r, 1).value
        if tc_id in dto_map:
            apply_row_data(ws_dest, r, dto_map[tc_id], 15, ws_master_dto)
    print("Updated 'Policies - DTO Validations' in Standalone workbook.")

wb_pol.save(pol_path)
print("Saved Standalone workbook successfully!")
