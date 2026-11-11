import openpyxl
import os
import datetime
import sys

sys.stdout.reconfigure(encoding='utf-8')

fname = 'AttendanceTestCases_Master_Consolidated.xlsx'
mtime = os.path.getmtime(fname)
mod_time = datetime.datetime.fromtimestamp(mtime).strftime('%Y-%m-%d %H:%M:%S')
print(f"=== Checking {fname} (Modified: {mod_time}) ===")

wb = openpyxl.load_workbook(fname)
print("Sheets count:", len(wb.sheetnames))
print("Sheet 18:", wb.sheetnames[-1])

ws_cases = wb['CDWT - Manual DTO Validations']
print("Target sheet rows:", ws_cases.max_row, "cols:", ws_cases.max_column)
print("AutoFilter:", ws_cases.auto_filter.ref)
print("Headers (1 to 15):", [ws_cases.cell(1, c).value for c in range(1, 16)])

ws_idx = wb['INDEX']
print("\nINDEX Row 21 (Module 17):", [ws_idx.cell(21, c).value for c in range(1, 14)])
print("INDEX Row 22 (TOTAL):", [ws_idx.cell(22, c).value for c in range(1, 14)])

