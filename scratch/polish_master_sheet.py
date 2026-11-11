import openpyxl, sys
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

sys.stdout.reconfigure(encoding='utf-8')

wb = openpyxl.load_workbook('AttendanceTestCases_Master_Consolidated.xlsx')

# 1. Polish 'User Scenarios (Add Here)'
ws_user = wb['User Scenarios (Add Here)']

# Header styling
header_font = Font(name='Segoe UI', size=11, bold=True, color='FFFFFF')
header_fill = PatternFill(start_color='1F4E78', end_color='1F4E78', fill_type='solid')
thin_border = Border(
    left=Side(style='thin', color='D9D9D9'),
    right=Side(style='thin', color='D9D9D9'),
    top=Side(style='thin', color='D9D9D9'),
    bottom=Side(style='thin', color='D9D9D9')
)

for col in range(1, 12):
    cell = ws_user.cell(row=1, column=col)
    cell.font = header_font
    cell.fill = header_fill
    cell.alignment = Alignment(horizontal='center', vertical='center', wrap_text=True)

# Data row styling
data_font = Font(name='Segoe UI', size=10)
bold_font = Font(name='Segoe UI', size=10, bold=True)
p1_fill = PatternFill(start_color='FFF2CC', end_color='FFF2CC', fill_type='solid') # soft yellow
failed_fill = PatternFill(start_color='FCE4D6', end_color='FCE4D6', fill_type='solid') # soft red/orange

for row in range(2, 30):
    tc_id = ws_user.cell(row=row, column=1).value
    if not tc_id: continue
    
    status_val = ws_user.cell(row=row, column=9).value
    pri_val = ws_user.cell(row=row, column=6).value
    
    for col in range(1, 12):
        cell = ws_user.cell(row=row, column=col)
        cell.font = data_font
        cell.border = thin_border
        
        # Alignments
        if col in [1, 6, 7, 8, 9]:
            cell.alignment = Alignment(horizontal='center', vertical='top')
        else:
            cell.alignment = Alignment(horizontal='left', vertical='top', wrap_text=True)
            
        if col == 1:
            cell.font = bold_font
            
        if col == 6 and pri_val == 'P1':
            cell.fill = p1_fill
            cell.font = bold_font
            
        if col == 9 and 'Failed' in str(status_val):
            cell.fill = failed_fill
            cell.font = bold_font

# Adjust column widths for User Scenarios
col_widths = {
    1: 12,  # TC ID
    2: 24,  # Section
    3: 38,  # Test Scenario
    4: 45,  # Input / Preconditions
    5: 50,  # Expected Result
    6: 8,   # Pri
    7: 14,  # Type
    8: 10,  # Env
    9: 16,  # Status
    10: 45, # QA Remarks
    11: 22  # Source Origin
}

for col_idx, width in col_widths.items():
    ws_user.column_dimensions[get_column_letter(col_idx)].width = width

# 2. Update 'INDEX' sheet
ws_index = wb['INDEX']

# Find or add row 15 in index table
# Currently table is rows 5 to 18 (with 18 being TOTAL)
# Let's count user test cases
user_count = 28 # USER-01 to USER-28
user_p1 = 20
user_p2 = 8
user_p3 = 0

# Check row 19 content
row19_val = ws_index.cell(row=19, column=1).value
print(f"Row 19 col 1: {row19_val}")

# Insert User Scenarios at row 19, move TOTAL to row 20
ws_index.cell(row=19, column=1, value=15)
ws_index.cell(row=19, column=2, value="User Scenarios (Add Here)")
ws_index.cell(row=19, column=3, value=user_count)
ws_index.cell(row=19, column=4, value=0)
ws_index.cell(row=19, column=5, value=user_p1)
ws_index.cell(row=19, column=6, value=user_p2)
ws_index.cell(row=19, column=7, value=user_p3)
ws_index.cell(row=19, column=8, value="Custom QA Exploratory, Gaps, DTO & Type Migration")

for col in range(1, 9):
    c = ws_index.cell(row=19, column=col)
    c.font = Font(name='Segoe UI', size=10, bold=(col in [1, 2, 3]))
    c.border = thin_border
    if col in [1, 3, 4, 5, 6, 7]:
        c.alignment = Alignment(horizontal='center', vertical='center')
    else:
        c.alignment = Alignment(horizontal='left', vertical='center')

# Update TOTAL row at row 20
total_tcs = 1079 + user_count
total_p0 = 456
total_p1 = 437 + user_p1
total_p2 = 173 + user_p2
total_p3 = 13 + user_p3

ws_index.cell(row=20, column=1, value="TOTAL")
ws_index.cell(row=20, column=2, value="All 15 Modules Combined")
ws_index.cell(row=20, column=3, value=total_tcs)
ws_index.cell(row=20, column=4, value=total_p0)
ws_index.cell(row=20, column=5, value=total_p1)
ws_index.cell(row=20, column=6, value=total_p2)
ws_index.cell(row=20, column=7, value=total_p3)
ws_index.cell(row=20, column=8, value="Master Consolidated Suite with Active User Scenarios")

total_fill = PatternFill(start_color='D9E1F2', end_color='D9E1F2', fill_type='solid')
total_font = Font(name='Segoe UI', size=11, bold=True)
for col in range(1, 9):
    c = ws_index.cell(row=20, column=col)
    c.font = total_font
    c.fill = total_fill
    c.border = thin_border
    if col in [1, 3, 4, 5, 6, 7]:
        c.alignment = Alignment(horizontal='center', vertical='center')
    else:
        c.alignment = Alignment(horizontal='left', vertical='center')

wb.save('AttendanceTestCases_Master_Consolidated.xlsx')
print(f"Successfully updated and polished AttendanceTestCases_Master_Consolidated.xlsx! Total TCs: {total_tcs}")

