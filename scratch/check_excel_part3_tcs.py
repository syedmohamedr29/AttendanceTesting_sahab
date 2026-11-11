import sys
import openpyxl

sys.stdout.reconfigure(encoding='utf-8')

wb = openpyxl.load_workbook('AttendanceTestCases_Master_Consolidated.xlsx', data_only=True)

# 1. User Scenarios
us_sheet = wb['User Scenarios (Add Here)']
print("=== User Scenarios (Add Here) ===")
for r in range(2, us_sheet.max_row + 1):
    tc = us_sheet.cell(r, 1).value
    if tc in ['USER-33', 'USER-61', 'USER-134', 'USER-135', 'USER-22', 'USER-37']:
        status = us_sheet.cell(r, 9).value
        remarks = us_sheet.cell(r, 10).value
        print(f"{tc} -> Status: {status} | Remarks: {remarks}")

# 2. WT - Company Default
wt_sheet = wb['WT - Company Default']
print("\n=== WT - Company Default ===")
for r in range(2, wt_sheet.max_row + 1):
    tc = wt_sheet.cell(r, 1).value
    if tc in ['DOC-F-01', 'DOC-F-02', 'DOC-A-05', 'ROOT-E-06']:
        status = wt_sheet.cell(r, 9).value if wt_sheet.cell(r, 9).value else wt_sheet.cell(r, 8).value
        remarks = wt_sheet.cell(r, 10).value
        print(f"{tc} -> Status: {status} | Remarks: {remarks}")

