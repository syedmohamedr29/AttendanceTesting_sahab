import sys
import openpyxl
from collections import defaultdict
import re

sys.stdout.reconfigure(encoding='utf-8')

wb = openpyxl.load_workbook('AttendanceTestCases_Master_Consolidated.xlsx', data_only=True)

print("Workbook sheets:", wb.sheetnames)

# Trackers
# 1. TC IDs per sheet
sheet_tc_ids = defaultdict(list)
all_tc_ids = defaultdict(list) # tc_id -> list of (sheet, row)

# 2. Test scenarios per sheet
sheet_scenarios = defaultdict(list)
all_scenarios = defaultdict(list) # normalized_scenario -> list of (sheet, row, tc_id, original_text)

for sheet_name in wb.sheetnames:
    if sheet_name == 'INDEX':
        continue
    ws = wb[sheet_name]
    
    # Find column indices for TC ID and Scenario
    header_row = [str(ws.cell(1, c).value or '').strip() for c in range(1, ws.max_column+1)]
    
    tc_id_col = 1
    scen_col = 3 # default in many sheets
    
    for idx, h in enumerate(header_row, 1):
        h_lower = h.lower()
        if 'tc' in h_lower or 'id' in h_lower or 'test case' in h_lower or 'code' in h_lower:
            if tc_id_col == 1:
                tc_id_col = idx
        if 'scenario' in h_lower or 'test' in h_lower or 'title' in h_lower or 'description' in h_lower:
            if idx != tc_id_col:
                scen_col = idx
                break
                
    # Loop rows
    for r in range(2, ws.max_row+1):
        tc_id_val = ws.cell(r, tc_id_col).value
        scen_val = ws.cell(r, scen_col).value
        
        tc_id_str = str(tc_id_val).strip() if tc_id_val is not None else ""
        scen_str = str(scen_val).strip() if scen_val is not None else ""
        
        if not tc_id_str and not scen_str:
            continue
            
        if tc_id_str:
            sheet_tc_ids[sheet_name].append((tc_id_str, r))
            all_tc_ids[tc_id_str].append((sheet_name, r))
            
        if scen_str:
            # Normalized scenario: lower, remove punctuation/extra whitespace
            norm_scen = re.sub(r'\s+', ' ', re.sub(r'[^\w\s]', '', scen_str.lower())).strip()
            if len(norm_scen) > 10: # Only check meaningful descriptions
                sheet_scenarios[sheet_name].append((scen_str, norm_scen, r, tc_id_str))
                all_scenarios[norm_scen].append((sheet_name, r, tc_id_str, scen_str))

print("\n" + "="*70)
print("1. DUPLICATE TC IDs WITHIN THE SAME SHEET")
print("="*70)
intra_sheet_id_dups = []
for sheet_name, id_list in sheet_tc_ids.items():
    counts = defaultdict(list)
    for tc_id, r in id_list:
        counts[tc_id].append(r)
    for tc_id, rows in counts.items():
        if len(rows) > 1:
            intra_sheet_id_dups.append((sheet_name, tc_id, rows))
            print(f"Sheet '{sheet_name}': TC ID '{tc_id}' duplicated on rows {rows}")

if not intra_sheet_id_dups:
    print("✓ None found! All TC IDs within individual sheets are unique.")

print("\n" + "="*70)
print("2. DUPLICATE TC IDs ACROSS DIFFERENT SHEETS")
print("="*70)
inter_sheet_id_dups = []
for tc_id, occurrences in all_tc_ids.items():
    sheets = set(s for s, r in occurrences)
    if len(sheets) > 1:
        inter_sheet_id_dups.append((tc_id, occurrences))
        print(f"TC ID '{tc_id}' appears in multiple sheets: {occurrences}")

if not inter_sheet_id_dups:
    print("✓ None found! All TC IDs are unique across all sheets.")

print("\n" + "="*70)
print("3. EXACT DUPLICATE SCENARIOS WITHIN THE SAME SHEET")
print("="*70)
intra_sheet_scen_dups = []
for sheet_name, scen_list in sheet_scenarios.items():
    counts = defaultdict(list)
    for orig, norm, r, tc_id in scen_list:
        counts[norm].append((r, tc_id, orig))
    for norm, items in counts.items():
        if len(items) > 1:
            intra_sheet_scen_dups.append((sheet_name, norm, items))
            print(f"Sheet '{sheet_name}': Duplicate scenario found in {len(items)} rows:")
            for r, tc_id, orig in items:
                print(f"   Row {r} (TC: {tc_id}): {orig[:90]}")

if not intra_sheet_scen_dups:
    print("✓ None found! All scenarios within individual sheets are distinct.")

print("\n" + "="*70)
print("4. EXACT DUPLICATE SCENARIOS ACROSS DIFFERENT SHEETS")
print("="*70)
inter_sheet_scen_dups = []
for norm, items in all_scenarios.items():
    sheets = set(s for s, r, tc, orig in items)
    if len(sheets) > 1:
        inter_sheet_scen_dups.append((norm, items))
        print(f"Scenario appears in {len(sheets)} different sheets:")
        for s, r, tc, orig in items:
            print(f"   Sheet '{s}', Row {r} (TC: {tc}): {orig[:80]}")

if not inter_sheet_scen_dups:
    print("✓ None found! No duplicate scenarios across different sheets.")

