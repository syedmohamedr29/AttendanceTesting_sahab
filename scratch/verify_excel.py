import openpyxl
import os
import datetime

for fname in ['CompanyDefault_DTO_Validation_TestCases.xlsx', 'AttendanceTestCases_Master_Consolidated.xlsx']:
    mtime = os.path.getmtime(fname)
    mod_time = datetime.datetime.fromtimestamp(mtime).strftime('%Y-%m-%d %H:%M:%S')
    print(f"=== {fname} (Modified: {mod_time}) ===")
    wb = openpyxl.load_workbook(fname)
    print("Sheets:", wb.sheetnames)
    print("Active sheet:", wb.active.title)
    for sheet_name in wb.sheetnames:
        if 'DTO' in sheet_name or sheet_name == 'SUMMARY':
            ws = wb[sheet_name]
            print(f"  [{sheet_name}] max_row={ws.max_row}, max_col={ws.max_column}")
            print(f"  [{sheet_name}] AutoFilter={ws.auto_filter.ref}")
            print(f"  [{sheet_name}] DV count={len(ws.data_validations.dataValidation)}")
            if len(ws.data_validations.dataValidation) > 0:
                for dv in ws.data_validations.dataValidation:
                    print(f"    DV: sqref={dv.sqref}, formula1={dv.formula1}, showDropDown={dv.showDropDown}")
            # check row 1 headers
            headers = [ws.cell(1, c).value for c in range(1, 15)]
            print(f"    Headers: {headers[:6]} ... {headers[10:14]}")
            # check row 2 sample
            row2 = [ws.cell(2, c).value for c in range(1, 15)]
            print(f"    Row 2: TC={row2[0]}, Scenario={row2[4]}, Status={row2[10]}")
    print()

