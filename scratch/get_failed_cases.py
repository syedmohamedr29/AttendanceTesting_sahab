import openpyxl

wb = openpyxl.load_workbook('AttendanceTestCases_Master_Consolidated.xlsx', data_only=True)

def inspect_failed_cases(sheet_name, status_col_idx, id_col_idx=1, title_col_idx=3, remarks_col_idx=10):
    ws = wb[sheet_name]
    print(f"\n=======================================================")
    print(f"FAILED / DEFECT ROWS IN: {sheet_name}")
    print(f"=======================================================")
    header_row = 1
    # Check headers
    headers = [cell.value for cell in ws[header_row]]
    
    count = 0
    for r in range(header_row + 1, ws.max_row + 1):
        status = ws.cell(row=r, column=status_col_idx).value
        s_str = str(status).strip() if status is not None else ""
        if s_str and not s_str.lower().startswith('pass'):
            count += 1
            tc_id = ws.cell(row=r, column=id_col_idx).value
            title = ws.cell(row=r, column=title_col_idx).value
            remarks = ws.cell(row=r, column=remarks_col_idx).value if remarks_col_idx else ""
            print(f"Row {r} | TC: {tc_id} | Status: {s_str} | Title: {str(title)[:60]} | Remarks: {str(remarks)[:80]}")
    print(f"Total non-pass rows found: {count}")

# 1. WT - Company Default (Status Col: 9, TC ID: 1, Title: 3, Remarks: 10)
inspect_failed_cases('WT - Company Default', 9, 1, 3, 10)

# 2. Policies - DTO Validations (Status Col: 12, TC ID: 1, Title: 5, Remarks: 14)
inspect_failed_cases('Policies - DTO Validations', 12, 1, 5, 14)

# 3. Holiday Calendar - Test Cases (Status Col: 9, TC ID: 1, Title: 3, Remarks: 10)
inspect_failed_cases('Holiday Calendar - Test Cases', 9, 1, 3, 10)

# 4. User Scenarios (Add Here) (Status Col: 9, TC ID: 1, Title: 3, Remarks: 10)
inspect_failed_cases('User Scenarios (Add Here)', 9, 1, 3, 10)

# 5. Attendance Policies (Status Col: 25, TC ID: 1, Title: 8, Remarks: 22)
inspect_failed_cases('Attendance Policies', 25, 1, 8, 22)
