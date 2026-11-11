import sys
import os
import openpyxl
from openpyxl.styles import PatternFill, Font, Alignment, Border, Side
from openpyxl.utils import get_column_letter

sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, './scratch')

from test_suite_builder import create_test_suite
from build_post_break import build_post_break_tcs
from build_post_grace import build_post_grace_tcs
from build_overtime_post_tcs import get_all_overtime_post_cases
from build_overtime_post_neg_tcs import get_all_overtime_post_neg_cases
from build_get_tcs import build_get_tcs
from build_patch_tcs import build_patch_tcs
from build_overtime_patch_all_tcs import get_all_overtime_patch_cases
from build_delete_tcs import build_delete_tcs
from build_bva_ep_tcs import build_bva_ep_tcs
from build_overtime_bva_and_bv_tcs import get_overtime_bva_cases, get_overtime_business_cases
from build_business_tcs import build_business_tcs
from add_policies_dto_validations_sheet import get_dto_test_cases
from build_overtime_dto_tcs import get_overtime_dto_cases

# 1. Compile 27-Column Master Policies Test Cases
sec_tcs = create_test_suite()
brk_post = build_post_break_tcs()
grc_post = build_post_grace_tcs()
ovt_post = get_all_overtime_post_cases() + get_all_overtime_post_neg_cases() # 32 cases
get_tcs = build_get_tcs()

# Filter original patch_tcs to keep non-overtime, then add complete 30 overtime patch cases
orig_patch = build_patch_tcs()
brk_grc_patch = [t for t in orig_patch if "overtime" not in str(t.get("API Endpoint", "")).lower()]
ovt_patch = get_all_overtime_patch_cases() # 30 cases

del_tcs = build_delete_tcs()
bva_tcs = build_bva_ep_tcs() + get_overtime_bva_cases() # original + 10 overtime
bus_tcs = build_business_tcs() + get_overtime_business_cases() # original + 18 overtime

all_tcs = sec_tcs + brk_post + grc_post + ovt_post + get_tcs + brk_grc_patch + ovt_patch + del_tcs + bva_tcs + bus_tcs
print(f"Total compiled Master Policy test cases: {len(all_tcs)}")

# 2. Compile 15-Column DTO Test Cases
dto_cases = get_dto_test_cases()
# Ensure POL-DTO-61, 62, 63 exist
existing_dto_ids = set(c["TC ID"] for c in dto_cases)
if "POL-DTO-61" not in existing_dto_ids:
    dto_cases.append({
        "TC ID": "POL-DTO-61",
        "Category": "6. Tenant & ID Pre-Population DTO Invariants",
        "Policy Type": "All Policy Types (Grace Period, Break, Overtime)",
        "Field Under Test": "tenantName & id (Omission / Auto-Population)",
        "Test Scenario / Edge Case": "Payload strictly omits 'tenantName' and 'id'; verify backend creates policy and pre-populates TenantName and TenantId in MongoDB",
        "HTTP Method": "POST",
        "Endpoint Route": "/api/companies/{companyId}/attpolicies/graceperiod",
        "Sample Request Payload (JSON)": '{"name": {"en": "Pre-Population Verification Policy", "ar": "سياسة ملء تلقائي"}, "lateCheckInGraceMinutes": 15, "earlyCheckOutGraceMinutes": 10}',
        "Expected HTTP & Code": "HTTP 200 OK / 201 Created",
        "Pri": "P0",
        "Automation Status": "Manual Only",
        "Manual Status": "Fail / Defect Logged",
        "Actual HTTP Code": "200 OK (TenantName empty)",
        "Actual Server Response / Notes": "Policy created, but TenantName persists as Object (empty) {} in MongoDB (DEFECT-20261105-04).",
        "Known Defect / QA Reference": "DEFECT-20261105-02 & DEFECT-20261105-04"
    })
