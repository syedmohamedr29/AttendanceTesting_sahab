import openpyxl, re, os

md_path = 'reports/WORK_ASSIGNMENT_TEST_CASES.md'
if os.path.exists(md_path):
    with open(md_path, 'r', encoding='utf-8') as f:
        text = f.read()
    tc_matches = re.findall(r'\| \*\*(WA-[A-Z0-9\-]+)\*\*', text)
    print(f'WORK_ASSIGNMENT_TEST_CASES.md total TCs found in tables: {len(tc_matches)}')
    unique_tcs = list(dict.fromkeys(tc_matches))
    print(f'Unique TCs in markdown: {len(unique_tcs)}')

excel_files = [
    'AttendanceTestCases_Master_Consolidated.xlsx',
    'AttendanceTestCases.xlsx',
    'Attendance_Policies_Manual_API_TestCases_MongoDB.xlsx'
]

for ef in excel_files:
    if os.path.exists(ef):
        try:
            wb = openpyxl.load_workbook(ef, data_only=True)
            sheet_name = 'Work Assignments'
            if sheet_name in wb.sheetnames:
                ws = wb[sheet_name]
                rows = 0
                for row in ws.iter_rows(values_only=True):
                    if any(row):
                        rows += 1
                print(f'{ef} -> sheet "{sheet_name}" has {rows} total rows (1 header + {rows - 1} test cases).')
            else:
                print(f'{ef} -> sheet "{sheet_name}" NOT FOUND! sheets: {wb.sheetnames}')
        except Exception as e:
            print(f'Error reading {ef}: {e}')
    else:
        print(f'{ef} does not exist!')
