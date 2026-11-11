import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter
import sys

sys.stdout.reconfigure(encoding='utf-8')

wb = openpyxl.load_workbook('AttendanceTestCases_Master_Consolidated.xlsx')

sheet_name = 'Holiday Calendar - Business'
if sheet_name in wb.sheetnames:
    print(f"Removing existing {sheet_name} to re-generate...")
    del wb[sheet_name]

ws = wb.create_sheet(title=sheet_name)

# Define business logic test cases
test_cases = [
    # Section A: POST - Create Holiday with English Name (en) & Holiday Types (From & To Dates)
    {
        "id": "HC-BUS-01",
        "section": "A. POST - Create Holiday (EN Only) & Type Enum with From/To Dates",
        "scenario": "Create holiday with EN name - Type: Public Holiday (Single-Day: From == To)",
        "input": "POST /api/companies/{companyId}/holidaylist (Year: 2026). Body: shortCode: 'HC2026', name: {'en': 'Company Holidays 2026'}, holidayLists: [{'holidayName': {'en': 'New Year Day'}, 'holidayType': {'_id': '{typePublic}', 'name': {'en': 'Public Holiday'}}, 'startDate': {'year': 2026, 'month': 1, 'day': 1}, 'endDate': {'year': 2026, 'month': 1, 'day': 1}}]",
        "expected": "1. HTTP 200 OK ('Holiday calendar created'). Response returns calendar document with generated holidayId, IsPublished=false.\n2. DB Verification (ERP.Attendance.HolidayCalendars): Document created; YearlyCalendar.HolidayLists[0] has HolidayName.en='New Year Day', HolidayType.Name.en='Public Holiday', StartDate={'Year':2026,'Month':1,'Day':1}, EndDate={'Year':2026,'Month':1,'Day':1}, TotalDays=1.",
        "pri": "P0",
        "type": "smoke"
    },
    {
        "id": "HC-BUS-02",
        "section": "A. POST - Create Holiday (EN Only) & Type Enum with From/To Dates",
        "scenario": "Create holiday with EN name - Type: Religious Holiday (Multi-Day: To > From)",
        "input": "POST /holidaylist with Type: Religious Holiday. Start: 2026-03-20, End: 2026-03-24 (5 days), holidayName: {'en': 'Eid Al-Fitr Holiday'}",
        "expected": "1. HTTP 200 OK.\n2. DB Verification: YearlyCalendar.HolidayLists has HolidayType.Name.en='Religious Holiday', StartDate={'Year':2026,'Month':3,'Day':20}, EndDate={'Year':2026,'Month':3,'Day':24}, TotalDays=5.",
        "pri": "P0",
        "type": "smoke"
    },
    {
        "id": "HC-BUS-03",
        "section": "A. POST - Create Holiday (EN Only) & Type Enum with From/To Dates",
        "scenario": "Create holiday with EN name - Type: National Holiday (Single-Day: From == To)",
        "input": "POST /holidaylist with Type: National Holiday. Start: 2026-09-23, End: 2026-09-23, holidayName: {'en': 'Saudi National Day'}",
        "expected": "1. HTTP 200 OK.\n2. DB Verification: HolidayType.Name.en='National Holiday', TotalDays=1, StartDate=2026-09-23, EndDate=2026-09-23.",
        "pri": "P0",
        "type": "smoke"
    },
    {
        "id": "HC-BUS-04",
        "section": "A. POST - Create Holiday (EN Only) & Type Enum with From/To Dates",
        "scenario": "Create holiday with EN name - Type: Bank Holiday (Single-Day)",
        "input": "POST /holidaylist with Type: Bank Holiday. Start: 2026-12-31, End: 2026-12-31, holidayName: {'en': 'Year-End Bank Closing'}",
        "expected": "1. HTTP 200 OK.\n2. DB Verification: HolidayType.Name.en='Bank Holiday', TotalDays=1.",
        "pri": "P1",
        "type": "positive"
    },
    {
        "id": "HC-BUS-05",
        "section": "A. POST - Create Holiday (EN Only) & Type Enum with From/To Dates",
        "scenario": "Create holiday with EN name - Type: Gazette Holiday (Multi-Day)",
        "input": "POST /holidaylist with Type: Gazette Holiday. Start: 2026-11-15, End: 2026-11-16 (2 days), holidayName: {'en': 'Official Gazette Special Holiday'}",
        "expected": "1. HTTP 200 OK.\n2. DB Verification: HolidayType.Name.en='Gazette Holiday', TotalDays=2.",
        "pri": "P1",
        "type": "positive"
    },
    {
        "id": "HC-BUS-06",
        "section": "A. POST - Create Holiday (EN Only) & Type Enum with From/To Dates",
        "scenario": "Create holiday calendar with all 5 Holiday Types in a single initial payload",
        "input": "POST /holidaylist with array containing 5 items: 1 Public, 1 Religious, 1 National, 1 Bank, 1 Gazette holiday",
        "expected": "1. HTTP 200 OK.\n2. DB Verification: YearlyCalendar.HolidayLists holds 5 documents, each with unique _id, matching types and correct individual TotalDays.",
        "pri": "P0",
        "type": "integration"
    },

    # Section B: POST - Bilingual (EN & AR) & "From Date Only is Mandatory"
    {
        "id": "HC-BUS-07",
        "section": "B. POST - Bilingual (EN & AR) & From Date Only Mandatory Rule",
        "scenario": "Bilingual Public Holiday - From Date only provided (EndDate omitted/null)",
        "input": "POST /holidaylist with holidayName: {'en': 'New Year Holiday', 'ar': 'عطلة رأس السنة'}, Type: Public Holiday, startDate: {'year': 2026, 'month': 1, 'day': 1}, endDate omitted",
        "expected": "1. HTTP 200 OK.\n2. DB Verification: System accepts From Date only, auto-populates EndDate={'Year':2026,'Month':1,'Day':1}, TotalDays=1. Both en and ar names stored in UTF-8.",
        "pri": "P0",
        "type": "smoke"
    },
    {
        "id": "HC-BUS-08",
        "section": "B. POST - Bilingual (EN & AR) & From Date Only Mandatory Rule",
        "scenario": "Bilingual Religious Holiday - From Date only provided (Single-Day Religious Off)",
        "input": "POST /holidaylist with holidayName: {'en': 'Islamic New Year', 'ar': 'عطلة رأس السنة الهجرية'}, Type: Religious Holiday, startDate: 2026-07-16, endDate: null",
        "expected": "1. HTTP 200 OK.\n2. DB Verification: EndDate automatically set equal to StartDate (2026-07-16), TotalDays=1, Arabic name persisted.",
        "pri": "P1",
        "type": "positive"
    },
    {
        "id": "HC-BUS-09",
        "section": "B. POST - Bilingual (EN & AR) & From Date Only Mandatory Rule",
        "scenario": "Bilingual National Holiday - From Date only provided",
        "input": "POST /holidaylist with holidayName: {'en': 'Saudi National Day', 'ar': 'اليوم الوطني للمملكة العربية السعودية'}, Type: National Holiday, startDate: 2026-09-23, endDate omitted",
        "expected": "1. HTTP 200 OK.\n2. DB Verification: EndDate matches StartDate (2026-09-23), TotalDays=1, Arabic name stored accurately.",
        "pri": "P0",
        "type": "smoke"
    },
    {
        "id": "HC-BUS-10",
        "section": "B. POST - Bilingual (EN & AR) & From Date Only Mandatory Rule",
        "scenario": "Bilingual Bank Holiday - From Date only provided",
        "input": "POST /holidaylist with holidayName: {'en': 'Central Bank Holiday', 'ar': 'عطلة البنك المركزي'}, Type: Bank Holiday, startDate: 2026-12-31, endDate: null",
        "expected": "1. HTTP 200 OK.\n2. DB Verification: EndDate matches StartDate, TotalDays=1, HolidayType.Name.en='Bank Holiday'.",
        "pri": "P1",
        "type": "positive"
    },
    {
        "id": "HC-BUS-11",
        "section": "B. POST - Bilingual (EN & AR) & From Date Only Mandatory Rule",
        "scenario": "Bilingual Gazette Holiday - From Date only provided",
        "input": "POST /holidaylist with holidayName: {'en': 'Gazetted Off Day', 'ar': 'يوم عطلة رسمية بالجريدة الرسمية'}, Type: Gazette Holiday, startDate: 2026-08-10, endDate omitted",
        "expected": "1. HTTP 200 OK.\n2. DB Verification: EndDate matches StartDate, TotalDays=1, HolidayType.Name.en='Gazette Holiday'.",
        "pri": "P1",
        "type": "positive"
    },
    {
        "id": "HC-BUS-12",
        "section": "B. POST - Bilingual (EN & AR) & From Date Only Mandatory Rule",
        "scenario": "Bilingual Multi-Day Holiday - Explicit From and To Dates provided",
        "input": "POST /holidaylist with holidayName: {'en': 'Eid Al-Adha Vacation', 'ar': 'إجازة عيد الأضحى المبارك'}, Type: Religious Holiday, Start: 2026-05-27, End: 2026-05-31",
        "expected": "1. HTTP 200 OK.\n2. DB Verification: StartDate=2026-05-27, EndDate=2026-05-31, TotalDays=5. Both English and Arabic names stored.",
        "pri": "P0",
        "type": "smoke"
    },

    # Section C: Negative - End Date Processing System Errors
    {
        "id": "HC-BUS-13",
        "section": "C. Negative - End Date Processing System Errors (POST & PATCH)",
        "scenario": "End Date is chronologically before Start Date (EndDate < StartDate)",
        "input": "POST /holidaylist with startDate: {'year': 2026, 'month': 9, 'day': 25}, endDate: {'year': 2026, 'month': 9, 'day': 23}",
        "expected": "HTTP 400 Bad Request, Cit.Attendance:1705 (data reason: 'endDate-before-startDate'). System throws error; no document written to DB.",
        "pri": "P0",
        "type": "negative"
    },
    {
        "id": "HC-BUS-14",
        "section": "C. Negative - End Date Processing System Errors (POST & PATCH)",
        "scenario": "End Date provided while Start Date is null / missing",
        "input": "POST /holidaylist with startDate: null, endDate: {'year': 2026, 'month': 9, 'day': 25}",
        "expected": "HTTP 400 Bad Request (Sbp:Validation - 'Start date is required.'). No DB insertion.",
        "pri": "P0",
        "type": "negative"
    },
    {
        "id": "HC-BUS-15",
        "section": "C. Negative - End Date Processing System Errors (POST & PATCH)",
        "scenario": "End Date crosses calendar year boundary into next year (Multi-year span)",
        "input": "POST for calendar Year 2026 with holiday startDate: 2026-12-30, endDate: 2027-01-02",
        "expected": "HTTP 400 Bad Request, Cit.Attendance:1705 ('Holiday date year must match the selected calendar year.'). System rejects multi-year span.",
        "pri": "P0",
        "type": "negative"
    },
    {
        "id": "HC-BUS-16",
        "section": "C. Negative - End Date Processing System Errors (POST & PATCH)",
        "scenario": "End Date causes range collision with an existing holiday",
        "input": "Calendar has H1: Oct 10 to Oct 15. Attempt to add H2 with StartDate: Oct 12, EndDate: Oct 18",
        "expected": "HTTP 400 Bad Request, Cit.Attendance:1707 (data reason: 'date-range-overlap'). System throws error; DB unchanged.",
        "pri": "P0",
        "type": "negative"
    },
    {
        "id": "HC-BUS-17",
        "section": "C. Negative - End Date Processing System Errors (POST & PATCH)",
        "scenario": "End Date is non-existent calendar date (February 30)",
        "input": "POST /holidaylist with startDate: 2026-02-28, endDate: 2026-02-30",
        "expected": "HTTP 400 Bad Request (Invalid calendar date). System throws error.",
        "pri": "P1",
        "type": "negative"
    },
    {
        "id": "HC-BUS-18",
        "section": "C. Negative - End Date Processing System Errors (POST & PATCH)",
        "scenario": "End Date is February 29 on a non-leap year (e.g. 2026)",
        "input": "POST /holidaylist (Year 2026) with startDate: 2026-02-28, endDate: 2026-02-29",
        "expected": "HTTP 400 Bad Request (2026 is not a leap year). System throws error.",
        "pri": "P1",
        "type": "negative"
    },
    {
        "id": "HC-BUS-19",
        "section": "C. Negative - End Date Processing System Errors (POST & PATCH)",
        "scenario": "Current Year: End Date in the past (historical holiday addition blocked)",
        "input": "POST /holidaylist for Current Year with startDate: D-5, endDate: D-3",
        "expected": "HTTP 400 Bad Request, Cit.Attendance:1706 ('For current year updates, holiday dates must be future dates.').",
        "pri": "P0",
        "type": "negative"
    },

    # Section D: PATCH - Edit Holiday List (All Types, EN & AR, Upsert & Staging)
    {
        "id": "HC-BUS-20",
        "section": "D. PATCH - Edit Holiday List & Full Business Lifecycle",
        "scenario": "PATCH edit existing holiday - Modify English and Arabic names",
        "input": "PATCH /api/companies/{companyId}/holidaylist/{id}/2026 with existing holidayId: update holidayName to {'en': 'Kingdom National Day (Observed)', 'ar': 'اليوم الوطني للمملكة (عطلة رسمية)'}",
        "expected": "1. HTTP 200 OK ('Holiday calendar updated successfully').\n2. DB Verification: YearlyCalendar.HolidayLists matching ID has updated en and ar names. IsPublished updated to false (staged edit).",
        "pri": "P0",
        "type": "smoke"
    },
    {
        "id": "HC-BUS-21",
        "section": "D. PATCH - Edit Holiday List & Full Business Lifecycle",
        "scenario": "PATCH edit existing holiday - Change Type enum from Public to National Holiday",
        "input": "PATCH /holidaylist/{id}/2026 with existing holidayId: change holidayType._id to {typeNational}, name: 'National Holiday'",
        "expected": "1. HTTP 200 OK.\n2. DB Verification: HolidayType._id and Name updated in MongoDB document. IsPublished=false.",
        "pri": "P0",
        "type": "smoke"
    },
    {
        "id": "HC-BUS-22",
        "section": "D. PATCH - Edit Holiday List & Full Business Lifecycle",
        "scenario": "PATCH edit existing holiday - Change Type enum to Religious Holiday",
        "input": "PATCH /holidaylist/{id}/2026 with existing holidayId: change holidayType to Religious Holiday",
        "expected": "1. HTTP 200 OK.\n2. DB Verification: HolidayType updated to Religious Holiday. IsPublished=false.",
        "pri": "P1",
        "type": "positive"
    },
    {
        "id": "HC-BUS-23",
        "section": "D. PATCH - Edit Holiday List & Full Business Lifecycle",
        "scenario": "PATCH edit existing holiday - Change Type enum to Bank Holiday",
        "input": "PATCH /holidaylist/{id}/2026 with existing holidayId: change holidayType to Bank Holiday",
        "expected": "1. HTTP 200 OK.\n2. DB Verification: HolidayType updated to Bank Holiday. IsPublished=false.",
        "pri": "P1",
        "type": "positive"
    },
    {
        "id": "HC-BUS-24",
        "section": "D. PATCH - Edit Holiday List & Full Business Lifecycle",
        "scenario": "PATCH edit existing holiday - Change Type enum to Gazette Holiday",
        "input": "PATCH /holidaylist/{id}/2026 with existing holidayId: change holidayType to Gazette Holiday",
        "expected": "1. HTTP 200 OK.\n2. DB Verification: HolidayType updated to Gazette Holiday. IsPublished=false.",
        "pri": "P1",
        "type": "positive"
    },
    {
        "id": "HC-BUS-25",
        "section": "D. PATCH - Edit Holiday List & Full Business Lifecycle",
        "scenario": "PATCH edit existing holiday - Extend End Date to increase holiday duration",
        "input": "PATCH with existing holidayId: change endDate from 2026-03-22 to 2026-03-24 (extending from 3 to 5 days)",
        "expected": "1. HTTP 200 OK.\n2. DB Verification: EndDate updated to 2026-03-24, TotalDays recalculated to 5, IsPublished=false.",
        "pri": "P0",
        "type": "smoke"
    },
    {
        "id": "HC-BUS-26",
        "section": "D. PATCH - Edit Holiday List & Full Business Lifecycle",
        "scenario": "PATCH edit existing holiday - Shorten End Date to decrease holiday duration",
        "input": "PATCH with existing holidayId: change endDate from 2026-03-24 to 2026-03-21 (reducing from 5 to 2 days)",
        "expected": "1. HTTP 200 OK.\n2. DB Verification: EndDate updated to 2026-03-21, TotalDays recalculated to 2, IsPublished=false.",
        "pri": "P1",
        "type": "positive"
    },
    {
        "id": "HC-BUS-27",
        "section": "D. PATCH - Edit Holiday List & Full Business Lifecycle",
        "scenario": "PATCH add new holiday via upsert (omitting holiday id) - Single Day From Date only",
        "input": "PATCH /holidaylist/{id}/2026 with new item: holidayName: {'en': 'Founding Day', 'ar': 'يوم التأسيس'}, Type: National Holiday, startDate: 2026-02-22, endDate omitted, no id",
        "expected": "1. HTTP 200 OK.\n2. DB Verification: Server generates fresh holiday UUID, appends to HolidayLists array, sets EndDate=2026-02-22, TotalDays=1, IsPublished=false.",
        "pri": "P0",
        "type": "smoke"
    },
    {
        "id": "HC-BUS-28",
        "section": "D. PATCH - Edit Holiday List & Full Business Lifecycle",
        "scenario": "PATCH add new holiday via upsert (omitting holiday id) - Multi-Day Religious Holiday",
        "input": "PATCH /holidaylist/{id}/2026 with new item: holidayName: {'en': 'Arafat & Eid Day', 'ar': 'يوم عرفة وعيد الأضحى'}, Type: Religious Holiday, Start: 2026-05-26, End: 2026-05-29, no id",
        "expected": "1. HTTP 200 OK.\n2. DB Verification: Fresh UUID generated, TotalDays=4, appended to staged list, IsPublished=false.",
        "pri": "P0",
        "type": "smoke"
    },
    {
        "id": "HC-BUS-29",
        "section": "D. PATCH - Edit Holiday List & Full Business Lifecycle",
        "scenario": "PATCH add new holiday via upsert (id: Guid.Empty)",
        "input": "PATCH with new item holding 'id': '00000000-0000-0000-0000-000000000000', Type: Bank Holiday, Start: 2026-06-30",
        "expected": "1. HTTP 200 OK.\n2. DB Verification: Server replaces Guid.Empty with unique UUID, appends holiday, IsPublished=false.",
        "pri": "P1",
        "type": "positive"
    },
    {
        "id": "HC-BUS-30",
        "section": "D. PATCH - Edit Holiday List & Full Business Lifecycle",
        "scenario": "PATCH negative: Update existing holiday with EndDate < StartDate",
        "input": "PATCH with existing holidayId: change StartDate to 2026-05-28, EndDate to 2026-05-26",
        "expected": "HTTP 400 Bad Request, Cit.Attendance:1705 (reason: 'endDate-before-startDate'). Calendar unchanged in DB.",
        "pri": "P0",
        "type": "negative"
    },
    {
        "id": "HC-BUS-31",
        "section": "D. PATCH - Edit Holiday List & Full Business Lifecycle",
        "scenario": "PATCH negative: Move existing holiday to clash with another existing holiday's StartDate",
        "input": "PATCH with H2: change StartDate to match H1's StartDate (2026-01-01)",
        "expected": "HTTP 400 Bad Request, Cit.Attendance:1707 ('Duplicate holiday date found in the calendar.'). Calendar unchanged.",
        "pri": "P0",
        "type": "negative"
    },
    {
        "id": "HC-BUS-32",
        "section": "D. PATCH - Edit Holiday List & Full Business Lifecycle",
        "scenario": "PATCH negative: Expand existing holiday range to overlap another holiday",
        "input": "PATCH with H1: extend EndDate to overlap H2's StartDate",
        "expected": "HTTP 400 Bad Request, Cit.Attendance:1707 (reason: 'date-range-overlap'). Calendar unchanged.",
        "pri": "P0",
        "type": "negative"
    },
    {
        "id": "HC-BUS-33",
        "section": "D. PATCH - Edit Holiday List & Full Business Lifecycle",
        "scenario": "PATCH remove holiday: Remove future holiday from staged list",
        "input": "PATCH /api/companies/{companyId}/holidaylist/{id}/remove/{holidayId}/2026 (future holiday)",
        "expected": "1. HTTP 200 OK ('Holiday removed successfully').\n2. DB Verification: Target holiday removed from HolidayLists array; IsPublished updated to false.",
        "pri": "P0",
        "type": "smoke"
    },
    {
        "id": "HC-BUS-34",
        "section": "D. PATCH - Edit Holiday List & Full Business Lifecycle",
        "scenario": "PATCH remove holiday negative: Attempt to remove past holiday in Current Year",
        "input": "PATCH /remove/{holidayId}/2026 where holiday startDate < Today",
        "expected": "HTTP 400 Cit.Attendance:1709 ('Past holidays cannot be removed. Only today or future holidays are allowed.'). DB unchanged.",
        "pri": "P0",
        "type": "negative"
    },

    # Section E: GET API Verification & End-to-End DB State Consistency
    {
        "id": "HC-BUS-35",
        "section": "E. GET API Verification & DB State Consistency",
        "scenario": "GET holiday calendar by Year - Verify response matches DB state exactly",
        "input": "GET /api/companies/{companyId}/holidaylist/2026",
        "expected": "1. HTTP 200 OK. Response returns list containing company default and all location calendars.\n2. JSON validation: yearlyCalendar.holidayLists contains all added/edited holidays with matching English & Arabic names, types, dates, and totalDays.\n3. DB Consistency: Response fields match ERP.Attendance.HolidayCalendars document exactly.",
        "pri": "P0",
        "type": "smoke"
    },
    {
        "id": "HC-BUS-36",
        "section": "E. GET API Verification & DB State Consistency",
        "scenario": "GET holiday calendar by ID - Verify staged changes and IsPublished flag",
        "input": "GET /api/companies/{companyId}/holidaylist/{calendarId} after a PATCH edit",
        "expected": "1. HTTP 200 OK.\n2. Response shows isPublished: false, reflecting staged changes pending publish.\n3. DB matches: IsPublished == false, LastPublishedOn retains previous timestamp.",
        "pri": "P0",
        "type": "smoke"
    },
    {
        "id": "HC-BUS-37",
        "section": "E. GET API Verification & DB State Consistency",
        "scenario": "GET holiday calendar with locationId query filter",
        "input": "GET /api/companies/{companyId}/holidaylist/2026?locationId={locId}",
        "expected": "HTTP 200 OK. Returns strictly the calendar applicable to that location (CalendarType: 2).",
        "pri": "P1",
        "type": "positive"
    },
    {
        "id": "HC-BUS-38",
        "section": "E. GET API Verification & DB State Consistency",
        "scenario": "GET holiday calendar with calendarType query filter (CompanyDefault == 1)",
        "input": "GET /api/companies/{companyId}/holidaylist/2026?calendarType=1",
        "expected": "HTTP 200 OK. Returns strictly Company Default calendar; excludes all location copies.",
        "pri": "P1",
        "type": "positive"
    },
    {
        "id": "HC-BUS-39",
        "section": "E. GET API Verification & DB State Consistency",
        "scenario": "GET holiday calendar with calendarType query filter (LocationDefault == 2)",
        "input": "GET /api/companies/{companyId}/holidaylist/2026?calendarType=2",
        "expected": "HTTP 200 OK. Returns strictly Location calendars; excludes Company Default.",
        "pri": "P1",
        "type": "positive"
    },
    {
        "id": "HC-BUS-40",
        "section": "E. GET API Verification & DB State Consistency",
        "scenario": "GET holiday calendar for year with no calendars configured",
        "input": "GET /api/companies/{companyId}/holidaylist/2029 (unconfigured year)",
        "expected": "HTTP 200 OK with empty list: {'holidayCalendars': []}. Does not throw 404 or 500.",
        "pri": "P1",
        "type": "positive"
    },

    # Section F: Fan-Out Cascade, Customise (Detach) & Publish Lifecycle
    {
        "id": "HC-BUS-41",
        "section": "F. Fan-Out Cascade, Customise (Detach) & Publish Lifecycle",
        "scenario": "Company Default creation triggers automatic location fan-out cascade in DB",
        "input": "POST /holidaylist (Company Default, 2 locations in Company Service)",
        "expected": "1. Attendance DB: 1 CompanyDefault (IsInherited=false, CalendarType=1, LocationId=Empty) created.\n2. Attendance DB: 2 LocationDefault calendars (CalendarType=2, IsInherited=true) created, each referencing location GUID and holding cloned holiday list with fresh holiday IDs.\n3. HTTP 200 response calendars array contains all 3 calendars.",
        "pri": "P0",
        "type": "integration"
    },
    {
        "id": "HC-BUS-42",
        "section": "F. Fan-Out Cascade, Customise (Detach) & Publish Lifecycle",
        "scenario": "Inherited location calendars are read-only: PATCH edit blocked",
        "input": "PATCH /holidaylist/{locCalId}/2026?locationId={locId} on inherited location calendar (IsInherited=true)",
        "expected": "HTTP 400 Bad Request, Cit.Attendance:1714 ('This location follows the company holidays. Customise it before editing.'). Calendar unchanged.",
        "pri": "P0",
        "type": "negative"
    },
    {
        "id": "HC-BUS-43",
        "section": "F. Fan-Out Cascade, Customise (Detach) & Publish Lifecycle",
        "scenario": "Customise location calendar (Detach from Company Default)",
        "input": "PATCH /api/companies/{companyId}/holidaylist/{locCalId}/customise",
        "expected": "1. HTTP 200 OK ('Holidays customised successfully').\n2. DB Verification: Target location calendar updates IsInherited = false. It is now unlocked for local editing.",
        "pri": "P0",
        "type": "smoke"
    },
    {
        "id": "HC-BUS-44",
        "section": "F. Fan-Out Cascade, Customise (Detach) & Publish Lifecycle",
        "scenario": "Edit customised location calendar - Add local custom holiday",
        "input": "PATCH /holidaylist/{customisedLocCalId}/2026?locationId={locId} adding local regional holiday",
        "expected": "1. HTTP 200 OK ('Holiday calendar updated successfully').\n2. DB Verification: Local holiday added to location calendar only. Company default calendar is unaffected.",
        "pri": "P0",
        "type": "smoke"
    },
    {
        "id": "HC-BUS-45",
        "section": "F. Fan-Out Cascade, Customise (Detach) & Publish Lifecycle",
        "scenario": "Company edits remain staged and do NOT alter inherited locations before publish",
        "input": "Edit company default to add new holiday, do NOT publish. Call GET on inherited location calendar",
        "expected": "1. Company default has IsPublished=false in DB.\n2. Inherited location calendar still displays previously published holidays in DB and GET API.",
        "pri": "P1",
        "type": "integration"
    },
    {
        "id": "HC-BUS-46",
        "section": "F. Fan-Out Cascade, Customise (Detach) & Publish Lifecycle",
        "scenario": "Publish company calendar: Overwrites inherited locations but preserves customised locations",
        "input": "POST /api/companies/{companyId}/holidaylist/publish/2026 where Loc1 is inherited and Loc2 is customised",
        "expected": "1. HTTP 200 OK ('Holidays published successfully').\n2. DB Verification (Company Default): IsPublished=true, LastPublishedOn updated to current timestamp.\n3. DB Verification (Loc1 - Inherited): Holidays overwritten to match company list.\n4. DB Verification (Loc2 - Customised): Custom local holidays untouched. Not overwritten.",
        "pri": "P0",
        "type": "smoke"
    },
    {
        "id": "HC-BUS-47",
        "section": "F. Fan-Out Cascade, Customise (Detach) & Publish Lifecycle",
        "scenario": "Negative: Customise company default calendar rejected",
        "input": "PATCH /holidaylist/{companyDefaultId}/customise",
        "expected": "HTTP 400 Bad Request, Cit.Attendance:1715 ('Company default holiday calendar cannot be customised.'). DB unmodified.",
        "pri": "P1",
        "type": "negative"
    },
    {
        "id": "HC-BUS-48",
        "section": "F. Fan-Out Cascade, Customise (Detach) & Publish Lifecycle",
        "scenario": "Negative: Re-customise an already customised location calendar",
        "input": "PATCH /holidaylist/{alreadyCustomisedLocId}/customise",
        "expected": "HTTP 400 Bad Request, Cit.Attendance:1716 ('Holiday calendar has already been customised.').",
        "pri": "P1",
        "type": "negative"
    },
    {
        "id": "HC-BUS-49",
        "section": "F. Fan-Out Cascade, Customise (Detach) & Publish Lifecycle",
        "scenario": "Publish with no Company Default existing for that year",
        "input": "POST /publish/2026 for company with no 2026 company default calendar",
        "expected": "HTTP 400 Cit.Attendance:1717 ('Company default holiday calendar not found for the selected year.').",
        "pri": "P1",
        "type": "negative"
    },
    {
        "id": "HC-BUS-50",
        "section": "F. Fan-Out Cascade, Customise (Detach) & Publish Lifecycle",
        "scenario": "Publish with year out of range (Y+2 or past year)",
        "input": "POST /publish/2028 (or past year)",
        "expected": "HTTP 400 Cit.Attendance:1704 ('Holidays can only be published for current or next year.').",
        "pri": "P1",
        "type": "negative"
    }
]

