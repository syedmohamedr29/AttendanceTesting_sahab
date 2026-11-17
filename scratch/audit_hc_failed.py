import openpyxl

wb = openpyxl.load_workbook('AttendanceTestCases_Master_Consolidated.xlsx', data_only=True)
sheet_name = 'Holiday Calendar - Test Cases'
ws = wb[sheet_name]
print("Total rows in sheet:", ws.max_row)
headers = [cell.value for cell in ws[1]]
print("Headers:", headers)

failed_rows = []
for r in range(2, ws.max_row + 1):
    row_vals = [ws.cell(row=r, column=c).value for c in range(1, len(headers) + 1)]
    status = ws.cell(row=r, column=9).value
    qa_remarks = ws.cell(row=r, column=10).value
    tc_id = ws.cell(row=r, column=1).value
    scenario = ws.cell(row=r, column=3).value
    expected = ws.cell(row=r, column=5).value
    
    if status and "fail" in str(status).lower():
        failed_rows.append((r, tc_id, scenario, expected, status, qa_remarks))
        print(f"Row {r:3d}: TC={tc_id} | Scenario={scenario[:40]} | Expected={expected[:40]} | Status={status} | Remarks={str(qa_remarks)[:60]}")

print(f"\nTotal failed rows in {sheet_name}: {len(failed_rows)}")
