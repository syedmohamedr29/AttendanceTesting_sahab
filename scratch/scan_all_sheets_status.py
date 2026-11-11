import openpyxl
import sys

sys.stdout.reconfigure(encoding='utf-8')

wb = openpyxl.load_workbook('AttendanceTestCases_Master_Consolidated.xlsx', data_only=True)

stats = {}

for name in wb.sheetnames:
    if name == "INDEX":
        continue
    ws = wb[name]
    
    # Find status column
    status_col = None
    for c in range(1, ws.max_column + 1):
        val = str(ws.cell(1, c).value or "")
        if "status" in val.lower():
            status_col = c
            break
            
    if not status_col:
        status_col = 9 # default
        
    passed = 0
    failed = 0
    not_run = 0
    other = 0
    
    for r in range(2, ws.max_row + 1):
        st = str(ws.cell(r, status_col).value or "").strip().lower()
        if st == "pass":
            passed += 1
        elif st == "fail":
            failed += 1
        elif st in ["not-run", "not run", "none", ""]:
            not_run += 1
        else:
            other += 1
            
    total = ws.max_row - 1
    stats[name] = {
        "total": total,
        "passed": passed,
        "failed": failed,
        "not_run": not_run,
        "other": other
    }
    print(f"Sheet: {name:<30} | Total: {total:4d} | Pass: {passed:3d} | Fail: {failed:3d} | Not-Run: {not_run:4d}")

tot_tcs = sum(s["total"] for s in stats.values())
tot_pass = sum(s["passed"] for s in stats.values())
tot_fail = sum(s["failed"] for s in stats.values())
tot_not_run = sum(s["not_run"] for s in stats.values())

print(f"\nOVERALL CONSOLIDATED TOTALS:")
print(f"Total TCs: {tot_tcs} | Passed: {tot_pass} | Failed: {tot_fail} | Not-Run: {tot_not_run}")

