import sys
import openpyxl

sys.stdout.reconfigure(encoding='utf-8')

wb = openpyxl.load_workbook('AttendanceTestCases_Master_Consolidated.xlsx', data_only=True)

print("Workbook sheets and row counts:")
total_cdwt_tcs = 0

# 1. WT - Company Default sheet
ws_comp = wb['WT - Company Default']
cdwt_core_count = ws_comp.max_row - 1
print(f"Sheet 'WT - Company Default': {cdwt_core_count} test cases")

# 2. User Scenarios (Add Here) sheet
ws_user = wb['User Scenarios (Add Here)']
user_count = ws_user.max_row - 1
print(f"Sheet 'User Scenarios (Add Here)': {user_count} custom test cases")

# Count how many in User Scenarios are CDWT specific
cdwt_user_tcs = []
for r in range(2, ws_user.max_row+1):
    tc = ws_user.cell(r, 1).value
    sec = ws_user.cell(r, 2).value
    scen = ws_user.cell(r, 3).value
    inp = ws_user.cell(r, 4).value
    text = f"{sec} {scen} {inp}".lower()
    if any(k in text for k in ['company default', 'cdwt', 'v1.0', 'v2.0', 'v3.0', 'v4.0', 'versions', 'sync-status', 'apply-sync', 'placeholder tenant', 'workschedulecreated', 'header location']):
        cdwt_user_tcs.append(tc)

print(f"CDWT-specific test cases in 'User Scenarios (Add Here)': {len(cdwt_user_tcs)}")
print(f"Total Dedicated CDWT Test Cases: {cdwt_core_count + len(cdwt_user_tcs)} test cases!")

# Check INDEX sheet
ws_idx = wb['INDEX']
print("\nINDEX Summary:")
for r in range(4, ws_idx.max_row+1):
    vals = [ws_idx.cell(r, c).value for c in range(1, 9) if ws_idx.cell(r, c).value is not None]
    if vals:
        print(f"  {vals[0]}: {vals[1]} -> Total: {vals[2]}")

