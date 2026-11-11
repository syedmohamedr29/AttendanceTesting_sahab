import openpyxl
import sys

sys.stdout.reconfigure(encoding='utf-8')

wb = openpyxl.load_workbook("AttendanceTestCases_Master_Consolidated.xlsx")
ws_us = wb["User Scenarios (Add Here)"]

# Row 5: USER-04
ws_us.cell(5, 9).value = "Failed (Defect)"
ws_us.cell(5, 10).value = (
    "[Full Microservice Audit 28-Oct]: CRITICAL DEFECT PERSISTS (FAIL). "
    "Scanned entire Attendance 2 Swagger: EXACTLY 26 POST & PATCH APIs still expose 'tenantName' in their request body DTOs "
    "(WorkTemplates 10, WorkPlans 3, WorkAssignments 3, Roster 3, Policies 6, Holiday 1). "
    "Verified via Swagger UI screenshot and live schema audit. "
    "Requirement: TenantName must be pre-populated by default by backend from JWT context; "
    "it must be completely purged from all 26 request body DTOs and never sent by user."
)

# Row 132: USER-131
ws_us.cell(132, 9).value = "Fail"
ws_us.cell(132, 10).value = (
    "[Re-verification on Attendance 3 & Full API Scan]: FAIL. "
    "Swagger UI still displays 'tenantName' in request body contracts across 26 POST/PATCH endpoints. "
    "Client spoofing verified with HTTP 200 OK. Complete purge required across all 26 command DTOs."
)

wb.save("AttendanceTestCases_Master_Consolidated.xlsx")
print("Updated USER-04 and USER-131 in Excel successfully!")

