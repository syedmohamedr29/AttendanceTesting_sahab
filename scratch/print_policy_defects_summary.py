import openpyxl

wb = openpyxl.load_workbook('AttendanceTestCases_Master_Consolidated.xlsx', data_only=True)
ws = wb['Policy Defects Log']
for r in range(2, 16):
    defect_id = ws.cell(r, 1).value
    severity = ws.cell(r, 2).value
    title = ws.cell(r, 3).value
    endpoint = ws.cell(r, 4).value
    print(f"Row {r}: {defect_id} | {severity} | {endpoint} | {title[:80]}...")
