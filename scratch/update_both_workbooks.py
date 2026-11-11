# -*- coding: utf-8 -*-
"""
Creates and updates both:
1. CompanyDefault_DTO_Validation_TestCases.xlsx (Dedicated Standalone Workbook)
   - Sheet 1 (Active / Opens by Default): 'CDWT DTO Validations'
   - Formatted as an official Excel Table with native AutoFilter buttons on every column header
   - In-cell DataValidation dropdown on Column K: Pending, Pass, Failed, Backlog, Noted
   - Sheet 2: 'SUMMARY' KPI Dashboard
2. AttendanceTestCases_Master_Consolidated.xlsx (Master Consolidated Workbook)
   - Adds 'CDWT - Manual DTO Validations' sheet so user can test inside master workbook too!
"""

import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.datavalidation import DataValidation
from openpyxl.worksheet.table import Table, TableStyleInfo

# Define all 52 DTO test cases
cases_data = [
    # Category 1: Route, Headers & Authorization
    (
        "CDWT-DTO-01", "1. Route & Security", "All Types", "Authorization",
        "Missing Authorization header in request",
        "POST", "/api/companies/{companyId}/worktemplates/fixed",
        "{}", "HTTP 401 Unauthorized", "P0", "Pending", "", "", "Cleanly enforced by API Gateway"
    ),
    (
        "CDWT-DTO-02", "1. Route & Security", "All Types", "Authorization",
        "Expired or forged Bearer token",
        "POST", "/api/companies/{companyId}/worktemplates/fixed",
        "{}", "HTTP 401 Unauthorized", "P0", "Pending", "", "", "Cleanly enforced"
    ),
    (
        "CDWT-DTO-03", "1. Route & Security", "All Types", "__tenant",
        "JWT token missing tenant claim",
        "POST", "/api/companies/{companyId}/worktemplates/fixed",
        "{}", "HTTP 401 / 403 SbpAuthorizationException", "P0", "Pending", "", "", "Cleanly enforced"
    ),
    (
        "CDWT-DTO-04", "1. Route & Security", "All Types", "__tenant",
        "Client tenant spoofing attempt via header",
        "POST", "/api/companies/{companyId}/worktemplates/fixed",
        "Header: __tenant: MaliciousTenant", "Header ignored; token claims enforced", "P1", "Pending", "", "", "Cleanly enforced"
    ),
    (
        "CDWT-DTO-05", "1. Route & Security", "All Types", "companyId (Route)",
        "Zero GUID companyId in route parameter",
        "GET", "/api/companies/00000000-0000-0000-0000-000000000000/worktemplates",
        "None", "HTTP 404 Company Not Found", "P2", "Pending", "", "", "DEFECT-20261028-04: Returns HTTP 200 []"
    ),
    (
        "CDWT-DTO-06", "1. Route & Security", "All Types", "companyId (Route)",
        "Malformed non-hex companyId in route",
        "POST", "/api/companies/invalid-company-guid/worktemplates/fixed",
        "{}", "HTTP 400 Bad Request", "P1", "Pending", "", "", "Route constraint parsing"
    ),
    (
        "CDWT-DTO-07", "1. Route & Security", "All Types", "companyId (Route)",
        "Cross-company tenant boundary access",
        "PATCH", "/api/companies/{companyA}/worktemplates/fixed/{templateOfCompanyB}",
        "{}", "HTTP 400 Cit.Attendance:9001", "P0", "Pending", "", "", "Strict company scoping enforced"
    ),

    # Category 2: Top-Level DTO Validations
    (
        "CDWT-DTO-08", "2. Common DTO", "All Types", "Request Body",
        "Empty JSON payload body ({}) on POST",
        "POST", "/api/companies/{companyId}/worktemplates/fixed",
        "{}", "HTTP 400 Bad Request (Mandatory fields missing)", "P0", "Pending", "", "", "Returns RFC 9110 400 on POST"
    ),
    (
        "CDWT-DTO-09", "2. Common DTO", "All Types", "shortCode",
        "shortCode length below minimum boundary (1 char)",
        "POST", "/api/companies/{companyId}/worktemplates/fixed",
        '{"shortCode": "A", "templateName": {"en": "Test"}, ...}', "HTTP 400 Bad Request", "P1", "Pending", "", "", "Length must be >= 2 characters"
    ),
    (
        "CDWT-DTO-10", "2. Common DTO", "All Types", "shortCode",
        "shortCode contains special symbols / punctuation",
        "POST", "/api/companies/{companyId}/worktemplates/fixed",
        '{"shortCode": "CDW@01!", "templateName": {"en": "Test"}, ...}', "HTTP 400 Bad Request", "P1", "Pending", "", "", "Only alphanumeric characters allowed"
    ),
    (
        "CDWT-DTO-11", "2. Common DTO", "All Types", "shortCode",
        "shortCode length at maximum boundary (30 chars)",
        "POST", "/api/companies/{companyId}/worktemplates/fixed",
        '{"shortCode": "COMPDEF00000000000000000000001", ...}', "HTTP 200 OK (Normalized to upper-case)", "P0", "Pending", "", "", "Valid boundary test"
    ),
    (
        "CDWT-DTO-12", "2. Common DTO", "All Types", "shortCode",
        "shortCode omitted or empty string",
        "POST", "/api/companies/{companyId}/worktemplates/fixed",
        '{"shortCode": "", "templateName": {"en": "Auto Code"}, ...}', "HTTP 200 OK (Auto-generates CDWxxxx)", "P1", "Pending", "", "", "Server auto-generates code"
    ),
    (
        "CDWT-DTO-13", "2. Common DTO", "All Types", "shortCode / CDWT",
        "Attempt to create duplicate Company Default",
        "POST", "/api/companies/{companyId}/worktemplates/fixed",
        '{"shortCode": "FIX002", "templateName": {"en": "Second CDWT"}, ...}', "HTTP 400 Cit.Attendance:1010", "P0", "Pending", "", "", "One-Default Guard enforced"
    ),
    (
        "CDWT-DTO-14", "2. Common DTO", "All Types", "templateName",
        "templateName object omitted or null",
        "POST", "/api/companies/{companyId}/worktemplates/fixed",
        '{"shortCode": "FIX003", "templateName": null, ...}', "HTTP 400 Bad Request", "P0", "Pending", "", "", "Name is mandatory"
    ),
    (
        "CDWT-DTO-15", "2. Common DTO", "All Types", "templateName.en",
        "templateName.en empty string ('')",
        "POST", "/api/companies/{companyId}/worktemplates/fixed",
        '{"shortCode": "FIX004", "templateName": {"en": ""}, ...}', "HTTP 400 Bad Request", "P0", "Pending", "", "", "English name cannot be empty"
    ),
    (
        "CDWT-DTO-16", "2. Common DTO", "All Types", "templateName.ar",
        "Bilingual Arabic UTF-8 name provided",
        "POST", "/api/companies/{companyId}/worktemplates/fixed",
        '{"templateName": {"en": "Standard Default", "ar": "الجدول الافتراضي"}, ...}', "HTTP 200 OK (Persisted byte-exact)", "P1", "Pending", "", "", "Multilingual persistence verified"
    ),
    (
        "CDWT-DTO-17", "2. Common DTO", "All Types", "tenantName",
        "tenantName exposed in client request body",
        "POST", "/api/companies/{companyId}/worktemplates/fixed",
        '{"tenantName": {"en": "ClientTenant"}, ...}', "Field should NOT exist in DTO", "P2", "Pending", "", "", "DEFECT-20261026-04: Exposed in 26 routes"
    ),
    (
        "CDWT-DTO-18", "2. Common DTO", "All Types", "Calendar Invariant",
        "Working Days + Days Off sum does NOT equal 7",
        "POST", "/api/companies/{companyId}/worktemplates/fixed",
        '{"totalWorkingDays": 6, "totalDaysOff": 2, ...}', "HTTP 400 Bad Request (Sum must equal 7)", "P0", "Pending", "", "", "DEFECT-20261028-02: Throws HTTP 500 crash"
    ),

    # Category 3: Fixed Work Template Validations
    (
        "CDWT-DTO-19", "3. Fixed WT", "Fixed", "fixedTimeSlots",
        "Standard 6 Working Days + 1 Day Off schedule",
        "POST", "/api/companies/{companyId}/worktemplates/fixed",
        '{"totalWorkDurationInMinutes": 2880, "totalWorkingDays": 6, "totalDaysOff": 1, "fixedTimeSlots": [7 daily slots]}', "HTTP 200 OK (v1.0 Active CDWT)", "P0", "Pending", "", "", "Happy path CDWT Fixed"
    ),
    (
        "CDWT-DTO-20", "3. Fixed WT", "Fixed", "dayEnum",
        "dayEnum invalid integer value (e.g. 8 or 0)",
        "POST", "/api/companies/{companyId}/worktemplates/fixed",
        '{"fixedTimeSlots": [{"dayEnum": 8, "isWorkingDay": true, ...}]}', "HTTP 400 Bad Request (DayEnum 1..7)", "P0", "Pending", "", "", "DEFECT-20261028-02: Throws HTTP 500 crash"
    ),
    (
        "CDWT-DTO-21", "3. Fixed WT", "Fixed", "dayEnum",
        "Complete 7-day week sequence (Sun=1 to Sat=7)",
        "POST", "/api/companies/{companyId}/worktemplates/fixed",
        '{"fixedTimeSlots": [{"dayEnum": 1}, ..., {"dayEnum": 7}]}', "HTTP 200 OK (All 7 days defined once)", "P0", "Pending", "", "", "Full weekly sequence verified"
    ),
    (
        "CDWT-DTO-22", "3. Fixed WT", "Fixed", "isWorkingDay",
        "Working day contradiction: isWorkingDay=false with duration",
        "POST", "/api/companies/{companyId}/worktemplates/fixed",
        '{"fixedTimeSlots": [{"dayEnum": 6, "isWorkingDay": false, "workDurationInMinutes": 480}]}', "HTTP 400 Bad Request", "P0", "Pending", "", "", "Off day cannot have duration"
    ),
    (
        "CDWT-DTO-23", "3. Fixed WT", "Fixed", "recurrenceOfMonth",
        "Empty recurrence array on an active working day",
        "POST", "/api/companies/{companyId}/worktemplates/fixed",
        '{"fixedTimeSlots": [{"dayEnum": 1, "isWorkingDay": true, "recurrenceOfMonth": []}]}', "HTTP 400 Bad Request", "P1", "Pending", "", "", "Active day requires >= 1 recurrence"
    ),
    (
        "CDWT-DTO-24", "3. Fixed WT", "Fixed", "recurrenceOfMonth",
        "Alternate Saturday Off pattern configuration",
        "POST", "/api/companies/{companyId}/worktemplates/fixed",
        'Fri [1..5]: Off, Sat [1,3,5]: Off, Sat [2,4]: Active (480m)', "HTTP 200 OK", "P1", "Pending", "", "", "Alternate weekend rotation pattern"
    ),
    (
        "CDWT-DTO-25", "3. Fixed WT", "Fixed", "Timings",
        "Temporal Inversion: startTime >= endTime (no overnight)",
        "POST", "/api/companies/{companyId}/worktemplates/fixed",
        '{"startTime": "17:00", "endTime": "09:00", "workDurationInMinutes": 480}', "HTTP 400 Bad Request", "P0", "Pending", "", "", "End time must be after start time"
    ),
    (
        "CDWT-DTO-26", "3. Fixed WT", "Fixed", "Math Consistency",
        "Total duration does not match sum of active daily slots",
        "POST", "/api/companies/{companyId}/worktemplates/fixed",
        '{"totalWorkDurationInMinutes": 2400, sum of daily slots = 2880}', "HTTP 400 Bad Request", "P1", "Pending", "", "", "Mathematical invariant check"
    ),

    # Category 4: Flexible Work Template Validations
    (
        "CDWT-DTO-27", "4. Flexi WT", "Flexible", "flexibleType",
        "flexibleType invalid enum value (e.g. 9 or 0)",
        "POST", "/api/companies/{companyId}/worktemplates/flexi",
        '{"flexibleType": 9, ...}', "HTTP 400 Bad Request (1=Daily, 2=Weekly)", "P0", "Pending", "", "", "DEFECT-20261028-02: Throws HTTP 500 crash"
    ),
    (
        "CDWT-DTO-28", "4. Flexi WT", "Flexible", "flexibleType (Daily)",
        "Standard Daily Flexi Mode configuration",
        "POST", "/api/companies/{companyId}/worktemplates/flexi",
        '{"flexibleType": 1, "totalWorkDurationInMinutes": 2400, daily: 480m}', "HTTP 200 OK (v1.0 Flexi Daily CDWT)", "P0", "Pending", "", "", "Happy path Flexi Daily"
    ),
    (
        "CDWT-DTO-29", "4. Flexi WT", "Flexible", "flexibleType (Weekly)",
        "Standard Weekly Pool Mode configuration",
        "POST", "/api/companies/{companyId}/worktemplates/flexi",
        '{"flexibleType": 2, "totalWorkDurationInMinutes": 2880, daily: 0m}', "HTTP 200 OK (v1.0 Flexi Weekly CDWT)", "P0", "Pending", "", "", "Happy path Flexi Weekly"
    ),
    (
        "CDWT-DTO-30", "4. Flexi WT", "Flexible", "workDurationInMinutes",
        "CRITICAL: Daily duration exceeding 24 hours (1500m / 25h)",
        "POST", "/api/companies/{companyId}/worktemplates/flexi",
        '{"flexibleType": 1, "workDurationInMinutes": 1500}', "HTTP 400 Bad Request (Max 1440 min)", "P0", "Pending", "", "", "DEFECT-20261028-01: Accepted with 200 OK!"
    ),
    (
        "CDWT-DTO-31", "4. Flexi WT", "Flexible", "totalWorkDurationInMinutes",
        "Weekly Pool exceeding 168 hours / week",
        "POST", "/api/companies/{companyId}/worktemplates/flexi",
        '{"flexibleType": 2, "totalWorkDurationInMinutes": 10500}', "HTTP 400 Bad Request (Max 10080 min)", "P0", "Pending", "", "", "Cleanly enforced"
    ),
    (
        "CDWT-DTO-32", "4. Flexi WT", "Flexible", "workDurationInMinutes",
        "Active working day configured with 0 hours",
        "POST", "/api/companies/{companyId}/worktemplates/flexi",
        '{"flexibleType": 1, "isWorkingDay": true, "workDurationInMinutes": 0}', "HTTP 400 Bad Request", "P1", "Pending", "", "", "Active day must have > 0 duration"
    ),
    (
        "CDWT-DTO-33", "4. Flexi WT", "Flexible", "workDurationInMinutes",
        "Negative work duration (< 0 minutes)",
        "POST", "/api/companies/{companyId}/worktemplates/flexi",
        '{"workDurationInMinutes": -480}', "HTTP 400 Bad Request", "P0", "Pending", "", "", "Cleanly enforced"
    ),
    (
        "CDWT-DTO-34", "4. Flexi WT", "Flexible", "Contradiction",
        "Weekly mode with non-zero daily durations assigned",
        "POST", "/api/companies/{companyId}/worktemplates/flexi",
        '{"flexibleType": 2, daily "workDurationInMinutes": 480}', "HTTP 400 Bad Request", "P1", "Pending", "", "", "Weekly mode requires daily duration = 0"
    ),

    # Category 5: Split Work Template Validations
    (
        "CDWT-DTO-35", "5. Split WT", "Split", "splitTimeSlots",
        "Standard 2-Interval Split Shift configuration",
        "POST", "/api/companies/{companyId}/worktemplates/split",
        'Slot 1: 08:00–12:00 (4h), Slot 2: 16:00–20:00 (4h), Break: 4h', "HTTP 200 OK (v1.0 Split CDWT)", "P0", "Pending", "", "", "Happy path Split Shift"
    ),
    (
        "CDWT-DTO-36", "5. Split WT", "Split", "intervals",
        "Contiguous intervals / Zero break gap",
        "POST", "/api/companies/{companyId}/worktemplates/split",
        'Slot 1: 08:00–12:00, Slot 2: 12:00–16:00 (Break Gap = 0 min)', "HTTP 400 Bad Request (Must have break gap)", "P0", "Pending", "", "", "DEFECT-20261028-02: Throws HTTP 500 crash"
    ),
    (
        "CDWT-DTO-37", "5. Split WT", "Split", "intervals",
        "Negative / zero break gap between intervals",
        "POST", "/api/companies/{companyId}/worktemplates/split",
        'Slot 1: 08:00–12:00, Slot 2: 11:30–15:30', "HTTP 400 Bad Request", "P0", "Pending", "", "", "DEFECT-20261028-02: Throws HTTP 500 crash"
    ),
    (
        "CDWT-DTO-38", "5. Split WT", "Split", "intervals",
        "Overlapping interval time ranges",
        "POST", "/api/companies/{companyId}/worktemplates/split",
        'Slot 1: 08:00–13:00, Slot 2: 12:00–17:00 (Overlap = 1h)', "HTTP 400 Bad Request", "P0", "Pending", "", "", "DEFECT-20261028-02: Throws HTTP 500 crash"
    ),
    (
        "CDWT-DTO-39", "5. Split WT", "Split", "intervals",
        "Inverted Start/End Timings in a split interval",
        "POST", "/api/companies/{companyId}/worktemplates/split",
        'Slot 1: startTime: "12:00", endTime: "08:00"', "HTTP 400 Bad Request", "P0", "Pending", "", "", "DEFECT-20261028-01: Accepted with 200 OK"
    ),
    (
        "CDWT-DTO-40", "5. Split WT", "Split", "isWorkingDay",
        "Active intervals configured on a Day Off",
        "POST", "/api/companies/{companyId}/worktemplates/split",
        'isWorkingDay: false, but timeSlots contains active intervals', "HTTP 400 Bad Request", "P0", "Pending", "", "", "DEFECT-20261028-02: Throws HTTP 500 crash"
    ),

    # Category 6: PATCH Validations & Immutability Locks
    (
        "CDWT-DTO-41", "6. PATCH & Immutability", "All Types", "Request Body",
        "CRITICAL: Empty JSON payload body ({}) on PATCH",
        "PATCH", "/api/companies/{companyId}/worktemplates/{type}/{id}",
        "{}", "HTTP 400 Bad Request (At least one field required)", "P0", "Pending", "", "", "DEFECT-20261028-02: Crashes with HTTP 500!"
    ),
    (
        "CDWT-DTO-42", "6. PATCH & Immutability", "All Types", "shortCode",
        "Attempt to mutate shortCode via PATCH",
        "PATCH", "/api/companies/{companyId}/worktemplates/{type}/{id}",
        '{"shortCode": "HACKCODE"}', "HTTP 400 Cit.Attendance:1107", "P0", "Pending", "", "", "ShortCode strictly locked after create"
    ),
    (
        "CDWT-DTO-43", "6. PATCH & Immutability", "All Types", "companyId",
        "Attempt to reassign entity to another company via PATCH",
        "PATCH", "/api/companies/{companyId}/worktemplates/{type}/{id}",
        '{"companyId": "<other-company-guid>"}', "Ignored or HTTP 400 Cit.Attendance:9001", "P0", "Pending", "", "", "Cross-company immutability enforced"
    ),
    (
        "CDWT-DTO-44", "6. PATCH & Immutability", "All Types", "tenantName",
        "Attempt to spoof tenantName via PATCH",
        "PATCH", "/api/companies/{companyId}/worktemplates/{type}/{id}",
        '{"tenantName": {"en": "SpoofedTenant"}}', "Reject or Ignore client value", "P2", "Pending", "", "", "DEFECT-20261026-04: Server accepts value"
    ),
    (
        "CDWT-DTO-45", "6. PATCH & Immutability", "All Types", "{id} (Route)",
        "Attempt to edit an archived / superseded version ID",
        "PATCH", "/api/companies/{companyId}/worktemplates/{type}/{archivedId}",
        '{"templateName": {"en": "Edit Archived"}}', "HTTP 400 Cit.Attendance:1107", "P1", "Pending", "", "", "Archived versions are protected"
    ),
    (
        "CDWT-DTO-46", "6. PATCH & Immutability", "All Types", "{id} (Route)",
        "Attempt to edit a non-existent template GUID",
        "PATCH", "/api/companies/{companyId}/worktemplates/{type}/{fakeGuid}",
        '{"templateName": {"en": "Non-Existent"}}', "HTTP 400 Cit.Attendance:1101", "P1", "Pending", "", "", "Entity not found"
    ),
    (
        "CDWT-DTO-47", "6. PATCH & Immutability", "Fixed", "Timings",
        "Valid In-Place Timing Shift on Thursday",
        "PATCH", "/api/companies/{companyId}/worktemplates/fixed/{activeId}",
        'Thursday shift updated from 08:00 to 09:00', "HTTP 200 OK (Creates v2.0, archives v1.0)", "P0", "Pending", "", "", "Happy path in-place edit"
    ),
    (
        "CDWT-DTO-48", "6. PATCH & Immutability", "Fixed -> Flexi", "Type Migration",
        "Migrate Company Default from Fixed to Flexible Daily",
        "PATCH", "/api/companies/{companyId}/worktemplates/fixed/{activeId}",
        '{"flexibleType": 1, "flexiTimeSlots": [7 slots]}', "HTTP 200 OK (Creates v2.0 Flexi CDWT)", "P0", "Pending", "", "", "Happy path Fixed to Flexi migration"
    ),
    (
        "CDWT-DTO-49", "6. PATCH & Immutability", "Fixed -> Split", "Type Migration",
        "Migrate Company Default from Fixed to Split Shift",
        "PATCH", "/api/companies/{companyId}/worktemplates/fixed/{activeId}",
        '{"splitTimeSlots": [7 split slots]}', "HTTP 200 OK (Creates v2.0 Split CDWT)", "P0", "Pending", "", "", "Happy path Fixed to Split migration"
    ),
    (
        "CDWT-DTO-50", "6. PATCH & Immutability", "All Types", "Type Migration Guard",
        "Attempt to migrate Company Default to Roster / Rotation",
        "PATCH", "/api/companies/{companyId}/worktemplates/{type}/{activeId}",
        'Payload attempting to convert to Roster or Rotation', "HTTP 400 Bad Request (Blocked for CDWT)", "P1", "Pending", "", "", "CDWT can only be Fixed, Flexi, Split"
    ),
    (
        "CDWT-DTO-51", "6. PATCH & Immutability", "All Types", "Archive Guard",
        "Attempt to archive active Company Default Work Template",
        "PATCH", "/api/companies/{companyId}/worktemplates/{activeId}/archive",
        "None", "HTTP 400 Cit.Attendance:1202", "P1", "Pending", "", "", "DEFECT-20261028-03: Accepted with 200 OK!"
    ),
    (
        "CDWT-DTO-52", "6. PATCH & Immutability", "All Types", "Delete Guard",
        "Attempt to soft-delete active Company Default Work Template",
        "PATCH", "/api/companies/{companyId}/worktemplates/{activeId}/delete",
        "None", "HTTP 400 Cit.Attendance:1202", "P1", "Pending", "", "", "DEFECT-20261028-03: Accepted with 200 OK!"
    )
]

