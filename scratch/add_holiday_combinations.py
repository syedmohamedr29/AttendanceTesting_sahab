import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter
import sys

sys.stdout.reconfigure(encoding='utf-8')

wb = openpyxl.load_workbook('AttendanceTestCases_Master_Consolidated.xlsx')

sheet_name = 'Holiday Calendar - Test Cases'
ws = wb[sheet_name]

# Define the 45 combination test cases
comb_test_cases = [
    # Group 1: POST Combinations — 5 Types x (Single-Day vs Multi-Day)
    {
        "id": "HC-COMB-01",
        "section": "1. POST Combinations - 5 Types x (Single vs Multi-Day)",
        "scenario": "POST: Type Public Holiday + Single-Day (Start: 2026-01-01, End: 2026-01-01)",
        "input": "POST /api/companies/{companyId}/holidaylist with Type: Public Holiday, Start: 2026-01-01, End: 2026-01-01 (Single day)",
        "expected": "HTTP 200 OK. DB: YearlyCalendar.HolidayLists[0] has HolidayType.Name.en='Public Holiday', TotalDays=1, StartDate=2026-01-01, EndDate=2026-01-01.",
        "pri": "P0",
        "type": "smoke"
    },
    {
        "id": "HC-COMB-02",
        "section": "1. POST Combinations - 5 Types x (Single vs Multi-Day)",
        "scenario": "POST: Type Public Holiday + Multi-Day (Start: 2026-01-01, End: 2026-01-03)",
        "input": "POST /holidaylist with Type: Public Holiday, Start: 2026-01-01, End: 2026-01-03 (3 days)",
        "expected": "HTTP 200 OK. DB: HolidayType.Name.en='Public Holiday', TotalDays=3, StartDate=2026-01-01, EndDate=2026-01-03.",
        "pri": "P0",
        "type": "smoke"
    },
    {
        "id": "HC-COMB-03",
        "section": "1. POST Combinations - 5 Types x (Single vs Multi-Day)",
        "scenario": "POST: Type Religious Holiday + Single-Day (Start: 2026-07-16, End: 2026-07-16)",
        "input": "POST /holidaylist with Type: Religious Holiday, Start: 2026-07-16, End: 2026-07-16 (Single day)",
        "expected": "HTTP 200 OK. DB: HolidayType.Name.en='Religious Holiday', TotalDays=1.",
        "pri": "P0",
        "type": "smoke"
    },
    {
        "id": "HC-COMB-04",
        "section": "1. POST Combinations - 5 Types x (Single vs Multi-Day)",
        "scenario": "POST: Type Religious Holiday + Multi-Day (Start: 2026-03-20, End: 2026-03-24)",
        "input": "POST /holidaylist with Type: Religious Holiday, Start: 2026-03-20, End: 2026-03-24 (5 days)",
        "expected": "HTTP 200 OK. DB: HolidayType.Name.en='Religious Holiday', TotalDays=5.",
        "pri": "P0",
        "type": "smoke"
    },
    {
        "id": "HC-COMB-05",
        "section": "1. POST Combinations - 5 Types x (Single vs Multi-Day)",
        "scenario": "POST: Type National Holiday + Single-Day (Start: 2026-09-23, End: 2026-09-23)",
        "input": "POST /holidaylist with Type: National Holiday, Start: 2026-09-23, End: 2026-09-23 (Single day)",
        "expected": "HTTP 200 OK. DB: HolidayType.Name.en='National Holiday', TotalDays=1.",
        "pri": "P0",
        "type": "smoke"
    },
    {
        "id": "HC-COMB-06",
        "section": "1. POST Combinations - 5 Types x (Single vs Multi-Day)",
        "scenario": "POST: Type National Holiday + Multi-Day (Start: 2026-02-22, End: 2026-02-24)",
        "input": "POST /holidaylist with Type: National Holiday, Start: 2026-02-22, End: 2026-02-24 (3 days)",
        "expected": "HTTP 200 OK. DB: HolidayType.Name.en='National Holiday', TotalDays=3.",
        "pri": "P0",
        "type": "smoke"
    },
    {
        "id": "HC-COMB-07",
        "section": "1. POST Combinations - 5 Types x (Single vs Multi-Day)",
        "scenario": "POST: Type Bank Holiday + Single-Day (Start: 2026-12-31, End: 2026-12-31)",
        "input": "POST /holidaylist with Type: Bank Holiday, Start: 2026-12-31, End: 2026-12-31 (Single day)",
        "expected": "HTTP 200 OK. DB: HolidayType.Name.en='Bank Holiday', TotalDays=1.",
        "pri": "P1",
        "type": "positive"
    },
    {
        "id": "HC-COMB-08",
        "section": "1. POST Combinations - 5 Types x (Single vs Multi-Day)",
        "scenario": "POST: Type Bank Holiday + Multi-Day (Start: 2026-06-29, End: 2026-06-30)",
        "input": "POST /holidaylist with Type: Bank Holiday, Start: 2026-06-29, End: 2026-06-30 (2 days)",
        "expected": "HTTP 200 OK. DB: HolidayType.Name.en='Bank Holiday', TotalDays=2.",
        "pri": "P1",
        "type": "positive"
    },
    {
        "id": "HC-COMB-09",
        "section": "1. POST Combinations - 5 Types x (Single vs Multi-Day)",
        "scenario": "POST: Type Gazette Holiday + Single-Day (Start: 2026-11-15, End: 2026-11-15)",
        "input": "POST /holidaylist with Type: Gazette Holiday, Start: 2026-11-15, End: 2026-11-15 (Single day)",
        "expected": "HTTP 200 OK. DB: HolidayType.Name.en='Gazette Holiday', TotalDays=1.",
        "pri": "P1",
        "type": "positive"
    },
    {
        "id": "HC-COMB-10",
        "section": "1. POST Combinations - 5 Types x (Single vs Multi-Day)",
        "scenario": "POST: Type Gazette Holiday + Multi-Day (Start: 2026-11-15, End: 2026-11-17)",
        "input": "POST /holidaylist with Type: Gazette Holiday, Start: 2026-11-15, End: 2026-11-17 (3 days)",
        "expected": "HTTP 200 OK. DB: HolidayType.Name.en='Gazette Holiday', TotalDays=3.",
        "pri": "P1",
        "type": "positive"
    },

    # Group 2: POST Date-wise Calendar Edge Boundaries
    {
        "id": "HC-COMB-11",
        "section": "2. POST Date-wise Calendar Edge Boundaries",
        "scenario": "POST: Month-spanning multi-day holiday across 31-day month to next month",
        "input": "POST with holiday StartDate: 2026-01-30, EndDate: 2026-02-02 (Jan 30 to Feb 2)",
        "expected": "HTTP 200 OK. DB: TotalDays=4 (Jan 30, Jan 31, Feb 1, Feb 2). Stored across month boundary.",
        "pri": "P1",
        "type": "boundary"
    },
    {
        "id": "HC-COMB-12",
        "section": "2. POST Date-wise Calendar Edge Boundaries",
        "scenario": "POST: Month-spanning multi-day holiday across 30-day month",
        "input": "POST with holiday StartDate: 2026-04-29, EndDate: 2026-05-03 (Apr 29 to May 3)",
        "expected": "HTTP 200 OK. DB: TotalDays=5 (Apr 29, Apr 30, May 1, May 2, May 3).",
        "pri": "P1",
        "type": "boundary"
    },
    {
        "id": "HC-COMB-13",
        "section": "2. POST Date-wise Calendar Edge Boundaries",
        "scenario": "POST: Year-end boundary single day (2026-12-31)",
        "input": "POST with holiday StartDate: 2026-12-31, EndDate: 2026-12-31",
        "expected": "HTTP 200 OK. DB: TotalDays=1, StartDate=EndDate=2026-12-31.",
        "pri": "P1",
        "type": "boundary"
    },
    {
        "id": "HC-COMB-14",
        "section": "2. POST Date-wise Calendar Edge Boundaries",
        "scenario": "POST: Year-start boundary single day (2026-01-01)",
        "input": "POST with holiday StartDate: 2026-01-01, EndDate: 2026-01-01",
        "expected": "HTTP 200 OK. DB: TotalDays=1, StartDate=EndDate=2026-01-01.",
        "pri": "P1",
        "type": "boundary"
    },
    {
        "id": "HC-COMB-15",
        "section": "2. POST Date-wise Calendar Edge Boundaries",
        "scenario": "POST: Leap-year date spanning Feb 29 (Year 2028: Feb 28 to March 2)",
        "input": "POST in 2028 calendar with StartDate: 2028-02-28, EndDate: 2028-03-02",
        "expected": "HTTP 200 OK. DB: TotalDays=4 (Feb 28, Feb 29, Mar 1, Mar 2). Leap day included.",
        "pri": "P1",
        "type": "boundary"
    },
    {
        "id": "HC-COMB-16",
        "section": "2. POST Date-wise Calendar Edge Boundaries",
        "scenario": "POST: Weekend-overlapping holiday (Starts on Friday, ends on Sunday / company day off)",
        "input": "POST with holiday StartDate: 2026-10-09 (Fri), EndDate: 2026-10-11 (Sun)",
        "expected": "HTTP 200 OK. DB: TotalDays=3. Attendance engine classifies days overlapping company day-off as HolidayOnDayOff.",
        "pri": "P1",
        "type": "integration"
    },

    # Group 3: POST Mixed-Type & Consecutive / Adjacent Date Combinations
    {
        "id": "HC-COMB-17",
        "section": "3. POST Mixed-Type & Consecutive / Adjacent Combinations",
        "scenario": "POST: Mixed payload containing all 5 different holiday types on non-consecutive dates",
        "input": "POST /holidaylist with 1 Public, 1 Religious, 1 National, 1 Bank, 1 Gazette holiday in YearlyCalendar.HolidayLists",
        "expected": "HTTP 200 OK. DB: All 5 types persisted with distinct UUIDs, correct names, and individual TotalDays.",
        "pri": "P0",
        "type": "integration"
    },
    {
        "id": "HC-COMB-18",
        "section": "3. POST Mixed-Type & Consecutive / Adjacent Combinations",
        "scenario": "POST: Adjacent consecutive holidays of DIFFERENT types (H1: National on Oct 1-3; H2: Public on Oct 4-5)",
        "input": "POST with H1 (National): 2026-10-01 to 2026-10-03; H2 (Public): 2026-10-04 to 2026-10-05",
        "expected": "HTTP 200 OK. DB: Both accepted cleanly without false collision error. TotalDays H1=3, H2=2.",
        "pri": "P1",
        "type": "boundary"
    },
    {
        "id": "HC-COMB-19",
        "section": "3. POST Mixed-Type & Consecutive / Adjacent Combinations",
        "scenario": "POST: Adjacent consecutive single-day holidays of SAME type (H1: Religious Aug 10, H2: Religious Aug 11)",
        "input": "POST with H1 (Religious): 2026-08-10 (1 day); H2 (Religious): 2026-08-11 (1 day)",
        "expected": "HTTP 200 OK. DB: Two distinct items in HolidayLists array, each TotalDays=1.",
        "pri": "P1",
        "type": "boundary"
    },
    {
        "id": "HC-COMB-20",
        "section": "3. POST Mixed-Type & Consecutive / Adjacent Combinations",
        "scenario": "POST: Mixed Single-Day and Multi-Day holidays across 3 different types in single calendar",
        "input": "POST with H1: Single Public (Jan 1), H2: Multi Religious (Mar 20-24), H3: Single National (Sep 23)",
        "expected": "HTTP 200 OK. DB: H1 TotalDays=1, H2 TotalDays=5, H3 TotalDays=1.",
        "pri": "P1",
        "type": "positive"
    },

    # Group 4: PATCH Type Mutations (Changing Holiday Type)
    {
        "id": "HC-COMB-21",
        "section": "4. PATCH Type Mutations (Changing Holiday Type)",
        "scenario": "PATCH: Mutate Type from Public Holiday -> National Holiday (same dates)",
        "input": "PATCH /holidaylist/{id}/2026 with holidayId: change type to National Holiday",
        "expected": "HTTP 200 OK. DB: HolidayType.Name.en updated to 'National Holiday', IsPublished=false.",
        "pri": "P0",
        "type": "smoke"
    },
    {
        "id": "HC-COMB-22",
        "section": "4. PATCH Type Mutations (Changing Holiday Type)",
        "scenario": "PATCH: Mutate Type from Public Holiday -> Religious Holiday (same dates)",
        "input": "PATCH with holidayId: change type to Religious Holiday",
        "expected": "HTTP 200 OK. DB: HolidayType.Name.en updated to 'Religious Holiday', IsPublished=false.",
        "pri": "P1",
        "type": "positive"
    },
    {
        "id": "HC-COMB-23",
        "section": "4. PATCH Type Mutations (Changing Holiday Type)",
        "scenario": "PATCH: Mutate Type from Religious Holiday -> Public Holiday",
        "input": "PATCH with holidayId: change type to Public Holiday",
        "expected": "HTTP 200 OK. DB: HolidayType updated to Public Holiday.",
        "pri": "P1",
        "type": "positive"
    },
    {
        "id": "HC-COMB-24",
        "section": "4. PATCH Type Mutations (Changing Holiday Type)",
        "scenario": "PATCH: Mutate Type from National Holiday -> Gazette Holiday",
        "input": "PATCH with holidayId: change type to Gazette Holiday",
        "expected": "HTTP 200 OK. DB: HolidayType updated to Gazette Holiday.",
        "pri": "P1",
        "type": "positive"
    },
    {
        "id": "HC-COMB-25",
        "section": "4. PATCH Type Mutations (Changing Holiday Type)",
        "scenario": "PATCH: Mutate Type from Bank Holiday -> Public Holiday",
        "input": "PATCH with holidayId: change type to Public Holiday",
        "expected": "HTTP 200 OK. DB: HolidayType updated to Public Holiday.",
        "pri": "P1",
        "type": "positive"
    },
    {
        "id": "HC-COMB-26",
        "section": "4. PATCH Type Mutations (Changing Holiday Type)",
        "scenario": "PATCH: Mutate Type from Gazette Holiday -> National Holiday",
        "input": "PATCH with holidayId: change type to National Holiday",
        "expected": "HTTP 200 OK. DB: HolidayType updated to National Holiday.",
        "pri": "P1",
        "type": "positive"
    },

    # Group 5: PATCH Date Combinations (Expand, Shrink, Shift across Types)
    {
        "id": "HC-COMB-27",
        "section": "5. PATCH Date Combinations (Expand, Shrink, Shift across Types)",
        "scenario": "PATCH: Single-Day -> Multi-Day expansion (National Holiday: Start 2026-09-23, End 2026-09-23 -> 2026-09-25)",
        "input": "PATCH with holidayId (National Holiday): change EndDate from 2026-09-23 to 2026-09-25",
        "expected": "HTTP 200 OK. DB: TotalDays updated from 1 to 3, EndDate=2026-09-25, IsPublished=false.",
        "pri": "P0",
        "type": "smoke"
    },
    {
        "id": "HC-COMB-28",
        "section": "5. PATCH Date Combinations (Expand, Shrink, Shift across Types)",
        "scenario": "PATCH: Multi-Day -> Single-Day shrink (Religious Holiday: Start 2026-03-20, End 2026-03-24 -> 2026-03-20)",
        "input": "PATCH with holidayId (Religious Holiday): change EndDate from 2026-03-24 to 2026-03-20",
        "expected": "HTTP 200 OK. DB: TotalDays updated from 5 to 1, EndDate=2026-03-20, IsPublished=false.",
        "pri": "P1",
        "type": "positive"
    },
    {
        "id": "HC-COMB-29",
        "section": "5. PATCH Date Combinations (Expand, Shrink, Shift across Types)",
        "scenario": "PATCH: Shift holiday date earlier within the year (Bank Holiday: shift from Dec 31 -> Dec 20)",
        "input": "PATCH with holidayId (Bank Holiday): change StartDate to 2026-12-20, EndDate to 2026-12-20",
        "expected": "HTTP 200 OK. DB: Dates shifted to Dec 20, TotalDays=1, IsPublished=false.",
        "pri": "P1",
        "type": "positive"
    },
    {
        "id": "HC-COMB-30",
        "section": "5. PATCH Date Combinations (Expand, Shrink, Shift across Types)",
        "scenario": "PATCH: Shift holiday date later within the year (Gazette Holiday: shift from Nov 15 -> Nov 25)",
        "input": "PATCH with holidayId (Gazette Holiday): change StartDate to 2026-11-25, EndDate to 2026-11-25",
        "expected": "HTTP 200 OK. DB: Dates shifted to Nov 25, TotalDays=1, IsPublished=false.",
        "pri": "P1",
        "type": "positive"
    },
    {
        "id": "HC-COMB-31",
        "section": "5. PATCH Date Combinations (Expand, Shrink, Shift across Types)",
        "scenario": "PATCH: Simultaneous Type AND Date change (Public Single-Day -> Religious Multi-Day on new dates)",
        "input": "PATCH with holidayId: change Type to Religious Holiday, StartDate to 2026-05-10, EndDate to 2026-05-13",
        "expected": "HTTP 200 OK. DB: Both Type and Dates updated in single atomic patch. TotalDays=4, IsPublished=false.",
        "pri": "P1",
        "type": "positive"
    },
    {
        "id": "HC-COMB-32",
        "section": "5. PATCH Date Combinations (Expand, Shrink, Shift across Types)",
        "scenario": "PATCH: Month-spanning extension (Expand holiday from March 30 to end on April 2)",
        "input": "PATCH with holidayId: change StartDate to 2026-03-30, EndDate to 2026-04-02",
        "expected": "HTTP 200 OK. DB: TotalDays=4 across month boundary (Mar 30, Mar 31, Apr 1, Apr 2).",
        "pri": "P1",
        "type": "positive"
    },

    # Group 6: Negative Collision Combinations (Date overlaps across different types)
    {
        "id": "HC-COMB-33",
        "section": "6. Negative Collision Combinations across Different Types",
        "scenario": "Collision: Attempt to create Public Holiday and Religious Holiday with identical Start Date",
        "input": "POST with H1 (Public): Start 2026-05-01; H2 (Religious): Start 2026-05-01",
        "expected": "HTTP 400 Bad Request, Cit.Attendance:1707 ('Duplicate holiday date found in the calendar.'). No DB write.",
        "pri": "P0",
        "type": "negative"
    },
    {
        "id": "HC-COMB-34",
        "section": "6. Negative Collision Combinations across Different Types",
        "scenario": "Collision: National Holiday date range overlaps existing Bank Holiday range",
        "input": "POST with H1 (National): 2026-09-20 to 2026-09-24; H2 (Bank): 2026-09-22 to 2026-09-26",
        "expected": "HTTP 400 Bad Request, Cit.Attendance:1707 (reason: 'date-range-overlap').",
        "pri": "P0",
        "type": "negative"
    },
    {
        "id": "HC-COMB-35",
        "section": "6. Negative Collision Combinations across Different Types",
        "scenario": "Collision: Gazette Holiday Start Date falls inside an existing Religious Holiday multi-day window",
        "input": "Calendar has H1 (Religious): 2026-03-20 to 2026-03-24. Attempt to add H2 (Gazette): Start 2026-03-22",
        "expected": "HTTP 400 Bad Request, Cit.Attendance:1707 (reason: 'date-range-overlap'). Calendar unchanged.",
        "pri": "P0",
        "type": "negative"
    },
    {
        "id": "HC-COMB-36",
        "section": "6. Negative Collision Combinations across Different Types",
        "scenario": "Collision via PATCH: Shifting a Public Holiday to collide with a National Holiday",
        "input": "PATCH with H1 (Public): change StartDate to match H2 (National) StartDate",
        "expected": "HTTP 400 Bad Request, Cit.Attendance:1707 ('Duplicate holiday date found in the calendar.'). DB unmodified.",
        "pri": "P1",
        "type": "negative"
    },
    {
        "id": "HC-COMB-37",
        "section": "6. Negative Collision Combinations across Different Types",
        "scenario": "Chronological inversion in Multi-Day across any type (EndDate < StartDate)",
        "input": "POST or PATCH with StartDate: 2026-11-20, EndDate: 2026-11-18",
        "expected": "HTTP 400 Bad Request, Cit.Attendance:1705 (reason: 'endDate-before-startDate').",
        "pri": "P0",
        "type": "negative"
    },
    {
        "id": "HC-COMB-38",
        "section": "6. Negative Collision Combinations across Different Types",
        "scenario": "Multi-year span rejection: Holiday starts in Dec 2026 and ends in Jan 2027",
        "input": "POST with StartDate: 2026-12-30, EndDate: 2027-01-02 in 2026 calendar",
        "expected": "HTTP 400 Bad Request, Cit.Attendance:1705 ('Holiday date year must match selected calendar year.').",
        "pri": "P0",
        "type": "negative"
    },

    # Group 7: GET API & DB Verification for Multiple Combinations
    {
        "id": "HC-COMB-39",
        "section": "7. GET API & DB Verification for Multiple Combinations",
        "scenario": "GET by Year: Verify list includes all combined holiday types with exact dates and calculated TotalDays",
        "input": "GET /api/companies/{companyId}/holidaylist/2026",
        "expected": "HTTP 200 OK. Response matches MongoDB YearlyCalendar.HolidayLists. Each type (Public/Rel/Nat/Bank/Gazette) correctly rendered with matching Start/End dates and TotalDays.",
        "pri": "P0",
        "type": "smoke"
    },
    {
        "id": "HC-COMB-40",
        "section": "7. GET API & DB Verification for Multiple Combinations",
        "scenario": "GET by Year: Verify month-spanning holidays render correct date structure {year, month, day}",
        "input": "GET /api/companies/{companyId}/holidaylist/2026 after adding month-spanning holiday",
        "expected": "HTTP 200 OK. JSON shows StartDate: {year: 2026, month: 1, day: 30}, EndDate: {year: 2026, month: 2, day: 2}, totalDays: 4.",
        "pri": "P1",
        "type": "positive"
    },
    {
        "id": "HC-COMB-41",
        "section": "7. GET API & DB Verification for Multiple Combinations",
        "scenario": "GET by ID: Verify isPublished=false after multiple PATCH type and date edits",
        "input": "GET /api/companies/{companyId}/holidaylist/{id} after PATCH mutations",
        "expected": "HTTP 200 OK. Calendar has isPublished: false, reflecting staged mutations pending publish.",
        "pri": "P0",
        "type": "smoke"
    },
    {
        "id": "HC-COMB-42",
        "section": "7. GET API & DB Verification for Multiple Combinations",
        "scenario": "Publish all combined holidays: POST /publish/{year} syncs all 5 types to inherited locations",
        "input": "POST /api/companies/{companyId}/holidaylist/publish/2026",
        "expected": "HTTP 200 OK ('Holidays published successfully'). DB: Company calendar has IsPublished=true; all inheriting location calendars updated with matching 5 types.",
        "pri": "P0",
        "type": "smoke"
    },
    {
        "id": "HC-COMB-43",
        "section": "7. GET API & DB Verification for Multiple Combinations",
        "scenario": "Customise location: Add unique local Gazette Holiday to location without affecting Company Default",
        "input": "PATCH /{locCalId}/customise, then PATCH to add local Gazette Holiday",
        "expected": "HTTP 200 OK. DB: Location calendar holds local Gazette holiday with IsInherited=false. Company default remains unchanged.",
        "pri": "P0",
        "type": "smoke"
    },
    {
        "id": "HC-COMB-44",
        "section": "7. GET API & DB Verification for Multiple Combinations",
        "scenario": "Remove one holiday from a mixed 5-type calendar: Remaining 4 types stay intact",
        "input": "PATCH /remove/{holidayId}/2026 for 1 holiday in 5-type calendar",
        "expected": "HTTP 200 OK. DB: Only target holiday removed; remaining 4 types persist intact. IsPublished=false.",
        "pri": "P1",
        "type": "regression"
    },
    {
        "id": "HC-COMB-45",
        "section": "7. GET API & DB Verification for Multiple Combinations",
        "scenario": "Re-publish after deletion: Overwrites inherited locations with 4 remaining types",
        "input": "POST /publish/2026 after removal",
        "expected": "HTTP 200 OK. DB: Inherited location calendars synced to 4 remaining types.",
        "pri": "P1",
        "type": "regression"
    }
]

