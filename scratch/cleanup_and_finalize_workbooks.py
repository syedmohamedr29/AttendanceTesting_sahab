import sys
import openpyxl

sys.stdout.reconfigure(encoding='utf-8')

# 1. Fix add_policies_dto_validations_sheet.py
script_path = 'scratch/add_policies_dto_validations_sheet.py'
with open(script_path, 'r', encoding='utf-8') as f:
    text = f.read()

target = "dto_cases = get_dto_test_cases()"
if target in text and 'if __name__ == "__main__":' not in text:
    text = text.replace(target, 'if __name__ == "__main__":\n    dto_cases = get_dto_test_cases()')
    with open(script_path, 'w', encoding='utf-8') as f:
        f.write(text)
    print("Guarded add_policies_dto_validations_sheet.py with if __name__ == '__main__':")

# 2. Clean Master Consolidated Workbook
wb_path = "AttendanceTestCases_Master_Consolidated.xlsx"
wb = openpyxl.load_workbook(wb_path)

if "Policies - Manual DTO Validations" in wb.sheetnames:
    del wb["Policies - Manual DTO Validations"]
    print("Deleted overlong sheet 'Policies - Manual DTO Validations'.")

# Check INDEX sheet
idx_ws = wb["INDEX"]

# Remove duplicate row in INDEX
for r in range(idx_ws.max_row, 4, -1):
    val = str(idx_ws.cell(r, 2).value or "").strip().lower()
    if "policies - manual dto validations" in val:
        idx_ws.delete_rows(r)
        print(f"Deleted duplicate row {r} from INDEX.")

# Recalculate and format rows
for r in range(5, idx_ws.max_row + 1):
    val = str(idx_ws.cell(r, 2).value or "").strip().lower()
    if val == "attendance policies":
        idx_ws.cell(r, 1, 6)
        idx_ws.cell(r, 3, 219)
        idx_ws.cell(r, 4, 55)
        idx_ws.cell(r, 5, 145)
        idx_ws.cell(r, 6, 19)
        idx_ws.cell(r, 7, 0)
    elif "policies - dto validations" in val:
        idx_ws.cell(r, 1, 18)
        idx_ws.cell(r, 2, "Policies - DTO Validations")
        idx_ws.cell(r, 3, 75)
        idx_ws.cell(r, 4, 23)
        idx_ws.cell(r, 5, 43)
        idx_ws.cell(r, 6, 9)
        idx_ws.cell(r, 7, 0)

# Recalculate TOTAL row
total_row = None
for r in range(5, idx_ws.max_row + 1):
    val = str(idx_ws.cell(r, 1).value or "").strip().upper()
    if "TOTAL" in val:
        total_row = r
        break

if total_row:
    num_modules = total_row - 5
    tot_tcs = sum(idx_ws.cell(r, 3).value or 0 for r in range(5, total_row))
    tot_p0 = sum(idx_ws.cell(r, 4).value or 0 for r in range(5, total_row))
    tot_p1 = sum(idx_ws.cell(r, 5).value or 0 for r in range(5, total_row))
    tot_p2 = sum(idx_ws.cell(r, 6).value or 0 for r in range(5, total_row))
    tot_p3 = sum(idx_ws.cell(r, 7).value or 0 for r in range(5, total_row))
    
    idx_ws.cell(total_row, 2, f"All {num_modules} Modules Combined")
    idx_ws.cell(total_row, 3, tot_tcs)
    idx_ws.cell(total_row, 4, tot_p0)
    idx_ws.cell(total_row, 5, tot_p1)
    idx_ws.cell(total_row, 6, tot_p2)
    idx_ws.cell(total_row, 7, tot_p3)
    print(f"INDEX Row {total_row} (TOTAL): Modules={num_modules}, Total={tot_tcs}, P0={tot_p0}, P1={tot_p1}, P2={tot_p2}, P3={tot_p3}")

wb.save(wb_path)
print(f"Successfully cleaned and saved {wb_path}!")

