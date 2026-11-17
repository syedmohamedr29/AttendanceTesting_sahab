import openpyxl
from collections import Counter

wb = openpyxl.load_workbook('AttendanceTestCases_Master_Consolidated.xlsx', data_only=True)

target_sheets = [
    'WT - Company Default',
    'Policies - DTO Validations',
    'Holiday Calendar - Test Cases',
    'User Scenarios (Add Here)',
    'Attendance Policies'
]

for name in target_sheets:
    if name not in wb.sheetnames:
        print(f"Sheet NOT FOUND: {name}")
        continue
    ws = wb[name]
    print(f"\n==================================================")
    print(f"SHEET: {name} | Dimensions: {ws.dimensions} | Max Row: {ws.max_row}, Max Col: {ws.max_column}")
    
    # Read header row (row 1 or row 2)
    headers = [cell.value for cell in ws[1]]
    if all(h is None for h in headers[:5]) and ws.max_row > 1:
        headers = [cell.value for cell in ws[2]]
        header_row = 2
    else:
        header_row = 1
    print(f"Header row {header_row}: {headers[:12]}")
    
    # Identify status column
    status_col_idx = None
    for idx, h in enumerate(headers):
        if h and any(k in str(h).lower() for k in ['status', 'result', 'verdict', 'execution', 'actual']):
            print(f"  Possible status col: idx {idx+1} -> {h}")
            if status_col_idx is None or 'status' in str(h).lower() or 'verdict' in str(h).lower() or 'result' in str(h).lower():
                status_col_idx = idx + 1
    
    # Count values in status column
    if status_col_idx:
        vals = []
        for r in range(header_row + 1, ws.max_row + 1):
            v = ws.cell(row=r, column=status_col_idx).value
            if v is not None:
                vals.append(str(v).strip())
        counts = Counter(vals)
        print(f"Status distribution (Col {status_col_idx}): {dict(counts.most_common(10))}")
    else:
        print("No status column detected!")
