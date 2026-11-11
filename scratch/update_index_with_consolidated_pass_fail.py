import openpyxl
from openpyxl.styles import PatternFill, Font, Alignment, Border, Side
from openpyxl.utils import get_column_letter
import sys

sys.stdout.reconfigure(encoding='utf-8')

wb = openpyxl.load_workbook('AttendanceTestCases_Master_Consolidated.xlsx')

# 1. Scan sheets to get live exact pass/fail counts
module_names = [
    ("WT - Company Default", 5),
    ("WT - Location Shifts", 6),
    ("WT - Roster & Rotation", 7),
    ("Holiday Calendar - Company", 8),
    ("Holiday Calendar - Location", 9),
    ("Attendance Policies", 10),
    ("Work Plans", 11),
    ("Work Assignments", 12),
    ("Attendance Exemptions", 13),
    ("Att Log - Upload (KT)", 14),
    ("Att Log - Finalise (KT)", 15),
    ("Att Log - Edits (KT)", 16),
    ("Att Log - Issues (KT)", 17),
    ("Att Log - Monthly L4-L5 (KT)", 18),
    ("User Scenarios (Add Here)", 19),
    ("Holiday Calendar - Test Cases", 20)
]

sheet_stats = {}
for sheet_name, row_idx in module_names:
    ws = wb[sheet_name]
    status_col = None
    for c in range(1, ws.max_column + 1):
        val = str(ws.cell(1, c).value or "")
        if "status" in val.lower():
            status_col = c
            break
    if not status_col:
        status_col = 9
        
    passed = 0
    failed = 0
    not_run = 0
    for r in range(2, ws.max_row + 1):
        st = str(ws.cell(r, status_col).value or "").strip().lower()
        if st == "pass":
            passed += 1
        elif st == "fail":
            failed += 1
        else:
            not_run += 1
            
    total = ws.max_row - 1
    sheet_stats[sheet_name] = {
        "row": row_idx,
        "total": total,
        "passed": passed,
        "failed": failed,
        "not_run": not_run
    }

# 2. Update INDEX sheet
ws_idx = wb['INDEX']

# Header styling
header_fill = PatternFill(start_color="1E3A8A", end_color="1E3A8A", fill_type="solid") # Dark Navy
header_font = Font(name="Calibri", size=10, bold=True, color="FFFFFF")
border_thin = Side(border_style="thin", color="CBD5E1")
cell_border = Border(left=border_thin, right=border_thin, top=border_thin, bottom=border_thin)

pass_fill = PatternFill(start_color="DCFCE7", end_color="DCFCE7", fill_type="solid") # light green
fail_fill = PatternFill(start_color="FEE2E2", end_color="FEE2E2", fill_type="solid") # light red
gray_fill = PatternFill(start_color="F1F5F9", end_color="F1F5F9", fill_type="solid") # light gray
total_fill = PatternFill(start_color="F8FAFC", end_color="F8FAFC", fill_type="solid")

bold_font = Font(name="Calibri", size=10, bold=True)
regular_font = Font(name="Calibri", size=10)

# Set Header Row (Row 4)
new_headers = {
    9: "Passed",
    10: "Failed",
    11: "Not-Run",
    12: "Exec %",
    13: "Execution Status"
}

for col_idx, h_text in new_headers.items():
    cell = ws_idx.cell(row=4, column=col_idx)
    cell.value = h_text
    cell.fill = header_fill
    cell.font = header_font
    cell.alignment = Alignment(horizontal="center", vertical="center")
    cell.border = cell_border

# Update each module row
tot_pass = 0
tot_fail = 0
tot_not_run = 0
tot_tcs = 0

for sheet_name, row_idx in module_names:
    st = sheet_stats[sheet_name]
    t = st["total"]
    p = st["passed"]
    f = st["failed"]
    nr = st["not_run"]
    
    tot_tcs += t
    tot_pass += p
    tot_fail += f
    tot_not_run += nr
    
    exec_count = p + f
    exec_pct = f"{exec_count / t * 100:.1f}%" if t > 0 else "0%"
    
    if exec_count == t and t > 0:
        health_status = f"100% Executed ({p/t*100:.1f}% Pass)"
    elif exec_count > 0:
        health_status = f"In Progress ({exec_count}/{t} run)"
    else:
        health_status = "Not-Run (Pending)"
        
    ws_idx.cell(row=row_idx, column=9).value = p
    ws_idx.cell(row=row_idx, column=10).value = f
    ws_idx.cell(row=row_idx, column=11).value = nr
    ws_idx.cell(row=row_idx, column=12).value = exec_pct
    ws_idx.cell(row=row_idx, column=13).value = health_status
    
    for c in range(9, 14):
        cell = ws_idx.cell(row=row_idx, column=c)
        cell.font = regular_font
        cell.border = cell_border
        cell.alignment = Alignment(horizontal="center", vertical="center")
        if c == 9 and p > 0:
            cell.fill = pass_fill
            cell.font = bold_font
        elif c == 10 and f > 0:
            cell.fill = fail_fill
            cell.font = bold_font
        elif c == 11:
            cell.fill = gray_fill
        elif c == 13:
            cell.alignment = Alignment(horizontal="left", vertical="center")
            if exec_count > 0:
                cell.font = bold_font

# Total Row (Row 21)
row_tot = 21
tot_exec = tot_pass + tot_fail
tot_pct = f"{tot_exec / tot_tcs * 100:.1f}%"
tot_health = f"{tot_exec} Executed ({tot_pass} Pass, {tot_fail} Fail, {tot_not_run} Not-Run)"

ws_idx.cell(row=row_tot, column=9).value = tot_pass
ws_idx.cell(row=row_tot, column=10).value = tot_fail
ws_idx.cell(row=row_tot, column=11).value = tot_not_run
ws_idx.cell(row=row_tot, column=12).value = tot_pct
ws_idx.cell(row=row_tot, column=13).value = tot_health

for c in range(9, 14):
    cell = ws_idx.cell(row=row_tot, column=c)
    cell.font = bold_font
    cell.border = cell_border
    cell.alignment = Alignment(horizontal="center", vertical="center")
    cell.fill = total_fill
    if c == 13:
        cell.alignment = Alignment(horizontal="left", vertical="center")

# Set Column Widths
ws_idx.column_dimensions['I'].width = 12 # Passed
ws_idx.column_dimensions['J'].width = 12 # Failed
ws_idx.column_dimensions['K'].width = 12 # Not-Run
ws_idx.column_dimensions['L'].width = 12 # Exec %
ws_idx.column_dimensions['M'].width = 35 # Status

wb.save('AttendanceTestCases_Master_Consolidated.xlsx')
print(f"Successfully updated INDEX with consolidated Pass ({tot_pass}), Fail ({tot_fail}), Not-Run ({tot_not_run}) across all 16 sheets!")