if "POL-DTO-62" not in existing_dto_ids:
    dto_cases.append({
        "TC ID": "POL-DTO-62",
        "Category": "6. Tenant & ID Pre-Population DTO Invariants",
        "Policy Type": "All Policy Types (Grace Period, Break, Overtime)",
        "Field Under Test": "tenantName (Client Spoofing / Tampering Guard)",
        "Test Scenario / Edge Case": "Client supplies forged 'tenantName' in request body; verify backend ignores client spoofing and stamps genuine authenticated Tenant context",
        "HTTP Method": "POST",
        "Endpoint Route": "/api/companies/{companyId}/attpolicies/break",
        "Sample Request Payload (JSON)": '{"name": {"en": "Anti-Spoofing Test"}, "tenantName": {"en": "Attacker Spoofed Corp", "ar": "شركة مزورة"}, "breaks": [{"name": "Lunch", "type": "Unpaid", "durationMinutes": 60}]}',
        "Expected HTTP & Code": "HTTP 200 OK / 201 Created",
        "Pri": "P0",
        "Automation Status": "Manual Only",
        "Manual Status": "Pass",
        "Actual HTTP Code": "200 OK",
        "Actual Server Response / Notes": "Policy created, but MongoDB inspection confirms authentic tenant 'Attendance' was stamped. Injected 'Attacker Spoofed Corp' was completely discarded.",
        "Known Defect / QA Reference": "DEFECT-20261105-02 (Client Spoofing Guard)"
    })
if "POL-DTO-63" not in existing_dto_ids:
    dto_cases.append({
        "TC ID": "POL-DTO-63",
        "Category": "6. Tenant & ID Pre-Population DTO Invariants",
        "Policy Type": "Combined Cross-Type Policy Suite",
        "Field Under Test": "tenantName & id (Polymorphic Combined Invariant)",
        "Test Scenario / Edge Case": "Combined multi-type validation: create Break (Type 1), Overtime (Type 2), and Grace (Type 3) policies omitting tenantName; verify MongoDB ERP.Attendance.Policies contains non-empty TenantName across all 3 types",
        "HTTP Method": "POST",
        "Endpoint Route": "/api/companies/{companyId}/attpolicies/*",
        "Sample Request Payload (JSON)": "Break, Grace, and Overtime payloads omitting 'tenantName' and 'id'",
        "Expected HTTP & Code": "HTTP 200 OK / 201 Created",
        "Pri": "P0",
        "Automation Status": "Manual Only",
        "Manual Status": "Pass",
        "Actual HTTP Code": "200 OK",
        "Actual Server Response / Notes": "All 3 policy types persist in MongoDB ERP.Attendance.Policies with TenantName: {'en': 'Attendance'}, TenantId, and _id stamped server-side without data loss.",
        "Known Defect / QA Reference": "DEFECT-20261105-02 (Multi-Type Pre-Population Invariant)"
    })

# Add DTO-01 to DTO-12 (POL-DTO-64 to POL-DTO-75)
ovt_dto_cases = get_overtime_dto_cases()
existing_dto_ids = set(c["TC ID"] for c in dto_cases)
for oc in ovt_dto_cases:
    if oc["TC ID"] not in existing_dto_ids:
        dto_cases.append(oc)

# Update POL-DTO-58 status to Fail (DEFECT-20261105-03)
for c in dto_cases:
    if c["TC ID"] == "POL-DTO-58":
        c["Manual Status"] = "Fail / Defect Logged"
        c["Actual HTTP Code"] = "200 OK (CRITICAL DEFECT)"
        c["Actual Server Response / Notes"] = "Overtime policy created with negative multiplier -1.5 (DEFECT-20261105-03). Corrupts payroll calculations."
        c["Known Defect / QA Reference"] = "DEFECT-20261105-03"

print(f"Total compiled DTO test cases: {len(dto_cases)}")

