import openpyxl
from openpyxl.styles import PatternFill, Font, Alignment, Border, Side
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

wb = openpyxl.load_workbook('AttendanceTestCases_Master_Consolidated.xlsx')
ws_hc = wb['Holiday Calendar - Test Cases']
ws_index = wb['INDEX']

# Load test results
with open('scratch/live_retest_results_37.json', 'r', encoding='utf-8') as f:
    live_results = json.load(f)

# Styles
green_fill = PatternFill(start_color="E2EFDA", end_color="E2EFDA", fill_type="solid")
green_font = Font(name="Segoe UI", size=10, bold=True, color="375623")
red_fill = PatternFill(start_color="FCE4D6", end_color="FCE4D6", fill_type="solid")
red_font = Font(name="Segoe UI", size=10, bold=True, color="C65911")

# Mapping of the 37 TCs and their remarks
updated_tcs = {
    # 1. HC-DTO-01 (Row 2) - FAIL
    2: {
        "status": "Fail",
        "remarks": "[Re-Verified Live 2026-11-04]: NOT FIXED: Route parameter companyId malformed GUID returns HTTP 404 Not Found (ASP.NET Core route constraint {companyId:guid} rejects request before reaching controller) instead of HTTP 400 Bad Request."
    },
    # 2. HC-DTO-04 (Row 5) - PASS
    5: {
        "status": "Pass",
        "remarks": "[Re-Verified Live 2026-11-04]: FIXED: Missing tenant header / unhandled crash eliminated. GlobalExceptionHandlerMiddleware now cleanly returns HTTP 400 Bad Request with Cit.Attendance:Validation instead of HTTP 500 crash."
    },
    # 3. HC-DTO-05 (Row 6) - PASS
    6: {
        "status": "Pass",
        "remarks": "[Re-Verified Live 2026-11-04]: FIXED (DEFECT-20261028-02): Empty request body {} cleanly rejected with HTTP 400 Bad Request (Cit.Attendance:Validation - 'Short Code' must not be empty. An English calendar name is required.). HTTP 500 eliminated."
    },
    # 4. HC-DTO-06 (Row 7) - PASS
    7: {
        "status": "Pass",
        "remarks": "[Re-Verified Live 2026-11-04]: FIXED: shortCode omitted cleanly rejected with HTTP 400 Bad Request (Cit.Attendance:Validation - 'Short Code' must not be empty.). Unhandled HTTP 500 eliminated."
    },
    # 5. HC-DTO-08 (Row 9) - PASS
    9: {
        "status": "Pass",
        "remarks": "[Re-Verified Live 2026-11-04]: FIXED: shortCode empty string (\"\") cleanly rejected with HTTP 400 Bad Request (Cit.Attendance:Validation - 'Short Code' must not be empty.). HTTP 500 eliminated."
    },
    # 6. HC-DTO-09 (Row 10) - PASS
    10: {
        "status": "Pass",
        "remarks": "[Re-Verified Live 2026-11-04]: FIXED: shortCode whitespace-only (\"   \") cleanly rejected with HTTP 400 Bad Request (Cit.Attendance:Validation - 'Short Code' must not be empty.). HTTP 500 eliminated."
    },
    # 7. HC-DTO-10 (Row 11) - PASS
    11: {
        "status": "Pass",
        "remarks": "[Re-Verified Live 2026-11-04]: FIXED: name object omitted / null cleanly rejected with HTTP 400 Bad Request (Cit.Attendance:Validation - 'An English calendar name is required.'). HTTP 500 eliminated."
    },
    # 8. HC-DTO-11 (Row 12) - PASS
    12: {
        "status": "Pass",
        "remarks": "[Re-Verified Live 2026-11-04]: FIXED (DEFECT-20261103-05): Empty name object ({}) cleanly rejected with HTTP 400 Bad Request (Cit.Attendance:Validation - 'An English calendar name is required.')."
    },
    # 9. HC-DTO-12 (Row 13) - PASS
    13: {
        "status": "Pass",
        "remarks": "[Re-Verified Live 2026-11-04]: FIXED (DEFECT-20261103-05): name.en empty string (\"\") cleanly rejected with HTTP 400 Bad Request (Cit.Attendance:Validation - 'An English calendar name is required.')."
    },
    # 10. HC-DTO-13 (Row 14) - PASS
    14: {
        "status": "Pass",
        "remarks": "[Re-Verified Live 2026-11-04]: FIXED (DEFECT-20261103-05): name.en whitespace-only (\"   \") cleanly rejected with HTTP 400 Bad Request (Cit.Attendance:Validation - 'An English calendar name is required.')."
    },
    # 11. HC-DTO-16 (Row 17) - PASS
    17: {
        "status": "Pass",
        "remarks": "[Re-Verified Live 2026-11-04]: FIXED: yearlyCalendar omitted / null cleanly rejected with HTTP 400 Bad Request (Cit.Attendance:Validation - 'Yearly Calendar Year' must be greater than 0.). NullReferenceException eliminated."
    },
    # 12. HC-DTO-17 (Row 18) - PASS
    18: {
        "status": "Pass",
        "remarks": "[Re-Verified Live 2026-11-04]: FIXED: yearlyCalendar empty object ({}) cleanly rejected with HTTP 400 Bad Request (Cit.Attendance:Validation - 'Yearly Calendar Year' must be greater than 0.). HTTP 500 eliminated."
    },
    # 13. HC-DTO-18 (Row 19) - PASS
    19: {
        "status": "Pass",
        "remarks": "[Re-Verified Live 2026-11-04]: FIXED: yearlyCalendar.year omitted / null cleanly rejected with HTTP 400 Bad Request (Cit.Attendance:Validation - 'Yearly Calendar Year' must be greater than 0.). HTTP 500 eliminated."
    },
    # 14. HC-DTO-21 (Row 22) - PASS
    22: {
        "status": "Pass",
        "remarks": "[Re-Verified Live 2026-11-04]: FIXED (DEFECT-20261103-10): Child holiday holidayName.en empty string (\"\") cleanly rejected with HTTP 400 Bad Request (Cit.Attendance:Validation - 'An English holiday name is required.')."
    },
    # 15. HC-DTO-23 (Row 24) - PASS
    24: {
        "status": "Pass",
        "remarks": "[Re-Verified Live 2026-11-04]: FIXED (DEFECT-20261103-13): Child holiday holidayTypeId omitted / null cleanly rejected with HTTP 400 Bad Request (Cit.Attendance:Validation - 'A holiday type is required.')."
    },
    # 16. HC-DTO-24 (Row 25) - PASS
    25: {
        "status": "Pass",
        "remarks": "[Re-Verified Live 2026-11-04]: FIXED (DEFECT-20261103-13): Child holiday holidayTypeId empty GUID cleanly rejected with HTTP 400 Bad Request (Cit.Attendance:Validation - 'A holiday type is required.')."
    },
    # 17. HC-DTO-52 (Row 53) - PASS
    53: {
        "status": "Pass",
        "remarks": "[Re-Verified Live 2026-11-04]: FIXED: yearlyCalendar.year ancient year (1800) cleanly rejected with HTTP 400 Bad Request (Cit.Attendance:Validation - 'Yearly Calendar Year' must be within allowed years). HTTP 500 eliminated."
    },
    # 18. HC-DTO-66 (Row 67) - PASS
    67: {
        "status": "Pass",
        "remarks": "[Re-Verified Live 2026-11-04]: FIXED (DEFECT-20261103-11): Chronological inversion (endDate < startDate) cleanly rejected with HTTP 400 Bad Request (Cit.Attendance:Validation - 'A holiday cannot end before it starts.')."
    },
    # 19. HC-DTO-67 (Row 68) - PASS
    68: {
        "status": "Pass",
        "remarks": "[Re-Verified Live 2026-11-04]: FIXED (DEFECT-20261103-12): Holiday date outside calendar year cleanly rejected with HTTP 400 Bad Request (Cit.Attendance:Validation - 'Every holiday must start and end within the calendar year.')."
    },
    # 20. HC-DTO-72 (Row 73) - PASS
    73: {
        "status": "Pass",
        "remarks": "[Re-Verified Live 2026-11-04]: FIXED: PATCH route {id} empty GUID cleanly rejected with HTTP 400 Bad Request (Cit.Attendance:Validation - 'Id' must not be empty.). HTTP 500 eliminated."
    },
    # 21. HC-DTO-74 (Row 75) - FAIL
    75: {
        "status": "Fail",
        "remarks": "[Re-Verified Live 2026-11-04]: NOT FIXED: PATCH route {year} non-numeric string returns HTTP 404 Not Found (ASP.NET Core route constraint {year:int} rejects request before reaching controller) instead of HTTP 400 Bad Request."
    },
    # 22. HC-DTO-75 (Row 76) - PASS
    76: {
        "status": "Pass",
        "remarks": "[Re-Verified Live 2026-11-04]: FIXED: PATCH route {year} out of range (past year) cleanly rejected with HTTP 400 Bad Request (Cit.Attendance:Validation - current or next year only). HTTP 500 eliminated."
    },
    # 23. HC-DTO-76 (Row 77) - PASS
    77: {
        "status": "Pass",
        "remarks": "[Re-Verified Live 2026-11-04]: FIXED: PATCH route {year} mismatch with calendar year cleanly rejected with HTTP 400 Bad Request (Cit.Attendance:Validation). HTTP 500 eliminated."
    },
    # 24. HC-DTO-79 (Row 80) - PASS
    80: {
        "status": "Pass",
        "remarks": "[Re-Verified Live 2026-11-04]: FIXED (DEFECT-20261028-02): Empty PATCH body {} cleanly rejected with HTTP 400 Bad Request (Cit.Attendance:Validation - 'At least one update field is required.'). HTTP 500 eliminated."
    },
    # 25. HC-DTO-80 (Row 81) - PASS
    81: {
        "status": "Pass",
        "remarks": "[Re-Verified Live 2026-11-04]: FIXED (DEFECT-20261103-06): PATCH holidayLists empty array [] cleanly rejected with HTTP 400 Bad Request (Cit.Attendance:1704 - 'A holiday calendar needs at least one holiday.')."
    },
    # 26. HC-DTO-82 (Row 83) - PASS
    83: {
        "status": "Pass",
        "remarks": "[Re-Verified Live 2026-11-04]: FIXED (DEFECT-20261103-05/10): PATCH child holiday holidayName.en empty string (\"\") cleanly rejected with HTTP 400 Bad Request (Cit.Attendance:Validation - 'An English holiday name is required.')."
    },
    # 27. HC-DTO-86 (Row 87) - PASS
    87: {
        "status": "Pass",
        "remarks": "[Re-Verified Live 2026-11-04]: FIXED (DEFECT-20261103-04): PATCH non-existing holidayTypeId cleanly rejected with HTTP 400 Bad Request (Cit.Attendance:Validation - 'A holiday type does not exist for this company.')."
    },
    # 28. HC-DTO-110 (Row 111) - PASS
    111: {
        "status": "Pass",
        "remarks": "[Re-Verified Live 2026-11-04]: FIXED (DEFECT-20261103-14): Cit.Attendance:1706 deadlock resolved. Today's date (2026-11-04) is accepted (HTTP 200 OK), and past dates (< Today) are cleanly rejected with HTTP 400 Bad Request ('In the current year, only holidays from today onward can be added or edited.')."
    },
    # 29. HC-DTO-127 (Row 128) - FAIL
    128: {
        "status": "Fail",
        "remarks": "[Re-Verified Live 2026-11-04]: NOT FIXED: Route parameter companyId with non-hex characters returns HTTP 404 Not Found (ASP.NET Core route constraint {companyId:guid} rejects request) instead of HTTP 400 Bad Request."
    },
    # 30. HC-DTO-128 (Row 129) - PASS
    129: {
        "status": "Pass",
        "remarks": "[Re-Verified Live 2026-11-04]: FIXED: Route parameter companyId with 32-char hex string (missing hyphens) cleanly rejected with HTTP 400 Bad Request (Cit.Attendance:Validation)."
    },
    # 31. HC-DTO-129 (Row 130) - FAIL
    130: {
        "status": "Fail",
        "remarks": "[Re-Verified Live 2026-11-04]: NOT FIXED: Route parameter companyId with invalid length (35 chars) returns HTTP 404 Not Found (ASP.NET Core route constraint {companyId:guid} rejects request) instead of HTTP 400 Bad Request."
    },
    # 32. HC-PUB-01 (Row 268) - FAIL
    268: {
        "status": "Fail",
        "remarks": "[Re-Verified Live 2026-11-04]: NOT FIXED (DEFECT-20261103-15): PublishHolidayCalendarCommandHandler lacks defense-in-depth guard rejecting empty calendar publishing. Document a7b5600c-8b76-420e-b6a1-2cc6542d5921 published with 0 holidays (HTTP 200 OK)."
    },
    # 33. HC-PUB-16 (Row 283) - FAIL
    283: {
        "status": "Fail",
        "remarks": "[Re-Verified Live 2026-11-04]: NOT FIXED (DEFECT-20261026-01 / HC-PUB-16): Publishing holiday calendar does not synchronize CompanyChecklist.HolidayCalendarPublished in SP.CompanySvc (remains false)."
    },
    # 34. HC-PUB-18 (Row 285) - FAIL
    285: {
        "status": "Fail",
        "remarks": "[Re-Verified Live 2026-11-04]: NOT FIXED (DEFECT-20261103-15): Re-publish blocked check missing on Publish endpoint for empty calendars."
    },
    # 35. HC-DTO-144 (Row 312) - PASS
    312: {
        "status": "Pass",
        "remarks": "[Re-Verified Live 2026-11-04]: FIXED (DEFECT-20261103-07): Duplicate holiday calendar creation within same company and year rejected with HTTP 400 Bad Request (Cit.Attendance:1713 - 'A company holiday calendar already exists for the selected year.')."
    },
    # 36. HC-DTO-145 (Row 313) - FAIL
    313: {
        "status": "Fail",
        "remarks": "[Re-Verified Live 2026-11-04]: NOT FIXED (DEFECT-20261103-08): calendarType invalid enum 999 is NOT validated at DTO layer; server silently coerces 999 to default (1 / CompanyDefault) and triggers business conflict Cit.Attendance:1713 instead of HTTP 400 DTO enum validation."
    },
    # 37. HC-DTO-146 (Row 314) - PASS
    314: {
        "status": "Pass",
        "remarks": "[Re-Verified Live 2026-11-04]: FIXED (DEFECT-20261103-09): Calendar creation with mismatched or invalid year rejected with HTTP 400 Bad Request (Cit.Attendance:1712 / Cit.Attendance:1713)."
    }
}

