import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter
import sys

sys.stdout.reconfigure(encoding='utf-8')

wb = openpyxl.load_workbook('AttendanceTestCases_Master_Consolidated.xlsx')

sheet_name = 'Holiday Calendar - Test Cases'
ws = wb[sheet_name]

# Define the 15 granular holiday removal test cases
rem_test_cases = [
    {
        "id": "HC-REM-01",
        "section": "8. Holiday Removal - Past, Today, Future & DB Fields Update Verification",
        "scenario": "Remove Future Single-Day Holiday (startDate > Today) - Verify exact DB fields updated",
        "input": "PATCH /api/companies/{companyId}/holidaylist/{id}/remove/{futureHolidayId}/{year} where holiday startDate > Today",
        "expected": "1. HTTP 200 OK ('Holiday removed successfully').\n2. DB Verification (ERP.Attendance.HolidayCalendars):\n   - YearlyCalendar.HolidayLists: target holiday completely removed; array count decreases (N -> N-1).\n   - IsPublished: updated to false (staged edit pending publish).\n   - LastPublishedOn: remains UNCHANGED (keeps previous publish timestamp).\n   - YearlyCalendar.Year: remains unchanged.\n3. Inherited Location Calendars: still retain the holiday in DB until explicit publish.",
        "pri": "P0",
        "type": "smoke"
    },
    {
        "id": "HC-REM-02",
        "section": "8. Holiday Removal - Past, Today, Future & DB Fields Update Verification",
        "scenario": "Remove Future Multi-Day Holiday (startDate > Today) - Verify duration and DB array",
        "input": "PATCH /holidaylist/{id}/remove/{multiDayHolidayId}/{year} (e.g. 5-day Eid vacation in future)",
        "expected": "1. HTTP 200 OK.\n2. DB Verification: Entire multi-day holiday document pulled from YearlyCalendar.HolidayLists array; IsPublished updated to false; other holidays in array unaffected.",
        "pri": "P0",
        "type": "smoke"
    },
    {
        "id": "HC-REM-03",
        "section": "8. Holiday Removal - Past, Today, Future & DB Fields Update Verification",
        "scenario": "Remove Today Holiday (startDate == Today) - Allowed per business specification",
        "input": "PATCH /holidaylist/{id}/remove/{todayHolidayId}/{currentYear} where holiday startDate == Today",
        "expected": "1. HTTP 200 OK ('Holiday removed successfully'). Allowed because holiday has not elapsed.\n2. DB Verification: Target holiday removed from HolidayLists array; IsPublished set to false.",
        "pri": "P0",
        "type": "smoke"
    },
    {
        "id": "HC-REM-04",
        "section": "8. Holiday Removal - Past, Today, Future & DB Fields Update Verification",
        "scenario": "Negative: Remove Past Single-Day Holiday in Current Year (startDate < Today)",
        "input": "PATCH /holidaylist/{id}/remove/{pastHolidayId}/{currentYear} where holiday startDate < Today (e.g. D-5)",
        "expected": "1. HTTP 400 Bad Request, Cit.Attendance:1709 ('Past holidays cannot be removed. Only today or future holidays are allowed.').\n2. DB Verification: Document NOT modified. YearlyCalendar.HolidayLists remains completely intact; IsPublished remains unchanged.",
        "pri": "P0",
        "type": "negative"
    },
    {
        "id": "HC-REM-05",
        "section": "8. Holiday Removal - Past, Today, Future & DB Fields Update Verification",
        "scenario": "Negative: Remove Ongoing Multi-Day Holiday (startDate < Today, endDate >= Today)",
        "input": "PATCH /holidaylist/{id}/remove/{ongoingHolidayId}/{currentYear} where holiday started yesterday (D-1) and ends tomorrow (D+1)",
        "expected": "1. HTTP 400 Bad Request, Cit.Attendance:1709 ('Past holidays cannot be removed. Only today or future holidays are allowed.').\n2. DB Verification: System checks StartDate; ongoing holiday cannot be removed. DB document remains unchanged.",
        "pri": "P0",
        "type": "negative"
    },
    {
        "id": "HC-REM-06",
        "section": "8. Holiday Removal - Past, Today, Future & DB Fields Update Verification",
        "scenario": "Negative: Remove Holiday in Past Year Calendar (Year Y-1)",
        "input": "PATCH /api/companies/{companyId}/holidaylist/{pastYearCalId}/remove/{holidayId}/{pastYear}",
        "expected": "HTTP 400 Bad Request, Cit.Attendance:1704 / 1709 ('Holidays can only be updated for current or next year.'). DB unchanged.",
        "pri": "P1",
        "type": "negative"
    },
    {
        "id": "HC-REM-07",
        "section": "8. Holiday Removal - Past, Today, Future & DB Fields Update Verification",
        "scenario": "Remove Last Remaining Holiday in Calendar (Emptying calendar to 0 holidays)",
        "input": "Calendar has exactly 1 future holiday. Call PATCH /remove/{holidayId}/{year}",
        "expected": "1. HTTP 200 OK ('Holiday removed successfully').\n2. DB Verification: YearlyCalendar.HolidayLists becomes an empty array []; IsPublished set to false; calendar document persists as an active empty shell (IsActive=true, IsDeleted=false).",
        "pri": "P1",
        "type": "boundary"
    },
    {
        "id": "HC-REM-08",
        "section": "8. Holiday Removal - Past, Today, Future & DB Fields Update Verification",
        "scenario": "Negative: Remove Holiday on Inherited Location Calendar (IsInherited == true)",
        "input": "PATCH /holidaylist/{locCalId}/remove/{holidayId}/{year}?locationId={locId} on inherited location calendar",
        "expected": "1. HTTP 400 Bad Request, Cit.Attendance:1714 ('This location follows the company holidays. Customise it before editing.').\n2. DB Verification: Inherited location calendar document is NOT modified.",
        "pri": "P0",
        "type": "negative"
    },
    {
        "id": "HC-REM-09",
        "section": "8. Holiday Removal - Past, Today, Future & DB Fields Update Verification",
        "scenario": "Remove Holiday on Customised Location Calendar (IsInherited == false)",
        "input": "PATCH /holidaylist/{customisedLocId}/remove/{holidayId}/{year}?locationId={locId} on detached calendar",
        "expected": "1. HTTP 200 OK ('Holiday removed successfully').\n2. DB Verification: Holiday removed from location calendar document immediately. Company Default calendar is NOT modified (complete scoping isolation).",
        "pri": "P0",
        "type": "smoke"
    },
    {
        "id": "HC-REM-10",
        "section": "8. Holiday Removal - Past, Today, Future & DB Fields Update Verification",
        "scenario": "Publish after removal: Overwrites inherited location calendars with updated list",
        "input": "Following HC-REM-01 removal, call POST /api/companies/{companyId}/holidaylist/publish/{year}",
        "expected": "1. HTTP 200 OK ('Holidays published successfully').\n2. DB Verification (Company Default): IsPublished updated to true; LastPublishedOn updated to current UTC datetime.\n3. DB Verification (Inherited Locations): HolidayLists array overwritten to match company list (target holiday removed across all locations).\n4. DB Verification (Customised Locations): Preserved untouched.",
        "pri": "P0",
        "type": "smoke"
    },
    {
        "id": "HC-REM-11",
        "section": "8. Holiday Removal - Past, Today, Future & DB Fields Update Verification",
        "scenario": "Negative: Remove Unknown / Non-Existent holidayId",
        "input": "PATCH /holidaylist/{id}/remove/{randomGuid}/{year} where randomGuid does not exist in HolidayLists",
        "expected": "HTTP 400 Bad Request, Cit.Attendance:1710 ('No holiday exists for the selected date.'). Calendar unchanged in DB.",
        "pri": "P1",
        "type": "negative"
    },
    {
        "id": "HC-REM-12",
        "section": "8. Holiday Removal - Past, Today, Future & DB Fields Update Verification",
        "scenario": "Negative: Remove with Route Year mismatching calendar stored Year",
        "input": "PATCH /holidaylist/{id2026}/remove/{holidayId}/2027",
        "expected": "HTTP 400 Bad Request, Cit.Attendance:1711 ('Calendar year does not match requested year.'). DB unchanged.",
        "pri": "P1",
        "type": "negative"
    },
    {
        "id": "HC-REM-13",
        "section": "8. Holiday Removal - Past, Today, Future & DB Fields Update Verification",
        "scenario": "Negative: Remove with Company ID mismatch in Route",
        "input": "PATCH /api/companies/{companyB}/holidaylist/{calendarOfCompanyA}/remove/{holidayId}/{year}",
        "expected": "HTTP 400 Bad Request, Cit.Attendance:1702 / 9001 ('The provided company ID does not match the calendar company.'). Calendar untouched.",
        "pri": "P0",
        "type": "negative"
    },
    {
        "id": "HC-REM-14",
        "section": "8. Holiday Removal - Past, Today, Future & DB Fields Update Verification",
        "scenario": "Negative: Cross-Tenant Holiday Removal attempt",
        "input": "PATCH /holidaylist/{calendarOfTenantB}/remove/{holidayId}/{year} with Tenant A Bearer token",
        "expected": "HTTP 403 Forbidden ('Cross-tenant access is not allowed.'). No DB modification.",
        "pri": "P1",
        "type": "negative"
    },
    {
        "id": "HC-REM-15",
        "section": "8. Holiday Removal - Past, Today, Future & DB Fields Update Verification",
        "scenario": "GET API response verification after removal - Staged state and array length",
        "input": "GET /api/companies/{companyId}/holidaylist/{id} immediately after removal (before publish)",
        "expected": "1. HTTP 200 OK.\n2. Response JSON: yearlyCalendar.holidayLists does NOT contain removed holiday; count is N-1.\n3. Response JSON: isPublished is false (staged changes pending publish).\n4. Response JSON: lastPublishedOn retains previous timestamp.",
        "pri": "P0",
        "type": "smoke"
    }
]

