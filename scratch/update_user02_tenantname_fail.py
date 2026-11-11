import openpyxl
import sys

sys.stdout.reconfigure(encoding='utf-8')

wb = openpyxl.load_workbook("AttendanceTestCases_Master_Consolidated.xlsx")
ws_us = wb["User Scenarios (Add Here)"]

# Row 3: USER-02
ws_us.cell(3, 9).value = "Failed (Defect)"
ws_us.cell(3, 10).value = (
    "[Found 26-Oct, Re-confirmed 28-Oct via MongoDB Compass]: DEFECT PERSISTS (FAIL). "
    "Developer removed 'Placeholder Tenant', but TenantName now persists as Object (empty) '{}'. "
    "Requirement: TenantName must be automatically pre-populated/resolved from Identity/JWT context on the backend; "
    "it must NEVER be expected from client/user payload."
)

# Row 130: USER-129
ws_us.cell(130, 9).value = "Fail"
ws_us.cell(130, 10).value = (
    "[Re-verified 28-Oct-2026 on Attendance 3 & Confirmed via MongoDB Compass]: FAIL. "
    "Document 99a56911-0d30-40e6-8fa4-ca64da88930c persists 'TenantName: Object (empty)'. "
    "TenantName is a mandatory system field that must be dynamically pre-populated by backend handler from current tenant context, "
    "not user-sent."
)

wb.save("AttendanceTestCases_Master_Consolidated.xlsx")
print("Successfully updated USER-02 and USER-129 in Excel with MongoDB Compass confirmation!")

