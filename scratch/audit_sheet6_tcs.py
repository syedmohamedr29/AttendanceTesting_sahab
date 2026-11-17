# -*- coding: utf-8 -*-
import openpyxl

wb = openpyxl.load_workbook('AttendanceTestCases_Master_Consolidated.xlsx', data_only=True)
sheet = wb['Holiday Calendar - Company']

print(f"Auditing Sheet 6: {sheet.title} ({sheet.max_row} rows)")

tcs = []
for r in range(2, sheet.max_row + 1):
    vals = [sheet.cell(r, c).value for c in range(1, 12)]
    if vals[0]:
        tcs.append((r, vals[0], vals[1], vals[2], vals[3], vals[4], vals[5], vals[6], vals[7], vals[8], vals[9]))

print(f"Loaded {len(tcs)} test cases from Sheet 6.")

# Let's inspect each TC and determine exact status based on live implementation & defects
# For instance:
# DOC-A-01: No token -> HTTP 401 -> PASS
# DOC-A-02: Expired or forged token -> Accepted with 200 OK! (DEFECT-20261029-01) -> FAIL
# DOC-A-03: Token without tenant -> Returns 401/403 or 500? -> Let's verify
# DOC-A-04: Calendar of another company -> Cit.Attendance:1702 -> PASS
# DOC-A-05: Calendar of another tenant -> __tenant ignored -> DEFECT-20261104-01 -> FAIL
# DOC-A-06: Org names from Company service -> CompanyName/TenantName empty in Mongo -> DEFECT-20261105-01 / 20261103-02 -> FAIL
# DOC-B-01: Validation -> Empty shortCode/name -> 500 ValidationException instead of 400 Sbp:Validation -> FAIL (DEFECT-20261028-02)
# DOC-B-02: Create for next year -> Happy path -> PASS
# DOC-B-03: Year not allowed (Y-1 or Y+2) -> Cit.Attendance:1712 -> PASS
# DOC-B-04: Company default already exists -> Cit.Attendance:1713 -> PASS
# DOC-B-05: Location already has calendar -> Location keeps own calendar -> PASS
# DOC-B-06: Deleted locations skipped -> PASS
# DOC-B-07: Holiday dates not checked on create -> Future year 2027 accepted on create -> FAIL (DEFECT-20261103-12)
# DOC-B-08: Company unknown -> 400 Cit.Attendance:1701 -> PASS

print("\nSample TCs analyzed.")
