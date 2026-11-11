import openpyxl
from openpyxl.worksheet.table import Table, TableStyleInfo

wb = openpyxl.Workbook()
ws = wb.active
ws.title = "TestTable"

ws.append(["TC ID", "Category", "Status"])
ws.append(["TC-01", "Cat 1", "Pending"])
ws.append(["TC-02", "Cat 2", "Pass"])

tab = Table(displayName="TestTable1", ref="A1:C3")
style = TableStyleInfo(name="TableStyleMedium2", showFirstColumn=False, showLastColumn=False, showRowStripes=True, showColumnStripes=False)
tab.tableStyleInfo = style
ws.add_table(tab)

wb.save("scratch/test_table.xlsx")
print("Saved table test successfully!")