def build_cases_sheet(ws):
    ws.views.sheetView[0].showGridLines = True

    navy_header = PatternFill(start_color="1F4E79", end_color="1F4E79", fill_type="solid")
    font_header = Font(name="Calibri", size=11, bold=True, color="FFFFFF")
    font_bold = Font(name="Calibri", size=10, bold=True)
    font_regular = Font(name="Calibri", size=10)
    font_code = Font(name="Consolas", size=9)
    user_input_fill = PatternFill(start_color="FFF2CC", end_color="FFF2CC", fill_type="solid")
    
    border_thin = Border(
        left=Side(style='thin', color='D9D9D9'),
        right=Side(style='thin', color='D9D9D9'),
        top=Side(style='thin', color='D9D9D9'),
        bottom=Side(style='thin', color='D9D9D9')
    )

    headers = [
        "TC ID", "Category", "Template Type", "Field Under Test",
        "Test Scenario / Edge Case", "HTTP Method", "Endpoint Route",
        "Sample Request Payload (JSON)", "Expected HTTP & Code", "Pri",
        "Manual Status", "Actual HTTP Code", "Actual Server Response / Notes",
        "Known Defect / QA Reference"
    ]
    
    ws.append(headers)
    for col_idx in range(1, len(headers) + 1):
        cell = ws.cell(1, col_idx)
        cell.font = font_header
        cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
        if col_idx in [11, 12, 13]:
            cell.fill = PatternFill(start_color="C65911", end_color="C65911", fill_type="solid")
        else:
            cell.fill = navy_header
    ws.row_dimensions[1].height = 28

    for row_idx, item in enumerate(cases_data, start=2):
        for col_idx, val in enumerate(item, start=1):
            cell = ws.cell(row_idx, col_idx)
            cell.value = val
            cell.border = border_thin
            cell.font = font_regular
            cell.alignment = Alignment(vertical="center", wrap_text=True)
            
            if col_idx == 1:
                cell.font = font_bold
                cell.alignment = Alignment(horizontal="center", vertical="center")
            elif col_idx in [6, 10, 11, 12]:
                cell.alignment = Alignment(horizontal="center", vertical="center")
            elif col_idx == 8:
                cell.font = font_code
            
            if col_idx in [11, 12, 13]:
                cell.fill = user_input_fill

        ws.row_dimensions[row_idx].height = 24

    # Add In-Cell Dropdown DataValidation on Column K (sqref="K2:K53")
    # Exact requested options: Pending, Pass, Failed, Backlog, Noted
    dv = DataValidation(type="list", formula1='"Pending,Pass,Failed,Backlog,Noted"', allow_blank=True)
    dv.showDropDown = None # standard Excel in-cell dropdown
    dv.showErrorMessage = True
    dv.errorTitle = "Invalid Status"
    dv.error = "Please select one of the allowed options: Pending, Pass, Failed, Backlog, Noted"
    dv.showInputMessage = True
    dv.promptTitle = "Manual Status"
    dv.prompt = "Choose from: Pending, Pass, Failed, Backlog, Noted"
    ws.add_data_validation(dv)
    dv.add(f"K2:K{len(cases_data) + 1}")

    # Set explicit AutoFilter on all columns
    ws.auto_filter.ref = f"A1:N{len(cases_data) + 1}"

    # Set Column Widths
    col_widths = {
        1: 15, 2: 22, 3: 16, 4: 20, 5: 38, 6: 12, 7: 38,
        8: 45, 9: 34, 10: 8, 11: 16, 12: 16, 13: 40, 14: 38
    }
    for col_idx, width in col_widths.items():
        ws.column_dimensions[get_column_letter(col_idx)].width = width