# Write headers
headers = ['TC ID', 'Section', 'Test Scenario', 'Input / Preconditions', 'Expected Result', 'Pri', 'Type', 'Env', 'Status', 'QA Remarks']
ws.append(headers)

# Styling setup
navy_fill = PatternFill(start_color="001E3A8A", end_color="001E3A8A", fill_type="solid")
header_font = Font(name="Calibri", size=11, bold=True, color="FFFFFF")
regular_font = Font(name="Calibri", size=10)
bold_font = Font(name="Calibri", size=10, bold=True)

thin_border_side = Side(border_style="thin", color="D1D5DB")
cell_border = Border(left=thin_border_side, right=thin_border_side, top=thin_border_side, bottom=thin_border_side)

p0_fill = PatternFill(start_color="FEE2E2", end_color="FEE2E2", fill_type="solid") # light red
p1_fill = PatternFill(start_color="FEF3C7", end_color="FEF3C7", fill_type="solid") # light yellow
p2_fill = PatternFill(start_color="F3F4F6", end_color="F3F4F6", fill_type="solid") # light gray

for col_idx, col_name in enumerate(headers, 1):
    cell = ws.cell(row=1, column=col_idx)
    cell.fill = navy_fill
    cell.font = header_font
    cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
    cell.border = cell_border
