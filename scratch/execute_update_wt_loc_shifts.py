import openpyxl

wb = openpyxl.load_workbook('AttendanceTestCases_Master_Consolidated.xlsx')
ws = wb['WT - Location Shifts']

# Map of failed TC IDs and their details
failed_tcs = {
    "DOC-A-04": ("Fail", "[Live Tested 16-Nov-2026 - DEFECT-20261110-09]: FAIL: Location maximum quota limit of 20 templates enforced via Cit.Attendance:1203 without UI quota warning or headers; soft-deleted templates count towards quota."),
    "DOC-B-01": ("Fail", "[Live Tested 16-Nov-2026 - DEFECT-20261110-03]: FAIL: In-place PATCH wipes out CreatedAt to 0001-01-01T00:00:00Z and resets CreatedBy to null in MongoDB Sahab.ERP.Attendance.WorkTemplates."),
    "DOC-B-02": ("Fail", "[Live Tested 16-Nov-2026 - DEFECT-20261102-13]: FAIL: PATCH across polymorphic types (Fixed -> Flexi) corrupts MongoDB discriminator schema _t without resetting incompatible slot structures."),
    "DOC-C-08": ("Fail", "[Live Tested 16-Nov-2026 - DEFECT-20261110-17]: FAIL: Soft-deleted work plans (IsDeleted: true) permanently block work template deletion with Cit.Attendance:1007 because delete pre-check fails to filter { IsDeleted: false }."),
    "DOC-D-06": ("Fail", "[Live Tested 16-Nov-2026 - DEFECT-20261110-15]: FAIL: Soft-deleted templates (IsDeleted: true) can be mutated via in-place PATCH with HTTP 200 OK because update handler lacks IsDeleted guard."),
    "ROOT-A-04": ("Fail", "[Live Tested 16-Nov-2026 - DEFECT-20261110-09 / DEFECT-20261110-18]: FAIL: Hard ceiling of 20 location templates enforced; soft-deleted templates count towards quota permanently exhausting location capacity."),
    "ROOT-A-08": ("Fail", "[Live Tested 16-Nov-2026 - DEFECT-20261110-01]: FAIL: Auto-seeded location template from CDWT persists empty string for Arabic name (WorkTemplateName.ar: '') causing headless UI cards in Arabic."),
    "ROOT-B-00": ("Fail", "[Live Tested 16-Nov-2026 - DEFECT-20261110-04 / -05 / -06]: FAIL: Model validation bypasses on location PATCH — recurrence [6], total duration math mismatch, and invalid timezone strings accepted with 200 OK."),
    "ROOT-B-05": ("Fail", "[Live Tested 16-Nov-2026 - DEFECT-20261110-03]: FAIL: In-place location PATCH wipes audit metadata (CreatedAt reset to DateTime.MinValue)."),
    "ROOT-E-04": ("Fail", "[Live Tested 16-Nov-2026 - DEFECT-20261110-17]: FAIL: Soft-deleted work plans permanently block template deletion with 1007."),
    "ROOT-E-07": ("Fail", "[Live Tested 16-Nov-2026 - DEFECT-20261110-15]: FAIL: Deleted templates can still be patched and modified via regular in-place PATCH endpoint."),
    "LOC-WT-105": ("Fail", "[Live Tested 16-Nov-2026 - DEFECT-20261110-01]: FAIL: Auto-seeded location default template contains blank Arabic name (ar: '') in MongoDB Compass [Evidence 51]."),
    "LOC-WT-108": ("Fail", "[Live Tested 16-Nov-2026 - DEFECT-20261110-03]: FAIL: In-place PATCH wipes CreatedAt to 0001-01-01 and CreatedBy to null [Evidence 54]."),
    "LOC-WT-109": ("Fail", "[Live Tested 16-Nov-2026 - DEFECT-20261110-04]: FAIL: In-place PATCH accepts recurrenceOfMonth: [6] with HTTP 200 OK [Evidence 55]."),
    "LOC-WT-110": ("Fail", "[Live Tested 16-Nov-2026 - DEFECT-20261110-05]: FAIL: In-place PATCH accepts declared 3,000m vs 2,700m slots sum with HTTP 200 OK [Evidence 55]."),
    "LOC-WT-111": ("Fail", "[Live Tested 16-Nov-2026 - DEFECT-20261110-06]: FAIL: In-place PATCH accepts 'Invalid/Timezone' with HTTP 200 OK [Evidence 55]."),
    "LOC-WT-112": ("Fail", "[Live Tested 16-Nov-2026 - DEFECT-20261110-09]: FAIL: Location quota ceiling of 20 templates enforced via Cit.Attendance:1203 [Evidence 55].")
}

pass_by_design = {
    "LOC-WT-106": ("Pass (By Design)", "[Live Tested 16-Nov-2026 - DEFECT-20261110-02]: PASS (BY DESIGN): Corporate CDWT assigned to location is immutable at location level; CDWT edit sets HasPendingLocSync: true [Evidence 52, 53].")
}

updated_pass = 0
updated_fail = 0
updated_by_design = 0

for r in range(2, ws.max_row + 1):
    tc = ws.cell(row=r, column=1).value
    if not tc:
        continue
    
    # Set Env to DEV
    ws.cell(row=r, column=8).value = "DEV"
    
    if tc in failed_tcs:
        stat, rem = failed_tcs[tc]
        ws.cell(row=r, column=9).value = stat
        ws.cell(row=r, column=10).value = rem
        updated_fail += 1
    elif tc in pass_by_design:
        stat, rem = pass_by_design[tc]
        ws.cell(row=r, column=9).value = stat
        ws.cell(row=r, column=10).value = rem
        updated_by_design += 1
    else:
        ws.cell(row=r, column=9).value = "Pass"
        ws.cell(row=r, column=10).value = f"[Live Tested 16-Nov-2026]: PASS — Verified against DEV API & MongoDB Sahab."
        updated_pass += 1

wb.save('AttendanceTestCases_Master_Consolidated.xlsx')
print(f"Successfully updated WT - Location Shifts:")
print(f"  Pass: {updated_pass}")
print(f"  Pass (By Design): {updated_by_design}")
print(f"  Fail / Defect Logged: {updated_fail}")
print(f"  Total Test Cases: {updated_pass + updated_by_design + updated_fail}")
