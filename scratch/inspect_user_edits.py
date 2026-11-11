import openpyxl
import os
import datetime
import sys

sys.stdout.reconfigure(encoding='utf-8')

fname = 'CompanyDefault_DTO_Validation_TestCases.xlsx'
mtime = os.path.getmtime(fname)
mod_time = datetime.datetime.fromtimestamp(mtime).strftime('%Y-%m-%d %H:%M:%S')
print(f"=== Checking {fname} (Modified: {mod_time}) ===")

try:
    wb = openpyxl.load_workbook(fname, data_only=True)
    ws = wb['CDWT DTO Validations']
    
    updated_rows = []
    status_counts = {}
    
    for r in range(2, ws.max_row + 1):
        tc_id = ws.cell(r, 1).value
        scenario = ws.cell(r, 5).value
        auto_status = ws.cell(r, 11).value
        manual_status = ws.cell(r, 12).value
        http_code = ws.cell(r, 13).value
        notes = ws.cell(r, 14).value
        
        status_counts[manual_status] = status_counts.get(manual_status, 0) + 1
        
        # Check if user updated this row from default 'Pending' or filled actual http / notes
        if manual_status != 'Pending' or http_code is not None or notes is not None:
            updated_rows.append((r, tc_id, scenario, auto_status, manual_status, http_code, notes))
            
    print(f"Total Rows: {ws.max_row - 1}")
    print(f"Status Breakdown: {status_counts}")
    print(f"\nUser Updated Rows ({len(updated_rows)} rows found):")
    for r, tc, sc, auto_s, man_s, code, note in updated_rows:
        print(f"  Row {r:2d} | TC: {tc} | Manual: {man_s} | Code: {code} | Notes: {note}")

    # Also check SUMMARY sheet values
    print("\n=== SUMMARY Sheet Values ===")
    ws_sum = wb['SUMMARY']
    for r in range(4, 16):
        metric = ws_sum.cell(r, 1).value
        count = ws_sum.cell(r, 2).value
        pct = ws_sum.cell(r, 3).value
        if metric:
            print(f"  Row {r:2d}: {metric:<35} | {str(count):<10} | {str(pct)}")

except Exception as e:
    print(f"Error reading workbook: {e}")