# Styling setup
regular_font = Font(name="Calibri", size=10)
bold_font = Font(name="Calibri", size=10, bold=True)
thin_border_side = Side(border_style="thin", color="D1D5DB")
cell_border = Border(left=thin_border_side, right=thin_border_side, top=thin_border_side, bottom=thin_border_side)

p0_fill = PatternFill(start_color="FEE2E2", end_color="FEE2E2", fill_type="solid") # light red
p1_fill = PatternFill(start_color="FEF3C7", end_color="FEF3C7", fill_type="solid") # light yellow
p2_fill = PatternFill(start_color="F3F4F6", end_color="F3F4F6", fill_type="solid") # light gray

start_row = ws.max_row + 1
current_row = start_row

comb_p0 = 0
comb_p1 = 0
comb_p2 = 0
comb_p3 = 0

for tc in comb_test_cases:
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
    if pri == "P0": comb_p0 += 1
    elif pri == "P1": comb_p1 += 1
    elif pri == "P2": comb_p2 += 1
    elif pri == "P3": comb_p3 += 1
    
    ws.row_dimensions[current_row].height = 26
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
print(f"Appended {len(comb_test_cases)} combination test cases to '{sheet_name}'.")
print(f"New total in '{sheet_name}': {total_in_sheet} test cases.")
print(f"New combinations breakdown: P0={comb_p0}, P1={comb_p1}, P2={comb_p2}, P3={comb_p3}")

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
ws_idx.cell(row_mod16, 8).value = "Complete Holiday Suite: DTO Validations, GUIDs, All 5 Types (Public/Rel/Nat/Bank/Gazette), Single/Multi-Day Combinations, Type Mutations, POST/PATCH/GET & DB State"

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
ws_idx.cell(row_total, 8).value = "Master Consolidated Suite with Active User Scenarios & Unified Holiday Calendar Multiple Combination Suite"

print(f"INDEX Row 20 (Module 16): Total={total_in_sheet} (P0:{all_p0}, P1:{all_p1}, P2:{all_p2}, P3:{all_p3})")
print(f"INDEX Row 21 (TOTAL): Total={tot_tcs} (P0:{tot_p0}, P1:{tot_p1}, P2:{tot_p2}, P3:{tot_p3})")

# Save workbook
wb.save('AttendanceTestCases_Master_Consolidated.xlsx')
print("Successfully saved AttendanceTestCases_Master_Consolidated.xlsx!")

