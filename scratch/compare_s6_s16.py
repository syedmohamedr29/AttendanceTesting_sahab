# -*- coding: utf-8 -*-
import openpyxl

wb = openpyxl.load_workbook('AttendanceTestCases_Master_Consolidated.xlsx', data_only=True)
s6 = wb['Holiday Calendar - Company']
s16 = wb['Holiday Calendar - Test Cases']

print(f"Sheet 6 rows: {s6.max_row}")
print(f"Sheet 16 rows: {s16.max_row}")

# Check columns of Sheet 16
s16_cols = [s16.cell(1, c).value for c in range(1, 15)]
print(f"Sheet 16 columns: {s16_cols}")

# Collect all Sheet 16 TC IDs and results
s16_data = {}
for r in range(2, s16.max_row + 1):
    tc = s16.cell(r, 1).value or s16.cell(r, 2).value
    status = s16.cell(r, 9).value or s16.cell(r, 8).value or s16.cell(r, 7).value
    # find status column
    for c in range(1, 15):
        val = str(s16.cell(r, c).value)
        if val in ['Pass', 'Fail', 'FAIL', 'PASS', 'Pass (By Design)']:
            status = val
            break
    s16_data[tc] = {
        'status': status,
        'row': r,
        'scenario': s16.cell(r, 3).value,
        'remarks': s16.cell(r, 10).value
    }

print(f"Total Sheet 16 TCs indexed: {len(s16_data)}")

# Sample Sheet 16 entries
for k, v in list(s16_data.items())[:10]:
    print(f"  {k}: {v['status']} | {str(v['scenario'])[:40]}")
