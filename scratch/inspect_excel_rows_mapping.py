import openpyxl

wb = openpyxl.load_workbook('AttendanceTestCases_Master_Consolidated.xlsx', data_only=True)

for sheet_name in ['WT - Company Default', 'User Scenarios (Add Here)']:
    ws = wb[sheet_name]
    print(f"\n==================== Sheet: {sheet_name} ====================")
    headers = [ws.cell(1, c).value for c in range(1, 15)]
    print("Headers:", headers)
    for r in range(2, ws.max_row + 1):
        tc_id = ws.cell(r, 1).value
        sec = ws.cell(r, 2).value
        scen = ws.cell(r, 3).value
        pri = ws.cell(r, 6).value
        status = ws.cell(r, 9).value
        # Check if DTO or validation related
        if tc_id and (tc_id.startswith('ROOT-A') or (tc_id.startswith('USER-') and int(tc_id.split('-')[1]) in [
            14, 15, 17, 33, 34, 35, 36, 37, 38, 39, 47, 59, 60, 61, 62, 63, 64, 66, 67, 68, 70, 71, 72, 73, 74, 75, 76, 89, 90, 95, 96, 97, 98, 124
        ])):
            print(f"Row {r:3d} | ID: {tc_id:<10} | Pri: {pri} | Status: {status} | Sec: {sec[:30]} | Scen: {scen[:40]}")

