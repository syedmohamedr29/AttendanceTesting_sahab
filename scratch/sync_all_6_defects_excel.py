import sys, openpyxl

sys.stdout.reconfigure(encoding='utf-8')

workbooks = [
    "AttendanceTestCases_Master_Consolidated.xlsx",
    "Attendance_Policies_Manual_API_TestCases_MongoDB.xlsx",
    "AttendanceTestCases.xlsx"
]

defect_rows = [
    [
        "DEFECT-20261110-04",
        "P1 Critical",
        "Fixed Work Template PATCH Validation Bypass: Accepts Out-of-Range Monthly Recurrence Index 6 with HTTP 200 OK",
        "PATCH /api/companies/{companyId}/worktemplates/fixed/{id}?locationId={locationId}",
        "Attendance 8 (3a249871-7a8d-dec5-2d72-47795dd2662d)",
        "PATCH /worktemplates/fixed/c9e00652-eae5-429a-bef0-4d4ddf9e0a0f with recurrenceOfMonth: [6]",
        "HTTP 200 OK | Endpoint silently accepts invalid recurrence index 6, bypassing domain validation",
        "Document c9e00652-eae5-429a-bef0-4d4ddf9e0a0f in Sahab.ERP.Attendance.WorkTemplates shows RecurrenceOfMonth: [6] saved in MongoDB",
        "Breaks schedule evaluation engine. Only 5 occurrences of any weekday exist in any calendar month.",
        "In UpdateFixedWorkTemplateValidator, enforce recurrence index between 1 and 5.",
        "Evidence 55 (file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_55_fixed_wt_location_patch_validation_bypasses_and_db_results.png)"
    ],
    [
        "DEFECT-20261110-05",
        "P1 Critical",
        "Fixed Work Template PATCH Validation Bypass: Accepts Mismatched Total Work Duration (3000m vs 2700m Slot Sum) with HTTP 200 OK",
        "PATCH /api/companies/{companyId}/worktemplates/fixed/{id}?locationId={locationId}",
        "Attendance 8 (3a249871-7a8d-dec5-2d72-47795dd2662d)",
        "PATCH /worktemplates/fixed/c9e00652-eae5-429a-bef0-4d4ddf9e0a0f with totalWorkDurationInMinutes: 3000 (actual slot sum: 2700)",
        "HTTP 200 OK | Endpoint accepts mismatched total duration without sum validation against slots",
        "Document c9e00652-eae5-429a-bef0-4d4ddf9e0a0f shows TotalWorkDurationInMinutes: 3000.0 while slots sum to 2700",
        "Corrupts payroll calculations and weekly work totals. Timesheet aggregation relies on declared duration.",
        "In UpdateFixedWorkTemplateValidator, enforce TotalWorkDurationInMinutes equals sum of working slot durations.",
        "Evidence 55 (file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_55_fixed_wt_location_patch_validation_bypasses_and_db_results.png)"
    ],
    [
        "DEFECT-20261110-06",
        "P1 Critical",
        "Fixed Work Template PATCH Validation Bypass: Accepts Arbitrary / Invalid Timezone String ('Invalid/Timezone') with HTTP 200 OK",
        "PATCH /api/companies/{companyId}/worktemplates/fixed/{id}?locationId={locationId}",
        "Attendance 8 (3a249871-7a8d-dec5-2d72-47795dd2662d)",
        "PATCH /worktemplates/fixed/c9e00652-eae5-429a-bef0-4d4ddf9e0a0f with timeZoneId: 'Invalid/Timezone'",
        "HTTP 200 OK | Endpoint accepts unvalidated timezone string without IANA/Windows timezone verification",
        "Document c9e00652-eae5-429a-bef0-4d4ddf9e0a0f shows TimeZoneId: 'Invalid/Timezone' in MongoDB",
        "Causes unhandled TimeZoneNotFoundException in punch reconciliation engine, crashing calculation workers.",
        "In UpdateFixedWorkTemplateValidator, validate TimeZoneId against TimeZoneInfo.FindSystemTimeZoneById.",
        "Evidence 55 (file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_55_fixed_wt_location_patch_validation_bypasses_and_db_results.png)"
    ],
    [
        "DEFECT-20261110-07",
        "P1 Critical",
        "Fixed Work Template POST Boundary Validation Gap: Accepts Out-of-Range Recurrence Values [0] and [6] on Working Days with HTTP 200 OK",
        "POST /api/companies/{companyId}/worktemplates/fixed?locationId={locationId}",
        "Attendance 8 (3a249871-7a8d-dec5-2d72-47795dd2662d)",
        "POST /worktemplates/fixed with recurrenceOfMonth: [0] (BVA16) and recurrenceOfMonth: [6] (BVA17)",
        "HTTP 200 OK | Creation endpoint accepts boundary invalid recurrence values 0 and 6, persisting into database",
        "Documents 9605711d-dc54-405c-a73b-e45a79cc22c9 (BVA16, [0]) and 6382798d-ed99-461d-a7df-c5add6896170 (BVA17, [6]) created in MongoDB",
        "Corrupts calendar scheduling. Month recurrence indices outside 1..5 break work plan generation.",
        "In CreateFixedWorkTemplateValidator, add RuleForEach on RecurrenceOfMonth to be InclusiveBetween(1, 5).",
        "Evidence 55 (file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_55_fixed_wt_location_patch_validation_bypasses_and_db_results.png)"
    ],
    [
        "DEFECT-20261110-08",
        "P2 Major",
        "Fixed Work Template POST Boundary Validation Gap: Accepts Continuous Work Duration of 10,080 Minutes (Full Week Continuous Working) with HTTP 200 OK",
        "POST /api/companies/{companyId}/worktemplates/fixed?locationId={locationId}",
        "Attendance 8 (3a249871-7a8d-dec5-2d72-47795dd2662d)",
        "POST /worktemplates/fixed with totalWorkDurationInMinutes: 10080 (BVA26)",
        "HTTP 200 OK | Endpoint accepts 168 hours nonstop weekly duration without upper ceiling validation",
        "Document 40ac02d3-85f8-4f3e-afb9-813d421c186e in MongoDB has TotalWorkDurationInMinutes: 10080.0",
        "Violates statutory labour laws capping weekly hours at 48 hours (Saudi Labour Law Art. 98).",
        "Enforce upper limit guardrail (e.g. <= 3600 minutes / 60 hours per week).",
        "Evidence 55 (file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_55_fixed_wt_location_patch_validation_bypasses_and_db_results.png)"
    ],
    [
        "DEFECT-20261110-09",
        "P2 Major",
        "Location Work Template Hard Quota Enforced at 20 Templates with Cit.Attendance:1203 Location maximum limit reached.",
        "POST /api/companies/{companyId}/worktemplates/fixed?locationId={locationId}",
        "Attendance 8 (3a249871-7a8d-dec5-2d72-47795dd2662d)",
        "POST /worktemplates/fixed?locationId=3a24d629-0d56-a428-baa1-98493a77e614 attempting to create 21st template (POST-P09)",
        "HTTP 400 Bad Request | Cit.Attendance:1203 Location maximum limit reached.",
        "Location 1 currently holds exactly 20 templates in Sahab.ERP.Attendance.WorkTemplates. Any further creation fails.",
        "Blocks HR operational expansion. No UI warning, capacity dashboard, or quota visibility exists.",
        "Expose quota metadata in GET worktemplates and surface a capacity indicator in the Web UI.",
        "Evidence 55 (file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_55_fixed_wt_location_patch_validation_bypasses_and_db_results.png)"
    ]
]

for wb_name in workbooks:
    print(f"=== Processing {wb_name} ===")
    wb = openpyxl.load_workbook(wb_name)
    
    if "Policy Defects Log" in wb.sheetnames:
        sheet = wb["Policy Defects Log"]
        for d_row in defect_rows:
            d_id = d_row[0]
            exists = False
            target_row = sheet.max_row + 1
            for r in range(1, sheet.max_row + 1):
                if sheet.cell(r, 1).value == d_id:
                    exists = True
                    target_row = r
                    break
            
            for c, val in enumerate(d_row, 1):
                sheet.cell(target_row, c).value = val
            print(f"  [{wb_name}] Added/Updated {d_id} at Row {target_row} in Policy Defects Log.")
    
    wb.save(wb_name)
    print(f"Saved {wb_name} successfully.\n")

print("All 3 Excel workbooks updated with all 6 defect issues!")