ws.row_dimensions[1].height = 28

p0_cnt = 0
p1_cnt = 0
p2_cnt = 0
p3_cnt = 0

for row_idx, tc in enumerate(test_cases, 2):
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
    if pri == "P0": p0_cnt += 1
    elif pri == "P1": p1_cnt += 1
    elif pri == "P2": p2_cnt += 1
    elif pri == "P3": p3_cnt += 1
    
    ws.row_dimensions[row_idx].height = 28
    
    for c_idx in range(1, 11):
        cell = ws.cell(row=row_idx, column=c_idx)
        cell.font = regular_font
        cell.border = cell_border
        cell.alignment = Alignment(vertical="center", wrap_text=True)
        
        # Center align short columns
        if c_idx in [1, 6, 7, 8, 9]:
            cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
            
        if c_idx == 1:
            cell.font = bold_font
            
        if c_idx == 6: # Pri coloring
            if pri == "P0": cell.fill = p0_fill; cell.font = bold_font
            elif pri == "P1": cell.fill = p1_fill; cell.font = bold_font
            elif pri == "P2": cell.fill = p2_fill

# Column widths
col_widths = {
    1: 14, # TC ID
    2: 38, # Section
    3: 45, # Test Scenario
    4: 60, # Input / Preconditions
    5: 65, # Expected Result
    6: 8,  # Pri
    7: 14, # Type
    8: 8,  # Env
    9: 12, # Status
    10: 30 # QA Remarks
}
for col_idx, width in col_widths.items():
    ws.column_dimensions[get_column_letter(col_idx)].width = width

