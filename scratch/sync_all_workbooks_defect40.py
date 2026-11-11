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
from build_post_overtime import build_post_overtime_tcs
from build_get_tcs import build_get_tcs
from build_patch_tcs import build_patch_tcs
from build_delete_tcs import build_delete_tcs
from build_bva_ep_tcs import build_bva_ep_tcs
from build_business_tcs import build_business_tcs

# Compile all 147 test cases
all_tcs = (
    create_test_suite() +
    build_post_break_tcs() +
    build_post_grace_tcs() +
    build_post_overtime_tcs() +
    build_get_tcs() +
    build_patch_tcs() +
    build_delete_tcs() +
    build_bva_ep_tcs() +
    build_business_tcs()
)
print(f"Total compiled test cases: {len(all_tcs)}")

# Load DTO test cases
from add_policies_dto_validations_sheet import get_dto_test_cases
dto_cases = get_dto_test_cases()

# Add POL-DTO-61, 62, 63 if not present
existing_dto_ids = [c["TC ID"] for c in dto_cases]
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
        "Manual Status": "Pass",
        "Actual HTTP Code": "200 OK",
        "Actual Server Response / Notes": "Policy created successfully. MongoDB Compass confirms TenantName: {'en': 'Attendance'} and TenantId are pre-populated by server. Client payload must not include tenantName or id.",
        "Known Defect / QA Reference": "DEFECT-20261105-02 (Server Pre-Population Contract)"
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

print(f"Total DTO test cases to write: {len(dto_cases)}")

# 15 DTO Headers
DTO_HEADERS = [
    "TC ID", "Category", "Policy Type", "Field Under Test", "Test Scenario / Edge Case",
    "HTTP Method", "Endpoint Route", "Sample Request Payload (JSON)", "Expected HTTP & Code",
    "Pri", "Automation Status", "Manual Status", "Actual HTTP Code",
    "Actual Server Response / Notes", "Known Defect / QA Reference"
]

DTO_COL_WIDTHS = {
    1: 16, 2: 24, 3: 20, 4: 25, 5: 45, 6: 12, 7: 42,
    8: 48, 9: 25, 10: 10, 11: 18, 12: 15, 13: 18, 14: 40, 15: 32
}

def render_dto_sheet(ws, cases):
    ws.views.sheetView[0].showGridLines = True
    ws.row_dimensions[1].height = 30
    
    hdr_fill = PatternFill(start_color="1B365D", end_color="1B365D", fill_type="solid")
    hdr_font = Font(name="Calibri", size=10, bold=True, color="FFFFFF")
    hdr_align = Alignment(horizontal="center", vertical="center", wrap_text=True)
    
    thin_side = Side(border_style="thin", color="CBD5E1")
    cell_border = Border(left=thin_side, right=thin_side, top=thin_side, bottom=thin_side)
    
    zebra_fill = PatternFill(start_color="F8FAFC", end_color="F8FAFC", fill_type="solid")
    white_fill = PatternFill(start_color="FFFFFF", end_color="FFFFFF", fill_type="solid")
    
    data_font = Font(name="Calibri", size=9, color="1E293B")
    data_font_bold = Font(name="Calibri", size=9, bold=True, color="1E293B")
    
    align_center = Alignment(horizontal="center", vertical="center", wrap_text=True)
    align_left = Alignment(horizontal="left", vertical="center", wrap_text=True)
    
    p0_fill = PatternFill(start_color="FEE2E2", end_color="FEE2E2", fill_type="solid")
    p0_font = Font(name="Calibri", size=9, bold=True, color="991B1B")
    p1_fill = PatternFill(start_color="FFEDD5", end_color="FFEDD5", fill_type="solid")
    p1_font = Font(name="Calibri", size=9, bold=True, color="C2410C")
    p2_fill = PatternFill(start_color="FEF3C7", end_color="FEF3C7", fill_type="solid")
    p2_font = Font(name="Calibri", size=9, bold=True, color="92400E")
    
    pass_fill = PatternFill(start_color="DCFCE7", end_color="DCFCE7", fill_type="solid")
    pass_font = Font(name="Calibri", size=9, bold=True, color="166534")
    
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
            cell.font = data_font
            cell.border = cell_border
            
            if c_idx in [1, 3, 6, 9, 10, 11, 12, 13]:
                cell.alignment = align_center
                if c_idx == 1:
                    cell.font = data_font_bold
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
                    
            if h in ["Automation Status", "Manual Status"] and str(val).strip().lower() in ["pass", "ready"]:
                cell.fill = pass_fill
                cell.font = pass_font
                
    for c_idx, w in DTO_COL_WIDTHS.items():
        ws.column_dimensions[get_column_letter(c_idx)].width = w
        
    ws.auto_filter.ref = f"A1:{get_column_letter(len(DTO_HEADERS))}{len(cases)+1}"
    ws.freeze_panes = "A2"

