import openpyxl

wb = openpyxl.load_workbook('Attendance_Policies_Manual_API_TestCases_MongoDB.xlsx')
if 'Policies - DTO Validations' in wb.sheetnames:
    ws = wb['Policies - DTO Validations']
    updated = 0
    for r in range(2, ws.max_row + 1):
        stat = ws.cell(row=r, column=12).value
        s_str = str(stat).strip().lower() if stat else ""
        if s_str and not s_str.startswith('pass'):
            notes = ws.cell(row=r, column=14).value or ""
            if "[Re-Verified 16-Nov-2026]" not in str(notes):
                ws.cell(row=r, column=14).value = f"[Re-Verified 16-Nov-2026: STILL NOT FIXED] {notes}"
                updated += 1
    wb.save('Attendance_Policies_Manual_API_TestCases_MongoDB.xlsx')
    print(f"Attendance_Policies_Manual_API_TestCases_MongoDB.xlsx: updated {updated} rows in Policies - DTO Validations.")
