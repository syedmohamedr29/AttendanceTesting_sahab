import openpyxl
import sys

sys.stdout.reconfigure(encoding='utf-8')

for wb_name in ['AttendanceTestCases_Master_Consolidated.xlsx', 'AttendanceTestCases.xlsx']:
    print(f"\n=== {wb_name} ===")
    wb = openpyxl.load_workbook(wb_name, read_only=True)
    for s in wb.sheetnames:
        if 'holiday' in s.lower():
            print(f"  Found sheet: {s}")

