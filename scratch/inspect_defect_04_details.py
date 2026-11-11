import sys
import openpyxl

sys.stdout.reconfigure(encoding='utf-8')

# Check Master Defect Log
with open('Defects/Attendance2_Master_Defect_Log.md', 'r', encoding='utf-8') as f:
    text = f.read()

import re
matches = re.findall(r'(### DEFECT-20261026-04.*?(?=### DEFECT-|\Z))', text, re.DOTALL)
if matches:
    print("=== Master Defect Log: DEFECT-20261026-04 ===")
    print(matches[0][:2000])
else:
    # search for USER-04 or USER-131
    print("Not found as DEFECT-20261026-04 header, searching for section containing USER-04 / USER-131...")
    m = re.findall(r'(#{2,4}\s+.*?USER-04.*?)(?=#{2,4}\s+|\Z)', text, re.DOTALL)
    for item in m:
        print(item[:1500])

# Check Report
with open('Attendance2_Defects_Gaps_and_Architecture_Inconsistencies_Report.md', 'r', encoding='utf-8') as f:
    text2 = f.read()

m2 = re.findall(r'(#### Defect `DEFECT-20261026-04`.*?(?=#### Defect|\Z))', text2, re.DOTALL)
if m2:
    print("=== Report: DEFECT-20261026-04 ===")
    print(m2[0][:2000])

# Check Excel USER-04 and USER-131
wb = openpyxl.load_workbook('AttendanceTestCases_Master_Consolidated.xlsx', data_only=True)
if 'User Scenarios (Add Here)' in wb.sheetnames:
    ws = wb['User Scenarios (Add Here)']
    for row in range(1, ws.max_row + 1):
        tc_id = ws.cell(row=row, column=1).value
        if tc_id in ['USER-04', 'USER-131', 'USER-122']:
            vals = [str(ws.cell(row=row, column=c).value) for c in range(1, 15)]
            print(f"Excel Row {row}: {tc_id} -> {vals[:8]}")

