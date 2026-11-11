import openpyxl, sys
sys.stdout.reconfigure(encoding='utf-8')

wb_path = 'AttendanceTestCases_Master_Consolidated.xlsx'
wb = openpyxl.load_workbook(wb_path)
ws = wb['User Scenarios (Add Here)']

new_test_cases = [
    (
        "USER-05",
        "Company Default - Setup Sequence",
        "Configure Company Default Work Template / Calendar BEFORE any location is added (0 locations)",
        "Company exists in Company Service with 0 active work locations. Call POST /api/companies/{companyId}/worktemplates/fixed (no locationId) with valid payload.",
        "HTTP 200 'Fixed work template created'. PERSISTENCE: 1 Company Default WT created in Sahab > ERP.Attendance.WorkTemplates (LocationId=00000000-..., IsDefault=true, Version=1.0). CASCADE: 0 location templates and 0 work plans provisioned. No error raised.",
        "P1", "functional", "dev", "Not-Run",
        "[User Scenario 1] Pre-location configuration: company default successfully created; cascade gracefully handles 0 locations without error.",
        "User Understanding & Spec C-03"
    ),
    (
        "USER-06",
        "Company Default - Setup Sequence",
        "Configure Company Default Work Template / Calendar AFTER locations are added (Active Locations Cascade)",
        "Company has ≥2 active work locations in Company Service. Call POST /api/companies/{companyId}/worktemplates/fixed (no locationId).",
        "HTTP 200 OK. PERSISTENCE: 1 Company Default WT (IsDefault=true, Version=1.0). CASCADE: N Location Default WTs (IsCompanyLinked=true, LOC0001...) and N Default Work Plans (LOCWOPL, IsDefault=true) auto-provisioned in Sahab database.",
        "P1", "functional", "dev", "Not-Run",
        "[User Scenario 2A] Post-location configuration: full cascade provisioning runs across all active locations.",
        "User Understanding & Spec C-01"
    ),
    (
        "USER-07",
        "Company Default - Late Location Sync",
        "New work location added to Company Service AFTER Company Default WT was already configured",
        "Company already has CDWT v1.0. A new location (e.g. Loc3) is added in Company Service. Admin calls POST /api/companies/{companyId}/worktemplates/apply-sync.",
        "HTTP 200 OK. Sync service detects Loc3 lacks company-linked template. Automatically provisions 1 Location Default WT (LOC0003) and 1 Default Work Plan (LOCWOPL) for Loc3 (result.templatesProvisioned=1).",
        "P1", "integration", "dev", "Not-Run",
        "[User Scenario 2B] Late-added location sync: apply-sync provisions missing defaults for new locations.",
        "User Understanding & Spec G-07"
    ),
    (
        "USER-08",
        "Company Default - One Default Rule (POST)",
        "Attempt to configure Flexi / Split Company Default when Fixed Company Default is already configured",
        "Company already has an active Company Default WT (Fixed, v1.0). Caller submits POST /api/companies/{companyId}/worktemplates/flexi (or /split) with no locationId.",
        "HTTP 400 Bad Request. Error Code: Cit.Attendance:1010 ('Company default already exists.'). PERSISTENCE: NO new document written, NO cascade runs. Existing company default remains untouched.",
        "P1", "negative", "dev", "Not-Run",
        "[User Scenario 3A] One-default guard on POST: second company default of any regular type is strictly rejected.",
        "User Understanding & Spec B-05"
    ),
    (
        "USER-09",
        "Company Default - Type Change on Edit (PATCH)",
        "Edit existing Fixed Company Default to Flexi / Split via PATCH endpoint (Allowed Type Migration)",
        "Company has active Fixed CDWT v1.0. Admin calls PATCH /api/companies/{companyId}/worktemplates/flexi/{v1Id} (no locationId) with valid Flexi pattern.",
        "HTTP 200 OK 'Company default work template patched'. Old Fixed v1.0 marked Status=Archived(3), IsSuperseded=true, IsDefault=false. NEW document v2.0 created with TemplateType=Flexi(2), IsDefault=true, Status=Active(1), HasPendingLocSync=true. Version chain continues (1.0 -> 2.0).",
        "P1", "functional", "dev", "Not-Run",
        "[User Scenario 3B] Type migration on PATCH: editing company default across regular types creates new version.",
        "User Understanding & Spec D-03"
    ),
    (
        "USER-10",
        "Company Default - Guard Violations on Edit (PATCH)",
        "Verify invalid PATCH attempts on Company Default (ShortCode edit, superseded version, roster template cross-type)",
        "1. PATCH /fixed/{id} with new shortCode. 2. PATCH on an archived v1.0 ID when v2.0 is active. 3. PATCH /fixed/{rosterTemplateId}.",
        "1. HTTP 400 Cit.Attendance:1107 ('Short code cannot be changed'). 2. HTTP 400 InvalidState ('Only active default company work templates can be updated'). 3. HTTP 400 Cit.Attendance:1105 ('Roster template cannot be changed to another type').",
        "P2", "negative", "dev", "Not-Run",
        "[User Scenario 3C] Guard violations on PATCH: shortCode immutability and state guards enforced.",
        "User Understanding & Spec D-06, D-07, B-04"
    )
]

start_row = 6
for idx, tc in enumerate(new_test_cases):
    row_num = start_row + idx
    for col_idx, val in enumerate(tc, start=1):
        ws.cell(row=row_num, column=col_idx, value=val)

wb.save(wb_path)
print(f"Successfully added {len(new_test_cases)} user test cases to Master Consolidated Excel (rows {start_row} to {start_row + len(new_test_cases) - 1})!")

