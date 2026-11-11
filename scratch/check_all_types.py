import sys
import openpyxl
from collections import Counter

sys.stdout.reconfigure(encoding='utf-8')

wb = openpyxl.load_workbook('AttendanceTestCases_Master_Consolidated.xlsx', data_only=True)

all_types = []
for sheet in wb.sheetnames:
    if sheet == 'INDEX':
        continue
    ws = wb[sheet]
    # find Type column
    type_col = 7
    for c in range(1, ws.max_column+1):
        h = str(ws.cell(1, c).value or '').lower()
        if h == 'type':
            type_col = c
            break
    for r in range(2, ws.max_row+1):
        val = ws.cell(r, type_col).value
        if val:
            all_types.append(str(val).strip().lower())

print("Grand Total Types Across Entire Master File (1,206 TCs):")
for t, c in Counter(all_types).most_common(15):
    print(f"  {t}: {c}")

