import openpyxl

wb = openpyxl.load_workbook('AttendanceTestCases_Master_Consolidated.xlsx')

sheets_info = [
    ('WT - Company Default', 9, 10),
    ('Policies - DTO Validations', 12, 14),
    ('Holiday Calendar - Test Cases', 9, 10),
    ('User Scenarios (Add Here)', 9, 10),
    ('Attendance Policies', 25, 26) # let's check remarks col for Attendance Policies
]

for sname, stat_col, rem_col in sheets_info:
    ws = wb[sname]
    print(f"\n=== {sname} (Stat Col {stat_col}, Rem Col {rem_col}) ===")
    headers = [cell.value for cell in ws[1]]
    print("Col headers:", [(i+1, h) for i, h in enumerate(headers) if i+1 in [stat_col, rem_col]])
    
    sample_count = 0
    for r in range(2, min(ws.max_row + 1, 300)):
        stat = ws.cell(row=r, column=stat_col).value
        s_str = str(stat).strip() if stat else ""
        if s_str and not s_str.lower().startswith('pass'):
            rem = ws.cell(row=r, column=rem_col).value
            tc = ws.cell(row=r, column=1).value
            print(f"  Row {r} | TC: {tc} | Stat: {s_str} | Rem: {str(rem)[:70]}")
            sample_count += 1
            if sample_count >= 4:
                break