# 1. Update Attendance_Policies_Manual_API_TestCases_MongoDB.xlsx
pol_file = "Attendance_Policies_Manual_API_TestCases_MongoDB.xlsx"
pol_wb = openpyxl.load_workbook(pol_file)

# Remove any old overlong sheet
for s in ["Policies - Manual DTO Validations", "Policies - DTO Validations"]:
    if s in pol_wb.sheetnames:
        del pol_wb[s]

ws_dto_pol = pol_wb.create_sheet(title="Policies - DTO Validations")
render_dto_sheet(ws_dto_pol, dto_cases)
pol_wb.save(pol_file)
print(f"Updated dedicated workbook: {pol_file} with 'Policies - DTO Validations' ({len(dto_cases)} cases)!")

# 2. Update AttendanceTestCases_Master_Consolidated.xlsx
master_file = "AttendanceTestCases_Master_Consolidated.xlsx"
master_wb = openpyxl.load_workbook(master_file)

# Remove invalid/overlong sheet
if "Policies - Manual DTO Validations" in master_wb.sheetnames:
    del master_wb["Policies - Manual DTO Validations"]
    print("Removed overlong sheet 'Policies - Manual DTO Validations' from master workbook.")

if "Policies - DTO Validations" in master_wb.sheetnames:
    del master_wb["Policies - DTO Validations"]

ws_dto_master = master_wb.create_sheet(title="Policies - DTO Validations")
render_dto_sheet(ws_dto_master, dto_cases)
print(f"Added clean sheet 'Policies - DTO Validations' ({len(dto_cases)} cases) to master workbook.")

# Update INDEX sheet
if "INDEX" in master_wb.sheetnames:
    idx_ws = master_wb["INDEX"]
    
    # 1. Update Attendance Policies row (Row 10)
    for r in range(5, idx_ws.max_row + 1):
        mod_name = str(idx_ws.cell(r, 2).value or "").strip()
        if mod_name.lower() == "attendance policies":
            p0 = sum(1 for t in all_tcs if t.get("Priority") == "P0")
            p1 = sum(1 for t in all_tcs if t.get("Priority") == "P1")
            p2 = sum(1 for t in all_tcs if t.get("Priority") == "P2")
            p3 = sum(1 for t in all_tcs if t.get("Priority") == "P3")
            idx_ws.cell(r, 3, len(all_tcs)) # 147
            idx_ws.cell(r, 4, p0)
            idx_ws.cell(r, 5, p1)
            idx_ws.cell(r, 6, p2)
            idx_ws.cell(r, 7, p3)
            print(f"Updated INDEX Row {r} (Attendance Policies): Total={len(all_tcs)}, P0={p0}, P1={p1}, P2={p2}, P3={p3}")
            break

    # 2. Remove any duplicate 'Policies - Manual DTO Validations' row in INDEX
    for r in range(idx_ws.max_row, 4, -1):
        mod_name = str(idx_ws.cell(r, 2).value or "").strip()
        if "policies - manual dto validations" in mod_name.lower():
            idx_ws.delete_rows(r)
            print(f"Deleted duplicate INDEX row {r} for 'Policies - Manual DTO Validations'.")

    # 3. Update 'Policies - DTO Validations' row in INDEX
    dto_p0 = sum(1 for t in dto_cases if t.get("Pri") == "P0")
    dto_p1 = sum(1 for t in dto_cases if t.get("Pri") == "P1")
    dto_p2 = sum(1 for t in dto_cases if t.get("Pri") == "P2")
    
    dto_found = False
    for r in range(5, idx_ws.max_row + 1):
        mod_name = str(idx_ws.cell(r, 2).value or "").strip()
        if "policies - dto validations" in mod_name.lower():
            idx_ws.cell(r, 1, 18)
            idx_ws.cell(r, 2, "Policies - DTO Validations")
            idx_ws.cell(r, 3, len(dto_cases))
            idx_ws.cell(r, 4, dto_p0)
            idx_ws.cell(r, 5, dto_p1)
            idx_ws.cell(r, 6, dto_p2)
            idx_ws.cell(r, 7, 0)
            dto_found = True
            print(f"Updated INDEX Row {r} (Policies - DTO Validations): Total={len(dto_cases)}, P0={dto_p0}, P1={dto_p1}, P2={dto_p2}")
            break
            
    # 4. Update TOTAL row
    total_row = None
    for r in range(5, idx_ws.max_row + 1):
        val = str(idx_ws.cell(r, 1).value or "").strip().upper()
        if "TOTAL" in val:
            total_row = r
            break
            
    if total_row:
        # Sum from row 5 up to total_row - 1
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
        print(f"Updated INDEX Row {total_row} (TOTAL): Modules={num_modules}, Total={tot_tcs}, P0={tot_p0}, P1={tot_p1}, P2={tot_p2}, P3={tot_p3}")

master_wb.save(master_file)
print("Master workbook saved successfully without openpyxl warnings!")

