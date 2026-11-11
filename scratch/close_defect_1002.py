import sys, openpyxl

sys.stdout.reconfigure(encoding='utf-8')

workbooks = [
    "AttendanceTestCases_Master_Consolidated.xlsx",
    "Attendance_Policies_Manual_API_TestCases_MongoDB.xlsx",
    "AttendanceTestCases.xlsx"
]

for wb_name in workbooks:
    print(f"=== Processing {wb_name} ===")
    wb = openpyxl.load_workbook(wb_name)
    
    # 1. Update Policy Defects Log
    if "Policy Defects Log" in wb.sheetnames:
        sheet = wb["Policy Defects Log"]
        for r in range(1, sheet.max_row + 1):
            if sheet.cell(r, 1).value == "DEFECT-20261110-02":
                sheet.cell(r, 2).value = "Closed (Working as Designed)"
                sheet.cell(r, 7).value = "CONFIRMED WORKING AS DESIGNED (NOT A BUG): Company default template assigned to location is immutable at location level. If location needs custom schedule, a new location template is created (e.g. Flexi LOC0002). Editing CDWT sets HasPendingLocSync: true on CDWT, driving sync banner."
                sheet.cell(r, 9).value = "No Defect / Architecture Invariant: Preserves organizational policy integrity by preventing location-level tampering with company defaults while allowing independent location template creation."
                sheet.cell(r, 10).value = "No code change required. System operates as intended per business architecture."
                print(f"  [{wb_name}] Updated DEFECT-20261110-02 at Row {r} to Closed (Working as Designed).")
                break
                
    # 2. Update WT - Location Shifts (in Master Consolidated)
    if "WT - Location Shifts" in wb.sheetnames:
        sheet = wb["WT - Location Shifts"]
        for r in range(1, sheet.max_row + 1):
            if sheet.cell(r, 1).value == "LOC-WT-106":
                sheet.cell(r, 5).value = "Company default assigned to location cannot be edited directly at location level; editing CDWT sets HasPendingLocSync=true on CDWT. Locations requiring custom schedules create new location templates (e.g. Flexi LOC0002). Working as Designed (Not a Bug)."
                sheet.cell(r, 7).value = "Working as Designed (Closed)"
                print(f"  [{wb_name}] Updated LOC-WT-106 at Row {r} to Working as Designed (Closed).")
                break
                
    wb.save(wb_name)
    print(f"Saved {wb_name} successfully.\n")
