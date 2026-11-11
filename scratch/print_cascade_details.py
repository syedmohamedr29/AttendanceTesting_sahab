import openpyxl, sys
sys.stdout.reconfigure(encoding='utf-8')

wb = openpyxl.load_workbook(r'document (Enum and db collection)\AttendanceTestCases.xlsx', data_only=True)
ws = wb['Work Template - Company']
rows = list(ws.iter_rows(values_only=True))

for i, r in enumerate(rows):
    if r[0] and str(r[0]).startswith(('B-', 'C-', 'D-', 'E-', 'F-')):
        print(f"{r[0]} | {r[1]} | {r[2]} | {r[3]} | {r[4]}")
