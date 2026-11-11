import openpyxl
from openpyxl.worksheet.table import Table, TableStyleInfo
from openpyxl.worksheet.datavalidation import DataValidation

wb = openpyxl.Workbook()
ws = wb.active
ws.title = "TestTableDV"

ws.append(["TC ID", "Category", "Manual Status"])
ws.append(["TC-01", "Cat 1", "Pending"])
ws.append(["TC-02", "Cat 2", "Pass"])

tab = Table(displayName="TestTableDV1", ref="A1:C3")
style = TableStyleInfo(name="TableStyleMedium2", showFirstColumn=False, showLastColumn=False, showRowStripes=True, showColumnStripes=False)
tab.tableStyleInfo = style
ws.add_table(tab)

dv = DataValidation(type="list", formula1='"Pending,Pass,Failed,Backlog,Noted"', allow_blank=True)
ws.add_data_validation(dv)
dv.add("C2:C3")

wb.save("scratch/test_table_dv.xlsx")
print("Saved table with DV successfully!")

# Re-read
wb2 = openpyxl.load_workbook("scratch/test_table_dv.xlsx")
ws2 = wb2.active
print("Tables in re-read:", list(ws2.tables.keys()))
print("DV count in re-read:", len(ws2.data_validations.dataValidation))
for d in ws2.data_validations.dataValidation:
    print("  DV formula:", d.formula1, "sqref:", d.sqref)