# =============================================================
# BUILD 1: Standalone Workbook (CompanyDefault_DTO_Validation_TestCases.xlsx)
# =============================================================
wb_standalone = openpyxl.Workbook()

# Sheet 1 (Active by default): CDWT DTO Validations
ws_cases_std = wb_standalone.active
ws_cases_std.title = "CDWT DTO Validations"
build_cases_sheet(ws_cases_std)

# Sheet 2: SUMMARY
ws_sum_std = wb_standalone.create_sheet(title="SUMMARY")
ws_sum_std.views.sheetView[0].showGridLines = True

navy_header = PatternFill(start_color="1F4E79", end_color="1F4E79", fill_type="solid")
font_title = Font(name="Calibri", size=14, bold=True, color="1F4E79")
font_header = Font(name="Calibri", size=11, bold=True, color="FFFFFF")
font_bold = Font(name="Calibri", size=10, bold=True)
font_regular = Font(name="Calibri", size=10)
user_input_fill = PatternFill(start_color="FFF2CC", end_color="FFF2CC", fill_type="solid")
border_thin = Border(left=Side(style='thin', color='D9D9D9'), right=Side(style='thin', color='D9D9D9'), top=Side(style='thin', color='D9D9D9'), bottom=Side(style='thin', color='D9D9D9'))

