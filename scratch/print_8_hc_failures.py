import openpyxl

wb = openpyxl.load_workbook('AttendanceTestCases_Master_Consolidated.xlsx', data_only=True)
ws = wb['Holiday Calendar - Test Cases']

headers = [cell.value for cell in ws[1]]

for r in range(2, ws.max_row + 1):
    status = ws.cell(row=r, column=9).value
    if status and "fail" in str(status).lower():
        tc_id = ws.cell(row=r, column=1).value
        section = ws.cell(row=r, column=2).value
        scenario = ws.cell(row=r, column=3).value
        precond = ws.cell(row=r, column=4).value
        expected = ws.cell(row=r, column=5).value
        qa = ws.cell(row=r, column=10).value
        print(f"==================================================")
        print(f"Row {r} | TC ID: {tc_id} | Section: {section}")
        print(f"Scenario: {scenario}")
        print(f"Preconditions: {precond}")
        print(f"Expected: {expected}")
        print(f"Status: {status}")
        print(f"QA Remarks: {qa}")
