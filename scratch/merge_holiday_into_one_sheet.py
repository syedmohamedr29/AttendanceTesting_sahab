import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter
import sys

sys.stdout.reconfigure(encoding='utf-8')

wb = openpyxl.load_workbook('AttendanceTestCases_Master_Consolidated.xlsx')

one_sheet_name = 'Holiday Calendar - Test Cases'

# Remove one_sheet_name if already exists
if one_sheet_name in wb.sheetnames:
    del wb[one_sheet_name]

ws_out = wb.create_sheet(title=one_sheet_name)

# Collect all test cases from 'Holiday Calendar - DTO' and 'Holiday Calendar - Business'
ws_dto = wb['Holiday Calendar - DTO']
ws_bus = wb['Holiday Calendar - Business']

headers = ['TC ID', 'Section', 'Test Scenario', 'Input / Preconditions', 'Expected Result', 'Pri', 'Type', 'Env', 'Status', 'QA Remarks']
ws_out.append(headers)

# Styling
navy_fill = PatternFill(start_color="001E3A8A", end_color="001E3A8A", fill_type="solid")
header_font = Font(name="Calibri", size=11, bold=True, color="FFFFFF")
regular_font = Font(name="Calibri", size=10)
bold_font = Font(name="Calibri", size=10, bold=True)

thin_border_side = Side(border_style="thin", color="D1D5DB")
cell_border = Border(left=thin_border_side, right=thin_border_side, top=thin_border_side, bottom=thin_border_side)

p0_fill = PatternFill(start_color="FEE2E2", end_color="FEE2E2", fill_type="solid") # light red
p1_fill = PatternFill(start_color="FEF3C7", end_color="FEF3C7", fill_type="solid") # light yellow
p2_fill = PatternFill(start_color="F3F4F6", end_color="F3F4F6", fill_type="solid") # light gray

for col_idx in range(1, 11):
    cell = ws_out.cell(row=1, column=col_idx)
    cell.fill = navy_fill
    cell.font = header_font
    cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
    cell.border = cell_border
ws_out.row_dimensions[1].height = 28

p0_cnt = 0
p1_cnt = 0
p2_cnt = 0
p3_cnt = 0

current_row = 2

# 1. Append all rows from Holiday Calendar - DTO
print(f"Reading from 'Holiday Calendar - DTO' (rows: {ws_dto.max_row})...")
for r in range(2, ws_dto.max_row + 1):
    vals = [ws_dto.cell(r, c).value for c in range(1, 11)]
    if not vals[0]:
        continue
    ws_out.append(vals)
    pri = vals[5]
    if pri == "P0": p0_cnt += 1
    elif pri == "P1": p1_cnt += 1
    elif pri == "P2": p2_cnt += 1
    elif pri == "P3": p3_cnt += 1
    
    ws_out.row_dimensions[current_row].height = 26
    for c in range(1, 11):
        cell = ws_out.cell(row=current_row, column=c)
        cell.font = regular_font
        cell.border = cell_border
        cell.alignment = Alignment(vertical="center", wrap_text=True)
        if c in [1, 6, 7, 8, 9]:
            cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
        if c == 1:
            cell.font = bold_font
        if c == 6:
            if pri == "P0": cell.fill = p0_fill; cell.font = bold_font
            elif pri == "P1": cell.fill = p1_fill; cell.font = bold_font
            elif pri == "P2": cell.fill = p2_fill
    current_row += 1

# 2. Append all rows from Holiday Calendar - Business
print(f"Reading from 'Holiday Calendar - Business' (rows: {ws_bus.max_row})...")
for r in range(2, ws_bus.max_row + 1):
    vals = [ws_bus.cell(r, c).value for c in range(1, 11)]
    if not vals[0]:
        continue
    ws_out.append(vals)
    pri = vals[5]
    if pri == "P0": p0_cnt += 1
    elif pri == "P1": p1_cnt += 1
    elif pri == "P2": p2_cnt += 1
    elif pri == "P3": p3_cnt += 1
    
    ws_out.row_dimensions[current_row].height = 26
    for c in range(1, 11):
        cell = ws_out.cell(row=current_row, column=c)
        cell.font = regular_font
        cell.border = cell_border
        cell.alignment = Alignment(vertical="center", wrap_text=True)
        if c in [1, 6, 7, 8, 9]:
            cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
        if c == 1:
            cell.font = bold_font
        if c == 6:
            if pri == "P0": cell.fill = p0_fill; cell.font = bold_font
            elif pri == "P1": cell.fill = p1_fill; cell.font = bold_font
            elif pri == "P2": cell.fill = p2_fill
    current_row += 1

total_tcs = current_row - 2
print(f"Total test cases consolidated into '{one_sheet_name}': {total_tcs}")
print(f"Priority breakdown: P0={p0_cnt}, P1={p1_cnt}, P2={p2_cnt}, P3={p3_cnt}")

