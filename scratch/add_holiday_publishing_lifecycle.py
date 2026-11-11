import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter
import sys

sys.stdout.reconfigure(encoding='utf-8')

wb = openpyxl.load_workbook('AttendanceTestCases_Master_Consolidated.xlsx')

sheet_name = 'Holiday Calendar - Test Cases'
ws = wb[sheet_name]

# Define the 20 comprehensive publishing lifecycle test cases
pub_test_cases = [
    {
        "id": "HC-PUB-01",
        "section": "9. Publish Lifecycle - Work Template Prerequisite, Staging, Company Svc Sync & Re-Publish",
        "scenario": "Publish Blocked: Compulsory at least one holiday required before publish (0 holidays in list)",
        "input": "POST /api/companies/{companyId}/holidaylist/publish/2026 where YearlyCalendar.HolidayLists is empty []",
        "expected": "1. HTTP 400 Bad Request, Cit.Attendance:1704 (reason: 'no-holidays-provided' / 'Cannot publish empty holiday calendar. At least one holiday is required.').\n2. DB Verification: IsPublished remains false. Locations are NOT published to.",
        "pri": "P0",
        "type": "negative"
    },
    {
        "id": "HC-PUB-02",
        "section": "9. Publish Lifecycle - Work Template Prerequisite, Staging, Company Svc Sync & Re-Publish",
        "scenario": "Publish Blocked: Company has NO active Company Default Work Template (CDWT)",
        "input": "POST /holidaylist/publish/2026 for a company that has no CDWT configured in ERP.Attendance.WorkTemplates",
        "expected": "1. HTTP 400 Bad Request (Business guard: 'Company Default Work Template is required before publishing holiday calendar.').\n2. DB Verification: Holiday calendar IsPublished remains false.",
        "pri": "P0",
        "type": "negative"
    },
    {
        "id": "HC-PUB-03",
        "section": "9. Publish Lifecycle - Work Template Prerequisite, Staging, Company Svc Sync & Re-Publish",
        "scenario": "Publish Blocked: Company Default Work Template is archived / superseded without active replacement",
        "input": "POST /holidaylist/publish/2026 where company CDWT has IsDeleted=true or IsActive=false",
        "expected": "HTTP 400 Bad Request ('Active Company Default Work Template is required before publishing holiday calendar.'). DB unmodified.",
        "pri": "P1",
        "type": "negative"
    },
    {
        "id": "HC-PUB-04",
        "section": "9. Publish Lifecycle - Work Template Prerequisite, Staging, Company Svc Sync & Re-Publish",
        "scenario": "Pre-Publish Staging: Add holiday -> Verify IsPublished remains false (Unpublished Changes)",
        "input": "PATCH /api/companies/{companyId}/holidaylist/{id}/2026 adding new holiday item before publish",
        "expected": "1. HTTP 200 OK ('Holiday calendar updated successfully').\n2. Attendance DB: IsPublished is false. LastPublishedOn is null/unchanged. Location copies untouched.",
        "pri": "P0",
        "type": "smoke"
    },
    {
        "id": "HC-PUB-05",
        "section": "9. Publish Lifecycle - Work Template Prerequisite, Staging, Company Svc Sync & Re-Publish",
        "scenario": "Pre-Publish Staging: Edit holiday -> Verify IsPublished remains false and locations unchanged",
        "input": "PATCH /holidaylist/{id}/2026 modifying holiday name and dates before publish",
        "expected": "1. HTTP 200 OK.\n2. Attendance DB: Company Default updated; IsPublished=false. Inherited location calendars still show baseline state.",
        "pri": "P0",
        "type": "smoke"
    },
    {
        "id": "HC-PUB-06",
        "section": "9. Publish Lifecycle - Work Template Prerequisite, Staging, Company Svc Sync & Re-Publish",
        "scenario": "Pre-Publish Staging: Remove holiday -> Verify IsPublished remains false",
        "input": "PATCH /holidaylist/{id}/remove/{holidayId}/2026 removing one holiday before publish",
        "expected": "1. HTTP 200 OK ('Holiday removed successfully').\n2. Attendance DB: Target holiday pulled from YearlyCalendar.HolidayLists; IsPublished=false.",
        "pri": "P0",
        "type": "smoke"
    },
    {
        "id": "HC-PUB-07",
        "section": "9. Publish Lifecycle - Work Template Prerequisite, Staging, Company Svc Sync & Re-Publish",
        "scenario": "GET API verification before publish: isPublished returns false and UI shows Unpublished Changes",
        "input": "GET /api/companies/{companyId}/holidaylist/{id}",
        "expected": "HTTP 200 OK. Response JSON shows isPublished: false, reflecting staged changes pending publish.",
        "pri": "P0",
        "type": "smoke"
    },
    {
        "id": "HC-PUB-08",
        "section": "9. Publish Lifecycle - Work Template Prerequisite, Staging, Company Svc Sync & Re-Publish",
        "scenario": "Publish Success: Active CDWT exists + valid holiday list -> Overwrites inherited locations",
        "input": "POST /api/companies/{companyId}/holidaylist/publish/2026 where CDWT is active and calendar has >=1 holiday",
        "expected": "1. HTTP 200 OK ('Holidays published successfully').\n2. Attendance DB (Company Default): IsPublished updated to true; LastPublishedOn updated to current UTC timestamp.\n3. Attendance DB (Inherited Locations): HolidayLists array overwritten with the exact company default holidays.",
        "pri": "P0",
        "type": "smoke"
    },
    {
        "id": "HC-PUB-09",
        "section": "9. Publish Lifecycle - Work Template Prerequisite, Staging, Company Svc Sync & Re-Publish",
        "scenario": "Company Service Sync: Publish updates Company Service calendar and checklist required field",
        "input": "Following HC-PUB-08 publish, verify Company Service database (CompaniesMaster in CompanySvcNET8test)",
        "expected": "1. Company Service DB: CompanyChecklist / Company calendar required fields updated (e.g. HolidayCalendarPublished / HolidaysConfigured = true).\n2. Onboarding wizard marks company holidays as configured.",
        "pri": "P0",
        "type": "integration"
    },
    {
        "id": "HC-PUB-10",
        "section": "9. Publish Lifecycle - Work Template Prerequisite, Staging, Company Svc Sync & Re-Publish",
        "scenario": "GET API verification after publish: isPublished returns true and lastPublishedOn is populated",
        "input": "GET /api/companies/{companyId}/holidaylist/{id} immediately after publish",
        "expected": "HTTP 200 OK. Response JSON shows isPublished: true, lastPublishedOn matches current publish timestamp.",
        "pri": "P0",
        "type": "smoke"
    },
    {
        "id": "HC-PUB-11",
        "section": "9. Publish Lifecycle - Work Template Prerequisite, Staging, Company Svc Sync & Re-Publish",
        "scenario": "Post-Publish Mutation (Add): Adding holiday after publish reverts IsPublished to false",
        "input": "After calendar is published, call PATCH /holidaylist/{id}/2026 to add a new holiday (e.g. Bank Holiday)",
        "expected": "1. HTTP 200 OK.\n2. Attendance DB: New holiday appended to HolidayLists; IsPublished REVERTS to false (staged edit).\n3. Location calendars do NOT receive the new holiday yet (re-publish required).",
        "pri": "P0",
        "type": "smoke"
    },
    {
        "id": "HC-PUB-12",
        "section": "9. Publish Lifecycle - Work Template Prerequisite, Staging, Company Svc Sync & Re-Publish",
        "scenario": "Post-Publish Mutation (Edit): Editing holiday after publish reverts IsPublished to false",
        "input": "After calendar is published, call PATCH /holidaylist/{id}/2026 modifying an existing holiday's dates",
        "expected": "1. HTTP 200 OK.\n2. Attendance DB: Target holiday updated in Company Default; IsPublished REVERTS to false.\n3. Location copies still show old dates in DB and GET API until republished.",
        "pri": "P0",
        "type": "smoke"
    },
    {
        "id": "HC-PUB-13",
        "section": "9. Publish Lifecycle - Work Template Prerequisite, Staging, Company Svc Sync & Re-Publish",
        "scenario": "Post-Publish Mutation (Remove): Removing holiday after publish reverts IsPublished to false",
        "input": "After calendar is published, call PATCH /holidaylist/{id}/remove/{holidayId}/2026",
        "expected": "1. HTTP 200 OK.\n2. Attendance DB: Holiday pulled from Company Default; IsPublished REVERTS to false.\n3. Location copies still retain the holiday in DB until republished.",
        "pri": "P0",
        "type": "smoke"
    },
    {
        "id": "HC-PUB-14",
        "section": "9. Publish Lifecycle - Work Template Prerequisite, Staging, Company Svc Sync & Re-Publish",
        "scenario": "GET API verification after post-publish mutations: Confirms Republish Required status",
        "input": "GET /api/companies/{companyId}/holidaylist/{id} after post-publish add/edit/remove",
        "expected": "HTTP 200 OK. Response JSON shows isPublished: false, indicating pending republish.",
        "pri": "P0",
        "type": "smoke"
    },
    {
        "id": "HC-PUB-15",
        "section": "9. Publish Lifecycle - Work Template Prerequisite, Staging, Company Svc Sync & Re-Publish",
        "scenario": "Re-Publish Success (Round 2): Syncs 2nd round additions, edits, and removals to locations",
        "input": "POST /api/companies/{companyId}/holidaylist/publish/2026 (second publish call)",
        "expected": "1. HTTP 200 OK ('Holidays published successfully').\n2. Attendance DB (Company Default): IsPublished updated to true; LastPublishedOn updated to NEW current UTC timestamp.\n3. Attendance DB (Inherited Locations): HolidayLists re-synced with second-round additions, edits, and removals.",
        "pri": "P0",
        "type": "smoke"
    },
    {
        "id": "HC-PUB-16",
        "section": "9. Publish Lifecycle - Work Template Prerequisite, Staging, Company Svc Sync & Re-Publish",
        "scenario": "Company Service Re-Sync: Re-publish refreshes Company Service calendar status",
        "input": "Following HC-PUB-15 re-publish, verify Company Service DB",
        "expected": "Company Service calendar status and checklist remain synchronized and true.",
        "pri": "P1",
        "type": "integration"
    },
    {
        "id": "HC-PUB-17",
        "section": "9. Publish Lifecycle - Work Template Prerequisite, Staging, Company Svc Sync & Re-Publish",
        "scenario": "Customised location calendar isolation: Protected across initial publish AND re-publish",
        "input": "Location A1 customised (IsInherited=false). Call initial publish, add/remove holidays, call re-publish",
        "expected": "1. Location A1's local holidays remain completely untouched across both publish rounds.\n2. In DB: Location A1 retains IsInherited=false and its own custom holiday array.",
        "pri": "P0",
        "type": "smoke"
    },
    {
        "id": "HC-PUB-18",
        "section": "9. Publish Lifecycle - Work Template Prerequisite, Staging, Company Svc Sync & Re-Publish",
        "scenario": "Negative: Re-publish blocked if all holidays were removed down to 0 holidays",
        "input": "After publishing, remove all holidays one by one until HolidayLists is []. Call POST /publish/2026",
        "expected": "HTTP 400 Bad Request, Cit.Attendance:1704 ('Cannot publish empty holiday calendar. At least one holiday is required.').",
        "pri": "P1",
        "type": "negative"
    },
    {
        "id": "HC-PUB-19",
        "section": "9. Publish Lifecycle - Work Template Prerequisite, Staging, Company Svc Sync & Re-Publish",
        "scenario": "Idempotent Re-publish: Calling publish twice consecutively with NO edits",
        "input": "Call POST /publish/2026 immediately after a successful publish with no changes made in between",
        "expected": "HTTP 200 OK. Idempotent safe. LastPublishedOn updated; no duplicate documents or duplicate holidays created in DB.",
        "pri": "P1",
        "type": "regression"
    },
    {
        "id": "HC-PUB-20",
        "section": "9. Publish Lifecycle - Work Template Prerequisite, Staging, Company Svc Sync & Re-Publish",
        "scenario": "GET by Year verification: Confirms all inherited locations match Company Default after re-publish",
        "input": "GET /api/companies/{companyId}/holidaylist/2026 after re-publish",
        "expected": "HTTP 200 OK. JSON array shows every inherited location calendar has identical holiday count and details to Company Default.",
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
p2_fill = PatternFill(start_color="E0F2FE", end_color="E0F2FE", fill_type="solid") # light blue

start_row = ws.max_row + 1
current_row = start_row

pub_p0 = 0
pub_p1 = 0
pub_p2 = 0
pub_p3 = 0

for tc in pub_test_cases:
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
    if pri == "P0": pub_p0 += 1
    elif pri == "P1": pub_p1 += 1
    elif pri == "P2": pub_p2 += 1
    elif pri == "P3": pub_p3 += 1
    
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
print(f"Appended {len(pub_test_cases)} publishing lifecycle test cases to '{sheet_name}'.")
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
ws_idx.cell(row_mod16, 8).value = "Complete Holiday Suite: DTO Validations, GUIDs, 5 Types, Combinations, Removals, CDWT Prerequisite, Publishing & Company Svc Sync"

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
ws_idx.cell(row_total, 8).value = "Master Consolidated Suite with Active User Scenarios & Unified Holiday Calendar Multiple Combination & Publishing Suite"

print(f"INDEX Row 20 (Module 16): Total={total_in_sheet} (P0:{all_p0}, P1:{all_p1}, P2:{all_p2}, P3:{all_p3})")
print(f"INDEX Row 21 (TOTAL): Total={tot_tcs} (P0:{tot_p0}, P1:{tot_p1}, P2:{tot_p2}, P3:{tot_p3})")

# Save workbook
wb.save('AttendanceTestCases_Master_Consolidated.xlsx')
print("Successfully saved AttendanceTestCases_Master_Consolidated.xlsx!")
