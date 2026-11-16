import os, openpyxl

workbooks = [
    'AttendanceTestCases_Master_Consolidated.xlsx',
    'AttendanceTestCases.xlsx',
    'Attendance_Policies_Manual_API_TestCases_MongoDB.xlsx'
]

for wb_path in workbooks:
    wb = openpyxl.load_workbook(wb_path, data_only=True)
    ws = wb['Rotation Work Assignments']
    print(f"{wb_path} -> Sheet 'Rotation Work Assignments' max_row: {ws.max_row}, max_col: {ws.max_column}")

for doc in ['reports/ROTATION_WORK_ASSIGNMENT_TEST_CASES.md', 'reports/ROTATION_WORK_ASSIGNMENT_BUSINESS_VALIDATION.md']:
    print(f"{doc} -> size: {os.path.getsize(doc)} bytes")
