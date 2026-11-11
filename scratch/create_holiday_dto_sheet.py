import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter
import sys

sys.stdout.reconfigure(encoding='utf-8')

wb = openpyxl.load_workbook('AttendanceTestCases_Master_Consolidated.xlsx')

sheet_name = 'Holiday Calendar - DTO'
if sheet_name in wb.sheetnames:
    print(f"Removing existing {sheet_name} to re-generate...")
    del wb[sheet_name]

ws = wb.create_sheet(title=sheet_name)

# Define test cases (1 to 125, plus 126 to 156)
test_cases = [
    # Section A: POST /holidaylist - Route, Header & Scoping Validations
    {
        "id": "HC-DTO-01",
        "section": "A. POST /holidaylist - Route, Header & Scoping Validations",
        "scenario": "companyId route parameter - malformed GUID",
        "input": "POST /api/companies/invalid-uuid-12345/holidaylist with valid body",
        "expected": "HTTP 400 Bad Request (Sbp:Validation - Route parameter companyId is not a valid GUID). No DB write.",
        "pri": "P0",
        "type": "negative"
    },
    {
        "id": "HC-DTO-02",
        "section": "A. POST /holidaylist - Route, Header & Scoping Validations",
        "scenario": "locationId query parameter - malformed GUID",
        "input": "POST /api/companies/{companyId}/holidaylist?locationId=not-a-guid with valid body",
        "expected": "HTTP 400 Bad Request (Sbp:Validation - Query parameter locationId is not a valid GUID).",
        "pri": "P1",
        "type": "negative"
    },
    {
        "id": "HC-DTO-03",
        "section": "A. POST /holidaylist - Route, Header & Scoping Validations",
        "scenario": "Missing Authorization header",
        "input": "POST /api/companies/{companyId}/holidaylist without Authorization header",
        "expected": "HTTP 401 Unauthorized. Request blocked at API gateway.",
        "pri": "P0",
        "type": "negative"
    },
    {
        "id": "HC-DTO-04",
        "section": "A. POST /holidaylist - Route, Header & Scoping Validations",
        "scenario": "Token without tenant ID claim",
        "input": "POST /api/companies/{companyId}/holidaylist with valid JWT omitting tenant claim",
        "expected": "HTTP 401 / 403 SbpAuthorizationException: 'Tenant ID was not resolved.' No documents written.",
        "pri": "P0",
        "type": "negative"
    },

    # Section B: POST /holidaylist - Mandatory vs Non-Mandatory Fields
    {
        "id": "HC-DTO-05",
        "section": "B. POST /holidaylist - Mandatory vs Non-Mandatory Fields",
        "scenario": "Empty request body payload",
        "input": "POST /api/companies/{companyId}/holidaylist with Body: {}",
        "expected": "HTTP 400 Bad Request (Sbp:Validation - Required fields shortCode, name, and yearlyCalendar are missing).",
        "pri": "P0",
        "type": "negative"
    },
    {
        "id": "HC-DTO-06",
        "section": "B. POST /holidaylist - Mandatory vs Non-Mandatory Fields",
        "scenario": "shortCode omitted from payload (Mandatory field)",
        "input": "POST /api/companies/{companyId}/holidaylist omitting shortCode key",
        "expected": "HTTP 400 Bad Request (Sbp:Validation - 'Short code is required.')",
        "pri": "P0",
        "type": "negative"
    },
    {
        "id": "HC-DTO-07",
        "section": "B. POST /holidaylist - Mandatory vs Non-Mandatory Fields",
        "scenario": "shortCode explicit null",
        "input": "POST /api/companies/{companyId}/holidaylist with 'shortCode': null",
        "expected": "HTTP 400 Bad Request (Sbp:Validation - 'Short code is required.')",
        "pri": "P0",
        "type": "negative"
    },
    {
        "id": "HC-DTO-08",
        "section": "B. POST /holidaylist - Mandatory vs Non-Mandatory Fields",
        "scenario": "shortCode empty string (\"\")",
        "input": "POST /api/companies/{companyId}/holidaylist with 'shortCode': \"\"",
        "expected": "HTTP 400 Bad Request (Sbp:Validation - 'Short code is required.')",
        "pri": "P0",
        "type": "negative"
    },
    {
        "id": "HC-DTO-09",
        "section": "B. POST /holidaylist - Mandatory vs Non-Mandatory Fields",
        "scenario": "shortCode whitespace only (\"   \")",
        "input": "POST /api/companies/{companyId}/holidaylist with 'shortCode': \"   \"",
        "expected": "HTTP 400 Bad Request (Sbp:Validation - 'Short code cannot be whitespace only.')",
        "pri": "P1",
        "type": "negative"
    },
    {
        "id": "HC-DTO-10",
        "section": "B. POST /holidaylist - Mandatory vs Non-Mandatory Fields",
        "scenario": "name object omitted or null (Mandatory field)",
        "input": "POST /api/companies/{companyId}/holidaylist with 'name': null",
        "expected": "HTTP 400 Bad Request (Sbp:Validation - 'Name is required.')",
        "pri": "P0",
        "type": "negative"
    },
    {
        "id": "HC-DTO-11",
        "section": "B. POST /holidaylist - Mandatory vs Non-Mandatory Fields",
        "scenario": "name empty object ({})",
        "input": "POST /api/companies/{companyId}/holidaylist with 'name': {}",
        "expected": "HTTP 400 Bad Request (Sbp:Validation - 'Name in English is required.')",
        "pri": "P0",
        "type": "negative"
    },
    {
        "id": "HC-DTO-12",
        "section": "B. POST /holidaylist - Mandatory vs Non-Mandatory Fields",
        "scenario": "name.en empty string (\"\")",
        "input": "POST /api/companies/{companyId}/holidaylist with 'name': {'en': \"\"}",
        "expected": "HTTP 400 Bad Request (Sbp:Validation - 'Name in English is required.')",
        "pri": "P0",
        "type": "negative"
    },
    {
        "id": "HC-DTO-13",
        "section": "B. POST /holidaylist - Mandatory vs Non-Mandatory Fields",
        "scenario": "name.en whitespace only (\"   \")",
        "input": "POST /api/companies/{companyId}/holidaylist with 'name': {'en': \"   \"}",
        "expected": "HTTP 400 Bad Request (Sbp:Validation - 'Name in English cannot be whitespace.')",
        "pri": "P1",
        "type": "negative"
    },
    {
        "id": "HC-DTO-14",
        "section": "B. POST /holidaylist - Mandatory vs Non-Mandatory Fields",
        "scenario": "name.ar omitted (Non-mandatory / optional field)",
        "input": "POST /api/companies/{companyId}/holidaylist with 'name': {'en': 'Company Holidays 2027'} (ar omitted)",
        "expected": "HTTP 200 OK. Calendar created successfully; name.ar persists as null or empty string without error.",
        "pri": "P0",
        "type": "smoke"
    },
    {
        "id": "HC-DTO-15",
        "section": "B. POST /holidaylist - Mandatory vs Non-Mandatory Fields",
        "scenario": "name.ar explicit null",
        "input": "POST /api/companies/{companyId}/holidaylist with 'name': {'en': 'Company Holidays 2027', 'ar': null}",
        "expected": "HTTP 200 OK. Handled gracefully; calendar created successfully.",
        "pri": "P1",
        "type": "positive"
    },
    {
        "id": "HC-DTO-16",
        "section": "B. POST /holidaylist - Mandatory vs Non-Mandatory Fields",
        "scenario": "yearlyCalendar omitted or null (KI-3 crash regression check)",
        "input": "POST /api/companies/{companyId}/holidaylist with 'yearlyCalendar': null",
        "expected": "HTTP 400 Bad Request (Sbp:Validation - 'Yearly calendar is required.'). Must NOT throw 500 NullReferenceException.",
        "pri": "P0",
        "type": "negative"
    },
    {
        "id": "HC-DTO-17",
        "section": "B. POST /holidaylist - Mandatory vs Non-Mandatory Fields",
        "scenario": "yearlyCalendar empty object ({})",
        "input": "POST /api/companies/{companyId}/holidaylist with 'yearlyCalendar': {}",
        "expected": "HTTP 400 Bad Request (Sbp:Validation - 'Year is required.')",
        "pri": "P1",
        "type": "negative"
    },
    {
        "id": "HC-DTO-18",
        "section": "B. POST /holidaylist - Mandatory vs Non-Mandatory Fields",
        "scenario": "yearlyCalendar.year omitted or null",
        "input": "POST /api/companies/{companyId}/holidaylist with 'yearlyCalendar': {'year': null}",
        "expected": "HTTP 400 Bad Request (Sbp:Validation - 'Year is required.')",
        "pri": "P0",
        "type": "negative"
    },
    {
        "id": "HC-DTO-19",
        "section": "B. POST /holidaylist - Mandatory vs Non-Mandatory Fields",
        "scenario": "yearlyCalendar.holidayLists omitted or empty array on initial create",
        "input": "POST /api/companies/{companyId}/holidaylist with 'yearlyCalendar': {'year': 2027, 'holidayLists': []}",
        "expected": "HTTP 200 OK. Shell calendar created with 0 holidays (blank calendar shell for subsequent staging).",
        "pri": "P1",
        "type": "positive"
    },
    {
        "id": "HC-DTO-20",
        "section": "B. POST /holidaylist - Mandatory vs Non-Mandatory Fields",
        "scenario": "Holiday item - holidayName object omitted",
        "input": "POST with holiday item: {'holidayType': {'_id': '{typeId}'}, 'startDate': {...}, 'endDate': {...}}",
        "expected": "HTTP 400 Bad Request (Sbp:Validation - 'Holiday name is required.')",
        "pri": "P0",
        "type": "negative"
    },
    {
        "id": "HC-DTO-21",
        "section": "B. POST /holidaylist - Mandatory vs Non-Mandatory Fields",
        "scenario": "Holiday item - holidayName.en empty string (\"\")",
        "input": "POST with holiday item: {'holidayName': {'en': \"\"}, 'holidayType': {...}, 'startDate': {...}, 'endDate': {...}}",
        "expected": "HTTP 400 Bad Request (Sbp:Validation - 'Holiday name in English is required.')",
        "pri": "P0",
        "type": "negative"
    },
    {
        "id": "HC-DTO-22",
        "section": "B. POST /holidaylist - Mandatory vs Non-Mandatory Fields",
        "scenario": "Holiday item - holidayName.ar omitted (Optional field)",
        "input": "POST with holiday item: {'holidayName': {'en': 'National Day'}, 'holidayType': {...}, 'startDate': {...}, 'endDate': {...}}",
        "expected": "HTTP 200 OK. Holiday created with English name only; holidayName.ar is null.",
        "pri": "P1",
        "type": "positive"
    },
    {
        "id": "HC-DTO-23",
        "section": "B. POST /holidaylist - Mandatory vs Non-Mandatory Fields",
        "scenario": "Holiday item - holidayType object omitted or null",
        "input": "POST with holiday item: {'holidayName': {'en': 'National Day'}, 'holidayType': null, 'startDate': {...}, 'endDate': {...}}",
        "expected": "HTTP 400 Bad Request (Sbp:Validation - 'Holiday type is required.')",
        "pri": "P0",
        "type": "negative"
    },
    {
        "id": "HC-DTO-24",
        "section": "B. POST /holidaylist - Mandatory vs Non-Mandatory Fields",
        "scenario": "Holiday item - holidayType._id empty GUID",
        "input": "POST with holiday item: {'holidayType': {'_id': '00000000-0000-0000-0000-000000000000'}}",
        "expected": "HTTP 400 Bad Request (Sbp:Validation - 'Holiday type ID cannot be empty GUID.')",
        "pri": "P1",
        "type": "negative"
    },
    {
        "id": "HC-DTO-25",
        "section": "B. POST /holidaylist - Mandatory vs Non-Mandatory Fields",
        "scenario": "Holiday item - startDate object omitted or null",
        "input": "POST with holiday item omitting startDate",
        "expected": "HTTP 400 Bad Request (Sbp:Validation - 'Start date is required.')",
        "pri": "P0",
        "type": "negative"
    },
    {
        "id": "HC-DTO-26",
        "section": "B. POST /holidaylist - Mandatory vs Non-Mandatory Fields",
        "scenario": "Holiday item - endDate object omitted or null",
        "input": "POST with holiday item omitting endDate",
        "expected": "HTTP 400 Bad Request (Sbp:Validation - 'End date is required.')",
        "pri": "P0",
        "type": "negative"
    },
    {
        "id": "HC-DTO-27",
        "section": "B. POST /holidaylist - Mandatory vs Non-Mandatory Fields",
        "scenario": "Holiday item - totalDays omitted (Auto-calculated duration)",
        "input": "POST with holiday item omitting totalDays (Start: 2027-09-23, End: 2027-09-25)",
        "expected": "HTTP 200 OK. Server auto-calculates and persists totalDays = 3.",
        "pri": "P1",
        "type": "positive"
    },

    # Section C: POST /holidaylist - String Lengths & Min/Max Character Boundaries
    {
        "id": "HC-DTO-28",
        "section": "C. POST /holidaylist - String Lengths & Min/Max Character Boundaries",
        "scenario": "shortCode - 1 character (below minimum length boundary)",
        "input": "POST with 'shortCode': 'H'",
        "expected": "HTTP 400 Bad Request (Sbp:Validation - Short code must be at least 2 characters).",
        "pri": "P1",
        "type": "negative"
    },
    {
        "id": "HC-DTO-29",
        "section": "C. POST /holidaylist - String Lengths & Min/Max Character Boundaries",
        "scenario": "shortCode - exactly 2 characters (minimum length boundary)",
        "input": "POST with 'shortCode': 'HC'",
        "expected": "HTTP 200 OK. Calendar created successfully with 2-character shortCode 'HC'.",
        "pri": "P0",
        "type": "positive"
    },
    {
        "id": "HC-DTO-30",
        "section": "C. POST /holidaylist - String Lengths & Min/Max Character Boundaries",
        "scenario": "shortCode - standard alphanumeric code",
        "input": "POST with 'shortCode': 'HC-2027'",
        "expected": "HTTP 200 OK. Stored as uppercase 'HC-2027'.",
        "pri": "P0",
        "type": "smoke"
    },
    {
        "id": "HC-DTO-31",
        "section": "C. POST /holidaylist - String Lengths & Min/Max Character Boundaries",
        "scenario": "shortCode - exactly 30 characters (maximum length boundary)",
        "input": "POST with 'shortCode': 'HC2027_SA_COMPANY_OFFICIAL_30'",
        "expected": "HTTP 200 OK. Calendar created with 30-character shortCode.",
        "pri": "P1",
        "type": "positive"
    },
    {
        "id": "HC-DTO-32",
        "section": "C. POST /holidaylist - String Lengths & Min/Max Character Boundaries",
        "scenario": "shortCode - 31 characters (exceeding maximum length boundary)",
        "input": "POST with 'shortCode': 'HC2027_SA_COMPANY_OFFICIAL_31_X'",
        "expected": "HTTP 400 Bad Request (Sbp:Validation - Short code exceeds maximum 30 characters).",
        "pri": "P1",
        "type": "negative"
    },
    {
        "id": "HC-DTO-33",
        "section": "C. POST /holidaylist - String Lengths & Min/Max Character Boundaries",
        "scenario": "shortCode - special symbols rejection",
        "input": "POST with 'shortCode': 'HC@2027!#$%'",
        "expected": "HTTP 400 Bad Request (Sbp:Validation - Short code can only contain letters, numbers, and hyphens/underscores).",
        "pri": "P2",
        "type": "negative"
    },
    {
        "id": "HC-DTO-34",
        "section": "C. POST /holidaylist - String Lengths & Min/Max Character Boundaries",
        "scenario": "shortCode - lowercase conversion",
        "input": "POST with 'shortCode': 'hc-2027'",
        "expected": "HTTP 200 OK. Stored and retrieved in uppercase format 'HC-2027'.",
        "pri": "P1",
        "type": "positive"
    },
    {
        "id": "HC-DTO-35",
        "section": "C. POST /holidaylist - String Lengths & Min/Max Character Boundaries",
        "scenario": "shortCode - leading and trailing whitespace trimming",
        "input": "POST with 'shortCode': '   HC2027   '",
        "expected": "HTTP 200 OK. Server trims leading/trailing whitespace, persisting 'HC2027'.",
        "pri": "P2",
        "type": "positive"
    },
    {
        "id": "HC-DTO-36",
        "section": "C. POST /holidaylist - String Lengths & Min/Max Character Boundaries",
        "scenario": "name.en - exactly 2 characters (minimum length boundary)",
        "input": "POST with 'name': {'en': 'HC'}",
        "expected": "HTTP 200 OK. Calendar created successfully.",
        "pri": "P1",
        "type": "positive"
    },
    {
        "id": "HC-DTO-37",
        "section": "C. POST /holidaylist - String Lengths & Min/Max Character Boundaries",
        "scenario": "name.en - standard descriptive text",
        "input": "POST with 'name': {'en': 'Official Saudi Public Holidays 2027'}",
        "expected": "HTTP 200 OK. Calendar created successfully.",
        "pri": "P0",
        "type": "smoke"
    },
    {
        "id": "HC-DTO-38",
        "section": "C. POST /holidaylist - String Lengths & Min/Max Character Boundaries",
        "scenario": "name.en - exactly 100 characters (maximum length boundary)",
        "input": "POST with 'name': {'en': 'A' * 100}",
        "expected": "HTTP 200 OK. 100-character name persisted without truncation.",
        "pri": "P1",
        "type": "positive"
    },
    {
        "id": "HC-DTO-39",
        "section": "C. POST /holidaylist - String Lengths & Min/Max Character Boundaries",
        "scenario": "name.en - 101 characters (exceeding maximum boundary)",
        "input": "POST with 'name': {'en': 'A' * 101}",
        "expected": "HTTP 400 Bad Request (Sbp:Validation - Name in English cannot exceed 100 characters).",
        "pri": "P1",
        "type": "negative"
    },
    {
        "id": "HC-DTO-40",
        "section": "C. POST /holidaylist - String Lengths & Min/Max Character Boundaries",
        "scenario": "name.en - allowed punctuation and symbols",
        "input": "POST with 'name': {'en': 'HQ & Regional Branches (2027) - Public Holidays / Shift A'}",
        "expected": "HTTP 200 OK. Standard punctuation preserved cleanly.",
        "pri": "P2",
        "type": "positive"
    },
    {
        "id": "HC-DTO-41",
        "section": "C. POST /holidaylist - String Lengths & Min/Max Character Boundaries",
        "scenario": "name.ar - valid Arabic UTF-8 text",
        "input": "POST with 'name': {'en': 'Company Holidays 2027', 'ar': 'عطلات الشركة الرسمية لعام 2027'}",
        "expected": "HTTP 200 OK. Arabic text stored and returned correctly in UTF-8.",
        "pri": "P1",
        "type": "positive"
    },
    {
        "id": "HC-DTO-42",
        "section": "C. POST /holidaylist - String Lengths & Min/Max Character Boundaries",
        "scenario": "name.ar - 101 characters (exceeding maximum boundary)",
        "input": "POST with 'name': {'en': 'Company Holidays', 'ar': 'ع' * 101}",
        "expected": "HTTP 400 Bad Request (Sbp:Validation - Arabic name cannot exceed 100 characters).",
        "pri": "P2",
        "type": "negative"
    },
    {
        "id": "HC-DTO-43",
        "section": "C. POST /holidaylist - String Lengths & Min/Max Character Boundaries",
        "scenario": "holidayLists[].holidayName.en - 2 characters (minimum boundary)",
        "input": "POST with holiday item holidayName.en: 'NY'",
        "expected": "HTTP 200 OK. Holiday created.",
        "pri": "P1",
        "type": "positive"
    },
    {
        "id": "HC-DTO-44",
        "section": "C. POST /holidaylist - String Lengths & Min/Max Character Boundaries",
        "scenario": "holidayLists[].holidayName.en - standard holiday name",
        "input": "POST with holiday item holidayName.en: 'Saudi National Day Holiday'",
        "expected": "HTTP 200 OK. Holiday created.",
        "pri": "P0",
        "type": "smoke"
    },
    {
        "id": "HC-DTO-45",
        "section": "C. POST /holidaylist - String Lengths & Min/Max Character Boundaries",
        "scenario": "holidayLists[].holidayName.en - exactly 100 characters (maximum boundary)",
        "input": "POST with holiday item holidayName.en: 'H' * 100",
        "expected": "HTTP 200 OK. 100-character holiday name persisted.",
        "pri": "P1",
        "type": "positive"
    },
    {
        "id": "HC-DTO-46",
        "section": "C. POST /holidaylist - String Lengths & Min/Max Character Boundaries",
        "scenario": "holidayLists[].holidayName.en - 101 characters (exceeding maximum boundary)",
        "input": "POST with holiday item holidayName.en: 'H' * 101",
        "expected": "HTTP 400 Bad Request (Sbp:Validation - Holiday name cannot exceed 100 characters).",
        "pri": "P1",
        "type": "negative"
    },
    {
        "id": "HC-DTO-47",
        "section": "C. POST /holidaylist - String Lengths & Min/Max Character Boundaries",
        "scenario": "holidayLists[].holidayName.ar - valid Arabic holiday name",
        "input": "POST with holiday item holidayName.ar: 'اليوم الوطني للمملكة العربية السعودية'",
        "expected": "HTTP 200 OK. Arabic holiday name persisted.",
        "pri": "P1",
        "type": "positive"
    },

    # Section D: POST /holidaylist - Year & Date Component Boundaries
    {
        "id": "HC-DTO-48",
        "section": "D. POST /holidaylist - Year & Date Component Boundaries",
        "scenario": "yearlyCalendar.year - Current Year (Y, e.g. 2026)",
        "input": "POST with yearlyCalendar.year: {currentYear}",
        "expected": "HTTP 200 OK. Calendar created for current year.",
        "pri": "P0",
        "type": "smoke"
    },
    {
        "id": "HC-DTO-49",
        "section": "D. POST /holidaylist - Year & Date Component Boundaries",
        "scenario": "yearlyCalendar.year - Next Year (Y+1, e.g. 2027)",
        "input": "POST with yearlyCalendar.year: {nextYear}",
        "expected": "HTTP 200 OK. Calendar created for next year.",
        "pri": "P0",
        "type": "smoke"
    },
    {
        "id": "HC-DTO-50",
        "section": "D. POST /holidaylist - Year & Date Component Boundaries",
        "scenario": "yearlyCalendar.year - Previous Year (Y-1, e.g. 2025) underflow",
        "input": "POST with yearlyCalendar.year: {pastYear}",
        "expected": "HTTP 400 Cit.Attendance:1712 ('Holiday calendar can only be created for the current year or next year.')",
        "pri": "P0",
        "type": "negative"
    },
    {
        "id": "HC-DTO-51",
        "section": "D. POST /holidaylist - Year & Date Component Boundaries",
        "scenario": "yearlyCalendar.year - Future Year (Y+2, e.g. 2028) overflow",
        "input": "POST with yearlyCalendar.year: {futureYearPlus2}",
        "expected": "HTTP 400 Cit.Attendance:1712 ('Holiday calendar can only be created for the current year or next year.')",
        "pri": "P1",
        "type": "negative"
    },
    {
        "id": "HC-DTO-52",
        "section": "D. POST /holidaylist - Year & Date Component Boundaries",
        "scenario": "yearlyCalendar.year - ancient year (1800) or negative year (-2027)",
        "input": "POST with yearlyCalendar.year: 1800",
        "expected": "HTTP 400 Cit.Attendance:1712 / Sbp:Validation.",
        "pri": "P1",
        "type": "negative"
    },
    {
        "id": "HC-DTO-53",
        "section": "D. POST /holidaylist - Year & Date Component Boundaries",
        "scenario": "yearlyCalendar.year - non-integer string ('twenty-twenty-seven')",
        "input": "POST with yearlyCalendar.year: 'twenty-twenty-seven'",
        "expected": "HTTP 400 Bad Request (JSON deserialization error - expected integer).",
        "pri": "P2",
        "type": "negative"
    },
    {
        "id": "HC-DTO-54",
        "section": "D. POST /holidaylist - Year & Date Component Boundaries",
        "scenario": "startDate.month - underflow month 0 or -1",
        "input": "POST with holiday startDate: {'year': 2027, 'month': 0, 'day': 15}",
        "expected": "HTTP 400 Bad Request (Sbp:Validation - Month must be between 1 and 12).",
        "pri": "P1",
        "type": "negative"
    },
    {
        "id": "HC-DTO-55",
        "section": "D. POST /holidaylist - Year & Date Component Boundaries",
        "scenario": "startDate.month - overflow month 13",
        "input": "POST with holiday startDate: {'year': 2027, 'month': 13, 'day': 15}",
        "expected": "HTTP 400 Bad Request (Sbp:Validation - Month must be between 1 and 12).",
        "pri": "P1",
        "type": "negative"
    },
    {
        "id": "HC-DTO-56",
        "section": "D. POST /holidaylist - Year & Date Component Boundaries",
        "scenario": "startDate.month - boundary valid months (January = 1, December = 12)",
        "input": "POST with H1 month: 1, H2 month: 12",
        "expected": "HTTP 200 OK. Valid boundary months accepted.",
        "pri": "P1",
        "type": "positive"
    },
    {
        "id": "HC-DTO-57",
        "section": "D. POST /holidaylist - Year & Date Component Boundaries",
        "scenario": "startDate.day - underflow day 0 or -1",
        "input": "POST with holiday startDate: {'year': 2027, 'month': 5, 'day': 0}",
        "expected": "HTTP 400 Bad Request (Sbp:Validation - Day must be between 1 and 31).",
        "pri": "P1",
        "type": "negative"
    },
    {
        "id": "HC-DTO-58",
        "section": "D. POST /holidaylist - Year & Date Component Boundaries",
        "scenario": "startDate.day - overflow day 32",
        "input": "POST with holiday startDate: {'year': 2027, 'month': 5, 'day': 32}",
        "expected": "HTTP 400 Bad Request (Sbp:Validation - Day must be between 1 and 31).",
        "pri": "P1",
        "type": "negative"
    },
    {
        "id": "HC-DTO-59",
        "section": "D. POST /holidaylist - Year & Date Component Boundaries",
        "scenario": "startDate.day - boundary valid days (day: 1 and day: 31 for 31-day month)",
        "input": "POST with holiday start: 2027-01-01, end: 2027-01-31",
        "expected": "HTTP 200 OK. Valid calendar boundaries accepted.",
        "pri": "P0",
        "type": "positive"
    },
    {
        "id": "HC-DTO-60",
        "section": "D. POST /holidaylist - Year & Date Component Boundaries",
        "scenario": "Invalid calendar date - February 29 on non-leap year (e.g. 2027-02-29)",
        "input": "POST with holiday startDate: {'year': 2027, 'month': 2, 'day': 29}",
        "expected": "HTTP 400 Bad Request (Invalid date - 2027 is not a leap year).",
        "pri": "P1",
        "type": "negative"
    },
    {
        "id": "HC-DTO-61",
        "section": "D. POST /holidaylist - Year & Date Component Boundaries",
        "scenario": "Valid calendar date - February 29 on leap year (e.g. 2028-02-29)",
        "input": "POST with holiday startDate: {'year': 2028, 'month': 2, 'day': 29} (in a 2028 calendar)",
        "expected": "HTTP 200 OK. Valid leap year date accepted.",
        "pri": "P1",
        "type": "positive"
    },
    {
        "id": "HC-DTO-62",
        "section": "D. POST /holidaylist - Year & Date Component Boundaries",
        "scenario": "Invalid calendar date - February 30 (2027-02-30)",
        "input": "POST with holiday startDate: {'year': 2027, 'month': 2, 'day': 30}",
        "expected": "HTTP 400 Bad Request (Invalid calendar date - February never has 30 days).",
        "pri": "P1",
        "type": "negative"
    },
    {
        "id": "HC-DTO-63",
        "section": "D. POST /holidaylist - Year & Date Component Boundaries",
        "scenario": "Invalid calendar date - April 31 (2027-04-31)",
        "input": "POST with holiday startDate: {'year': 2027, 'month': 4, 'day': 31}",
        "expected": "HTTP 400 Bad Request (Invalid calendar date - April has only 30 days).",
        "pri": "P1",
        "type": "negative"
    },
    {
        "id": "HC-DTO-64",
        "section": "D. POST /holidaylist - Year & Date Component Boundaries",
        "scenario": "Single-day holiday: startDate == endDate",
        "input": "POST with startDate: {year: 2027, month: 9, day: 23}, endDate: {year: 2027, month: 9, day: 23}",
        "expected": "HTTP 200 OK. Persisted with totalDays = 1.",
        "pri": "P0",
        "type": "smoke"
    },
    {
        "id": "HC-DTO-65",
        "section": "D. POST /holidaylist - Year & Date Component Boundaries",
        "scenario": "Multi-day holiday: endDate > startDate",
        "input": "POST with startDate: {year: 2027, month: 9, day: 23}, endDate: {year: 2027, month: 9, day: 26}",
        "expected": "HTTP 200 OK. Persisted with totalDays = 4.",
        "pri": "P0",
        "type": "smoke"
    },
    {
        "id": "HC-DTO-66",
        "section": "D. POST /holidaylist - Year & Date Component Boundaries",
        "scenario": "Chronological inversion: endDate < startDate",
        "input": "POST with startDate: {year: 2027, month: 9, day: 25}, endDate: {year: 2027, month: 9, day: 23}",
        "expected": "HTTP 400 Cit.Attendance:1705 (reason: 'endDate-before-startDate').",
        "pri": "P0",
        "type": "negative"
    },
    {
        "id": "HC-DTO-67",
        "section": "D. POST /holidaylist - Year & Date Component Boundaries",
        "scenario": "Holiday year mismatch with calendar year",
        "input": "POST for calendar year 2027 with a holiday dated 2026-12-31",
        "expected": "HTTP 400 Cit.Attendance:1705 ('Holiday date year must match selected calendar year.')",
        "pri": "P0",
        "type": "negative"
    },
    {
        "id": "HC-DTO-68",
        "section": "D. POST /holidaylist - Year & Date Component Boundaries",
        "scenario": "Current year past holiday on create (startDate < Today)",
        "input": "POST for Current Year with a holiday dated yesterday",
        "expected": "HTTP 400 Cit.Attendance:1706 ('For current year, holiday dates must be future dates.')",
        "pri": "P0",
        "type": "negative"
    },
    {
        "id": "HC-DTO-69",
        "section": "D. POST /holidaylist - Year & Date Component Boundaries",
        "scenario": "Two holidays with identical startDate in create payload",
        "input": "POST with H1 start: 2027-05-01, H2 start: 2027-05-01",
        "expected": "HTTP 400 Cit.Attendance:1707 ('Duplicate holiday date found in the calendar.')",
        "pri": "P0",
        "type": "negative"
    },
    {
        "id": "HC-DTO-70",
        "section": "D. POST /holidaylist - Year & Date Component Boundaries",
        "scenario": "Two holidays with overlapping date ranges in create payload",
        "input": "POST with H1: 2027-06-01 to 2027-06-05, H2: 2027-06-03 to 2027-06-08",
        "expected": "HTTP 400 Cit.Attendance:1707 (Date range overlap).",
        "pri": "P0",
        "type": "negative"
    },

    # Section E: PATCH /{id}/{year} - Route & Query Parameter Validations
    {
        "id": "HC-DTO-71",
        "section": "E. PATCH /{id}/{year} - Route & Query Parameter Validations",
        "scenario": "Route {id} - malformed GUID format",
        "input": "PATCH /api/companies/{companyId}/holidaylist/not-a-guid/2027",
        "expected": "HTTP 400 Bad Request (Sbp:Validation - Route id is not a valid GUID).",
        "pri": "P0",
        "type": "negative"
    },
    {
        "id": "HC-DTO-72",
        "section": "E. PATCH /{id}/{year} - Route & Query Parameter Validations",
        "scenario": "Route {id} - empty GUID",
        "input": "PATCH /api/companies/{companyId}/holidaylist/00000000-0000-0000-0000-000000000000/2027",
        "expected": "HTTP 400 Bad Request (Sbp:Validation - Route id cannot be empty GUID).",
        "pri": "P0",
        "type": "negative"
    },
    {
        "id": "HC-DTO-73",
        "section": "E. PATCH /{id}/{year} - Route & Query Parameter Validations",
        "scenario": "Route {id} - unknown calendar ID not in DB",
        "input": "PATCH /api/companies/{companyId}/holidaylist/{randomGuid}/2027",
        "expected": "HTTP 400 Cit.Attendance:1701 ('Holiday calendar not found.')",
        "pri": "P0",
        "type": "negative"
    },
    {
        "id": "HC-DTO-74",
        "section": "E. PATCH /{id}/{year} - Route & Query Parameter Validations",
        "scenario": "Route {year} - non-numeric string value",
        "input": "PATCH /api/companies/{companyId}/holidaylist/{id}/year2027",
        "expected": "HTTP 400 Bad Request (Route parameter type mismatch).",
        "pri": "P0",
        "type": "negative"
    },
    {
        "id": "HC-DTO-75",
        "section": "E. PATCH /{id}/{year} - Route & Query Parameter Validations",
        "scenario": "Route {year} - out of range (Y-1 or Y+2)",
        "input": "PATCH /api/companies/{companyId}/holidaylist/{id}/{pastYear}",
        "expected": "HTTP 400 Cit.Attendance:1704 ('Holidays can only be updated for current or next year.')",
        "pri": "P1",
        "type": "negative"
    },
    {
        "id": "HC-DTO-76",
        "section": "E. PATCH /{id}/{year} - Route & Query Parameter Validations",
        "scenario": "Route {year} mismatch with target calendar's stored Year",
        "input": "PATCH /api/companies/{companyId}/holidaylist/{id2027}/2026",
        "expected": "HTTP 400 Cit.Attendance:1711 ('Calendar year does not match requested year.')",
        "pri": "P0",
        "type": "negative"
    },
    {
        "id": "HC-DTO-77",
        "section": "E. PATCH /{id}/{year} - Route & Query Parameter Validations",
        "scenario": "Query locationId - malformed GUID on location edit",
        "input": "PATCH /api/companies/{companyId}/holidaylist/{id}/2027?locationId=bad-guid",
        "expected": "HTTP 400 Bad Request (Sbp:Validation - Query parameter locationId is not a valid GUID).",
        "pri": "P1",
        "type": "negative"
    },
    {
        "id": "HC-DTO-78",
        "section": "E. PATCH /{id}/{year} - Route & Query Parameter Validations",
        "scenario": "Query locationId mismatch with location calendar's locationId",
        "input": "PATCH /api/companies/{companyId}/holidaylist/{locCalA}/2027?locationId={locB}",
        "expected": "HTTP 400 Cit.Attendance:1703 ('The provided location ID does not match the calendar location.')",
        "pri": "P1",
        "type": "negative"
    },

    # Section F: PATCH /{id}/{year} - Mandatory & Non-Mandatory Fields
    {
        "id": "HC-DTO-79",
        "section": "F. PATCH /{id}/{year} - Mandatory & Non-Mandatory Fields",
        "scenario": "Empty PATCH body payload ({})",
        "input": "PATCH /api/companies/{companyId}/holidaylist/{id}/2027 with Body: {}",
        "expected": "HTTP 400 Bad Request (Sbp:Validation - 'At least one update field is required.')",
        "pri": "P0",
        "type": "negative"
    },
    {
        "id": "HC-DTO-80",
        "section": "F. PATCH /{id}/{year} - Mandatory & Non-Mandatory Fields",
        "scenario": "holidayLists sent as empty array ([]) on update",
        "input": "PATCH /api/companies/{companyId}/holidaylist/{id}/2027 with 'holidayLists': []",
        "expected": "HTTP 400 Cit.Attendance:1704 (reason: 'no-holidays-provided').",
        "pri": "P0",
        "type": "negative"
    },
    {
        "id": "HC-DTO-81",
        "section": "F. PATCH /{id}/{year} - Mandatory & Non-Mandatory Fields",
        "scenario": "Holiday item in PATCH missing holidayName",
        "input": "PATCH with holiday item omitting holidayName",
        "expected": "HTTP 400 Bad Request (Sbp:Validation - 'Holiday name is required.')",
        "pri": "P0",
        "type": "negative"
    },
    {
        "id": "HC-DTO-82",
        "section": "F. PATCH /{id}/{year} - Mandatory & Non-Mandatory Fields",
        "scenario": "Holiday item in PATCH with holidayName.en empty string (\"\")",
        "input": "PATCH with holidayName: {'en': \"\"}",
        "expected": "HTTP 400 Bad Request (Sbp:Validation - 'Holiday name in English is required.')",
        "pri": "P0",
        "type": "negative"
    },
    {
        "id": "HC-DTO-83",
        "section": "F. PATCH /{id}/{year} - Mandatory & Non-Mandatory Fields",
        "scenario": "Holiday item in PATCH with holidayName.ar omitted (Optional)",
        "input": "PATCH with holidayName: {'en': 'Updated National Day'} (ar omitted)",
        "expected": "HTTP 200 OK. Holiday updated with English name; IsPublished becomes false.",
        "pri": "P1",
        "type": "positive"
    },
    {
        "id": "HC-DTO-84",
        "section": "F. PATCH /{id}/{year} - Mandatory & Non-Mandatory Fields",
        "scenario": "Holiday item in PATCH with holidayName.ar: null",
        "input": "PATCH with holidayName: {'en': 'Updated National Day', 'ar': null}",
        "expected": "HTTP 200 OK. Handled gracefully; holiday updated.",
        "pri": "P1",
        "type": "positive"
    },
    {
        "id": "HC-DTO-85",
        "section": "F. PATCH /{id}/{year} - Mandatory & Non-Mandatory Fields",
        "scenario": "Holiday item in PATCH missing holidayType",
        "input": "PATCH with holiday item omitting holidayType",
        "expected": "HTTP 400 Bad Request (Sbp:Validation - 'Holiday type is required.')",
        "pri": "P0",
        "type": "negative"
    },
    {
        "id": "HC-DTO-86",
        "section": "F. PATCH /{id}/{year} - Mandatory & Non-Mandatory Fields",
        "scenario": "Holiday item in PATCH with unknown holidayType._id",
        "input": "PATCH with holidayType: {'_id': '{randomGuid}'}",
        "expected": "HTTP 400 Bad Request ('Holiday type not found in Company Service.')",
        "pri": "P1",
        "type": "negative"
    },
    {
        "id": "HC-DTO-87",
        "section": "F. PATCH /{id}/{year} - Mandatory & Non-Mandatory Fields",
        "scenario": "Holiday item in PATCH missing startDate",
        "input": "PATCH with holiday item omitting startDate",
        "expected": "HTTP 400 Bad Request (Sbp:Validation - 'Start date is required.')",
        "pri": "P0",
        "type": "negative"
    },
    {
        "id": "HC-DTO-88",
        "section": "F. PATCH /{id}/{year} - Mandatory & Non-Mandatory Fields",
        "scenario": "Holiday item in PATCH missing endDate",
        "input": "PATCH with holiday item omitting endDate",
        "expected": "HTTP 400 Bad Request (Sbp:Validation - 'End date is required.')",
        "pri": "P0",
        "type": "negative"
    },
    {
        "id": "HC-DTO-89",
        "section": "F. PATCH /{id}/{year} - Mandatory & Non-Mandatory Fields",
        "scenario": "Holiday item in PATCH omitting totalDays",
        "input": "PATCH with holiday item without totalDays",
        "expected": "HTTP 200 OK. Server auto-calculates totalDays from updated date range.",
        "pri": "P1",
        "type": "positive"
    },
    {
        "id": "HC-DTO-90",
        "section": "F. PATCH /{id}/{year} - Mandatory & Non-Mandatory Fields",
        "scenario": "Holiday item in PATCH with id omitted (Add new holiday via upsert)",
        "input": "PATCH with new holiday item without id field",
        "expected": "HTTP 200 OK. Server assigns fresh UUID and appends holiday to staged list. IsPublished = false.",
        "pri": "P0",
        "type": "smoke"
    },
    {
        "id": "HC-DTO-91",
        "section": "F. PATCH /{id}/{year} - Mandatory & Non-Mandatory Fields",
        "scenario": "Holiday item in PATCH with id: Guid.Empty (Add new holiday via upsert)",
        "input": "PATCH with new holiday item with 'id': '00000000-0000-0000-0000-000000000000'",
        "expected": "HTTP 200 OK. Server generates fresh UUID and appends holiday.",
        "pri": "P1",
        "type": "positive"
    },

    # Section G: PATCH /{id}/{year} - String Lengths & Character Boundaries
    {
        "id": "HC-DTO-92",
        "section": "G. PATCH /{id}/{year} - String Lengths & Character Boundaries",
        "scenario": "PATCH holidayName.en - 2 characters (minimum boundary)",
        "input": "PATCH holiday with holidayName.en: 'FD'",
        "expected": "HTTP 200 OK. Updated successfully.",
        "pri": "P1",
        "type": "positive"
    },
    {
        "id": "HC-DTO-93",
        "section": "G. PATCH /{id}/{year} - String Lengths & Character Boundaries",
        "scenario": "PATCH holidayName.en - standard descriptive name",
        "input": "PATCH holiday with holidayName.en: 'Founding Day Extended Holiday'",
        "expected": "HTTP 200 OK. Updated successfully.",
        "pri": "P0",
        "type": "smoke"
    },
    {
        "id": "HC-DTO-94",
        "section": "G. PATCH /{id}/{year} - String Lengths & Character Boundaries",
        "scenario": "PATCH holidayName.en - exactly 100 characters (maximum boundary)",
        "input": "PATCH holiday with holidayName.en: 'F' * 100",
        "expected": "HTTP 200 OK. Persisted without truncation.",
        "pri": "P1",
        "type": "positive"
    },
    {
        "id": "HC-DTO-95",
        "section": "G. PATCH /{id}/{year} - String Lengths & Character Boundaries",
        "scenario": "PATCH holidayName.en - 101 characters (exceeding boundary)",
        "input": "PATCH holiday with holidayName.en: 'F' * 101",
        "expected": "HTTP 400 Bad Request (Sbp:Validation - Holiday name cannot exceed 100 characters).",
        "pri": "P1",
        "type": "negative"
    },
    {
        "id": "HC-DTO-96",
        "section": "G. PATCH /{id}/{year} - String Lengths & Character Boundaries",
        "scenario": "PATCH holidayName.ar - valid Arabic text",
        "input": "PATCH holiday with holidayName.ar: 'عطلة يوم التأسيس الرسمي'",
        "expected": "HTTP 200 OK. Arabic text updated in UTF-8.",
        "pri": "P1",
        "type": "positive"
    },
    {
        "id": "HC-DTO-97",
        "section": "G. PATCH /{id}/{year} - String Lengths & Character Boundaries",
        "scenario": "PATCH holidayName.ar - 101 characters (exceeding boundary)",
        "input": "PATCH holiday with holidayName.ar: 'ع' * 101",
        "expected": "HTTP 400 Bad Request (Sbp:Validation - Arabic holiday name cannot exceed 100 characters).",
        "pri": "P2",
        "type": "negative"
    },

    # Section H: PATCH /{id}/{year} - Date Component & Chronological Boundaries
    {
        "id": "HC-DTO-98",
        "section": "H. PATCH /{id}/{year} - Date Component & Chronological Boundaries",
        "scenario": "PATCH startDate.month - underflow month 0 or -1",
        "input": "PATCH holiday with startDate: {'year': 2027, 'month': 0, 'day': 10}",
        "expected": "HTTP 400 Bad Request (Sbp:Validation - Month must be between 1 and 12).",
        "pri": "P1",
        "type": "negative"
    },
    {
        "id": "HC-DTO-99",
        "section": "H. PATCH /{id}/{year} - Date Component & Chronological Boundaries",
        "scenario": "PATCH startDate.month - overflow month 13",
        "input": "PATCH holiday with startDate: {'year': 2027, 'month': 13, 'day': 10}",
        "expected": "HTTP 400 Bad Request (Sbp:Validation - Month must be between 1 and 12).",
        "pri": "P1",
        "type": "negative"
    },
    {
        "id": "HC-DTO-100",
        "section": "H. PATCH /{id}/{year} - Date Component & Chronological Boundaries",
        "scenario": "PATCH startDate.day - underflow day 0 or -1",
        "input": "PATCH holiday with startDate: {'year': 2027, 'month': 7, 'day': 0}",
        "expected": "HTTP 400 Bad Request (Sbp:Validation - Day must be between 1 and 31).",
        "pri": "P1",
        "type": "negative"
    },
    {
        "id": "HC-DTO-101",
        "section": "H. PATCH /{id}/{year} - Date Component & Chronological Boundaries",
        "scenario": "PATCH startDate.day - overflow day 32",
        "input": "PATCH holiday with startDate: {'year': 2027, 'month': 7, 'day': 32}",
        "expected": "HTTP 400 Bad Request (Sbp:Validation - Day must be between 1 and 31).",
        "pri": "P1",
        "type": "negative"
    },
    {
        "id": "HC-DTO-102",
        "section": "H. PATCH /{id}/{year} - Date Component & Chronological Boundaries",
        "scenario": "PATCH invalid date - February 29 on non-leap year (e.g. 2027-02-29)",
        "input": "PATCH holiday with startDate: {'year': 2027, 'month': 2, 'day': 29}",
        "expected": "HTTP 400 Bad Request (Invalid date - 2027 is not a leap year).",
        "pri": "P1",
        "type": "negative"
    },
    {
        "id": "HC-DTO-103",
        "section": "H. PATCH /{id}/{year} - Date Component & Chronological Boundaries",
        "scenario": "PATCH leap year date - February 29 on leap year (e.g. 2028-02-29)",
        "input": "PATCH holiday in 2028 calendar with startDate: {'year': 2028, 'month': 2, 'day': 29}",
        "expected": "HTTP 200 OK. Valid leap year holiday updated.",
        "pri": "P1",
        "type": "positive"
    },
    {
        "id": "HC-DTO-104",
        "section": "H. PATCH /{id}/{year} - Date Component & Chronological Boundaries",
        "scenario": "PATCH invalid date - February 30 (2027-02-30)",
        "input": "PATCH holiday with startDate: {'year': 2027, 'month': 2, 'day': 30}",
        "expected": "HTTP 400 Bad Request (Invalid calendar date).",
        "pri": "P1",
        "type": "negative"
    },
    {
        "id": "HC-DTO-105",
        "section": "H. PATCH /{id}/{year} - Date Component & Chronological Boundaries",
        "scenario": "PATCH invalid date - June 31 (2027-06-31)",
        "input": "PATCH holiday with startDate: {'year': 2027, 'month': 6, 'day': 31}",
        "expected": "HTTP 400 Bad Request (Invalid calendar date - June has 30 days).",
        "pri": "P1",
        "type": "negative"
    },
    {
        "id": "HC-DTO-106",
        "section": "H. PATCH /{id}/{year} - Date Component & Chronological Boundaries",
        "scenario": "PATCH single-day holiday: startDate == endDate",
        "input": "PATCH holiday with startDate: 2027-02-22, endDate: 2027-02-22",
        "expected": "HTTP 200 OK. TotalDays = 1.",
        "pri": "P0",
        "type": "smoke"
    },
    {
        "id": "HC-DTO-107",
        "section": "H. PATCH /{id}/{year} - Date Component & Chronological Boundaries",
        "scenario": "PATCH multi-day holiday: endDate > startDate",
        "input": "PATCH holiday with startDate: 2027-02-22, endDate: 2027-02-25",
        "expected": "HTTP 200 OK. TotalDays = 4.",
        "pri": "P0",
        "type": "smoke"
    },
    {
        "id": "HC-DTO-108",
        "section": "H. PATCH /{id}/{year} - Date Component & Chronological Boundaries",
        "scenario": "PATCH chronological inversion: endDate < startDate",
        "input": "PATCH holiday with startDate: 2027-02-25, endDate: 2027-02-22",
        "expected": "HTTP 400 Cit.Attendance:1705 (reason: 'endDate-before-startDate').",
        "pri": "P0",
        "type": "negative"
    },
    {
        "id": "HC-DTO-109",
        "section": "H. PATCH /{id}/{year} - Date Component & Chronological Boundaries",
        "scenario": "PATCH holiday date year mismatch with calendar year",
        "input": "PATCH 2027 calendar with a holiday dated 2026-12-31",
        "expected": "HTTP 400 Cit.Attendance:1705 ('Holiday date year must match selected calendar year.')",
        "pri": "P0",
        "type": "negative"
    },
    {
        "id": "HC-DTO-110",
        "section": "H. PATCH /{id}/{year} - Date Component & Chronological Boundaries",
        "scenario": "PATCH current year past holiday (startDate < Today)",
        "input": "PATCH Current Year calendar with holiday dated yesterday or earlier",
        "expected": "HTTP 400 Cit.Attendance:1706 ('For current year updates, holiday dates must be future dates.')",
        "pri": "P0",
        "type": "negative"
    },
    {
        "id": "HC-DTO-111",
        "section": "H. PATCH /{id}/{year} - Date Component & Chronological Boundaries",
        "scenario": "PATCH current year future holiday (startDate > Today)",
        "input": "PATCH Current Year calendar with holiday dated today + 10 days",
        "expected": "HTTP 200 OK. Holiday added/updated successfully.",
        "pri": "P1",
        "type": "positive"
    },

    # Section I: PATCH /{id}/{year} - Holiday Collision, Overlap & Duplicate Validation
    {
        "id": "HC-DTO-112",
        "section": "I. PATCH /{id}/{year} - Holiday Collision, Overlap & Duplicate Validation",
        "scenario": "Adding new holiday with duplicate startDate of existing holiday",
        "input": "PATCH to add a new holiday with startDate matching an existing holiday on calendar",
        "expected": "HTTP 400 Cit.Attendance:1707 ('Duplicate holiday date found in the calendar.') Calendar NOT changed.",
        "pri": "P0",
        "type": "negative"
    },
    {
        "id": "HC-DTO-113",
        "section": "I. PATCH /{id}/{year} - Holiday Collision, Overlap & Duplicate Validation",
        "scenario": "Adding new holiday overlapping existing multi-day holiday range",
        "input": "Existing holiday: Oct 10-15. New holiday: Oct 12-18",
        "expected": "HTTP 400 Cit.Attendance:1707 (reason: 'date-range-overlap'). Calendar NOT changed.",
        "pri": "P0",
        "type": "negative"
    },
    {
        "id": "HC-DTO-114",
        "section": "I. PATCH /{id}/{year} - Holiday Collision, Overlap & Duplicate Validation",
        "scenario": "Two new holidays in same PATCH payload with overlapping ranges",
        "input": "PATCH payload with New H1: Nov 1-4, New H2: Nov 3-7",
        "expected": "HTTP 400 Cit.Attendance:1707 (reason: 'duplicate-startDate-after-merge').",
        "pri": "P0",
        "type": "negative"
    },
    {
        "id": "HC-DTO-115",
        "section": "I. PATCH /{id}/{year} - Holiday Collision, Overlap & Duplicate Validation",
        "scenario": "Updating existing holiday name/type without altering its non-conflicting dates",
        "input": "PATCH with existing holiday id, new name, same date range",
        "expected": "HTTP 200 OK. Successfully updated without false self-collision error.",
        "pri": "P1",
        "type": "positive"
    },
    {
        "id": "HC-DTO-116",
        "section": "I. PATCH /{id}/{year} - Holiday Collision, Overlap & Duplicate Validation",
        "scenario": "Adjacent holiday ranges without overlap (Boundary test)",
        "input": "Existing holiday: Oct 1-5. New holiday: Oct 6-10",
        "expected": "HTTP 200 OK. Adjacent non-overlapping dates accepted.",
        "pri": "P1",
        "type": "positive"
    },

    # Section J: PATCH /{id}/{year} - Holiday Identity, Upsert & Removal Validations
    {
        "id": "HC-DTO-117",
        "section": "J. PATCH /{id}/{year} - Holiday Identity, Upsert & Removal Validations",
        "scenario": "Upsert - update existing holiday by valid UUID",
        "input": "PATCH with existing holiday id on calendar and modified details",
        "expected": "HTTP 200 'Holiday calendar updated successfully'. Target holiday updated; IsPublished = false.",
        "pri": "P0",
        "type": "smoke"
    },
    {
        "id": "HC-DTO-118",
        "section": "J. PATCH /{id}/{year} - Holiday Identity, Upsert & Removal Validations",
        "scenario": "Upsert - holiday id provided but not found on calendar",
        "input": "PATCH with holiday item holding random UUID not present in calendar",
        "expected": "HTTP 400 Cit.Attendance:1710 ('No holiday exists for the selected date / id').",
        "pri": "P1",
        "type": "negative"
    },
    {
        "id": "HC-DTO-119",
        "section": "J. PATCH /{id}/{year} - Holiday Identity, Upsert & Removal Validations",
        "scenario": "Upsert - holiday id has malformed GUID format",
        "input": "PATCH with holiday item holding 'id': 'invalid-uuid'",
        "expected": "HTTP 400 Bad Request (Sbp:Validation - Holiday id is not a valid GUID).",
        "pri": "P1",
        "type": "negative"
    },
    {
        "id": "HC-DTO-120",
        "section": "J. PATCH /{id}/{year} - Holiday Identity, Upsert & Removal Validations",
        "scenario": "Remove holiday - valid future holiday ID",
        "input": "PATCH /api/companies/{companyId}/holidaylist/{id}/remove/{holidayId}/{year}",
        "expected": "HTTP 200 'Holiday removed successfully'. Holiday deleted; IsPublished = false.",
        "pri": "P0",
        "type": "smoke"
    },
    {
        "id": "HC-DTO-121",
        "section": "J. PATCH /{id}/{year} - Holiday Identity, Upsert & Removal Validations",
        "scenario": "Remove holiday - past holiday on current year calendar",
        "input": "PATCH /remove/{pastHolidayId}/{currentYear} where holiday startDate < Today",
        "expected": "HTTP 400 Cit.Attendance:1709 ('Past holidays cannot be removed. Only today or future holidays are allowed.')",
        "pri": "P0",
        "type": "negative"
    },
    {
        "id": "HC-DTO-122",
        "section": "J. PATCH /{id}/{year} - Holiday Identity, Upsert & Removal Validations",
        "scenario": "Remove holiday - unknown holidayId not on calendar",
        "input": "PATCH /remove/{randomHolidayId}/{year}",
        "expected": "HTTP 400 Cit.Attendance:1710 ('No holiday exists for the selected date.')",
        "pri": "P1",
        "type": "negative"
    },
    {
        "id": "HC-DTO-123",
        "section": "J. PATCH /{id}/{year} - Holiday Identity, Upsert & Removal Validations",
        "scenario": "Remove holiday - malformed holidayId GUID in route",
        "input": "PATCH /remove/bad-guid-123/{year}",
        "expected": "HTTP 400 Bad Request (Sbp:Validation - Route parameter holidayId is not a valid GUID).",
        "pri": "P1",
        "type": "negative"
    },
    {
        "id": "HC-DTO-124",
        "section": "J. PATCH /{id}/{year} - Holiday Identity, Upsert & Removal Validations",
        "scenario": "Edit holiday on Inherited Location Calendar (IsInherited == true)",
        "input": "PATCH /holidaylist/{locCalId}/{year}?locationId={locId} on inherited calendar",
        "expected": "HTTP 400 Cit.Attendance:1714 ('This location follows the company holidays. Customise it before editing.')",
        "pri": "P0",
        "type": "negative"
    },
    {
        "id": "HC-DTO-125",
        "section": "J. PATCH /{id}/{year} - Holiday Identity, Upsert & Removal Validations",
        "scenario": "Remove holiday on Inherited Location Calendar (IsInherited == true)",
        "input": "PATCH /holidaylist/{locCalId}/remove/{holidayId}/{year}?locationId={locId} on inherited calendar",
        "expected": "HTTP 400 Cit.Attendance:1714 ('This location follows the company holidays. Customise it before editing.')",
        "pri": "P0",
        "type": "negative"
    },

    # Section K: K. GUID Validation - companyId (Route, Query, Header, Malformed & Scoping)
    {
        "id": "HC-DTO-126",
        "section": "K. GUID Validation - companyId (Route, Query, Header, Malformed & Scoping)",
        "scenario": "Valid companyId GUID in Route",
        "input": "POST /api/companies/c0000000-0000-0000-0000-000000000001/holidaylist with valid body",
        "expected": "HTTP 200 OK. Route companyId resolved successfully; calendar created.",
        "pri": "P0",
        "type": "smoke"
    },
    {
        "id": "HC-DTO-127",
        "section": "K. GUID Validation - companyId (Route, Query, Header, Malformed & Scoping)",
        "scenario": "Malformed companyId GUID in Route - non-hex characters",
        "input": "POST /api/companies/zzzzzzzz-zzzz-zzzz-zzzz-zzzzzzzzzzzz/holidaylist",
        "expected": "HTTP 400 Bad Request (Sbp:Validation - Route parameter companyId is not a valid GUID).",
        "pri": "P0",
        "type": "negative"
    },
    {
        "id": "HC-DTO-128",
        "section": "K. GUID Validation - companyId (Route, Query, Header, Malformed & Scoping)",
        "scenario": "Malformed companyId GUID in Route - missing hyphens (32-char hex string)",
        "input": "POST /api/companies/c0000000000000000000000000000001/holidaylist",
        "expected": "HTTP 400 Bad Request (Strict UUID format required with hyphens).",
        "pri": "P0",
        "type": "negative"
    },
    {
        "id": "HC-DTO-129",
        "section": "K. GUID Validation - companyId (Route, Query, Header, Malformed & Scoping)",
        "scenario": "Malformed companyId GUID in Route - truncated / invalid length (35 chars)",
        "input": "POST /api/companies/c0000000-0000-0000-0000-00000000000/holidaylist",
        "expected": "HTTP 400 Bad Request (Sbp:Validation - Company ID length invalid).",
        "pri": "P1",
        "type": "negative"
    },
    {
        "id": "HC-DTO-130",
        "section": "K. GUID Validation - companyId (Route, Query, Header, Malformed & Scoping)",
        "scenario": "Empty GUID companyId in Route (Guid.Empty)",
        "input": "POST /api/companies/00000000-0000-0000-0000-000000000000/holidaylist",
        "expected": "HTTP 400 Bad Request (Sbp:Validation - Company ID cannot be empty GUID).",
        "pri": "P0",
        "type": "negative"
    },
    {
        "id": "HC-DTO-131",
        "section": "K. GUID Validation - companyId (Route, Query, Header, Malformed & Scoping)",
        "scenario": "companyId passed as Query parameter instead of Route parameter",
        "input": "POST /api/companies/holidaylist?companyId=c0000000-0000-0000-0000-000000000001",
        "expected": "HTTP 404 Not Found (Missing mandatory route parameter {companyId}).",
        "pri": "P1",
        "type": "negative"
    },
    {
        "id": "HC-DTO-132",
        "section": "K. GUID Validation - companyId (Route, Query, Header, Malformed & Scoping)",
        "scenario": "companyId passed in Query parameter conflicting with Route companyId",
        "input": "POST /api/companies/{companyA}/holidaylist?companyId={companyB}",
        "expected": "Route parameter {companyA} strictly governs execution; query parameter is ignored or HTTP 400.",
        "pri": "P1",
        "type": "negative"
    },
    {
        "id": "HC-DTO-133",
        "section": "K. GUID Validation - companyId (Route, Query, Header, Malformed & Scoping)",
        "scenario": "companyId passed via header X-Company-Id mismatching Route companyId",
        "input": "Header: X-Company-Id: {companyB}, Route: /api/companies/{companyA}/holidaylist",
        "expected": "Route companyId {companyA} strictly enforced; cross-company write prevented.",
        "pri": "P1",
        "type": "negative"
    },
    {
        "id": "HC-DTO-134",
        "section": "K. GUID Validation - companyId (Route, Query, Header, Malformed & Scoping)",
        "scenario": "Non-existent companyId GUID (syntactically valid but unknown in Company Service)",
        "input": "POST /api/companies/ffffffff-ffff-ffff-ffff-ffffffffffff/holidaylist",
        "expected": "HTTP 400 Cit.Attendance:1701 ('Holiday calendar not found' / company service lookup failed).",
        "pri": "P0",
        "type": "negative"
    },
    {
        "id": "HC-DTO-135",
        "section": "K. GUID Validation - companyId (Route, Query, Header, Malformed & Scoping)",
        "scenario": "Cross-tenant companyId GUID (Company belongs to Tenant B, JWT is Tenant A)",
        "input": "POST /api/companies/{companyOfTenantB}/holidaylist with Tenant A token",
        "expected": "HTTP 403 Forbidden ('Cross-tenant access is not allowed.').",
        "pri": "P0",
        "type": "negative"
    },

    # Section L: L. GUID Validation - holidayId & holidayType (Route, Body, Query & Scoping)
    {
        "id": "HC-DTO-136",
        "section": "L. GUID Validation - holidayId & holidayType (Route, Body, Query & Scoping)",
        "scenario": "Valid holidayId GUID in Route for holiday removal",
        "input": "PATCH /api/companies/{companyId}/holidaylist/{id}/remove/{validHolidayGuid}/{year}",
        "expected": "HTTP 200 OK ('Holiday removed successfully'). Target holiday removed from calendar.",
        "pri": "P0",
        "type": "smoke"
    },
    {
        "id": "HC-DTO-137",
        "section": "L. GUID Validation - holidayId & holidayType (Route, Body, Query & Scoping)",
        "scenario": "Malformed holidayId GUID in Route - non-hex characters",
        "input": "PATCH /api/companies/{companyId}/holidaylist/{id}/remove/not-a-valid-uuid-here/{year}",
        "expected": "HTTP 400 Bad Request (Sbp:Validation - Route parameter holidayId is not a valid GUID).",
        "pri": "P0",
        "type": "negative"
    },
    {
        "id": "HC-DTO-138",
        "section": "L. GUID Validation - holidayId & holidayType (Route, Body, Query & Scoping)",
        "scenario": "Malformed holidayId GUID in Route - truncated / invalid length",
        "input": "PATCH /api/companies/{companyId}/holidaylist/{id}/remove/66666666-6666-6666/{year}",
        "expected": "HTTP 400 Bad Request (Sbp:Validation - Holiday ID is not a valid GUID).",
        "pri": "P1",
        "type": "negative"
    },
    {
        "id": "HC-DTO-139",
        "section": "L. GUID Validation - holidayId & holidayType (Route, Body, Query & Scoping)",
        "scenario": "Empty GUID holidayId in Route (Guid.Empty)",
        "input": "PATCH /api/companies/{companyId}/holidaylist/{id}/remove/00000000-0000-0000-0000-000000000000/{year}",
        "expected": "HTTP 400 Bad Request (Sbp:Validation - Holiday ID cannot be empty GUID).",
        "pri": "P0",
        "type": "negative"
    },
    {
        "id": "HC-DTO-140",
        "section": "L. GUID Validation - holidayId & holidayType (Route, Body, Query & Scoping)",
        "scenario": "holidayId passed as Query parameter instead of Route parameter",
        "input": "PATCH /api/companies/{companyId}/holidaylist/{id}/remove?holidayId={guid}",
        "expected": "HTTP 404 Not Found (Missing mandatory route parameter {holidayId}).",
        "pri": "P1",
        "type": "negative"
    },
    {
        "id": "HC-DTO-141",
        "section": "L. GUID Validation - holidayId & holidayType (Route, Body, Query & Scoping)",
        "scenario": "Unknown / Non-existent holidayId GUID on calendar",
        "input": "PATCH /remove/{randomGuid}/{year} where randomGuid is not on target calendar",
        "expected": "HTTP 400 Cit.Attendance:1710 ('No holiday exists for the selected date.').",
        "pri": "P0",
        "type": "negative"
    },
    {
        "id": "HC-DTO-142",
        "section": "L. GUID Validation - holidayId & holidayType (Route, Body, Query & Scoping)",
        "scenario": "Cross-calendar holidayId GUID (Holiday ID exists in Calendar B, sent against Calendar A)",
        "input": "PATCH /remove/{holidayIdOfCalendarB}/{year} against Calendar A",
        "expected": "HTTP 400 Cit.Attendance:1710 ('No holiday exists for the selected date.'). Calendar A unmodified.",
        "pri": "P0",
        "type": "negative"
    },
    {
        "id": "HC-DTO-143",
        "section": "L. GUID Validation - holidayId & holidayType (Route, Body, Query & Scoping)",
        "scenario": "Valid holidayId GUID in PATCH body (holidayLists[].id)",
        "input": "PATCH /{id}/{year} with holiday item holding valid existing holiday UUID",
        "expected": "HTTP 200 OK. Existing holiday entry updated in place; IsPublished = false.",
        "pri": "P0",
        "type": "smoke"
    },
    {
        "id": "HC-DTO-144",
        "section": "L. GUID Validation - holidayId & holidayType (Route, Body, Query & Scoping)",
        "scenario": "Empty GUID id in PATCH body (00000000-0000-0000-0000-000000000000)",
        "input": "PATCH /{id}/{year} with holiday item holding 'id': '00000000-0000-0000-0000-000000000000'",
        "expected": "HTTP 200 OK. Server generates fresh UUID and appends holiday as new item.",
        "pri": "P1",
        "type": "positive"
    },
    {
        "id": "HC-DTO-145",
        "section": "L. GUID Validation - holidayId & holidayType (Route, Body, Query & Scoping)",
        "scenario": "Malformed holiday id string in PATCH body",
        "input": "PATCH /{id}/{year} with holiday item holding 'id': 'invalid-uuid-xyz'",
        "expected": "HTTP 400 Bad Request (Sbp:Validation - Holiday id is not a valid GUID).",
        "pri": "P0",
        "type": "negative"
    },
    {
        "id": "HC-DTO-146",
        "section": "L. GUID Validation - holidayId & holidayType (Route, Body, Query & Scoping)",
        "scenario": "Malformed holidayType._id GUID in payload body",
        "input": "POST / PATCH with holidayType: {'_id': 'invalid-type-uuid-999'}",
        "expected": "HTTP 400 Bad Request (Sbp:Validation - Holiday type ID is not a valid GUID).",
        "pri": "P0",
        "type": "negative"
    },
    {
        "id": "HC-DTO-147",
        "section": "L. GUID Validation - holidayId & holidayType (Route, Body, Query & Scoping)",
        "scenario": "Empty GUID holidayType._id in payload body",
        "input": "POST / PATCH with holidayType: {'_id': '00000000-0000-0000-0000-000000000000'}",
        "expected": "HTTP 400 Bad Request (Sbp:Validation - Holiday type ID cannot be empty GUID).",
        "pri": "P0",
        "type": "negative"
    },
    {
        "id": "HC-DTO-148",
        "section": "L. GUID Validation - holidayId & holidayType (Route, Body, Query & Scoping)",
        "scenario": "Non-existent holidayType._id GUID (Valid UUID not in Company Service)",
        "input": "POST / PATCH with holidayType: {'_id': '77777777-7777-7777-7777-777777777777'}",
        "expected": "HTTP 400 Bad Request ('Holiday type not found in Company Service.').",
        "pri": "P1",
        "type": "negative"
    },

    # Section M: M. GUID Validation - Query & Header Parameters (locationId, TenantId & Correlation)
    {
        "id": "HC-DTO-149",
        "section": "M. GUID Validation - Query & Header Parameters (locationId, TenantId & Correlation)",
        "scenario": "Valid locationId GUID in Query parameter",
        "input": "POST /api/companies/{companyId}/holidaylist?locationId={validLocationGuid}",
        "expected": "HTTP 200 OK. Location-specific calendar created (CalendarType: 2, IsInherited: false).",
        "pri": "P0",
        "type": "smoke"
    },
    {
        "id": "HC-DTO-150",
        "section": "M. GUID Validation - Query & Header Parameters (locationId, TenantId & Correlation)",
        "scenario": "Malformed locationId GUID in Query parameter",
        "input": "POST /api/companies/{companyId}/holidaylist?locationId=bad-location-guid-123",
        "expected": "HTTP 400 Bad Request (Sbp:Validation - Query parameter locationId is not a valid GUID).",
        "pri": "P0",
        "type": "negative"
    },
    {
        "id": "HC-DTO-151",
        "section": "M. GUID Validation - Query & Header Parameters (locationId, TenantId & Correlation)",
        "scenario": "Empty GUID locationId in Query parameter (00000000-0000-0000-0000-000000000000)",
        "input": "POST /api/companies/{companyId}/holidaylist?locationId=00000000-0000-0000-0000-000000000000",
        "expected": "HTTP 400 Bad Request (Sbp:Validation - Location ID cannot be empty GUID) or treated as company default.",
        "pri": "P1",
        "type": "negative"
    },
    {
        "id": "HC-DTO-152",
        "section": "M. GUID Validation - Query & Header Parameters (locationId, TenantId & Correlation)",
        "scenario": "Foreign locationId GUID (Location belonging to another company)",
        "input": "POST /api/companies/{companyA}/holidaylist?locationId={locationOfCompanyB}",
        "expected": "HTTP 400 Cit.Attendance:1701 (reason: 'location-not-found-on-company').",
        "pri": "P0",
        "type": "negative"
    },
    {
        "id": "HC-DTO-153",
        "section": "M. GUID Validation - Query & Header Parameters (locationId, TenantId & Correlation)",
        "scenario": "Bearer Token Header - Malformed tenantId claim GUID",
        "input": "POST with Authorization Bearer JWT having tenantId: 'not-a-valid-guid'",
        "expected": "HTTP 401 / 403 SbpAuthorizationException ('Tenant ID was not resolved.').",
        "pri": "P0",
        "type": "negative"
    },
    {
        "id": "HC-DTO-154",
        "section": "M. GUID Validation - Query & Header Parameters (locationId, TenantId & Correlation)",
        "scenario": "Bearer Token Header - Empty tenantId claim GUID (Guid.Empty)",
        "input": "POST with Authorization Bearer JWT having tenantId: '00000000-0000-0000-0000-000000000000'",
        "expected": "HTTP 401 / 403 SbpAuthorizationException ('Tenant ID was not resolved.').",
        "pri": "P0",
        "type": "negative"
    },
    {
        "id": "HC-DTO-155",
        "section": "M. GUID Validation - Query & Header Parameters (locationId, TenantId & Correlation)",
        "scenario": "Custom Header - X-Correlation-Id with valid GUID",
        "input": "Header: X-Correlation-Id: 99999999-9999-9999-9999-999999999999",
        "expected": "HTTP 200 OK. Correlation ID tracked in logs and echoed back in response header.",
        "pri": "P2",
        "type": "positive"
    },
    {
        "id": "HC-DTO-156",
        "section": "M. GUID Validation - Query & Header Parameters (locationId, TenantId & Correlation)",
        "scenario": "Custom Header - X-Correlation-Id with malformed GUID string",
        "input": "Header: X-Correlation-Id: 'corrupted-guid@#$'",
        "expected": "HTTP 200 or 400. Server safely sanitizes or ignores; must NOT throw unhandled 500 error.",
        "pri": "P2",
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
    
    ws.row_dimensions[row_idx].height = 24
    
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
    2: 36, # Section
    3: 45, # Test Scenario
    4: 55, # Input / Preconditions
    5: 55, # Expected Result
    6: 8,  # Pri
    7: 12, # Type
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

# Find row for Holiday Calendar - DTO and TOTAL
hc_dto_row = None
total_row = None

for r in range(5, ws_idx.max_row + 1):
    val_c1 = str(ws_idx.cell(r, 1).value).strip() if ws_idx.cell(r, 1).value is not None else ""
    val_c2 = str(ws_idx.cell(r, 2).value).strip() if ws_idx.cell(r, 2).value is not None else ""
    
    if val_c2 == sheet_name:
        hc_dto_row = r
    elif val_c1.upper() == 'TOTAL':
        total_row = r

print(f"Holiday Calendar - DTO row in INDEX: {hc_dto_row}, TOTAL row: {total_row}")

if hc_dto_row:
    ws_idx.cell(hc_dto_row, 3).value = len(test_cases)
    ws_idx.cell(hc_dto_row, 4).value = p0_cnt
    ws_idx.cell(hc_dto_row, 5).value = p1_cnt
    ws_idx.cell(hc_dto_row, 6).value = p2_cnt
    ws_idx.cell(hc_dto_row, 7).value = p3_cnt
    ws_idx.cell(hc_dto_row, 8).value = "POST & PATCH DTO Validations, GUID Parameters (Company, Holiday, Location, Headers), Min/Max Characters & Dates"

# Recalculate TOTAL row
if total_row:
    tot_tcs = sum(ws_idx.cell(r, 3).value for r in range(5, total_row) if isinstance(ws_idx.cell(r, 3).value, int))
    tot_p0 = sum(ws_idx.cell(r, 4).value for r in range(5, total_row) if isinstance(ws_idx.cell(r, 4).value, int))
    tot_p1 = sum(ws_idx.cell(r, 5).value for r in range(5, total_row) if isinstance(ws_idx.cell(r, 5).value, int))
    tot_p2 = sum(ws_idx.cell(r, 6).value for r in range(5, total_row) if isinstance(ws_idx.cell(r, 6).value, int))
    tot_p3 = sum(ws_idx.cell(r, 7).value for r in range(5, total_row) if isinstance(ws_idx.cell(r, 7).value, int))

    ws_idx.cell(total_row, 3).value = tot_tcs
    ws_idx.cell(total_row, 4).value = tot_p0
    ws_idx.cell(total_row, 5).value = tot_p1
    ws_idx.cell(total_row, 6).value = tot_p2
    ws_idx.cell(total_row, 7).value = tot_p3
    ws_idx.cell(total_row, 8).value = "Master Consolidated Suite with Active User Scenarios & Holiday Calendar DTO Validations (including GUID & Headers)"

    print(f"Updated INDEX sheet:")
    print(f"  Row {hc_dto_row}: Module 16 ({sheet_name}) -> Total: {len(test_cases)} (P0:{p0_cnt}, P1:{p1_cnt}, P2:{p2_cnt}, P3:{p3_cnt})")
    print(f"  Row {total_row}: Grand Total -> Total: {tot_tcs} (P0:{tot_p0}, P1:{tot_p1}, P2:{tot_p2}, P3:{tot_p3})")

# Save workbook
wb.save('AttendanceTestCases_Master_Consolidated.xlsx')
print("Successfully updated AttendanceTestCases_Master_Consolidated.xlsx!")
