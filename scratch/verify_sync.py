import os, openpyxl

for fname in ['AttendanceTestCases_Master_Consolidated.xlsx', 'AttendanceTestCases.xlsx', 'Attendance_Policies_Manual_API_TestCases_MongoDB.xlsx']:
    wb = openpyxl.load_workbook(fname, data_only=True)
    ws = wb['Rotation Work Plans']
    print(f"{fname} -> Sheet 'Rotation Work Plans' exists, max_row: {ws.max_row}, max_column: {ws.max_column}")

for doc in ['reports/ROTATION_WORK_PLAN_TEST_CASES.md', 'reports/ROTATION_WORK_PLAN_BUSINESS_VALIDATION.md']:
    print(f"{doc} -> size: {os.path.getsize(doc)} bytes")
