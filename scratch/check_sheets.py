import openpyxl

for fname in ['AttendanceTestCases_Master_Consolidated.xlsx', 'AttendanceTestCases.xlsx', 'Attendance_Policies_Manual_API_TestCases_MongoDB.xlsx']:
    try:
        wb = openpyxl.load_workbook(fname, read_only=True)
        print(f"=== {fname} ===")
        print("Sheets:", wb.sheetnames)
    except Exception as e:
        print(f"Error {fname}: {e}")
