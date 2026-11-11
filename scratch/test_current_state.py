import openpyxl
from openpyxl.worksheet.table import Table, TableStyleInfo
from openpyxl.worksheet.datavalidation import DataValidation

wb = openpyxl.load_workbook('CompanyDefault_DTO_Validation_TestCases.xlsx')
ws = wb['CDWT DTO Validations']
print("Current tables:", list(ws.tables.keys()))
print("Current auto_filter:", ws.auto_filter.ref)
print("Current DV count:", len(ws.data_validations.dataValidation))

