import openpyxl
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

wb = openpyxl.load_workbook('AttendanceTestCases_Master_Consolidated.xlsx', data_only=True)
sheet = wb['Holiday Calendar - Test Cases']

print(f"Sheet title: {sheet.title}, max_row: {sheet.max_row}, max_column: {sheet.max_column}")
headers = [sheet.cell(1, c).value for c in range(1, sheet.max_column + 1)]
print(f"Headers: {headers}")

# Look at rows corresponding to our failed TCs
failed_rows = [2, 5, 6, 7, 9, 10, 11, 12, 13, 14, 17, 18, 19, 22, 24, 25, 53, 67, 68, 73, 75, 76, 77, 80, 81, 83, 87, 111, 128, 129, 130, 268, 283, 285, 312, 313, 314]

failed_tcs_data = []
for r in failed_rows:
    row_vals = {headers[c-1]: sheet.cell(r, c).value for c in range(1, len(headers) + 1)}
    row_vals['_row_idx'] = r
    failed_tcs_data.append(row_vals)

with open('scratch/failed_holiday_tcs_full_info.json', 'w', encoding='utf-8') as f:
    json.dump(failed_tcs_data, f, indent=2, default=str)

print(f"Extracted full details for {len(failed_tcs_data)} test cases to scratch/failed_holiday_tcs_full_info.json")

