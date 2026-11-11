import sys
import openpyxl
from collections import Counter

sys.stdout.reconfigure(encoding='utf-8')

wb = openpyxl.load_workbook('AttendanceTestCases_Master_Consolidated.xlsx', data_only=True)
ws_user = wb['User Scenarios (Add Here)']

types_user = [ws_user.cell(r, 7).value for r in range(2, ws_user.max_row+1)]
pri_user = [ws_user.cell(r, 6).value for r in range(2, ws_user.max_row+1)]

print("User Scenarios (Add Here) Types Distribution:")
for t, c in Counter(types_user).most_common():
    print(f"  {t}: {c}")

print("\nUser Scenarios Priority Distribution:")
for p, c in Counter(pri_user).most_common():
    print(f"  {p}: {c}")