print(f"Generated sheet '{sheet_name}' with {len(test_cases)} test cases.")
print(f"Priority breakdown: P0={p0_cnt}, P1={p1_cnt}, P2={p2_cnt}, P3={p3_cnt}, Total={len(test_cases)}")

# Now synchronize INDEX sheet
ws_idx = wb['INDEX']

# Find if Holiday Calendar - Business row exists or where to insert before TOTAL
bus_row = None
total_row = None

for r in range(5, ws_idx.max_row + 1):
    val_c1 = str(ws_idx.cell(r, 1).value).strip() if ws_idx.cell(r, 1).value is not None else ""
    val_c2 = str(ws_idx.cell(r, 2).value).strip() if ws_idx.cell(r, 2).value is not None else ""
    
    if val_c2 == sheet_name:
        bus_row = r
    elif val_c1.upper() == 'TOTAL':
        total_row = r

if not bus_row and total_row:
    # Insert new row before TOTAL
    ws_idx.insert_rows(total_row)
    bus_row = total_row
    total_row = total_row + 1

print(f"Holiday Calendar - Business row in INDEX: {bus_row}, TOTAL row: {total_row}")

mod_num = bus_row - 4
ws_idx.cell(bus_row, 1).value = mod_num
ws_idx.cell(bus_row, 2).value = sheet_name
ws_idx.cell(bus_row, 3).value = len(test_cases)
ws_idx.cell(bus_row, 4).value = p0_cnt
ws_idx.cell(bus_row, 5).value = p1_cnt
ws_idx.cell(bus_row, 6).value = p2_cnt
ws_idx.cell(bus_row, 7).value = p3_cnt
ws_idx.cell(bus_row, 8).value = "Business Logic: All 5 Types (Public, Religious, National, Bank, Gazette), EN & AR, From-Date-Only, End-Date Errors, POST, PATCH & DB State"