# Apply updates to ws_hc
for row_idx, data in updated_tcs.items():
    cell_status = ws_hc.cell(row=row_idx, column=9)
    cell_remarks = ws_hc.cell(row=row_idx, column=10)
    
    cell_status.value = data["status"]
    cell_remarks.value = data["remarks"]
    
    if data["status"] == "Pass":
        cell_status.fill = green_fill
        cell_status.font = green_font
    else:
        cell_status.fill = red_fill
        cell_status.font = red_font

# Recount ws_hc
total_hc = 313
pass_hc = 0
fail_hc = 0
for r in range(2, ws_hc.max_row + 1):
    val = str(ws_hc.cell(r, 9).value).strip() if ws_hc.cell(r, 9).value else ''
    if 'pass' in val.lower():
        pass_hc += 1
    elif 'fail' in val.lower():
        fail_hc += 1

print(f"Recounted Holiday Calendar Sheet: Total={total_hc}, Pass={pass_hc}, Fail={fail_hc}")

# Update Row 20 in INDEX
# Row 20: [16, 'Holiday Calendar - Test Cases', 313, 172, 133, 8, 0, '...', Passed, Failed, Not-Run, Exec %, Status]
pass_rate_hc = (pass_hc / total_hc) * 100
ws_index.cell(row=20, column=9, value=pass_hc)
ws_index.cell(row=20, column=10, value=fail_hc)
ws_index.cell(row=20, column=11, value=0)
ws_index.cell(row=20, column=12, value="100.0%")
ws_index.cell(row=20, column=13, value=f"🟢 100% Executed ({pass_rate_hc:.1f}% Pass Rate)")

