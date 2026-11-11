from openpyxl.worksheet.datavalidation import DataValidation
import xml.etree.ElementTree as ET

dv = DataValidation(type="list", formula1='"Pending,Pass,Failed,Backlog,Noted"', allow_blank=True)
print("Default XML:", ET.tostring(dv.to_tree(), encoding="utf-8").decode("utf-8"))

dv.showDropDown = None
print("With None XML:", ET.tostring(dv.to_tree(), encoding="utf-8").decode("utf-8"))

