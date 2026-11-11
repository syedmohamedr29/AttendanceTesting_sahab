import openpyxl
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

wb = openpyxl.load_workbook('AttendanceTestCases_Master_Consolidated.xlsx', data_only=True)
ws = wb['User Scenarios (Add Here)']

tcs = []
for r in range(2, ws.max_row + 1):
    tc_id = ws.cell(r, 1).value
    sec = ws.cell(r, 2).value
    scenario = ws.cell(r, 3).value
    input_pre = ws.cell(r, 4).value
    expected = ws.cell(r, 5).value
    pri = ws.cell(r, 6).value
    tc_type = ws.cell(r, 7).value
    env = ws.cell(r, 8).value
    status = ws.cell(r, 9).value
    remarks = ws.cell(r, 10).value
    origin = ws.cell(r, 11).value

    if tc_id:
        tcs.append({
            "row": r,
            "tc_id": str(tc_id).strip(),
            "section": str(sec or '').strip(),
            "scenario": str(scenario or '').strip(),
            "input_pre": str(input_pre or '').strip(),
            "expected": str(expected or '').strip(),
            "priority": str(pri or '').strip(),
            "type": str(tc_type or '').strip(),
            "status": str(status or '').strip(),
            "remarks": str(remarks or '').strip(),
            "origin": str(origin or '').strip()
        })

print(f"Total test cases extracted: {len(tcs)}")
with open("scratch/all_user_scenarios_dump.json", "w") as f:
    json.dump(tcs, f, indent=2)

print("Saved to scratch/all_user_scenarios_dump.json")