# Column widths
col_widths = {
    1: 14, # TC ID
    2: 38, # Section
    3: 45, # Test Scenario
    4: 60, # Input / Preconditions
    5: 65, # Expected Result
    6: 8,  # Pri
    7: 14, # Type
    8: 8,  # Env
    9: 12, # Status
    10: 30 # QA Remarks
}
for col_idx, width in col_widths.items():
    ws_out.column_dimensions[get_column_letter(col_idx)].width = width

# Remove the two separate sheets
print("Removing separate sheets 'Holiday Calendar - DTO' and 'Holiday Calendar - Business'...")
del wb['Holiday Calendar - DTO']
del wb['Holiday Calendar - Business']

# Synchronize INDEX sheet
ws_idx = wb['INDEX']

# Clean up any rows beyond row 19 that were temporary
# Row 19 is 'User Scenarios (Add Here)'
# Let's find rows 20 and beyond
idx_border = Border(left=thin_border_side, right=thin_border_side, top=thin_border_side, bottom=thin_border_side)

# Clear rows 20 to max_row
while ws_idx.max_row > 19:
    ws_idx.delete_rows(ws_idx.max_row)

# Add Row 20: Module 16 -> Holiday Calendar - Test Cases
row_mod16 = 20
ws_idx.cell(row_mod16, 1).value = 16
ws_idx.cell(row_mod16, 2).value = one_sheet_name
ws_idx.cell(row_mod16, 3).value = total_tcs
ws_idx.cell(row_mod16, 4).value = p0_cnt
ws_idx.cell(row_mod16, 5).value = p1_cnt
ws_idx.cell(row_mod16, 6).value = p2_cnt
ws_idx.cell(row_mod16, 7).value = p3_cnt
ws_idx.cell(row_mod16, 8).value = "Complete Holiday Calendar Suite: DTO Validation, GUIDs, All 5 Types (Public/Rel/Nat/Bank/Gazette), EN/AR, From-Date-Only, End-Date Errors, POST/PATCH/GET & DB State"

for c in range(1, 9):
    cell = ws_idx.cell(row_mod16, c)
    cell.font = regular_font
    cell.border = idx_border
    if c in [1, 3, 4, 5, 6, 7]:
        cell.alignment = Alignment(horizontal="center", vertical="center")
    else:
        cell.alignment = Alignment(vertical="center")

# Add Row 21: TOTAL
row_total = 21
tot_tcs = sum(ws_idx.cell(r, 3).value for r in range(5, 21) if isinstance(ws_idx.cell(r, 3).value, int))
tot_p0 = sum(ws_idx.cell(r, 4).value for r in range(5, 21) if isinstance(ws_idx.cell(r, 4).value, int))
tot_p1 = sum(ws_idx.cell(r, 5).value for r in range(5, 21) if isinstance(ws_idx.cell(r, 5).value, int))
tot_p2 = sum(ws_idx.cell(r, 6).value for r in range(5, 21) if isinstance(ws_idx.cell(r, 6).value, int))
tot_p3 = sum(ws_idx.cell(r, 7).value for r in range(5, 21) if isinstance(ws_idx.cell(r, 7).value, int))

ws_idx.cell(row_total, 1).value = "TOTAL"
ws_idx.cell(row_total, 2).value = "All 16 Modules Combined"
ws_idx.cell(row_total, 3).value = tot_tcs
ws_idx.cell(row_total, 4).value = tot_p0
ws_idx.cell(row_total, 5).value = tot_p1
ws_idx.cell(row_total, 6).value = tot_p2
ws_idx.cell(row_total, 7).value = tot_p3
ws_idx.cell(row_total, 8).value = "Master Consolidated Suite with Active User Scenarios & Unified Holiday Calendar Test Suite"

total_font = Font(name="Calibri", size=11, bold=True)
for c in range(1, 9):
    ws_idx.cell(row_total, c).font = total_font
    ws_idx.cell(row_total, c).border = idx_border
    if c in [1, 3, 4, 5, 6, 7]:
        ws_idx.cell(row_total, c).alignment = Alignment(horizontal="center", vertical="center")
    else:
        ws_idx.cell(row_total, c).alignment = Alignment(vertical="center")

print(f"INDEX Row 20 (Module 16): Total={total_tcs} (P0:{p0_cnt}, P1:{p1_cnt}, P2:{p2_cnt}, P3:{p3_cnt})")
print(f"INDEX Row 21 (TOTAL): Total={tot_tcs} (P0:{tot_p0}, P1:{tot_p1}, P2:{tot_p2}, P3:{tot_p3})")

# Save workbook
wb.save('AttendanceTestCases_Master_Consolidated.xlsx')
print("Successfully merged into ONE sheet and saved AttendanceTestCases_Master_Consolidated.xlsx!")

