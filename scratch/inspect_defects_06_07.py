import openpyxl
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

print("=== CHECKING EXCEL FOR USER-137 AND USER-138 ===")
wb = openpyxl.load_workbook('AttendanceTestCases_Master_Consolidated.xlsx', data_only=True)
ws = wb['User Scenarios (Add Here)']
header = [ws.cell(row=1, column=c).value for c in range(1, ws.max_column + 1)]

for r in range(2, ws.max_row + 1):
    tc = ws.cell(row=r, column=1).value
    if tc in ['USER-137', 'USER-138', 'DTO-VAL-06', 'DTO-VAL-07']:
        row_vals = {header[c-1]: ws.cell(row=r, column=c).value for c in range(1, ws.max_column + 1)}
        print(f"\nRow {r}: {tc}")
        for k, v in row_vals.items():
            if v is not None:
                print(f"  {k}: {v}")

print("\n=== CHECKING DEFECT LOGS ===")
with open('Defects/Attendance2_Master_Defect_Log.md', 'r', encoding='utf-8') as f:
    text1 = f.read()

for d_id in ['DEFECT-20261027-06', 'DEFECT-20261027-07']:
    m = re.findall(rf'(#{2,4}\s+.*?{d_id}.*?(?=#{2,4}\s+|\Z))', text1, re.DOTALL)
    if m:
        print(f"\n--- Master Defect Log: {d_id} ---")
        print(m[0][:1500])
    else:
        print(f"Not found as header: {d_id}")

with open('Attendance2_Defects_Gaps_and_Architecture_Inconsistencies_Report.md', 'r', encoding='utf-8') as f:
    text2 = f.read()

for d_id in ['DEFECT-20261027-06', 'DEFECT-20261027-07']:
    m = re.findall(rf'(#### Defect `?{d_id}`?.*?(?=#### Defect|\Z))', text2, re.DOTALL)
    if m:
        print(f"\n--- Report: {d_id} ---")
        print(m[0][:1500])
    else:
        print(f"Not found in Report: {d_id}")

