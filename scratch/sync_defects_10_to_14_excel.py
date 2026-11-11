import sys, openpyxl

sys.stdout.reconfigure(encoding='utf-8')

workbooks = [
    "AttendanceTestCases_Master_Consolidated.xlsx",
    "Attendance_Policies_Manual_API_TestCases_MongoDB.xlsx",
    "AttendanceTestCases.xlsx"
]

defect_rows = [
    [
        "DEFECT-20261110-10",
        "P1 Critical",
        "Flexible Work Template POST & PATCH Validation Bypass: Accepts Out-of-Range Monthly Recurrence Index 6 with HTTP 200 OK",
        "POST/PATCH /api/companies/{companyId}/worktemplates/flexi",
        "Attendance 8 (3a249871-7a8d-dec5-2d72-47795dd2662d)",
        "POST/PATCH /worktemplates/flexi with recurrenceOfMonth: [6] (FLX-NEG-09, FLX-PAT-05)",
        "HTTP 200 OK | Endpoints accept invalid recurrence index 6, persisting into database",
        "Documents 0ee23f7d-aa83-493b-af79-93c99c2f7c9d and 7ecfbe95-8d3c-4612-a0cc-1454e9093a53 in Sahab.ERP.Attendance.WorkTemplates show RecurrenceOfMonth: [6]",
        "Breaks schedule evaluation engine. Only 5 occurrences of any weekday exist in any calendar month.",
        "In CreateFlexiWorkTemplateValidator and UpdateFlexiWorkTemplateValidator, enforce recurrence index between 1 and 5.",
        "Evidence 56 (file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_56_flexi_split_location_validation_bypasses_and_db_results.png)"
    ],
    [
        "DEFECT-20261110-11",
        "P1 Critical",
        "Flexible Work Template POST & PATCH Validation Bypass: Accepts Mismatched Total Work Duration with HTTP 200 OK",
        "POST/PATCH /api/companies/{companyId}/worktemplates/flexi",
        "Attendance 8 (3a249871-7a8d-dec5-2d72-47795dd2662d)",
        "POST/PATCH /worktemplates/flexi with declared 3000m / 3500m vs 2400m / 2700m slot sums (FLX-NEG-10, FLX-PAT-06)",
        "HTTP 200 OK | Endpoints accept mismatched total duration without slot sum validation",
        "Documents 96a20f25-47fb-496a-b595-0259aedba8c5 and 7ecfbe95-8d3c-4612-a0cc-1454e9093a53 show corrupt TotalWorkDurationInMinutes",
        "Corrupts payroll calculations and weekly work totals. Timesheet aggregation relies on declared duration.",
        "In CreateFlexiWorkTemplateValidator and UpdateFlexiWorkTemplateValidator, enforce TotalWorkDurationInMinutes equals sum of slot durations.",
        "Evidence 56 (file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_56_flexi_split_location_validation_bypasses_and_db_results.png)"
    ],
    [
        "DEFECT-20261110-12",
        "P1 Critical",
        "Flexible Work Template PATCH Validation Bypass: Accepts Arbitrary / Invalid Timezone String ('Invalid/Timezone') with HTTP 200 OK",
        "PATCH /api/companies/{companyId}/worktemplates/flexi/{id}?locationId={locationId}",
        "Attendance 8 (3a249871-7a8d-dec5-2d72-47795dd2662d)",
        "PATCH /worktemplates/flexi/7ecfbe95-8d3c-4612-a0cc-1454e9093a53 with timeZoneId: 'Invalid/Timezone' (FLX-PAT-07)",
        "HTTP 200 OK | Endpoint accepts unvalidated timezone string without IANA/Windows timezone verification",
        "Document 7ecfbe95-8d3c-4612-a0cc-1454e9093a53 shows TimeZoneId: 'Invalid/Timezone' in MongoDB",
        "Causes unhandled TimeZoneNotFoundException in punch reconciliation engine, crashing calculation workers.",
        "In UpdateFlexiWorkTemplateValidator, validate TimeZoneId against TimeZoneInfo.FindSystemTimeZoneById.",
        "Evidence 56 (file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_56_flexi_split_location_validation_bypasses_and_db_results.png)"
    ],
    [
        "DEFECT-20261110-13",
        "P1 Critical",
        "Split Work Template POST & PATCH Validation Bypass: Accepts Mismatched Total Work Duration with HTTP 200 OK",
        "POST/PATCH /api/companies/{companyId}/worktemplates/split",
        "Attendance 8 (3a249871-7a8d-dec5-2d72-47795dd2662d)",
        "POST/PATCH /worktemplates/split with declared 3000m / 3200m vs 2400m interval sums (SPL-NEG-10, SPL-PAT-07)",
        "HTTP 200 OK | Endpoints accept mismatched total duration without interval sum validation",
        "Documents 31f4a4df-1c71-464a-95c0-aa5198031d2d and ab6bb972-24e9-4b3c-9c23-55ef8770f6e5 show corrupt TotalWorkDurationInMinutes",
        "Corrupts timesheet aggregation and shift balance accounting.",
        "In CreateSplitWorkTemplateValidator and UpdateSplitWorkTemplateValidator, enforce TotalWorkDurationInMinutes equals sum of split interval durations.",
        "Evidence 56 (file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_56_flexi_split_location_validation_bypasses_and_db_results.png)"
    ],
    [
        "DEFECT-20261110-14",
        "P1 Critical",
        "Split Work Template PATCH Validation Bypass: Accepts Out-of-Range Monthly Recurrence Index 6 with HTTP 200 OK",
        "PATCH /api/companies/{companyId}/worktemplates/split/{id}?locationId={locationId}",
        "Attendance 8 (3a249871-7a8d-dec5-2d72-47795dd2662d)",
        "PATCH /worktemplates/split/ab6bb972-24e9-4b3c-9c23-55ef8770f6e5 with recurrenceOfMonth: [6] (SPL-PAT-06)",
        "HTTP 200 OK | Endpoint accepts invalid recurrence index 6, persisting into database",
        "Document ab6bb972-24e9-4b3c-9c23-55ef8770f6e5 shows RecurrenceOfMonth: [6] in MongoDB",
        "Causes downstream scheduling failure due to impossible 6th recurrence in a calendar month.",
        "In UpdateSplitWorkTemplateValidator, enforce recurrence index between 1 and 5.",
        "Evidence 56 (file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_56_flexi_split_location_validation_bypasses_and_db_results.png)"
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
            for row in sheet.iter_rows(values_only=True):
                if row and row[0] == d_id:
                    exists = True
                    break
            if not exists:
                sheet.append(d_row)
                print(f"  Appended {d_id} to Policy Defects Log")
            else:
                print(f"  {d_id} already exists in Policy Defects Log")
    
    if "Defects" in wb.sheetnames:
        sheet = wb["Defects"]
        for d_row in defect_rows:
            d_id = d_row[0]
            exists = False
            for row in sheet.iter_rows(values_only=True):
                if row and row[0] == d_id:
                    exists = True
                    break
            if not exists:
                sheet.append(d_row)
                print(f"  Appended {d_id} to Defects")
            else:
                print(f"  {d_id} already exists in Defects")
                
    wb.save(wb_name)
    print(f"Saved {wb_name}\n")