ws_sum_std["A1"] = "Company Default Work Template - Manual DTO Validation Tracker"
ws_sum_std["A1"].font = font_title
ws_sum_std["A2"] = "Instructions: On sheet 'CDWT DTO Validations', select Status in Column K (Pending, Pass, Failed, Backlog, Noted), enter Actual HTTP Code in Col L, and Notes in Col M."
ws_sum_std["A2"].font = Font(name="Calibri", size=10, italic=True, color="595959")

ws_sum_std["A4"] = "Execution Metric"
ws_sum_std["B4"] = "Count"
ws_sum_std["C4"] = "Percentage"
for c in ["A4", "B4", "C4"]:
    ws_sum_std[c].fill = navy_header
    ws_sum_std[c].font = font_header

metrics = [
    ("Total DTO Test Cases", f"=COUNTA('CDWT DTO Validations'!A2:A{len(cases_data)+1})", "100.0%"),
    ("Passed Tests (Pass)", f'=COUNTIF(\'CDWT DTO Validations\'!K2:K{len(cases_data)+1}, "Pass")', f'=B6/B5'),
    ("Failed Tests (Failed)", f'=COUNTIF(\'CDWT DTO Validations\'!K2:K{len(cases_data)+1}, "Failed")', f'=B7/B5'),
    ("Pending Tests (Pending)", f'=COUNTIF(\'CDWT DTO Validations\'!K2:K{len(cases_data)+1}, "Pending")', f'=B8/B5'),
    ("Backlog Tests (Backlog)", f'=COUNTIF(\'CDWT DTO Validations\'!K2:K{len(cases_data)+1}, "Backlog")', f'=B9/B5'),
    ("Noted / Observations (Noted)", f'=COUNTIF(\'CDWT DTO Validations\'!K2:K{len(cases_data)+1}, "Noted")', f'=B10/B5'),
    ("Total Verified / Executed", f'=B6+B7+B10', f'=B11/B5')
]

