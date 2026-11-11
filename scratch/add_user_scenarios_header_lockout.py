import sys
import openpyxl
from openpyxl.styles import Font, Alignment, Border, Side, PatternFill

sys.stdout.reconfigure(encoding='utf-8')

wb = openpyxl.load_workbook('AttendanceTestCases_Master_Consolidated.xlsx')
ws = wb['User Scenarios (Add Here)']

new_test_cases = [
    {
        "TC ID": "USER-51",
        "Section": "First-Time CDWT Creation - Header Location Lockout (Fixed)",
        "Test Scenario": "Reject first-time Company Default Fixed Work Template creation when LocationId is passed in HTTP request headers",
        "Input / Preconditions": "Company has active locations in Company Service, but 0 default templates in Attendance DB. Request: POST /api/companies/{companyId}/worktemplates/fixed. Headers: Authorization: Bearer, X-Location-Id: {valid-location-uuid} (or locationId header). Body: Valid Fixed template payload.",
        "Expected Result": "HTTP 400 Bad Request. System rejects creation with Cit.Attendance:1205 ('Company default is not available.') or Validation Error. Default template MUST NOT contain location scoping in headers. LocationId must be 00000000-0000-0000-0000-000000000000.",
        "Pri": "P0",
        "Type": "security/integrity",
        "Env": "dev",
        "Status": "Not-Run",
        "QA Remarks": "[First-Time Header Lockout - Fixed] Prevents unintended location scoping or 1205 deadlock when location header is present during CDWT setup.",
        "Source Origin": "User Execution Clarification (27-Oct-2026)"
    },
    {
        "TC ID": "USER-52",
        "Section": "First-Time CDWT Creation - Header Location Lockout (Flexible)",
        "Test Scenario": "Reject first-time Company Default Flexible Work Template creation when LocationId is passed in HTTP request headers",
        "Input / Preconditions": "Company has active locations in Company Service, but 0 default templates in Attendance DB. Request: POST /api/companies/{companyId}/worktemplates/flexi. Headers: Authorization: Bearer, X-Location-Id: {valid-location-uuid}. Body: Valid Flexi template payload (Daily or Weekly).",
        "Expected Result": "HTTP 400 Bad Request. System rejects creation with Cit.Attendance:1205 ('Company default is not available.') or Validation Error. Flexible default template cannot be created when location is injected via header.",
        "Pri": "P0",
        "Type": "security/integrity",
        "Env": "dev",
        "Status": "Not-Run",
        "QA Remarks": "[First-Time Header Lockout - Flexi] Validates mutual exclusion between CDWT creation and location header injection for Flexible mode.",
        "Source Origin": "User Execution Clarification (27-Oct-2026)"
    },
    {
        "TC ID": "USER-53",
        "Section": "First-Time CDWT Creation - Header Location Lockout (Split Shift)",
        "Test Scenario": "Reject first-time Company Default Split Shift Work Template creation when LocationId is passed in HTTP request headers",
        "Input / Preconditions": "Company has active locations in Company Service, but 0 default templates in Attendance DB. Request: POST /api/companies/{companyId}/worktemplates/split. Headers: Authorization: Bearer, X-Location-Id: {valid-location-uuid}. Body: Valid Split shift payload with two time slots.",
        "Expected Result": "HTTP 400 Bad Request. System rejects creation with Cit.Attendance:1205 ('Company default is not available.') or Validation Error. Split default template cannot be created when location is injected via header.",
        "Pri": "P0",
        "Type": "security/integrity",
        "Env": "dev",
        "Status": "Not-Run",
        "QA Remarks": "[First-Time Header Lockout - Split] Ensures Split shift CDWT setup follows identical company-level scoping rules.",
        "Source Origin": "User Execution Clarification (27-Oct-2026)"
    },
    {
        "TC ID": "USER-54",
        "Section": "First-Time CDWT Creation - Clean Header Success Baseline",
        "Test Scenario": "Verify successful first-time CDWT creation across Fixed, Flexi, or Split when LocationId is strictly omitted from headers and URL",
        "Input / Preconditions": "Company has active locations in Company Service, but 0 default templates. Request: POST /api/companies/{companyId}/worktemplates/{fixed|flexi|split}. Headers: Only CompanyId and Bearer token (NO location header). URL: Clean route without ?locationId=.",
        "Expected Result": "HTTP 201 Created. CDWT successfully created with LocationId: 00000000-0000-0000-0000-000000000000, IsDefault: true, Version: '1.0'. Automatically triggers location default cascade and work plans across all existing active locations.",
        "Pri": "P1",
        "Type": "functional",
        "Env": "dev",
        "Status": "Not-Run",
        "QA Remarks": "[Clean Setup Baseline] Confirms positive path when client properly isolates company-level context from location context.",
        "Source Origin": "Standard Operating Procedure & Verification Matrix"
    }
]

headers = [ws.cell(1, col).value for col in range(1, ws.max_column+1)]
start_row = ws.max_row + 1

thin_border = Border(
    left=Side(style='thin', color='00D9D9D9'),
    right=Side(style='thin', color='00D9D9D9'),
    top=Side(style='thin', color='00D9D9D9'),
    bottom=Side(style='thin', color='00D9D9D9')
)

font_regular = Font(name='Segoe UI', size=10, bold=False)
font_bold = Font(name='Segoe UI', size=10, bold=True)

for i, tc in enumerate(new_test_cases):
    row_idx = start_row + i
    for col_idx, header in enumerate(headers, start=1):
        cell = ws.cell(row=row_idx, column=col_idx)
        val = tc.get(header, "")
        cell.value = val
        cell.border = thin_border
        
        if header in ['TC ID', 'Pri', 'Type', 'Env', 'Status']:
            cell.alignment = Alignment(horizontal='center', vertical='top')
            cell.font = font_bold if header in ['TC ID', 'Pri'] else font_regular
        else:
            cell.alignment = Alignment(horizontal='left', vertical='top', wrap_text=True)
            cell.font = font_bold if header == 'Section' else font_regular

print(f"Added {len(new_test_cases)} test cases from row {start_row} to {start_row + len(new_test_cases) - 1}")

# Update INDEX sheet
ws_index = wb['INDEX']
# Row 19: User Scenarios (Add Here)
# Previous: Total 50, P0: 3, P1: 35, P2: 12, P3: 0
# Added: 4, P0: 3, P1: 1, P2: 0, P3: 0
# New: Total 54, P0: 6, P1: 36, P2: 12, P3: 0
ws_index.cell(19, 3).value = 54
ws_index.cell(19, 4).value = 6
ws_index.cell(19, 5).value = 36
ws_index.cell(19, 6).value = 12
ws_index.cell(19, 7).value = 0

# Row 20: TOTAL
# Previous: 1129, P0: 459, P1: 472, P2: 185, P3: 13
# New: 1133, P0: 462, P1: 473, P2: 185, P3: 13
ws_index.cell(20, 3).value = 1133
ws_index.cell(20, 4).value = 462
ws_index.cell(20, 5).value = 473
ws_index.cell(20, 6).value = 185
ws_index.cell(20, 7).value = 13

wb.save('AttendanceTestCases_Master_Consolidated.xlsx')
print("Successfully saved AttendanceTestCases_Master_Consolidated.xlsx with 1,133 test cases!")

