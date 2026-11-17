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
ws.views.sheetView[0].showGridLines = True

headers = [
    "TC ID", "Requirement ID", "Module", "Submodule", "API Method", "Endpoint",
    "Test Scenario", "Test Technique", "Test Type", "Preconditions", "Test Data",
    "Request Payload", "Execution Steps", "Expected HTTP Status", "Expected Response",
    "DB Validation", "Priority", "Actual Result", "Status"
]

header_fill = PatternFill(start_color="1F497D", end_color="1F497D", fill_type="solid")
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

# Let's read all 147 test cases directly from AM_Scheduler_Roster_Master_QA_Test_Suite.md
md_path = r"C:\Users\Comm-IT India\.gemini\antigravity\brain\65113ff1-ddbc-4539-afe6-44cf63216ecc\AM_Scheduler_Roster_Master_QA_Test_Suite.md"
with open(md_path, "r", encoding="utf-8") as f:
    lines = f.readlines()

# Parse tables in Section 5, 6, 7, 8, 9, 10, 11, 12, 13, 17, 18
all_rows = []

# 1. Parse Section 5 (Positive Test Scenarios - 31 TCs)
# 2. Parse Section 6 (Negative Test Scenarios - 36 TCs)
# 3. Parse Section 7 (EP Scenarios - 12 TCs)
# 4. Parse Section 8 (BVA Scenarios - 13 TCs)
# 5. Parse Section 9 (Decision Tables - 10 TCs)
# 6. Parse Section 10 (State Transitions - 9 TCs)
# 7. Parse Section 11 & 12 (Dedicated POST/PATCH - 12 TCs)
# 8. Parse Section 13 (GET Verification - 10 TCs)
# 9. Parse Section 17 (Regression - 6 TCs)
# 10. Parse Section 18 (Security - 8 TCs)

print("Reading and parsing markdown test suite...")