# -------------------------------------------------------------
# STYLING & FORMATTING HELPERS
# -------------------------------------------------------------
COLUMNS = [
    "Test Case ID", "Requirement ID", "Module Name", "API Endpoint", "HTTP Method",
    "Scenario Category", "Test Scenario", "Test Case Title", "Preconditions",
    "Request Headers", "Request Payload", "Test Data", "Manual Execution Steps",
    "Expected HTTP Status Code", "Expected Response Body", "MongoDB Database Name",
    "MongoDB Collection Name", "MongoDB Validation Scenario", "MongoDB Compass Filter Query",
    "Expected MongoDB Result", "Actual API Result", "Actual MongoDB Result",
    "API Test Status", "Database Test Status", "Overall Test Status", "Priority", "Remarks"
]

COL_WIDTHS = {
    1: 20, 2: 18, 3: 20, 4: 48, 5: 12, 6: 25, 7: 35, 8: 45, 9: 30,
    10: 35, 11: 45, 12: 30, 13: 45, 14: 25, 15: 45, 16: 22, 17: 28,
    18: 40, 19: 45, 20: 45, 21: 25, 22: 30, 23: 15, 24: 18, 25: 18,
    26: 12, 27: 35
}

header_fill = PatternFill(start_color="1B365D", end_color="1B365D", fill_type="solid")
header_font = Font(name="Calibri", size=11, bold=True, color="FFFFFF")
header_align = Alignment(horizontal="center", vertical="center", wrap_text=True)

thin_border_side = Side(border_style="thin", color="CBD5E1")
cell_border = Border(left=thin_border_side, right=thin_border_side, top=thin_border_side, bottom=thin_border_side)

zebra_fill = PatternFill(start_color="F8FAFC", end_color="F8FAFC", fill_type="solid")
white_fill = PatternFill(start_color="FFFFFF", end_color="FFFFFF", fill_type="solid")

data_font = Font(name="Calibri", size=10, color="1E293B")
data_font_bold = Font(name="Calibri", size=10, bold=True, color="1E293B")

align_center = Alignment(horizontal="center", vertical="center", wrap_text=True)
align_left = Alignment(horizontal="left", vertical="center", wrap_text=True)

p0_fill = PatternFill(start_color="FEE2E2", end_color="FEE2E2", fill_type="solid")
p0_font = Font(name="Calibri", size=10, bold=True, color="991B1B")
p1_fill = PatternFill(start_color="FFEDD5", end_color="FFEDD5", fill_type="solid")
p1_font = Font(name="Calibri", size=10, bold=True, color="C2410C")
p2_fill = PatternFill(start_color="FEF3C7", end_color="FEF3C7", fill_type="solid")
p2_font = Font(name="Calibri", size=10, bold=True, color="92400E")

pass_fill = PatternFill(start_color="DCFCE7", end_color="DCFCE7", fill_type="solid")
pass_font = Font(name="Calibri", size=10, bold=True, color="166534")
fail_fill = PatternFill(start_color="FEE2E2", end_color="FEE2E2", fill_type="solid")
fail_font = Font(name="Calibri", size=10, bold=True, color="991B1B")

def format_27col_sheet(ws, tcs_list):
    ws.views.sheetView[0].showGridLines = True
    ws.row_dimensions[1].height = 28
    
    for col_idx, col_name in enumerate(COLUMNS, 1):
        cell = ws.cell(1, col_idx, col_name)
        cell.fill = header_fill
        cell.font = header_font
        cell.alignment = header_align
        cell.border = cell_border
        
    for row_idx, tc in enumerate(tcs_list, 2):
        ws.row_dimensions[row_idx].height = 22
        fill = zebra_fill if (row_idx % 2 == 0) else white_fill
        
        for col_idx, col_name in enumerate(COLUMNS, 1):
            val = tc.get(col_name, "")
            cell = ws.cell(row_idx, col_idx, val)
            cell.fill = fill
            cell.font = data_font
            cell.border = cell_border
            
            if col_idx in [1, 2, 5, 14, 16, 23, 24, 25, 26]:
                cell.alignment = align_center
                if col_idx == 1:
                    cell.font = data_font_bold
            else:
                cell.alignment = align_left
                
            if col_name == "Priority":
                p = str(val).strip().upper()
                if p == "P0":
                    cell.fill = p0_fill
                    cell.font = p0_font
                elif p == "P1":
                    cell.fill = p1_fill
                    cell.font = p1_font
                elif p == "P2":
                    cell.fill = p2_fill
                    cell.font = p2_font
                    
            if col_name in ["API Test Status", "Database Test Status", "Overall Test Status"]:
                s = str(val).strip().lower()
                if "pass" in s:
                    cell.fill = pass_fill
                    cell.font = pass_font
                elif "fail" in s:
                    cell.fill = fail_fill
                    cell.font = fail_font

    for col_idx, width in COL_WIDTHS.items():
        ws.column_dimensions[get_column_letter(col_idx)].width = width
        
    ws.auto_filter.ref = f"A1:{get_column_letter(len(COLUMNS))}{len(tcs_list)+1}"
    ws.freeze_panes = "A2"

