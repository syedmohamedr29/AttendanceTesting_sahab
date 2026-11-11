import openpyxl, sys
sys.stdout.reconfigure(encoding='utf-8')

wb_path = 'AttendanceTestCases_Master_Consolidated.xlsx'
wb = openpyxl.load_workbook(wb_path)
ws = wb['User Scenarios (Add Here)']

new_test_cases = [
    (
        "USER-29",
        "Flexi Work Template - POST (Daily Mode, 54h Weekly)",
        "Create Flexible Company Default WT in Daily Mode (6 days x 9 hrs = 54h / 3240 mins)",
        "POST /api/companies/{companyId}/worktemplates/flexi (no locationId). Body with templateName {'en':'Attendance 1'}, flexibleType:'Daily'(1), totalWorkDurationInMinutes:3240, 6 working days x 540 mins, Fri off x 0 mins.",
        "HTTP 200 OK 'Flexi work template created'. DB PERSISTENCE: 1 doc in Sahab > ERP.Attendance.WorkTemplates with LocationId=00000000-..., IsDefault=true, Version='1.0', TemplateType=2 (Flexi), FlexibleType=1 (Daily), TotalWorkDurationInMinutes=3240, FlexiTimeSlots with 7 days (Sun=1 to Sat=7, Fri=6 off).",
        "P1", "functional", "dev", "Not-Run",
        "[Real User Payload Verification] Validates exact user example payload: Flexible Daily mode, 540 mins/day, Every Week recurrence.",
        "User Example Payload & UI"
    ),
    (
        "USER-30",
        "Flexi Work Template - POST (Weekly Mode, 48h Weekly)",
        "Create Flexible Company Default WT in Weekly Mode (48 Hours / 2880 mins per week)",
        "POST /api/companies/{companyId}/worktemplates/flexi (no locationId). Body with flexibleType:'Weekly'(2), totalWorkDurationInMinutes:2880, working days enabled without individual slot start/end times.",
        "HTTP 200 OK 'Flexi work template created'. DB PERSISTENCE: Stored with TemplateType=2 (Flexi), FlexibleType=2 (Weekly), TotalWorkDurationInMinutes=2880. Only weekly total is enforced.",
        "P1", "functional", "dev", "Not-Run",
        "[UI Per-Week Verification] Validates 'Per week' toggle selection (48 hours standard) from uploaded UI screenshot.",
        "User UI Screenshot"
    ),
    (
        "USER-31",
        "Flexi Work Template - PATCH Migration (Fixed to Flexi Daily)",
        "Migrate Company Default from Fixed to Flexible Daily mode via PATCH (Creates Version 2.0)",
        "PATCH /api/companies/{companyId}/worktemplates/flexi/{fixedV1Id} (no locationId). Body with flexibleType:'Daily', totalWorkDurationInMinutes:3240, 6 days x 540 mins.",
        "HTTP 200 OK 'Flexi company default work template patched (new document created)'. Returns oldTemplateId and newTemplateId. DB: Old doc marked Status=Archived(3), IsSuperseded=true. NEW doc v2.0 created with TemplateType=2, FlexibleType=1, ChangeLog chips: 1) Work Type: Fixed -> Flexible, 2) Timings Changed, 3) Weekly hours: 6h -> 54h.",
        "P1", "functional", "dev", "Not-Run",
        "[Real Run Verification] Confirms exact real-world response and ChangeLog entries from user test execution.",
        "User Test Run & DB Proof"
    ),
    (
        "USER-32",
        "Flexi Work Template - PATCH Migration (Fixed to Flexi Weekly)",
        "Migrate Company Default from Fixed to Flexible Weekly mode (48h) via PATCH",
        "PATCH /api/companies/{companyId}/worktemplates/flexi/{fixedV1Id} (no locationId). Body with flexibleType:'Weekly', totalWorkDurationInMinutes:2880.",
        "HTTP 200 OK. Version bumped to 2.0. DB stores FlexibleType=2 (Weekly), TotalWorkDurationInMinutes=2880. ChangeLog records WorkType and Weekly hours changes.",
        "P1", "functional", "dev", "Not-Run",
        "[PATCH Weekly Mode] Migration from Fixed to Flexible Weekly mode.",
        "User UI Screenshot & Specs"
    ),
    (
        "USER-33",
        "Flexi Work Template - Daily Limit Negative (> 24 Hours / 25 Hours)",
        "Reject daily work duration exceeding 24 hours (e.g. 25 hours / 1500 mins per day)",
        "POST or PATCH /worktemplates/flexi. Monday configured with isWorkingDay:true, workDurationInMinutes:1500 (25 hours).",
        "HTTP 400 Bad Request. Sbp:Validation 'Daily work duration cannot exceed 24 hours (1440 minutes).' Physical impossibility guard strictly enforced.",
        "P1", "negative", "dev", "Not-Run",
        "[User Requested 25h Negative Check] Verifies system blocks per-day hours greater than 24h.",
        "User Request Scenario"
    ),
    (
        "USER-34",
        "Flexi Work Template - Weekly Limit Negative (> 168 Hours / Week)",
        "Reject weekly work duration exceeding total hours in a week (e.g. 170 hours / 10200 mins)",
        "POST or PATCH /worktemplates/flexi in Weekly mode. totalWorkDurationInMinutes:10200 (170 hours).",
        "HTTP 400 Bad Request. Sbp:Validation 'Weekly work duration cannot exceed total hours in a week (168 hours / 10080 minutes).' Labor boundary enforced.",
        "P1", "negative", "dev", "Not-Run",
        "[User Requested Week Negative Check] Verifies system blocks total weekly hours exceeding calendar week.",
        "User Request Scenario"
    ),
    (
        "USER-35",
        "Flexi Work Template - Daily Zero Hours Negative",
        "Reject active working day configured with 0 hours in Daily Flexible mode",
        "POST or PATCH /worktemplates/flexi in Daily mode. Monday configured with isWorkingDay:true, but workDurationInMinutes:0.",
        "HTTP 400 Bad Request. Sbp:Validation 'Each working day must have a work duration greater than zero.'",
        "P2", "negative", "dev", "Not-Run",
        "[Zero Hours Negative Check] Ensures active working day cannot have 0 minutes.",
        "Specification Validation"
    ),
    (
        "USER-36",
        "Flexi Work Template - Negative Hours Validation (< 0)",
        "Reject negative work duration in Daily or Weekly mode (e.g. -60 mins / -540 mins)",
        "POST or PATCH /worktemplates/flexi. workDurationInMinutes:-60 or totalWorkDurationInMinutes:-3240.",
        "HTTP 400 Bad Request. Sbp:Validation 'Work duration must be greater than or equal to 0.'",
        "P2", "negative", "dev", "Not-Run",
        "[Negative Number Check] Ensures durations cannot be negative.",
        "Specification Validation"
    ),
    (
        "USER-37",
        "Enum Validation - FlexibleType (Daily vs Weekly vs Invalid)",
        "Validate FlexibleType enum accepted values ('Daily'=1, 'Weekly'=2) and reject invalid enum values",
        "1. flexibleType:'Daily' (or 1) -> 200. 2. flexibleType:'Weekly' (or 2) -> 200. 3. flexibleType:'Monthly' (or 3, -1, 'Invalid') -> 400.",
        "1 & 2: HTTP 200 OK. Persisted in MongoDB as FlexibleType:1 and FlexibleType:2. 3: HTTP 400 Bad Request 'The value 'Monthly' is not a valid FlexibleType. Allowed values are: Daily, Weekly.'",
        "P1", "dto-enum", "dev", "Not-Run",
        "[Enum Validation] Validates string names and integer mapping for FlexibleType.",
        "Enum-List.md"
    ),
    (
        "USER-38",
        "Enum Validation - Fixed & Flexi DayEnum (Sun=1 to Sat=7)",
        "Validate DayEnum string values ('Sun'..'Sat') and numeric storage (Sun=1, Mon=2, ..., Sat=7)",
        "Send dayEnum:'Mon' in request. Inspect MongoDB document.",
        "HTTP 200 OK. MongoDB stores DayEnum: NumberInt(2) (Mon=2). Verify Sun=1, Tue=3, Wed=4, Thu=5, Fri=6, Sat=7. Invalid string 'Funday' returns HTTP 400.",
        "P1", "dto-enum", "dev", "Not-Run",
        "[Enum Validation] Confirms Middle East standard DayEnum mapping across both Fixed and Flexi.",
        "Enum-List.md & User DB Proof"
    ),
    (
        "USER-39",
        "Enum Validation - RecurrenceOfMonth (1st..5th and Dropdown Combinations)",
        "Validate RecurrenceOfMonth enum values ('First'..'Fifth') across 'Every Week', '1st & 3rd', '2nd & 4th'",
        "1. Every Week: ['First'..'Fifth'] -> DB [1..5]. 2. 1st & 3rd only: ['First','Third'] -> DB [1,3]. 3. 2nd & 4th only: ['Second','Fourth'] -> DB [2,4]. 4. Invalid 'Tenth' -> 400.",
        "1, 2, 3: HTTP 200 OK. Correctly persisted as NumberInt array in MongoDB. 4: HTTP 400 Bad Request 'Invalid RecurrenceOfMonth'.",
        "P1", "dto-enum", "dev", "Not-Run",
        "[Enum Validation] Validates dropdown combinations from UI screenshots for both Fixed and Flexi.",
        "Enum-List.md & UI Screenshot"
    ),
    (
        "USER-40",
        "Flexi Work Template - Weekly vs Daily Contradiction Guard",
        "Reject contradiction where Weekly total requires more hours than physically possible on active days",
        "POST /worktemplates/flexi in Weekly mode. totalWorkDurationInMinutes:2880 (48 hours), but only 1 day (Sunday) is marked isWorkingDay:true (requires 48h in 1 day!).",
        "HTTP 400 Bad Request. Sbp:Validation 'Total weekly duration exceeds the maximum possible hours (24h per active day) for the number of configured working days.'",
        "P2", "boundary", "dev", "Not-Run",
        "[Mathematical Contradiction Guard] Prevents impossible schedules where weekly hours exceed active day capacity.",
        "Specification Boundary Validation"
    )
]

start_row = 30
for idx, tc in enumerate(new_test_cases):
    row_num = start_row + idx
    for col_idx, val in enumerate(tc, start=1):
        ws.cell(row=row_num, column=col_idx, value=val)

wb.save(wb_path)
print(f"Successfully added {len(new_test_cases)} user test cases to Master Consolidated Excel (rows {start_row} to {start_row + len(new_test_cases) - 1})!")

