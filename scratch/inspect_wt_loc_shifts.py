import openpyxl
from collections import Counter

wb = openpyxl.load_workbook('AttendanceTestCases_Master_Consolidated.xlsx', data_only=True)

if 'WT - Location Shifts' in wb.sheetnames:
    ws = wb['WT - Location Shifts']
    print(f"SHEET: WT - Location Shifts | Max Row: {ws.max_row}, Max Col: {ws.max_column}")
    headers = [cell.value for cell in ws[1]]
    print("Headers:", headers)
    
    # Check status distribution
    status_col = None
    for idx, h in enumerate(headers):
        if h and 'status' in str(h).lower():
            status_col = idx + 1
            print(f"Status column found at {status_col}: {h}")
    
    if status_col:
        stats = [str(ws.cell(row=r, column=status_col).value).strip() for r in range(2, ws.max_row + 1)]
        print("Status count:", Counter(stats))
        
        # Print non-pass rows
        print("\nNon-pass / Failed rows in WT - Location Shifts:")
        for r in range(2, ws.max_row + 1):
            s = str(ws.cell(row=r, column=status_col).value or "").strip()
            if s and not s.lower().startswith('pass'):
                tc_id = ws.cell(row=r, column=1).value
                title = ws.cell(row=r, column=3).value
                remarks = ws.cell(row=r, column=10).value
                print(f"Row {r} | TC: {tc_id} | Stat: {s} | Title: {str(title)[:60]} | Remarks: {str(remarks)[:80]}")
else:
    print("WT - Location Shifts NOT in wb.sheetnames")