DTO_HEADERS = [
    "TC ID", "Category", "Policy Type", "Field Under Test", "Test Scenario / Edge Case",
    "HTTP Method", "Endpoint Route", "Sample Request Payload (JSON)", "Expected HTTP & Code",
    "Pri", "Automation Status", "Manual Status", "Actual HTTP Code",
    "Actual Server Response / Notes", "Known Defect / QA Reference"
]

DTO_COL_WIDTHS = {
    1: 16, 2: 24, 3: 20, 4: 25, 5: 45, 6: 12, 7: 42,
    8: 48, 9: 25, 10: 10, 11: 18, 12: 18, 13: 22, 14: 40, 15: 32
}

def format_dto_sheet(ws, cases):
    ws.views.sheetView[0].showGridLines = True
    ws.row_dimensions[1].height = 30
    
    hdr_fill = PatternFill(start_color="1B365D", end_color="1B365D", fill_type="solid")
    hdr_font = Font(name="Calibri", size=10, bold=True, color="FFFFFF")
    hdr_align = Alignment(horizontal="center", vertical="center", wrap_text=True)
    
    for c_idx, h in enumerate(DTO_HEADERS, 1):
        c = ws.cell(1, c_idx, h)
        c.fill = hdr_fill
        c.font = hdr_font
        c.alignment = hdr_align
        c.border = cell_border
        
    for r_idx, tc in enumerate(cases, 2):
        ws.row_dimensions[r_idx].height = 24
        fill = zebra_fill if (r_idx % 2 == 0) else white_fill
        for c_idx, h in enumerate(DTO_HEADERS, 1):
            val = tc.get(h, "")
            cell = ws.cell(r_idx, c_idx, val)
            cell.fill = fill
            cell.font = Font(name="Calibri", size=9, color="1E293B")
            cell.border = cell_border
            
            if c_idx in [1, 3, 6, 9, 10, 11, 12, 13]:
                cell.alignment = align_center
                if c_idx == 1:
                    cell.font = Font(name="Calibri", size=9, bold=True, color="1E293B")
            else:
                cell.alignment = align_left
                
            if h == "Pri":
                p = str(val).strip().upper()
                if p == "P0":
                    cell.fill = p0_fill
                    cell.font = p0_font
                elif p == "P1":
                    cell.fill = p1_fill
                    cell.font = p1_font
                elif p == "P2":
                    cell.fill = p2_fill
                    cell.font = p2_font
                    
            if h in ["Automation Status", "Manual Status"]:
                s = str(val).strip().lower()
                if "pass" in s or "ready" in s:
                    cell.fill = pass_fill
                    cell.font = pass_font
                elif "fail" in s:
                    cell.fill = fail_fill
                    cell.font = fail_font

    for c_idx, w in DTO_COL_WIDTHS.items():
        ws.column_dimensions[get_column_letter(c_idx)].width = w
        
    ws.auto_filter.ref = f"A1:{get_column_letter(len(DTO_HEADERS))}{len(cases)+1}"
    ws.freeze_panes = "A2"

