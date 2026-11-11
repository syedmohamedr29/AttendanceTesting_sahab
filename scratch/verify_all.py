import openpyxl

for fn in ['AttendanceTestCases_Master_Consolidated.xlsx', 'Attendance_Policies_Manual_API_TestCases_MongoDB.xlsx', 'AttendanceTestCases.xlsx']:
    wb = openpyxl.load_workbook(fn, data_only=True)
    ws = wb['Policy Defects Log']
    print(f'{fn}: max_row={ws.max_row} | Last Defect={ws.cell(ws.max_row, 1).value}')

for md in ['Attendance2_Defects_Gaps_and_Architecture_Inconsistencies_Report.md', 'Defects/Attendance2_Master_Defect_Log.md']:
    txt = open(md, encoding='utf-8').read()
    print(f'{md}: Size={len(txt)} | Has DEFECT-19: {"DEFECT-20261110-19" in txt} | Has DEFECT-23: {"DEFECT-20261110-23" in txt}')
