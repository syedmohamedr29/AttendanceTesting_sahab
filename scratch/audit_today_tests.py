import openpyxl
import sys

sys.stdout.reconfigure(encoding='utf-8')

wb = openpyxl.load_workbook('AttendanceTestCases_Master_Consolidated.xlsx', data_only=True)
ws = wb['User Scenarios (Add Here)']

print(f"Total Rows in User Scenarios: {ws.max_row}")

tested_today = []
for r in range(2, ws.max_row + 1):
    tc = ws.cell(r, 1).value
    sec = ws.cell(r, 2).value
    title = ws.cell(r, 3).value
    st = ws.cell(r, 9).value
    rem = str(ws.cell(r, 10).value or '')
    
    tested_today.append({
        "row": r,
        "tc": str(tc),
        "section": str(sec),
        "title": str(title),
        "status": str(st),
        "remarks": rem
    })

print(f"Total test cases: {len(tested_today)}")
pass_count = sum(1 for x in tested_today if str(x['status']).lower() == 'pass')
fail_count = sum(1 for x in tested_today if str(x['status']).lower() == 'fail')
not_run_count = sum(1 for x in tested_today if str(x['status']).lower() not in ['pass', 'fail'])

print(f"Pass: {pass_count} | Fail: {fail_count} | Not-Run: {not_run_count}")

# Print summary by company tested
print("\n--- Breakdown by Remarks / Company Mentioned ---")
att4 = [x for x in tested_today if "attendance 4" in x["remarks"].lower()]
att3 = [x for x in tested_today if "attendance 3" in x["remarks"].lower()]
part2 = [x for x in tested_today if "part 2" in x["section"].lower() or "defect-20261027" in x["remarks"].lower()]
defects = [x for x in tested_today if x["status"].lower() == "fail"]

print(f"Attendance 4 verified cases: {len(att4)}")
for x in att4:
    print(f"  {x['tc']}: {x['title'][:40]} -> {x['status']}")

print(f"\nPart 1 / Attendance 3 re-verified cases: {len(att3)}")
for x in att3:
    print(f"  {x['tc']}: {x['title'][:40]} -> {x['status']}")

print(f"\nPart 2 re-verified cases: {len(part2)}")
for x in part2:
    print(f"  {x['tc']}: {x['title'][:40]} -> {x['status']}")

print(f"\nTotal Failures / Defects: {len(defects)}")
for x in defects:
    print(f"  {x['tc']} ({x['section']}): {x['remarks'][:60]}")

