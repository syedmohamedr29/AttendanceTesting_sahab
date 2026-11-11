import openpyxl
from openpyxl.styles import PatternFill, Font, Alignment
import sys

sys.stdout.reconfigure(encoding='utf-8')

pass_fill = PatternFill(start_color="DCFCE7", end_color="DCFCE7", fill_type="solid")
fail_fill = PatternFill(start_color="FEE2E2", end_color="FEE2E2", fill_type="solid")
bold_font = Font(name="Calibri", size=10, bold=True)
regular_font = Font(name="Calibri", size=10)

# ==========================================
# 1. Update AttendanceTestCases_Master_Consolidated.xlsx
# ==========================================
file1 = "AttendanceTestCases_Master_Consolidated.xlsx"
wb1 = openpyxl.load_workbook(file1)
ws1 = wb1["WT - Company Default"]

# Failed rows in WT - Company Default:
# Row 5: DOC-A-04
# Row 6: DOC-A-05
# Row 89: ROOT-E-05
# Row 90: ROOT-E-06

failed_master_rows = {
    5: ("Fail", "HTTP 200 (Cross-tenant leak: __tenant header ignored; returned company templates) | 1202ms"),
    6: ("Fail", "HTTP 200 (Cross-company scoping fallback: returned 200 empty array instead of 400 Cit.Attendance:9001) | 1275ms"),
    89: ("Fail", "HTTP 200 (Tenant isolation failure: __tenant header bypassed; cross-tenant template access allowed) | 1210ms"),
    90: ("Fail", "HTTP 200 (Company scoping fallback: invalid/foreign company returns HTTP 200 [] instead of 400 Cit.Attendance:9001) | 1250ms")
}

for r, (st, rem) in failed_master_rows.items():
    cell_st = ws1.cell(row=r, column=9)
    cell_st.value = st
    cell_st.font = bold_font
    cell_st.fill = fail_fill
    cell_st.alignment = Alignment(horizontal="center", vertical="center")
    
    cell_rem = ws1.cell(row=r, column=10)
    cell_rem.value = rem
    cell_rem.font = regular_font
    cell_rem.alignment = Alignment(vertical="center", wrap_text=True)

# Count passes and fails
pass_count1 = 0
fail_count1 = 0
for r in range(2, ws1.max_row + 1):
    val = ws1.cell(r, 9).value
    if val == "Pass":
        pass_count1 += 1
    elif val == "Fail":
        fail_count1 += 1

print(f"Master Consolidated WT - Company Default: Pass={pass_count1}, Fail={fail_count1}, Total={ws1.max_row - 1}")

# Update INDEX in wb1
ws1_idx = wb1["INDEX"]
ws1_idx.cell(row=5, column=9).value = pass_count1
ws1_idx.cell(row=5, column=10).value = fail_count1
ws1_idx.cell(row=5, column=11).value = 0
ws1_idx.cell(row=5, column=12).value = "100.0%"
pass_rate1 = (pass_count1 / (ws1.max_row - 1)) * 100
ws1_idx.cell(row=5, column=13).value = f"✅ 100% Executed ({pass_rate1:.1f}% Pass Rate)"

wb1.save(file1)
print(f"Saved {file1} successfully.")


# ==========================================
# 2. Update AttendanceTestCases.xlsx
# ==========================================
file2 = "AttendanceTestCases.xlsx"
wb2 = openpyxl.load_workbook(file2)
ws2 = wb2["Work Template - Company"]

failed_att_rows = {
    37: ("Fail", "HTTP 200 (Tenant isolation failure: cross-tenant access not blocked by __tenant scoping) | 1210ms"),
    38: ("Fail", "HTTP 200 (Company scoping failure: invalid/foreign company returns HTTP 200 [] instead of Cit.Attendance:9001) | 1250ms")
}

for r, (st, rem) in failed_att_rows.items():
    cell_st = ws2.cell(row=r, column=10)
    cell_st.value = st
    cell_st.font = bold_font
    cell_st.fill = fail_fill
    cell_st.alignment = Alignment(horizontal="center", vertical="center")
    
    cell_rem = ws2.cell(row=r, column=11)
    cell_rem.value = rem
    cell_rem.font = regular_font
    cell_rem.alignment = Alignment(vertical="center", wrap_text=True)

# Count passes and fails
pass_count2 = 0
fail_count2 = 0
for r in range(2, ws2.max_row + 1):
    val = ws2.cell(r, 10).value
    if val == "Pass":
        pass_count2 += 1
    elif val == "Fail":
        fail_count2 += 1

print(f"AttendanceTestCases.xlsx Work Template - Company: Pass={pass_count2}, Fail={fail_count2}, Total={ws2.max_row - 1}")

# Check INDEX in wb2
ws2_idx = wb2["INDEX"]
# Find the row for Work Template - Company
for r in range(1, ws2_idx.max_row + 1):
    cell_val = str(ws2_idx.cell(r, 2).value or '')
    if "Work Template - Company" in cell_val or "Company Default" in cell_val:
        # Check column headers of wb2 INDEX
        print(f"Found row in wb2 INDEX: {r} -> {cell_val}")
        # update pass/fail if applicable
        if ws2_idx.max_column >= 9:
            ws2_idx.cell(r, 9).value = pass_count2
        if ws2_idx.max_column >= 10:
            ws2_idx.cell(r, 10).value = fail_count2

wb2.save(file2)
print(f"Saved {file2} successfully.")

