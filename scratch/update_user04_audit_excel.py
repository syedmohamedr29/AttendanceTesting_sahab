import openpyxl
from openpyxl.styles import PatternFill, Font, Alignment
import sys

sys.stdout.reconfigure(encoding='utf-8')

wb = openpyxl.load_workbook("AttendanceTestCases_Master_Consolidated.xlsx")
ws_us = wb["User Scenarios (Add Here)"]

fail_fill = PatternFill(start_color="FEE2E2", end_color="FEE2E2", fill_type="solid")
bold_font = Font(name="Calibri", size=10, bold=True)

# Row 5: USER-04
ws_us.cell(5, 9).value = "Failed (Defect)"
ws_us.cell(5, 9).fill = fail_fill
ws_us.cell(5, 10).value = (
    "[Re-audited 28-Oct across all POST & PATCH]: DEFECT PERSISTS (FAIL). "
    "Developer removed tenantId, companyId, locationId, BUT tenantName remains declared in ALL 6 POST and PATCH DTOs! "
    "Live test proved client can send spoofed tenantName in body (HTTP 200 accepted!), or if omitted, Mongo persists TenantName: {} empty. "
    "TenantName must be completely removed from body DTOs and pre-populated by backend from JWT context."
)

# Row 132: USER-131
ws_us.cell(132, 9).value = "Fail"
ws_us.cell(132, 9).fill = fail_fill
ws_us.cell(132, 10).value = (
    "[Full POST/PATCH Audit 28-Oct]: FAIL. "
    "While backend accepts clean payload omitting tenantId/companyId, tenantName is still exposed in FixedWorkTemplateDto, "
    "FlexiWorkTemplateDto, SplitWorkTemplateDto, and all 3 Update*Dto models. "
    "PATCH /fixed accepted client-spoofed tenantName with HTTP 200 OK. "
    "Immutable shortCode also remains in Update DTOs."
)

# Recalculate Pass / Fail for User Scenarios
passed = 0
failed = 0
not_run = 0
for r in range(2, ws_us.max_row + 1):
    st = str(ws_us.cell(r, 9).value or "").strip().lower()
    if st == "pass":
        passed += 1
    elif "fail" in st:
        failed += 1
    else:
        not_run += 1

print(f"User Scenarios: Passed={passed}, Failed={failed}, Not-Run={not_run}")

# Update INDEX tab
ws_idx = wb["INDEX"]
ws_idx.cell(19, 9).value = passed
ws_idx.cell(19, 10).value = failed
ws_idx.cell(19, 11).value = not_run
exec_pct = f"{(passed + failed) / (passed + failed + not_run) * 100:.1f}%"
ws_idx.cell(19, 12).value = exec_pct
ws_idx.cell(19, 13).value = f"In Progress ({passed + failed}/{passed + failed + not_run} run)"

# Recalculate TOTAL row
tot_pass = sum(int(ws_idx.cell(r, 9).value or 0) for r in range(5, 21))
tot_fail = sum(int(ws_idx.cell(r, 10).value or 0) for r in range(5, 21))
tot_not_run = sum(int(ws_idx.cell(r, 11).value or 0) for r in range(5, 21))
tot_tcs = sum(int(ws_idx.cell(r, 3).value or 0) for r in range(5, 21))

ws_idx.cell(21, 9).value = tot_pass
ws_idx.cell(21, 10).value = tot_fail
ws_idx.cell(21, 11).value = tot_not_run
tot_pct = f"{(tot_pass + tot_fail) / tot_tcs * 100:.1f}%"
ws_idx.cell(21, 12).value = tot_pct
ws_idx.cell(21, 13).value = f"{tot_pass + tot_fail} Executed ({tot_pass} Pass, {tot_fail} Fail, {tot_not_run} Not-Run)"

print(f"INDEX TOTAL: Pass={tot_pass}, Fail={tot_fail}, Not-Run={tot_not_run}, Total TCs={tot_tcs}")

wb.save("AttendanceTestCases_Master_Consolidated.xlsx")
print("Saved AttendanceTestCases_Master_Consolidated.xlsx successfully!")

