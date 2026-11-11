import openpyxl

for fname in ['CompanyDefault_DTO_Validation_TestCases.xlsx', 'AttendanceTestCases_Master_Consolidated.xlsx']:
    wb = openpyxl.load_workbook(fname)
    sheet_name = 'CDWT DTO Validations' if fname.startswith('Company') else 'CDWT - Manual DTO Validations'
    ws = wb[sheet_name]
    
    # Row 3 is CDWT-DTO-02
    ws.cell(3, 15).value = "DEFECT-20261029-01: Accepts expired & forged JWT; DEFECT-20261029-02: Missing Swagger OAuth2"
    
    wb.save(fname)
    print(f"Updated {fname} successfully!")

