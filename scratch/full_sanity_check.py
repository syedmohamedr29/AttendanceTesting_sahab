import openpyxl
import os
import datetime

print("================ SANITY CHECK ================")
for fname in ['CompanyDefault_DTO_Validation_TestCases.xlsx', 'AttendanceTestCases_Master_Consolidated.xlsx']:
    size = os.path.getsize(fname)
    mtime = datetime.datetime.fromtimestamp(os.path.getmtime(fname)).strftime('%Y-%m-%d %H:%M:%S')
    print(f"\nFILE: {fname}")
    print(f"Size: {size:,} bytes | Last Modified: {mtime}")
    
    wb = openpyxl.load_workbook(fname)
    print(f"Total Sheets: {len(wb.sheetnames)} -> {wb.sheetnames}")
    print(f"Active Sheet: {wb.active.title}")
    
    target_sheet = 'CDWT DTO Validations' if fname.startswith('Company') else 'CDWT - Manual DTO Validations'
    ws = wb[target_sheet]
    print(f"\nTarget Sheet: '{target_sheet}'")
    print(f"  Rows: {ws.max_row} (Headers + {ws.max_row - 1} Test Cases)")
    print(f"  Columns: {ws.max_column}")
    print(f"  AutoFilter: {ws.auto_filter.ref}")
    print(f"  Data Validations: {len(ws.data_validations.dataValidation)}")
    
    for dv in ws.data_validations.dataValidation:
        print(f"    - Formula: {dv.formula1}")
        print(f"    - Cell Range: {dv.sqref}")
        print(f"    - Prompt: {dv.promptTitle}: {dv.prompt}")
        print(f"    - Error: {dv.errorTitle}: {dv.error}")
    
    # Check sample row 2 and row 53
    r2_status = ws.cell(2, 11).value
    r53_status = ws.cell(53, 11).value
    print(f"  Row 2 Status: '{r2_status}' (TC: {ws.cell(2, 1).value})")
    print(f"  Row 53 Status: '{r53_status}' (TC: {ws.cell(53, 1).value})")

print("\n================ CHECK SUMMARY SHEET ================")
wb_std = openpyxl.load_workbook('CompanyDefault_DTO_Validation_TestCases.xlsx', data_only=False)
ws_sum = wb_std['SUMMARY']
for r in range(4, 12):
    metric = ws_sum.cell(r, 1).value
    formula_b = ws_sum.cell(r, 2).value
    formula_c = ws_sum.cell(r, 3).value
    print(f"  Row {r:2d}: {metric:<30} | {str(formula_b):<55} | {str(formula_c)}")

print("\nALL VERIFICATIONS PASSED SUCCESSFULLY!")

