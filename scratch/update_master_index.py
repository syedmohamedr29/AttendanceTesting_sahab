import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
import sys

sys.stdout.reconfigure(encoding='utf-8')

wb = openpyxl.load_workbook('AttendanceTestCases_Master_Consolidated.xlsx')
ws = wb['INDEX']

font_regular = Font(name="Calibri", size=10)
font_bold = Font(name="Calibri", size=10, bold=True)
border_thin = Border(left=Side(style='thin', color='D9D9D9'), right=Side(style='thin', color='D9D9D9'), top=Side(style='thin', color='D9D9D9'), bottom=Side(style='thin', color='D9D9D9'))
user_input_fill = PatternFill(start_color="FFF2CC", end_color="FFF2CC", fill_type="solid")
navy_fill = PatternFill(start_color="1F4E79", end_color="1F4E79", fill_type="solid")
font_header = Font(name="Calibri", size=10, bold=True, color="FFFFFF")

# Check if row 21 is currently Module 17 or TOTAL
row21_val = ws.cell(21, 1).value

# If row 21 is TOTAL, insert row 21 for Module 17 and move TOTAL to row 22
if row21_val == 'TOTAL':
    ws.insert_rows(21)
    print("Inserted row at 21 for Module 17")

# Row 21: Module 17
row17_data = [
    17,
    "CDWT - Manual DTO Validations",
    52,
    27,
    20,
    5,
    0,
    "Company Default DTO Edge Cases: Route/Security, Common DTO, Fixed, Flexi, Split & Immutability Locks with In-Cell Dropdown & Filter",
    0,
    0,
    52,
    "0.0%",
    "📝 Ready for Manual Verification"
]

for col_idx, val in enumerate(row17_data, start=1):
    cell = ws.cell(21, col_idx)
    cell.value = val
    cell.font = font_bold if col_idx in [1, 2, 3, 13] else font_regular
    cell.border = border_thin
    cell.fill = user_input_fill if col_idx in [9, 10, 11] else PatternFill(fill_type=None)
    if col_idx in [1, 3, 4, 5, 6, 7, 9, 10, 11, 12, 13]:
        cell.alignment = Alignment(horizontal="center", vertical="center")
    else:
        cell.alignment = Alignment(vertical="center")

# Row 22: TOTAL
total_data = [
    "TOTAL",
    "All 17 Modules Combined",
    1579, # 1527 + 52
    686,  # 659 + 27
    667,  # 647 + 20
    206,  # 201 + 5
    13,   # 13 + 0
    "Master Consolidated Suite with Active User Scenarios, Holiday Calendar Suite & Dedicated CDWT Manual DTO Edge-Case Verification",
    541,
    57,
    981,  # 929 + 52
    0.379, # 598 / 1579
    "🎯 598 Executed (541 Pass, 57 Fail — 90.5% Pass Rate) | 52 Ready for Manual Verification"
]

for col_idx, val in enumerate(total_data, start=1):
    cell = ws.cell(22, col_idx)
    cell.value = val
    cell.font = font_bold
    cell.border = border_thin
    cell.fill = navy_fill
    cell.font = font_header
    if col_idx in [1, 3, 4, 5, 6, 7, 9, 10, 11, 12, 13]:
        cell.alignment = Alignment(horizontal="center", vertical="center")
    else:
        cell.alignment = Alignment(vertical="center")

ws.cell(22, 12).number_format = "0.0%"

wb.save('AttendanceTestCases_Master_Consolidated.xlsx')
print("SUCCESS: Updated INDEX sheet in AttendanceTestCases_Master_Consolidated.xlsx!")

