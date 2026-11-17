import openpyxl

wb = openpyxl.load_workbook('AttendanceTestCases_Master_Consolidated.xlsx')
ws = wb['INDEX']

# Row 6 is WT - Location Shifts
# Col A: # (2)
# Col B: Module / Sheet ('WT - Location Shifts')
# Col C: Total TCs (103 -> 112)
# Col D: P0 (47 -> 51)
# Col E: P1 (38 -> 43)
# Col F: P2 (18)
# Col G: P3 (0)
# Col H: Testing Scope / Notes
print("Old Row 6:", [ws.cell(6, c).value for c in range(1, 9)])
ws.cell(6, 3).value = 112
ws.cell(6, 4).value = 51
ws.cell(6, 5).value = 43
ws.cell(6, 8).value = "100% Executed on 16-Nov-2026: 112 TCs (94 Passed, 1 By Design, 17 Failed — 6 Defects DEFECT-20261116-01 to 06 Logged)"
print("New Row 6:", [ws.cell(6, c).value for c in range(1, 9)])

# Update Total row (Row 24)
# Row 24 Total TCs: 2111 + 9 = 2120
ws.cell(24, 3).value = 2120
ws.cell(24, 4).value = 894
ws.cell(24, 5).value = 986

wb.save('AttendanceTestCases_Master_Consolidated.xlsx')
print("Successfully updated INDEX sheet in AttendanceTestCases_Master_Consolidated.xlsx")
