import openpyxl

wb = openpyxl.load_workbook('AttendanceTestCases.xlsx')
ws = wb['Work Template - Location']

failed_map = {
    "A-04": "Fail",
    "A-08": "Fail",
    "B-00": "Fail",
    "B-05": "Fail",
    "E-04": "Fail",
    "E-07": "Fail"
}

for r in range(2, ws.max_row + 1):
    tc = ws.cell(row=r, column=2).value
    if tc in failed_map:
        ws.cell(row=r, column=10).value = "Fail"
    else:
        ws.cell(row=r, column=10).value = "Pass"

wb.save('AttendanceTestCases.xlsx')
print("Successfully updated AttendanceTestCases.xlsx sheet 'Work Template - Location'.")
