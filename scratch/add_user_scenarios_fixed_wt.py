import openpyxl, sys
sys.stdout.reconfigure(encoding='utf-8')

wb_path = 'AttendanceTestCases_Master_Consolidated.xlsx'
wb = openpyxl.load_workbook(wb_path)
ws = wb['User Scenarios (Add Here)']

new_test_cases = [
    (
        "USER-11",
        "Fixed Work Template - POST (Company Default)",
        "Create Company Default Fixed Work Template (6 working days, Friday off, 360 mins, Every Week recurrence)",
        "POST /api/companies/{companyId}/worktemplates/fixed (no locationId). Body with templateName {'en':'Attendance 1','ar':'ترجمة'}, shortCode 'ATTEDQA', 6 working days (08:00-09:00, Every Week), Fri off (00:00-00:00, recurrence []).",
        "HTTP 200 OK 'Fixed work template created'. DB PERSISTENCE: 1 doc in Sahab > ERP.Attendance.WorkTemplates with LocationId=00000000-..., IsDefault=true, Version='1.0', ShortCode='ATTEDQA', TotalWorkDurationInMinutes=360, TotalWorkingDays=6, TotalDaysOff=1, TemplateType=1, FixedTimeSlots with 7 days (Sun=1 to Sat=7, Fri=6 isWorkingDay=false).",
        "P1", "functional", "dev", "Not-Run",
        "[Real Payload Verification] Validates exact user example payload: 6 working days, Fri off, Every Week recurrence, numeric DayEnum mapping.",
        "User Example Payload & UI"
    ),
    (
        "USER-12",
        "Fixed Work Template - POST (Location Level)",
        "Create Location-Level Fixed Work Template using same payload with query locationId",
        "POST /api/companies/{companyId}/worktemplates/fixed?locationId={locationId}. Same valid payload with shortCode 'LOCED01'.",
        "HTTP 200 OK 'Fixed work template created'. DB PERSISTENCE: Stored with LocationId={locationId}, IsDefault=false, Version='1.0', IsCompanyLinked=false. Does NOT trigger cascade.",
        "P1", "functional", "dev", "Not-Run",
        "[Real Payload Verification] Location-scoped creation using identical slot structure.",
        "User Example Payload & UI"
    ),
    (
        "USER-13",
        "Fixed Work Template - Recurrence Rules",
        "Create Fixed Work Template with Alternate Week Recurrence (1st & 3rd / 2nd & 4th only)",
        "POST /worktemplates/fixed. Saturday configured with isWorkingDay:true, recurrenceOfMonth:['First', 'Third'], 08:00-09:00.",
        "HTTP 200 OK. Persisted in MongoDB with RecurrenceOfMonth:[1, 3] on Saturday. System correctly calculates monthly working hours based on recurrence pattern.",
        "P1", "functional", "dev", "Not-Run",
        "[UI Recurrence Verification] Validates '1st & 3rd only' dropdown selection from uploaded UI screenshot.",
        "User UI Screenshot"
    ),
    (
        "USER-14",
        "Fixed Work Template - Day Off Validation",
        "Reject Working Day payload contradiction (isWorkingDay=false with non-zero duration or non-zero start/end times)",
        "POST /worktemplates/fixed. Friday configured with isWorkingDay:false, but startTime:'08:00:00', endTime:'09:00:00', workDurationInMinutes:60.",
        "HTTP 400 Bad Request. Sbp:Validation 'A day off cannot have non-zero working hours or active time slots.' (or automatically normalized to 00:00:00).",
        "P2", "negative", "dev", "Not-Run",
        "[Negative Validation] Data integrity check: ensures day-off slots cannot hold active shift timings.",
        "Specification Validation"
    ),
    (
        "USER-15",
        "Fixed Work Template - Recurrence Validation",
        "Reject invalid / empty recurrence on an active working day (isWorkingDay=true, recurrenceOfMonth=[])",
        "POST /worktemplates/fixed. Monday configured with isWorkingDay:true, but recurrenceOfMonth:[].",
        "HTTP 400 Bad Request. Sbp:Validation 'At least one recurrence week must be specified for a working day.'",
        "P2", "negative", "dev", "Not-Run",
        "[Negative Validation] Guard against orphaned active working day with no scheduled weeks.",
        "Specification Validation"
    ),
    (
        "USER-16",
        "Fixed Work Template - Mathematical Consistency",
        "Verify totalWorkDurationInMinutes vs sum of active slots",
        "POST /worktemplates/fixed. Client sends totalWorkDurationInMinutes:480, but slots sum to 360 (6 * 60).",
        "Server recalculates server-side and stores correct duration Double('360'), or rejects with HTTP 400 'Total work duration does not match slot duration sum.'",
        "P2", "boundary", "dev", "Not-Run",
        "[Data Consistency] Guard against client-side math spoofing or corrupted total duration.",
        "Specification Validation"
    ),
    (
        "USER-17",
        "Fixed Work Template - DayEnum Validation",
        "Reject invalid / unrecognized dayEnum string (e.g. 'Funday', 'Mon123')",
        "POST /worktemplates/fixed. fixedTimeSlots contains dayEnum:'Funday'.",
        "HTTP 400 Bad Request. Sbp:Validation 'The value 'Funday' is not a valid DayEnum. Allowed values are: Sun, Mon, Tue, Wed, Thu, Fri, Sat.'",
        "P2", "negative", "dev", "Not-Run",
        "[DTO Schema Validation] Enum deserialization check on dayEnum string values.",
        "Specification Validation"
    ),
    (
        "USER-18",
        "Fixed Work Template - PATCH (Company Default Timings)",
        "Update Thursday timings on Company Default via PATCH (creates Version 2.0 and sets HasPendingLocSync)",
        "PATCH /api/companies/{companyId}/worktemplates/fixed/{cdwV1Id} (no locationId). Send updated Thursday slot: startTime:'08:00:00', endTime:'10:00:00', workDurationInMinutes:120, totalWorkDurationInMinutes:420.",
        "HTTP 200 OK 'Company default work template patched'. Old v1.0 doc marked Status=Archived(3), IsSuperseded=true. NEW doc v2.0 created with TotalWorkDurationInMinutes=420, Version='2.0', IsDefault=true, Status=Active(1), HasPendingLocSync=true. ChangeLog contains Timings/WorkHours chip.",
        "P1", "functional", "dev", "Not-Run",
        "[PATCH Company Default] Validates immutable versioning, version bump 1.0 -> 2.0, and sync flag.",
        "User Example Payload & Spec D-01"
    ),
    (
        "USER-19",
        "Fixed Work Template - PATCH (Location Template In-Place)",
        "Update timings on Location-Level Fixed Template via PATCH (in-place update, same ID)",
        "PATCH /api/companies/{companyId}/worktemplates/fixed/{locTemplateId}?locationId={locationId}. Send updated timings.",
        "HTTP 200 OK 'Fixed work template patched'. Modifies document IN-PLACE (same _id), keeps Version='1.0', updates ModifiedBy/ModifiedAt from JWT, does NOT archive.",
        "P1", "functional", "dev", "Not-Run",
        "[PATCH Location Template] In-place mutation check on location-scoped work template.",
        "User Example Payload & Spec B-01"
    ),
    (
        "USER-20",
        "Fixed Work Template - PATCH (Weekly Off Change)",
        "Convert Saturday from working day to Weekly Off via PATCH",
        "PATCH /worktemplates/fixed/{id}. Saturday updated to isWorkingDay:false, startTime:'00:00:00', endTime:'00:00:00', workDurationInMinutes:0, totalWorkingDays:5, totalDaysOff:2.",
        "HTTP 200 OK. Saturday stored with IsWorkingDay=false, TotalWorkingDays=5, TotalDaysOff=2. ChangeLog records DayOff change.",
        "P1", "functional", "dev", "Not-Run",
        "[PATCH Days Off Migration] Shift pattern re-allocation test.",
        "User UI Screenshot & Spec D-04"
    ),
    (
        "USER-21",
        "Fixed Work Template - PATCH Guard (ShortCode Locked)",
        "Reject attempt to change shortCode via PATCH",
        "PATCH /worktemplates/fixed/{id}. Body includes shortCode:'NEWATTQA'.",
        "HTTP 400 Bad Request. Error Code: Cit.Attendance:1107 ('A work template's short code cannot be changed after it is created.').",
        "P1", "negative", "dev", "Not-Run",
        "[PATCH Security Guard] Ensures shortCode immutability on update.",
        "Specification Spec D-06"
    ),
    (
        "USER-22",
        "Fixed Work Template - PATCH Guard (Empty Payload)",
        "Reject PATCH request with empty body or no updatable fields",
        "PATCH /worktemplates/fixed/{id}. Request body is empty JSON object {}.",
        "HTTP 400 Bad Request. Sbp:Validation 'At least one field must be provided to update.'",
        "P2", "negative", "dev", "Not-Run",
        "[PATCH Validation] Guards against empty mutation payloads.",
        "Specification Spec D-05"
    )
]

start_row = 12
for idx, tc in enumerate(new_test_cases):
    row_num = start_row + idx
    for col_idx, val in enumerate(tc, start=1):
        ws.cell(row=row_num, column=col_idx, value=val)

wb.save(wb_path)
print(f"Successfully added {len(new_test_cases)} user test cases to Master Consolidated Excel (rows {start_row} to {start_row + len(new_test_cases) - 1})!")

