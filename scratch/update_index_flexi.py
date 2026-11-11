import openpyxl, sys
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

sys.stdout.reconfigure(encoding='utf-8')

wb = openpyxl.load_workbook('AttendanceTestCases_Master_Consolidated.xlsx')

ws_user = wb['User Scenarios (Add Here)']
thin_border = Border(
    left=Side(style='thin', color='D9D9D9'), right=Side(style='thin', color='D9D9D9'),
    top=Side(style='thin', color='D9D9D9'), bottom=Side(style='thin', color='D9D9D9')
)
data_font = Font(name='Segoe UI', size=10)
bold_font = Font(name='Segoe UI', size=10, bold=True)
p1_fill = PatternFill(start_color='FFF2CC', end_color='FFF2CC', fill_type='solid')

for row in range(30, 42):
    tc_id = ws_user.cell(row=row, column=1).value
    if not tc_id: continue
    pri_val = ws_user.cell(row=row, column=6).value
    for col in range(1, 12):
        cell = ws_user.cell(row=row, column=col)
        cell.font = data_font
        cell.border = thin_border
        if col in [1, 6, 7, 8, 9]:
            cell.alignment = Alignment(horizontal='center', vertical='top')
        else:
            cell.alignment = Alignment(horizontal='left', vertical='top', wrap_text=True)
        if col == 1:
            cell.font = bold_font
        if col == 6 and pri_val == 'P1':
            cell.fill = p1_fill
            cell.font = bold_font

# Update INDEX
ws_index = wb['INDEX']
user_count = 40
user_p1 = 29
user_p2 = 11

ws_index.cell(row=19, column=3, value=user_count)
ws_index.cell(row=19, column=5, value=user_p1)
ws_index.cell(row=19, column=6, value=user_p2)
ws_index.cell(row=19, column=8, value="Custom QA Exploratory, Gaps, DTO, Fixed/Flexi Enums & Daily/Weekly Boundaries")

total_tcs = 1079 + user_count
total_p1 = 437 + user_p1
total_p2 = 173 + user_p2

ws_index.cell(row=20, column=3, value=total_tcs)
ws_index.cell(row=20, column=5, value=total_p1)
ws_index.cell(row=20, column=6, value=total_p2)

wb.save('AttendanceTestCases_Master_Consolidated.xlsx')
print(f"Successfully updated INDEX with 40 User Test Cases! New Suite Total: {total_tcs}")