# Style the new index row
idx_border = Border(left=thin_border_side, right=thin_border_side, top=thin_border_side, bottom=thin_border_side)
for c in range(1, 9):
    cell = ws_idx.cell(bus_row, c)
    cell.font = regular_font
    cell.border = idx_border
    if c in [1, 3, 4, 5, 6, 7]:
        cell.alignment = Alignment(horizontal="center", vertical="center")
    else:
        cell.alignment = Alignment(vertical="center")

# Recalculate TOTAL row
tot_tcs = sum(ws_idx.cell(r, 3).value for r in range(5, total_row) if isinstance(ws_idx.cell(r, 3).value, int))
tot_p0 = sum(ws_idx.cell(r, 4).value for r in range(5, total_row) if isinstance(ws_idx.cell(r, 4).value, int))
tot_p1 = sum(ws_idx.cell(r, 5).value for r in range(5, total_row) if isinstance(ws_idx.cell(r, 5).value, int))
tot_p2 = sum(ws_idx.cell(r, 6).value for r in range(5, total_row) if isinstance(ws_idx.cell(r, 6).value, int))
tot_p3 = sum(ws_idx.cell(r, 7).value for r in range(5, total_row) if isinstance(ws_idx.cell(r, 7).value, int))

ws_idx.cell(total_row, 1).value = "TOTAL"
ws_idx.cell(total_row, 2).value = f"All {mod_num} Modules Combined"
ws_idx.cell(total_row, 3).value = tot_tcs
ws_idx.cell(total_row, 4).value = tot_p0
ws_idx.cell(total_row, 5).value = tot_p1
ws_idx.cell(total_row, 6).value = tot_p2
ws_idx.cell(total_row, 7).value = tot_p3
ws_idx.cell(total_row, 8).value = "Master Consolidated Suite with Active User Scenarios, Holiday DTO & Business Logic Test Cases"

total_font = Font(name="Calibri", size=11, bold=True)
for c in range(1, 9):
    ws_idx.cell(total_row, c).font = total_font
    ws_idx.cell(total_row, c).border = idx_border

print(f"Updated INDEX sheet:")
print(f"  Row {bus_row}: Module {mod_num} ({sheet_name}) -> Total: {len(test_cases)} (P0:{p0_cnt}, P1:{p1_cnt}, P2:{p2_cnt}, P3:{p3_cnt})")
print(f"  Row {total_row}: Grand Total -> Total: {tot_tcs} (P0:{tot_p0}, P1:{tot_p1}, P2:{tot_p2}, P3:{tot_p3})")

# Save workbook
wb.save('AttendanceTestCases_Master_Consolidated.xlsx')
print("Successfully generated and saved AttendanceTestCases_Master_Consolidated.xlsx!")