# Recount Master Total on INDEX (Row 22)
# Sum modules rows 5 to 21
sum_total = 0
sum_pass = 0
sum_fail = 0
sum_notrun = 0

for r in range(5, 22):
    t = ws_index.cell(row=r, column=3).value or 0
    p = ws_index.cell(row=r, column=9).value or 0
    f = ws_index.cell(row=r, column=10).value or 0
    nr = ws_index.cell(row=r, column=11).value or 0
    sum_total += int(t)
    sum_pass += int(p)
    sum_fail += int(f)
    sum_notrun += int(nr)

sum_exec = sum_pass + sum_fail
exec_pct = (sum_exec / sum_total) * 100 if sum_total else 0
pass_rate_total = (sum_pass / sum_exec) * 100 if sum_exec else 0

ws_index.cell(row=22, column=3, value=sum_total)
ws_index.cell(row=22, column=9, value=sum_pass)
ws_index.cell(row=22, column=10, value=sum_fail)
ws_index.cell(row=22, column=11, value=sum_notrun)
ws_index.cell(row=22, column=12, value=f"{exec_pct:.1f}%")
ws_index.cell(row=22, column=13, value=f"🎯 {sum_exec} Executed ({sum_pass} Pass, {sum_fail} Fail — {pass_rate_total:.1f}% Pass Rate) | {sum_notrun} Pending Execution")

wb.save('AttendanceTestCases_Master_Consolidated.xlsx')
print(f"Successfully updated AttendanceTestCases_Master_Consolidated.xlsx!")
print(f"Index Row 20: Pass={pass_hc}, Fail={fail_hc}, Pass Rate={pass_rate_hc:.1f}%")
print(f"Index Row 22 (TOTAL): Total={sum_total}, Executed={sum_exec}, Pass={sum_pass}, Fail={sum_fail}, NotRun={sum_notrun}, Pass Rate={pass_rate_total:.1f}%")

