from openpyxl.worksheet.datavalidation import DataValidation
from xml.etree import ElementTree as ET

dv = DataValidation(type='list', formula1='"A,B,C"')
print('Default showDropDown:', repr(dv.showDropDown))
node = dv.to_tree()
print('Default XML:', ET.tostring(node, encoding='utf-8').decode('utf-8'))

dv.showDropDown = True
node = dv.to_tree()
print('With True XML:', ET.tostring(node, encoding='utf-8').decode('utf-8'))

dv.showDropDown = False
node = dv.to_tree()
print('With False XML:', ET.tostring(node, encoding='utf-8').decode('utf-8'))

dv.showDropDown = None
node = dv.to_tree()
print('With None XML:', ET.tostring(node, encoding='utf-8').decode('utf-8'))

