import sys, openpyxl

sys.stdout.reconfigure(encoding='utf-8')

wb_name = "AttendanceTestCases_Master_Consolidated.xlsx"
wb = openpyxl.load_workbook(wb_name)

row_loc_107 = [
    "LOC-WT-107",
    "B. Edit Company Default & Location Cascade Sync",
    "Verify Location Synchronization Result via GET /sync-status API vs MongoDB HasPendingLocSync & Polymorphic Overwrite Safety",
    "Company Attendance 8 with CDWT v2.0 and 3 Flexible templates at locations. Query GET /worktemplates/company-default/sync-status and GET /worktemplates?locationId={locId}",
    "API returns accurate sync status (hasPendingLocSync=true if CDWT v2.0 pending); Flexible templates in MongoDB show HasPendingLocSync=false as creation default; apply-sync must not overwrite Flexible templates with Fixed CDWT",
    "P1",
    "Pass / Verified (Evidence 53)"
]

if "WT - Location Shifts" in wb.sheetnames:
    sheet = wb["WT - Location Shifts"]
    target_row = sheet.max_row + 1
    for r in range(1, sheet.max_row + 1):
        if sheet.cell(r, 1).value == "LOC-WT-107":
            target_row = r
            break
    for c, val in enumerate(row_loc_107, 1):
        sheet.cell(target_row, c).value = val
    print(f"Added/Updated LOC-WT-107 at Row {target_row} in WT - Location Shifts.")

wb.save(wb_name)
print(f"Saved {wb_name} successfully.")
