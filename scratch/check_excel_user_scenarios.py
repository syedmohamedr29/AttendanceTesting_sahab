import sys
import openpyxl

sys.stdout.reconfigure(encoding='utf-8')

wb = openpyxl.load_workbook('AttendanceTestCases_Master_Consolidated.xlsx', data_only=True)
sheet = wb['User Scenarios (Add Here)']

print(f"Max row: {sheet.max_row}, Max col: {sheet.max_column}")

headers = [sheet.cell(1, c).value for c in range(1, sheet.max_column + 1)]
print("Headers:", headers)

# Count status
status_col = None
tc_id_col = None
for idx, h in enumerate(headers):
    if h and 'status' in str(h).lower():
        status_col = idx + 1
    if h and ('id' in str(h).lower() or 'tc' in str(h).lower()):
        tc_id_col = idx + 1

print(f"TC Col: {tc_id_col}, Status Col: {status_col}")

status_counts = {}
rows_data = []

for r in range(2, sheet.max_row + 1):
    tc_id = sheet.cell(r, 1).value
    status = sheet.cell(r, status_col).value if status_col else None
    if tc_id:
        status_counts[status] = status_counts.get(status, 0) + 1
        rows_data.append((tc_id, status))

print("Status counts:", status_counts)
print(f"Total rows with TC ID: {len(rows_data)}")

# Print any failed ones
failed = [r for r in rows_data if r[1] and 'fail' in str(r[1]).lower()]
print(f"Failed count: {len(failed)}")
print("Failed TCs:", failed)

