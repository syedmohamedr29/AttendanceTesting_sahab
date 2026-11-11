import openpyxl, sys
sys.stdout.reconfigure(encoding='utf-8')

for wb_name in ['AttendanceTestCases.xlsx', r'document (Enum and db collection)\AttendanceTestCases.xlsx']:
    wb = openpyxl.load_workbook(wb_name, data_only=True)
    for sname in wb.sheetnames:
        ws = wb[sname]
        for r_idx, row in enumerate(ws.iter_rows(values_only=True), 1):
            row_str = ' '.join(str(c) for c in row if c is not None)
            lower = row_str.lower()
            if any(k in lower for k in ['checklist', 'workschedulescreated', 'company service', 'companyservice', 'master']):
                print(f'{wb_name} [{sname}] R{r_idx}: {row_str[:150]}')
