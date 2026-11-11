import openpyxl
import sys

sys.stdout.reconfigure(encoding='utf-8')

wb = openpyxl.load_workbook('AttendanceTestCases_Master_Consolidated.xlsx', data_only=True)
print("Sheet Names:", len(wb.sheetnames))
for i, name in enumerate(wb.sheetnames, 1):
    ws = wb[name]
    print(f"{i:2d}. {name:<35} | Max Row: {ws.max_row}")

print("\n--- INDEX SUMMARY ---")
idx = wb['INDEX']
for r in range(4, idx.max_row + 1):
    vals = [idx.cell(r, c).value for c in range(1, 9)]
    if any(vals):
        print(f"Row {r:2d}: {str(vals[0]):<4} | {str(vals[1]):<35} | Total: {str(vals[2]):<5} | P0: {str(vals[3]):<4} | P1: {str(vals[4]):<4} | P2: {str(vals[5]):<4} | P3: {str(vals[6]):<4}")

hc_ws = wb['Holiday Calendar - Test Cases']
print(f"\nHoliday Calendar - Test Cases total test cases: {hc_ws.max_row - 1}")
print("First 3 test cases:")
for r in range(2, 5):
    print(f"  {hc_ws.cell(r, 1).value} | {hc_ws.cell(r, 2).value} | {hc_ws.cell(r, 3).value}")
print("Last 3 test cases:")
for r in range(hc_ws.max_row - 2, hc_ws.max_row + 1):
    print(f"  {hc_ws.cell(r, 1).value} | {hc_ws.cell(r, 2).value} | {hc_ws.cell(r, 3).value}")

