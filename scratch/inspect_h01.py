import sys
import openpyxl

sys.stdout.reconfigure(encoding='utf-8')

wb = openpyxl.load_workbook('AttendanceTestCases_Master_Consolidated.xlsx', data_only=True)
ws = wb['WT - Company Default']
print("WT - Company Default DOC-H-01 rows 48 to 54:")
for r in range(48, 55):
    print(f"Row {r}: {[ws.cell(r, c).value for c in range(1, 6)]}")

