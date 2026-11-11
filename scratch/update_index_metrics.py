import openpyxl

wb = openpyxl.load_workbook("AttendanceTestCases_Master_Consolidated.xlsx")
ws = wb["INDEX"]

# Row 10: Attendance Policies
ws.cell(10, 9, 207)   # Passed
ws.cell(10, 10, 12)   # Failed
ws.cell(10, 11, 0)    # Not-Run
ws.cell(10, 12, "100.0%")
ws.cell(10, 13, "🟢 100% Executed (207 Pass, 12 Fail / Defects Logged)")

# Row 22: Policies - DTO Validations
ws.cell(22, 9, 68)    # Passed
ws.cell(22, 10, 10)   # Failed
ws.cell(22, 11, 0)    # Not-Run
ws.cell(22, 12, "100.0%")
ws.cell(22, 13, "🟢 100% Executed (68 Pass, 10 Fail / Defects Logged)")

# Row 23: TOTAL - recalculate sum of rows 5 to 22
total_tcs = sum(ws.cell(r, 3).value or 0 for r in range(5, 23))
total_p0 = sum(ws.cell(r, 4).value or 0 for r in range(5, 23))
total_p1 = sum(ws.cell(r, 5).value or 0 for r in range(5, 23))
total_p2 = sum(ws.cell(r, 6).value or 0 for r in range(5, 23))
total_p3 = sum(ws.cell(r, 7).value or 0 for r in range(5, 23))
total_passed = sum(ws.cell(r, 9).value or 0 for r in range(5, 23))
total_failed = sum(ws.cell(r, 10).value or 0 for r in range(5, 23))
total_notrun = sum(ws.cell(r, 11).value or 0 for r in range(5, 23))

ws.cell(23, 3, total_tcs)
ws.cell(23, 4, total_p0)
ws.cell(23, 5, total_p1)
ws.cell(23, 6, total_p2)
ws.cell(23, 7, total_p3)
ws.cell(23, 9, total_passed)
ws.cell(23, 10, total_failed)
ws.cell(23, 11, total_notrun)
exec_pct = round((total_passed + total_failed) / total_tcs * 100, 1)
ws.cell(23, 12, f"{exec_pct}%")
ws.cell(23, 13, f"🎯 {total_passed + total_failed} Executed ({total_passed} Pass, {total_failed} Fail) | {total_notrun} Pending Execution")

wb.save("AttendanceTestCases_Master_Consolidated.xlsx")
print(f"INDEX Updated! Total TCs={total_tcs}, Passed={total_passed}, Failed={total_failed}, NotRun={total_notrun}")
