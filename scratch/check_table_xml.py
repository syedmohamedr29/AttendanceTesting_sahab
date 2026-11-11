import openpyxl
from openpyxl.worksheet.table import Table, TableStyleInfo

wb = openpyxl.Workbook()
ws = wb.active
ws.title = "Test"
ws.append(["A", "B", "C"])
ws.append([1, 2, 3])

tab = Table(displayName="TestTable", ref="A1:C2")
tab.tableStyleInfo = TableStyleInfo(name="TableStyleLight1")
ws.add_table(tab)

wb.save("scratch/test_tab_only.xlsx")

# Check sheet XML
import zipfile
with zipfile.ZipFile("scratch/test_tab_only.xlsx", "r") as z:
    for name in z.namelist():
        if "sheet1" in name or "table1" in name:
            print(f"--- {name} ---")
            print(z.read(name).decode("utf-8")[:300])

