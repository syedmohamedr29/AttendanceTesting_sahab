import openpyxl

wb_path = 'AttendanceTestCases_Master_Consolidated.xlsx'
wb = openpyxl.load_workbook(wb_path)
ws = wb['Holiday Calendar - Test Cases']

updates = {
    2: "[Re-Verified 16-Nov-2026 - HC-DTO-01]: STILL NOT FIXED. Route parameter companyId malformed GUID returns HTTP 404 Not Found (ASP.NET Core route constraint {companyId:guid}) instead of RFC 9110 HTTP 400 Bad Request. Synced to Confluence Row 13.",
    75: "[Re-Verified 16-Nov-2026 - HC-DTO-74]: STILL NOT FIXED. PATCH route {year} non-numeric string returns HTTP 404 Not Found (ASP.NET Core route constraint {year:int}) instead of HTTP 400 Bad Request. Synced to Confluence Row 13.",
    128: "[Re-Verified 16-Nov-2026 - HC-DTO-127]: STILL NOT FIXED. Route parameter companyId with non-hex characters returns HTTP 404 Not Found instead of HTTP 400 Bad Request. Synced to Confluence Row 13.",
    130: "[Re-Verified 16-Nov-2026 - HC-DTO-129]: STILL NOT FIXED. Route parameter companyId with invalid length (35 chars) returns HTTP 404 Not Found instead of HTTP 400 Bad Request. Synced to Confluence Row 13.",
    268: "[Re-Verified 16-Nov-2026 - HC-PUB-01 / DEFECT-20261103-15]: STILL NOT FIXED. PublishHolidayCalendarCommandHandler lacks defense-in-depth guard; empty calendar with 0 holidays successfully published with HTTP 200 OK (IsPublished: true). Synced to Confluence Row 11.",
    283: "[Re-Verified 16-Nov-2026 - HC-PUB-16 / DEFECT-20261026-01]: STILL NOT FIXED. Publishing holiday calendar does not synchronize CompanyChecklist.HolidayCalendarPublished in SP.CompanySvc (remains false). Synced to Confluence Row 14.",
    285: "[Re-Verified 16-Nov-2026 - HC-PUB-18 / DEFECT-20261103-15]: STILL NOT FIXED. Re-publish check missing on Publish endpoint for empty calendars. Synced to Confluence Row 11.",
    313: "[Re-Verified 16-Nov-2026 - HC-DTO-145 / DEFECT-20261103-08]: STILL NOT FIXED. calendarType invalid enum 999 is NOT validated at DTO layer; server silently coerces 999 to 1 (CompanyDefault) in MongoDB and triggers Cit.Attendance:1713 conflict. Synced to Confluence Row 10."
}

for row_idx, note in updates.items():
    ws.cell(row=row_idx, column=10).value = note
    print(f"Updated Row {row_idx}: {ws.cell(row=row_idx, column=1).value}")

wb.save(wb_path)
print("Successfully updated AttendanceTestCases_Master_Consolidated.xlsx for Holiday Calendar!")
