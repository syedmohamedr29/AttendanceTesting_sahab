import sys
import os
import openpyxl
from openpyxl.styles import PatternFill, Font, Alignment, Border, Side
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.datavalidation import DataValidation

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

# 27 Mandatory Columns
COLUMNS = [
    "Test Case ID",
    "Requirement ID",
    "Module Name",
    "API Endpoint",
    "HTTP Method",
    "Scenario Category",
    "Test Scenario",
    "Test Case Title",
    "Preconditions",
    "Request Headers",
    "Request Payload",
    "Test Data",
    "Manual Execution Steps",
    "Expected HTTP Status Code",
    "Expected Response Body",
    "MongoDB Database Name",
    "MongoDB Collection Name",
    "MongoDB Validation Scenario",
    "MongoDB Compass Filter Query",
    "Expected MongoDB Result",
    "Actual API Result",
    "Actual MongoDB Result",
    "API Test Status",
    "Database Test Status",
    "Overall Test Status",
    "Priority",
    "Remarks"
]

print("Assembling all test cases...")
sec = create_test_suite()
brk = build_post_break_tcs()
grc = build_post_grace_tcs()
ovt = build_post_overtime_tcs()
get_tcs = build_get_tcs()
patch_tcs = build_patch_tcs()
del_tcs = build_delete_tcs()
bva_ep = build_bva_ep_tcs()
bus = build_business_tcs()

all_tcs = sec + brk + grc + ovt + get_tcs + patch_tcs + del_tcs + bva_ep + bus
print(f"Total compiled test cases: {len(all_tcs)}")

# Helper filters
post_tcs = [t for t in all_tcs if t["HTTP Method"] == "POST"]
get_only_tcs = [t for t in all_tcs if t["HTTP Method"] == "GET"]
patch_only_tcs = [t for t in all_tcs if t["HTTP Method"] == "PATCH" and not str(t["API Endpoint"]).endswith("/delete")]
del_only_tcs = [t for t in all_tcs if str(t["API Endpoint"]).endswith("/delete")]
bva_ep_tcs = [t for t in all_tcs if t["Scenario Category"] in ["Boundary Value Analysis (BVA)", "Equivalence Partitioning (EP)"]]
bus_tcs = [t for t in all_tcs if t["Scenario Category"] == "Business Use Case Testing"]

print(f"POST TCs: {len(post_tcs)}")
print(f"GET TCs: {len(get_only_tcs)}")
print(f"PATCH TCs: {len(patch_only_tcs)}")
print(f"DELETE TCs: {len(del_only_tcs)}")
print(f"BVA & EP TCs: {len(bva_ep_tcs)}")
print(f"Business TCs: {len(bus_tcs)}")

# Styling definitions
header_fill = PatternFill(start_color="1B365D", end_color="1B365D", fill_type="solid") # Deep Navy
header_font = Font(name="Calibri", size=11, bold=True, color="FFFFFF")
header_align = Alignment(horizontal="center", vertical="center", wrap_text=True)

zebra_fill = PatternFill(start_color="F8FAFC", end_color="F8FAFC", fill_type="solid") # Slate-50
white_fill = PatternFill(start_color="FFFFFF", end_color="FFFFFF", fill_type="solid")

thin_border_side = Side(border_style="thin", color="CBD5E1")
cell_border = Border(left=thin_border_side, right=thin_border_side, top=thin_border_side, bottom=thin_border_side)

data_font = Font(name="Calibri", size=10, color="1E293B")
data_font_bold = Font(name="Calibri", size=10, bold=True, color="1E293B")

align_center = Alignment(horizontal="center", vertical="center", wrap_text=True)
align_left = Alignment(horizontal="left", vertical="center", wrap_text=True)

# Priority styling
p0_fill = PatternFill(start_color="FEE2E2", end_color="FEE2E2", fill_type="solid") # Red
p0_font = Font(name="Calibri", size=10, bold=True, color="991B1B")

p1_fill = PatternFill(start_color="FFEDD5", end_color="FFEDD5", fill_type="solid") # Orange
p1_font = Font(name="Calibri", size=10, bold=True, color="C2410C")

p2_fill = PatternFill(start_color="FEF3C7", end_color="FEF3C7", fill_type="solid") # Yellow
p2_font = Font(name="Calibri", size=10, bold=True, color="92400E")

p3_fill = PatternFill(start_color="E0F2FE", end_color="E0F2FE", fill_type="solid") # Blue
p3_font = Font(name="Calibri", size=10, bold=True, color="075985")

