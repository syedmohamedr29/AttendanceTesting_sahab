import openpyxl

wb = openpyxl.load_workbook('AttendanceTestCases_Master_Consolidated.xlsx')

# 1. WT - Company Default (Stat Col 9, Rem Col 10)
ws1 = wb['WT - Company Default']
updated_count1 = 0
for r in range(2, ws1.max_row + 1):
    stat = ws1.cell(row=r, column=9).value
    if stat and str(stat).strip().lower() == 'fail':
        rem = ws1.cell(row=r, column=10).value or ""
        if "[Re-Verified 16-Nov-2026]" not in str(rem):
            ws1.cell(row=r, column=10).value = f"[Re-Verified 16-Nov-2026: STILL NOT FIXED] {rem}"
            updated_count1 += 1
print(f"WT - Company Default: updated {updated_count1} rows.")

# 2. Policies - DTO Validations (Stat Col 12, Notes Col 14)
ws2 = wb['Policies - DTO Validations']
updated_count2 = 0
for r in range(2, ws2.max_row + 1):
    stat = ws2.cell(row=r, column=12).value
    s_str = str(stat).strip().lower() if stat else ""
    if s_str and not s_str.startswith('pass'):
        notes = ws2.cell(row=r, column=14).value or ""
        if "[Re-Verified 16-Nov-2026]" not in str(notes):
            ws2.cell(row=r, column=14).value = f"[Re-Verified 16-Nov-2026: STILL NOT FIXED] {notes}"
            updated_count2 += 1
print(f"Policies - DTO Validations: updated {updated_count2} rows.")

# 3. Holiday Calendar - Test Cases (Stat Col 9, Rem Col 10)
ws3 = wb['Holiday Calendar - Test Cases']
updated_count3 = 0
for r in range(2, ws3.max_row + 1):
    stat = ws3.cell(row=r, column=9).value
    if stat and str(stat).strip().lower() == 'fail':
        rem = ws3.cell(row=r, column=10).value or ""
        if "[Re-Verified 16-Nov-2026]" not in str(rem):
            ws3.cell(row=r, column=10).value = f"[Re-Verified 16-Nov-2026: STILL NOT FIXED] {rem}"
            updated_count3 += 1
print(f"Holiday Calendar - Test Cases: updated {updated_count3} rows.")

# 4. User Scenarios (Add Here) (Stat Col 9, Rem Col 10)
ws4 = wb['User Scenarios (Add Here)']
updated_count4 = 0
for r in range(2, ws4.max_row + 1):
    stat = ws4.cell(row=r, column=9).value
    if stat and str(stat).strip().lower() == 'fail':
        rem = ws4.cell(row=r, column=10).value or ""
        if "[Live Verified 16-Nov-2026]" not in str(rem) and "[Re-Verified 16-Nov-2026]" not in str(rem):
            ws4.cell(row=r, column=10).value = f"[Re-Verified 16-Nov-2026: STILL NOT FIXED] {rem}"
            updated_count4 += 1
print(f"User Scenarios (Add Here): updated {updated_count4} rows.")

# 5. Attendance Policies (Stat Col 25, Rem Col 27)
ws5 = wb['Attendance Policies']
updated_count5 = 0
for r in range(2, ws5.max_row + 1):
    stat = ws5.cell(row=r, column=25).value
    if stat and str(stat).strip().lower() == 'fail':
        rem = ws5.cell(row=r, column=27).value or ""
        if "[Re-Verified 16-Nov-2026]" not in str(rem):
            ws5.cell(row=r, column=27).value = f"[Re-Verified 16-Nov-2026: STILL NOT FIXED] {rem}"
            updated_count5 += 1
print(f"Attendance Policies: updated {updated_count5} rows.")

wb.save('AttendanceTestCases_Master_Consolidated.xlsx')
print("Successfully saved AttendanceTestCases_Master_Consolidated.xlsx!")
