import openpyxl, sys, os
sys.stdout.reconfigure(encoding='utf-8')

wb = openpyxl.load_workbook(r'document (Enum and db collection)\AttendanceTestCases.xlsx', data_only=True)
print("=== Work Template - Company ===")
ws = wb['Work Template - Company']
for r in ws.iter_rows(values_only=True):
    line = ' | '.join(str(c) for c in r if c is not None)
    if any(k in line.lower() for k in ['plan', 'location', 'cascade', 'locwopl', 'default', 'sync', 'created']):
        print(line[:140])

print("\n=== Work Plan - Regular ===")
ws2 = wb['Work Plan - Regular']
for r in ws2.iter_rows(values_only=True):
    line = ' | '.join(str(c) for c in r if c is not None)
    if any(k in line.lower() for k in ['default', 'locwopl', 'loc', 'template', 'cascade']):
        print(line[:140])
