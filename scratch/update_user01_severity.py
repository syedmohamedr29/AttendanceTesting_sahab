import openpyxl
from openpyxl.styles import PatternFill, Font, Alignment
import sys

sys.stdout.reconfigure(encoding='utf-8')

wb = openpyxl.load_workbook("AttendanceTestCases_Master_Consolidated.xlsx")
ws_us = wb["User Scenarios (Add Here)"]

# Row 2: USER-01
ws_us.cell(2, 6).value = "P2"
old_rem_1 = str(ws_us.cell(2, 10).value or "")
ws_us.cell(2, 10).value = old_rem_1 + " | [Update 28-Oct]: De-escalated from Blocker to P2 per QA review; pending confirmation with Naushad on whether checklist step is non-blocking."

# Row 129: USER-128
ws_us.cell(129, 6).value = "P2"
old_rem_128 = str(ws_us.cell(129, 10).value or "")
ws_us.cell(129, 10).value = old_rem_128 + " | [Update 28-Oct]: Non-Blocker (P2); pending confirmation with Naushad."

# Recount P0, P1, P2, P3 in User Scenarios
p0 = p1 = p2 = p3 = 0
for r in range(2, ws_us.max_row + 1):
    pri = str(ws_us.cell(r, 6).value or "").strip().upper()
    if pri == "P0":
        p0 += 1
    elif pri == "P1":
        p1 += 1
    elif pri == "P2":
        p2 += 1
    elif pri == "P3":
        p3 += 1

print(f"User Scenarios Priorities: P0={p0}, P1={p1}, P2={p2}, P3={p3}")

# Update INDEX tab Row 19 (User Scenarios)
ws_idx = wb["INDEX"]
ws_idx.cell(19, 4).value = p0
ws_idx.cell(19, 5).value = p1
ws_idx.cell(19, 6).value = p2
ws_idx.cell(19, 7).value = p3

# Recalculate Row 21 (TOTAL) P0, P1, P2, P3
tot_p0 = sum(int(ws_idx.cell(r, 4).value or 0) for r in range(5, 21))
tot_p1 = sum(int(ws_idx.cell(r, 5).value or 0) for r in range(5, 21))
tot_p2 = sum(int(ws_idx.cell(r, 6).value or 0) for r in range(5, 21))
tot_p3 = sum(int(ws_idx.cell(r, 7).value or 0) for r in range(5, 21))

ws_idx.cell(21, 4).value = tot_p0
ws_idx.cell(21, 5).value = tot_p1
ws_idx.cell(21, 6).value = tot_p2
ws_idx.cell(21, 7).value = tot_p3

print(f"INDEX TOTAL Priorities: P0={tot_p0}, P1={tot_p1}, P2={tot_p2}, P3={tot_p3}")

wb.save("AttendanceTestCases_Master_Consolidated.xlsx")
print("Successfully updated Excel: USER-01 and USER-128 changed to P2, INDEX priorities refreshed!")

