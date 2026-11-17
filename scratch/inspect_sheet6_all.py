# -*- coding: utf-8 -*-
import openpyxl

wb = openpyxl.load_workbook('AttendanceTestCases_Master_Consolidated.xlsx', data_only=True)
sheet = wb['Holiday Calendar - Company']

print(f"Columns: {[sheet.cell(1, c).value for c in range(1, 12)]}")

rows = []
for r in range(2, sheet.max_row + 1):
    vals = [sheet.cell(r, c).value for c in range(1, 12)]
    if vals[0]:
        rows.append(vals)

print(f"Total rows in Sheet 6: {len(rows)}")

# Print by sections
current_section = None
for r in rows:
    tc_id, section, scenario, precond, expected, pri, ttype, env, status, remarks, origin = r[:11]
    if section != current_section:
        current_section = section
        print(f"\n=== SECTION: {section} ===")
    print(f"  {tc_id:12s} | {str(pri):2s} | {str(status):7s} | {str(scenario):45s} | Expected: {str(expected)[:50]}")