# Status styling
pass_fill = PatternFill(start_color="DCFCE7", end_color="DCFCE7", fill_type="solid") # Green
pass_font = Font(name="Calibri", size=10, bold=True, color="166534")

# Column Widths mapping
COL_WIDTHS = {
    1: 18,  # Test Case ID
    2: 16,  # Requirement ID
    3: 20,  # Module Name
    4: 38,  # API Endpoint
    5: 12,  # HTTP Method
    6: 25,  # Scenario Category
    7: 35,  # Test Scenario
    8: 45,  # Test Case Title
    9: 35,  # Preconditions
    10: 30, # Request Headers
    11: 45, # Request Payload
    12: 30, # Test Data
    13: 50, # Manual Execution Steps
    14: 25, # Expected HTTP Status Code
    15: 45, # Expected Response Body
    16: 18, # MongoDB Database Name
    17: 28, # MongoDB Collection Name
    18: 45, # MongoDB Validation Scenario
    19: 45, # MongoDB Compass Filter Query
    20: 45, # Expected MongoDB Result
    21: 25, # Actual API Result
    22: 25, # Actual MongoDB Result
    23: 16, # API Test Status
    24: 18, # Database Test Status
    25: 18, # Overall Test Status
    26: 12, # Priority
    27: 35  # Remarks
}

def format_test_sheet(ws, cases, title_prefix=""):
    ws.views.sheetView[0].showGridLines = True
    ws.row_dimensions[1].height = 32
    
    # Headers
    for c_idx, col_name in enumerate(COLUMNS, 1):
        cell = ws.cell(row=1, column=c_idx, value=col_name)
        cell.fill = header_fill
        cell.font = header_font
        cell.alignment = header_align
        cell.border = cell_border
        col_letter = get_column_letter(c_idx)
        ws.column_dimensions[col_letter].width = COL_WIDTHS.get(c_idx, 20)
        
    # Enable Autofilter
    max_col_letter = get_column_letter(len(COLUMNS))
    ws.auto_filter.ref = f"A1:{max_col_letter}{len(cases)+1}"
    
    # Freeze header
    ws.freeze_panes = "A2"
    
    # Data Validation Dropdowns
    dv_status = DataValidation(type="list", formula1='"Pass,Fail,Blocked,Not Executed"', allow_blank=True)
    dv_priority = DataValidation(type="list", formula1='"P0,P1,P2,P3"', allow_blank=True)
    ws.add_data_validation(dv_status)
    ws.add_data_validation(dv_priority)
    
    center_cols = {1, 2, 5, 6, 14, 16, 23, 24, 25, 26}
    
    for r_idx, tc in enumerate(cases, 2):
        ws.row_dimensions[r_idx].height = 24
        fill = zebra_fill if (r_idx % 2 == 0) else white_fill
        
        for c_idx, col_name in enumerate(COLUMNS, 1):
            val = tc.get(col_name, "")
            cell = ws.cell(row=r_idx, column=c_idx, value=val)
            cell.fill = fill
            cell.font = data_font
            cell.border = cell_border
            
            if c_idx in center_cols:
                cell.alignment = align_center
            else:
                cell.alignment = align_left
                
            # Priority color coding
            if col_name == "Priority":
                p_val = str(val).strip().upper()
                if p_val == "P0":
                    cell.fill = p0_fill
                    cell.font = p0_font
                elif p_val == "P1":
                    cell.fill = p1_fill
                    cell.font = p1_font
                elif p_val == "P2":
                    cell.fill = p2_fill
                    cell.font = p2_font
                elif p_val == "P3":
                    cell.fill = p3_fill
                    cell.font = p3_font
                    
            # Status color coding
            if col_name in ["API Test Status", "Database Test Status", "Overall Test Status"]:
                s_val = str(val).strip().lower()
                if s_val == "pass":
                    cell.fill = pass_fill
                    cell.font = pass_font
                    
            if col_name == "Test Case ID":
                cell.font = data_font_bold

    # Apply dropdowns to columns
    last_row = max(len(cases) + 1, 2)
    dv_status.add(f"W2:W{last_row}") # API Test Status
    dv_status.add(f"X2:X{last_row}") # Database Test Status
    dv_status.add(f"Y2:Y{last_row}") # Overall Test Status
    dv_priority.add(f"Z2:Z{last_row}") # Priority

print("Sheet formatter ready.")
