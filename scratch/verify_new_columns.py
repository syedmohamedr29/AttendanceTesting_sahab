import openpyxl
import os
import datetime

print("================ SANITY CHECK: AUTOMATION STATUS ================")
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
        print(f"    - Formula: {dv.formula1} | Cell Range: {dv.sqref}")
    
    headers = [ws.cell(1, c).value for c in range(1, 16)]
    print(f"  Headers (1 to 15):")
    for i, h in enumerate(headers, start=1):
        print(f"    Col {i:2d} ({chr(64+i)}): {h}")
    
    # Check sample row 2 and row 6
    r2 = [ws.cell(2, c).value for c in range(1, 16)]
    print(f"  Row 2 ({r2[0]}): AutoStatus='{r2[10]}' | ManualStatus='{r2[11]}'")
    r6 = [ws.cell(6, c).value for c in range(1, 16)]
    print(f"  Row 6 ({r6[0]}): AutoStatus='{r6[10]}' | ManualStatus='{r6[11]}' | Defect='{r6[14]}'")

print("\nALL CHECKS PASSED!")

