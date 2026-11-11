import sys
import openpyxl

sys.stdout.reconfigure(encoding='utf-8')

wb = openpyxl.load_workbook('AttendanceTestCases_Master_Consolidated.xlsx', data_only=True)
idx_sheet = wb['INDEX']

print(f"Max row: {idx_sheet.max_row}, Max col: {idx_sheet.max_column}")

headers = [idx_sheet.cell(1, c).value for c in range(1, idx_sheet.max_column + 1)]
print("Headers:", headers)

for r in range(2, idx_sheet.max_row + 1):
    vals = [idx_sheet.cell(r, c).value for c in range(1, idx_sheet.max_column + 1)]
    if vals[1]: # Sheet name
        print(f"Row {r:2d} | Module: {vals[0]} | Sheet: {vals[1]:<35} | Total: {vals[2]:>4} | Pass: {vals[8]:>4} | Fail: {vals[9]:>3} | Status: {vals[12] if len(vals) > 12 else vals[-1]}")

