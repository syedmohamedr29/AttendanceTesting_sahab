import sys
import openpyxl

sys.stdout.reconfigure(encoding='utf-8')

wb = openpyxl.load_workbook('AttendanceTestCases_Master_Consolidated.xlsx', data_only=True)

for sheet_name in ['WT - Location Shifts', 'Attendance Policies', 'Work Plans', 'CDWT - Manual DTO Validations']:
    if sheet_name in wb.sheetnames:
        s = wb[sheet_name]
        print(f"\n==================== Sheet: {sheet_name} (Rows: {s.max_row}, Cols: {s.max_column}) ====================")
        headers = [s.cell(1, c).value for c in range(1, min(s.max_column + 1, 12))]
        print("Headers:", headers)
        # sample first 3 test cases
        for r in range(2, min(5, s.max_row + 1)):
            row_vals = [s.cell(r, c).value for c in range(1, min(s.max_column + 1, 10))]
            print(f"Row {r}: {row_vals}")

