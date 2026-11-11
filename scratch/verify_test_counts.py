import openpyxl
import sys

sys.stdout.reconfigure(encoding='utf-8')

wb = openpyxl.load_workbook("AttendanceTestCases_Master_Consolidated.xlsx", data_only=True)

for sheet_name in ["WT - Company Default", "User Scenarios (Add Here)"]:
    ws = wb[sheet_name]
    passed = sum(1 for r in range(2, ws.max_row + 1) if ws.cell(r, 9).value == "Pass")
    failed = sum(1 for r in range(2, ws.max_row + 1) if ws.cell(r, 9).value == "Fail")
    not_run = sum(1 for r in range(2, ws.max_row + 1) if ws.cell(r, 9).value == "Not-Run")
    print(f"Sheet '{sheet_name}': Passed={passed}, Failed={failed}, Not-Run={not_run}, Total={ws.max_row - 1}")

