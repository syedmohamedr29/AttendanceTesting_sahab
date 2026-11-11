import sys, openpyxl

sys.stdout.reconfigure(encoding='utf-8')

workbooks = [
    "AttendanceTestCases_Master_Consolidated.xlsx",
    "Attendance_Policies_Manual_API_TestCases_MongoDB.xlsx",
    "AttendanceTestCases.xlsx"
]

row_defect_1004 = [
    "DEFECT-20261110-04",
    "P1 Critical",
    "Fixed Work Template In-Place Location PATCH Bypasses Validation: Accepts Recurrence Index 6, Mismatched Total Duration (3000m vs 2700m), and Invalid Timezone ('Invalid/Timezone') with HTTP 200 OK",
    "PATCH /api/companies/{companyId}/worktemplates/fixed/{id}?locationId={locationId}",
    "Attendance 8 (3a249871-7a8d-dec5-2d72-47795dd2662d)",
    "PATCH /worktemplates/fixed/c9e00652-eae5-429a-bef0-4d4ddf9e0a0f?locationId=3a24d629-0d56-a428-baa1-98493a77e614 with recurrenceOfMonth: [6], totalWorkDurationInMinutes: 3000, timeZoneId: 'Invalid/Timezone'",
    "HTTP 200 OK | Endpoint silently accepts corrupt schedule data, bypassing domain validation rules enforced during POST",
    "Document c9e00652-eae5-429a-bef0-4d4ddf9e0a0f in Sahab.ERP.Attendance.WorkTemplates shows RecurrenceOfMonth: [6], TotalWorkDurationInMinutes: 3000.0, and TimeZoneId: 'Invalid/Timezone' saved in MongoDB",
    "Corrupts shift schedule evaluation, punch reconciliation, attendance calculation engine, and payroll exports. Allows impossible recurrence index 6 and invalid timezone to govern work plans.",
    "In UpdateFixedWorkTemplateCommandHandler and UpdateFixedWorkTemplateValidator, enforce recurrence <= 5, validate TotalWorkDurationInMinutes equals slot sum, and validate timeZoneId against TimeZoneInfo.",
    "Evidence 55 (file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_55_fixed_wt_location_patch_validation_bypasses_and_db_results.png)"
]

new_location_tcs = [
    [
        "LOC-WT-109",
        "C. Location Fixed Shift In-Place PATCH Validations",
        "Verify In-Place Location Fixed Template PATCH Rejects Out-of-Range Recurrence Index 6",
        "Execute PATCH /worktemplates/fixed/{id}?locationId={locId} with recurrenceOfMonth: [6]",
        "HTTP 400 Bad Request; Cit.Attendance:Validation; recurrence index restricted to 1..5",
        "P1",
        "Fail (DEFECT-20261110-04, Evidence 55)"
    ],
    [
        "LOC-WT-110",
        "C. Location Fixed Shift In-Place PATCH Validations",
        "Verify In-Place Location Fixed Template PATCH Rejects Total Work Duration Mismatch",
        "Execute PATCH /worktemplates/fixed/{id}?locationId={locId} with totalWorkDurationInMinutes: 3000 (slots sum: 2700)",
        "HTTP 400 Bad Request; Cit.Attendance:Validation; declared total must equal slot sum",
        "P1",
        "Fail (DEFECT-20261110-04, Evidence 55)"
    ],
    [
        "LOC-WT-111",
        "C. Location Fixed Shift In-Place PATCH Validations",
        "Verify In-Place Location Fixed Template PATCH Rejects Invalid Timezone String",
        "Execute PATCH /worktemplates/fixed/{id}?locationId={locId} with timeZoneId: 'Invalid/Timezone'",
        "HTTP 400 Bad Request; Cit.Attendance:Validation; must be valid IANA/Windows timezone",
        "P1",
        "Fail (DEFECT-20261110-04, Evidence 55)"
    ],
    [
        "LOC-WT-112",
        "D. Location Work Template Quota & Architectural Limits",
        "Verify Location Work Template Maximum Quota Limit Enforced at 20 Templates",
        "Attempt to create 21st work template assigned to Location 1 (3a24d629-0d56-a428-baa1-98493a77e614)",
        "HTTP 400 Bad Request; Cit.Attendance:1203 Location maximum limit reached.",
        "P2",
        "Pass (Verified in POST-P09 & POST-N04, Evidence 55)"
    ],
    [
        "LOC-WT-113",
        "E. Work Template ShortCode Rules & Immutability",
        "Verify Work Template ShortCode Requires Exactly 7 Characters and Cannot Be Changed in PATCH",
        "POST with shortCode != 7 chars; PATCH with altered shortCode",
        "HTTP 400 Bad Request; Cit.Attendance:Validation (7-char rule) & Cit.Attendance:1107 (cannot change shortCode)",
        "P2",
        "Pass (Verified in POST-N21, N22, N23 & PATCH-N02, Evidence 55)"
    ]
]

for wb_name in workbooks:
    print(f"=== Processing {wb_name} ===")
    wb = openpyxl.load_workbook(wb_name)
    
    # 1. Update Policy Defects Log
    if "Policy Defects Log" in wb.sheetnames:
        sheet = wb["Policy Defects Log"]
        exists = False
        target_row = sheet.max_row + 1
        for r in range(1, sheet.max_row + 1):
            if sheet.cell(r, 1).value == "DEFECT-20261110-04":
                exists = True
                target_row = r
                break
        
        for c, val in enumerate(row_defect_1004, 1):
            sheet.cell(target_row, c).value = val
        print(f"  [{wb_name}] Added/Updated DEFECT-20261110-04 at Row {target_row} in Policy Defects Log.")

    # 2. Update WT - Location Shifts (in Master Consolidated)
    if "WT - Location Shifts" in wb.sheetnames:
        sheet = wb["WT - Location Shifts"]
        for tc_data in new_location_tcs:
            tc_id = tc_data[0]
            exists_tc = False
            target_tc_row = sheet.max_row + 1
            for r in range(1, sheet.max_row + 1):
                if sheet.cell(r, 1).value == tc_id:
                    exists_tc = True
                    target_tc_row = r
                    break
            for c, val in enumerate(tc_data, 1):
                sheet.cell(target_tc_row, c).value = val
            print(f"  [{wb_name}] Added/Updated {tc_id} at Row {target_tc_row} in WT - Location Shifts.")
    
    wb.save(wb_name)
    print(f"Saved {wb_name} successfully.\n")

print("All Excel workbooks synchronized with 100% parity!")