# Styling setup
regular_font = Font(name="Calibri", size=10)
bold_font = Font(name="Calibri", size=10, bold=True)
thin_border_side = Side(border_style="thin", color="D1D5DB")
cell_border = Border(left=thin_border_side, right=thin_border_side, top=thin_border_side, bottom=thin_border_side)

p0_fill = PatternFill(start_color="FEE2E2", end_color="FEE2E2", fill_type="solid") # light red
p1_fill = PatternFill(start_color="FEF3C7", end_color="FEF3C7", fill_type="solid") # light yellow

start_row = ws.max_row + 1
current_row = start_row

rem_p0 = 0
rem_p1 = 0
rem_p2 = 0
rem_p3 = 0

for tc in rem_test_cases:
    ws.append([
        tc["id"],
        tc["section"],
        tc["scenario"],
        tc["input"],
        tc["expected"],
        tc["pri"],
        tc["type"],
        "dev",
        "Not-Run",
        None
    ])
    
    pri = tc["pri"]
    if pri == "P0": rem_p0 += 1
    elif pri == "P1": rem_p1 += 1
    elif pri == "P2": rem_p2 += 1
    elif pri == "P3": rem_p3 += 1
    
    ws.row_dimensions[current_row].height = 28
    for c in range(1, 11):
        cell = ws.cell(row=current_row, column=c)
        cell.font = regular_font
        cell.border = cell_border
        cell.alignment = Alignment(vertical="center", wrap_text=True)
        if c in [1, 6, 7, 8, 9]:
            cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
        if c == 1:
            cell.font = bold_font
        if c == 6:
            if pri == "P0": cell.fill = p0_fill; cell.font = bold_font
            elif pri == "P1": cell.fill = p1_fill; cell.font = bold_font
            elif pri == "P2": cell.fill = p2_fill
    current_row += 1

