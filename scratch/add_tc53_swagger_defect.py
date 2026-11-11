import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
import sys

sys.stdout.reconfigure(encoding='utf-8')

wb = openpyxl.load_workbook('AttendanceTestCases_Master_Consolidated.xlsx')
ws = wb['CDWT - Manual DTO Validations']

# Check if CDWT-DTO-53 is already there
found = False
for r in range(2, ws.max_row + 1):
    if ws.cell(r, 1).value == 'CDWT-DTO-53':
        found = True
        break

if not found:
    new_row = [
        "CDWT-DTO-53",
        "1. Route & Security",
        "Swagger UI",
        "Authorization Scheme",
        "Swagger UI missing OAuth2 (authorizationCode) flow with WebGateway_Swagger client",
        "GET",
        "/swagger/index.html",
        "None",
        "HTTP 200 with OAuth2 AuthorizationCode configured",
        "P1",
        "Failed",
        "Failed",
        "401 / Manual Bearer only",
        "DEFECT-20261029-02: Missing oauth2 security scheme; only raw Bearer supported",
        "DEFECT-20261029-02: Missing OAuth2 authorizationCode in Swagger"
    ]
    
    row_idx = ws.max_row + 1
    border_thin = Border(left=Side(style='thin', color='D9D9D9'), right=Side(style='thin', color='D9D9D9'), top=Side(style='thin', color='D9D9D9'), bottom=Side(style='thin', color='D9D9D9'))
    font_bold = Font(name="Calibri", size=10, bold=True)
    font_regular = Font(name="Calibri", size=10)
    font_code = Font(name="Consolas", size=9)
    fail_fill = PatternFill(start_color="FCE4D6", end_color="FCE4D6", fill_type="solid")
    fail_font = Font(name="Calibri", size=10, bold=True, color="C65911")
    user_input_fill = PatternFill(start_color="FFF2CC", end_color="FFF2CC", fill_type="solid")

    for col_idx, val in enumerate(new_row, start=1):
        cell = ws.cell(row_idx, col_idx)
        cell.value = val
        cell.border = border_thin
        cell.font = font_regular
        cell.alignment = Alignment(vertical="center", wrap_text=True)
        if col_idx == 1:
            cell.font = font_bold
            cell.alignment = Alignment(horizontal="center", vertical="center")
        elif col_idx in [6, 10, 11, 12, 13]:
            cell.alignment = Alignment(horizontal="center", vertical="center")
        elif col_idx == 8:
            cell.font = font_code
            
        if col_idx == 11:
            cell.fill = fail_fill
            cell.font = fail_font
        elif col_idx in [12, 13, 14]:
            cell.fill = user_input_fill
            if col_idx == 12:
                cell.font = fail_font

    ws.row_dimensions[row_idx].height = 24
    ws.auto_filter.ref = f"A1:O{row_idx}"
    print(f"Added CDWT-DTO-53 to row {row_idx} of CDWT - Manual DTO Validations!")

# Also update INDEX
ws_idx = wb['INDEX']
# Row 21 is Module 17
ws_idx.cell(21, 3).value = 53 # Total TCs
ws_idx.cell(21, 5).value = 21 # P1 count (was 20, now 21)
ws_idx.cell(21, 10).value = 1  # Failed count = 1 (CDWT-DTO-53 confirmed failed)
ws_idx.cell(21, 11).value = 52 # Not-Run / Pending = 52
ws_idx.cell(21, 12).value = "1.9%" # Exec %
ws_idx.cell(21, 13).value = "⚠️ 1 Failed (DEFECT-20261029-02) | 52 Pending"

# Row 22 is TOTAL
ws_idx.cell(22, 3).value = 1580 # 1579 + 1
ws_idx.cell(22, 5).value = 668  # 667 + 1
ws_idx.cell(22, 10).value = 58  # 57 + 1
ws_idx.cell(22, 13).value = "🎯 599 Executed (541 Pass, 58 Fail — 90.3% Pass Rate) | 52 Ready for Manual Verification"

wb.save('AttendanceTestCases_Master_Consolidated.xlsx')
print("SUCCESS: Updated AttendanceTestCases_Master_Consolidated.xlsx with CDWT-DTO-53 and updated INDEX!")

