import sys
import openpyxl
from collections import defaultdict

sys.stdout.reconfigure(encoding='utf-8')

wb = openpyxl.load_workbook('AttendanceTestCases_Master_Consolidated.xlsx', data_only=True)

ws_user = wb['User Scenarios (Add Here)']
user_ids = []
user_scens = []
for r in range(2, ws_user.max_row+1):
    tc = ws_user.cell(r, 1).value
    sc = ws_user.cell(r, 3).value
    if tc:
        user_ids.append((tc, r))
    if sc:
        user_scens.append((sc, r))

print(f"Total rows in 'User Scenarios (Add Here)': {len(user_ids)}")

id_counts = defaultdict(list)
for tc, r in user_ids:
    id_counts[tc].append(r)

dups_user_id = {k: v for k, v in id_counts.items() if len(v) > 1}
print("Duplicate TC IDs in 'User Scenarios (Add Here)':", dups_user_id)

scen_counts = defaultdict(list)
for sc, r in user_scens:
    scen_counts[sc.strip().lower()].append(r)

dups_user_scen = {k: v for k, v in scen_counts.items() if len(v) > 1}
print("Duplicate Scenarios in 'User Scenarios (Add Here)':", len(dups_user_scen))
for k, v in dups_user_scen.items():
    print(f"  Rows {v}: {k[:80]}")