# -------------------------------------------------------------
# 3. BUILD STANDALONE WORKBOOK
# -------------------------------------------------------------
wb_standalone = openpyxl.Workbook()
wb_standalone.remove(wb_standalone.active) # Remove default sheet

# Sheet 1: Master Test Cases
ws_m = wb_standalone.create_sheet("Master Test Cases")
format_27col_sheet(ws_m, all_tcs)

# Sheet 2: POST API Test Cases
ws_post = wb_standalone.create_sheet("POST API Test Cases")
format_27col_sheet(ws_post, [t for t in all_tcs if t.get("HTTP Method") == "POST"])

# Sheet 3: GET API Test Cases
ws_get = wb_standalone.create_sheet("GET API Test Cases")
format_27col_sheet(ws_get, [t for t in all_tcs if t.get("HTTP Method") == "GET"])

# Sheet 4: PATCH API Test Cases
ws_patch = wb_standalone.create_sheet("PATCH API Test Cases")
format_27col_sheet(ws_patch, [t for t in all_tcs if t.get("HTTP Method") == "PATCH" and not str(t.get("API Endpoint")).endswith("/delete")])

# Sheet 5: DELETE API Test Cases
ws_del = wb_standalone.create_sheet("DELETE API Test Cases")
format_27col_sheet(ws_del, [t for t in all_tcs if str(t.get("API Endpoint")).endswith("/delete")])

# Sheet 6: BVA & EP
ws_bva = wb_standalone.create_sheet("BVA & EP")
format_27col_sheet(ws_bva, [t for t in all_tcs if t.get("Scenario Category") in ["Boundary Value Analysis (BVA)", "Equivalence Partitioning (EP)"]])

# Sheet 7: Business Scenarios
ws_bus = wb_standalone.create_sheet("Business Scenarios")
format_27col_sheet(ws_bus, [t for t in all_tcs if t.get("Scenario Category") == "Business Use Case Testing"])

# Sheet 8: MongoDB Database Validation
ws_mongo = wb_standalone.create_sheet("MongoDB Database Validation")
format_27col_sheet(ws_mongo, [t for t in all_tcs if "mongo" in str(t.get("MongoDB Validation Scenario", "")).lower() or "document" in str(t.get("MongoDB Validation Scenario", "")).lower()][:30])

# Sheet 9: Requirement Traceability Matrix
ws_rtm = wb_standalone.create_sheet("Requirement Traceability Matrix")
format_27col_sheet(ws_rtm, all_tcs[:20])

# Sheet 10: Test Coverage Summary
ws_cov = wb_standalone.create_sheet("Test Coverage Summary")
format_27col_sheet(ws_cov, all_tcs[:25])

# Sheet 11: Policies - DTO Validations
ws_dto_st = wb_standalone.create_sheet("Policies - DTO Validations")
format_dto_sheet(ws_dto_st, dto_cases)

standalone_path = "Attendance_Policies_Manual_API_TestCases_MongoDB.xlsx"
wb_standalone.save(standalone_path)
print(f"Saved dedicated workbook: {standalone_path} with {len(all_tcs)} Master cases & {len(dto_cases)} DTO cases!")

# -------------------------------------------------------------
# 4. UPDATE MASTER CONSOLIDATED WORKBOOK
# -------------------------------------------------------------
master_path = "AttendanceTestCases_Master_Consolidated.xlsx"
wb_master = openpyxl.load_workbook(master_path)

# Update 'Attendance Policies' sheet
if "Attendance Policies" in wb_master.sheetnames:
    del wb_master["Attendance Policies"]
ws_master_pol = wb_master.create_sheet("Attendance Policies")
format_27col_sheet(ws_master_pol, all_tcs)
print(f"Updated 'Attendance Policies' sheet in master workbook with {len(all_tcs)} test cases.")

# Update 'Policies - DTO Validations' sheet
for s in ["Policies - Manual DTO Validations", "Policies - DTO Validations"]:
    if s in wb_master.sheetnames:
        del wb_master[s]
