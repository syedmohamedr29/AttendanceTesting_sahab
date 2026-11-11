from openpyxl.worksheet.datavalidation import DataValidation
import openpyxl

dv = DataValidation(type="list", formula1='"A,B,C"')
print("showDropDown default:", dv.showDropDown)
print("showInputMessage:", dv.showInputMessage)
print("showErrorMessage:", dv.showErrorMessage)

# In OpenXML standard for list validation:
# If showDropDown="1", Excel SUPPRESSES the dropdown arrow!
# To SHOW the dropdown arrow in Excel, showDropDown must be omitted or False or None!