for idx, (label, formula_b, formula_c) in enumerate(metrics, start=5):
    ws_sum_std[f"A{idx}"] = label
    ws_sum_std[f"B{idx}"] = formula_b
    ws_sum_std[f"C{idx}"] = formula_c
    ws_sum_std[f"A{idx}"].font = font_bold
    ws_sum_std[f"B{idx}"].font = font_bold
    ws_sum_std[f"C{idx}"].font = font_bold
    ws_sum_std[f"B{idx}"].alignment = Alignment(horizontal="center")
    ws_sum_std[f"C{idx}"].alignment = Alignment(horizontal="center")
    
    for col in ["A", "B", "C"]:
        ws_sum_std[f"{col}{idx}"].border = border_thin
        if idx == 6:
            ws_sum_std[f"{col}{idx}"].fill = PatternFill(start_color="E2EFDA", end_color="E2EFDA", fill_type="solid")
        elif idx == 7:
            ws_sum_std[f"{col}{idx}"].fill = PatternFill(start_color="FCE4D6", end_color="FCE4D6", fill_type="solid")
        elif idx == 8:
            ws_sum_std[f"{col}{idx}"].fill = user_input_fill
        elif idx == 9:
            ws_sum_std[f"{col}{idx}"].fill = PatternFill(start_color="EDEDED", end_color="EDEDED", fill_type="solid")
        elif idx == 10:
            ws_sum_std[f"{col}{idx}"].fill = PatternFill(start_color="DDEBF7", end_color="DDEBF7", fill_type="solid")