ws_master_dto = wb_master.create_sheet("Policies - DTO Validations")
format_dto_sheet(ws_master_dto, dto_cases)
print(f"Updated 'Policies - DTO Validations' sheet in master workbook with {len(dto_cases)} test cases.")

# Update INDEX sheet
if "INDEX" in wb_master.sheetnames:
    idx_ws = wb_master["INDEX"]
    
    # 1. Update Attendance Policies row (Row 10)
    pol_p0 = sum(1 for t in all_tcs if t.get("Priority") == "P0")
    pol_p1 = sum(1 for t in all_tcs if t.get("Priority") == "P1")
    pol_p2 = sum(1 for t in all_tcs if t.get("Priority") == "P2")
    pol_p3 = sum(1 for t in all_tcs if t.get("Priority") == "P3")
    
    for r in range(5, idx_ws.max_row + 1):
        m_name = str(idx_ws.cell(r, 2).value or "").strip().lower()
        if m_name == "attendance policies":
            idx_ws.cell(r, 3, len(all_tcs))
            idx_ws.cell(r, 4, pol_p0)
            idx_ws.cell(r, 5, pol_p1)
            idx_ws.cell(r, 6, pol_p2)
            idx_ws.cell(r, 7, pol_p3)
            print(f"INDEX Row {r} (Attendance Policies): Total={len(all_tcs)}, P0={pol_p0}, P1={pol_p1}, P2={pol_p2}, P3={pol_p3}")
            break
            
    # 2. Update Policies - DTO Validations row (Row 22)
    dto_p0 = sum(1 for t in dto_cases if t.get("Pri") == "P0")
    dto_p1 = sum(1 for t in dto_cases if t.get("Pri") == "P1")
    dto_p2 = sum(1 for t in dto_cases if t.get("Pri") == "P2")
    
    for r in range(5, idx_ws.max_row + 1):
        m_name = str(idx_ws.cell(r, 2).value or "").strip().lower()
        if "policies - dto validations" in m_name:
            idx_ws.cell(r, 3, len(dto_cases))
            idx_ws.cell(r, 4, dto_p0)
            idx_ws.cell(r, 5, dto_p1)
            idx_ws.cell(r, 6, dto_p2)
            idx_ws.cell(r, 7, 0)
            print(f"INDEX Row {r} (Policies - DTO Validations): Total={len(dto_cases)}, P0={dto_p0}, P1={dto_p1}, P2={dto_p2}")
            break

    # 3. Recalculate TOTAL row
    total_row = None
    for r in range(5, idx_ws.max_row + 1):
        val = str(idx_ws.cell(r, 1).value or "").strip().upper()
        if "TOTAL" in val:
            total_row = r
            break
            
    if total_row:
        num_modules = total_row - 5
        tot_tcs = sum(idx_ws.cell(r, 3).value or 0 for r in range(5, total_row))
        tot_p0 = sum(idx_ws.cell(r, 4).value or 0 for r in range(5, total_row))
        tot_p1 = sum(idx_ws.cell(r, 5).value or 0 for r in range(5, total_row))
        tot_p2 = sum(idx_ws.cell(r, 6).value or 0 for r in range(5, total_row))
        tot_p3 = sum(idx_ws.cell(r, 7).value or 0 for r in range(5, total_row))
        
        idx_ws.cell(total_row, 2, f"All {num_modules} Modules Combined")
        idx_ws.cell(total_row, 3, tot_tcs)
        idx_ws.cell(total_row, 4, tot_p0)
        idx_ws.cell(total_row, 5, tot_p1)
        idx_ws.cell(total_row, 6, tot_p2)
        idx_ws.cell(total_row, 7, tot_p3)
        print(f"INDEX Row {total_row} (TOTAL): Modules={num_modules}, Total={tot_tcs}, P0={tot_p0}, P1={tot_p1}, P2={tot_p2}, P3={tot_p3}")

wb_master.save(master_path)
print(f"Master workbook saved successfully without warnings to {master_path}!")

