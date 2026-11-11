import openpyxl, sys
sys.stdout.reconfigure(encoding='utf-8')

wb_path = 'AttendanceTestCases_Master_Consolidated.xlsx'
wb = openpyxl.load_workbook(wb_path)
ws = wb['User Scenarios (Add Here)']

new_test_cases = [
    (
        "USER-23",
        "Company Default - Edit (Fixed to Fixed)",
        "Edit Company Default Work Template maintaining Fixed type (Same Type Edit)",
        "Company has active Fixed CDWT v1.0. Call PATCH /api/companies/{companyId}/worktemplates/fixed/{v1Id} (no locationId) with modified timings/working days.",
        "HTTP 200 OK 'Fixed work template patched'. Old v1.0 marked Status=Archived(3), IsSuperseded=true. NEW doc v2.0 created with TemplateType=Fixed(1), IsDefault=true, Status=Active(1), HasPendingLocSync=true. Version bumped to 2.0.",
        "P1", "functional", "dev", "Not-Run",
        "[Scenario A.1] Same-type edit on company default creates version 2.0 and sets location sync banner.",
        "User Scenario A & Spec D-01"
    ),
    (
        "USER-24",
        "Company Default - Type Migration (Fixed to Flexi)",
        "Migrate Company Default Work Template from Fixed to Flexible via PATCH",
        "Company has active Fixed CDWT v1.0. Call PATCH /api/companies/{companyId}/worktemplates/flexi/{v1Id} (no locationId) with flexibleType:1 (Daily) and totalRequiredHours:'08:00'.",
        "HTTP 200 OK. Cross-type migration allowed among regular types. Old Fixed v1.0 archived. NEW doc v2.0 created with TemplateType=Flexi(2), IsDefault=true, Status=Active(1), HasPendingLocSync=true. Version bumped to 2.0.",
        "P1", "functional", "dev", "Not-Run",
        "[Scenario A.2] Cross-type migration Fixed -> Flexi allowed on company default.",
        "User Scenario A & Spec D-03"
    ),
    (
        "USER-25",
        "Company Default - Type Migration (Fixed to Split)",
        "Migrate Company Default Work Template from Fixed to Split Shift via PATCH",
        "Company has active Fixed CDWT v1.0. Call PATCH /api/companies/{companyId}/worktemplates/split/{v1Id} (no locationId) with splitTimeSlots (2 slots per working day).",
        "HTTP 200 OK. Old Fixed v1.0 archived. NEW doc v2.0 created with TemplateType=Split(3), IsDefault=true, Status=Active(1), HasPendingLocSync=true. Version bumped to 2.0.",
        "P1", "functional", "dev", "Not-Run",
        "[Scenario A.3] Cross-type migration Fixed -> Split allowed on company default.",
        "User Scenario A & Spec D-03"
    ),
    (
        "USER-26",
        "Company Default - Type Migration Guard (Fixed to Roster/Rotation)",
        "Block attempt to migrate Company Default to Roster or Rotation template on PATCH",
        "Company has active Fixed CDWT v1.0. Call PATCH /api/companies/{companyId}/worktemplates/roster/{v1Id} or /rotation/{v1Id} (no locationId).",
        "HTTP 400 Bad Request. Error Code: Cit.Attendance:1105 ('A roster work template cannot be changed to another template type.') or Cit.Attendance:1205. Company default cannot be roster/rotation.",
        "P1", "negative", "dev", "Not-Run",
        "[Scenario A.4] Roster/Rotation conversion guard: company default must be a regular type (Fixed/Flexi/Split).",
        "User Scenario A & Spec B-04"
    ),
    (
        "USER-27",
        "Location WT - Prerequisite Guard (No CDWT)",
        "Reject attempt to create Location Work Template when Company Default does not exist",
        "Company has active location, but NO Company Default WT configured yet. Call POST /api/companies/{companyId}/worktemplates/fixed?locationId={locId}.",
        "HTTP 400 Bad Request. Error Code: Cit.Attendance:1205 ('Company default is not available.'). Location template creation strictly blocked until CDWT exists.",
        "P1", "negative", "dev", "Not-Run",
        "[Scenario B.1] Prerequisite guard: Company default must exist before any location template can be created.",
        "User Scenario B & Spec A-03"
    ),
    (
        "USER-28",
        "Location WT - Header vs Query Scoping Trap",
        "Attempt to create Location Work Template passing locationId in headers/body instead of query string",
        "Company Default exists. Client calls POST /api/companies/{companyId}/worktemplates/fixed passing locationId in header or JSON body, but omitting ?locationId= in URL query.",
        "HTTP 400 Bad Request. Error Code: Cit.Attendance:1010 ('Company default already exists.'). EXPLANATION: Backend only binds locationId from [FromQuery]. Because query is missing, server assumes Company Default creation and rejects because CDWT already exists.",
        "P1", "defect-trap", "dev", "Not-Run",
        "[Scenario B.2] Scoping trap: Passing locationId in header/body causes server to interpret request as second CDWT and throw 1010.",
        "User Scenario B & Architecture Analysis"
    )
]

start_row = 24
for idx, tc in enumerate(new_test_cases):
    row_num = start_row + idx
    for col_idx, val in enumerate(tc, start=1):
        ws.cell(row=row_num, column=col_idx, value=val)

wb.save(wb_path)
print(f"Successfully added {len(new_test_cases)} user test cases to Master Consolidated Excel (rows {start_row} to {start_row + len(new_test_cases) - 1})!")

