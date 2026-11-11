import sys
import openpyxl

sys.stdout.reconfigure(encoding='utf-8')

wb = openpyxl.load_workbook('AttendanceTestCases.xlsx', data_only=True)
ws_loc = wb['Work Template - Location']
for c in range(1, ws_loc.max_column+1):
    print(ws_loc.cell(1, c).value, ':', ws_loc.cell(11, c).value)
print('='*50)
for c in range(1, ws_loc.max_column+1):
    print(ws_loc.cell(1, c).value, ':', ws_loc.cell(55, c).value)

print('='*50)
ws_comp = wb['Work Template - Company']
for c in range(1, ws_comp.max_column+1):
    print(ws_comp.cell(1, c).value, ':', ws_comp.cell(53, c).value)