for row in range(6, 12):
    ws_sum_std[f"C{row}"].number_format = "0.0%"

ws_sum_std["A14"] = "Target Environment Details:"
ws_sum_std["A14"].font = font_bold
ws_sum_std["A15"] = "Microservice URL: https://attendance2.dev.zoolwork.com"
ws_sum_std["A16"] = "Auth Server URL: https://auth8.dev.zoolwork.com/connect/token"
ws_sum_std["A17"] = "Company 2 GUID (Attendance 2): 3a247435-3cea-83ae-6a9f-6dda99f386a3"
ws_sum_std["A18"] = "Company 3 GUID (Attendance 3): 3a247435-e31d-ef15-8cc9-62c587f4eb3f"
ws_sum_std["A19"] = "Company 4 GUID (Attendance 4): 3a247436-8669-844a-7d2f-1a209af02d8e"
ws_sum_std["A20"] = "Tenant GUID: 3a24741e-2667-1223-f12e-62a69fab3838 (Attendance)"

ws_sum_std.column_dimensions["A"].width = 35
ws_sum_std.column_dimensions["B"].width = 18
ws_sum_std.column_dimensions["C"].width = 22

# Ensure Sheet 1 ('CDWT DTO Validations') is ACTIVE so Excel opens right to it!
wb_standalone.active = 0
wb_standalone.save("CompanyDefault_DTO_Validation_TestCases.xlsx")
print("SUCCESS: Saved CompanyDefault_DTO_Validation_TestCases.xlsx with Sheet 1 active!")


# =============================================================
# BUILD 2: Add sheet into AttendanceTestCases_Master_Consolidated.xlsx
# =============================================================
wb_master = openpyxl.load_workbook("AttendanceTestCases_Master_Consolidated.xlsx")
sheet_name = "CDWT - Manual DTO Validations"

if sheet_name in wb_master.sheetnames:
    del wb_master[sheet_name]
    print(f"Removed existing '{sheet_name}' sheet in master.")

ws_master_cases = wb_master.create_sheet(title=sheet_name)
build_cases_sheet(ws_master_cases)

wb_master.save("AttendanceTestCases_Master_Consolidated.xlsx")
print(f"SUCCESS: Added '{sheet_name}' sheet into AttendanceTestCases_Master_Consolidated.xlsx!")