total_in_sheet = ws.max_row - 1
print(f"Appended {len(rem_test_cases)} removal test cases to '{sheet_name}'.")
print(f"New total in '{sheet_name}': {total_in_sheet} test cases.")

# Re-count all priorities in ws
all_p0 = sum(1 for r in range(2, ws.max_row + 1) if ws.cell(r, 6).value == "P0")
all_p1 = sum(1 for r in range(2, ws.max_row + 1) if ws.cell(r, 6).value == "P1")
all_p2 = sum(1 for r in range(2, ws.max_row + 1) if ws.cell(r, 6).value == "P2")
all_p3 = sum(1 for r in range(2, ws.max_row + 1) if ws.cell(r, 6).value == "P3")
print(f"Sheet Total: {total_in_sheet} | P0={all_p0}, P1={all_p1}, P2={all_p2}, P3={all_p3}")

# Synchronize INDEX sheet
ws_idx = wb['INDEX']
row_mod16 = 20
ws_idx.cell(row_mod16, 3).value = total_in_sheet
ws_idx.cell(row_mod16, 4).value = all_p0
ws_idx.cell(row_mod16, 5).value = all_p1
ws_idx.cell(row_mod16, 6).value = all_p2
ws_idx.cell(row_mod16, 7).value = all_p3
ws_idx.cell(row_mod16, 8).value = "Complete Holiday Suite: DTO Validations, GUIDs, 5 Types, Combinations, Past/Today/Future Removal & DB Fields Update Verification"

# Recalculate TOTAL row (Row 21)
row_total = 21
tot_tcs = sum(ws_idx.cell(r, 3).value for r in range(5, 21) if isinstance(ws_idx.cell(r, 3).value, int))
tot_p0 = sum(ws_idx.cell(r, 4).value for r in range(5, 21) if isinstance(ws_idx.cell(r, 4).value, int))
tot_p1 = sum(ws_idx.cell(r, 5).value for r in range(5, 21) if isinstance(ws_idx.cell(r, 5).value, int))
tot_p2 = sum(ws_idx.cell(r, 6).value for r in range(5, 21) if isinstance(ws_idx.cell(r, 6).value, int))
tot_p3 = sum(ws_idx.cell(r, 7).value for r in range(5, 21) if isinstance(ws_idx.cell(r, 7).value, int))

ws_idx.cell(row_total, 3).value = tot_tcs
ws_idx.cell(row_total, 4).value = tot_p0
ws_idx.cell(row_total, 5).value = tot_p1
ws_idx.cell(row_total, 6).value = tot_p2
ws_idx.cell(row_total, 7).value = tot_p3
ws_idx.cell(row_total, 8).value = "Master Consolidated Suite with Active User Scenarios & Unified Holiday Calendar Multiple Combination & Removal Suite"

print(f"INDEX Row 20 (Module 16): Total={total_in_sheet} (P0:{all_p0}, P1:{all_p1}, P2:{all_p2}, P3:{all_p3})")
print(f"INDEX Row 21 (TOTAL): Total={tot_tcs} (P0:{tot_p0}, P1:{tot_p1}, P2:{tot_p2}, P3:{tot_p3})")

# Save workbook
wb.save('AttendanceTestCases_Master_Consolidated.xlsx')
print("Successfully saved AttendanceTestCases_Master_Consolidated.xlsx!")

