import openpyxl
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

wb = openpyxl.load_workbook('AttendanceTestCases_Master_Consolidated.xlsx', data_only=True)
ws = wb['User Scenarios (Add Here)']

fails = []
for r in range(2, ws.max_row + 1):
    val = ws.cell(r, 9).value
    if val == 'Fail':
        fails.append({
            'row': r,
            'id': ws.cell(r, 1).value,
            'sec': ws.cell(r, 2).value,
            'scen': ws.cell(r, 3).value,
            'inp': ws.cell(r, 4).value,
            'exp': ws.cell(r, 5).value,
            'pri': ws.cell(r, 6).value,
            'remark': ws.cell(r, 10).value
        })

print(f"Total Failed User Scenarios: {len(fails)}")
for f in fails:
    print(f"Row {f['row']:3d} | {f['id']:<10} | {f['pri']} | {f['scen'][:40]:<40} | {str(f['remark'])[:60]}")

with open("scratch/failed_user_scenarios.json", "w", encoding="utf-8") as out:
    json.dump(fails, out, indent=2, ensure_ascii=False)

