# coding: utf-8
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

wb_path = "AttendanceTestCases_Master_Consolidated.xlsx"
wb = openpyxl.load_workbook(wb_path)

sheet_name = "Scheduler (Roster)"
if sheet_name in wb.sheetnames:
    del wb[sheet_name]

ws = wb.create_sheet(title=sheet_name)

# Ensure gridlines
ws.views.sheetView[0].showGridLines = True

headers = [
    "TC ID", "Requirement ID", "Module", "Submodule", "API Method", "Endpoint",
    "Test Scenario", "Test Technique", "Test Type", "Preconditions", "Test Data",
    "Request Payload", "Execution Steps", "Expected HTTP Status", "Expected Response",
    "DB Validation", "Priority", "Actual Result", "Status"
]

header_fill = PatternFill(start_color="1F497D", end_color="1F497D", fill_type="solid") # Dark Navy
header_font = Font(name="Calibri", size=11, bold=True, color="FFFFFF")
thin_border = Border(
    left=Side(style='thin', color='D9D9D9'),
    right=Side(style='thin', color='D9D9D9'),
    top=Side(style='thin', color='D9D9D9'),
    bottom=Side(style='thin', color='D9D9D9')
)

for col_idx, h in enumerate(headers, 1):
    cell = ws.cell(row=1, column=col_idx, value=h)
    cell.fill = header_fill
    cell.font = header_font
    cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
    cell.border = thin_border

ws.row_dimensions[1].height = 28

# Let's import our test cases from the python modules we generated
import sec_05_to_10
import sec_11_to_15
import sec_16_to_22

print("Sec modules imported")
