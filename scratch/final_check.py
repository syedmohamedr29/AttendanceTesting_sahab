import openpyxl, os

print('--- EXCEL FILES CHECK ---')
for fn in ['AttendanceTestCases_Master_Consolidated.xlsx', 'Attendance_Policies_Manual_API_TestCases_MongoDB.xlsx', 'AttendanceTestCases.xlsx']:
    wb = openpyxl.load_workbook(fn, data_only=True)
    ws = wb['Policy Defects Log']
    print(f'{fn}: {ws.max_row} rows (Defects up to: {ws.cell(ws.max_row, 1).value})')

print('\n--- MARKDOWN DEFECT LOGS CHECK ---')
for md in ['Attendance2_Defects_Gaps_and_Architecture_Inconsistencies_Report.md', 'Defects/Attendance2_Master_Defect_Log.md']:
    txt = open(md, encoding='utf-8').read()
    has15 = 'DEFECT-20261110-15' in txt
    has18 = 'DEFECT-20261110-18' in txt
    print(f'{md}: Size={len(txt)} bytes | DEFECT-15={has15} | DEFECT-18={has18}')

print('\n--- STANDALONE DELETE REPORTS CHECK ---')
for r in ['reports/WORK_TEMPLATE_DELETE_EXECUTION.md', 'defects/WORK_TEMPLATE_DELETE_DEFECTS.md']:
    txt = open(r, encoding='utf-8').read()
    print(f'{r}: Size={len(txt)} bytes, Lines={len(txt.splitlines())}')
