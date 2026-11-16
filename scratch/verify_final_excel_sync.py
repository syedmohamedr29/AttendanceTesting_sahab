import openpyxl

excel_files = [
    'AttendanceTestCases_Master_Consolidated.xlsx',
    'AttendanceTestCases.xlsx',
    'Attendance_Policies_Manual_API_TestCases_MongoDB.xlsx'
]

for ef in excel_files:
    wb = openpyxl.load_workbook(ef, data_only=True)
    ws1 = wb['Work Assignments']
    ws2 = wb['Work Assignments (Master 203)']
    print(f"{ef}:")
    print(f"  'Work Assignments': {ws1.max_row} rows (1 header + {ws1.max_row - 1} TCs)")
    print(f"  'Work Assignments (Master 203)': {ws2.max_row} rows (1 header + {ws2.max_row - 1} TCs)")
